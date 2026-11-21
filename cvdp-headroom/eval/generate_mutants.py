"""Create held-out realistic bug candidates using the verified H-only model."""

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from designs import ROOT, config, design_code, load, save, select

sys.path.insert(0, str(ROOT.parent / "experiments" / "autobench-pilot"))
from pilot2_generate import request, settings


def parse(text):
    pattern = chr(96) * 3 + r"(?:json)?\s*\n(.*?)" + chr(96) * 3
    fenced = re.search(pattern, text, re.S)
    return json.loads(fenced[1] if fenced else text)["mutants"]


def apply_edits(code, edits):
    spans = []
    for patch in edits:
        old, new = patch["old"], patch["new"]
        if not old or new == old or code.count(old) != 1:
            raise ValueError("Quoted edit did not change exactly one original occurrence")
        start = code.index(old)
        spans.append((start, start + len(old), new))
    limit = len(code)
    for start, end, replacement in sorted(spans, reverse=True):
        if end > limit:
            raise ValueError("Quoted edits overlap in the original source")
        code = code[:start] + replacement + code[end:]
        limit = start
    return code


def apply_entry(code, entry):
    if not isinstance(entry["bug"], str) or not entry["bug"].strip() or not entry["edits"]:
        raise ValueError("Empty bug description or edit list")
    return apply_edits(code, entry["edits"]).rstrip() + "\n"


def generate(row, batch):
    root = ROOT / "eval" / "heldout" / row["id"]
    folder = root / f"batch{batch}"
    folder.mkdir(parents=True, exist_ok=True)
    plan = config()
    infer = {**settings(), **plan["mutant_inference"], "model": plan["mutant_model"], "max_tokens": 12000}
    assert infer["model"] in plan["mutant_model_priority"] and infer["model"] != plan["stimulus_model"]
    number = plan["mutants_per_task"] // plan["h_batches"]
    emphasis = ("state updates, protocol sequencing, enables, reset and event timing" if batch == 1 else
                "data selection, boundary conditions, bit widths, priority and interactions between datapath and control")
    code = design_code(row)
    prompt = f"""Create exactly {number} independent, realistic RTL bug mutants of the supplied reference.
Each mutant must be based on the original RTL and represent one plausible implementation mistake,
ideally a distinct behavior observable on an output after a legal input sequence. Use a compact and local
change, without changing the interface, synthesizability, testbench, or introducing any new files or system tasks.
Favor bugs in {emphasis}, where applicable. Avoid five interchangeable constant changes.
Output valid JSON only, with a top-level "mutants" array. Each entry has "bug" (a short plain description)
and "edits" (a list of objects with two JSON strings "old" and "new"). Each "old" must occur exactly once
verbatim in the supplied source, including whitespace. Prefer a single targeted replacement per mutant;
use multiple disjoint edits only when necessary to model one bug. No markdown.
Reference RTL for {row['dut_module_name']}:
{code}
"""
    answer = folder / "response.txt"
    try:
        if not answer.exists():
            answer.write_text(request(folder / "calls.jsonl", prompt, infer))
        results = parse(answer.read_text())
        if not isinstance(results, list) or len(results) != number:
            raise ValueError(f"Expected exactly {number} independent mutants")
    except (RuntimeError, ValueError, KeyError) as exc:
        save(folder / "status.json", {"status": "failed", "reason": str(exc)})
        print(row["id"], batch, "failed", flush=True)
        return
    for offset, entry in enumerate(results, 1):
        tag = f"H{(batch - 1) * number + offset:02d}"
        item = root / tag
        try:
            mutated = apply_entry(code, entry)
        except (ValueError, TypeError, KeyError) as exc:
            save(item / "mutation.json", {"status": "invalid_patch", "reason": str(exc), "raw": entry})
        else:
            save(item / "mutation.json", {"status": "materialized", **entry})
            (item / "rtl.sv").write_text(mutated)
    save(folder / "status.json", {"status": "complete", "returned": len(results)})
    print(row["id"], batch, "complete", flush=True)


def replace_duplicates(row):
    root = ROOT / "eval" / "heldout" / row["id"]
    plan = config()
    infer = {**settings(), **plan["mutant_inference"], "model": plan["mutant_model"], "max_tokens": 4000}
    code = design_code(row)
    paths = sorted(root.glob("H*/mutation.json"))
    seen = {}
    for path in paths:
        item = load(path)
        if item["status"] == "materialized":
            rtl = path.with_name("rtl.sv").read_text()
            if rtl not in seen:
                seen[rtl] = (path, item["bug"])
                continue
            reason = f"duplicate of {seen[rtl][0].parent.name}"
        else:
            reason = item["status"]
        where = path.parent
        prior = where / "original_mutation.json"
        if not prior.exists():
            save(prior, {**item, "replaced_because": reason})
        bugs = [load(other).get("bug", "") for other in paths if other != path]
        evidence = "\n".join(bug for bug in bugs if bug)
        prompt = f"""Create one plausible and distinct RTL bug in this reference design.
Do not change any interface, add system tasks, include files, or generate a testbench.
Choose a substantially different implementation mistake from these existing proposals:
{evidence}
Return JSON only as {{"mutants":[{{"bug":"short description","edits":[{{"old":"verbatim unique text","new":"replacement"}}]}}]}}.
The 'old' text must occur exactly once in this original RTL. Choose a change to an executable expression.
Reference RTL:
{code}"""
        for attempt in range(1, 3):
            try:
                cached = where / f"replacement_{attempt}.txt"
                if not cached.exists():
                    cached.write_text(request(where / "replacement_calls.jsonl", prompt, infer))
                new, = parse(cached.read_text())
                rtl = apply_entry(code, new)
                if rtl in seen or rtl.rstrip() == code.rstrip():
                    raise ValueError("Duplicate or unmodified RTL")
            except (RuntimeError, ValueError, TypeError, KeyError) as exc:
                save(where / f"replacement_{attempt}_error.json", {"reason": str(exc)})
            else:
                save(path, {"status": "materialized", **new, "replacement_attempt": attempt})
                path.with_name("rtl.sv").write_text(rtl)
                seen[rtl] = (path, new["bug"])
                print(row["id"], where.name, "replaced", reason, flush=True)
                break
        else:
            save(path, {"status": "invalid_patch", "reason": f"{reason}; replacement attempts exhausted"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    rows = select(args.dataset)
    jobs = [(row, batch) for row in rows for batch in range(1, config()["h_batches"] + 1)]
    with ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(lambda job: generate(*job), jobs))
        list(pool.map(replace_duplicates, rows))


if __name__ == "__main__":
    main()
