"""Export the amended toolchain gate and per-task results from saved checkpoints."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
CATEGORIES=("counterexample","bounded_equivalent","parse_or_elab_failure","unsupported_syntax",
            "timeout","conversion_failure","reset_mismatch","other")


def read(path):
    return json.loads(path.read_text())


def write(name, rows):
    with (REPORTS/name).open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round",type=int,choices=(2,3),default=2)
    args=parser.parse_args()
    catalogs=[read(p) for p in sorted((ROOT/"generation/G").glob("*/*/catalog.json"))]
    matrix={(r["task"],r["proxy"],g["id"]) for r in catalogs for g in r["candidates"]}
    if len(catalogs)!=100 or not matrix:
        raise ValueError("Missing the frozen proxy-only G archive")
    solved={}
    for path in (ROOT/"stage0"/f"round{args.round}").glob("*/*/G*.json"):
        record=read(path)
        key=(record["task"],record["proxy"],record["G"])
        assert key in matrix
        solved[key]=record
    vetted=sum(r["formal_success"] for r in solved.values())
    total=len(matrix)
    done=len(solved)
    pending=total-done
    min_rate=vetted/total
    max_rate=(vetted+pending)/total
    result="passed" if pending==0 and min_rate>=.70 else "failed" if pending==0 else "in_progress"
    write("stage0_amended_gate.csv",[
        {"status":result,"round":args.round,"proxy_slots":len(catalogs),
         "proxies_with_G":sum(bool(r["candidates"]) for r in catalogs),
         "total_pairs":total,"completed_pairs":done,"pending_pairs":pending,"formal_successes":vetted,
         "observed_completed_success_rate":vetted/done if done else "",
         "success_rate_if_all_pending_fail":min_rate,"success_rate_if_all_pending_succeed":max_rate,
         "gate_threshold":.70}])
    records=[]
    for task in sorted({x[0] for x in matrix}):
        part=[r for key,r in solved.items() if key[0]==task]
        cases=sum(key[0]==task for key in matrix)
        counts=Counter(r["category"] for r in part)
        records.append({"task":task,"proxy_slots":10,"proxies_with_G":sum(r["task"]==task and
                         bool(r["candidates"]) for r in catalogs),
                        "planned_pairs":cases,"completed_pairs":len(part),"pending":cases-len(part),
                        "formal_successes":sum(r["formal_success"] for r in part),
                        "replayable":sum(r["replayable"] for r in part),
                        **{cat:counts[cat] for cat in CATEGORIES}})
    write("stage0_amended_by_task.csv",records)
    detailed=[]
    for key in sorted(matrix):
        r=solved.get(key,{})
        detailed.append({"task":key[0],"proxy":key[1],"G":key[2],"category":r.get("category","pending"),
                         "formal_success":r.get("formal_success",""),"replayable":r.get("replayable",""),
                         "cycles":r.get("cycles",""),"seconds":r.get("seconds",""),"reason":r.get("reason","")})
    write("stage0_amended_pairs.csv",detailed)
    print(result,done,total,vetted,flush=True)


if __name__=="__main__":
    main()
