import re
from dataclasses import asdict
from itertools import combinations

from mutations import Candidate, candidate, diagnostic, proposals
from pilot2_generate import BASE, load, save
from pilot2_screen_vectors import random_rows
from pilot2_sim import VectorReplay
from simulate import RunError, differences


def edit(source, mutation):
    result = source
    for atom in mutation["edits"]:
        result = candidate(atom).rtl(result)
    return result


def temporal_edits(source):
    names = r"(?:(?:a|s)?reset(?:n|_n)?|rst(?:n|_n)?|ar)"
    for index, line in enumerate(source.splitlines(), start=1):
        for point in re.finditer(r"\b(posedge|negedge)\s+(\w+)", line):
            edge, signal = point.groups()
            other = "negedge" if edge == "posedge" else "posedge"
            revised = line[:point.start(1)] + other + line[point.end(1):]
            yield Candidate("clock_edge", index, line, revised, edge, other, "1'b1", "", 1)
        asynchronous = re.search(rf"\s*(?:or|,)\s*(?:pos|neg)edge\s+{names}\b", line, re.I)
        if asynchronous:
            revised = line[:asynchronous.start()] + line[asynchronous.end():]
            yield Candidate("temporal_reset", index, line, revised, "1'b1", "1'b0", "1'b1", "", 1)
        control = re.search(rf"\bif\s*\(([^()]*(?:{names}|enable|ena)[^()]*)\)", line, re.I)
        if control:
            condition = control[1]
            for replacement in (f"!({condition})", "1'b0", "1'b1"):
                revised = line[:control.start(1)] + replacement + line[control.end(1):]
                yield Candidate("temporal_control", index, line, revised, condition,
                                replacement, "1'b1", "", 1)


def unique_edits(items):
    seen = set()
    for atom in items:
        key = atom.line, atom.after
        if key not in seen:
            yield atom
            seen.add(key)


def screen(items, original, screening, baseline, *, take, prefix, attempt_limit):
    variants, invalid = [], []
    attempted = 0
    for atoms in items:
        attempted += 1
        specification = {"edits": [asdict(atom) for atom in atoms]}
        changed = edit(original, specification)
        try:
            observed = [bench.trace(changed)[0] for bench in screening]
        except (RunError, ValueError) as exc:
            invalid.append({**specification, "reason": str(exc)})
        else:
            count = [len(differences(base, seen)) for base, seen in zip(baseline, observed, strict=True)]
            variants.append({**specification, "id": f"{prefix}-{len(variants) + 1:02d}",
                             "screen_differences": count, "retained": any(count)})
        if len(variants) >= take or attempted >= attempt_limit:
            break
    return {"candidates": variants, "invalid": invalid, "attempted": attempted,
            "retained": sum(m["retained"] for m in variants)}


def build_catalog(task, problem, interface, original, stimulus, plan):
    location = BASE / "guidance" / task / "catalog.json"
    if location.is_file():
        return load(location)
    inputs, outputs, _, _ = interface
    screening = [VectorReplay(interface, vectors, proxy_compat=True)
                 for vectors in random_rows(stimulus, problem, inputs, plan)]
    baseline = [bench.trace(original)[0] for bench in screening]
    basic = list(unique_edits(proposals(original, inputs, outputs)))
    temporal = list(unique_edits(temporal_edits(original)))
    seeds = list(unique_edits((*basic, *temporal)))
    initial = screen(((atom,) for atom in seeds), original, screening, baseline,
                     take=plan["initial_G_candidates"], prefix="G1", attempt_limit=150)
    initial_atoms = [candidate(row["edits"][0]) for row in initial["candidates"] if row["retained"]]
    extra = list(unique_edits((*initial_atoms, *temporal)))[:52]
    pairs = [(a, b) for a, b in combinations(extra, 2) if a.line != b.line]
    pairs.sort(key=lambda pair: (
        not (pair[0].lhs and pair[1].lhs and pair[0].lhs != pair[1].lhs),
        not any(x.rule.startswith(("clock", "temporal", "removed", "negated")) for x in pair),
        abs(pair[0].line - pair[1].line),
    ))
    single_extras = [(a,) for a in temporal if a not in seeds[:plan["initial_G_candidates"]]]
    groups = [initial]
    width = plan["new_G_candidates"]
    # Screen more than one batch once. Only a saturated run activates a new batch.
    advanced = screen(iter(single_extras + pairs), original, screening, baseline,
                      take=width * (plan["max_rounds"] - 1) + 16,
                      prefix="GX", attempt_limit=width * 9)
    retained = sorted((m for m in advanced["candidates"] if m["retained"]),
                      key=lambda m: (sum(m["screen_differences"]), m["id"]))
    groups.extend({"candidates": retained[i:i + width], "retained": len(retained[i:i + width])}
                  for i in range(0, min(len(retained), width * 4), width))
    result = {"task": task, "groups": groups, "advanced_screen": advanced,
              "initial_proposal_count": len(basic), "policy": "rarer differences first among harder edits",
              "proxy_enum_policy": "strict Icarus first, then width-preserving enum lowering"}
    save(location, result)
    return result


def exposure(mutations, original, bench, baseline):
    found = {}
    for mutation in mutations:
        rows, _ = bench.trace(edit(original, mutation))
        if differences(baseline, rows):
            found[mutation["id"]] = rows
    return found


def diagnostic_lines(mutations, original, bench, exposed_ids, method):
    lines, findings = [], {}
    for mutation in mutations:
        tag = mutation["id"]
        if tag in exposed_ids:
            continue
        atoms = mutation["edits"]
        edits = " | ".join(candidate(atom).feedback(tag) for atom in atoms)
        lines.append(edits)
        if method != "O":
            continue
        # Probe constituent sites on the common proxy prestate. A composite can
        # interact downstream, so retain separate observations for its sites.
        diagnoses = []
        for atom in atoms:
            try:
                finding = diagnostic(atom, original, bench)
            except (RunError, KeyError, ValueError) as exc:
                finding = {"label": "诊断未完成", "reason": str(exc).splitlines()[0]}
            diagnoses.append(finding)
        findings[tag] = diagnoses
        for finding in diagnoses:
            brief = finding["label"]
            if values := finding.get("operands_binary"):
                brief += " operands " + str(values)
            if intervals := finding.get("intervals"):
                brief += " " + str(intervals[:1])
            if reason := finding.get("cause") or finding.get("reason"):
                brief += " " + reason
            lines.append(brief)
    return "\n".join(lines), findings
