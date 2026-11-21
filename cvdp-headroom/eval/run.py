"""Evaluate archived A0 vectors against independent model-generated H mutants."""

import argparse
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from replay import SimulationError, compare, compile_pair, coverage, prepare_vectors, reset_rows

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from designs import ROOT, config, design_code, interface, load, save, select

sys.path.insert(0, str(ROOT.parent / "experiments" / "autobench-pilot"))
from pilot3_generate import driver_rows
from pilot2_sim import lower_proxy_enums


def exposure(evidence):
    return bool(evidence["known_difference_samples"])


def aggregate(kept, tags):
    results = {}
    for tag in tags:
        seen = [k for k, case in kept.items() if tag in case["runs"] and exposure(case["runs"][tag])]
        results[tag] = {"exposed": seen, "total": len(kept), "rate": len(seen) / len(kept) if kept else None}
    return results


def evaluate(row):
    plan = config()
    task = row["id"]
    base = ROOT / "eval" / "heldout" / task
    ports = interface(row)
    source = design_code(row)
    cycles = plan["random_cycles"]
    assert cycles == plan["stimulus_cycles"]
    baseline = [f"random_{seed}" for seed in plan["random_seeds"]]
    screening = [f"screen_{seed}" for seed in plan["screen_seeds"]]
    stimulus = {f"random_{seed}": reset_rows(ports, seed, cycles) for seed in plan["random_seeds"]}
    stimulus.update({f"screen_{seed}": reset_rows(ports, seed, cycles) for seed in plan["screen_seeds"]})
    a0 = {}
    failures = {}
    for seed in plan["stimulus_seeds"]:
        where = ROOT / "generation" / task / str(seed)
        tag = f"a0_{seed}"
        status_file = where / "status.json"
        if not status_file.exists() or load(status_file)["status"] != "complete":
            failures[tag] = load(status_file) if status_file.exists() else {"status": "missing"}
            continue
        vec = where / "vectors.json"
        a0[tag] = load(vec) if vec.exists() else driver_rows((where / "stimulus.py").read_text(),
                                                           ports["input"], seed, cycles)
    stimulus.update(a0)
    with tempfile.TemporaryDirectory(prefix="cvdp-eval-") as tmp:
        workspace = Path(tmp)
        prepare_vectors(workspace, stimulus, ports)
        gold = source
        policy = "original RTL"
        try:
            reference = compile_pair(workspace / "reference", gold, gold, ports, cycles)
        except SimulationError as exc:
            lowered = lower_proxy_enums(gold)
            if lowered == gold or "requires an explicit cast" not in str(exc):
                raise
            gold = lowered
            reference = compile_pair(workspace / "reference", gold, gold, ports, cycles)
            policy = "Icarus enum compatibility lowering"
        for tag in screening + baseline + list(a0):
            control = compare(reference, workspace / tag, cycles, ports["output"])
            if control["raw_difference_samples"] or control["golden_z_samples"]:
                raise SimulationError(f"{task} fails identical replay or uses golden Z: {tag}")
        cases = {}
        for i in range(1, plan["mutants_per_task"] + 1):
            tag = f"H{i:02d}"
            folder = base / tag
            if not (folder / "mutation.json").exists():
                cases[tag] = {"status": "missing_generation"}
                continue
            item = load(folder / "mutation.json")
            if item["status"] != "materialized":
                cases[tag] = {"status": item["status"], "reason": item["reason"]}
                continue
            if any(re.search(r"[`]|\$(?!signed\b|unsigned\b|clog2\b|bits\b)", part["new"])
                   for part in item["edits"]):
                cases[tag] = {"status": "unsupported_edit", "bug": item["bug"]}
                continue
            variant = (folder / "rtl.sv").read_text()
            if policy != "original RTL":
                variant = lower_proxy_enums(variant)
            try:
                sim = compile_pair(workspace / tag, gold, variant, ports, cycles)
            except SimulationError as exc:
                cases[tag] = {"status": "compile_failure", "reason": str(exc), "bug": item["bug"]}
                continue
            try:
                screen = {seed: compare(sim, workspace / seed, cycles, ports["output"]) for seed in screening}
                keep = any(map(exposure, screen.values()))
                if not keep:
                    status = ("scoring_equivalent" if any(x["raw_difference_samples"] for x in screen.values())
                              else "suspected_equivalent")
                    cases[tag] = {"status": status, "bug": item["bug"], "screen": screen}
                    continue
                measured = {seed: compare(sim, workspace / seed, cycles, ports["output"])
                            for seed in baseline + list(a0)}
            except SimulationError as exc:
                cases[tag] = {"status": "simulation_failure", "reason": str(exc), "bug": item["bug"]}
                continue
            cases[tag] = {"status": "kept", "bug": item["bug"], "screen": screen, "runs": measured}
        kept = {tag: item for tag, item in cases.items() if item["status"] == "kept"}
        try:
            cov = coverage(workspace / "coverage", source, ports, cycles,
                           {tag: workspace / tag for tag in baseline + list(a0)})
        except SimulationError as exc:
            cov = {"error": str(exc)}
        tests = aggregate(kept, baseline + list(a0))
        result = {"task": task, "simulator_policy": policy, "functional_coverage": "待补", "H": cases,
                  "runs": tests, "code_coverage": cov, "a0_failed_or_missing": failures}
    save(ROOT / "eval" / "results" / f"{task}.json", result)
    print(task, "kept", len(kept), "A0", len(a0), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--task", action="append")
    args = parser.parse_args()
    rows = [r for r in select(args.dataset) if not args.task or any(r["id"].endswith(t) for t in args.task)]
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(evaluate, rows))


if __name__ == "__main__":
    main()
