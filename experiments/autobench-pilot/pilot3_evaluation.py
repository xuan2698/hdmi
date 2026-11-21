import argparse
import csv
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pilot2_generate import load, save
from pilot2_screen_vectors import random_rows
from pilot2_sim import VectorReplay
from pilot3_inputs import BASE, PREVIOUS, public, setup, tasks
from postpilot_analysis import golden_proxy_result
from simulate import RunError, differences


def archive(task):
    return BASE / "eval" / task


def upstream(task):
    return PREVIOUS / "eval" / task


def screen(task, plan, code):
    where = archive(task) / "prescreen.json"
    if where.is_file():
        return load(where)
    source = upstream(task)
    spec, interface = public(task)
    ref = (source / "golden_rtl.v").read_text()
    replays = [VectorReplay(interface, vectors, all_edges=True)
               for vectors in random_rows(code, spec, interface[0], plan)]
    expected = [replay.trace(ref)[0] for replay in replays]
    cases = []
    for item in sorted((source / "official_mutants").glob("*.v")):
        try:
            observed = [replay.trace(item.read_text())[0] for replay in replays]
        except (RunError, ValueError) as exc:
            cases.append({"id": item.stem, "status": "invalid", "reason": str(exc)})
            continue
        raw = [sum(a != b for a, b in zip(x, y, strict=True)) for x, y in zip(expected, observed, strict=True)]
        known = [len(differences(x, y)) for x, y in zip(expected, observed, strict=True)]
        status = "kept" if any(known) else "scoring_equivalent" if any(raw) else "suspected_equivalent"
        cases.append({"id": item.stem, "status": status, "raw_different_samples": raw,
                      "known_difference_positions": known})
    result = {"task": task, "task_number": spec["task_number"], "total": len(cases),
              **{name: sum(x["status"] == name for x in cases) for name in
                 ("invalid", "suspected_equivalent", "scoring_equivalent", "kept")},
              "cycles_per_seed": plan["screen_cycles"], "seeds": plan["screen_seeds"],
              "cases": cases}
    save(where, result)
    return result


def proxy_accuracy(task):
    path = archive(task) / "proxy_accuracy.json"
    if path.is_file():
        return load(path)
    tb = upstream(task) / "golden_tb.v"
    proxies = BASE / "proxies" / task
    with tempfile.TemporaryDirectory(prefix="pilot3-proxy-") as directory:
        workspace = Path(directory)
        entries = {p.stem: golden_proxy_result(workspace / p.stem, tb, p)
                   for p in sorted(proxies.glob("*.v"))}
    result = {"task": task, "total": len(entries),
              "strict_correct": sum(x["strict"]["verdict"] == "passed" for x in entries.values()),
              "compatible_correct": sum(x.get("enum_compatible", x["strict"])["verdict"] == "passed"
                                        for x in entries.values()),
              "proxies": entries}
    if result["total"] != 9:
        raise ValueError(f"{task} expected 9 proxies")
    save(path, result)
    return result


def table(where, rows, columns):
    where.parent.mkdir(parents=True, exist_ok=True)
    with where.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prepare_eval(workers):
    plan = setup()
    code = (PREVIOUS / "protocol" / "screen_vectors.py").read_text()
    names = [row["task_id"] for row in tasks()]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        a = list(pool.map(lambda task: screen(task, plan, code), names))
        b = list(pool.map(proxy_accuracy, names))
    table(BASE / "reports" / "h_prescreen.csv", a,
          ("task_number", "task", "total", "invalid", "suspected_equivalent", "scoring_equivalent", "kept"))
    table(BASE / "reports" / "proxy_correctness.csv", b,
          ("task", "strict_correct", "compatible_correct", "total"))
    print(f"Prescreened {len(a)} tasks and verified {sum(item['total'] for item in b)} proxies", flush=True)


def check_differences(predictions, observed, masks):
    return [{signal for signal, bits in ref.items() if any(
        known in "01" and want != got
        for known, want, got in zip(bits, f"{want_row[signal]:0{len(bits)}b}", obs[signal], strict=True)
    )} for want_row, obs, ref in zip(predictions, observed, masks, strict=True)]


def evaluate(task, bench, predictions):
    source = upstream(task)
    prescreen = load(archive(task) / "prescreen.json")
    reference, _ = bench.trace((source / "golden_rtl.v").read_text())
    golden_mismatches = check_differences(predictions, reference, reference)
    passed = not any(golden_mismatches)
    results = []
    for row in prescreen["cases"]:
        if row["status"] != "kept":
            continue
        tag = row["id"]
        try:
            muted, _ = bench.trace((source / "official_mutants" / f"{tag}.v").read_text())
        except (RunError, ValueError) as exc:
            results.append({"id": tag, "status": "simulation_error", "reason": str(exc)})
            continue
        actual = differences(reference, muted)
        mismatch = check_differences(predictions, muted, reference)
        verdict = ("golden_failed" if not passed else "detected" if any(mismatch)
                   else "checker_missed" if actual else "not_exposed")
        results.append({"id": tag, "status": verdict, "exposed": bool(actual),
                        "checker_reported": any(mismatch), "known_difference_positions": len(actual)})
    return {
        "golden_pass": passed, "golden_failed_cycles": sum(bool(m) for m in golden_mismatches),
        "golden_known_output_bits": sum(bit in "01" for row in reference for bits in row.values() for bit in bits),
        "H_total": len(results), "H_detected": sum(row["status"] == "detected" for row in results),
        "H_not_exposed": sum(row["status"] == "not_exposed" for row in results),
        "H_unexposed_all": sum("exposed" in row and not row["exposed"] for row in results),
        "H_checker_missed": sum(row["status"] == "checker_missed" for row in results),
        "H_golden_failed": sum(row["status"] == "golden_failed" for row in results),
        "H_simulation_errors": sum(row["status"] == "simulation_error" for row in results),
        "H_outcomes": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=5)
    prepare_eval(parser.parse_args().workers)
