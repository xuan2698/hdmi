import csv
from concurrent.futures import ThreadPoolExecutor

from pilot2_generate import BASE, load, save, settings
from pilot2_screen_vectors import generator, random_rows
from pilot2_sim import VectorReplay, interface_from
from simulate import RunError, differences, mismatches


def prescreen(task, plan, code):
    base = BASE / "eval" / task
    result = base / "prescreen.json"
    if result.exists():
        return load(result)
    problem = load(BASE / "generation" / task / "problem.json")
    rows = []
    official = sorted((base / "official_mutants").glob("*.v"))
    try:
        interface = interface_from(problem)
        benches = [VectorReplay(interface, run, all_edges=True)
                   for run in random_rows(code, problem, interface[0], plan)]
        golden = (base / "golden_rtl.v").read_text()
        references = [bench.trace(golden)[0] for bench in benches]
    except (RunError, ValueError) as exc:
        diagnostic = {"task": task, "status": "blocked_golden", "reason": str(exc),
                      "total": len(official), "invalid": 0, "suspected_equivalent": 0,
                      "kept": 0, "unclassified": len(official), "mutants": []}
        save(result, diagnostic)
        return diagnostic
    for item in official:
        rtl = item.read_text()
        try:
            observed = [bench.trace(rtl)[0] for bench in benches]
        except (RunError, ValueError) as exc:
            reason = str(exc)
            status = "invalid_compile" if "iverilog exited" in reason else "invalid_simulation"
            rows.append({"id": item.stem, "status": status, "reason": reason})
            continue
        counts = [sum(a != b for a, b in zip(ref, obs, strict=True))
                  for ref, obs in zip(references, observed, strict=True)]
        rows.append({"id": item.stem, "status": "kept" if any(counts) else "suspected_equivalent",
                     "different_samples_by_seed": counts})
    diagnostic = {"task": task, "status": "complete", "total": len(official), "unclassified": 0,
                  "seeds": plan["screen_seeds"], "cycles_per_seed": plan["screen_cycles"],
                  "samples_per_cycle": 3,
                  "invalid": sum(r["status"].startswith("invalid") for r in rows),
                  "suspected_equivalent": sum(r["status"] == "suspected_equivalent" for r in rows),
                  "kept": sum(r["status"] == "kept" for r in rows), "mutants": rows}
    save(result, diagnostic)
    return diagnostic


def batch_prescreen(task_file, workers=4, plan=None):
    plan = plan or settings()
    code = generator(plan)
    tasks = load(task_file)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda row: prescreen(row["task_id"], plan, code), tasks))
    stem = "h_prescreen_all" if len(results) > 25 else "h_prescreen_25"
    reports = BASE / "reports"
    reports.mkdir(exist_ok=True)
    columns = ("task_number", "task", "status", "total", "invalid", "suspected_equivalent",
               "kept", "unclassified", "reason")
    with (reports / f"{stem}.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({**result, "task_number": task["task_number"]}
                         for task, result in zip(tasks, results, strict=True))
    return results


def stage_score(task, bench, expected):
    folder = BASE / "eval" / task
    screen = load(folder / "prescreen.json")
    if screen["status"] != "complete":
        raise RunError("Evaluation prescreen status is " + screen["status"])
    golden, _ = bench.trace((folder / "golden_rtl.v").read_text())
    goracle = mismatches(expected, golden)
    golden_cycles = [i + 1 for i, names in enumerate(goracle) if names]
    cases = []
    for entry in screen["mutants"]:
        if entry["status"] != "kept":
            continue
        i = entry["id"]
        try:
            observed, _ = bench.trace((folder / "official_mutants" / f"{i}.v").read_text())
        except (RunError, ValueError) as exc:
            cases.append({"id": i, "verdict": "simulation_error", "reason": str(exc)})
            continue
        wrong = mismatches(expected, observed)
        output = differences(golden, observed)
        extra = sum(len(a - b) for a, b in zip(wrong, goracle, strict=True))
        verdict = ("detected" if extra else "checker_missed" if output else "not_exposed")
        cases.append({"id": i, "verdict": verdict, "raw_checker_failure": any(wrong),
                      "exposed": bool(output), "additional_mismatch_count": extra})
    return {"golden_pass": not golden_cycles, "golden_mismatch_cycles": golden_cycles,
            "H_total": len(cases), "H_exposed": sum(c.get("exposed", False) for c in cases),
            "H_detected": sum(c["verdict"] == "detected" for c in cases),
            "H_not_exposed": sum(c["verdict"] == "not_exposed" for c in cases),
            "H_checker_missed": sum(c["verdict"] == "checker_missed" for c in cases),
            "H_simulation_errors": sum(c["verdict"] == "simulation_error" for c in cases),
            "H_cases": cases}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    rows = batch_prescreen(BASE / ("all_tasks.json" if args.all else "initial_tasks.json"), args.workers)
    for r in rows:
        print(r["task"], r["status"], r["invalid"], r["suspected_equivalent"], r["kept"], flush=True)
