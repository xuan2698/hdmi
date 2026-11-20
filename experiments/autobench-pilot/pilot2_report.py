import csv
import json
from collections import Counter
from difflib import unified_diff

from pilot2_checker import CASE_NAMES
from pilot2_generate import BASE, load, save, settings


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
            useful = [(tag, cases) for tag, cases in evidence.items()
                      if any(case["label"] != "诊断未完成" for case in cases)]
            if not useful:
                continue
            short = dict(useful[:3])
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
            if not change:
                continue
        origin, modified = (row["held_out"] for row in (current, following))
        yield {"task": result["task"], "config": result["config"], "repeat": result["repeat"],
               "round_before": step, "round_after": step + 1,
               "stimulus_also_appended": following["cycles"] > current["cycles"],
               "checker_also_updated": source_in(folder, "checker", step + 1) is not None,
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
            row["stimulus_also_appended"] if role == "checker" else row["checker_also_updated"],
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


def plot_exposure(folder, rows, configs):
    chosen = load(folder / "selection.json")["selected"]
    if len(rows) != len(chosen) * len(configs) * 2:
        return
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        from matplotlib.ticker import PercentFormatter
    except ModuleNotFoundError:
        return
    colors = dict(zip(configs, ("#555555", "#0072B2", "#009E73", "#D55E00", "#CC79A7")))
    fig, axes = plt.subplots(2, 3, figsize=(12, 6.3), sharex=True, sharey=True, layout="constrained")
    for ax, task in zip(axes.flat, chosen, strict=True):
        ax.set_title(f"#{task['task_number']}  {task['task_id']}")
        for run in rows:
            if run["task"] != task["task_id"]:
                continue
            points = run["per_round"]
            ax.plot([step["round"] for step in points], [step["fixed_G_rate"] for step in points],
                    marker=".", color=colors[run["config"]], linestyle="-" if run["repeat"] == 1 else "--",
                    linewidth=1.4, alpha=0.85)
        ax.set(xlim=(0.8, 5.2), ylim=(-0.03, 1.035), xticks=range(1, 6))
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis="y", linewidth=0.6, alpha=0.35)
    fig.suptitle("Pilot 2 guidance exposure by round")
    fig.supxlabel("Round · solid = repeat 1, dashed = repeat 2")
    fig.supylabel("Exposed share of each run’s final G pool")
    axes[0][0].legend(handles=[Line2D([], [], color=color, label=name)
                                  for name, color in colors.items()],
                     loc="lower right", fontsize=8, frameon=False)
    fig.savefig(folder / "g_exposure.png", dpi=170)
    plt.close(fig)


def main():
    folder = BASE / "reports"
    plan = settings()
    probes = sorted((BASE / "runs").glob("*/*/*/*/result.json"))
    trials, rounds, summaries = [], [], {}
    second = []
    for path in probes:
        row = load(path)
        cols = {key: row[key] for key in ("phase", "task", "config", "repeat", "status")}
        if row["status"] == "complete":
            vectors = load(path.parent / "stimulus_snapshots.json")
            if any(new[:len(old)] != old for old, new in zip(vectors, vectors[1:])):
                raise ValueError(f"{row['task']}/{row['config']} modified its input prefix")
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
        for request in calls:
            if (request["model_requested"] != plan["model"] or
                    request["temperature"] != plan["temperature"] or
                    request["max_tokens"] != plan["max_tokens"] or
                    request["stream"] != plan["stream"] or
                    request.get("thinking") != plan["thinking"] or
                    request["timeout_seconds"] != plan["transport"]["timeout_seconds"]):
                raise ValueError(f"Request parameters diverged from the locked {phase} plan")
            if "eval/" in request["prompt"].lower():
                raise ValueError(f"A {phase} generation prompt exposes an evaluation path")
        totals = {field: sum(row.get(field, 0) for row in cohort) for field in
                  ("H_detected", "H_total", "H_not_exposed", "H_checker_missed", "H_simulation_errors")}
        verdicts = Counter(row["status"] for row in cohort)
        config_counts = {}
        for config in sorted({r["config"] for r in cohort}):
            cases = [row for row in cohort if row["config"] == config and row["status"] == "complete"]
            config_counts[config] = {"complete": len(cases), **{
                field: sum(row[field] for row in cases) for field in
                (*scores, *CASE_NAMES, "calls", "http_attempts", "tokens", "allowance_usd")}}
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
            "trials_that_activated_new_G": sum(
                any(round["introduced_new_batch"] for round in row.get("per_round", []))
                for row in cohort
            ),
            "G_expansion_rounds": sum(
                round["introduced_new_batch"]
                for row in cohort for round in row.get("per_round", [])
            ),
            "append_only_and_fixed_G_monotonicity_verified": True,
        }
    save(folder / "v2_summary.json", summaries)
    save(folder / "v2_diagnostic_examples.json", examples(second))
    if (folder / "selection.json").is_file():
        plot_exposure(folder, [load(path) for path in second], plan["configs"])


if __name__ == "__main__":
    main()
