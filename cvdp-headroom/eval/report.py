"""Summarize the frozen CVDP headroom results without inference."""

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, stdev

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from designs import ROOT, config, load, save

DEST = ROOT / "reports"


def average(values):
    values = [value for value in values if value is not None]
    return mean(values) if values else None


def average_coverage(result, tags, kind):
    values = [result.get(tag, {}).get(kind, {}) for tag in tags]
    return average(v["hit"] / v["total"] for v in values if v.get("total"))


def table(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def per_task(result, plan):
    a0 = [f"a0_{seed}" for seed in plan["stimulus_seeds"]]
    random = [f"random_{seed}" for seed in plan["random_seeds"]]
    counts = Counter(item["status"] for item in result["H"].values())
    h = counts["kept"]
    if not h:
        raise ValueError(f"No eligible held-out mutants for {result['task']}")
    rates = {tag: result["runs"][tag]["rate"] for tag in a0 if tag in result["runs"]}
    scored = [rates.get(tag, 0) for tag in a0]
    random_rates = [result["runs"][tag]["rate"] for tag in random]
    random_union = set(m for tag in random for m in result["runs"][tag]["exposed"])
    cov = result["code_coverage"]
    row = {"task": result["task"], "H_candidates": len(result["H"]), "H_retained": h,
           **{f"H_{k}": counts[k] for k in ("compile_failure", "scoring_equivalent", "suspected_equivalent",
                                          "invalid_patch", "missing_generation", "unsupported_edit",
                                          "simulation_failure")},
           "A0_valid": len(rates), "A0_planned": len(a0),
           "A0_H_mean": mean(scored), "A0_H_sample_sd": stdev(scored),
           "A0_H_valid_mean": average(rates.values()),
           "A0_H_valid_sample_sd": stdev(rates.values()) if len(rates) > 1 else None,
           "long_random_H_mean": mean(random_rates), "long_random_H_sample_sd": stdev(random_rates),
           "long_random_H_union": len(random_union) / h,
           "A0_line_coverage_mean_valid": average_coverage(cov, a0, "line"),
           "long_random_line_coverage_mean": average_coverage(cov, random, "line"),
           "A0_branch_coverage_mean_valid": average_coverage(cov, a0, "branch"),
           "long_random_branch_coverage_mean": average_coverage(cov, random, "branch"),
           "code_coverage_policy": cov.get("policy", "Verilator original RTL" if "error" not in cov else "unavailable"),
           "functional_coverage": "待补"}
    detail = []
    for tag in a0 + random:
        trial = result["runs"].get(tag)
        line = cov.get(tag, {}).get("line", {})
        branch = cov.get(tag, {}).get("branch", {})
        detail.append({"task": result["task"], "run": tag, "valid": trial is not None, "H_retained": h,
                       "H_exposed": len(trial["exposed"]) if trial else 0, "H_rate": trial["rate"] if trial else 0,
                       "line_hit": line.get("hit"), "line_total": line.get("total"),
                       "branch_hit": branch.get("hit"), "branch_total": branch.get("total"),
                       "failure_reason": result["a0_failed_or_missing"].get(tag, {}).get("reason")})
    missed = []
    for tag, candidate in result["H"].items():
        if candidate["status"] != "kept":
            continue
        seeds = [seed for seed in rates if tag not in result["runs"][seed]["exposed"]]
        if seeds:
            missed.append({"task": result["task"], "mutant": tag, "bug": candidate["bug"],
                           "valid_a0_misses": "|".join(seeds), "valid_a0_runs": len(rates),
                           "unexposed_in_all_valid_a0": len(seeds) == len(rates)})
    return row, detail, missed


def receipts(paths, expected):
    authored = []
    for path in paths:
        for line in path.read_text().splitlines():
            row = json.loads(line)
            if row["model_requested"] != expected or row.get("model_actual", expected) != expected:
                raise ValueError(f"Unexpected actual model in {path}")
            authored.append(row)
    return {"model": expected, "requests": len({row["session"] for row in authored}),
            "http_attempts": len(authored), "tokens": sum(r.get("usage", {}).get("total_tokens", 0) for r in authored),
            "truncations": sum(bool(row.get("truncated")) for row in authored),
            "cost_usd": sum(row.get("charged_usd") or 0 for row in authored),
            "allowance_usd": sum(row.get("allowance") or 0 for row in authored),
            "request_seconds": sum(row.get("request_seconds", 0) for row in authored)}


def main():
    plan = config()
    selected = load(DEST / "selection.json")["selected"]
    detailed = [load(ROOT / "eval" / "results" / (t["task_id"] + ".json")) for t in selected]
    rows, seeds, misses = [], [], []
    for result in detailed:
        row, trials, mutants = per_task(result, plan)
        rows.append(row)
        seeds.extend(trials)
        misses.extend(mutants)
    table(DEST / "headroom_by_task.csv", rows)
    table(DEST / "headroom_by_run.csv", seeds)
    if misses:
        table(DEST / "unexposed_in_valid_a0.csv", misses)
    h_calls = receipts(list((ROOT / "eval" / "heldout").rglob("*calls.jsonl")), plan["mutant_model"])
    a0_calls = receipts(list((ROOT / "generation").rglob("calls.jsonl")), plan["stimulus_model"])
    missing_coverage = [r["task"] for r in detailed if "error" in r["code_coverage"]]
    summary = {"task_count": len(rows), "functional_coverage": "待补",
               "H_filter": dict(Counter(c["status"] for r in detailed for c in r["H"].values())),
               "H_replacements": sum(p.is_file() for p in (ROOT / "eval" / "heldout").rglob("original_mutation.json")),
               "A0_valid": sum(r["A0_valid"] for r in rows), "A0_planned": sum(r["A0_planned"] for r in rows),
               "macro_average": {k: average(r[k] for r in rows) for k in
                                 ("A0_H_mean", "A0_H_valid_mean", "long_random_H_mean", "long_random_H_union",
                                  "A0_line_coverage_mean_valid", "long_random_line_coverage_mean",
                                  "A0_branch_coverage_mean_valid", "long_random_branch_coverage_mean")},
               "headroom_gate_threshold_percent": plan["headroom_cutoff_percent"],
               "meets_no_obvious_headroom_threshold": mean(r["A0_H_mean"] for r in rows) * 100
                                                      >= plan["headroom_cutoff_percent"],
               "valid_A0_missed_mutant_count": len(misses),
               "never_exposed_in_any_valid_A0": sum(m["unexposed_in_all_valid_a0"] for m in misses),
               "code_coverage_tasks_with_line_points": sum(r["long_random_line_coverage_mean"] is not None for r in rows),
               "code_coverage_tasks_with_branch_points": sum(r["long_random_branch_coverage_mean"] is not None for r in rows),
               "missing_code_coverage": missing_coverage, "inference": {"A0": a0_calls, "H": h_calls}}
    save(DEST / "headroom_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
