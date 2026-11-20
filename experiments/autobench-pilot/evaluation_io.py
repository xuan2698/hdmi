import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMAND_ENV = {"PATH": f"{ROOT / '.local/bin'}{os.pathsep}{os.environ['PATH']}", "LC_ALL": "C"}


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


def simulate(directory, top, *sources):
    directory.mkdir(parents=True, exist_ok=True)

    def run(args, log):
        started = time.perf_counter()
        result = subprocess.run(args, cwd=directory, env=COMMAND_ENV, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
        (directory / log).write_text(result.stdout)
        return result, round(time.perf_counter() - started, 4)

    compiled, compile_seconds = run(
        ["iverilog", "-g2012", "-s", top, "-o", "sim.vvp", *map(str, sources)], "compile.log"
    )
    if compiled.returncode:
        raise RuntimeError(f"Compilation failed: {directory / 'compile.log'}")
    result, simulation_seconds = run(["vvp", "sim.vvp"], "simulation.log")
    return result, {"compile_seconds": compile_seconds, "simulation_seconds": simulation_seconds}
