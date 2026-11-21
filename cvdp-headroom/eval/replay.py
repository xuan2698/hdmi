"""Run four-state dual-edge RTL comparisons and golden code coverage."""

import os
import re
import subprocess
from pathlib import Path
from random import Random

MODULE = re.compile(r"(?m)^[ \t]*module[ \t]+([A-Za-z_]\w*)")
COVERAGE_TYPES = ("line", "branch")


class SimulationError(RuntimeError):
    pass


def run(where, *cmd, timeout=35):
    try:
        process = subprocess.run(cmd, cwd=where, capture_output=True, text=True, timeout=timeout,
                                 env={"PATH": os.environ["PATH"], "LC_ALL": "C"})
    except subprocess.TimeoutExpired as exc:
        raise SimulationError(f"{cmd[0]} exceeded {timeout}s") from exc
    if process.returncode:
        raise SimulationError(f"{cmd[0]} exited {process.returncode}: {(process.stderr or process.stdout)[-2500:]}")
    return process.stdout


def rename(source, prefix):
    names = set(MODULE.findall(source))
    if not names:
        raise ValueError("Missing Verilog modules")
    pattern = r"\b(?:" + "|".join(map(re.escape, sorted(names))) + r")\b"
    return re.sub(pattern, lambda m: prefix + m[0], source)


def reset_rows(ports, seed, n):
    rng = Random(seed)
    out = []
    for cycle in range(n):
        row = {key: rng.getrandbits(width) for key, width in ports["input"].items()}
        for name, active in ports["resets"].items():
            row[name] = active if cycle < 2 or rng.randrange(128) == 0 else 1 - active
        out.append(row)
    return out


def pack(row, widths):
    return "".join(f"{row[k]:0{width}b}" for k, width in widths.items())


def prepare_vectors(where, scores, ports):
    ins = ports["input"]
    for tag, vectors in scores.items():
        location = where / tag
        location.mkdir(parents=True, exist_ok=True)
        words = [pack(row, ins) for row in vectors]
        mids = [pack({**row, **row.get("mid", {})}, ins) for row in vectors]
        (location / "inputs.mem").write_text("\n".join(words) + "\n")
        (location / "mid.mem").write_text("\n".join(mids) + "\n")


def harness(ports, cycles, mode):
    ins, outs, clock, top = (ports[key] for key in ("input", "output", "clock", "top"))
    sw, ow = sum(ins.values()), sum(outs.values())
    declara = [f"reg [{w-1}:0] {name};" for name, w in ins.items()]
    declara += [f"wire [{w-1}:0] r_{n}, m_{n};" for n, w in outs.items()]
    common = f".{clock}(phase), " + ", ".join(f".{n}({n})" for n in ins)
    def bind(prefix):
        return common + ", " + ", ".join(f".{name}({prefix}_{name})" for name in outs)
    bundle = "{" + ", ".join(ins) + "}"
    r = "{" + ", ".join(f"r_{n}" for n in outs) + "}"
    m = "{" + ", ".join(f"m_{n}" for n in outs) + "}"
    compared = f"""
cvdp_m_{top} mutated ({bind("m")});
wire [{ow-1}:0] ref_bits = {r};
wire [{ow-1}:0] mut_bits = {m};
wire tb_match = (ref_bits === (ref_bits ^ mut_bits ^ ref_bits));
always @(posedge phase, negedge phase) begin
    $display("TRACE %0d %b %b %b %b", cycle+1, phase, ref_bits, mut_bits, tb_match);
end
""" if mode == "compare" else f"""
always @(posedge phase, negedge phase) begin
    #0.001; $display("GTRACE %b", {r});
end
"""
    return f"""
`timescale 1ns/1ps
module replay;
reg phase = 0;
integer cycle;
reg [{sw-1}:0] vectors [0:{cycles-1}], middles [0:{cycles-1}];
{chr(10).join(declara)}
{("cvdp_r_" if mode == "compare" else "")+top} golden ({bind("r")});
{compared}
initial begin
    $readmemb("inputs.mem", vectors);
    $readmemb("mid.mem", middles);
    for (cycle = 0; cycle < {cycles}; cycle = cycle + 1) begin
        {bundle} = vectors[cycle];
        #5; phase = 1;
        #2; {bundle} = middles[cycle];
        #3; phase = 0;
        #1;
    end
    $finish;
end
endmodule
"""


def compile_pair(where, gold, variant, ports, cycles):
    where.mkdir(parents=True, exist_ok=True)
    (where / "gold.sv").write_text(rename(gold, "cvdp_r_"))
    (where / "mut.sv").write_text(rename(variant, "cvdp_m_"))
    (where / "replay.sv").write_text(harness(ports, cycles, "compare"))
    run(where, "iverilog", "-g2012", "-s", "replay", "-o", "sim.vvp", "gold.sv", "mut.sv", "replay.sv")
    return where / "sim.vvp"


def compare(binary, stimulus, cycles, outs, *, collect_probes=False):
    text = run(stimulus, "vvp", str(binary))
    counts = {"raw_difference_samples": 0, "known_difference_samples": 0, "official_mismatch_samples": 0,
              "golden_z_samples": 0, "first_exposure": None}
    samples = 0
    evidence = []
    for row in text.splitlines():
        if collect_probes and row.startswith("PROBE "):
            evidence.append(row.split()[1:])
        if not row.startswith("TRACE "):
            continue
        _, cycle, phase, ref, muted, match = row.split()
        samples += 1
        if (int(cycle), phase) != ((samples + 1) // 2, str(samples % 2)):
            raise SimulationError(f"Unexpected edge order: {row}")
        known = [i for i, (a, b) in enumerate(zip(ref, muted, strict=True)) if a in "01" and a != b]
        counts["raw_difference_samples"] += ref != muted
        counts["known_difference_samples"] += bool(known)
        counts["official_mismatch_samples"] += match == "0"
        counts["golden_z_samples"] += "z" in ref
        if match == "0" and ref != muted and counts["first_exposure"] is None:
            begin = 0
            differing = {}
            for name, width in outs.items():
                end = begin + width
                if ref[begin:end] != muted[begin:end] and any(i in known for i in range(begin, end)):
                    differing[name] = [ref[begin:end], muted[begin:end]]
                begin = end
            counts["first_exposure"] = {"cycle": int(cycle), "edge": "posedge" if phase == "1" else "negedge",
                                        "outputs": differing}
    if samples != cycles * 2:
        raise SimulationError(f"Captured {samples} edges instead of {cycles * 2}")
    if not counts["golden_z_samples"] and counts["known_difference_samples"] != counts["official_mismatch_samples"]:
        raise SimulationError("Four-state sample disagreement with the AutoBench predicate")
    if collect_probes:
        counts["probes"] = evidence
    return counts


def coverage(where, code, ports, cycles, stimulus_dirs):
    where.mkdir(parents=True, exist_ok=True)
    (where / "gold.sv").write_text(code)
    (where / "replay.sv").write_text(harness(ports, cycles, "coverage"))
    command = ("verilator", "--binary", "--timing", "--coverage-line", "--top-module", "replay",
               "-j", "2", "-Wno-fatal")
    files = ("gold.sv", "replay.sv")
    policy = "Verilator original RTL"
    try:
        run(where, *command, *files, timeout=150)
    except SimulationError as exc:
        if "%Error-BLKANDNBLK" not in str(exc) or ports["top"] != "Word_Change_Pulse":
            raise
        return icarus_word_coverage(where, code, stimulus_dirs, cycles)
    binary = where / "obj_dir" / "Vreplay"
    results = {"policy": policy}
    for tag, folder in stimulus_dirs.items():
        run(folder, str(binary), "+verilator+coverage+file+coverage.dat")
        records = {kind: {} for kind in COVERAGE_TYPES}
        for line in (folder / "coverage.dat").read_text().splitlines():
            if not line.startswith("C '"):
                continue
            key, value = line[3:].rsplit("' ", 1)
            fields = dict(part.split("\x02", 1) for part in key.split("\x01") if "\x02" in part)
            if fields.get("f") != "gold.sv":
                continue
            for kind in records:
                if fields.get("page", "").startswith("v_" + kind + "/"):
                    records[kind][key] = int(value) > 0
        results[tag] = {kind: {"hit": sum(values.values()), "total": len(values)}
                        for kind, values in records.items()}
    return results


def icarus_word_coverage(where, code, stimulus_dirs, cycles):
    """Count assignment lines and branch arms on the unchanged mixed-assignment DUT."""
    if code.count("latched_pattern <= match_pattern;") != 1:
        raise SimulationError("Word-change coverage needs its frozen implicit-else anchor")
    lines, locations = [], {key: set() for key in COVERAGE_TYPES}
    closing_latch = False
    for number, line in enumerate(code.splitlines(), 1):
        plain = line.split("//", 1)[0].strip()
        if closing_latch and plain == "end":
            line = f'{line} else begin $display("COVER branch {number}"); end'
            locations["branch"].add(number)
            closing_latch = False
        if re.fullmatch(r"\w+\s*(?:<=|=(?!=))\s*[^;]+;", plain):
            lines.append(f'$display("COVER line {number}");')
            locations["line"].add(number)
        lines.append(line)
        if plain.endswith("begin") and re.search(r"\b(?:if\s*\(|else\s+begin)", plain):
            lines.append(f'$display("COVER branch {number}");')
            locations["branch"].add(number)
        if plain == "latched_pattern <= match_pattern;":
            closing_latch = True
    if closing_latch or not all(locations.values()):
        raise SimulationError("Unrecognized word-change coverage sites")
    (where / "instrumented.sv").write_text("\n".join(lines) + "\n")
    for source, binary in (("gold.sv", "plain.vvp"), ("instrumented.sv", "probed.vvp")):
        run(where, "iverilog", "-g2012", "-s", "replay", "-o", binary, source, "replay.sv")
    results = {"policy": "Icarus executed assignment lines and branch arms; probed and original outputs agree"}
    for tag, folder in stimulus_dirs.items():
        original, observed = (run(folder, "vvp", str(where / name)) for name in ("plain.vvp", "probed.vvp"))
        reference, traced = (re.findall(r"^GTRACE ([01xz]+)$", result, re.M) for result in (original, observed))
        if len(reference) != 2 * cycles or reference != traced:
            raise SimulationError(f"Icarus coverage instrumentation changed outputs on {tag}")
        results[tag] = {}
        for kind, points in locations.items():
            hit = {int(x) for x in re.findall(rf"^COVER {kind} (\d+)$", observed, re.M)}
            results[tag][kind] = {"hit": len(hit), "total": len(points)}
    return results
