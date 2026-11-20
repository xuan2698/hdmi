#!/usr/bin/env python3
"""Prepare isolated CorrectBench inputs for a caller-supplied ordered task sample."""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from evaluation_io import ROOT, read_table, simulate


def put_once(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = content.encode()
    if path.is_file() and path.read_bytes() == encoded:
        return
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(encoded)
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != encoded:
                raise ValueError(f"Existing pilot input differs: {path}") from None
    finally:
        Path(temporary).unlink(missing_ok=True)


def prepare(task_ids, target, sources, *, write_sample=True):
    auto = sources / "AutoBench/data/HDLBits"
    correct = sources / "CorrectBench/data/HDLBits"
    types = read_table(auto, "circuit_type")
    problems = read_table(auto, "data")
    mutants = read_table(auto, "data_mutants")
    proxies = read_table(correct, "data_RTL_4o_20")

    if len(set(task_ids)) != len(task_ids):
        raise ValueError("The ordered sample contains duplicate task IDs")
    sample = []
    for task_id in task_ids:
        if not re.fullmatch(r"[a-zA-Z0-9_]+", task_id):
            raise ValueError("Invalid task ID")
        if types[task_id]["circuit_type"] != "SEQ":
            raise ValueError(f"Expected a sequential task: {task_id}")

        problem = problems[task_id]
        variants = proxies[task_id]["llmgen_RTL"][:3]
        if len(variants) != 3 or any(not rtl.strip() for rtl in variants):
            raise ValueError(f"Expected three GPT-4o proxy RTLs: {task_id}")
        evaluation = target / "eval" / task_id
        generation = target / "generation" / task_id
        put_once(evaluation / "golden_rtl.v", problem["module_code"])
        put_once(evaluation / "golden_tb.v", problem["testbench"])
        for i, variant in enumerate(mutants[task_id]["mutants"], start=1):
            put_once(evaluation / "official_mutants" / f"{i:02d}.v", variant)
        details = {"task_id": task_id, "task_number": problem["task_number"],
                   "spec": problem["description"], "module_header": problem["header"]}
        put_once(generation / "problem.json", json.dumps(details, ensure_ascii=False, indent=2) + "\n")
        for i, proxy in enumerate(variants, start=1):
            put_once(generation / f"R{i}.v", proxy)
        sample.append({k: details[k] for k in ("task_id", "task_number")})
    if write_sample:
        put_once(target / "sample.json", json.dumps(sample, indent=2) + "\n")


def score_proxies(target, task_ids):
    for task_id in task_ids:
        evaluation = target / "eval" / task_id
        generation = target / "generation" / task_id
        result = {}
        for i in range(1, 4):
            name = f"R{i}"
            directory = evaluation / "proxy_checks" / name
            try:
                run, elapsed = simulate(directory, "tb", generation / f"{name}.v",
                                        evaluation / "golden_tb.v")
            except RuntimeError:
                result[name] = {"verdict": "compile_error"}
                continue
            except subprocess.TimeoutExpired as exc:
                result[name] = {"verdict": "timeout", "seconds": exc.timeout}
                continue
            mismatch = re.search(r"^Mismatches:\s+(\d+) in (\d+) samples", run.stdout, re.MULTILINE)
            if mismatch is None or run.returncode:
                result[name] = {"verdict": "simulation_error", "vvp_exit_code": run.returncode,
                                **elapsed}
                continue
            errors, count = map(int, mismatch.groups())
            result[name] = {"verdict": "passed" if errors == 0 else "failed", "mismatches": errors,
                            "samples": count, **elapsed}
        (evaluation / "proxy_checks" / "results.json").write_text(json.dumps(result, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--sources", type=Path, default=ROOT / "sources")
    parser.add_argument("--score-proxies", action="store_true")
    parser.add_argument("task_ids", nargs="+")
    args = parser.parse_args()
    target = args.target.resolve()
    prepare(args.task_ids, target, args.sources.resolve())
    if args.score_proxies:
        score_proxies(target, args.task_ids)


if __name__ == "__main__":
    main()
