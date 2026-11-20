import argparse
import json
import random
from pathlib import Path

from pilot_inputs import prepare, put_once, score_proxies
from preflight import read_table

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=ROOT / "sources")
    args = parser.parse_args()
    cfg = json.loads((ROOT / "plan.json").read_text())
    sources = args.sources.resolve()
    paths = sources / "AutoBench/data/HDLBits"
    types = read_table(paths, "circuit_type")
    rows = read_table(paths, "data")
    seq = sorted((k for k, v in types.items() if v["circuit_type"] == "SEQ"),
                 key=lambda k: rows[k]["task_number"])
    assert len(seq) == 75
    selected = random.Random(cfg["sample_seed"]).sample(seq, cfg["sample_count"])
    put_once(ROOT / "selected_tasks.json", json.dumps([
        {"task_number": rows[k]["task_number"], "task_id": k} for k in selected
    ], indent=2) + "\n")
    pilot = selected[:cfg["pilot_count"]]
    prepare(pilot, ROOT, sources)
    score_proxies(ROOT, pilot)


if __name__ == "__main__":
    main()
