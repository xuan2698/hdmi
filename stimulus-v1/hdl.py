"""Shared Icarus replay with exact dual-edge scoring and fixed parameters."""

import hashlib
import re
import threading
from pathlib import Path

from common import ROOT, protocol
from replay import prepare_vectors, rename, reset_rows, run

WORK = ROOT / ".work"
LOCKS = {}
GATE = threading.Lock()


def bind_params(text, top, parameters):
    if not parameters:
        return text
    body = ", ".join(f".{n}({v})" for n, v in parameters.items())
    return re.sub(rf"(?m)^(cvdp_[rm]_{re.escape(top)})(?=\s|\()", rf"\1 #({body})", text)


def compile_sim(gold, variant, ports, extra=""):
    from replay import harness
    maximum = protocol()["max_cycles"]
    bench = harness(ports, maximum, "compare")
    bench = bind_params(bench, ports["top"], ports["parameters"])
    bench = bench.replace("integer cycle;", 'integer cycle, cycles, hits=0, first_hit=0;')
    bench = bench.replace('$readmemb("inputs.mem", vectors);',
                          'if (!$value$plusargs("cycles=%d", cycles)) $fatal(1, "cycles missing");\n'
                          '    $readmemb("inputs.mem", vectors, 0, cycles-1);')
    bench = bench.replace('$readmemb("mid.mem", middles);', '$readmemb("mid.mem", middles, 0, cycles-1);')
    bench = bench.replace(f"cycle < {maximum};", "cycle < cycles;")
    bench = bench.replace('$display("TRACE %0d %b %b %b %b", cycle+1, phase, ref_bits, mut_bits, tb_match);',
                          'if (!tb_match) begin hits=hits+1; if (first_hit==0) first_hit=cycle+1; end')
    bench = bench.replace("$finish;", '$display("EXPOSE %0d %0d", hits, first_hit);\n    $finish;')
    if extra:
        bench = bench.replace("endmodule", extra + "\nendmodule")
    pair = (rename(gold, "cvdp_r_"), rename(variant, "cvdp_m_"), bench)
    k = hashlib.sha256("\0".join(pair).encode()).hexdigest()
    where = WORK / "compiled" / k
    binary = where / "run.vvp"
    if not binary.exists():
        with GATE:
            lock = LOCKS.setdefault(k, threading.Lock())
        with lock:
            if not binary.exists():
                where.mkdir(parents=True, exist_ok=True)
                for name, text in zip(("gold.sv", "variant.sv", "bench.sv"), pair, strict=True):
                    (where / name).write_text(text)
                run(where, "iverilog", "-g2012", "-s", "replay", "-o", "tmp.vvp",
                    "gold.sv", "variant.sv", "bench.sv")
                (where / "tmp.vvp").replace(binary)
    return binary


def input_dir(where, vectors, ports):
    where.mkdir(parents=True, exist_ok=True)
    prepare_vectors(where.parent, {where.name: vectors}, ports)
    return where


def observe(binary, where, cycles):
    data = run(where, "vvp", str(binary), f"+cycles={cycles}", timeout=20)
    matches = re.findall(r"^EXPOSE (\d+) (\d+)$", data, re.M)
    if len(matches) != 1:
        raise RuntimeError(f"Missing dual-edge summary: {data[-500:]}")
    return {"samples": int(matches[0][0]), "first": int(matches[0][1]), "text": data}
