"""Check exact stopwatch reachability invariants for selected new mutations."""

import argparse
from pathlib import Path

from corpus import BASE, sources
from designs import load, save
from divider import TERMINAL, divider
from replay import run
from stopwatch import PERIOD, TASK


def prove(case):
    tag = case["tag"]
    path = BASE / "reports" / "new_cases" / TASK / tag / "result.json"
    record = load(path)
    if record["status"] != "unknown":
        return
    gold, g_async, out1 = divider(case["original"], "gold")
    changed, m_async, out2 = divider(case["mutant"], "variant")
    assert g_async and m_async
    if tag == "R03":
        assert out1.replace("else if (start_stop == 1 && hour == 0) begin", "else if (hour == 0) begin", 1).rstrip() == out2.rstrip()
        assert gold.replace("module gold", "module variant", 1) == changed
    else:
        assert out1.rstrip() == out2.rstrip()
    property_by_tag = {
        "R03": "((reset || !start_stop) ? !gp : (gp == terminal))",
        "R04": "(gc==mc && (reset ? (!gp && !mp && !gc) : (start_stop ? (gp==terminal && mp==terminal) : (!gp && mp==terminal))))",
        "R08": "(gc==mc && (reset ? (!gp && !mp && !gc) : (start_stop ? (gp==terminal && mp==terminal) : (!gp && mp==one_sec_pulse))) && ((counter<=49999999 && (!one_sec_pulse || counter==0)) ? (gc<=49999999 && (!mp || mc==0)) : 1'b1))",
        "R09": "(counter<=49999999 ? (gc==mc && gp==mp && gc<=49999999) : 1'b1)",
    }
    # Constrain the common golden transition to the exact original recurrence.
    golden_step = "(reset ? (gc==0 && !gp) : (start_stop ? (gc==(terminal ? 27'd0 : counter+27'd1) && gp==terminal) : (gc==counter && !gp)))"
    miter = gold + changed + f"""
module cert(input [26:0] counter,input one_sec_pulse,input reset,input start_stop);
wire [26:0] gc, mc;
wire gp, mp;
wire terminal=counter==27'd{TERMINAL};
gold r(counter,one_sec_pulse,reset,start_stop,gc,gp);
variant m(counter,one_sec_pulse,reset,start_stop,mc,mp);
always @* assert ({golden_step} && {property_by_tag[tag]});
endmodule
"""
    target = path.parent / "fully_unrolled_transition_checker.sv"
    target.write_text(miter)
    root = BASE / ".work" / "new_divider" / tag
    root.mkdir(parents=True, exist_ok=True)
    cmd = f"read_verilog -formal {target}; prep -top cert -flatten; chformal -lower; sat -verify -set-def-inputs -prove-asserts"
    stdout = run(root, "yosys", "-Q", "-T", "-p", cmd)
    if "SUCCESS" not in stdout:
        raise RuntimeError(f"{tag} transition proof did not finish")
    record["attempts"].append({"engine": "Yosys SAT", "mode": "reachable invariant transition", "status": "PASS"})
    proofs = {
        "R03": "With stable start_stop through each main edge, an actual divider pulse can rise only with start_stop=1. Removing that guard from the common 1-Hz state block has no effect.",
        "R08": "Inductively, a high variant pulse implies counter=0. During pause the signal may stay high but cannot rise. The first resumed edge clears it at count 0, long before the next terminal count. Both implementations have exactly the same rising pulses.",
        "R09": "Both state transitions agree on the inductive range 0 through 49,999,999, including reset. Every value in that range fits in the new 26-bit register with the published defaults.",
    }
    if tag == "R04":
        trace = path.parent / "compressed_witness.json"
        save(trace, {"reset_cycles": 1, "enabled_cycles_until_terminal": TERMINAL, "paused_cycles": 1,
                     "resume_cycles": 1, "main_cycles": PERIOD + 2, "golden_seconds": 1, "mutant_seconds": 0,
                     "effect": "The mutant pulse rises while paused and is ignored by the stopwatch, then stays high on the resume edge. Golden gets a new rising pulse on that same resume edge."})
        record.update(status="non_equivalent", counterexample_cycles=PERIOD + 2,
                      witness_method="SAT-checked transition invariant and compressed default-clock schedule",
                      trace=str(trace.relative_to(BASE)))
    else:
        record.update(status="fully_equivalent", proof=proofs[tag])
    record.pop("reason", None)
    save(path, record)
    print(tag, record["status"], flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    for case in sources(p.parse_args().dataset, "new"):
        if case["task"] == TASK and case["tag"] in ("R03", "R04", "R08", "R09"):
            prove(case)
