"""Summarize H, the matched-budget comparisons, and the exploratory rounds."""

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import numpy as np

from base import ROOT, load, plan, save
from diagnostic_audit import LABELS
from evaluate import GROUPS
from pilot3_report import exact_signed_rank

REPORTS=ROOT/"reports"
PAIRS=(("O","B"),("O+F","O"),("B","A0-long"),("O","A0-long"))


def write_csv(name, rows):
    if rows:
        with (REPORTS/name).open("w",newline="") as handle:
            writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def exposure(results):
    configs=plan()["configs"]
    records=[]
    individual=[]
    for data in results:
        q=data["task"]
        for group,n in data["H_totals"].items():
            for cfg in configs:
                trials=[item for item in data["trials"] if item["config"]==cfg]
                rows=[{"task":q,"group":group,"config":cfg,"seed":t["seed"],"cycles":t["cycles"],
                       "stop":t["stop"],"G":len(t["history"][-1]["exposed"]) if t["history"] else 0,
                       "G_total":t["G_total"],"H":len(t["final_H"][group]),"H_total":n,
                       "H_rate":len(t["final_H"][group])/n} for t in trials]
                assert len(rows)==len(plan()["seeds"])
                individual+=rows
                records.append({"task":q,"group":group,"config":cfg,"H_total":n,
                                "H_rate":mean(r["H_rate"] for r in rows),
                                "G_rate":mean(r["G"]/r["G_total"] for r in rows),
                                "mean_cycles":mean(r["cycles"] for r in rows)})
    write_csv("by_task.csv",records)
    write_csv("by_run.csv",individual)
    summary=[{"group":group,"config":cfg,"macro":mean(r["H_rate"] for r in records
                                                    if (r["group"],r["config"])==(group,cfg))}
             for group in GROUPS for cfg in configs]
    write_csv("macro.csv",summary)
    return individual,summary


def paired(runs):
    plan_data=plan()
    out=[]
    for group in GROUPS:
        rows=[r for r in runs if r["group"]==group]
        mapping={(r["task"],r["seed"],r["config"]):r for r in rows}
        tasks=sorted({r["task"] for r in rows})
        for left,right in PAIRS:
            scopes=(("all",False),) if "A0-long" not in (left,right) else (
                ("all",False),("only_both_20000",True))
            for scope,budget in scopes:
                per_task=[]
                matches=0
                for task in tasks:
                    gains=[]
                    for seed in plan_data["seeds"]:
                        a,b=(mapping[task,seed,c] for c in (left,right))
                        if budget and (a["cycles"]!=20000 or b["cycles"]!=20000):
                            continue
                        matches+=1
                        gains.append(a["H_rate"]-b["H_rate"])
                    if gains:
                        per_task.append(round(mean(gains),12))
                if not per_task:
                    continue
                values=np.array(per_task)
                k=len(values)
                rng=np.random.default_rng(plan_data["bootstrap_seed"])
                ids=rng.integers(0,k,size=(plan_data["bootstrap_draws"],k))
                lo,hi=np.percentile(values[ids].mean(axis=1),[2.5,97.5])
                w,p,nonzero=exact_signed_rank(values)
                out.append({"group":group,"left":left,"right":right,"scope":scope,
                            "task_pairs":k,"nonzero_pairs":nonzero,"run_pairs":matches,"W":w,"p":p,
                            "mean_delta_pp":values.mean()*100,"ci_low_pp":lo*100,"ci_high_pp":hi*100})
    write_csv("paired.csv",out)
    return out


def exploratory(results):
    rows=[]
    eligible=0
    unpaired=0
    for result in results:
        task=result["task"]
        by_key={(r["config"],r["seed"]):r for r in result["trials"]}
        for seed in plan()["seeds"]:
            o,b=(by_key[cfg,seed] for cfg in ("O","B"))
            o_hist={r["round"]:r for r in o["history"]}
            b_hist={r["round"]:r for r in b["history"]}
            for i in sorted(o_hist):
                file=ROOT/"trial"/task/str(seed)/"O"/f"round{i}"/"feedback.json"
                if i<=1 or not file.exists():
                    continue
                eligible+=1
                if i not in b_hist:
                    unpaired+=1
                    continue
                labels=[entry.get("diagnosis",{}).get("label") for entry in load(file).values()]
                stable=sum(label in LABELS for label in labels)
                row={"task":task,"seed":seed,"round":i,"stable_O_entries":stable,
                     "total_O_entries":len(labels),"G_denominator":o["G_total"]}
                for cfg,run,history in (("O",o,o_hist),("B",b,b_hist)):
                    row[f"G_gain_{cfg}"]=len(history[i]["exposed"])-len(history[i-1]["exposed"])
                    for group,denominator in result["H_totals"].items():
                        current=run["H_history"][str(i)][group]
                        previous=run["H_history"][str(i-1)][group]
                        row[f"H_{group}_denominator"]=denominator
                        row[f"H_{group}_gain_{cfg}"]=len(current)-len(previous)
                rows.append(row)
    write_csv("exploratory_rounds.csv",rows)
    aggregated=[]
    for tag,choose in (("any_stable",lambda r:r["stable_O_entries"]>0),
                       ("all_stable",lambda r:r["stable_O_entries"]==r["total_O_entries"]),
                       ("none_stable",lambda r:r["stable_O_entries"]==0),
                       ("all_paired",lambda r:True)):
        selected=[row for row in rows if choose(row)]
        out={"subset":tag,"round_pairs":len(selected)}
        for measure in ("G","H_original_plus","H_rare"):
            if not selected:
                for cfg in ("O","B","O_minus_B"):
                    out[f"{measure}_{cfg}_pp"]=None
                continue
            for cfg in ("O","B"):
                out[f"{measure}_{cfg}_pp"]=100*mean(
                    row[f"{measure}_gain_{cfg}"]/row[f"{measure}_denominator"] for row in selected)
            out[f"{measure}_O_minus_B_pp"]=out[f"{measure}_O_pp"]-out[f"{measure}_B_pp"]
        aggregated.append(out)
    write_csv("exploratory_summary.csv",aggregated)
    return {"eligible_O_rounds":eligible,"unpaired":unpaired,"comparisons":aggregated}


def usage():
    phases=defaultdict(list)
    for file in (ROOT/"trial").rglob("calls.jsonl"):
        phase=file.relative_to(ROOT/"trial").parts[2]
        phases[phase].extend(json.loads(line) for line in file.read_text().splitlines())
    out=[]
    for phase,receipts in sorted(phases.items()):
        out.append({"phase":phase,"calls":len({r["session"] for r in receipts}),"attempts":len(receipts),
                    "retries":sum(bool(r.get("is_retry")) for r in receipts),
                    "truncations":sum(bool(r.get("truncated")) for r in receipts),
                    "tokens":sum(r.get("usage",{}).get("total_tokens",0) for r in receipts),
                    "charged_usd":sum(r.get("charged_usd") or 0 for r in receipts),
                    "go_allowance_usd":sum(r.get("allowance") or 0 for r in receipts),
                    "list_usd":sum(r.get("list_cost_usd") or 0 for r in receipts),
                    "request_seconds":sum(r.get("request_seconds",0) for r in receipts)})
    times=[datetime.fromisoformat(r["timestamp_utc"]) for receipts in phases.values() for r in receipts]
    counts=Counter(r["status"] for receipts in phases.values() for r in receipts)
    write_csv("usage.csv",out)
    return {"phases":out,"receipts":dict(counts),"receipt_span_seconds":(max(times)-min(times)).total_seconds()}


def formal(results):
    audit=load(ROOT/"audits"/"formal.json")
    same={}
    for version in ("v1","v2"):
        times=[r["previous_seconds" if version=="v1" else "seconds"] for r in audit]
        same[version]={"jobs":len(audit),"status":dict(Counter(r[version] for r in audit)),
                       "seconds_sum":sum(times),"seconds_mean":mean(times)}
    usage_records=set()
    witness_uses=0
    for path in (ROOT/"trial").rglob("feedback.json"):
        task,seed,config,stage,_=path.relative_to(ROOT/"trial").parts
        if config!="O+F":
            continue
        for tag,item in load(path).items():
            if "formal_status" in item:
                usage_records.add((task,tag))
                witness_uses+=int("formal" in item)
    used=[load(ROOT/"formal"/task/(tag+".json")) for task,tag in sorted(usage_records)]
    clocks={row["task"]:row["clock"] for row in results}
    training={"jobs":len(used),"status":dict(Counter(r["status"] for r in used)),
              "wall_seconds_sum":sum(r["solve_wall_seconds"] for r in used),
              "mean_seconds":mean(r["solve_wall_seconds"] for r in used) if used else None,
              "witness_feedback_entries":witness_uses,
              "witnesses_with_internal_state":sum(
                  bool(set(r.get("state",{}).get("signals",[]))-{clocks[r["task"]]} and
                       r.get("state",{}).get("samples")) for r in used)}
    return {"audit_comparison":same,"training":training}


def training_diagnoses():
    counts=defaultdict(Counter)
    for path in (ROOT/"trial").rglob("feedback.json"):
        config=path.relative_to(ROOT/"trial").parts[2]
        for entry in load(path).values():
            if "diagnosis" in entry:
                counts[config][entry["diagnosis"]["label"]]+=1
    return {config:{"labels":dict(labels),"total":sum(labels.values()),
                   "stable":sum(labels[label] for label in LABELS)}
            for config,labels in counts.items()}


def main():
    REPORTS.mkdir(parents=True,exist_ok=True)
    saved=sorted((ROOT/"evaluation").glob("*/result.json"))
    assert len(saved)==10
    results=[load(path) for path in saved]
    runs,macro=exposure(results)
    out={"macro":macro,"paired":paired(runs),"exploratory":exploratory(results),
         "usage":usage(),"formal":formal(results),"evaluation":load(ROOT/"evaluation"/"verification.json"),
         "diagnostic":load(ROOT/"audits"/"diagnostic"/"summary.json"),
         "training_diagnoses":training_diagnoses(),
         "archive_verification":load(REPORTS/"verification.json")}
    save(REPORTS/"summary.json",out)
    print(json.dumps({k:out[k] for k in ("macro","paired","formal","exploratory","usage")},
                     indent=2,ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
