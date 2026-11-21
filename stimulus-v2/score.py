"""Replay the two frozen development H cohorts after generation is closed."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from base import ROOT, V1, WORK, load, plan, public, save, trial, vectors_at
from evaluate import GROUPS, binaries, events
from run import ready


def extend_exposure(row, matrix, vectors, location, previous):
    if all(len(previous[group])==len(variants) for group,variants in matrix.items()):
        return previous
    return events(row,matrix,vectors,location,{group:set(found) for group,found in previous.items()})


def score(row, replay=False):
    task=row["id"]
    directory=ROOT/"evaluation"/task
    path=directory/"result.json"
    if path.exists() and not replay:
        return load(path)
    setup=plan()
    matrix=binaries(row)
    previous=load(V1/"evaluation"/task/"result.json")
    counts={g:len(entries) for g,entries in matrix.items()}
    if counts!=previous["H_totals"]:
        raise ValueError(f"The frozen H cohort changed in {task}")
    by_trial=[]
    for seed in setup["seeds"]:
        base=trial(row,seed)
        shared=vectors_at(base/"initial",row)
        size=setup["round_cycles"]
        storage=WORK/"score"/task/str(seed)
        a0=({g:[] for g in GROUPS} if shared is None else
            events(row,matrix,shared[:size],storage/"initial"))
        for cfg in setup["configs"]:
            run=load(base/cfg/"result.json")
            matches=a0
            h_history={}
            if shared is not None:
                h_history["1"]=a0
                if cfg=="A0-long":
                    matches=extend_exposure(row,matrix,shared,storage/cfg,a0)
                    h_history["full"]=matches
                elif cfg!="A0":
                    vectors=shared[:size]
                    for stage in run["history"][1:]:
                        current=stage["round"]
                        source=stage["source"]
                        if source=="initial_slice":
                            appended=shared[(current-1)*size:current*size]
                        else:
                            appended=vectors_at(base/cfg/source,row)
                        vectors=vectors+appended
                        assert len(vectors)==stage["cycles"]
                        if cfg in ("B","O") or stage==run["history"][-1]:
                            matches=extend_exposure(row,matrix,vectors,storage/cfg/f"round{current}",matches)
                            h_history[str(current)]=matches
            by_trial.append({**run,"initial_H":a0,"final_H":matches,"H_history":h_history})
    data={"task":task,"clock":row["ports"]["clock"],"H_totals":counts,"trials":by_trial,
          "v1_long_random":previous["baseline"]}
    save(path,data)
    print(task,counts,"evaluation complete",flush=True)
    return data


def main():
    argument=argparse.ArgumentParser(description=__doc__)
    argument.add_argument("dataset",type=Path)
    argument.add_argument("--replay",action="store_true",help="recompute archived H evaluations")
    args=argument.parse_args()
    rows=public(args.dataset)
    assert ready(rows)==500
    start=datetime.now(timezone.utc)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda row:score(row,args.replay),rows))
    end=datetime.now(timezone.utc)
    totals={group:sum(result["H_totals"][group] for result in results) for group in GROUPS}
    assert totals=={"original_plus":100,"rare":95}
    save(ROOT/"evaluation"/"verification.json",{"generation_checkpoints_before_H":500,
         "evaluated_tasks":len(results),"runs":sum(len(r["trials"]) for r in results),"H_totals":totals,
         "evaluation_started_utc":start.isoformat(),"evaluation_completed_utc":end.isoformat(),
         "evaluation_seconds":(end-start).total_seconds()})


if __name__=="__main__":
    main()
