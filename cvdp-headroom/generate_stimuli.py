"""Generate A0 stimulus in one model response per sample using only public sources."""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from designs import ROOT, config, design_code, interface, save, select

sys.path.insert(0, str(ROOT.parent / "experiments" / "autobench-pilot"))
from pilot2_generate import request, settings
from pilot3_generate import driver_rows


def stimulus(row, seed):
    location = ROOT / "generation" / row["id"] / str(seed)
    if (location / "status.json").exists():
        return
    location.mkdir(parents=True, exist_ok=True)
    plan = config()
    ports = interface(row)
    infer = settings()
    infer["model"] = plan["stimulus_model"]
    infer["transport"] = {**infer["transport"], "retry_truncation": False}
    public_spec = "\n\n".join(f["content"] for f in row["spec_files"]) or row["instruction"]
    prompt = f"""Generate input-only stimulus for this Verilog design. Return only Python source defining
stimulus(rng, cycles), under 75 lines with no imports, printing, external files, or checks.
Use the public spec and reference RTL. Seek broad behavior and corners using directed patterns,
meaningful temporal sequences, and seeded random exploration. Do not attempt to modify the design.
Return a list of exactly cycles dicts. Each row assigns every non-clock input as a nonnegative integer
less than 2**width. The main clock makes one full cycle per row. A row may include a 'mid' dict
of changes to some input ports between the positive and negative edges. Mid changes hold until the next row.
Inputs and widths: {ports['input']}. Clock: {ports['clock']}. Reset polarities: {ports['resets']}.
The caller uses {plan['stimulus_cycles']} cycles and seed {seed}. Use compact loops and rng methods.
Public spec:
{public_spec}

Reference RTL:
{design_code(row)}
"""
    code_path = location / "stimulus.py"
    try:
        if not code_path.exists():
            code_path.write_text(request(location / "calls.jsonl", prompt, infer))
        vectors = driver_rows(code_path.read_text(), ports["input"], seed, plan["stimulus_cycles"])
        save(location / "vectors.json", vectors)
    except (RuntimeError, ValueError) as exc:
        save(location / "status.json", {"status": "failed", "reason": str(exc)})
    else:
        save(location / "status.json", {"status": "complete", "cycles": len(vectors)})
    print(row["id"], seed, (location / "status.json").read_text().splitlines()[1].strip(), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    rows = select(args.dataset)
    jobs = [(row, seed) for row in rows for seed in config()["stimulus_seeds"]]
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda job: stimulus(*job), jobs))


if __name__ == "__main__":
    main()
