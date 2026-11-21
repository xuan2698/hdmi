"""Exercise dual-edge Icarus sampling and Verilator line coverage on one released RTL."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

import pyarrow.parquet as pq

CASE = "cvdp_copilot_simple_spi_0003"
SEEDS = (101, 203, 307)
CYCLES = 2000
HARNESS = r"""
`timescale 1ns/1ps
module smoke;
    reg clk = 0;
    reg rst_n, enable, fault, clear;
    reg [15:0] word_in;
    reg [31:0] seed;
    integer cycle, edges = 0, mismatch = 0, forced_mismatch = 0;
    wire [10:0] ref_out, identical_out;
    // A deliberately inverted observed bit validates the monitor without changing the DUT.
    wire [10:0] flipped_out = ref_out ^ 11'b1;
    wire pair_match = (ref_out === (ref_out ^ identical_out ^ ref_out));
    wire forced_match = (ref_out === (ref_out ^ flipped_out ^ ref_out));
    spi_fsm golden (.i_clk(clk), .i_rst_b(rst_n), .i_data_in(word_in),
        .i_enable(enable), .i_fault(fault), .i_clear(clear),
        .o_spi_cs_b(ref_out[10]), .o_spi_clk(ref_out[9]), .o_spi_data(ref_out[8]),
        .o_bits_left(ref_out[7:3]), .o_done(ref_out[2]), .o_fsm_state(ref_out[1:0]));
`ifndef COVERAGE_ONLY
    spi_fsm identical (.i_clk(clk), .i_rst_b(rst_n), .i_data_in(word_in),
        .i_enable(enable), .i_fault(fault), .i_clear(clear),
        .o_spi_cs_b(identical_out[10]), .o_spi_clk(identical_out[9]), .o_spi_data(identical_out[8]),
        .o_bits_left(identical_out[7:3]), .o_done(identical_out[2]), .o_fsm_state(identical_out[1:0]));
    // Use the active region, with no post-edge delay, as in official AutoBench TBs.
    always @(posedge clk, negedge clk) begin
        edges = edges + 1;
        if (!pair_match) mismatch = mismatch + 1;
        if (!forced_match) forced_mismatch = forced_mismatch + 1;
    end
`endif
    initial begin
        if (!$value$plusargs("seed=%d", seed)) $fatal(1, "Missing seed");
`ifndef COVERAGE_ONLY
        if (!(1'bx === (1'bx ^ 1'b0 ^ 1'bx))) $fatal(1, "Golden X must mask");
        if (1'bz === (1'bz ^ 1'bz ^ 1'bz)) $fatal(1, "Golden Z is not masked by the XOR formula");
`endif
        for (cycle = 0; cycle < 2000; cycle = cycle + 1) begin
            seed = seed ^ (seed << 13);
            seed = seed ^ (seed >> 17);
            seed = seed ^ (seed << 5);
            rst_n = cycle != 0 && seed[6:0] != 7'd0;
            enable = seed[30];
            fault = seed[14:11] == 0;
            clear = seed[25:22] == 0;
            word_in = seed[15:0];
            #5 clk = 1;
            #5 clk = 0;
            #1;
        end
`ifndef COVERAGE_ONLY
        $display("COUNTS %0d %0d %0d", edges, mismatch, forced_mismatch);
`endif
        $finish;
    end
endmodule
"""


def run(work, *command, timeout=45):
    completed = subprocess.run(command, cwd=work, check=True, capture_output=True, text=True, timeout=timeout)
    return completed.stdout


def line_points(path):
    points = {}
    for line in path.read_text().splitlines():
        if not line.startswith("C '"):
            continue
        key, count = line[3:].rsplit("' ", 1)
        fields = dict(item.split("\x02", 1) for item in key.split("\x01") if "\x02" in item)
        if fields.get("page", "").startswith("v_line/") and fields.get("f") == "spi.sv":
            points[key] = int(count) > 0
    if not points:
        raise ValueError("No instrumented golden RTL line points found")
    return points


def simulate(dataset):
    row = next(r for r in pq.read_table(dataset).to_pylist() if r["id"] == CASE)
    rtl, = row["rtl_files"]
    samples = []
    with tempfile.TemporaryDirectory(prefix="cvdp-spi-smoke-") as directory:
        work = Path(directory)
        (work / "spi.sv").write_text(rtl["content"])
        (work / "smoke.sv").write_text(HARNESS)
        run(work, "iverilog", "-g2012", "-s", "smoke", "-o", "smoke.vvp", "spi.sv", "smoke.sv")
        run(work, "verilator", "--binary", "--timing", "--coverage-line", "--top-module", "smoke",
            "-j", "2", "-Wno-fatal", "+define+COVERAGE_ONLY", "spi.sv", "smoke.sv", timeout=90)
        union = set()
        for seed in SEEDS:
            text = run(work, "vvp", "smoke.vvp", f"+seed={seed}")
            counts = tuple(map(int, re.search(r"COUNTS (\d+) (\d+) (\d+)", text).groups()))
            total, identical, forced = counts
            if (total, identical) != (2 * CYCLES, 0) or not forced:
                raise ValueError(f"Dual-edge comparator smoke failed for seed {seed}: {counts}")
            filename = f"coverage-{seed}.dat"
            run(work, "obj_dir/Vsmoke", f"+seed={seed}", f"+verilator+coverage+file+{filename}")
            coverage = line_points(work / filename)
            union.update(k for k, hit in coverage.items() if hit)
            samples.append({"seed": seed, "cycles": CYCLES, "edge_samples": total, "identical_mismatches": identical,
                            "forced_mismatches": forced, "dut_line_points_hit": sum(coverage.values()),
                            "dut_line_points_total": len(coverage)})
    return {"scope": "toolchain smoke only", "task": row["id"], "coverage_tool": "Verilator line instrumentation",
            "samples": samples, "union_dut_line_points_hit": len(union),
            "dut_line_points_total": samples[0]["dut_line_points_total"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parquet", type=Path)
    args = parser.parse_args()
    print(json.dumps(simulate(args.parquet), indent=2))


if __name__ == "__main__":
    main()
