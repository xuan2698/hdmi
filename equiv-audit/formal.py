"""Yosys/SBY comparison with explicit four-state golden masks."""

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from corpus import BASE, CYCLES, make, sources
from designs import save
from replay import SimulationError, compile_pair, rename, run


def module(ports):
    ins, out, top = (ports[x] for x in ("input", "output", "top"))
    clk = ports["clock"]
    decl = [f"input wire [{w-1}:0] in_{n}" for n, w in ins.items()]
    total = sum(out.values())
    out_decl = [f"output wire [{total-1}:0] gold, candidate", "output wire [1:0] phase", "output wire permit"]
    con = ([f".{clk}(phase[1])"] if clk else []) + [f".{n}(in_{n})" for n in ins]
    wires = []
    inst = []
    for prefix, name in (("cvdp_r_", "gold"), ("cvdp_m_", "candidate")):
        wires.extend(f"wire [{w-1}:0] {name}_{n};" for n, w in out.items())
        route = con + [f".{n}({name}_{n})" for n in out]
        inst.append(f"{prefix}{top} {name}_dut ({', '.join(route)});")
        inst.append(f"assign {name} = {{{', '.join(name + '_' + n for n in out)}}};")
    prev_decl = [f"reg [{bits-1}:0] previous_{n};" for n, bits in ins.items()]
    remember = [f"previous_{n} <= in_{n};" for n in ins]
    good_stability = " && ".join(f"(in_{n} == previous_{n})" for n in ins) or "1'b1"
    good_reset = " && ".join(f"(in_{n} == {value})" for n, value in ports["resets"].items()) or "1'b1"
    return f"""module audit({', '.join(decl + out_decl)});
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
{chr(10).join(prev_decl)}
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  {chr(10).join(remember)}
end
assign permit = (first || phase[0] || ({good_stability})) && (!startup || ({good_reset}));
{chr(10).join(wires)}
{chr(10).join(inst)}
endmodule
"""


def assertion(ports):
    inputs = ", ".join(f"input [{bits-1}:0] in_{name}" for name, bits in ports["input"].items())
    bound = ", ".join(f".in_{name}(in_{name})" for name in ports["input"])
    width = sum(ports["output"].values()) - 1
    return f"""module formal_top({inputs});
wire [{width}:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core ({bound + ', ' if bound else ''}.gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
"""


def sv_source(source, prefix):
    # Parse archived auto RTL with the original module names and never substitute a DUT.
    return rename(source, prefix)


def config(steps, *, mode="bmc", engine="abc bmc3", timeout=25, address_subset=False):
    return f"""[options]
mode {mode}
depth {steps}
timeout {timeout}
multiclock on
aigsmt none

[engines]
{engine}

[script]
read_verilog -sv -formal golden.sv mutant.sv miter.sv
hierarchy -check -top audit
proc
flatten -noscopeinfo
opt -keepdc
memory_map
opt -keepdc
clk2fflogic
xprop -required -formal -split-outputs -assume-def-inputs
opt -keepdc
read_verilog -formal assertion.sv
prep -top formal_top

[files]
golden.sv
mutant.sv
miter.sv
assertion.sv
"""


def execute(where, name, data):
    cfg = where / f"{name}.sby"
    cfg.write_text(data)
    command = ["sby", "-f", cfg.name]
    completed = subprocess.run(command, cwd=where, capture_output=True, text=True, timeout=60)
    (where / f"{name}.log").write_text(completed.stdout + completed.stderr)
    job = where / name
    status_file = job / "status"
    if status_file.exists():
        status = status_file.read_text().split()[0]
    else:
        status = "ERROR"
    text = completed.stdout + completed.stderr
    return status, job, text


def vcd_rows(path):
    names, widths, hierarchy = {}, {}, []
    state, records = {}, []
    with path.open() as stream:
        for line in stream:
            row = line.strip().split()
            if not row:
                continue
            if row[0] == "$scope":
                hierarchy.append(row[2])
            elif row[0] == "$upscope":
                hierarchy.pop()
            elif row[0] == "$var" and hierarchy == ["formal_top"]:
                names[row[3]] = row[4]
                widths[row[3]] = int(row[2])
            elif row[0] == "$enddefinitions":
                break
        valid_time = False
        for line in stream:
            line = line.strip()
            if line.startswith("#"):
                if valid_time:
                    records.append(dict(state))
                valid_time = True
                continue
            if not line:
                continue
            if line[0] in "bB":
                value, ident = line[1:].split()
            elif line[0] in "01xz":
                value, ident = line[0], line[1:]
            else:
                continue
            if ident in names:
                state[names[ident]] = value.zfill(widths[ident])
        if valid_time:
            records.append(dict(state))
    # SMTBMC adds a final timestamp without a fresh formal step.
    if len(records) > 1 and records[-1] == records[-2]:
        records.pop()
    # Each SMTBMC state has a rising timestamp and a half-tick with only smt_clock changing.
    return records[::2]


def witness(case, job, text, dest, trace=None):
    trace = trace or next(job.glob("engine_*/trace.vcd"), None)
    if trace is None:
        return None
    steps = vcd_rows(trace)
    if not steps:
        return None
    fail = re.findall(r"(?:in step|at step|failed in step)\s+(\d+)", text)
    terminal = steps[min(int(fail[-1]), len(steps)-1)] if fail else steps[-1]
    index = next((i for i, r in enumerate(steps) if r is terminal), len(steps)-1)
    interested = {n: terminal.get("in_" + n) for n in case["ports"]["input"]}
    changed = {}
    def masked(value, xbits):
        xbits = xbits if len(xbits) == len(value) else "0" * len(value)
        return "".join("x" if x == "1" else b for b, x in zip(value, xbits, strict=True))

    gold = masked(terminal.get("gold", ""), terminal.get("gold_x", ""))
    gate = masked(terminal.get("candidate", ""), terminal.get("candidate_x", ""))
    cursor = 0
    if gold and gate and len(gold) == len(gate):
        for name, bits in case["ports"]["output"].items():
            x, y = gold[cursor:cursor+bits], gate[cursor:cursor+bits]
            if any(a in "01" and a != b for a, b in zip(x, y, strict=True)):
                changed[name] = {"golden": x, "mutant": y}
            cursor += bits
    waves = dest / "witness.vcd"
    shutil.copyfile(trace, waves)
    save(dest / "witness.json", {"steps": steps, "last_formal_step": index})
    return {"counterexample_cycles": math.ceil(index / 4), "formal_step": index,
            "terminal_inputs_binary": interested, "different_outputs": changed,
            "trace": str(waves.relative_to(BASE)), "phase_binary": terminal.get("phase")}


def concise_reason(text):
    errors = [line.split("ERROR:", 1)[-1].strip() for line in text.splitlines() if "ERROR:" in line]
    return (errors[0] if errors else "\n".join(text.splitlines()[-4:]))[-600:]


def replay_witness(case, root, dest, *, subset):
    data = json.loads((dest / "witness.json").read_text())
    width = sum(case["ports"]["input"].values())
    ins, outs = case["ports"]["input"], case["ports"]["output"]
    rows = data["steps"][:data["last_formal_step"] + 1]
    names = list(ins)
    words = []
    for current in rows:
        values = {n: current["in_" + n] for n in names}
        if subset:
            for n in ("addr_a", "addr_b"):
                values[n] = values[n][-3:].zfill(ins[n])
        words.append(current["phase"][0] + "".join(values[n] for n in names))
    (root / "witness.mem").write_text("\n".join(words) + "\n")
    decl = [f"reg [{bits-1}:0] v_{name};" for name, bits in ins.items()]
    pairs = ([f".{case['ports']['clock']}(clk)"] if case["ports"]["clock"] else []) + [f".{n}(v_{n})" for n in ins]
    for prefix in ("gold", "changed"):
        decl += [f"wire [{bits-1}:0] {prefix}_{name};" for name, bits in outs.items()]
    bindings = [", ".join(pairs + [f".{n}({prefix}_{n})" for n in outs]) for prefix in ("gold", "changed")]
    output = ["{" + ",".join(f"{p}_{n}" for n in outs) + "}" for p in ("gold", "changed")]
    row = ",".join(("clk", *["v_" + n for n in names]))
    top = case["ports"]["top"]
    harness = f"""
module discrepancy_replay;
reg clk=0;
integer i;
reg [{width}:0] vectors [0:{len(words)-1}];
{chr(10).join(decl)}
cvdp_r_{top} r ({bindings[0]});
cvdp_m_{top} m ({bindings[1]});
initial begin
  $readmemb("witness.mem",vectors);
  for (i=0;i<{len(words)};i=i+1) begin
    {{{row}}}=vectors[i];
    #2; $display("CHECK %0d %b %b", i, {', '.join(output)});
  end
  $finish;
end
endmodule
"""
    (root / "original_gold.sv").write_text(sv_source(case["original"], "cvdp_r_"))
    (root / "original_mut.sv").write_text(sv_source(case["mutant"], "cvdp_m_"))
    (root / "trace_replay.sv").write_text(harness)
    run(root, "iverilog", "-g2012", "-s", "discrepancy_replay", "-o", "trace.vvp",
        "original_gold.sv", "original_mut.sv", "trace_replay.sv")
    text = run(root, "vvp", "trace.vvp")
    for line in text.splitlines():
        if not line.startswith("CHECK "):
            continue
        _, step, gold, candidate = line.split()
        if any(a in "01" and a != b for a, b in zip(gold, candidate, strict=True)):
            return {"replayed_formal_step": int(step), "golden_bits": gold, "mutant_bits": candidate,
                    "address_subset_zero_extended": subset}
    return None


def accept_witness(result, case, root, dest, evidence, *, subset):
    if not evidence:
        result.update(status="unknown", reason="Solver did not emit a readable known-bit counterexample")
        return
    try:
        replayed = replay_witness(case, root, dest, subset=subset)
    except (SimulationError, ValueError, KeyError) as exc:
        replayed = None
        result["replay_error"] = str(exc)
    if replayed:
        result.update(status="non_equivalent", concrete_rtl_replay=replayed, **evidence)
    else:
        result.update(status="unknown", reason="Formal witness failed concrete RTL replay", **evidence)


def abc_witness(case, job, dest, attempts):
    """Translate the older ABC writer's inline comment before replaying its witness."""
    trace = next(job.glob("engine_*/trace.aiw"), None)
    map_file = job / "model" / "design_aiger.ywa"
    if not trace or not map_file.exists():
        return None
    (job / "normalized.aiw").write_text("\n".join(line.partition("#")[0].strip()
                                                  for line in trace.read_text().splitlines()) + "\n")
    commands = (["yosys-witness", "aiw2yw", "normalized.aiw", str(map_file), "normalized.yw"],
                ["yosys", "-Q", "-p", "read_rtlil model/design_prep.il; write_smt2 -wires witness.smt2"],
                ["yosys-smtbmc", "-s", "boolector", "--yw", "normalized.yw", "--dump-vcd",
                 "normalized.vcd", "witness.smt2"])
    for args in commands:
        try:
            p = subprocess.run(args, cwd=job, capture_output=True, text=True, timeout=14)
        except subprocess.TimeoutExpired:
            return None
        if p.returncode not in ((0, 1) if args[0] == "yosys-smtbmc" else (0,)):
            return None
    if (job / "normalized.vcd").exists() and "BMC failed!" in p.stdout:
        attempts.append({"mode": "witness_translation", "engine": "ABC + Boolector", "status": "FAIL"})
        return witness(case, job, p.stdout, dest, job / "normalized.vcd")
    return None


def reconstruct(case, root, text, dest, attempts, *, subset=False, job=None):
    if job and (result := abc_witness(case, job, dest, attempts)):
        return result
    frame = re.findall(r"asserted in frame (\d+)", text)
    steps = int(frame[-1]) + 2 if frame else 4 * CYCLES + 1
    spec = config(steps, engine="smtbmc z3", timeout=15, address_subset=subset)
    (dest / "witness.sby").write_text(spec)
    status, job, log = execute(root, "witness", spec)
    attempts.append({"mode": "witness", "engine": "smtbmc z3", "formal_steps": steps, "status": status})
    return witness(case, job, log, dest) if status == "FAIL" else None


def audit(case, cohort, *, smoke=False):
    root = BASE / ".work" / cohort / case["task"] / case["tag"]
    dest = BASE / "reports" / ("smoke_cases" if smoke else f"{cohort}_cases") / case["task"] / case["tag"]
    dest.mkdir(parents=True, exist_ok=True)
    root.mkdir(parents=True, exist_ok=True)
    subset = case["ports"]["top"] == "custom_byte_enable_ram"
    latch_compat = case["task"] in {"lemmings4", "review2015_fsmseq", "review2015_fsmshift"}
    result = {k: v for k, v in case.items() if k not in ("original", "mutant", "ports")}
    if cohort == "new":
        try:
            compile_pair(root / "compile", case["original"], case["mutant"], case["ports"], 1)
        except SimulationError as exc:
            result.update(status="compile_failure", reason=str(exc), attempts=[])
            save(dest / "result.json", result)
            return result
    def lowered(source, prefix):
        if subset:
            source, count = re.subn(r"(parameter\s+LINES\s*=\s*)8192\b", r"\g<1>8", source)
            if count != 1:
                raise ValueError("Default RAM geometry cannot be isolated")
        if latch_compat:
            source = re.sub(r"\balways_comb\b", "always @*", source)
        return sv_source(source, prefix)
    for fn, code in (("golden.sv", lowered(case["original"], "cvdp_r_")),
                     ("mutant.sv", lowered(case["mutant"], "cvdp_m_")),
                     ("miter.sv", module(case["ports"])), ("assertion.sv", assertion(case["ports"]))):
        (root / fn).write_text(code)
    bounded = min(case["required_cycles"], CYCLES)
    engine = ("smtbmc boolector" if case["ports"]["top"] in {"custom_byte_enable_ram", "iir_filt", "hill_cipher"}
              else "abc bmc3")
    cfg = config(4 * bounded + 1, timeout=22, engine=engine, address_subset=subset)
    (dest / "miter.sv").write_text(module(case["ports"]))
    (dest / "assertion.sv").write_text(assertion(case["ports"]))
    (dest / "bmc.sby").write_text(cfg)
    status, work, text = execute(root, "bmc", cfg)
    attempts = [{"mode": "bmc", "engine": engine, "requested_cycles": bounded, "status": status}]
    if status == "UNKNOWN":
        fallback = config(4 * bounded + 1, engine="smtbmc z3", timeout=15, address_subset=subset)
        (dest / "fallback.sby").write_text(fallback)
        status, work, text = execute(root, "fallback", fallback)
        attempts.append({"mode": "bmc", "engine": "smtbmc z3", "requested_cycles": bounded, "status": status})
    result.update({"attempts": attempts, "bounded_cycles": bounded if status == "PASS" else None,
                   "address_subset": subset, "latch_compatibility": latch_compat})
    if status == "FAIL":
        evidence = (witness(case, work, text, dest) if attempts[-1]["engine"].startswith("smtbmc")
                    else reconstruct(case, root, text, dest, attempts, subset=subset, job=work))
        accept_witness(result, case, root, dest, evidence, subset=subset)
    elif status == "PASS" and not subset and bounded == case["required_cycles"]:
        result.update(status="bounded_equivalent", proof="bounded")
    elif status == "PASS" and not subset:
        full = config(24, mode="prove", engine="smtbmc z3", timeout=8)
        (dest / "prove.sby").write_text(full)
        status, proof, text = execute(root, "prove", full)
        attempts.append({"mode": "prove", "engine": "smtbmc z3 k-induction", "status": status})
        if status == "PASS":
            result.update(status="fully_equivalent", proof="SMTBMC k-induction unbounded")
        elif status == "FAIL" and (evidence := reconstruct(case, root, text, dest, attempts, job=proof)):
            accept_witness(result, case, root, dest, evidence, subset=subset)
        else:
            result.update(status="unknown", reason=f"Required bound {case['required_cycles']} exceeds completed "
                                                   f"{bounded} cycles; unbounded induction {status.lower()}")
    elif subset and status == "PASS":
        result.update(status="unknown", reason="8-address abstraction cannot prove the full 8192-address RAM")
    else:
        result.update(status="unknown", reason=concise_reason(text))
    save(dest / "result.json", result)
    print(cohort, case["task"], case["tag"], result["status"], result.get("counterexample_cycles", ""), flush=True)
    return result


def smoke_test():
    baseline = "module probe(input clk, input x, output reg q); always @(posedge clk) q <= x ? 1'bx : 1'b0; endmodule\n"
    ports = {"input": {"x": 1}, "output": {"q": 1}, "clock": "clk", "resets": {}, "top": "probe"}
    expected = {"equivalent": "bounded_equivalent", "different": "non_equivalent"}
    for name, gate in (("equivalent", baseline.replace("1'bx", "1'b1")),
                       ("different", baseline.replace("1'b0", "1'b1"))):
        case = make("smoke", name, baseline, gate, ports)
        outcome = audit(case, "smoke", smoke=True)
        if outcome["status"] != expected[name]:
            raise RuntimeError(f"Unexpected smoke result: {outcome}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cohort", choices=("smoke", "old", "new"))
    p.add_argument("dataset", type=Path, nargs="?")
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--resume", action="store_true")
    args = p.parse_args()
    if args.cohort == "smoke":
        smoke_test()
        return
    cases = sources(args.dataset, args.cohort)
    if args.resume:
        def pending(case):
            result = BASE / "reports" / f"{args.cohort}_cases" / case["task"] / case["tag"] / "result.json"
            return not result.exists() or "latch_compatibility" not in json.loads(result.read_text())
        cases = [case for case in cases if pending(case)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda c: audit(c, args.cohort), cases))


if __name__ == "__main__":
    main()
