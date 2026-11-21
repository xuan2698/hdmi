"""Use specialized search reductions only to obtain witnesses for original RTL replay."""

import argparse
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from corpus import BASE, CYCLES, sources
from designs import load, save
from formal import accept_witness, assertion, config, execute, module, reconstruct, sv_source, witness


def search(case, cohort):
    task, tag = case["task"], case["tag"]
    dest = BASE / "reports" / f"{cohort}_cases" / task / tag
    record = load(dest / "result.json")
    if record["status"] != "unknown":
        return
    root = BASE / ".work" / cohort / task / tag / "restricted_search"
    root.mkdir(parents=True, exist_ok=True)
    word = task.endswith("word_change_detector_0012")
    for name, text, prefix in (("golden", case["original"], "cvdp_r_"),
                               ("mutant", case["mutant"], "cvdp_m_")):
        if word:
            # The archived RTL has two processes driving change_pulse.
            # Drop the procedural reset assignment for finding candidates;
            # this model cannot prove behavior of the original circuit.
            text = re.sub(r"\bchange_pulse\s*<=\s*[^;]+;", "", text)
        (root / f"{name}.sv").write_text(sv_source(text, prefix))
    (root / "miter.sv").write_text(module(case["ports"]))
    claim = assertion(case["ports"])
    if not word:
        fixed = """
reg [2:0] age = 0;
always @($global_clock) if (age < 5) age <= age + 1;
always @* assume (in_i_rst_b == (age == 5) && in_i_enable && !in_i_fault && !in_i_clear &&
                  in_i_data_in == 16'hdead);
"""
        claim = claim.replace("endmodule", fixed + "endmodule")
    (root / "assertion.sv").write_text(claim)
    (dest / "restricted_assertion.sv").write_text(claim)
    engine = "abc bmc3" if word else "smtbmc boolector"
    cfg = config(4 * CYCLES + 1, engine=engine, timeout=14 if word else 35)
    (dest / "restricted_search.sby").write_text(cfg)
    status, job, text = execute(root, "bmc", cfg)
    scope = "mixed-driver search normalization" if word else "reset then fixed SPI transfer"
    record["attempts"].append({"mode": scope, "engine": engine, "status": status, "requested_cycles": CYCLES})
    if status == "FAIL":
        proof = (reconstruct(case, root, text, dest, record["attempts"], job=job) if word
                 else witness(case, job, text, dest))
        accept_witness(record, case, root, dest, proof, subset=False)
        if record["status"] == "non_equivalent":
            record["witness_method"] = scope + ", confirmed on unchanged Icarus RTL"
            record.pop("reason", None)
    save(dest / "result.json", record)
    print(task, tag, status, record["status"], flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    p.add_argument("--cohort", choices=("old", "new"), required=True)
    args = p.parse_args()
    suffix = "simple_spi_0003" if args.cohort == "old" else "word_change_detector_0012"
    cases = [r for r in sources(args.dataset, args.cohort) if r["task"].endswith(suffix)]
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda c: search(c, args.cohort), cases))
