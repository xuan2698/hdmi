import hashlib
import re
import tempfile
from pathlib import Path

from simulate import Replay, RunError
from vcd import rising_edges

DECL = re.compile(r"^(input|output|inout)\b\s*(?:(?:wire|logic|reg|signed|unsigned|var)\s+)*"
                  r"(?:\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*)?(\w+)\s*$")
COMPILED = tempfile.TemporaryDirectory(prefix="autobench-v2-compiled-")
ENUM = re.compile(r"\btypedef\s+enum\s+(?:(logic|reg|bit|int)(\s*\[[^\]]+\])?\s*)?"
                  r"\{([^{}]+)\}\s*(\w+)\s*;", re.S)


def lower_proxy_enums(rtl):
    """Preserve state encodings while bypassing Icarus enum assignment restrictions."""
    def lower(match):
        kind, dimensions, members, alias = match.groups()
        carrier = "int" if not kind or kind == "int" else kind
        declaration = carrier + (dimensions or "")
        clean = re.sub(r"//[^\n]*|/\*.*?\*/", "", members, flags=re.S)
        constants, prior = [], None
        for piece in clean.split(","):
            member = re.fullmatch(r"\s*(\w+)\s*(?:=\s*(.+?))?\s*", piece, re.S)
            if not member:
                return match[0]
            name, value = member.groups()
            value = value or (f"({prior}) + 1" if prior else "0")
            constants.append(f"localparam {declaration} {name} = {value};")
            prior = name
        return f"typedef {declaration} {alias};\n" + "\n".join(constants)
    return ENUM.sub(lower, rtl)


def compiled(harness, rtl):
    token = hashlib.sha256((harness + "\0" + rtl).encode()).hexdigest()
    root = Path(COMPILED.name)
    executable = root / f"{token}.vvp"
    if executable.is_file():
        return executable
    with tempfile.TemporaryDirectory(dir=root) as directory:
        where = Path(directory)
        (where / "replay.v").write_text(harness)
        (where / "subject.v").write_text(rtl)
        Replay._run(where, "iverilog", "-g2012", "-s", "replay", "-o", "sim.vvp",
                    "subject.v", "replay.v")
        (where / "sim.vvp").replace(executable)
    return executable


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

    def __init__(self, interface, vectors, *, all_edges=False, proxy_compat=False):
        self.inputs, self.outputs, self.clock, self.edge = interface
        self.vectors = vectors
        self.all_edges = all_edges
        self.proxy_compat = proxy_compat

    def trace(self, rtl, *, observe=(), probes=None):
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
        mid_mem = ""
        mid_step = "#4;"
        read_mid = ""
        if inputs:
            width = sum(inputs.values())
            declarations.append(f"reg [{width - 1}:0] samples [0:{len(self.vectors) - 1}];")
            drive = "{" + ", ".join(inputs) + "} = samples[cycle];"
            vector_mem = "\n".join("".join(f"{row[n]:0{w}b}" for n, w in inputs.items())
                                   for row in self.vectors) + "\n"
            if any(row.get("mid") for row in self.vectors):
                declarations.append(f"reg [{width - 1}:0] middle [0:{len(self.vectors) - 1}];")
                mid_mem = "\n".join("".join(f"{row.get('mid', {}).get(n, row[n]):0{w}b}"
                                             for n, w in inputs.items()) for row in self.vectors) + "\n"
                read_mid = '$readmemb("middle.mem", middle);'
                mid_step = "#2; {" + ", ".join(inputs) + "} = middle[cycle]; #2;"
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
    {read_mid}
    for (cycle = 0; cycle < {len(self.vectors)}; cycle = cycle + 1) begin
        {drive}
        {before}
        phase = {1 - initial};
        #1; {display}
        {mid_step} phase = {initial};
        {after}
    end
    $finish;
end
endmodule
"""
        with tempfile.TemporaryDirectory(prefix="autobench-v2-") as temp:
            where = Path(temp)
            (where / "vectors.mem").write_text(vector_mem)
            if mid_mem:
                (where / "middle.mem").write_text(mid_mem)
            try:
                executable = compiled(code, rtl)
            except RunError as exc:
                if not self.proxy_compat or not re.search(
                    "requires an explicit cast|Enumeration name .* incorrectly sized", str(exc)
                ):
                    raise
                relaxed = lower_proxy_enums(rtl)
                if relaxed == rtl:
                    raise
                executable = compiled(code, relaxed)
            text = Replay._run(where, "vvp", str(executable))
            waves = []
            if observe:
                full = tuple(f"replay.dut.{n}" for n in observe)
                _, sampled = rising_edges(where / "trace.vcd", "replay.phase", full, edge=edge)
                waves = [{name: row[f] for name, f in zip(observe, full)} for _, row in sampled]
        rows = [dict(zip(outputs, line.split()[1:]))
                for line in text.splitlines() if line.startswith("TRACE ")]
        if probes is not None:
            probes.extend(line.split()[1:] for line in text.splitlines() if line.startswith("PROBE "))
        count = len(self.vectors) * (3 if self.all_edges else 1)
        if len(rows) != count or any(row.keys() != outputs.keys() for row in rows):
            raise RunError(f"Replay captured {len(rows)} of {count} samples")
        return rows, waves


def replay(interface, vectors, *, proxy_compat=False):
    return VectorReplay(interface, vectors, proxy_compat=proxy_compat)
