import argparse
import hashlib
import json
from pathlib import Path

from evaluation_io import read_table
from pilot2_generate import atomic, load, save
from pilot2_sim import interface_from

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "v3"
PREVIOUS = ROOT / "v2"
MODEL_FILES = {
    "gpt4o": "data_RTL_4o_20",
    "gpt4omini": "data_RTL_4omini_20",
    "claude35sonnet": "data_RTL_sonnet35_20",
}


def setup():
    protocol = load(ROOT / "pilot3.json")
    old = load(ROOT / protocol["locked_inference"])
    return {**old, **protocol}


def fingerprint(plan):
    return hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()


def public(task):
    where = PREVIOUS / "generation" / task
    spec = load(where / "problem.json")
    return spec, interface_from(spec)


def tasks():
    path = BASE / "tasks.json"
    if path.exists():
        return load(path)
    rows = [item for item in load(PREVIOUS / "reports/selection.json")["candidates"]
            if item["eligibility"] == "retained"]
    if len(rows) != 17:
        raise ValueError(f"Expected 17 frozen retained tasks, found {len(rows)}")
    return [{"task_number": row["task_number"], "task_id": row["task_id"]} for row in rows]


def prepare(sources):
    selected = tasks()
    save(BASE / "tasks.json", selected)
    folder = sources / "CorrectBench/data/HDLBits"
    index = {family: read_table(folder, filename) for family, filename in MODEL_FILES.items()}
    for entry in selected:
        task = entry["task_id"]
        for family, library in index.items():
            for i, rtl in enumerate(library[task]["llmgen_RTL"][:3], 1):
                dest = BASE / "proxies" / task / f"{family}_{i}.v"
                if dest.exists() and dest.read_text() != rtl:
                    raise ValueError(f"An archived proxy changed: {dest}")
                atomic(dest, rtl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=ROOT / "sources")
    prepare(parser.parse_args().sources)
