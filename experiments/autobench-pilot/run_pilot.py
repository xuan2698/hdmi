import argparse
import json
import os
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from feedback import checker_feedback, stimulus_feedback
from generate import generate
from mutations import candidate, screen
from pilot_checkpoint import TaskCheckpoint
from scoring import score_final
from simulate import Replay, RunError, differences, expected_from, ports, vectors_from

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def save(path, data):
    temporary = path.with_suffix(".pending")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def validated(location, problem, plan, role, step, validate, feedback="", previous=""):
    stem = location / f"{role}_{step:02d}"
    for repair in range(plan["compile_repairs"] + 1):
        suffix = "" if repair == 0 else f"_repair{repair}"
        code = generate(location, problem, plan, role, stem.with_name(stem.name + suffix + ".py"),
                        feedback, previous)
        try:
            return code, validate(code)
        except (RunError, subprocess.TimeoutExpired) as exc:
            if repair >= plan["compile_repairs"]:
                raise
            previous = code
            feedback = "Fix only the implementation or interface error below.\n" + str(exc)
    raise AssertionError("Unreachable")


def prepare_screen(task, problem, plan, original):
    location = ROOT / "runs" / task / "screen"
    location.mkdir(parents=True, exist_ok=True)
    record = location / "screening.json"
    if record.exists():
        return read(record)
    ins, outs = ports(problem)
    def stimulus(code):
        return [Replay(ins, outs, vectors_from(code, ins, seed, plan["screen_cycles"]))
                for seed in plan["screen_seeds"]]
    started = time.monotonic()
    _, samples = validated(location, problem, plan, "screen", 1, stimulus)
    result = screen(original, ins, outs, samples)
    result.update({"seeds": plan["screen_seeds"], "cycles_per_seed": plan["screen_cycles"],
                   "seconds": round(time.monotonic() - started, 3)})
    save(record, result)
    return result


def totals(log):
    rows = [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
    received = [r for r in rows if r["status"] == "received"]
    return {
        "calls": len({row["session"] for row in rows if row["attempt"] > 0}),
        "http_attempts": sum(row["attempt"] > 0 for row in rows),
        "prompt_tokens": sum(r["usage"].get("prompt_tokens", 0) for r in received),
        "completion_tokens": sum(r["usage"].get("completion_tokens", 0) for r in received),
        "tokens": sum(r["usage"].get("total_tokens", 0) for r in received),
        "allowance_usd": sum(r["allowance"] for r in received if r.get("allowance") is not None),
        "charged_usd": sum(r["charged_usd"] for r in received if r.get("charged_usd") is not None),
        "calls_with_explicit_charge": sum(r.get("charged_usd") is not None for r in received),
        "calls_with_allowance": sum(r.get("allowance") is not None for r in received),
        "sum_request_seconds": round(sum(row.get("request_seconds", 0) for row in rows), 3),
    }


def trial(task, cfg, plan, screening):
    location = ROOT / "runs" / task / cfg
    location.mkdir(parents=True, exist_ok=True)
    result_path = location / "result.json"
    if result_path.exists():
        return task, cfg, read(result_path)
    started = time.monotonic()
    work = ROOT / "generation" / task
    problem = read(work / "problem.json")
    ins, outs = ports(problem)
    rtl = [(work / f"R{i}.v").read_text() for i in (1, 2, 3)]
    retained = [m for m in screening["variants"] if m["retained"]]
    mutants = {m["id"]: candidate(m).rtl(rtl[0]) for m in retained}
    seed, count = plan["stimulus_seed"], plan["stimulus_cycles"]

    def make_vectors(code):
        return vectors_from(code, ins, seed, count)

    driver, vectors = validated(location, problem, plan, "stimulus", 1, make_vectors)
    checker, expected = validated(location, problem, plan, "checker", 1,
                                  lambda code: expected_from(code, outs, vectors))
    max_rounds = 1 if cfg == "A0" else plan["max_rounds"]
    applied = "", ""
    for iteration in range(1, max_rounds + 1):
        replay = Replay(ins, outs, vectors)
        obs = [replay.trace(source)[0] for source in rtl]
        seen, missed = {}, []
        for label, source in mutants.items():
            test, _ = replay.trace(source)
            if differences(obs[0], test):
                seen[label] = test
            else:
                missed.append(label)
        sf, sd = ("", {}) if cfg == "A0" else stimulus_feedback(retained, rtl[0], replay, missed, cfg[0])
        cf, cd = ("", {}) if cfg == "A0" else checker_feedback(problem, vectors, expected, obs, seen, cfg[2])
        round_record = {"round": iteration, "G_exposed": list(seen), "G_not_exposed": missed,
                        "stimulus_prompt_feedback": sf, "stimulus_diagnostics": sd,
                        "checker_prompt_feedback": cf, "checker_diagnostics": cd}
        save(location / f"round_{iteration:02d}.json", round_record)
        revise_driver, revise_checker = bool(sf and sf != applied[0]), bool(cf and cf != applied[1])
        if iteration == max_rounds or not (revise_driver or revise_checker):
            break
        if revise_driver:
            driver, vectors = validated(location, problem, plan, "stimulus", iteration + 1, make_vectors,
                                        sf, driver)
        if revise_checker:
            checker, expected = validated(location, problem, plan, "checker", iteration + 1,
                                          lambda code: expected_from(code, outs, vectors), cf, checker)
        else:
            expected = expected_from(checker, outs, vectors)
        applied = sf, cf

    result = score_final(ROOT, task, replay, expected)
    (location / "final_stimulus.py").write_text(driver)
    (location / "final_checker.py").write_text(checker)
    save(location / "final_vectors.json", vectors)
    save(location / "final_expected.json", expected)
    timing = location / "initial_timing.json"
    initial_seconds = read(timing)["elapsed_seconds"] if timing.is_file() else 0
    result.update({"task": task, "configuration": cfg, "rounds": iteration,
                   "elapsed_seconds": round(time.monotonic() - started + initial_seconds, 3),
                   "expected_values_checked": sum(v is not None for row in expected for v in row.values()),
                   "G_retained": len(retained), "G_exposed": len(seen),
                   "G_suspected_equivalent": screening["suspected_equivalent"],
                   **totals(location / "calls.jsonl")})
    save(result_path, result)
    return task, cfg, result


def git_commit(destination, paths, message):
    secret = os.environ["OPENCODE_GO_API_KEY"].strip().encode()
    files = []
    for relative in paths:
        target = destination / relative
        files.extend(p for p in (target.rglob("*") if target.is_dir() else [target]) if p.is_file())
    if any(secret in path.read_bytes() for path in files):
        raise RuntimeError("A tracked artifact contains credential material")
    subprocess.run(["git", "add", "--", *map(str, paths)], cwd=destination, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=destination)
    if diff.returncode == 1:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", message],
                       cwd=destination, check=True)
    elif diff.returncode:
        raise RuntimeError("Unable to inspect staged changes")
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=destination).strip()


def commit_result(destination, task, cfg, plan, result):
    run_path = Path("runs") / task / cfg
    if ROOT.resolve() != destination.resolve():
        shutil.copytree(ROOT / run_path, destination / run_path, dirs_exist_ok=True)
    with TaskCheckpoint(destination / "checkpoints", task, plan) as state:
        saved = state.read()
        saved[cfg] = {"result": str(run_path / "result.json"), "rounds": result["rounds"]}
        state.save(saved)
    return git_commit(destination, [run_path, Path("checkpoints") / f"{task}.json"],
                      f"Complete S1 {task} {cfg} and save task checkpoint")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit-dir", type=Path, default=ROOT)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not os.environ.get("OPENCODE_GO_API_KEY", "").strip():
        raise SystemExit("Missing OPENCODE_GO_API_KEY")
    plan = read(ROOT / "plan.json")
    tasks = [entry["task_id"] for entry in read(ROOT / "sample.json")]
    destination = args.commit_dir.resolve()
    kind = "failed"
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}
        for task in tasks:
            work = ROOT / "generation" / task
            problem = read(work / "problem.json")
            screening = prepare_screen(task, problem, plan, (work / "R1.v").read_text())
            setup = Path("runs") / task / "screen"
            if ROOT.resolve() != destination:
                shutil.copytree(ROOT / setup, destination / setup, dirs_exist_ok=True)
            git_commit(destination, [setup], f"Screen guidance mutations for {task}")
            with TaskCheckpoint(destination / "checkpoints", task, plan) as checkpoint:
                progress = checkpoint.read()
            for cfg in plan["configs"]:
                record = progress.get(cfg)
                if record and (destination / record["result"]).is_file():
                    print(f"resume: {task} {cfg} already complete", flush=True)
                else:
                    future = pool.submit(trial, task, cfg, plan, screening)
                    futures[future] = task, cfg
        failures = []
        for future in as_completed(futures):
            task, cfg = futures[future]
            try:
                task, cfg, result = future.result()
                commit = commit_result(destination, task, cfg, plan, result)
                print(f"completed: {task} {cfg} {commit[:10]}", flush=True)
            except Exception as exc:
                failures.append((task, cfg))
                print(f"{kind}: {task} {cfg} {type(exc).__name__}: {exc}", flush=True)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
