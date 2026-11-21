"""Load fixed H only after training has written all 200 development checkpoints."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import CVDP, REPO, ROOT, get_vectors, load, protocol, public, sample_path, save
from hdl import WORK, compile_sim, input_dir, observe, reset_rows

EQ = REPO / "equiv-audit"
GROUPS = ("original_plus", "rare")


def paths(row):
    task = row["id"]
    old_dir = CVDP / "eval" / "results"
    original = load(old_dir / f"{task}.json")
    old = {name for name, case in original["H"].items() if case["status"] == "kept"}
    old.update(p.parent.name for p in (EQ / "reports" / "old_cases" / task).glob("*/result.json")
               if load(p)["status"] == "non_equivalent")
    new = {p.parent.name for p in (EQ / "reports" / "new_cases" / task).glob("*/result.json")
           if load(p)["status"] in ("non_equivalent", "unknown")}
    return {"original_plus": {tag: CVDP / "eval" / "heldout" / task / tag / "rtl.sv" for tag in sorted(old)},
            "rare": {tag: EQ / "eval" / "new" / task / tag / "rtl.sv" for tag in sorted(new)}}


def binaries(row):
    out = {}
    for group, paths_by_tag in paths(row).items():
        out[group] = {tag: compile_sim(row["gold"], source.read_text(), row["ports"])
                      for tag, source in paths_by_tag.items()}
    return out


def events(row, paths_by_group, vectors, where, already=None):
    bins = input_dir(where, vectors, row["ports"])
    previous = already or {group: set() for group in GROUPS}
    outcome = {}
    for group, index in paths_by_group.items():
        outcome[group] = sorted(set(previous[group]) | {tag for tag, sim in index.items()
                                 if tag not in previous[group] and observe(sim, bins, len(vectors))["samples"]})
    return outcome


def replay_vectors(row, seed, config, rounds):
    plan = protocol()
    base = sample_path(row["id"], seed)
    rows = get_vectors(base / "initial", row, seed, plan["round_cycles"])
    for i in range(2, rounds + 1):
        rows = rows + get_vectors(base / config / f"round{i}", row, seed+i-1, plan["round_cycles"])
    return rows


def evaluate(row, replay=False):
    task = row["id"]
    report = ROOT / "evaluation" / task / "result.json"
    if report.exists() and not replay:
        return load(report)
    plan = protocol()
    matrix = binaries(row)
    totals = {group: len(matrix[group]) for group in GROUPS}
    root = WORK / "eval" / task
    baseline = {str(seed): events(row, matrix, reset_rows(row["ports"], seed, plan["max_cycles"]),
                                  root / f"baseline{seed}")
                for seed in plan["baseline_seeds"]}
    trials = []
    for seed in plan["seeds"]:
        base = sample_path(task, seed)
        a0 = load(base / "A0" / "result.json")
        initial = ({g: [] for g in GROUPS} if a0["status"] != "complete" else
                   events(row, matrix, replay_vectors(row, seed, "A0", 1), root / str(seed) / "shared"))
        for cfg in plan["configs"]:
            run = load(base / cfg / "result.json")
            last = run.get("last_round", 0)
            end = initial
            if last > 1:
                end = events(row, matrix, replay_vectors(row, seed, cfg, last), root / str(seed) / cfg,
                             {k: set(v) for k, v in initial.items()})
            trials.append({**run, "initial_H": initial, "final_H": end})
    out = {"task": task, "H_totals": totals, "baseline": baseline, "trials": trials}
    save(report, out)
    print(task, totals, "evaluation complete", flush=True)
    return out


def check_completion(rows):
    # Do not open any held-out file before this precondition passes.
    plan = protocol()
    if not all((sample_path(row["id"], seed) / cfg / "result.json").exists()
               for row in rows for seed in plan["seeds"] for cfg in plan["configs"]):
        raise ValueError("Finish the frozen generation checkpoint matrix before evaluating H")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    p.add_argument("--replay", action="store_true", help="recompute archived evaluation checkpoints")
    args = p.parse_args()
    rows = public(args.dataset)
    check_completion(rows)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda row: evaluate(row, args.replay), rows))
