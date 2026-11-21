"""Run the append-only development configurations without access to H."""

import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import ROOT, generate, get_vectors, load, protocol, public, sample_path, save
from diagnose import diagnose
from formal_g import evidence
from guide import prepare, span
from hdl import WORK, compile_sim, input_dir, observe
from mutations import Candidate

LOCK = threading.Lock()
PER_SEED = {}


def measure(row, remaining, folder, cycles):
    return [item["id"] for item in remaining
            if observe(compile_sim(row["gold"], span(row, item["edit"]), row["ports"]), folder, cycles)["samples"]]


def shared(row, seed, cases):
    task = row["id"]
    base = sample_path(task, seed)
    first = base / "initial"
    result = load(first / "status.json")
    if result["status"] != "complete":
        return None, set()
    cycles = protocol()["round_cycles"]
    vectors = get_vectors(first, row, seed, cycles)
    where = base / "initial_G.json"
    with LOCK:
        lock = PER_SEED.setdefault((task, seed), threading.Lock())
    with lock:
        if not where.exists():
            folder = input_dir(WORK / "train" / task / str(seed) / "shared", vectors, row["ports"])
            exposed = measure(row, cases, folder, cycles)
            save(where, {"exposed": exposed, "total": len(cases)})
    return vectors, set(load(where)["exposed"])


def current_context(row, seed, cfg, index):
    base = sample_path(row["id"], seed)
    if index == 1:
        where = base / "initial"
    else:
        where = base / cfg / f"round{index}"
    return (where / load(where / "status.json")["source"]).read_text()


def improvements(row, seed, cfg):
    task = row["id"]
    plan = protocol()
    base = sample_path(task, seed) / cfg
    checkpoint = base / "result.json"
    if checkpoint.exists():
        return
    bank = prepare(row)["candidates"]
    vectors, exposed = shared(row, seed, bank)
    if vectors is None:
        save(checkpoint, {"task": task, "seed": seed, "config": cfg, "status": "initial_failed",
                          "G_total": len(bank), "history": []})
        return
    hist = [{"round": 1, "cycles": len(vectors), "exposed": sorted(exposed), "new": sorted(exposed)}]
    last = 1
    stop = "single_generation" if cfg == "A0" else "budget"
    for i in range(2, 2 if cfg == "A0" else plan["max_rounds"]+1):
        missed = [item for item in bank if item["id"] not in exposed]
        if not missed:
            stop = "all_G_exposed"
            break
        work = WORK / "train" / task / str(seed) / cfg
        folder = input_dir(work / f"before{i}", vectors, row["ports"])
        lines, local = [], {}
        for item in missed:
            tag, atom = item["id"], item["edit"]
            lines.append(Candidate(**atom).feedback(tag))
            detail = {}
            if cfg in ("O", "O+F"):
                finding = diagnose(row, atom, folder, len(vectors))
                detail["diagnosis"] = finding
                lines.append(json.dumps(finding, ensure_ascii=False))
            if cfg == "O+F":
                result = evidence(row, item)
                detail["formal_status"] = result["status"]
                if result["status"] == "witness":
                    witness = {k: result[k] for k in ("cycles", "compressed", "state")}
                    detail["formal"] = witness
                    lines.append("Verified bounded witness: " + json.dumps(witness, ensure_ascii=False))
                else:
                    lines.append(f"Bounded witness unavailable ({result['status']}).")
            local[tag] = detail
        dest = base / f"round{i}"
        save(dest / "feedback.json", local)
        edit = generate(dest, row, seed + i-1, evidence="\n".join(lines),
                        previous=current_context(row, seed, cfg, i-1))
        if edit is None:
            stop = "append_failed"
            break
        vectors = vectors + edit
        if len(vectors) > plan["max_cycles"]:
            raise ValueError("Stimulus exceeded the frozen budget")
        after = input_dir(work / f"after{i}", vectors, row["ports"])
        added = set(measure(row, missed, after, len(vectors)))
        exposed |= added
        hist.append({"round": i, "cycles": len(vectors), "exposed": sorted(exposed), "new": sorted(added)})
        last = i
    save(checkpoint, {"task": task, "seed": seed, "config": cfg, "status": "complete",
                      "G_total": len(bank), "last_round": last, "stop": stop, "history": hist})
    print(task, seed, cfg, last, len(exposed), stop, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    p.add_argument("--workers", type=int, default=20)
    args = p.parse_args()
    rows, plan = public(args.dataset), protocol()
    jobs = [(r,s,c) for s in plan["seeds"] for r in rows for c in plan["configs"]]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda job: improvements(*job), jobs))
