"""Retry inconclusive cases with word-level SMT, preserving the primary audit."""

import argparse
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from corpus import BASE, CYCLES, sources
from designs import load, save
from formal import abc_witness, accept_witness, config, concise_reason, execute, witness


def retry(case, cohort):
    dest = BASE / "reports" / f"{cohort}_cases" / case["task"] / case["tag"]
    record = load(dest / "result.json")
    if record["status"] != "unknown":
        return
    prior = BASE / ".work" / cohort / case["task"] / case["tag"]
    if record["attempts"][0]["status"] == "FAIL" and (evidence := abc_witness(case, prior / "bmc", dest, record["attempts"])):
        accept_witness(record, case, prior, dest, evidence, subset=record["address_subset"])
        if record["status"] == "non_equivalent":
            record.pop("reason", None)
            save(dest / "result.json", record)
            print(cohort, case["task"], case["tag"], "translated witness", flush=True)
            return
    root = prior / "smt_retry"
    root.mkdir(parents=True, exist_ok=True)
    subset = record["address_subset"]
    for name in ("golden.sv", "mutant.sv", "miter.sv", "assertion.sv"):
        code = (prior / name).read_text()
        if subset and name in ("golden.sv", "mutant.sv"):
            code = re.sub(r"(parameter\s+LINES\s*=\s*)8\b", r"\g<1>2", code)
        (root / name).write_text(code)
    if subset:
        # Keep the unused high address bits fixed in the witness, so the
        # reduced compile cannot generate an unintended high-address replay.
        assertion = root / "assertion.sv"
        code = assertion.read_text()
        assertion.write_text(code.replace("assume (permit && !permit_x);",
                             "assume (permit && !permit_x && in_addr_a[12:1]==0 && in_addr_b[12:1]==0);"))
    deep = case["required_cycles"] > CYCLES
    cfg = (config(32, mode="prove", engine="smtbmc boolector", timeout=12) if deep else
           config(4 * CYCLES + 1, engine="smtbmc boolector", timeout=16))
    label = "smt_retry"
    (dest / f"{label}.sby").write_text(cfg)
    status, work, text = execute(root, label, cfg)
    record["attempts"].append({"mode": "prove" if deep else "bmc", "engine": "smtbmc boolector",
                               "formal_steps": 32 if deep else 4 * CYCLES + 1,
                               "ram_addresses": 2 if subset else None, "status": status})
    if subset:
        shutil.copyfile(root / "assertion.sv", dest / "smt_retry_assertion.sv")
    if status == "FAIL":
        proof = witness(case, work, text, dest)
        accept_witness(record, case, root, dest, proof, subset=subset)
    elif status == "PASS" and not subset:
        record.pop("reason", None)
        record.update(status="fully_equivalent" if deep else "bounded_equivalent",
                      proof="SMTBMC Boolector k-induction" if deep else "bounded",
                      bounded_cycles=record["bounded_cycles"] if deep else CYCLES)
    else:
        record["supplemental_reason"] = (
            "Two-address search cannot prove equivalence of the full RAM" if subset and status == "PASS"
            else concise_reason(text))
    if record["status"] == "non_equivalent":
        record.pop("reason", None)
    save(dest / "result.json", record)
    print(cohort, case["task"], case["tag"], status, record["status"], flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cohort", choices=("old", "new"))
    p.add_argument("dataset", type=Path)
    p.add_argument("--only", action="append")
    p.add_argument("--workers", type=int, default=3)
    args = p.parse_args()
    cases = [c for c in sources(args.dataset, args.cohort) if not args.only
             or any(term in c["task"] for term in args.only)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda case: retry(case, args.cohort), cases))


if __name__ == "__main__":
    main()
