"""Cache bounded evidence for the fixed guidance group only."""

import subprocess
import sys
import threading
import time

from common import REPO, ROOT, load, protocol, save
from guide import span
from hdl import WORK, bind_params, compile_sim, input_dir, observe
from replay import SimulationError, rename

sys.path.append(str(REPO / "equiv-audit"))
from formal import assertion, config, module, vcd_rows

LOCK = threading.Lock()
PER_MUTANT = {}
SOLVERS = threading.BoundedSemaphore(4)


def vectors_from_witness(signals, inputs):
    groups = []
    for i in range(0, len(signals), 4):
        cycle = signals[i:i + 4]
        before = cycle[min(1, len(cycle)-1)]
        row = {k: int(before["in_"+k], 2) for k in inputs}
        if len(cycle) == 4:
            mid = {k: int(cycle[3]["in_"+k], 2) for k in inputs
                   if cycle[3].get("in_"+k) != before["in_"+k]}
            if mid:
                row["mid"] = mid
        groups.append(row)
    if groups:
        # An output updated on the last edge may become observable on the next one.
        groups.append({k: groups[-1].get("mid", {}).get(k, groups[-1][k]) for k in inputs})
    return groups


def compressed(rows, last):
    groups = []
    for i, row in enumerate(rows[:last], 1):
        if groups and groups[-1]["input"] == row:
            groups[-1]["through"] = i
        else:
            groups.append({"from": i, "through": i, "input": row})
    if len(groups) > 9:
        return groups[:3] + [{"omitted_input_changes": len(groups)-9}] + groups[-6:]
    return groups


def solve(row, item, destination):
    task = row["id"]
    atom = item["edit"]
    ports = row["ports"]
    directory = WORK / "formal" / task / item["id"]
    directory.mkdir(parents=True, exist_ok=True)
    variant = span(row, atom)
    for file, code in (("golden.sv", rename(row["gold"], "cvdp_r_")),
                       ("mutant.sv", rename(variant, "cvdp_m_")),
                       ("assertion.sv", assertion(ports)),
                       ("miter.sv", bind_params(module(ports), ports["top"], ports["parameters"]))):
        (directory / file).write_text(code)
    plan = protocol()
    cfg = config(4*plan["formal_cycles"]+1, engine="smtbmc boolector", timeout=plan["formal_timeout_seconds"])
    (directory / "proof.sby").write_text(cfg)
    with SOLVERS:
        started = time.monotonic()
        try:
            p = subprocess.run(["sby", "-f", "proof.sby"], cwd=directory, text=True, capture_output=True,
                               timeout=18)
            log = p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            log = ""
    seconds = time.monotonic() - started
    job = directory / "proof"
    status = (job / "status").read_text().split()[0] if (job / "status").exists() else "TIMEOUT"
    result = {"task": task, "id": item["id"], "cycles_requested": plan["formal_cycles"],
              "solve_wall_seconds": round(seconds, 3), "status": status}
    trace = next(job.glob("engine_*/trace.vcd"), None)
    if status == "FAIL" and trace:
        try:
            signals = vcd_rows(trace)
            vectors = vectors_from_witness(signals, ports["input"])
            where = input_dir(directory / "concrete", vectors, ports)
            observed = observe(compile_sim(row["gold"], variant, ports), where, len(vectors))
        except (KeyError, ValueError, RuntimeError, SimulationError) as exc:
            result.update(status="unverified", reason=str(exc)[-350:])
        else:
            if observed["samples"]:
                state = signals[-1]
                sample = {"golden_outputs_binary": state.get("gold"), "unknown_mask": state.get("gold_x"),
                          "witness_phase": state.get("phase"), "G_site": atom["before"].strip()}
                # The concrete sequence is retained in full. Prompt receives only
                # the condensed early and terminal input changes.
                result.update(status="witness", cycles=observed["first"], compressed=compressed(vectors, observed["first"]),
                              state=sample, concrete_inputs=vectors)
            else:
                result.update(status="unverified", reason="Witness did not expose the G mutant in dual-edge Icarus replay")
    elif status != "PASS":
        result["reason"] = next((l.split("ERROR:", 1)[-1].strip() for l in log.splitlines() if "ERROR:" in l),
                                status)
    save(destination, result)
    return result


def evidence(row, item):
    task = row["id"]
    path = ROOT / "guidance" / task / "formal" / f"{item['id']}.json"
    with LOCK:
        lock = PER_MUTANT.setdefault((task,item["id"]), threading.Lock())
    with lock:
        return load(path) if path.exists() else solve(row, item, path)
