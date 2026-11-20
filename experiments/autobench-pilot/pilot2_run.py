import argparse
import fcntl
import hashlib
import json
import os
import random
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pilot2_checker import CASE_NAMES, feedback as checker_feedback
from pilot2_evaluation import batch_prescreen, stage_score
from pilot2_generate import BASE, ROOT, atomic, load, save, settings, source
from pilot2_guidance import build_catalog, diagnostic_lines, exposure
from pilot2_prepare import stage
from pilot2_screen_vectors import generator
from pilot2_sim import interface_from, replay
from run_pilot import git_commit, totals
from simulate import RunError, differences, expected_from, vectors_from


def commit(paths, message):
    folder = ROOT / ".scratch"
    folder.mkdir(exist_ok=True)
    with (folder / "git.lock").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        return git_commit(ROOT, [Path(path).relative_to(ROOT) for path in paths], message)


def validated(where, role, iteration, spec, interface, plan, validator, *,
              message="", previous=""):
    stem = f"{'stimulus' if role == 'append' else role}_{iteration:02d}"
    for fix in range(plan["compile_repairs"] + 1):
        suffix = f"_repair{fix}" if fix else ""
        code = source(where, stem + suffix + ".py", spec, interface, role, plan, message, previous)
        try:
            return code, validator(code)
        except (RunError, subprocess.TimeoutExpired, ValueError) as exc:
            if fix == plan["compile_repairs"]:
                raise
            previous = code
            message = "Fix the source implementation error only.\n" + str(exc)
    raise AssertionError("Repair loop was not entered")


def append_batch(active, groups, next_group):
    if next_group >= len(groups):
        return False, next_group
    new = [m for m in groups[next_group]["candidates"] if m["retained"]]
    if not new:
        return False, next_group + 1
    active.extend(new)
    return True, next_group + 1


def trial(phase, task, cfg, rep, seed, plan, catalogue):
    where = BASE / "runs" / phase / task / cfg / f"rep{rep}"
    result_file = where / "result.json"
    plan_hash = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
    if result_file.is_file():
        frozen = load(result_file)
        if frozen.get("status") == "complete":
            if frozen["plan_sha256"] != plan_hash:
                raise ValueError("Checkpoint differs from the locked experiment plan")
            return where, frozen
    started = time.monotonic()
    public_files = BASE / "generation" / task
    spec = load(public_files / "problem.json")
    interface = interface_from(spec)
    ins, outs, _, _ = interface
    initial, vectors = validated(where, "stimulus", 1, spec, interface, plan,
                                 lambda code: vectors_from(code, ins, seed, plan["stimulus_cycles"]))
    checker, expected = validated(where, "checker", 1, spec, interface, plan,
                                  lambda code: expected_from(code, outs, vectors))
    snapshots = []
    records = []
    stop = "A0_single_round" if cfg == "A0" else "round_limit"
    if catalogue:
        original = [(public_files / f"R{i}.v").read_text() for i in range(1, 4)]
        cohorts = catalogue["groups"]
        active = [m for m in cohorts[0]["candidates"] if m["retained"]]
    else:
        original, active, cohorts = [], [], []
    next_group = 1
    added, streak = False, 0
    exposure_cache = {}
    last_checker_message = ""
    for number in range(1, (1 if cfg == "A0" else plan["max_rounds"]) + 1):
        bench = replay(interface, vectors)
        observations = []
        if catalogue:
            key = len(vectors)
            cache = exposure_cache.setdefault(key, {"observations": None, "seen": {}, "processed": set()})
            if cache["observations"] is None:
                cache["observations"] = [bench.trace(text)[0] for text in original]
            observations = cache["observations"]
            untested = [m for m in active if m["id"] not in cache["processed"]]
            cache["seen"].update(exposure(untested, original[0], bench, observations[0]))
            cache["processed"].update(m["id"] for m in untested)
            exposed = dict(cache["seen"])
        else:
            exposed = {}
        if records and not set(records[-1]["exposed"]).issubset(exposed):
            raise RuntimeError("Append-only exposure lost a previously observed mutant")
        saturated = bool(active) and len(exposed) == len(active)
        if added:
            streak = streak + 1 if saturated else 0
        elif not saturated:
            streak = 0
        item = {"round": number, "cycles": len(vectors), "active_G_total": len(active),
                "exposed": sorted(exposed), "active_G_rate": len(exposed) / len(active) if active else None,
                "introduced_new_batch": added, "consecutive_fully_exposed_new_batches": streak}
        snapshots.append((list(vectors), expected, checker))
        records.append(item)
        if cfg == "A0":
            break
        sd, cd = ({}, {"counts": dict.fromkeys(CASE_NAMES, 0)})
        s_message = c_message = ""
        if observations:
            if not saturated:
                s_message, sd = diagnostic_lines(active, original[0], bench, exposed, cfg[0])
            c_message, cd = checker_feedback(spec, vectors, expected, observations, exposed, cfg[2])
        item.update({"stimulus_feedback": s_message, "stimulus_diagnostics": sd,
                     "checker_feedback": c_message, "checker_diagnostics": cd})
        save(where / f"round_{number:02d}.json", item)
        if streak >= 2:
            stop = "two_fully_exposed_new_batches"
            break
        if number == plan["max_rounds"]:
            break
        added = False
        if saturated:
            added, next_group = append_batch(active, cohorts, next_group)
        if s_message:
            segment, appended = validated(
                where, "append", number + 1, spec, interface, plan,
                lambda code: vectors_from(code, ins, seed + number, plan["append_cycles"]),
                message=s_message,
            )
            vectors = vectors + appended
        if c_message and c_message != last_checker_message:
            checker, expected = validated(where, "checker", number + 1, spec, interface, plan,
                                          lambda code: expected_from(code, outs, vectors),
                                          message=c_message, previous=checker)
            last_checker_message = c_message
        else:
            expected = expected_from(checker, outs, vectors)

    if active:
        first_difference = {tag: min(i for i, *_ in differences(observations[0], trace)) + 1
                            for tag, trace in exposed.items()}
        for item, (samples, _, _) in zip(records, snapshots, strict=True):
            common = sum(cycle <= len(samples) for cycle in first_difference.values())
            item["fixed_G_exposed"] = common
            item["fixed_G_total"] = len(active)
            item["fixed_G_rate"] = common / len(active)
        if any(b["fixed_G_rate"] < a["fixed_G_rate"] for a, b in zip(records, records[1:])):
            raise RuntimeError("Fixed-denominator guidance exposure declined")
    # Only after model generation for this configuration is closed.
    scores = []
    for item, (samples, answers, _) in zip(records, snapshots, strict=True):
        outcome = stage_score(task, replay(interface, samples), answers)
        scores.append(outcome)
        item["held_out"] = {field: value for field, value in outcome.items() if field != "H_cases"}
        save(where / f"round_{item['round']:02d}.json", item)
    save(where / "final_vectors.json", vectors)
    save(where / "final_expected.json", expected)
    atomic(where / "final_checker.py", checker)
    save(where / "stimulus_snapshots.json", [samples for samples, _, _ in snapshots])
    counter = {key: sum(row.get("checker_diagnostics", {}).get("counts", {}).get(key, 0)
                        for row in records) for key in CASE_NAMES}
    result = {"phase": phase, "task": task, "config": cfg, "repeat": rep, "seed": seed,
              "plan_sha256": plan_hash,
              "status": "complete", "rounds": len(records), "stop_reason": stop,
              "seconds": round(time.monotonic() - started, 3),
              "case_counts": counter, "per_round": records,
              **scores[-1], **totals(where / "calls.jsonl")}
    save(result_file, result)
    return where, result


def batch(phase, tasks, plan, workers, guidance, repeats, *, only=None):
    spec_by_task = {task: load(BASE / "generation" / task / "problem.json") for task in tasks}
    if guidance:
        generic = generator(plan)
        def guide(task):
            spec = spec_by_task[task]
            r1 = (BASE / "generation" / task / "R1.v").read_text()
            try:
                dataset = build_catalog(task, spec, interface_from(spec), r1, generic, plan)
                commit([BASE / "guidance" / task], f"Screen v2 guidance sets for {task}")
                return task, dataset
            except (RunError, ValueError) as exc:
                print("guidance blocked", task, str(exc), flush=True)
                return task, None

        with ThreadPoolExecutor(max_workers=min(4, workers)) as pool:
            catalogues = dict(pool.map(guide, tasks))
    else:
        catalogues = dict.fromkeys(tasks)
    configs = plan["configs"] if guidance else ["A0"]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {}
        for rep, seed in enumerate(repeats, 1):
            for config in configs:
                for task in tasks:
                    if only and (task, config, rep) not in only:
                        continue
                    def run(task=task, config=config, rep=rep, seed=seed):
                        if config != "A0" and catalogues[task] is None:
                            raise RunError("R1 was unusable for screened guidance")
                        return trial(phase, task, config, rep, seed, plan, catalogues[task])
                    jobs[pool.submit(run)] = (task, config, rep)
        outcomes = []
        for future in as_completed(jobs):
            task, config, rep = jobs[future]
            try:
                folder, result = future.result()
                sha = commit([folder], f"Complete v2 {phase} {task} {config} repeat {rep}")
                print(f"{phase} {task} {config} r{rep} {result['H_detected']}/{result['H_total']} {sha[:8]}",
                      flush=True)
            except Exception as exc:
                folder = BASE / "runs" / phase / task / config / f"rep{rep}"
                result = {"status": "blocked", "phase": phase, "task": task, "config": config,
                          "repeat": rep, "reason": f"{type(exc).__name__}: {exc}"}
                save(folder / "result.json", result)
                sha = commit([folder], f"Record blocked v2 {phase} {task} {config} repeat {rep}")
                print("blocked", phase, task, config, rep, result["reason"], sha[:8], flush=True)
            outcomes.append(result)
    return outcomes


def select(results, tasks, plan):
    by_task = {row["task"]: row for row in results}
    rows = []
    for task in tasks:
        trial = by_task[task["task_id"]]
        if trial["status"] != "complete":
            eligibility = "unscored"
        elif trial["H_total"] == 0:
            eligibility = "no_valid_H"
        elif trial["H_detected"] == trial["H_total"]:
            eligibility = "ceiling"
        else:
            eligibility = "retained"
        rows.append({**task, "eligibility": eligibility, "H_detected": trial.get("H_detected"),
                     "H_total": trial.get("H_total"), "golden_pass": trial.get("golden_pass")})
    return rows


def calibrate(plan, sources, workers):
    task_file = BASE / "initial_tasks.json"
    tasks = load(task_file)
    results = batch("calibration", [r["task_id"] for r in tasks], plan, workers,
                    False, [plan["calibration_seed"]])
    rows = select(results, tasks, plan)
    if sum(row["eligibility"] == "retained" for row in rows) < plan["minimum_calibration_eligible"]:
        tasks = stage(sources, all_tasks=True)
        for path in ("all_tasks.json", "generation", "eval"):
            commit([BASE / path], f"Stage expanded v2 calibration asset {path}")
        batch_prescreen(BASE / "all_tasks.json", 4, plan)
        commit([BASE / "eval", BASE / "reports" / "h_prescreen_all.csv"], "Prescreen expanded H cohort")
        results = batch("calibration", [r["task_id"] for r in tasks], plan, workers,
                        False, [plan["calibration_seed"]])
        rows = select(results, tasks, plan)
    retained = [row for row in rows if row["eligibility"] == "retained"]
    selected = random.Random(plan["selection_seed"]).sample(retained, min(len(retained), plan["second_pilot_count"]))
    output = BASE / "reports" / "selection.json"
    save(output, {"calibration_seed": plan["calibration_seed"], "selection_seed": plan["selection_seed"],
                  "candidates": rows, "selected": selected})
    commit([output], "Freeze v2 A0 calibration and six-task selection")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("calibrate", "rerun", "second"))
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--sources", type=Path, default=ROOT / "sources")
    args = parser.parse_args()
    if not os.environ.get("OPENCODE_GO_API_KEY", "").strip():
        raise SystemExit("Missing OPENCODE_GO_API_KEY")
    plan = settings()
    if args.phase == "calibrate":
        calibrate(plan, args.sources.resolve(), args.workers)
        return
    if args.phase == "rerun":
        tasks = load(ROOT / "sample.json")
        repeats = plan["repeat_seeds"][:1]
    else:
        tasks = load(BASE / "reports" / "selection.json")["selected"]
        if len(tasks) != plan["second_pilot_count"]:
            raise SystemExit("The calibration did not produce six scorable non-ceiling tasks")
        repeats = plan["repeat_seeds"]
    batch(args.phase, [r["task_id"] for r in tasks], plan, args.workers, True, repeats)


if __name__ == "__main__":
    main()
