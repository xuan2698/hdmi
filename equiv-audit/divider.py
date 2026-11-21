"""Exact transition certificates for the stopwatch's four divider mutations."""

import argparse
import re
from pathlib import Path

from corpus import BASE, sources
from designs import load, save
from replay import run
from stopwatch import MARK, PERIOD, TASK

TERMINAL = PERIOD - 1


def divider(source, name):
    prefix, mark, output_logic = source.partition(MARK)
    pre, clock_comment, process = prefix.partition("// Clock divider")
    match = re.search(r"always\s*@\(([^)]*)\)\s*begin(.*)\bend\s*$", process, re.S)
    if not mark or not clock_comment or not match:
        raise ValueError("Stopwatch divider source anchors changed")
    assert "localparam COUNTER_MAX = CLK_FREQ - 1" in pre
    width = 26 if "reg [$clog2(COUNTER_MAX)-1:0] counter;" in pre else 27
    if width == 27:
        assert "reg [$clog2(COUNTER_MAX):0] counter;" in pre
    assert re.search(r"parameter CLK_FREQ\s*=\s*50000000\b", pre)
    assert re.fullmatch(r"\s*posedge clk(?: or posedge reset)?\s*", match[1])
    body = re.sub(r"\b(counter|one_sec_pulse)\s*<=", r"next_\1 =", match[2])
    return f"""
module {name}(input [{width - 1}:0] counter, input one_sec_pulse, input reset, input start_stop,
              output reg [{width - 1}:0] next_counter, output reg next_one_sec_pulse);
localparam COUNTER_MAX={TERMINAL};
always @* begin
    next_counter=counter;
    next_one_sec_pulse=one_sec_pulse;
    {body}
end
endmodule
""", "or posedge reset" in match[1], output_logic


def prove(case):
    path = BASE / "reports" / "old_cases" / TASK / case["tag"] / "result.json"
    result = load(path)
    if result["status"] != "unknown":
        return
    tag = case["tag"]
    gold, gold_async, outs = divider(case["original"], "gold")
    mutant, gate_async, gate_outs = divider(case["mutant"], "variant")
    if outs.rstrip() != gate_outs.rstrip() or not gold_async:
        raise ValueError("Divider proof requires the unchanged exposed stopwatch state block")
    if gate_async != (tag != "H05"):
        raise ValueError("Unexpected reset event in divider proof")
    run_ref = "(gc == (terminal ? 27'd0 : counter + 27'd1) && gp == terminal)"
    run_mut = "(mc == (terminal ? 27'd0 : counter + 27'd1) && mp == terminal)"
    common = f"(reset ? (gc==0 && !gp) : (start_stop ? {run_ref} : (gc==counter && !gp)))"
    checks = {
        "H01": f"(reset ? (mc==0 && !mp) : (start_stop ? {run_mut} : (mc==0 && !mp)))",
        "H05": "(gc == mc && gp == mp)",
        "H06": "(reset ? (mc==0 && !mp) : ((start_stop && !counter[0]) ? (!mc[0] && !mp) : 1'b1))",
        "H07": f"(reset ? (mc==0 && !mp) : {run_mut})",
    }
    check = checks[tag]
    miter = gold + mutant + f"""
module cert(input [26:0] counter,input one_sec_pulse,input reset,input start_stop);
wire [26:0] gc, mc;
wire gp, mp;
wire terminal = counter == 27'd{TERMINAL};
gold g(counter,one_sec_pulse,reset,start_stop,gc,gp);
variant m(counter,one_sec_pulse,reset,start_stop,mc,mp);
always @* assert ({common} && {check});
endmodule
"""
    out = path.parent / "divider_certificate.sv"
    out.write_text(miter)
    here = BASE / ".work" / "divider" / tag
    here.mkdir(parents=True, exist_ok=True)
    script = f"read_verilog -formal {out}; prep -top cert -flatten; chformal -lower; sat -verify -set-def-inputs -prove-asserts"
    text = run(here, "yosys", "-Q", "-T", "-p", script)
    if "SUCCESS" not in text:
        raise RuntimeError(f"Divider transition certificate: {tag} did not prove")
    result["attempts"].append({"mode": "combinational transition certificate", "engine": "Yosys SAT", "status": "PASS"})
    schedules = {
            "H01": {"reset_cycles": 1, "enabled_cycles_before_pause": 1, "paused_cycles": 1,
                    "enabled_cycles_after_pause": TERMINAL,
                    "effect": "Golden holds a partial count while paused; the variant clears it and ticks a cycle later."},
            "H05": {"reset_cycles": 1, "enabled_cycles_before_async_reset_pulse": 1,
                    "inter_edge_reset_pulse": "assert and release reset between rising edges",
                    "enabled_cycles_after_pulse": TERMINAL,
                    "effect": "Variant holds its prior counter on the inter-edge reset pulse; its first 1-Hz tick arrives one cycle early."},
            "H06": {"reset_cycles": 1, "uninterrupted_enabled_cycles": PERIOD,
                    "effect": "The variant stays even from zero and cannot reach the odd terminal count; only golden emits a 1-Hz tick."},
            "H07": {"reset_cycles": 1, "paused_cycles": TERMINAL, "then_enabled_cycles": 1,
                    "effect": "Variant increments while paused; enabling at the terminal count makes only the variant tick."},
        }
    trace = path.parent / "compressed_witness.json"
    cycles = PERIOD + (2 if tag == "H01" else 1)
    golden_early = tag in ("H01", "H06")
    save(trace, {**schedules[tag], "main_cycles": cycles, "divider_period": PERIOD,
                 "output": "seconds", "golden_seconds": int(golden_early), "mutant_seconds": int(not golden_early)})
    result.update(status="non_equivalent", counterexample_cycles=cycles,
                  witness_method="SAT-checked transition invariant and compressed default-clock schedule",
                  trace=str(trace.relative_to(BASE)))
    result.pop("reason", None)
    save(path, result)
    print(tag, result["status"], result.get("counterexample_cycles"), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    for row in sources(p.parse_args().dataset, "old"):
        if row["task"] == TASK and row["tag"] in ("H01", "H05", "H06", "H07"):
            prove(row)
