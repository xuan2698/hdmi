"""Replay frozen CVDP stimuli using the existing four-state harness."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data import CVDP, PLAN, REPO, interface, load, roster, save, vectors

sys.path[:0] = [str(REPO / "stimulus-v1"), str(CVDP / "eval"), str(CVDP)]
from hdl import bind_params
from replay import harness, prepare_vectors, rename, run


def gold_sources(dataset):
    import pyarrow.parquet as pq
    allowed = [task for group, task, seed in roster("full") if group == "B" and seed == PLAN["seeds"][0]]
    table = pq.read_table(dataset, columns=["id", "rtl_files"], filters=[("id", "in", allowed)])
    sources = {row["id"]: "\n\n".join(part["content"] for part in row["rtl_files"])
               for row in table.to_pylist()}
    if set(sources) != set(allowed):
        raise ValueError("Frozen CVDP evaluation dataset incomplete")
    return sources


def confirmed_h(task):
    audit = REPO / "equiv-audit"
    return {p.parent.name: audit / "eval/new" / task / p.parent.name / "rtl.sv"
            for p in sorted((audit / "reports/new_cases" / task).glob("*/result.json"))
            if load(p)["status"] == "non_equivalent"}


def parse_trace(text, cycles, outputs):
    width = sum(outputs.values())
    ref, other = [], []
    for line in text.splitlines():
        if not line.startswith("TRACE "):
            continue
        _, cycle, phase, gold, variant, _ = line.split()
        pos = len(ref)
        if int(cycle) != pos // 2 + 1 or int(phase) != 1 - pos % 2:
            raise ValueError("CVDP edge order changed")
        if len(gold) != width or len(variant) != width:
            raise ValueError("CVDP trace width changed")
        ref.append(unpack(gold, outputs))
        other.append(unpack(variant, outputs))
    if len(ref) != 2 * cycles:
        raise ValueError(f"CVDP produced {len(ref)} edges for {cycles} cycles")
    return ref, other


def unpack(bits, outputs):
    at = 0
    row = {}
    for output, width in outputs.items():
        row[output] = bits[at:at + width]
        at += width
    return row


def replay_pair(golden, other, ports, stimulus):
    with tempfile.TemporaryDirectory(prefix="dual-oracle-cvdp-") as temp:
        path = Path(temp)
        count = len(stimulus)
        bench = bind_params(harness(ports, count, "compare"), ports["top"], ports["parameters"])
        (path / "gold.sv").write_text(rename(golden, "cvdp_r_"))
        (path / "other.sv").write_text(rename(other, "cvdp_m_"))
        (path / "harness.sv").write_text(bench)
        prepare_vectors(path.parent, {path.name: stimulus}, ports)
        run(path, "iverilog", "-g2012", "-s", "replay", "-o", "sim.vvp", "gold.sv", "other.sv", "harness.sv")
        return parse_trace(run(path, "vvp", "sim.vvp"), count, ports["output"])


def disagreement(expected, actual, mask):
    return {n for n, bits in mask.items()
            if any(m in "01" and a != b for a, b, m in zip(expected[n], actual[n], bits, strict=True))}


def self_replay(dataset):
    refs = gold_sources(dataset)
    checks = []
    for group, task, seed in roster("full"):
        if group != "B":
            continue
        ports = interface(group, task)
        stimulus = vectors(group, task, seed, ports)
        expected, measured = replay_pair(refs[task], refs[task], ports, stimulus)
        known = sum(b in "01" for sample in expected for bits in sample.values() for b in bits)
        failed = sum(bool(disagreement(a, b, a)) for a, b in zip(expected, measured, strict=True))
        checks.append({"task": task, "seed": seed, "cycles": len(stimulus), "samples": len(expected),
                       "known_bits": known, "mismatching_samples": failed, "pass": bool(known) and failed == 0})
        print(task, seed, len(expected), known, failed, flush=True)
    report = {"status": "passed" if all(r["pass"] for r in checks) else "failed", "checks": checks}
    save(ROOT / "reports/cvdp_self_replay.json", report)
    if report["status"] != "passed":
        raise SystemExit("CVDP golden self-replay did not pass")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    self_replay(args.dataset)
