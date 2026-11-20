import argparse
import json
from pathlib import Path

from evaluation_io import read_table
from pilot_inputs import prepare, put_once

ROOT = Path(__file__).resolve().parent


def stage(sources, all_tasks=False):
    frozen = json.loads((ROOT / "selected_tasks.json").read_text())
    if all_tasks:
        data = sources / "AutoBench/data/HDLBits"
        types, rows = read_table(data, "circuit_type"), read_table(data, "data")
        fixed = {k["task_id"] for k in frozen}
        frozen += [{"task_id": k, "task_number": r["task_number"]} for k, r in
                   sorted(rows.items(), key=lambda item: item[1]["task_number"])
                   if types[k]["circuit_type"] == "SEQ" and k not in fixed]
    base = ROOT / "v2"
    prepare([r["task_id"] for r in frozen], base, sources, write_sample=False)
    put_once(base / ("all_tasks.json" if all_tasks else "initial_tasks.json"),
             json.dumps(frozen, indent=2) + "\n")
    return frozen


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=ROOT / "sources")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    stage(args.sources.resolve(), args.all)
