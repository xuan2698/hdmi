"""Build the frozen G catalog from golden RTL and public rule operators."""

import argparse
import hashlib
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from itertools import zip_longest
from pathlib import Path

from common import ROOT, load, protocol, public, save
from hdl import WORK, compile_sim, input_dir, observe, reset_rows
from mutations import Candidate, proposals, signals
from pilot2_guidance import temporal_edits
from replay import SimulationError

ASSIGN = re.compile(r"^(\s*(?:(?:\w+|\d+'[bhd]\w+)\s*:\s*)?)(\w+(?:\[[^\]]+\])?)\s*(<=|=(?!=))\s*([^;]+);(.*)$")
IF = re.compile(r"\bif\s*\(([^()]+)\)")
SELECT = re.compile(r"\b(\w+)\[(\d+)(?::(\d+))?\]")
EVENT = re.compile(r"\b(always(?:_ff)?\s*@\()([^)]*)(\))")
RELATION = re.compile(r"(==|!=|<=|>=|<|>)\s*(\d+(?:'[bBdDhH][0-9a-fA-F_]+)?)\b")


def number(token):
    if "'" not in token:
        return int(token), ""
    width, digits = token.split("'")
    return int(digits[1:].replace("_", ""), {"b": 2, "d": 10, "h": 16}[digits[0].lower()]), width


def variants(row):
    source, ports = row["gold"], row["ports"]
    width = {**ports["input"], **ports["output"], **signals(source, ports["input"], ports["output"])}
    by_kind = defaultdict(list)
    for edit in (*proposals(source, ports["input"], ports["output"]), *temporal_edits(source)):
        by_kind[edit.rule].append(edit)
    recent_if = recent_case = -100
    for index, line in enumerate(source.splitlines(), 1):
        text = line.split("//", 1)[0]
        assign = ASSIGN.fullmatch(text)
        expr = IF.search(text)
        if expr:
            recent_if = index
        if re.search(r"\bcase[xz]?\s*\(", text):
            recent_case = index
        if re.search(r"\bendcase\b", text):
            recent_case = -100

        def add(rule, start, end, replacement, lhs="", bits=1):
            before = line[start:end].strip()
            changed = line[:start] + replacement + line[end:]
            if changed != line:
                by_kind[rule].append(Candidate(rule, index, line, changed, before, replacement,
                                               "1'b1", lhs, bits))

        if (ev := EVENT.search(text)) and re.search(r"\b(?:posedge|negedge)\b", ev[2]):
            for n, value in ports["resets"].items():
                if re.search(rf"\b{n}\b", ev[2]) is None:
                    add("EdgeInsert", ev.start(2), ev.end(2), f"{ev[2]} or {'posedge' if value else 'negedge'} {n}")
            for edge in re.finditer(r"(?:or|,)\s*(?:pos|neg)edge\s+\w+", ev[2]):
                add("EdgeDelete", ev.start(2)+edge.start(), ev.start(2)+edge.end(), "")
        group = (assign, 4) if assign else (expr, 1)
        m, g = group
        if not m:
            continue
        rhs = m[g]
        start = m.start(g)
        lhs = assign[2] if assign else ""
        bits = width.get(lhs, 1)
        for relation in RELATION.finditer(rhs):
            try:
                value, size = number(relation[2])
            except ValueError:
                continue
            for new in (value-1, value+1):
                if new >= 0 and (not size or new < 2**int(size)):
                    add("threshold_offset", start+relation.start(2), start+relation.end(2),
                        f"{size}'d{new}" if size else str(new), lhs, bits)
        for select in SELECT.finditer(rhs):
            name, hi, lo = select.groups()
            if lo is None:
                add("PointerUpdate", start+select.start(), start+select.end(), f"{name}[{int(hi)+1}]", lhs, bits)
                add("PointerDelete", start+select.start(), start+select.end(), name, lhs, bits)
            else:
                add("PartselectUpdate", start+select.start(), start+select.end(),
                    f"{name}[{int(hi)+1}:{int(lo)+1}]", lhs, bits)
                add("PartselectDelete", start+select.start(), start+select.end(), name, lhs, bits)
        for name in re.finditer(r"\b[A-Za-z_]\w*\b(?!\s*\[)", rhs):
            w = width.get(name[0], 0)
            span = start+name.start(), start+name.end()
            if w > 1:
                add("PointerInsert", *span, name[0] + "[0]", lhs, bits)
            if w > 2:
                add("PartselectInsert", *span, name[0] + f"[{w-2}:0]", lhs, bits)
            if name[0] in ports["input"]:
                add("IOFlip1", *span, f"(~{name[0]})", lhs, bits)
        if not assign:
            continue
        end = m.end(g)
        add("ExprInsert", start, end, f"({rhs}) ^ 1", lhs, bits)
        # Restrict removal/updates to simple two-operand expressions.
        infix = re.fullmatch(r"(\w+)\s*([&|^+*-])\s*(\w+)", rhs.strip())
        if infix:
            add("ExprDelete", start, end, infix[1], lhs, bits)
            add("ExprUpdate", start, end, f"{infix[1]} {'|' if infix[2] == '&' else '&'} {infix[3]}", lhs, bits)
        if lhs in ports["output"]:
            add("IOFlip2", start, end, f"~({rhs})", lhs, bits)
        op_rule = "AssignN2B" if m[3] == "<=" else "AssignB2N"
        add(op_rule, m.start(3), m.end(3), "=" if m[3] == "<=" else "<=", lhs, bits)
        if m[3] == "<=":
            add("NSubUpdate", start, end, f"({rhs}) + 1", lhs, bits)
            add("NSubDelete", m.start(2), text.rfind(";")+1, ";", lhs, bits)
            for family, limit in (("NSubInsert", True), ("NSubInsert_Case", recent_case > 0),
                                  ("NSubInsert_IF", index-recent_if < 8)):
                if limit:
                    add(family, m.start(2), text.rfind(";")+1, f"begin {lhs} <= {rhs}; {lhs} <= 0; end", lhs, bits)
    seen = set()
    seed = protocol()["G_seed"]
    for rule, edits in by_kind.items():
        edits.sort(key=lambda x: hashlib.sha256(f"{seed}:{rule}:{x.line}:{x.after}".encode()).digest())
    # Alternate public VeriBugBench operators and the retained original rules.
    upstream = ("Pointer", "Partselect", "Expr", "NSub", "Assign", "IO", "Edge")
    family = sorted(by_kind, key=lambda key: (not key.startswith(upstream), key))
    for batch in zip_longest(*(by_kind[k] for k in family)):
        for edit in batch:
            if edit is None or (edit.line, edit.after) in seen:
                continue
            seen.add((edit.line, edit.after))
            yield edit


def span(row, atom):
    return Candidate(**atom).rtl(row["gold"])


def catalog_path(task):
    return ROOT / "guidance" / task / "catalog.json"


def prepare(row):
    task = row["id"]
    path = catalog_path(task)
    if path.exists():
        return load(path)
    sample = reset_rows(row["ports"], protocol()["G_seed"], 12)
    where = input_dir(WORK / "preflight" / task, sample, row["ports"])
    control = observe(compile_sim(row["gold"], row["gold"], row["ports"]), where, len(sample))
    if control["samples"]:
        raise ValueError(f"Golden control unexpectedly disagrees in {task}")
    kept, failures = [], []
    for item in variants(row):
        if len(kept) == protocol()["G_per_task"]:
            break
        try:
            res = observe(compile_sim(row["gold"], item.rtl(row["gold"]), row["ports"]), where, len(sample))
        except (SimulationError, ValueError, RuntimeError) as exc:
            failures.append({"line": item.line, "rule": item.rule, "error": str(exc)[-330:]})
            continue
        kept.append({"id": f"G{len(kept)+1:02d}", "edit": asdict(item)})
    if not kept:
        raise ValueError(f"No rule G available for {task}")
    result = {"task": task, "candidates": kept, "excluded": failures}
    save(path, result)
    print(task, len(kept), "G", len(failures), "rejects", flush=True)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    args = p.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(prepare, public(args.dataset)))
