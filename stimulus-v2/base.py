"""Inputs, checkpoints, and requests for the frozen v2 protocol."""

import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V1 = ROOT.parent / "stimulus-v1"
sys.path.insert(0, str(V1))

from common import digest, load, public, request, save, settings
from pilot2_generate import atomic
from pilot3_generate import driver_rows

WORK = ROOT / ".work"
FROZEN = "0a424d75cda2630745f724f13b8a9c139fab2395"


def plan():
    return load(ROOT / "protocol.json")


def trial(row, seed):
    return ROOT / "trial" / row["id"] / str(seed)


def vectors_at(where, row):
    status = load(where / "status.json")
    if status["status"] != "complete":
        return None
    cache = where / "vectors.json"
    if cache.exists():
        vectors = load(cache)
    else:
        code = (where / status["source"]).read_text()
        vectors = driver_rows(code, row["ports"]["input"], status["seed"], status["cycles"])
    if digest(vectors) != status["vector_sha256"]:
        raise ValueError(f"Archived stimulus checksum differs at {where}")
    return vectors


def generate(where, row, seed, cycles, *, feedback=None, previous=""):
    where.mkdir(parents=True, exist_ok=True)
    status = where / "status.json"
    if status.exists():
        return vectors_at(where, row)
    spec = "\n\n".join(part["content"] for part in row["spec_files"])
    ports = row["ports"]
    draft = f"""Generate ONLY executable Python function stimulus(rng, cycles) for RTL input stimulus.
Return code only. No imports, classes, prints, external state, HDL, output checking, or DUT reading.
Return exactly {cycles} ordered chronological dictionaries. Every row has all the non-clock ports and
unsigned integers in [0, 2**width). Optional 'mid' is a dict that overrides inputs AFTER the rising edge
and before the falling edge. Those values persist until the start of the next row. Clock edges are provided.
Use compact loops and bounded-width arithmetic, including resets and long runs as warranted by the spec.
Widths: {ports['input']}. Active reset levels: {ports['resets']}.
Fixed parameter bindings: {ports['parameters']}. This input function must not change parameters.
Seed: {seed}. Keep the function under 85 source lines.
Public spec:
{spec}
Released RTL:
{row['gold']}
"""
    if feedback is not None:
        draft += ("\nReturn only the new suffix. All previous rows are immutable and will run first.\n"
                  "Guidance from compiled rule variants:\n" + feedback + "\n"
                  "\nPrevious stimulus function, for context:\n" + previous + "\n")
    infer = {**settings(), "model": plan()["model"]}
    errors = []
    last = ""
    for attempt in range(plan()["repair_limit"] + 1):
        source = where / f"try{attempt+1}.py"
        prompt = draft if not errors else draft + "\nRepair this failure: " + errors[-1] + "\nLast source:\n" + last
        try:
            if not source.exists():
                atomic(source, request(where / "calls.jsonl", prompt, infer))
            last = source.read_text()
            vectors = driver_rows(last, ports["input"], seed, cycles)
        except (RuntimeError, ValueError, TypeError) as exc:
            errors.append(str(exc)[-500:])
            continue
        save(where / "vectors.json", vectors)
        save(status, {"status":"complete", "source":source.name, "errors":errors, "seed":seed,
                      "cycles":cycles, "vector_sha256":digest(vectors)})
        return vectors
    save(status, {"status":"failed", "errors":errors, "seed":seed, "cycles":cycles})
    return None


def initial(job):
    row, seed = job
    vectors = generate(trial(row, seed) / "initial", row, seed, plan()["max_cycles"])
    print(row["id"], seed, "complete" if vectors is not None else "failed", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    if not os.environ.get("OPENCODE_GO_API_KEY", "").strip():
        raise SystemExit("OPENCODE_GO_API_KEY is missing")
    jobs = [(row, seed) for seed in plan()["seeds"] for row in public(args.dataset)]
    with ThreadPoolExecutor(max_workers=14) as pool:
        list(pool.map(initial, jobs))
