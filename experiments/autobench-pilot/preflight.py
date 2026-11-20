#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

from vcd import rising_edges

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
CHECKS = ROOT / "checks"
TASK = "timer"
CLOCK = "timer_random_tb.clk"
INPUTS = ("timer_random_tb.load", "timer_random_tb.data")
OUTPUT = "timer_random_tb.tc"
INTERNAL = "timer_random_tb.dut.count_value"
GUARD_HIT = "timer_random_tb.dut.probe_guard_hit"
GUARD_DIFFERS = "timer_random_tb.dut.probe_guard_differs"
DECREMENT_HIT = "timer_random_tb.dut.probe_decrement_hit"
WAVE_SIGNALS = (*INPUTS, OUTPUT, INTERNAL)
PROBES = (GUARD_HIT, GUARD_DIFFERS, DECREMENT_HIT)
RULES = {
    "decrement_constant": ("count_value - 1", "count_value - 3"),
    "guard_operator": ("count_value != 0", "count_value > 0"),
    "terminal_condition": ("assign tc = count_value == 0;", "assign tc = count_value != 0;"),
}
TIMER_PROCESS = re.compile(
    r"always @\(posedge clk\)\s+if\(load\) count_value <= data;\s+"
    r"else if\(count_value != 0\) count_value <= count_value - 1;"
)
PROBED_TIMER_PROCESS = """
    reg probe_guard_hit, probe_guard_differs, probe_decrement_hit;
    always @(posedge clk) begin
        probe_guard_hit <= 0;
        probe_guard_differs <= 0;
        probe_decrement_hit <= 0;
        if(load) count_value <= data;
        else begin
            probe_guard_hit <= 1;
            probe_guard_differs <= ((count_value != 0) !== (count_value > 0));
            if(count_value != 0) begin
                probe_decrement_hit <= 1;
                count_value <= count_value - 1;
            end
        end
    end
"""
RUN_ENV = {"PATH": f"{ROOT / '.local/bin'}{os.pathsep}{os.environ['PATH']}", "LC_ALL": "C"}


def read_table(data_dir, filename):
    rows = {}
    with (data_dir / f"HDLBits_{filename}.jsonl").open() as stream:
        for line in stream:
            if not line.strip():
                continue
            row = json.loads(line)
            task = row["task_id"]
            if task in rows:
                raise ValueError(f"{filename}: duplicate task ID {task}")
            rows[task] = row
    return rows


def census():
    dirs = {name: ROOT / "sources" / name / "data/HDLBits"
            for name in ("AutoBench", "CorrectBench")}
    official = read_table(dirs["AutoBench"], "data")
    types = read_table(dirs["AutoBench"], "circuit_type")
    mutants = read_table(dirs["AutoBench"], "data_mutants")
    libraries = {
        "autobench_mutants": (mutants, "mutants"),
        "autobench_gptgen_rtl": (read_table(dirs["AutoBench"], "data_RTL"), "gptgen_RTL"),
        "correctbench_mutants": (read_table(dirs["CorrectBench"], "data_mutants"), "mutants"),
    }
    for model in ("4o", "4omini", "sonnet35"):
        variants = read_table(dirs["CorrectBench"], f"data_RTL_{model}_20")
        libraries[f"correctbench_{model}_rtl"] = (variants, "llmgen_RTL")
    if official.keys() != types.keys() or any(official.keys() != rows.keys()
                                             for rows, _ in libraries.values()):
        raise ValueError("Dataset tables do not have identical task ID coverage")

    columns = ("task_number", "task_id", "circuit_type", "spec", "golden_rtl", "golden_tb",
               *libraries)
    totals = {category: {name: Counter() for name in libraries} for category in ("CMB", "SEQ")}
    presence = Counter()
    with (OUT / "dataset_by_task.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for task, row in sorted(official.items(), key=lambda item: item[1]["task_number"]):
            category = types[task]["circuit_type"]
            record = {"task_number": row["task_number"], "task_id": task, "circuit_type": category}
            for label, field in (("spec", "description"), ("golden_rtl", "module_code"),
                                 ("golden_tb", "testbench")):
                record[label] = bool(row[field].strip())
                presence[label] += record[label]
            for name, (rows, field) in libraries.items():
                entries = rows[task][field]
                if not isinstance(entries, list) or any(not x.strip() for x in entries):
                    raise ValueError(f"{name}/{task}: invalid RTL entry")
                record[name] = len(entries)
                totals[category][name][len(entries)] += 1
            writer.writerow(record)
    result = {
        "tasks": dict(Counter(r["circuit_type"] for r in types.values())),
        "field_presence": dict(presence),
        "tasks_by_variant_count": totals,
        "correctbench_identical_base_records": official == read_table(dirs["CorrectBench"], "data"),
        "correctbench_identical_mutant_records": mutants == libraries["correctbench_mutants"][0],
        "correctbench_identical_types": types == read_table(dirs["CorrectBench"], "circuit_type"),
    }
    return official[TASK], mutants[TASK]["mutants"][0], result


def run_logged(args, directory, log):
    started = time.perf_counter()
    result = subprocess.run(args, cwd=directory, env=RUN_ENV, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    (directory / log).write_text(result.stdout)
    return result, round(time.perf_counter() - started, 4)


def simulate(directory, top, *sources):
    directory.mkdir(parents=True, exist_ok=True)
    compile_result, compile_seconds = run_logged(
        ["iverilog", "-g2012", "-s", top, "-o", "sim.vvp", *map(str, sources)],
        directory, "compile.log",
    )
    if compile_result.returncode != 0:
        raise RuntimeError(f"Compilation failed: {directory / 'compile.log'}")
    run_result, simulation_seconds = run_logged(["vvp", "sim.vvp"], directory, "simulation.log")
    return run_result, {"compile_seconds": compile_seconds, "simulation_seconds": simulation_seconds}


def smoke_test():
    directory = OUT / "counter"
    run, elapsed = simulate(directory, "counter_tb", CHECKS / "counter.v", CHECKS / "counter_tb.v")
    if run.returncode or "PASS:" not in run.stdout:
        raise RuntimeError(f"Counter failed: {directory / 'simulation.log'}")
    unit, waves = rising_edges(directory / "counter.vcd", "counter_tb.clk", ("counter_tb.q",))
    values = [int(sample["counter_tb.q"], 2) for _, sample in waves]
    if values != [step % 16 for step in range(21)]:
        raise RuntimeError("Counter waveform differs from expected cycle values")
    return {**elapsed, "timescale": unit, "samples": len(values), "q": values}


def check_official(task, mutant):
    directory = OUT / "official_timer"
    directory.mkdir(exist_ok=True)
    testbench = directory / "golden_tb.v"
    testbench.write_text(task["testbench"])
    checks = {}
    for label, rtl in (("golden", task["module_code"]), ("official_mutant_01", mutant)):
        target = directory / label
        target.mkdir(exist_ok=True)
        source = target / "rtl.v"
        source.write_text(rtl)
        run, elapsed = simulate(target, "tb", source, testbench)
        match = re.search(r"^Mismatches:\s+(\d+) in (\d+) samples", run.stdout, re.MULTILINE)
        if not match:
            raise RuntimeError(f"No golden TB verdict: {target / 'simulation.log'}")
        mismatches, samples = map(int, match.groups())
        checks[label] = {**elapsed, "vvp_exit_code": run.returncode, "mismatches": mismatches,
                         "samples": samples, "passed": run.returncode == 0 and mismatches == 0}
    if not checks["golden"]["passed"] or checks["official_mutant_01"]["mismatches"] == 0:
        raise RuntimeError(f"Unexpected golden TB verdict: {checks}")
    return checks


def replace_one(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Expected one mutation or instrumentation site: {old}")
    return source.replace(old, new, 1)


def classify(reference, mutant, rule, *, limit=None):
    unit, baseline = rising_edges(reference, CLOCK, (*WAVE_SIGNALS, *PROBES))
    mutant_unit, changed = rising_edges(mutant, CLOCK, WAVE_SIGNALS)
    if unit != mutant_unit or [t for t, _ in baseline] != [t for t, _ in changed]:
        raise ValueError("Waveforms have different clock edges or timescales")
    hits, infections, exposures, intervals = [], [], [], []
    active = None
    for cycle, ((tick, before), (_, after)) in enumerate(zip(baseline[:limit], changed[:limit]), 1):
        if any(before[name] != after[name] for name in INPUTS):
            raise ValueError(f"Input mismatch at cycle {cycle}")
        if any(set(value) - {"0", "1"} for value in (*before.values(), *after.values())):
            raise ValueError(f"Unknown value at cycle {cycle}")
        output_differs = before[OUTPUT] != after[OUTPUT]
        internal_differs = before[INTERNAL] != after[INTERNAL]
        if rule == "decrement_constant":
            hit = before[DECREMENT_HIT] == "1"
            # Mask to the assignment width and compare both RHSs on the same pre-state.
            # The golden post-state gives pre_state - 1 when that branch executes.
            mask = (1 << len(before[INTERNAL])) - 1
            pre_state = (int(before[INTERNAL], 2) + 1) & mask
            infected = hit and ((pre_state - 1) & mask) != ((pre_state - 3) & mask)
        elif rule == "guard_operator":
            hit = before[GUARD_HIT] == "1"
            infected = hit and before[GUARD_DIFFERS] == "1"
        else:
            hit, infected = True, output_differs  # Continuous comparison feeds the output.
        if hit:
            hits.append(cycle)
        if infected:
            infections.append(cycle)
        if output_differs:
            exposures.append(cycle)
        if internal_differs and active is None:
            active = {
                "signal": INTERNAL, "first_cycle": cycle, "first_tick": tick,
                "first_golden_value": int(before[INTERNAL], 2),
                "first_mutant_value": int(after[INTERNAL], 2),
            }
        if active is not None and not internal_differs:
            intervals.append({**active, "last_different_cycle": cycle - 1,
                              "first_equal_cycle": cycle, "first_equal_tick": tick})
            active = None
    sample_count = len(baseline[:limit])
    if active is not None:
        intervals.append({**active, "last_different_cycle": sample_count,
                          "first_equal_cycle": None, "first_equal_tick": None})

    if exposures and not infections:
        raise ValueError("Output difference without an observed mutation-site infection")
    if exposures:
        classification = "已暴露"
    elif infections:
        classification = "未传播"
    elif hits:
        classification = "未感染"
    else:
        classification = "未到达"
    return {
        "classification": classification, "cycles": sample_count, "timescale": unit,
        "reached_cycles": hits, "infected_cycles": infections, "exposed_cycles": exposures,
        "internal_difference_intervals": intervals,
    }


def mutation_diagnostics(golden_rtl):
    directory = OUT / "timer_diagnostics"
    golden_with_probes, process_count = TIMER_PROCESS.subn(PROBED_TIMER_PROCESS, golden_rtl)
    if process_count != 1:
        raise ValueError("Expected one timer process to instrument")
    sources = {"golden": golden_rtl, "golden_probes": golden_with_probes}
    sources.update({rule: replace_one(golden_rtl, *replacement) for rule, replacement in RULES.items()})
    timings = {}
    for label, rtl in sources.items():
        target = directory / label
        target.mkdir(parents=True, exist_ok=True)
        source = target / "rtl.v"
        source.write_text(rtl)
        run, timings[label] = simulate(target, "timer_random_tb", source, CHECKS / "timer_random_tb.v")
        if run.returncode:
            raise RuntimeError(f"Simulation failed: {target / 'simulation.log'}")
    baseline = directory / "golden_probes" / "timer.vcd"
    if rising_edges(directory / "golden" / "timer.vcd", CLOCK, WAVE_SIGNALS) != rising_edges(
        baseline, CLOCK, WAVE_SIGNALS
    ):
        raise RuntimeError("Instrumentation changed the original timer waveform")
    results = {
        rule: {**classify(baseline, directory / rule / "timer.vcd", rule), **timings[rule]}
        for rule in RULES
    }
    prefix = classify(baseline, directory / "decrement_constant" / "timer.vcd",
                      "decrement_constant", limit=1)
    expected = ("未传播", "未感染", "已暴露")
    if tuple(r["classification"] for r in results.values()) != expected or (
        prefix["classification"] != "未到达"
    ):
        raise RuntimeError(f"Unexpected diagnostic verdicts: {results}, {prefix}")
    return {"golden": timings["golden"], "variants": results, "load_only_prefix": prefix}


def main():
    parser = argparse.ArgumentParser(description="Run the offline preflight or compare a VCD pair.")
    commands = parser.add_subparsers(dest="command")
    compare = commands.add_parser("compare")
    compare.add_argument("rule", choices=RULES)
    compare.add_argument("reference", type=Path)
    compare.add_argument("mutant", type=Path)
    args = parser.parse_args()
    if args.command == "compare":
        result = classify(args.reference, args.mutant, args.rule)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    OUT.mkdir(exist_ok=True)
    timer, official_mutant, datasets = census()
    results = {
        "counter": smoke_test(),
        "datasets": datasets,
        "official_timer": check_official(timer, official_mutant),
        "timer_diagnostics": mutation_diagnostics(timer["module_code"]),
    }
    report = OUT / "offline_results.json"
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(f"Offline checks passed. Results: {report}")


if __name__ == "__main__":
    main()
