import json
from collections import Counter
from datetime import datetime, timedelta
from statistics import mean

import numpy as np
from scipy import stats

from pilot2_generate import load, save
from pilot3_evaluation import table
from pilot3_inputs import BASE, setup, tasks
from pilot3_run import ledger, use

REPORTS = BASE / "reports"
PAIRINGS = (("O-B", "B-B"), ("B-O", "B-B"), ("O-O", "B-O"), ("O-O", "B-B"))


def avg(values):
    numbers = [x for x in values if x is not None]
    return mean(numbers) if numbers else None


def scores_for_task(trials, config, task):
    rows = [row for _, row in trials if row["configuration"] == config and row["task"] == task["task_id"]]
    size = sum(row["H_total"] for row in rows)
    hits = sum(row["H_detected"] for row in rows)
    complete = [row for row in rows if row["status"] == "complete"]
    false = sum(not row["golden_pass"] for row in complete)
    return {**task, "configuration": config, "planned_repeats": len(rows), "evaluated": len(complete),
            "generated_failures": sum(row["status"] == "generation_failed" for row in rows),
            "infra_failures": sum(row["status"] == "infrastructure_failed" for row in rows),
            "golden_pass_count": len(complete) - false, "golden_false_positives": false,
            "false_positive_rate_evaluated": false / len(complete) if complete else None,
            "mean_cycles_evaluated": avg(row["cycles"] for row in complete),
            "H_detected": hits, "H_total": size, "H_rate": hits / size if size else None,
            **{k: sum(row.get(k, 0) for row in rows) for k in
               ("H_not_exposed", "H_checker_missed", "H_golden_failed", "H_generation_failed",
                "H_infrastructure_failed", "H_simulation_errors")},
            "checker_regenerations_in_trials": sum(row["incremental_regenerations"]["checker"] for row in rows),
            "stimulus_regenerations_in_trials": sum(row["incremental_regenerations"]["stimulus"] for row in rows)}


def summarize(trials, plan):
    individual = [scores_for_task(trials, config, item) for item in tasks() for config in plan["configs"]]
    macro = []
    for config in plan["configs"]:
        rows = [row for row in individual if row["configuration"] == config]
        macro.append({
            "configuration": config, "tasks": len(rows),
            "macro_H_rate": avg(row["H_rate"] for row in rows),
            "macro_false_positive_rate_evaluated": avg(row["false_positive_rate_evaluated"] for row in rows),
            "macro_mean_cycles_evaluated": avg(row["mean_cycles_evaluated"] for row in rows),
            **{key: sum(row[key] for row in rows) for key in
               ("planned_repeats", "evaluated", "golden_false_positives", "golden_pass_count",
                "generated_failures", "infra_failures", "H_detected", "H_total", "H_not_exposed",
                "H_checker_missed", "H_golden_failed", "H_generation_failed", "H_infrastructure_failed",
                "H_simulation_errors")},
        })
    for name, rows in (("per_task.csv", individual), ("macro.csv", macro)):
        table(REPORTS / name, rows, tuple(rows[0]))
    return individual, macro


def exact_signed_rank(delta):
    magnitudes = [abs(value) for value in delta if value != 0]
    observed_signs = [value > 0 for value in delta if value != 0]
    if not magnitudes:
        return 0.0, 1.0, 0
    ranks = [int(round(x)) for x in 2 * stats.rankdata(np.round(magnitudes, 12), method="average")]
    total = sum(ranks)
    observed = sum(r for r, sign in zip(ranks, observed_signs) if sign)
    distribution = Counter({0: 1})
    for rank in ranks:
        distribution += Counter({subtotal + rank: count for subtotal, count in distribution.items()})
    distance = abs(2 * observed - total)
    extreme = sum(count for subtotal, count in distribution.items() if abs(2 * subtotal - total) >= distance)
    return min(observed, total - observed) / 2, extreme / (1 << len(ranks)), len(ranks)


def paired(rows, plan):
    registry = {(row["task_id"], row["configuration"]): row["H_rate"] for row in rows}
    output, pair_values = [], []
    for index, (left, right) in enumerate(PAIRINGS):
        observations = []
        for q in tasks():
            task = q["task_id"]
            u, v = registry[task, left], registry[task, right]
            if u is None or v is None:
                continue
            delta = round(u - v, 12)
            observations.append(delta)
            pair_values.append({**q, "left": left, "right": right, "left_rate": u,
                                "right_rate": v, "difference_pp": 100 * delta})
        calc = np.array(observations)
        if not len(calc):
            raise ValueError("Wilcoxon needs at least one task pair")
        w, p, nonzero = exact_signed_rank(calc)
        rng = np.random.default_rng(plan["bootstrap_seed"] + index)
        sampled = rng.choice(calc, size=(plan["bootstrap_draws"], len(calc)), replace=True).mean(axis=1)
        low, high = np.percentile(sampled, [2.5, 97.5])
        output.append({"left": left, "right": right, "task_pairs": len(calc), "nonzero_pairs": nonzero,
                       "wilcoxon_W": w, "wilcoxon_p_two_sided_unadjusted": p,
                       "paired_mean_delta_pp": 100 * float(calc.mean()), "bootstrap_95_low_pp": 100 * float(low),
                       "bootstrap_95_high_pp": 100 * float(high)})
    table(REPORTS / "paired_comparisons.csv", output, tuple(output[0]))
    table(REPORTS / "paired_task_deltas.csv", pair_values, tuple(pair_values[0]))
    return output


def correlation(trials, plan):
    cycles = [{"task": row["task"], "configuration": row["configuration"], "repeat": row["repeat"],
               "cycles": row["cycles"], "golden_pass": int(row["golden_pass"]),
               "golden_failed": int(not row["golden_pass"])}
              for _, row in trials if row["status"] == "complete"]
    table(REPORTS / "length_scatter.csv", cycles,
          ("task", "configuration", "repeat", "cycles", "golden_pass", "golden_failed"))
    output = []
    for scope in ("all", *plan["configs"]):
        subset = [row for row in cycles if scope == "all" or row["configuration"] == scope]
        x, y = [[row[key] for row in subset] for key in ("cycles", "golden_failed")]
        if len(set(x)) < 2 or len(set(y)) < 2:
            output.append({"scope": scope, "TBs": len(subset), "pearson_r": None, "spearman_rho": None})
            continue
        linear, rank = stats.pearsonr(x, y), stats.spearmanr(x, y)
        output.append({"scope": scope, "TBs": len(subset), "pearson_r": float(linear.statistic),
                       "pearson_p_descriptive": float(linear.pvalue), "spearman_rho": float(rank.statistic),
                       "spearman_p_descriptive": float(rank.pvalue)})
    table(REPORTS / "length_correlations.csv", output, tuple(dict.fromkeys(k for row in output for k in row)))
    plot_lengths(cycles, output, plan)
    return output


def plot_lengths(cycles, stats_by_scope, plan):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.6), sharex=True, sharey=True, layout="constrained")
    for panel, scope in zip(axes.flat, ("all", *plan["configs"]), strict=True):
        group = Counter((r["cycles"], r["golden_failed"]) for r in cycles
                        if scope == "all" or r["configuration"] == scope)
        for (length, outcome), copies in group.items():
            panel.scatter(length, outcome, s=18 * (copies ** .6),
                          color=("#2474a7" if outcome == 0 else "#b34824"), alpha=.7)
            panel.annotate(str(copies), (length, outcome), xytext=(0, 8),
                           textcoords="offset points", fontsize=8, ha="center")
        record = next(r for r in stats_by_scope if r["scope"] == scope)
        coeff = record["pearson_r"]
        panel.set_title(scope + (f" · r = {coeff:.3f}" if coeff is not None else " · r undefined"))
        panel.set(yticks=[0, 1], yticklabels=["PASS", "FAIL"], ylim=(-.35, 1.35),
                  xticks=sorted({k["cycles"] for k in cycles}))
        panel.grid(axis="x", alpha=.18)
    fig.suptitle("Pilot 3 testbench length and golden outcome")
    fig.supxlabel("Stimulus cycles · labels show coincident testbench counts")
    fig.savefig(REPORTS / "length_scatter.png", dpi=170)
    plt.close(fig)


def feedback_effects(trials):
    infection, issues = [], []
    defended_checker_points = set()
    temporal = 0
    for folder, result in trials:
        records = result.get("guidance", [])
        for here, after in zip(records, records[1:]):
            turn = here["round"]
            scope = {key: result[key] for key in ("task", "configuration", "repeat")}
            for tag, evidence in here.get("stimulus_diagnostics", {}).items():
                if not here.get("stimulus_sent"):
                    continue
                temporal += bool(evidence["between_edge_differences"])
                validation_path = folder / f"stimulus_{turn + 1:02d}_validation.json"
                selected = load(validation_path)["selected"]
                first_request = selected is not None and selected.endswith("_try1.py")
                for site, finding in enumerate(evidence["sites"]):
                    if finding["label"] != "未感染":
                        continue
                    row = {**scope, "round": turn, "mutant": tag, "site": site,
                           "condition": finding.get("infection_condition"),
                           "ranges": finding.get("operand_ranges", {}),
                           "exposed_next_round": tag in after["exposed"],
                           "exposed_by_final": tag in records[-1]["exposed"],
                           "selected_suffix_request_had_feedback": first_request,
                           "cycles_before": here["cycles"], "cycles_after": after["cycles"],
                           "generated_suffix": str(validation_path.relative_to(BASE))}
                    infection.append(row)
            if here.get("checker_sent"):
                for point in here.get("checker_diagnostics", {}).get("issues", []):
                    issues.append({**scope, "round": turn, **point,
                                   "generated_checker": str(folder.relative_to(BASE) /
                                                            f"checker_{turn + 1:02d}_validation.json")})
            defended_checker_points.update(
                (scope["task"], scope["configuration"], scope["repeat"], signal, clause)
                for signal, clause in here.get("checker_diagnostics", {}).get("R1_bug_points", [])
            )
    table(REPORTS / "infection_feedback.csv", [
        {**row, "ranges": json.dumps(row["ranges"], ensure_ascii=False)} for row in infection
    ], ("task", "configuration", "repeat", "round", "mutant", "site", "condition", "ranges",
        "exposed_next_round", "exposed_by_final", "selected_suffix_request_had_feedback",
        "cycles_before", "cycles_after", "generated_suffix"))
    save(REPORTS / "checker_issues.json", issues)
    unique = {(row["task"], row["signal"], row["clause"]) for row in issues}
    issue_counts = []
    for q in tasks():
        for config in ("B-O", "O-O"):
            rows = [row for row in issues if row["task"] == q["task_id"] and row["configuration"] == config]
            issue_counts.append({**q, "configuration": config, "issued_points": len(rows),
                                 "unique_points_across_repeats": len({(r["signal"], r["clause"]) for r in rows}),
                                 "accepted": sum(r["accepted"] for r in rows),
                                 "not_accepted": sum(not r["accepted"] for r in rows)})
    table(REPORTS / "checker_issue_counts.csv", issue_counts, tuple(issue_counts[0]))
    derived = [row for row in infection if row["condition"]]
    mutant_rounds = {(r["task"], r["configuration"], r["repeat"], r["round"], r["mutant"]):
                     r["exposed_next_round"] for r in derived}
    ordered = sorted(derived or infection, key=lambda row: (
        not row["exposed_next_round"], not row["selected_suffix_request_had_feedback"]))
    examples = []
    seen = set()
    for row in ordered:
        identity = (row["task"], row["mutant"])
        if identity not in seen:
            examples.append(row)
            seen.add(identity)
        if len(examples) == 2:
            break
    checker_examples = [next((row for row in issues if row["accepted"] is kind), None)
                        for kind in (True, False)]
    save(REPORTS / "feedback_examples.json", {"stimulus": examples,
                                               "checker": [row for row in checker_examples if row]})
    return {
        "uninfected_site_feedback_events": len(infection),
        "derived_condition_events": len(derived),
        "derived_condition_exposed_next": sum(row["exposed_next_round"] for row in derived),
        "derived_condition_exposed_by_final": sum(row["exposed_by_final"] for row in derived),
        "derived_condition_distinct_mutant_rounds": len(mutant_rounds),
        "derived_condition_mutant_rounds_exposed_next": sum(mutant_rounds.values()),
        "derived_with_feedback_in_selected_request": sum(r["selected_suffix_request_had_feedback"] for r in derived),
        "derived_with_feedback_in_selected_request_exposed_next": sum(
            r["selected_suffix_request_had_feedback"] and r["exposed_next_round"] for r in derived),
        "unable_to_derive": len(infection) - len(derived),
        "all_events_exposed_next": sum(row["exposed_next_round"] for row in infection),
        "between_edge_feedback_events": temporal,
        "checker_issue_deliveries": len(issues),
        "distinct_task_signal_clause_points": len(unique),
        "accepted_proxy_majority": sum(row["accepted"] for row in issues),
        "not_accepted_proxy_majority": sum(not row["accepted"] for row in issues),
        "distinct_R1_bug_points_not_forwarded": len(defended_checker_points),
        "examples": {"stimulus": len(examples), "checker": sum(row is not None for row in checker_examples)},
    }


def usage_summary(trials, plan):
    initial_rows = [row for path in sorted((BASE / "initial").glob("*/*/calls.jsonl"))
                    for row in ledger(path)]
    guided_rows = [row for where, _ in trials for row in ledger(where / "calls.jsonl")]
    full = initial_rows + guided_rows
    for row in full:
        got = {k: row[k] for k in ("model_requested", "temperature", "max_tokens", "stream", "thinking",
                                    "timeout_seconds")}
        want = {"model_requested": plan["model"], "temperature": plan["temperature"],
                "max_tokens": plan["max_tokens"], "stream": plan["stream"], "thinking": plan["thinking"],
                "timeout_seconds": plan["transport"]["timeout_seconds"]}
        if got != want or "eval/" in row["prompt"].lower():
            raise ValueError("A v3 log departed from the locked model protocol or held-out boundary")
    start = min(datetime.fromisoformat(row["timestamp_utc"]) -
                timedelta(seconds=row["request_seconds"]) for row in full)
    end = max(datetime.fromisoformat(row["finished_utc"]) for _, row in trials)
    by_config = {cfg: use([r for path, row in trials if row["configuration"] == cfg
                           for r in ledger(path / "calls.jsonl")]) for cfg in plan["configs"]}
    return {"initial_shared": use(initial_rows), "incremental": use(guided_rows), "unique_total": use(full),
            "incremental_by_configuration": by_config, "response_started_utc": start.isoformat(),
            "last_trial_finished_utc": end.isoformat(), "wall_seconds": (end - start).total_seconds(),
            "time_in_trials_seconds": sum(row["seconds"] for _, row in trials)}


def completeness():
    groups = {}
    for scope in ("initial", "runs"):
        results = [load(path) for path in (BASE / scope).rglob("checker_*_validation.json")]
        groups[scope] = {
            "checker_generation_stages": len(results),
            "regenerations": sum(row["regenerations"] for row in results),
            "missing_expectation_failures": sum("missing expected values" in error
                                                or "expected precisely these ports" in error
                                                for row in results for error in row["errors"]),
            "failed_stages": sum(row["selected"] is None for row in results),
        }
    return groups


def main():
    plan = setup()
    paths = sorted((BASE / "runs").glob("*/*/*/result.json"))
    trials = [(p.parent, load(p)) for p in paths]
    scope = {(t["task_id"], cfg, rep) for t in tasks() for cfg in plan["configs"]
             for rep in range(1, len(plan["repeat_seeds"]) + 1)}
    seen = {(row["task"], row["configuration"], row["repeat"]) for _, row in trials}
    if seen != scope or len(trials) != len(scope):
        raise ValueError(f"Expected {len(scope)} archived trials, found {len(trials)}")
    trial_table = []
    for path, row in trials:
        record = {k: v for k, v in row.items() if not isinstance(v, (dict, list))}
        record.update({f"shared_{name}": value for name, value in row["shared_initial_usage"].items()})
        record.update({f"incremental_{name}": value for name, value in row["incremental_usage"].items()})
        record.update({"shared_checker_regenerations": row["shared_initial_regenerations"]["checker"],
                       "incremental_checker_regenerations": row["incremental_regenerations"]["checker"]})
        trial_table.append(record)
    table(REPORTS / "trials.csv", trial_table, tuple(dict.fromkeys(k for r in trial_table for k in r)))
    rows, macro = summarize(trials, plan)
    summary = {"statuses": Counter(row["status"] for _, row in trials), "macro": macro,
               "paired": paired(rows, plan), "correlation": correlation(trials, plan),
               "feedback": feedback_effects(trials), "usage": usage_summary(trials, plan),
               "completeness": completeness()}
    save(REPORTS / "summary.json", summary)


if __name__ == "__main__":
    main()
