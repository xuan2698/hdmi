"""Score the frozen checker treatments in the v3 evaluation domain."""

import argparse
import csv
import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from core import V3, case_path, check_rows, input_file, load, public, save, vectors
from pilot2_sim import VectorReplay
from pilot3_evaluation import archive, check_differences, upstream
from simulate import RunError, differences


def predictions(ref,outputs,vectors):
    if not ref:
        return None
    return check_rows((ROOT/ref).read_text(),outputs,vectors)


def mismatch_count(pred,ref):
    return sum(bool(row) for row in check_differences(pred,ref,ref))


def score(task,rep,phase):
    _,interface=public(task)
    outputs=interface[1]
    data=vectors(task,rep)
    bench=VectorReplay(interface,data)
    held=upstream(task)
    gold,_=bench.trace((held/"golden_rtl.v").read_text())
    pre=load(archive(task)/"prescreen.json")
    H={}
    for instance in pre["cases"]:
        if instance["status"]!="kept":
            continue
        tag=instance["id"]
        try:
            bad,_=bench.trace((held/"official_mutants"/(tag+".v")).read_text())
            H[tag]=(bad,bool(differences(gold,bad)))
        except (RunError,ValueError):
            H[tag]=(None,None)
    if len(H)!=pre["kept"]:
        raise ValueError("Frozen H cohort changed")
    base=case_path(task,rep)
    result=[]
    inferred={}
    def cached(path):
        if path not in inferred:
            inferred[path]=predictions(path,outputs,data)
        return inferred[path]
    for folder in sorted((base/"configs").iterdir()):
        entry=load(folder/"result.json")
        model=entry.get("model")
        expected=cached(model)
        coverage={"golden_pass":None,"golden_failed_cycles":None,"H_total":len(H),"H_detected":0,
                  "H_sim_errors":sum(value is None for value,_ in H.values())}
        fail_examples=[]
        outcomes=[]
        if expected is not None:
            failures=check_differences(expected,gold,gold)
            count=sum(bool(row) for row in failures)
            coverage.update(golden_pass=count==0,golden_failed_cycles=count)
            for i,signals in enumerate(failures):
                if signals and len(fail_examples)<4:
                    fail_examples.append({"cycle":i+1,"inputs":data[i],
                                         "golden":{n:gold[i][n] for n in sorted(signals)},
                                         "expected":{n:expected[i][n] for n in sorted(signals)},
                                         "prior_golden":gold[i-1] if i else None,
                                         "next_golden":gold[i+1] if i+1<len(gold) else None})
            for tag,(bad,exposed) in H.items():
                if bad is None:
                    outcomes.append({"id":tag,"simulation_error":True})
                    continue
                mismatched=any(check_differences(expected,bad,gold))
                detected=count==0 and mismatched
                coverage["H_detected"]+=int(detected)
                outcomes.append({"id":tag,"exposed":exposed,"checker_reported":mismatched,"detected":detected})
        if entry["config"]=="Base":
            historical=load(V3/"runs"/task/"A0"/f"rep{rep}"/"result.json")
            for key in ("golden_pass","H_total","H_detected","golden_failed_cycles"):
                if historical.get(key)!=coverage[key]:
                    raise ValueError(f"Base reproduces a different v3 {key} for {task}/{rep}")
            identical=(ROOT/entry["model"]).read_bytes()==(V3/"initial"/task/f"rep{rep}"/"checker.py").read_bytes()
            if not identical:
                raise ValueError("Base is not the archived v3 checker")
        checks={}
        A=entry.get("A") or {}
        B=entry.get("B") or {}
        if A.get("blocked"):
            first=cached(A.get("first_model"))
            checks["A"]={"blocked":A["blocked"],"before":mismatch_count(first,gold) if first else None,
                         "after":coverage["golden_failed_cycles"]}
        if B.get("B_rejected") or B.get("status")=="selected_by_spec_example":
            previous=cached(B.get("writer_model"))
            selected=cached(B.get("raw_model"))
            checks["B"]={"blocked":B["B_rejected"],"before":mismatch_count(previous,gold) if previous else None,
                         "after":mismatch_count(selected,gold) if selected else None}
        result.append({**entry,**coverage,"first_golden_mismatches":fail_examples,
                       "H_outcomes":outcomes,"check_effects":checks})
    precision=[]
    for mode in ("off","on"):
        path=base/mode/"precision"/"index.json"
        if not path.is_file():
            continue
        index=load(path)
        for route,items in index["accepted"].items():
            for item in items:
                before=cached(index["models"].get(item["before"]))
                after=cached(index["models"].get(item["after"]))
                mb=mismatch_count(before,gold) if before else None
                ma=mismatch_count(after,gold) if after else None
                verdict=("unscored" if ma is None or mb is None else
                         "decreased" if ma<mb else "increased" if ma>mb else "unchanged")
                precision.append({"route":route,"task":task,"rep":rep,"think":mode=="on",
                                  "before":mb,"after":ma,"effect":verdict,"issue_id":item["issue"]})
    record={"task":task,"rep":rep,"vectors_sha256":hashlib.sha256(input_file(task,rep).read_bytes()).hexdigest(),
            "cycles":len(data),"mid_rows":sum(bool(row.get("mid")) for row in data),"outcomes":result,
            "precision":precision}
    home=ROOT/"eval"/phase/task/f"rep{rep}.json"
    save(home,record)
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("pilot","full"))
    parser.add_argument("--workers",type=int,default=6)
    args=parser.parse_args()
    written=load(ROOT/"reports"/f"{args.phase}_generation.json")
    jobs=[(task,rep,args.phase) for task in written["tasks"] for rep in written["reps"]]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records=list(pool.map(lambda args:score(*args),jobs))
    if sum(len(r["outcomes"]) for r in records)!=written["matrix"]:
        raise ValueError("Evaluation matrix is incomplete")
    print(args.phase,len(records),"input sets replayed with v3 masks",flush=True)


if __name__=="__main__":
    main()
