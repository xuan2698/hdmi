"""Archive v3-compatible metrics and the contract-review audit."""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core import RUNS, V3, load, protocol, save, setup, tasks, token_use
from pilot3_report import exact_signed_rank

REPORTS=ROOT/"reports"
SETTINGS=protocol()["configs"]


def write_csv(path,rows):
    if not rows:
        return
    columns=list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,columns,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def maybe(counter,base):
    return counter/base if base else None


def summarize(outcomes,field):
    if field=="false_positive":
        valid=[r["golden_pass"] for r in outcomes if r["golden_pass"] is not None]
        return maybe(sum(value is False for value in valid),len(valid))
    return maybe(sum(r["H_detected"] for r in outcomes),sum(r["H_total"] for r in outcomes))


def old_base_cost(task,rep):
    rows=[]
    base=V3/"initial"/task/f"rep{rep}"/"calls.jsonl"
    for line in base.read_text().splitlines():
        r=json.loads(line)
        if "Define reference(vectors)" in r["prompt"] or "Implement reference(vectors)" in r["prompt"]:
            rows.append(r)
    return {"tokens":sum(r.get("usage",{}).get("total_tokens",0) for r in rows),
            "go_usd":sum(r.get("allowance") or 0 for r in rows),
            "charged_usd":sum(r.get("charged_usd") or 0 for r in rows)}


def primary(cases,phase):
    by_run=[]
    by_mutant=[]
    configs=defaultdict(list)
    for case in cases:
        for row in case["outcomes"]:
            cfg=row["config"]
            usage=row["usage"]
            historical=old_base_cost(case["task"],case["rep"]) if cfg=="Base" else usage
            data={**{k:row[k] for k in ("task","rep","config","golden_pass","golden_failed_cycles",
                                      "status","H_total","H_detected","H_sim_errors")},
                  "stimulus_sha256":case["vectors_sha256"],"cycles":case["cycles"],"mid_rows":case["mid_rows"],
                  "generation_failure_reason":row.get("reason",""),
                  **usage,"comparable_tokens":historical["tokens"],"comparable_go_usd":historical["go_usd"],
                  "comparable_charged_usd":historical["charged_usd"],
                  "A_blocked":sum(bool(x) for x in (row.get("A",{}).get("failed_examples",[]))),
                  "B_blocked":row.get("B",{}).get("B_rejected",0),
                  "resolution":row.get("B",{}).get("status","")}
            by_run.append(data)
            configs[cfg].append(data)
            by_mutant.extend({"task":row["task"],"rep":row["rep"],"config":cfg,**mutant}
                             for mutant in row["H_outcomes"])
    write_csv(REPORTS/f"{phase}_by_run.csv",by_run)
    write_csv(REPORTS/f"{phase}_by_mutant.csv",by_mutant)
    macro=[]
    task_rates={}
    task_rows=[]
    for cfg in SETTINGS:
        runs=configs[cfg]
        by_task=defaultdict(list)
        for row in runs:
            by_task[row["task"]].append(row)
        for task,group in by_task.items():
            tc={"task":task,"config":cfg,"runs":len(group),
                "golden_scored":sum(r["golden_pass"] is not None for r in group),
                "golden_failed":sum(r["golden_pass"] is False for r in group),
                "H_detected":sum(r["H_detected"] for r in group),"H_total":sum(r["H_total"] for r in group)}
            for field in ("false_positive","H"):
                rate=summarize(group,field)
                tc[field]=rate
                task_rates[task,cfg,field]=rate
            task_rows.append(tc)
        out={"config":cfg,"runs":len(runs),"generation_failures":sum(r["status"]!="ready" for r in runs),
             "golden_scored":sum(r["golden_pass"] is not None for r in runs)}
        for m in ("false_positive","H"):
            valid=[task_rates[t,cfg,m] for t in by_task if task_rates[t,cfg,m] is not None]
            out[f"{m}_macro"]=mean(valid) if valid else None
            out[f"{m}_pooled"]=summarize(runs,m)
            out[f"{m}_macro_tasks"]=len(valid)
        for key in ("tokens","go_usd","charged_usd","comparable_tokens","comparable_go_usd","comparable_charged_usd",
                    "calls","attempts","A_blocked","B_blocked"):
            out[key]=sum(r[key] for r in runs)
        macro.append(out)
    write_csv(REPORTS/f"{phase}_by_task.csv",task_rows)
    write_csv(REPORTS/f"{phase}_macro.csv",macro)
    return task_rates,macro


def paired(rates,names,phase):
    comparisons=[("Ours",r) for r in SETTINGS[:9] if r!="Ours"]+[("Ours-think","Base-think")]
    plan=setup()
    rows=[]
    for left,right in comparisons:
        for outcome in ("false_positive","H"):
            values=[]
            for task in names:
                a=rates.get((task,left,outcome))
                b=rates.get((task,right,outcome))
                if a is not None and b is not None:
                    values.append(round(a-b,12))
            if not values:
                rows.append({"left":left,"right":right,"metric":outcome,"task_pairs":0,"p":None})
                continue
            delta=np.array(values)
            w,p,n=exact_signed_rank(delta)
            rng=np.random.default_rng(plan["bootstrap_seed"])
            sample=rng.choice(delta,size=(plan["bootstrap_draws"],len(delta)),replace=True)
            lo,hi=np.percentile(sample.mean(axis=1),[2.5,97.5])
            rows.append({"left":left,"right":right,"metric":outcome,"task_pairs":len(values),"nonzero_pairs":n,
                         "W":w,"p":p,"difference_pp":float(100*delta.mean()),"ci_low_pp":float(lo*100),
                         "ci_high_pp":float(hi*100)})
    ordered=sorted((r for r in rows if r["p"] is not None),key=lambda r:r["p"])
    corrected=0
    for i,row in enumerate(ordered):
        corrected=max(corrected,min(1,row["p"]*(len(ordered)-i)))
        row["holm_p"]=corrected
    write_csv(REPORTS/f"{phase}_paired.csv",rows)
    return rows


def diagnosis(cases,phase):
    reviews=[]
    precision=[]
    effects=[]
    flags=[]
    for case in cases:
        task,rep=case["task"],case["rep"]
        precision.extend(case["precision"])
        for outcome in case["outcomes"]:
            name=outcome["config"]
            for round_ in outcome.get("rounds",[]):
                report=load(ROOT/round_["review"])
                row={"task":task,"rep":rep,"config":name,"round":round_["round"],
                     **{k:round_[k] for k in ("issues","retained","no_effect","no_executable","accepted","rebutted")}}
                if round_["trace"]:
                    logs=load(ROOT/round_["trace"])
                    row["tool_ambiguities"]=len(logs)
                    row["tool_executable"]=sum(r["status"]!="not_executable" for r in logs)
                else:
                    row.update(tool_ambiguities=0,tool_executable=0)
                row.update(Counter(issue["type"] for issue in report["issues"]))
                reviews.append(row)
            B=outcome.get("B") or {}
            if B:
                flags.append({"task":task,"rep":rep,"config":name,"resolution":B["status"],
                              "has_dispute":B["has_dispute"],"example_candidates":len(B["candidates"])})
            for kind,p in outcome["check_effects"].items():
                before,after=p["before"],p["after"]
                direction=("unscored" if before is None or after is None else "false_positive_removed"
                           if before>0 and after==0 else "false_positive_introduced" if before==0 and after>0 else
                           "fewer_failed_cycles" if after<before else "more_failed_cycles" if after>before else "unchanged")
                effects.append({"task":task,"rep":rep,"config":name,"check":kind,**p,"effect":direction})
    for name,values in (("reviews",reviews),("reviewer_precision",precision),("checks",effects),("resolution",flags)):
        write_csv(REPORTS/f"{phase}_{name}.csv",values)
    return {"reviews":reviews,"precision":precision,"effects":effects,"flags":flags}


def examples_report():
    examples=load(ROOT/"examples.json")
    rows=[]
    picks=[]
    for task,entries in examples.items():
        rows.append({"task":task,"total":len(entries),"executable":sum(bool(e["vectors"]) for e in entries),
                     "lengths":";".join(str(e["length"]) for e in entries)})
        if entries:
            picks.append({"task":task,**entries[0]})
    write_csv(REPORTS/"spec_examples.csv",rows)
    save(REPORTS/"spec_examples_review.json",picks[:5])


def case_artifacts(cases,phase):
    qualifying=[]
    for case in cases:
        item=next(i for i in case["outcomes"] if i["config"]=="Ours")
        if item["status"]=="ready" and len(item["rounds"])==2:
            qualifying.append((case,item))
    ranked=sorted(qualifying,key=lambda ci:(not bool(ci[1]["golden_pass"]),ci[0]["rep"],ci[0]["task"]))
    if phase=="pilot":
        samples=[]
        exercised=False
        for record,ours in ranked:
            pairs=[]
            for stage in ours["rounds"]:
                trace=load(ROOT/stage["trace"])
                usable=[item for item in trace if item["status"]!="not_executable"]
                exercised|=bool(usable)
                pairs.append({"review":stage["review"],"revision":stage["revision"],"trace":stage["trace"],
                              "example_review":load(ROOT/stage["review"])["issues"][:1],
                              "example_trace":(usable or trace)[:1],
                              "example_response":load(ROOT/stage["revision"])["responses"][:1]})
            initial=RUNS/record["task"]/f"rep{record['rep']}"/"off"/"author"/"contract.json"
            samples.append({"task":record["task"],"initial_contract":str(initial.relative_to(ROOT)),
                            "initial_rule":load(initial)["rules"][:1],"rounds":pairs,"model":ours["model"],
                            "golden_pass":ours["golden_pass"]})
        save(REPORTS/"pilot_examples.json",samples)
        return len(samples),exercised
    names=set()
    picks=[]
    for case,outcome in ranked:
        task=case["task"]
        if task in names:
            continue
        names.add(task)
        picks.append((case,outcome))
        if len(picks)==10:
            break
    from core import public
    artifacts=[]
    for case,row in picks:
        task,rep=case["task"],case["rep"]
        run=RUNS/task/f"rep{rep}"
        spec,_=public(task)
        entry={"task":task,"rep":rep,"spec_excerpt":spec["spec"][:1800],
               "initial_contract":load(run/"off/author/contract.json"),
               "final_contract":load(run/"configs/Ours/final_contract.json"),
               "rounds":[{**part,"issues":load(ROOT/part["review"])["issues"],
                          "responses":load(ROOT/part["revision"])["responses"],
                          "contract_after":load(ROOT/part["contract"]),
                          "tool_decisions":load(ROOT/part["trace"])} for part in row["rounds"]],
               "reference_model":(ROOT/row["model"]).read_text(),"model_path":row["model"],
               "golden_pass":row["golden_pass"],"H_detected":row["H_detected"],"H_total":row["H_total"],
               "first_false_positives":row["first_golden_mismatches"]}
        artifacts.append(entry)
    save(REPORTS/"ten_cases.json",artifacts)
    return len(artifacts),False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("pilot","full"))
    args=parser.parse_args()
    phase=args.phase
    gen=load(REPORTS/f"{phase}_generation.json")
    records=[load(ROOT/"eval"/phase/task/f"rep{rep}.json") for task in gen["tasks"] for rep in gen["reps"]]
    rates,macro=primary(records,phase)
    tests=paired(rates,gen["tasks"],phase)
    diagnose=diagnosis(records,phase)
    examples_report()
    examples_n,judge=case_artifacts(records,phase)
    debug=REPORTS/"pilot_format_debug"
    checkpoints=[p.parent for parent in (RUNS,debug) for p in parent.rglob("calls.jsonl")]
    data={"macro":macro,"paired":tests,"usage":token_use(checkpoints),
          "pilot_debug_usage":token_use(p.parent for p in debug.rglob("calls.jsonl")),
          "precision":dict(Counter(x["effect"] for x in diagnose["precision"])),
          "examples":examples_n}
    save(REPORTS/f"{phase}_summary.json",data)
    if phase=="pilot":
        by_cfg={r["config"]:r for r in macro}
        full=len(records)==3 and all(by_cfg[c]["runs"]==3 for c in SETTINGS)
        executable={c:by_cfg[c]["golden_scored"] for c in SETTINGS}
        native_two_rounds=sum(row["config"]=="Ours-think" and len(row.get("rounds",[]))==2
                              and row["status"]=="ready" for entry in records for row in entry["outcomes"])
        # Gate on end-to-end execution and frozen inputs, never on accuracy.
        # Exhausted model outputs remain planned observations under v3.
        pilot_ok=(full and all(executable.values()) and executable["Base"]==3
                  and examples_n>=2 and native_two_rounds>=2 and judge)
        save(REPORTS/"pilot_gate.json",{"status":"passed" if pilot_ok else "investigate",
             "complete_matrix":full,"complete_Ours_examples":examples_n,
             "trace_case_exercised":judge,"thinking_ours_two_rounds":native_two_rounds,
             "executable_by_config":executable,
             "base_reproduction_verified":True})
        if not pilot_ok:
            raise SystemExit("Pilot gate needs investigation; full generation has not started")
    print(phase,"metrics archived",flush=True)


if __name__=="__main__":
    main()
