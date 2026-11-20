import csv
import json
import math
from collections import Counter
from datetime import datetime
from difflib import unified_diff
from pathlib import Path
from statistics import median
from urllib.request import Request, urlopen

from audit import audit
from run_pilot import ROOT, read, save, totals


def model_catalog():
    endpoint = "https://opencode.ai/inference/go/v1/models"
    req = Request(endpoint, headers={"User-Agent": "autobench-preflight/1.0"})
    with urlopen(req, timeout=20) as response:
        data = json.load(response)
    models = {row["id"]: row for row in data["data"]}
    selected = {}
    for name in ("deepseek-v4.1-flash", "hy4", "hy4-flash-free"):
        entry = models[name]
        selected[name] = {key: entry[key] for key in ("id", "name", "canonical_id", "cost", "go")}
    return {"endpoint": endpoint, "models": selected}


def examples():
    selections = (("stimulus", "O-O", "stimulus_diagnostics"),
                  ("checker", "B-O", "checker_diagnostics"))
    rows = {}
    for role, cfg, field in selections:
        folder = ROOT / "runs" / "edgecapture" / cfg
        items = read(folder / "round_01.json")[field]
        before, after = (folder / f"{role}_{n:02d}.py" for n in (1, 2))
        if role == "stimulus":
            evidence = items
        else:
            evidence = items["additional"][:1]
        delta = list(unified_diff(before.read_text().splitlines(), after.read_text().splitlines(),
                                  fromfile=before.name, tofile=after.name, lineterm=""))
        rows[role] = {"task": "edgecapture", "configuration": cfg, "round": 1,
                      "feedback": evidence, "change": delta}
    return rows


def main():
    target = ROOT / "reports"
    target.mkdir(exist_ok=True)
    plan = read(ROOT / "plan.json")
    records = []
    logs, screening = [], {}
    for row in read(ROOT / "sample.json"):
        task = row["task_id"]
        path = ROOT / "runs" / task / "screen"
        screened = read(path / "screening.json")
        screening[task] = {"generated": len(screened["variants"]), "retained": screened["retained"],
                           "suspected_equivalent": screened["suspected_equivalent"],
                           **totals(path / "calls.jsonl")}
        logs += [json.loads(line) for line in (path / "calls.jsonl").read_text().splitlines()]
        for cfg in plan["configs"]:
            item = ROOT / "runs" / task / cfg
            result = read(item / "result.json")
            h = sum(result[f"H_{field}"] for field in
                    ("detected", "not_exposed", "checker_missed", "simulation_errors"))
            if h != result["H_total"]:
                raise ValueError(f"H verdicts do not sum to the denominator for {task}/{cfg}")
            records.append(result)
            logs += [json.loads(line) for line in (item / "calls.jsonl").read_text().splitlines()]

    cols = ("task", "configuration", "golden_pass", "H_detected", "H_total", "H_new_error",
            "H_not_exposed", "H_checker_missed", "H_simulation_errors", "rounds", "calls",
            "http_attempts", "prompt_tokens", "completion_tokens", "tokens", "allowance_usd",
            "charged_usd", "calls_with_explicit_charge", "elapsed_seconds", "sum_request_seconds",
            "G_retained", "G_exposed", "G_suspected_equivalent")
    with (target / "metrics.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    calls = [r for r in logs if r["attempt"] > 0]
    durations = [r["request_seconds"] for r in calls]
    options = Counter((row["temperature"], row["max_tokens"], row.get("reasoning_effort", "default"),
                       row.get("thinking", "default"), row.get("stream", False)) for row in calls)
    peak = [r for r in calls if (d := datetime.fromisoformat(r["timestamp_utc"])).weekday() < 5
            and (1 <= d.hour < 4 or 6 <= d.hour < 10)]
    total_fields = ("calls", "http_attempts", "tokens", "prompt_tokens", "completion_tokens",
                    "allowance_usd", "charged_usd", "sum_request_seconds")
    trial_totals = {f: sum(row[f] for row in records) for f in total_fields}
    screen_totals = {f: sum(row[f] for row in screening.values()) for f in total_fields}
    trial_scale, screen_scale = 25 * 3 / len(screening), 25 / len(screening)
    estimate = {f: trial_totals[f] * trial_scale + screen_totals[f] * screen_scale for f in total_fields}
    estimate.update({"trials": 25 * len(plan["configs"]) * 3,
                     "serial_request_hours": estimate["sum_request_seconds"] / 3600,
                     "ideal_8_worker_request_hours": estimate["sum_request_seconds"] / (3600 * 8),
                     "full_standard_go_5h_allowance_windows": math.ceil(estimate["allowance_usd"] / 20)})
    summary = {
        "screening": screening, "configs": len(records), "trial_totals": trial_totals,
        "screen_totals": screen_totals,
        "call_latency_median_seconds": median(durations),
        "call_latency_mean_seconds": sum(durations) / len(durations),
        "peak_requests": len(peak),
        "truncated_requests": sum(r.get("finish_reason") == "length" for r in calls),
        "transport_failure_attempts": sum(r["status"] != "received" for r in calls),
        "request_settings": [
            {"temperature": t, "max_tokens": n, "reasoning_effort": effort, "thinking": thinking,
             "stream": stream, "attempts": count}
            for (t, n, effort, thinking, stream), count in sorted(options.items())
        ],
        "earliest_request_finished_utc": min(r["timestamp_utc"] for r in calls),
        "latest_request_finished_utc": max(r["timestamp_utc"] for r in calls),
        "recorded_model_http_attempts": len(calls), "formal_estimate": estimate,
    }
    save(target / "summary.json", summary)
    save(target / "prompt_audit.json", audit(ROOT, plan["sample_seed"] + 1))
    save(target / "diagnostic_examples.json", examples())
    save(target / "go_catalog.json", model_catalog())


if __name__ == "__main__":
    main()
