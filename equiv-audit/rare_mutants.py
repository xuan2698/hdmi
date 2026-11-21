"""Generate a new, evaluation-only CVDP mutant cohort from the released RTL."""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parent
sys.path.extend(map(str, (REPO / "cvdp-headroom", REPO / "cvdp-headroom" / "eval",
                         REPO / "experiments" / "autobench-pilot")))
from designs import ROOT as CVDP, design_code, load, save
from generate_mutants import apply_entry, parse
from pilot2_generate import request, settings
import pyarrow.parquet as pq


def selected(dataset):
    tasks = {r["id"]: r for r in pq.read_table(dataset).to_pylist()}
    return [tasks[t["task_id"]] for t in load(CVDP / "reports" / "selection.json")["selected"]]


def run_task(row):
    task = row["id"]
    path = BASE / "eval" / "new" / task
    path.mkdir(parents=True, exist_ok=True)
    source = design_code(row)
    inference = {**settings(), "model": "gpt-6-luna", "thinking": None, "max_tokens": 13000}
    # Avoid byte-identical duplicates from the original H, without looking at its outcomes.
    seen = {f.read_text().rstrip() for f in (CVDP / "eval" / "heldout" / task).glob("H*/rtl.sv")}
    descriptions = []
    accepted = []
    for batch in range(1, 11):
        left = 10 - len(accepted)
        if not left:
            break
        count = min(5, left)
        plan = ("boundary values, counter wrap, deep sequential history, or precise protocol sequences" if batch % 2
                else "rare coincidence, terminal-state priority, exact data patterns, or a corner-case reset timing")
        prompt = f"""Create exactly {count} distinct realistic synthesizable RTL bug mutants of this original
design. Each bug should be latent in normal traffic and observable only under a genuinely specific condition.
Favor {plan}, where applicable. Use a single plausible implementation mistake per mutant.
Do not add artificial test-only triggers, long delay constructs, special system tasks, or new files.
Do not change the I/O or parameter defaults. Avoid reusing previous bug descriptions: {descriptions}.
Output JSON only with shape {{"mutants":[{{"bug":"summary","trigger":"exact state/input and history needed, with
a concrete example or terminal count when possible","effect":"observable consequence","edits":[{{"old":
"verbatim unique original text","new":"replacement"}}]}}]}}.
Each old span must appear exactly once in the original. Edits for a mutant must be disjoint. Every mutant
must start from the original. Avoid broad faults that change ordinary operation.
Reference RTL:
{source}
"""
        raw = path / f"batch{batch}.txt"
        if not raw.exists():
            try:
                raw.write_text(request(path / "calls.jsonl", prompt, inference))
            except RuntimeError as exc:
                save(path / f"batch{batch}_error.json", {"error": str(exc)})
                continue
        try:
            candidates = parse(raw.read_text())
        except (ValueError, KeyError) as exc:
            save(path / f"batch{batch}_error.json", {"error": str(exc)})
            continue
        for candidate in candidates:
            try:
                changed = apply_entry(source, candidate)
                if changed.rstrip() in seen or changed.rstrip() == source.rstrip():
                    continue
                if not candidate["trigger"].strip() or not candidate["effect"].strip():
                    continue
                if len(accepted) == 10:
                    break
            except (ValueError, TypeError, KeyError, AttributeError):
                continue
            seen.add(changed.rstrip())
            descriptions.append(candidate["bug"])
            name = f"R{len(accepted)+1:02d}"
            save(path / name / "mutation.json", {**candidate, "model": "gpt-6-luna", "batch": batch})
            (path / name / "rtl.sv").write_text(changed)
            accepted.append(name)
    save(path / "status.json", {"task": task, "candidates": accepted, "model": "gpt-6-luna"})
    print(task, len(accepted), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    args = p.parse_args()
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(run_task, selected(args.dataset)))
