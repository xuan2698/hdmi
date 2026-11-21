"""Frozen public inputs and sandboxed stimulus-only generation."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
CVDP = REPO / "cvdp-headroom"
AUTO = REPO / "experiments" / "autobench-pilot"
sys.path.extend(map(str, (CVDP, CVDP / "eval", AUTO)))
import pyarrow.parquet as pq
from designs import design_code, interface, load, save
from pilot2_generate import request, settings
from pilot3_generate import driver_rows


def protocol():
    return load(ROOT / "protocol.json")


def public(dataset):
    want = load(CVDP / "reports" / "dataset_audit.json")["sha256"]
    if hashlib.sha256(Path(dataset).read_bytes()).hexdigest() != want:
        raise ValueError("Use the archived CVDP-ECov dataset revision")
    split = load(ROOT / "split.json")
    rows = pq.read_table(dataset, filters=[("id", "in", split["development"])]).to_pylist()
    if {row["id"] for row in rows} != set(split["development"]):
        raise ValueError("The dataset does not match the frozen development split")
    for row in rows:
        row["ports"] = {**interface(row), "parameters": split["parameters"][row["id"]]}
        row["gold"] = design_code(row)
    return rows


def digest(vectors):
    return hashlib.sha256(json.dumps(vectors, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def sample_path(task, seed):
    return ROOT / "trial" / task / str(seed)


def source_vectors(where, row, seed, cycles):
    status = load(where / "status.json")
    return driver_rows((where / status["source"]).read_text(), row["ports"]["input"], seed, cycles)


def get_vectors(where, row, seed, cycles):
    path = where / "vectors.json"
    vectors = load(path) if path.exists() else source_vectors(where, row, seed, cycles)
    if digest(vectors) != load(where / "status.json")["vector_sha256"]:
        raise ValueError(f"Stimulus checksum differs: {where}")
    return vectors


def generate(where, row, seed, *, evidence="", previous=""):
    plan = protocol()
    cycles = plan["round_cycles"]
    where.mkdir(parents=True, exist_ok=True)
    status = where / "status.json"
    if status.exists():
        if load(status)["status"] == "complete":
            return get_vectors(where, row, seed, cycles)
        return None
    spec = "\n\n".join(f["content"] for f in row["spec_files"])
    primary = f"""Generate ONLY executable Python function stimulus(rng, cycles) for RTL input stimulus.
Return code only. No imports, classes, prints, external state, HDL, output checking, or DUT reading.
Return exactly {cycles} ordered chronological dictionaries. Every row has all the non-clock ports and
unsigned integers in [0, 2**width). Optional 'mid' is a dict that overrides inputs AFTER the rising edge
and before the falling edge; those values persist until the start of the next row. Clock edges are provided.
Use loops and bounded-width arithmetic; use a valid reset sequence as needed and preserve long runs
where appropriate. Use the supplied rng for diversity, and strive to trigger behaviors in this spec.
Widths: {row['ports']['input']}. Active reset levels: {row['ports']['resets']}.
Fixed parameter bindings: {row['ports']['parameters']}. This input function must not change parameters.
Seed: {seed}. Keep the function under 85 source lines.
Public spec:
{spec}
Released RTL:
{row['gold']}
"""
    if evidence:
        primary += ("\nReturn only the new suffix. The preceding rows are immutable and will run first. "
                    "Use a reset when needed to start a clean directed scenario.\n"
                    "Guidance from compiled rule variants:\n" + evidence + "\n")
    if previous:
        primary += "\nPrevious stimulus function, for context:\n" + previous + "\n"
    infer = {**settings(), "model": plan["model"]}
    errors = []
    last = ""
    for attempt in range(plan["repair_limit"] + 1):
        source = where / f"try{attempt + 1}.py"
        prompt = primary
        if attempt:
            prompt += "\nRepair only the last generation failure: " + errors[-1] + "\nLast source:\n" + last
        try:
            if not source.exists():
                source.write_text(request(where / "calls.jsonl", prompt, infer))
            last = source.read_text()
            vectors = driver_rows(last, row["ports"]["input"], seed, cycles)
        except (RuntimeError, ValueError, TypeError) as error:
            errors.append(str(error)[-500:])
            continue
        save(where / "vectors.json", vectors)
        save(status, {"status": "complete", "source": source.name, "errors": errors, "seed": seed,
                      "cycles": len(vectors), "vector_sha256": digest(vectors)})
        return vectors
    save(status, {"status": "failed", "seed": seed, "errors": errors})
    return None
