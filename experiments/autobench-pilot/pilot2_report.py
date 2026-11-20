import csv
import json
from collections import Counter
from difflib import unified_diff

from pilot2_checker import CASE_NAMES
from pilot2_generate import BASE, load, save


def table(path, columns, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_in(folder, name, step):
    choices = sorted(folder.glob(f"{name}_{step:02d}*.py"))
    return choices[-1] if choices else None


def example_candidates(artifact, role):
    folder = artifact.parent
    result = load(artifact)
    steps = result["per_round"]
    for current, following in zip(steps, steps[1:]):
        step = current["round"]
        update = source_in(folder, role, step + 1)
        if not update:
            continue
        if role == "stimulus":
            evidence = current.get("stimulus_diagnostics", {})
            if not evidence:
                continue
            short = dict(list(evidence.items())[:3])
            modified = update.read_text().splitlines()
            change = modified[:25]
        else:
            evidence = current.get("checker_diagnostics", {})
            counts = evidence.get("counts", {})
            if not current.get("checker_feedback") or not counts or not sum(counts.values()):
                continue
            short = {"counts": counts,
                     "cases": {group: data[:1] for group, data in evidence["diagnostics"].items()}}
            before = next((f for n in reversed(range(1, step + 1))
                           if (f := source_in(folder, role, n))), None)
            if before is None:
                continue
            change = list(unified_diff(before.read_text().splitlines(), update.read_text().splitlines(),
                                       fromfile=before.name, tofile=update.name, lineterm=""))[:48]
        origin, modified = (row["held_out"] for row in (current, following))
        yield {"task": result["task"], "config": result["config"], "repeat": result["repeat"],
               "round_before": step, "round_after": step + 1,
               "artifact": str(update.relative_to(BASE)), "evidence": short,
               "generated_change": change,
               "G_fixed_before": [current["fixed_G_exposed"], current["fixed_G_total"]],
               "G_fixed_after": [following["fixed_G_exposed"], following["fixed_G_total"]],
               "H_exposed_before": [origin["H_exposed"], origin["H_total"]],
               "H_exposed_after": [modified["H_exposed"], modified["H_total"]],
               "H_detected_before": origin["H_detected"], "H_detected_after": modified["H_detected"]}


def examples(artifacts):
    choices = {}
    for role in ("stimulus", "checker"):
        items = [row for path in artifacts for row in example_candidates(path, role)]
        items.sort(key=lambda row: (
            -abs(row["H_exposed_after"][0] - row["H_exposed_before"][0]),
            -abs(row["G_fixed_after"][0] - row["G_fixed_before"][0]),
            -abs(row["H_detected_after"] - row["H_detected_before"]),
            not bool(row["generated_change"]), row["task"],
        ))
        distinct, seen = [], set()
        for item in items:
            if item["task"] not in seen:
                distinct.append(item)
                seen.add(item["task"])
        choices[role] = (distinct + [item for item in items if item not in distinct])[:2]
    return choices


def main():
    folder = BASE / "reports"
    probes = sorted((BASE / "runs").glob("*/*/*/*/result.json"))
    trials, rounds, summaries = [], [], {}
    second = []
    for path in probes:
        row = load(path)
        cols = {key: row[key] for key in ("phase", "task", "config", "repeat", "status")}
        if row["status"] == "complete":
            if row["phase"] == "second":
                second.append(path)
            for item in row["per_round"]:
                rounds.append({**cols, **item, **item["held_out"],
                               **item.get("checker_diagnostics", {}).get("counts", {})})
            cols.update(row["case_counts"])
        trials.append({**row, **cols})
    common = ("phase", "task", "config", "repeat", "status")
    scores = ("golden_pass", "H_detected", "H_total", "H_exposed", "H_not_exposed",
              "H_checker_missed", "H_simulation_errors")
    table(folder / "trial_metrics.csv", (*common, *scores, *CASE_NAMES, "rounds", "stop_reason",
          "calls", "http_attempts", "tokens", "allowance_usd", "charged_usd",
          "calls_with_explicit_charge", "sum_request_seconds", "seconds", "reason"), trials)
    table(folder / "round_metrics.csv", (*common, "round", "cycles", "active_G_total",
          "active_G_rate", "fixed_G_exposed", "fixed_G_total", "fixed_G_rate",
          "introduced_new_batch", "consecutive_fully_exposed_new_batches",
          *scores, *CASE_NAMES), rounds)
    for phase in ("calibration", "rerun", "second"):
        cohort = [row for row in trials if row["phase"] == phase]
        calls = []
        for file in (BASE / "runs" / phase).glob("*/*/*/calls.jsonl"):
            calls.extend(json.loads(line) for line in file.read_text().splitlines())
        totals = {field: sum(row.get(field, 0) for row in cohort) for field in
                  ("H_detected", "H_total", "H_not_exposed", "H_checker_missed", "H_simulation_errors")}
        verdicts = Counter(row["status"] for row in cohort)
        config_counts = {}
        for config in sorted({r["config"] for r in cohort}):
            cases = [row for row in cohort if row["config"] == config and row["status"] == "complete"]
            config_counts[config] = {"complete": len(cases), **{
                field: sum(row[field] for row in cases) for field in (*scores, *CASE_NAMES)}}
        for row in cohort:
            if row["status"] != "complete":
                continue
            trail = row["per_round"]
            fixed = [item["fixed_G_rate"] for item in trail if "fixed_G_rate" in item]
            if fixed != sorted(fixed):
                raise ValueError(f"{row['task']}/{row['config']} loses earlier G exposure")
        summaries[phase] = {
            "states": verdicts, "totals": totals, "by_config": config_counts,
            "logical_calls": len({j["session"] for j in calls}), "http_attempts": len(calls),
            "truncations": sum(j.get("truncated", False) for j in calls),
            "retries": sum(j.get("is_retry", False) for j in calls),
            "transport_errors": sum(j["status"] != "received" for j in calls),
            "tokens": sum(j.get("usage", {}).get("total_tokens", 0) for j in calls),
            "allowance_usd": sum(j.get("allowance") or 0 for j in calls),
            "explicit_charge_usd": sum(j.get("charged_usd") or 0 for j in calls),
            "sum_request_seconds": sum(j["request_seconds"] for j in calls),
            "declines_on_active_denominator": sum(
                (b["active_G_rate"] is not None and a["active_G_rate"] is not None and
                 b["active_G_rate"] < a["active_G_rate"])
                for r in cohort for a, b in zip(r.get("per_round", []), r.get("per_round", [])[1:])
            ),
            "stops": Counter(row["stop_reason"] for row in cohort if row["status"] == "complete"),
        }
    save(folder / "v2_summary.json", summaries)
    save(folder / "v2_diagnostic_examples.json", examples(second))


if __name__ == "__main__":
    main()
