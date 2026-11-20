import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from vcd import rising_edges

ROOT = Path(__file__).resolve().parent
PATH = f"{ROOT / '.local/bin'}{os.pathsep}{os.environ['PATH']}"
COMMAND_ENV = {"PATH": PATH, "LC_ALL": "C"}
PORT = re.compile(r"\b(input|output)\s+(?:(?:reg|wire|logic)\s+)?(?:\[(\d+):(\d+)\]\s*)?(\w+)")


class RunError(RuntimeError):
    pass


def ports(problem):
    parsed = {"input": {}, "output": {}}
    for direction, hi, lo, name in PORT.findall(problem["module_header"]):
        parsed[direction][name] = abs(int(hi) - int(lo)) + 1 if hi else 1
    if parsed["input"].pop("clk", None) != 1 or not parsed["output"]:
        raise RunError("The replay harness expects a scalar clk and at least one output")
    return parsed["input"], parsed["output"]


def execute_code(source, kind, *, vectors=None, seed=None, cycles=None):
    request = {"source": source, "kind": kind, "vectors": vectors, "seed": seed, "cycles": cycles}
    args = ["bwrap", "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
            "--ro-bind", str(ROOT / "model_worker.py"), "/worker.py",
            "/usr/bin/python3", "-I", "-S", "/worker.py"]
    proc = subprocess.run(args, input=json.dumps(request), capture_output=True, text=True,
                          env=COMMAND_ENV, timeout=12, cwd=ROOT)
    if proc.returncode:
        raise RunError("Generated Python failed: " + proc.stderr[-1100:])
    try:
        return json.loads(proc.stdout)
    except ValueError as exc:
        raise RunError("Generated Python did not return valid JSON") from exc


def validate_rows(rows, widths, length, *, allow_unknown=False):
    if not isinstance(rows, list) or len(rows) != length:
        raise RunError(f"Expected {length} rows")
    for cycle, row in enumerate(rows, 1):
        if not isinstance(row, dict) or row.keys() != widths.keys():
            raise RunError(f"Cycle {cycle}: expected precisely these ports: {list(widths)}")
        for name, value in row.items():
            if value is None and allow_unknown:
                continue
            if type(value) is not int or not 0 <= value < 1 << widths[name]:
                raise RunError(f"Cycle {cycle}: {name} must be an integer fitting {widths[name]} bits")
    return rows


def vectors_from(code, inputs, seed, cycles):
    return validate_rows(execute_code(code, "stimulus", seed=seed, cycles=cycles), inputs, cycles)


def expected_from(code, outputs, vectors):
    values = execute_code(code, "checker", vectors=vectors)
    return validate_rows(values, outputs, len(vectors), allow_unknown=True)


class Replay:
    """Bind named ports, replay externally generated input rows, and observe the outputs."""

    def __init__(self, inputs, outputs, vectors):
        self.inputs = inputs
        self.outputs = outputs
        self.vectors = vectors
        self.packed = "\n".join("".join(f"{row[n]:0{w}b}" for n, w in inputs.items())
                                for row in vectors) + "\n"

    def trace(self, rtl, *, observe=()):
        inputs = self.inputs
        outputs = self.outputs
        decl = ["reg clk = 0;"]
        for kind, widths in (("reg", inputs), ("wire", outputs)):
            decl.extend(f"{kind} [{w - 1}:0] {n};" for n, w in widths.items())
        binding = ", ".join(f".{n}({n})" for n in ("clk", *inputs, *outputs))
        packed_targets = "{" + ", ".join(inputs) + "}"
        values = ", ".join(outputs)
        patterns = " %b" * len(outputs)
        dump = '$dumpfile("trace.vcd"); $dumpvars(0, replay);' if observe else ""
        harness = f"""
`timescale 1ns/1ps
module replay;
{chr(10).join(decl)}
reg [{sum(inputs.values()) - 1}:0] samples [0:{len(self.vectors) - 1}];
integer cycle;
top_module dut ({binding});
initial begin
    {dump}
    $readmemb("vectors.mem", samples);
    for (cycle = 0; cycle < {len(self.vectors)}; cycle = cycle + 1) begin
        {packed_targets} = samples[cycle];
        #5; clk = 1;
        #1; $display("TRACE{patterns}", {values});
        #4; clk = 0;
    end
    $finish;
end
endmodule
"""
        with tempfile.TemporaryDirectory(prefix="autobench-trace-") as temp:
            path = Path(temp)
            (path / "vectors.mem").write_text(self.packed)
            (path / "replay.v").write_text(harness)
            (path / "subject.v").write_text(rtl)
            self._run(path, "iverilog", "-g2012", "-s", "replay", "-o", "sim.vvp",
                      "replay.v", "subject.v")
            stdout = self._run(path, "vvp", "sim.vvp")
            if observe:
                signals = tuple(f"replay.dut.{name}" for name in observe)
                _, wave = rising_edges(path / "trace.vcd", "replay.clk", signals)
                internals = [{name: row[full] for name, full in zip(observe, signals)}
                             for _, row in wave]
            else:
                internals = []
        rows = [dict(zip(outputs, line.split()[1:]))
                for line in stdout.splitlines() if line.startswith("TRACE ")]
        if len(rows) != len(self.vectors) or any(row.keys() != outputs.keys() for row in rows):
            raise RunError(f"Simulator returned {len(rows)} rows for {len(self.vectors)} cycles")
        return rows, internals

    @staticmethod
    def _run(path, *args):
        try:
            run = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=path, env=COMMAND_ENV, timeout=16)
        except subprocess.TimeoutExpired as exc:
            raise RunError(f"{args[0]} timed out") from exc
        if run.returncode:
            raise RunError(f"{args[0]} exited {run.returncode}: {(run.stderr or run.stdout)[-1000:]}")
        return run.stdout


def known_int(bits):
    return int(bits, 2) if set(bits) <= {"0", "1"} else None


def mismatches(expected, trace):
    return [{name for name, value in guess.items()
             if value is not None and known_int(obs[name]) != value}
            for guess, obs in zip(expected, trace, strict=True)]


def differences(reference, candidate):
    return [(i, name, left, b[name])
            for i, (a, b) in enumerate(zip(reference, candidate, strict=True))
            for name, left in a.items()
            if any(x in "01" and x != y for x, y in zip(left, b[name], strict=True))]
