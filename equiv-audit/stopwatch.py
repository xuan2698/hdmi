"""Use the shared divider as a clock-period certificate for downstream faults."""

import argparse
import re
from pathlib import Path

from corpus import BASE, sources
from designs import load, save
from replay import SimulationError, rename, run

TASK = "cvdp_copilot_digital_stopwatch_0017"
MARK = "// Stopwatch logic"
PERIOD = 50_000_000
TICKS = 3602


def tick_model(original, changed):
    ref, sep1, body = original.partition(MARK)
    alt, sep2, mutant = changed.partition(MARK)
    # On a continuous start, reset sets counter=0. The unmodified divider's
    # exact recurrence is c'=c+1 until c=CLK_FREQ-1, then c'=0 and pulse'=1.
    if not sep1 or not sep2 or ref != alt or not re.search(r"parameter CLK_FREQ\s*=\s*50000000", ref):
        return None
    patterns = ["counter <= 0;", "if (counter == COUNTER_MAX)", "counter <= counter + 1;",
                "one_sec_pulse <= 1'b1;", "localparam COUNTER_MAX = CLK_FREQ - 1;"]
    if not all(x in ref for x in patterns):
        raise ValueError("The shared divider no longer matches the period certificate")
    header = ref.split("    localparam COUNTER_MAX", 1)[0]
    return [header + re.sub(r"\bone_sec_pulse\b", "clk", text) for text in (body, mutant)]


def find_counterexample(case, cohort):
    if case["task"] != TASK:
        return
    result_path = BASE / "reports" / f"{cohort}_cases" / TASK / case["tag"] / "result.json"
    result = load(result_path)
    if result["status"] != "unknown" or (models := tick_model(case["original"], case["mutant"])) is None:
        return
    dest = result_path.parent
    root = BASE / ".work" / cohort / TASK / case["tag"] / "pulse_transition"
    root.mkdir(parents=True, exist_ok=True)
    for name, text in zip(("reference", "changed"), models, strict=True):
        (root / f"{name}.sv").write_text(rename(text, name + "_"))
    tb = f"""
module pulse_replay;
reg clk=0, reset=1;
wire [5:0] gs, gm, ms, mm;
wire gh, mh;
integer n;
reference_dig_stopwatch g(clk,reset,1'b1,gs,gm,gh);
changed_dig_stopwatch m(clk,reset,1'b1,ms,mm,mh);
initial begin
  #1 clk=1;
  #1 clk=0; reset=0;
  $display("STATE 0 %b %b", {{gh,gm,gs}}, {{mh,mm,ms}});
  for (n=1;n<={TICKS};n=n+1) begin
    #2 clk=1;
    #1;
    $display("STATE %d %b %b", n, {{gh,gm,gs}}, {{mh,mm,ms}});
    if (({{gh,gm,gs}} ^ {{mh,mm,ms}}) !== 0 && (^{{gh,gm,gs}}) !== 1'bx) begin
      $display("FIRST %d %b %b", n, {{gh,gm,gs}}, {{mh,mm,ms}});
      $finish;
    end
    #1 clk=0;
  end
  $finish;
end
endmodule
"""
    (root / "pulse_replay.sv").write_text(tb)
    run(root, "iverilog", "-g2012", "-s", "pulse_replay", "-o", "pulse.vvp",
        "reference.sv", "changed.sv", "pulse_replay.sv")
    output = run(root, "vvp", "pulse.vvp")
    match = re.search(r"FIRST\s+(\d+) ([01x]+) ([01x]+)", output)
    if not match:
        result["attempts"].append({"mode": "shared-divider continuous-start trace", "bounded_ticks": TICKS,
                                   "status": "no witness on this input schedule"})
        save(result_path, result)
        return
    tick, g, m = int(match[1]), match[2], match[3]
    states = re.findall(r"STATE\s+(\d+) ([01x]+) ([01x]+)", output)
    _, prev_g, prev_m = states[-2]
    if "x" in prev_g + prev_m:
        return
    for name, bits in (("reference", prev_g), ("changed", prev_m)):
        original = (root / f"{name}.sv").read_text()
        initial = f"initial begin hour=1'b{bits[0]}; minutes=6'b{bits[1:7]}; seconds=6'b{bits[7:13]}; end\n"
        micro = original.replace("posedge clk or posedge reset", "posedge clk")
        (root / f"{name}_transition.sv").write_text(micro.replace("endmodule", initial + "endmodule"))
    cmds = ("read_verilog -sv -formal reference_transition.sv changed_transition.sv; proc; opt -keepdc; "
            "miter -equiv -ignore_gold_x -make_outputs -flatten reference_dig_stopwatch changed_dig_stopwatch pulse; "
            "hierarchy -top pulse; dffunmap; "
            "sat -seq 2 -enable_undef -set-def-inputs -set-init-undef "
            "-set in_start_stop 1 -set in_clk 0 -set in_reset 0 -prove-skip 1 "
            "-prove trigger 0 -show trigger -dump_json pulse_witness.json pulse")
    (dest / "pulse_certificate.ys").write_text(cmds + "\n")
    try:
        formal = run(root, "yosys", "-Q", "-T", "-p", cmds, timeout=10)
    except SimulationError as exc:
        result["pulse_certificate_error"] = str(exc)[-700:]
        save(result_path, result)
        return
    failed = "FAIL!" in formal and (root / "pulse_witness.json").exists()
    result["attempts"].append({"mode": "shared-divider reachable transition", "engine": "Yosys sequential SAT",
                               "reached_tick": tick, "period_default_cycles": PERIOD,
                               "status": "FAIL" if failed else "transition witness not confirmed"})
    if not failed:
        save(result_path, result)
        return
    trace = {"reset_cycles": 1, "repeat": {"start_stop": 1, "reset": 0, "cycles": tick * PERIOD},
             "first_different_1hz_tick": tick, "golden_hour_minutes_seconds": g, "mutant_hour_minutes_seconds": m,
             "reachable_previous_outputs": {"golden": prev_g, "mutant": prev_m},
             "certificate": "Shared unchanged divider reaches terminal after exactly 50000000 enabled input edges. "
                            "Reset first, then hold start_stop=1 continuously. The pulse model preserves both output blocks."}
    save(dest / "compressed_witness.json", trace)
    result.update(status="non_equivalent", counterexample_cycles=1 + tick * PERIOD,
                  witness_method="shared-divider SAT plus 1-Hz Icarus replay",
                  concrete_rtl_replay={"scope": "unchanged downstream RTL at certified pulse edges",
                                       "first_tick": tick, "golden_bits": g, "mutant_bits": m},
                  trace=str((dest / "compressed_witness.json").relative_to(BASE)))
    result.pop("reason", None)
    save(result_path, result)
    print(cohort, case["tag"], tick, 1 + tick * PERIOD, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--cohort", choices=("old", "new"), required=True)
    args = parser.parse_args()
    for item in sources(args.dataset, args.cohort):
        find_counterexample(item, args.cohort)
