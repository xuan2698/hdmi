"""Score task-paired results and extract feedback examples after held-out evaluation."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import numpy as np
from scipy import stats

from common import ROOT, load, protocol, public, sample_path, save
from evaluate import GROUPS, binaries, check_completion, events, replay_vectors
from hdl import WORK
from pilot3_report import exact_signed_rank

REPORTS = ROOT / "reports"
PAIRS = (("O", "B"), ("O+F", "O"), ("O+F", "B"))


def csv_out(name, data):
    if not data:
        return
    with (REPORTS / name).open("w", newline="") as f:
        keys = tuple(dict.fromkeys(k for row in data for k in row))
        wr = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        wr.writeheader()
        wr.writerows(data)


def headroom(results):
    records, all_trials = [], []
    for report in results:
        task = report["task"]
        by = report["trials"]
        for group, total in report["H_totals"].items():
            a0 = [t for t in by if t["config"] == "A0"]
            combined_a0 = {v for run in a0 for v in run["final_H"][group]}
            combined_random = {v for vlist in report["baseline"].values() for v in vlist[group]}
            for cfg in protocol()["configs"]:
                trials = [t for t in by if t["config"] == cfg]
                rd = []
                for trial in trials:
                    hist = trial["history"]
                    g_d = ((len(hist[-1]["exposed"])-len(hist[0]["exposed"]))/trial["G_total"] if hist else 0)
                    initial = len(trial["initial_H"][group])
                    final = len(trial["final_H"][group])
                    rd.append({"task": task, "group": group, "config": cfg, "seed": trial["seed"],
                               "cycles": hist[-1]["cycles"] if hist else 0, "rounds": len(hist),
                               "stop": trial.get("stop", trial["status"]),
                               "total_H": total, "initial_H": initial, "final_H": final,
                               "final_rate": final/total, "H_improvement": (final-initial)/total,
                               "G_improvement": g_d,
                               "initial_G": len(hist[0]["exposed"]) if hist else 0,
                               "final_G": len(hist[-1]["exposed"]) if hist else 0, "total_G": trial["G_total"]})
                records.append({"task": task, "group": group, "config": cfg, "H_total": total,
                                "exposure": mean(r["final_rate"] for r in rd),
                                "improvement_over_A0": mean(r["H_improvement"] for r in rd),
                                "A0_union_missed": total-len(combined_a0),
                                "long_random_union_missed": total-len(combined_random),
                                "long_random_mean": mean(len(t[group])/total for t in report["baseline"].values())})
                all_trials.extend(rd)
    csv_out("by_task.csv", records)
    csv_out("by_run.csv", all_trials)
    return records, all_trials


def infer(tables, trials):
    plan = protocol()
    tasks = list(dict.fromkeys(row["task"] for row in tables))
    look = {(r["task"],r["group"],r["config"]):r for r in tables}
    rng = np.random.default_rng(plan["bootstrap_seed"])
    sample = rng.integers(0, len(tasks), size=(plan["bootstrap_draws"], len(tasks)))
    paired, per_config, corr = [], [], []
    for group in GROUPS:
        for a,b in PAIRS:
            d = np.array([round(look[t,group,a]["exposure"] - look[t,group,b]["exposure"], 12) for t in tasks])
            w, p, n = exact_signed_rank(d)
            low, high = np.percentile(d[sample].mean(axis=1), [2.5,97.5])
            paired.append({"group":group,"left":a,"right":b,"task_pairs":len(tasks),"nonzero_pairs":n,
                           "W":w,"p":p, "mean_delta_pp":float(d.mean()*100),"ci_low_pp":float(low*100),
                           "ci_high_pp":float(high*100)})
        for cfg in plan["configs"]:
            records = [look[t,group,cfg] for t in tasks]
            per_config.append({"group":group,"config":cfg,"macro":mean(r["exposure"] for r in records),
                               "gain":mean(r["improvement_over_A0"] for r in records),
                               "long_random_macro":mean(r["long_random_mean"] for r in records)})
            subset = [t for t in trials if t["group"]==group and t["config"]==cfg]
            x,y = (np.array([t[key] for t in subset]) for key in ("G_improvement","H_improvement"))
            valid = np.ptp(x)>0 and np.ptp(y)>0
            corr.append({"group":group,"config":cfg,"n":len(subset),"mean_G_gain":float(x.mean()),
                         "mean_H_gain":float(y.mean()),
                         "pearson":float(stats.pearsonr(x,y).statistic) if valid else None,
                         "spearman":float(stats.spearmanr(x,y).statistic) if valid else None})
    for name,data in (("paired.csv",paired),("macro.csv",per_config),("correlations.csv",corr)):
        csv_out(name,data)
    return per_config, paired, corr


def cost():
    data = defaultdict(list)
    for path in (ROOT/"trial").rglob("calls.jsonl"):
        parts = path.relative_to(ROOT/"trial").parts
        kind = "initial" if parts[2]=="initial" else parts[2]
        for line in path.read_text().splitlines():
            rec = json.loads(line)
            if rec["model_requested"] != protocol()["model"] or (rec.get("model_actual") or protocol()["model"]) != protocol()["model"]:
                raise ValueError("Generation used an unexpected model")
            if "equiv-audit/" in rec["prompt"] or "evaluation/" in rec["prompt"] or "/eval/" in rec["prompt"]:
                raise ValueError("A generation prompt contains a held-out path")
            data[kind].append(rec)
    out = []
    for k, calls in sorted(data.items()):
        out.append({"phase":k,"calls":len({r["session"] for r in calls}),"attempts":len(calls),
                    "tokens":sum(r.get("usage",{}).get("total_tokens",0) for r in calls),
                    "transport_retries":sum(bool(r.get("is_retry")) for r in calls),
                    "charged_usd":sum(r.get("charged_usd") or 0 for r in calls),
                    "go_allowance_usd":sum(r.get("allowance") or 0 for r in calls),
                    "provider_list_usd":sum(r.get("list_cost_usd") or 0 for r in calls),
                    "truncated_attempts":sum(bool(r.get("truncated")) for r in calls),
                    "request_seconds":round(sum(r.get("request_seconds",0) for r in calls), 3)})
    csv_out("usage.csv",out)
    solved = [load(p) for p in (ROOT/"guidance").glob("*/formal/*.json")]
    formal = {"unique_jobs":len(solved),"wall_seconds_sum":sum(r["solve_wall_seconds"] for r in solved),
              "statuses":dict(Counter(r["status"] for r in solved))}
    feedback = [load(p) for p in (ROOT / "trial").rglob("feedback.json")]
    formal["feedback_witness_uses"] = sum("formal" in item for entries in feedback for item in entries.values())
    formal["diagnosis_labels"] = dict(Counter(item["diagnosis"]["label"] for entries in feedback
                                             for item in entries.values() if "diagnosis" in item))
    instants = sorted(datetime.fromisoformat(r["timestamp_utc"]) for phase in data.values() for r in phase)
    work = {"first_record_utc":instants[0].isoformat(), "last_record_utc":instants[-1].isoformat(),
            "record_span_seconds":(instants[-1]-instants[0]).total_seconds(),
            "generation_repairs":sum(len(load(p)["errors"]) for p in (ROOT/"trial").rglob("status.json"))}
    return out, formal, work


def examples(rows, results):
    entries = []
    by_id = {r["id"]:r for r in rows}
    for cfg in ("O","O+F"):
        choices = []
        for result in results:
            for trial in result["trials"]:
                if trial["config"]!=cfg:
                    continue
                base = sample_path(trial["task"],trial["seed"])/cfg
                for now in trial["history"][1:]:
                    i = now["round"]
                    feed = load(base/f"round{i}"/"feedback.json")
                    for key,d in feed.items():
                        usable = ("formal" in d if cfg=="O+F" else d.get("diagnosis",{}).get("label") in
                                  ("未到达","未感染","未传播"))
                        if not usable:
                            continue
                        hit = key in now["new"]
                        final_d = sum(len(trial["final_H"][g])-len(trial["initial_H"][g]) for g in GROUPS)
                        choices.append((hit,final_d, len(now["new"]),trial["task"],trial["seed"],i,key,d,trial))
        picked = set()
        for hit,_,_,task,seed,i,tag,feedback,trial in sorted(choices, key=lambda x:x[:7], reverse=True):
            if task in picked:
                continue
            row = by_id[task]
            matrix = binaries(row)
            folder = WORK/"examples"/task/str(seed)/cfg
            before = events(row,matrix,replay_vectors(row,seed,cfg,i-1),folder/"before")
            after = events(row,matrix,replay_vectors(row,seed,cfg,i),folder/"after",
                           {k:set(v) for k,v in before.items()})
            stages = {s["round"]:s for s in trial["history"]}
            base = sample_path(task,seed)/cfg/f"round{i}"
            script = base/load(base/"status.json")["source"]
            catalog = load(ROOT/"guidance"/task/"catalog.json")["candidates"]
            edit = next(item["edit"] for item in catalog if item["id"]==tag)
            entries.append({"config":cfg,"task":task,"seed":seed,"round":i,"mutant":tag,"G_exposed_by_append":hit,
                            "source_edit":{"line":edit["line"],"before":edit["before"],"after":edit["after"]},
                            "feedback":feedback,"script":str(script.relative_to(ROOT)),
                            "appended_source":script.read_text(),
                            "G_before":len(stages[i-1]["exposed"]),"G_after":len(stages[i]["exposed"]),
                            "H_before":before,"H_after":after})
            picked.add(task)
            if len(picked)==2:
                break
    return entries


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset",type=Path)
    a=p.parse_args()
    rows=public(a.dataset)
    check_completion(rows)
    results=[load(ROOT/"evaluation"/r["id"]/"result.json") for r in rows]
    REPORTS.mkdir(parents=True,exist_ok=True)
    table,trials=headroom(results)
    assert len(trials) == len(rows)*len(protocol()["seeds"])*len(protocol()["configs"])*len(GROUPS)
    for result in results:
        for trial in result["trials"]:
            for group in GROUPS:
                assert set(trial["initial_H"][group]) <= set(trial["final_H"][group])
    macros, tests, correlations=infer(table,trials)
    receipts, solver, work=cost()
    selected=examples(rows,results)
    save(REPORTS/"feedback_examples.json",selected)
    summary={"macro":macros,"paired":tests,"correlations":correlations,"usage":receipts,"formal":solver,
             "generation_records":work,
             "H_totals":{group:sum(r["H_totals"][group] for r in results) for group in GROUPS},
             "stops":dict(Counter({k:sum(r["stop"]==k for r in trials)//len(GROUPS)
                                                for k in set(r["stop"] for r in trials)})),
             "example_counts":dict(Counter(e["config"] for e in selected))}
    save(REPORTS/"summary.json",summary)
    print(json.dumps(summary,indent=2,ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
