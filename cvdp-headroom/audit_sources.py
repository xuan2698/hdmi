"""Verify public task artifacts and draw a reproducible sample from measured coverage."""

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
COMMENTS = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
SEQUENTIAL = re.compile(r"\balways(?:_ff)?\s*@\s*\([^)]*\b(?:posedge|negedge)\b", re.I)
FUNCTIONAL = re.compile(r"\b(?:covergroup|coverpoint|cover\s+(?:property|sequence))\b", re.I)
SV_EXTENSIONS = (".sv", ".svh", ".v", ".vh")


def contains_coverage(files):
    return sorted(name for name, source in files.items()
                  if name.lower().endswith(SV_EXTENSIONS)
                  and FUNCTIONAL.search(COMMENTS.sub("", source)))


def candidate_inventory(parquet, originals):
    frame = pq.read_table(parquet)
    original_by_task = {}
    for original in originals:
        with original.open() as stream:
            for line in stream:
                row = json.loads(line)
                harness = row["harness"]
                original_by_task[row["id"]] = harness.get("files", harness)
    items = []
    for row in sorted(frame.to_pylist(), key=lambda r: r["id"]):
        rtl = {f["name"]: f["content"] for f in row["rtl_files"]}
        harness = original_by_task.get(row["id"])
        items.append({
            "task_id": row["id"], "dut_module": row["dut_module_name"],
            "edge_triggered_rtl": any(SEQUENTIAL.search(COMMENTS.sub("", source)) for source in rtl.values()),
            "ecov_rtl_files": len(rtl), "ecov_spec_files": len(row["spec_files"]),
            "target_metrics": "|".join(t["metric"] for t in row["targets"]),
            "matched_original_harness": harness is not None,
            "original_imc_report_file": bool(harness and any(name.endswith("/coverage.cmd") for name in harness)),
            "ecov_functional_sources": "|".join(contains_coverage(rtl)),
            "original_functional_sources": "|".join(contains_coverage(harness or {})),
        })
    metadata = {
        "sha256": hashlib.sha256(parquet.read_bytes()).hexdigest(),
        "dataset_columns": frame.column_names,
        "public_tasks": len(items),
        "tasks_with_edge_triggered_rtl": sum(row["edge_triggered_rtl"] for row in items),
        "tasks_matched_to_original_harness": sum(row["matched_original_harness"] for row in items),
        "original_harnesses_with_imc_report_command": sum(row["original_imc_report_file"] for row in items),
        "ecov_tasks_with_functional_sources": sum(bool(row["ecov_functional_sources"]) for row in items),
        "original_harnesses_with_functional_sources": sum(bool(row["original_functional_sources"]) for row in items),
        "targets": dict(sorted(Counter(t for row in items for t in row["target_metrics"].split("|") if t).items())),
    }
    return items, metadata


def draw(items, measured, plan):
    """Read one functional percent per configured seed, with its coverage model identifier."""
    known = {row["task_id"] for row in items if row["edge_triggered_rtl"]}
    measures = defaultdict(dict)
    models = {}
    for row in measured:
        task, model = row["task_id"], row["coverage_model"].strip()
        seed, cycles = int(row["seed"]), int(row["cycles"])
        percent = float(row["functional_percent"])
        if task not in known or not model or not 0 <= percent <= 100:
            raise ValueError(f"Invalid functional coverage record for {task}")
        if cycles != plan["random_cycles"] or seed not in plan["random_seeds"] or seed in measures[task]:
            raise ValueError(f"Invalid cycle count or seed for {task}")
        if models.setdefault(task, model) != model:
            raise ValueError(f"Functional coverage model changed between seeds for {task}")
        measures[task][seed] = percent
    seeds = plan["random_seeds"]
    candidates = [{"task_id": task, "coverage_model": models[task],
                   "long_random_functional_percent_by_seed": {seed: values[seed] for seed in seeds},
                   "long_random_functional_percent_mean": mean(values.values())}
                  for task, values in sorted(measures.items()) if set(values) == set(seeds)]
    if len(candidates) < plan["selection_count"]:
        raise ValueError(f"Only {len(candidates)} tasks have complete functional coverage measurements")
    low = [row for row in candidates if row["long_random_functional_percent_mean"] < plan["nonsaturation_cutoff_percent"]]
    high = [row for row in candidates if row not in low]
    rng = random.Random(plan["selection_seed"])
    n = min(len(low), plan["selection_count"])
    selected = rng.sample(low, n) + rng.sample(high, plan["selection_count"] - n)
    return {"selection_seed": plan["selection_seed"], "complete_candidates": len(candidates),
            "below_cutoff_candidates": len(low), "selected": selected}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parquet", type=Path)
    parser.add_argument("--original", type=Path, nargs="*", default=[])
    parser.add_argument("--coverage-runs", type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "reports")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    plan = json.loads((HERE / "protocol.json").read_text())
    items, metadata = candidate_inventory(args.parquet, args.original)
    with (args.output / "dataset_inventory.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=items[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(items)
    write_json(args.output / "dataset_audit.json", metadata)
    if args.coverage_runs:
        with args.coverage_runs.open(newline="") as stream:
            selected = draw(items, csv.DictReader(stream), plan)
        write_json(args.output / "selection.json", selected)


if __name__ == "__main__":
    main()
