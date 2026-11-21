import argparse
import json
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from pilot2_generate import load, save
from pilot2_guidance import exposure
from pilot2_run import append_batch, commit
from pilot2_sim import VectorReplay
from pilot3_checker import bank, feedback
from pilot3_evaluation import archive, evaluate
from pilot3_generate import check_rows, driver_rows, generate
from pilot3_guidance import added_feedback, prepare
from pilot3_inputs import BASE, fingerprint, public, setup, tasks
from simulate import RunError, differences


def stamp():
    return datetime.now(timezone.utc).isoformat()


def ledger(path):
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines()]


def use(rows):
    return {"calls": len({row["session"] for row in rows}), "attempts": len(rows),
            "tokens": sum(row.get("usage", {}).get("total_tokens", 0) for row in rows),
            "allowance_usd": sum(row.get("allowance") or 0 for row in rows),
            "charged_usd": sum(row.get("charged_usd") or 0 for row in rows),
            "request_seconds": round(sum(row.get("request_seconds", 0) for row in rows), 4),
            "truncated": sum(bool(row.get("truncated")) for row in rows),
            "retries": sum(bool(row.get("is_retry")) for row in rows),
            "transport_errors": sum(row["status"] != "received" for row in rows)}


def regenerate_counts(folder):
    return {role: sum(load(path)["regenerations"] for path in folder.glob(f"{role}_*_validation.json"))
            for role in ("checker", "stimulus")}


def fail(where, run, reason, status, task, started):
    size = load(archive(task) / "prescreen.json")["kept"]
    run.update({"status": status, "reason": str(reason), "golden_pass": None, "H_total": size,
                "H_detected": 0, "H_generation_failed": size if status == "generation_failed" else 0,
                "H_infrastructure_failed": size if status == "infrastructure_failed" else 0,
                "seconds": round(time.monotonic() - started, 3), "finished_utc": stamp(),
                "incremental_usage": use(ledger(where / "calls.jsonl")),
                "incremental_regenerations": regenerate_counts(where)})
    save(where / "result.json", run)
    return where, run


def apply_guidance(where, task, cfg, seed, plan, vectors, checker, expect, catalogue):
    spec, interface = public(task)
    ins, outs = interface[:2]
    rounds, issued, cached = [], set(), {}
    if cfg == "A0":
        return vectors, checker, expect, [{"round": 1, "cycles": len(vectors)}], "A0_single_round"
    anchor, guide = catalogue
    cohorts = guide["groups"]
    active = [m for m in cohorts[0]["candidates"] if m["retained"]]
    next_group, new, streak = 1, False, 0
    stop = "round_limit"
    last_checker_feedback = ""
    for round_number in range(1, plan["max_rounds"] + 1):
        bench = VectorReplay(interface, vectors, proxy_compat=True)
        block = cached.get(len(vectors))
        if block is None:
            reference, _ = bench.trace(anchor)
            proxies, missing = bank(task, bench, outs, cfg[2])
            block = {"reference": reference, "proxies": proxies, "missing": missing,
                     "exposed": {}, "processed": set()}
            cached[len(vectors)] = block
        unseen = [record for record in active if record["id"] not in block["processed"]]
        block["exposed"].update(exposure(unseen, anchor, bench, block["reference"]))
        block["processed"].update(record["id"] for record in unseen)
        current = block["exposed"]
        saturated = bool(active) and len(current) == len(active)
        if new and saturated:
            streak += 1
        elif not saturated:
            streak = 0
        row = {"round": round_number, "cycles": len(vectors), "active_G": len(active),
               "exposed": sorted(current), "new_cohort": new,
               "consecutive_new_cohorts_exposed": streak,
               "absent_proxies": sorted(block["missing"])}
        if rounds and not set(rounds[-1]["exposed"]) <= current.keys():
            raise RuntimeError("Appending stimuli changed a prefix exposure")
        rounds.append(row)
        if round_number == plan["max_rounds"] or streak >= 2:
            if streak >= 2:
                stop = "two_fully_exposed_new_batches"
            break

        s_text, s_details = added_feedback(active, anchor, bench, current, cfg[0])
        c_text, c_details = feedback(task, spec, vectors, expect, block["proxies"],
                                     block["reference"], current, cfg[2], issued, plan)
        row.update({"stimulus_diagnostics": s_details, "checker_diagnostics": c_details,
                    "stimulus_sent": bool(s_text), "checker_sent": bool(c_text and c_text != last_checker_feedback)})
        save(where / f"round_{round_number:02d}.json", row)
        new = False
        if saturated:
            new, next_group = append_batch(active, cohorts, next_group)
        if s_text:
            _, suffix, _ = generate(
                where, "stimulus", round_number + 1, task, plan, seed + round_number,
                lambda code: driver_rows(code, ins, seed + round_number, plan["append_cycles"]),
                evidence=s_text,
            )
            vectors = vectors + suffix
        if c_text and c_text != last_checker_feedback:
            checker, expect, _ = generate(where, "checker", round_number + 1, task, plan, seed,
                                           lambda code: check_rows(code, outs, vectors), evidence=c_text,
                                           previous=checker)
            last_checker_feedback = c_text
        elif s_text:
            try:
                expect = check_rows(checker, outs, vectors)
            except (RunError, ValueError) as exc:
                checker, expect, _ = generate(where, "checker", round_number + 1, task, plan, seed,
                                               lambda code: check_rows(code, outs, vectors),
                                               evidence=f"The appended rows triggered a checker failure: {exc}",
                                               previous=checker)
    # A fixed final cohort avoids a changing denominator when plotting rounds.
    first = {tag: min(i for i, *_ in differences(block["reference"], traces)) + 1
             for tag, traces in current.items()}
    for row in rounds:
        row["fixed_G"] = len(active)
        row["fixed_G_exposed"] = sum(cycle <= row["cycles"] for cycle in first.values())
    return vectors, checker, expect, rounds, stop


def trial(task, cfg, rep, seed, plan, catalogue):
    started = time.monotonic()
    where = BASE / "runs" / task / cfg / f"rep{rep}"
    checkpoint = where / "result.json"
    if checkpoint.exists():
        result = load(checkpoint)
        if result["plan_sha256"] != fingerprint(plan):
            raise ValueError("Archived trial differs from the current plan")
        if result["status"] != "infrastructure_failed":
            return where, result
    initial = BASE / "initial" / task / f"rep{rep}"
    deadline = time.monotonic() + 900
    while not (initial / "result.json").is_file():
        if time.monotonic() > deadline:
            raise RunError(f"Initial checkpoint did not finish: {initial}")
        time.sleep(1)
    frozen = load(initial / "result.json")
    run = {"task": task, "configuration": cfg, "repeat": rep, "seed": seed,
           "plan_sha256": fingerprint(plan), "started_utc": stamp(),
           "initial": str(initial.relative_to(BASE)),
           "shared_initial_usage": use(ledger(initial / "calls.jsonl")),
           "shared_initial_regenerations": regenerate_counts(initial)}
    if frozen["status"] != "complete":
        return fail(where, run, frozen["reason"], "generation_failed", task, started)
    initial_vectors = load(initial / "vectors.json")
    try:
        vectors, checker, expected, rounds, stop = apply_guidance(
            where, task, cfg, seed, plan, initial_vectors, (initial / "checker.py").read_text(),
            load(initial / "expected.json"), catalogue,
        )
    except RunError as exc:
        status = "generation_failed" if "regeneration opportunities" in str(exc) else "infrastructure_failed"
        return fail(where, run, exc, status, task, started)
    if vectors[:len(initial_vectors)] != initial_vectors:
        raise RuntimeError("Initial stimulus prefix changed")
    _, interface = public(task)
    expected = check_rows(checker, interface[1], vectors)
    score = evaluate(task, VectorReplay(interface, vectors), expected)
    if sum(score[k] for k in ("H_detected", "H_not_exposed", "H_checker_missed",
                               "H_golden_failed", "H_simulation_errors")) != score["H_total"]:
        raise ValueError("Evaluation outcomes must partition H")
    for row in rounds:
        save(where / f"round_{row['round']:02d}.json", row)
    save(where / "final_vectors.json", vectors)
    save(where / "final_expected.json", expected)
    (where / "final_checker.py").write_text(checker)
    run.update({"status": "complete", "cycles": len(vectors), "rounds": len(rounds), "stop_reason": stop,
                "guidance": rounds, "seconds": round(time.monotonic() - started, 3),
                "finished_utc": stamp(), **score, "incremental_usage": use(ledger(where / "calls.jsonl")),
                "incremental_regenerations": regenerate_counts(where)})
    save(checkpoint, run)
    return where, run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=26)
    parser.add_argument("--no-commit", action="store_true")
    args = parser.parse_args()
    plan = setup()
    names = [item["task_id"] for item in tasks()]
    catalogues = {task: prepare(task, plan) for task in names}
    counters = Counter()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(trial, task, cfg, rep, seed, plan, catalogues[task]): (task, cfg, rep)
                for rep, seed in enumerate(plan["repeat_seeds"], 1)
                for cfg in plan["configs"] for task in names}
        for future in as_completed(jobs):
            task, cfg, rep = jobs[future]
            try:
                where, result = future.result()
                if not args.no_commit:
                    sha = commit([where], f"Archive v3 {task} {cfg} repeat {rep}")
                else:
                    sha = "-"
                counters[result["status"]] += 1
                print(sum(counters.values()), task, cfg, rep, result["status"],
                      result["H_detected"], "/", result["H_total"], sha[:8], flush=True)
            except Exception as exc:
                counters["unarchived"] += 1
                print("error", task, cfg, rep, type(exc).__name__, str(exc), flush=True)
    print(dict(counters), flush=True)
    return bool(counters["unarchived"] or counters["infrastructure_failed"])


if __name__ == "__main__":
    raise SystemExit(main())
