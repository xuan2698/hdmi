"""Audit published proxy availability without loading any evaluation inputs."""

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CORRECTBENCH = "a2dcd36097b9416fd48dece8c2801401425dfcd1"
DATA_PREFIX = "data/HDLBits/HDLBits_data_RTL_"
MODELS = ("4o", "4omini", "sonnet35")
TOOLS = {
    "yosys": ("-V",),
    "sby": ("--version",),
    "boolector": ("--version",),
    "z3": ("--version",),
    "iverilog": ("-V",),
}


def correctbench_git(checkout, *args):
    return subprocess.check_output(["git", "-C", str(checkout), *args])


def write_csv(output, name, fields, rows):
    with (output / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def inventory(checkout, tasks):
    index = {}
    audits = []
    names = {task.split("_", 2)[-1].casefold() for task in tasks}
    published = correctbench_git(checkout, "ls-tree", "-r", "--name-only", CORRECTBENCH, "data")
    data_files = {line for line in published.decode().splitlines() if line.startswith(DATA_PREFIX)}
    expected = {f"{DATA_PREFIX}{model}_20.jsonl" for model in MODELS}
    if data_files != expected:
        raise ValueError("Pinned CorrectBench proxy inventory differs from the expected published release")
    for model in MODELS:
        file = f"{DATA_PREFIX}{model}_20.jsonl"
        raw = correctbench_git(checkout, "show", f"{CORRECTBENCH}:{file}")
        entries = [json.loads(line) for line in raw.splitlines() if line.strip()]
        by_id = {entry["task_id"]: len(entry["llmgen_RTL"]) for entry in entries}
        if len(by_id) != len(entries):
            raise ValueError(f"Duplicate task IDs in {file}")
        index[model] = by_id
        audits.append({
            "family": model,
            "source_path": file,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "tasks": len(by_id),
            "rtl_entries": sum(by_id.values()),
            "cvdp_prefix_ids": sum(key.casefold().startswith("cvdp_") for key in by_id),
            "exact_development_matches": len(set(tasks) & set(by_id)),
            "stripped_development_matches": len(names & {key.casefold() for key in by_id}),
        })
    return index, audits


def tool_status():
    rows = []
    for name, args in TOOLS.items():
        try:
            completed = subprocess.run([name, *args], capture_output=True, text=True, timeout=15)
        except FileNotFoundError:
            rows.append({"tool": name, "status": "missing", "version": ""})
        except subprocess.TimeoutExpired:
            rows.append({"tool": name, "status": "version_timeout", "version": ""})
        else:
            lines = (completed.stdout + "\n" + completed.stderr).strip().splitlines()
            rows.append({"tool": name, "status": "available" if completed.returncode == 0 else "version_error",
                         "version": lines[0] if lines else ""})
    return rows


def run(checkout, output):
    split_path = REPO / "stimulus-v1" / "split.json"
    tasks = json.loads(split_path.read_text())["development"]
    if len(tasks) != 10 or len(set(tasks)) != 10:
        raise ValueError("Expected the fixed ten development IDs")
    output.mkdir(parents=True, exist_ok=True)
    index, audits = inventory(checkout, tasks)
    tools = tool_status()
    tasks_rows = []
    for task in tasks:
        counts = {model: index[model].get(task, 0) for model in MODELS}
        tasks_rows.append({"task": task, **counts, "proxy_rtl_rows": sum(counts.values()),
                           "prerequisite": "matched_id" if any(counts.values()) else "missing_published_proxy"})
    pairs = 0
    if any(row["prerequisite"] == "matched_id" for row in tasks_rows):
        raise ValueError("The audited release has a task match that requires proxy provenance validation")
    write_csv(output, "correctbench_inventory.csv", tuple(audits[0]), audits)
    write_csv(output, "toolchain.csv", ("tool", "status", "version"), tools)
    write_csv(output, "stage0_tasks.csv", tuple(tasks_rows[0]), tasks_rows)
    write_csv(output, "stage0_pairs.csv",
              ("task", "proxy", "G", "depth", "solver", "category", "seconds"), [])
    categories = ("parse_or_elab_failure", "unsupported_syntax", "bounded_equivalent", "timeout",
                  "conversion_failure", "reset_mismatch", "other")
    write_csv(output, "stage0_categories.csv", ("category", "unit", "count"),
              [{"category": "missing_published_proxy", "unit": "task", "count": len(tasks_rows)},
               *({"category": category, "unit": "attempted_pair", "count": 0} for category in categories)])
    write_csv(output, "stage0_gate.csv",
              ("status", "missing_proxy_tasks", "pairs_attempted", "success_rate",
               "required_success_rate", "repair_rounds", "stage1_runs", "oracle_runs", "model_calls"),
              [{"status": "blocked_missing_published_proxy", "missing_proxy_tasks": len(tasks),
                "pairs_attempted": pairs, "success_rate": "", "required_success_rate": 0.70,
                "repair_rounds": 0, "stage1_runs": 0, "oracle_runs": 0, "model_calls": 0}])
    print(f"CorrectBench {CORRECTBENCH}: 0 matching proxy tasks of {len(tasks)}. Stage 0 input blocked.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("correctbench_checkout", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports")
    arguments = parser.parse_args()
    run(arguments.correctbench_checkout, arguments.output)
