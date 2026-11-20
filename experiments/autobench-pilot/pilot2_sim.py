import re
import tempfile
from pathlib import Path

from simulate import Replay, RunError
from vcd import rising_edges

DECL = re.compile(r"^(input|output|inout)\b\s*(?:(?:wire|logic|reg|signed|unsigned|var)\s+)*"
                  r"(?:\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*)?(\w+)\s*$")


def interface_from(problem):
    header = re.sub(r"//[^\n]*", "", problem["module_header"])
    pins = re.search(r"\((.*)\)\s*;", header, re.S)
    if not pins:
        raise RunError("Could not parse the public module interface")
    groups = {"input": {}, "output": {}}
    kind, width = None, None
    for item in pins[1].strip().split(","):
        token = item.strip()
        dec = DECL.fullmatch(token)
        if dec:
            kind, hi, lo, name = dec.groups()
            width = abs(int(hi) - int(lo)) + 1 if hi else 1
        elif kind and re.fullmatch(r"\w+", token):
            name = token
        else:
            raise RunError(f"Unsupported public port declaration: {token}")
        if kind not in groups:
            raise RunError(f"Unsupported direction: {kind}")
        groups[kind][name] = width
    inputs, outputs = groups["input"], groups["output"]
    clock = next((n for n in inputs if n.lower() in ("clk", "clock")), None)
    if clock:
        if inputs.pop(clock) != 1:
            raise RunError("Replay requires a scalar clock")
    spec = problem["spec"].lower()
    negative = re.search(r"negative[- ]edge|falling[- ]edge|\bnegedge\b", spec)
    positive = re.search(r"positive[- ]edge|rising[- ]edge|\bposedge\b", spec)
    edge = "negedge" if negative and not positive else "posedge"
    if not outputs:
        raise RunError("Public interface has no outputs")
    return inputs, outputs, clock, edge


class VectorReplay:
    """Connect public ports and observe settled outputs during pure input replay."""

    def __init__(self, interface, vectors, *, all_edges=False):
        self.inputs, self.outputs, self.clock, self.edge = interface
        self.vectors = vectors
        self.all_edges = all_edges

    def trace(self, rtl, *, observe=()):
        inputs, outputs = self.inputs, self.outputs
        clock = self.clock
        edge = self.edge
        initial = int(edge == "negedge")
        declarations = [f"reg phase = {initial};"]
        declarations.extend(f"{kind} [{w - 1}:0] {n};"
                            for kind, ws in (("reg", inputs), ("wire", outputs))
                            for n, w in ws.items())
        binding = ([f".{clock}(phase)"] if clock else [])
        binding.extend(f".{name}({name})" for name in (*inputs, *outputs))
        values = ", ".join(outputs)
        format_string = " %b" * len(outputs)
        display = f'$display("TRACE{format_string}", {values});'
        drive = ""
        vector_mem = ""
        if inputs:
            width = sum(inputs.values())
            declarations.append(f"reg [{width - 1}:0] samples [0:{len(self.vectors) - 1}];")
            drive = "{" + ", ".join(inputs) + "} = samples[cycle];"
            vector_mem = "\n".join("".join(f"{row[n]:0{w}b}" for n, w in inputs.items())
                                   for row in self.vectors) + "\n"
        read_vectors = '$readmemb("vectors.mem", samples);' if inputs else ""
        dump = '$dumpfile("trace.vcd"); $dumpvars(0, replay);' if observe else ""
        before = f"#1; {display} #4;" if self.all_edges else "#5;"
        after = f"#1; {display}" if self.all_edges else "#1;"
        code = f"""
`timescale 1ns/1ps
module replay;
{chr(10).join(declarations)}
integer cycle;
top_module dut ({", ".join(binding)});
initial begin
    {dump}
    {read_vectors}
    for (cycle = 0; cycle < {len(self.vectors)}; cycle = cycle + 1) begin
        {drive}
        {before}
        phase = {1 - initial};
        #1; {display}
        #4; phase = {initial};
        {after}
    end
    $finish;
end
endmodule
"""
        with tempfile.TemporaryDirectory(prefix="autobench-v2-") as temp:
            where = Path(temp)
            (where / "vectors.mem").write_text(vector_mem)
            (where / "replay.v").write_text(code)
            (where / "subject.v").write_text(rtl)
            Replay._run(where, "iverilog", "-g2012", "-s", "replay", "-o", "sim.vvp",
                        "subject.v", "replay.v")
            text = Replay._run(where, "vvp", "sim.vvp")
            waves = []
            if observe:
                full = tuple(f"replay.dut.{n}" for n in observe)
                _, sampled = rising_edges(where / "trace.vcd", "replay.phase", full, edge=edge)
                waves = [{name: row[f] for name, f in zip(observe, full)} for _, row in sampled]
        rows = [dict(zip(outputs, line.split()[1:]))
                for line in text.splitlines() if line.startswith("TRACE ")]
        count = len(self.vectors) * (3 if self.all_edges else 1)
        if len(rows) != count or any(row.keys() != outputs.keys() for row in rows):
            raise RunError(f"Replay captured {len(rows)} of {count} samples")
        return rows, waves


def replay(interface, vectors):
    return VectorReplay(interface, vectors)
