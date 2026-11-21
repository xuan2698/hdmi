"""Generate and profile the five stimulus configurations using only G."""

import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from base import V1, WORK, generate, load, plan, public, save, trial, vectors_at
from diagnostic import diagnose
from guide import span
from hdl import compile_sim, input_dir, observe
from mutations import Candidate
from solver import evidence

GATE = threading.Lock()
LOCKS = {}


@lru_cache(maxsize=16)
def catalog(task):
    return load(V1/"guidance"/task/"catalog.json")["candidates"]


def measure(row, variants, folder, cycles):
    return [item["id"] for item in variants if
            observe(compile_sim(row["gold"],span(row,item["edit"]),row["ports"]),folder,cycles)["samples"]]


def shared(row, seed, vectors, cases):
    task=row["id"]
    path=trial(row,seed)/"initial_G.json"
    with GATE:
        lock=LOCKS.setdefault((task,seed),threading.Lock())
    with lock:
        if not path.exists():
            folder=input_dir(WORK/"generating"/task/str(seed)/"shared",vectors,row["ports"])
            save(path,{"exposed":measure(row,cases,folder,len(vectors)),"total":len(cases)})
        return load(path)["exposed"]


def prompt_feedback(row, cfg, missed, folder, cycles):
    lines=[]
    entries={}
    for item in missed:
        tag, atom=item["id"],item["edit"]
        lines.append(Candidate(**atom).feedback(tag))
        entry={}
        if cfg in ("O","O+F"):
            entry["diagnosis"]=diagnose(row,atom,folder,cycles)
            lines.append(json.dumps(entry["diagnosis"],ensure_ascii=False))
        if cfg=="O+F":
            case=evidence(row,item)
            entry["formal_status"]=case["status"]
            if case["status"]=="witness":
                entry["formal"]={k:case[k] for k in ("cycles","compressed","state")}
                lines.append("Verified G witness: "+json.dumps(entry["formal"],ensure_ascii=False))
            else:
                lines.append(f"No usable bounded witness ({case['status']}).")
        entries[tag]=entry
    return entries,"\n".join(lines)


def read_source(path):
    return (path/load(path/"status.json")["source"]).read_text()


def job(row, seed, cfg):
    task=row["id"]
    model=plan()
    base=trial(row,seed)
    here=base/cfg
    destination=here/"result.json"
    if destination.exists():
        return
    init=base/"initial"
    bank=catalog(task)
    result={"task":task,"seed":seed,"config":cfg,"G_total":len(bank),"history":[]}
    full=vectors_at(init,row)
    if full is None:
        save(destination,{**result,"status":"initial_failed","stop":"initial_failed","cycles":0})
        return
    size=model["round_cycles"]
    vectors=full[:size]
    original=shared(row,seed,vectors,bank)
    exposed=set(original)
    hist=[{"round":1,"cycles":len(vectors),"exposed":sorted(exposed),"new":sorted(exposed),"source":"initial"}]
    stop="single_generation" if cfg in ("A0","A0-long") else "budget"
    if cfg=="A0-long":
        target=input_dir(WORK/"generating"/task/str(seed)/cfg/"complete",full,row["ports"])
        new=measure(row,[item for item in bank if item["id"] not in exposed],target,len(full))
        exposed.update(new)
        vectors=full
        hist.append({"round":1,"cycles":len(full),"exposed":sorted(exposed),"new":sorted(new),"source":"initial_full"})
    if cfg not in ("A0","A0-long"):
        previous=read_source(init)
        for i in range(2,model["max_rounds"]+1):
            missed=[item for item in bank if item["id"] not in exposed]
            work=WORK/"generating"/task/str(seed)/cfg
            where=here/f"round{i}"
            source=f"round{i}"
            if not missed:
                append=full[(i-1)*size:i*size]
                source="initial_slice"
            else:
                folder=input_dir(work/f"prefix{i}",vectors,row["ports"])
                entries,text=prompt_feedback(row,cfg,missed,folder,len(vectors))
                save(where/"feedback.json",entries)
                append=generate(where,row,seed+i-1,size,feedback=text,previous=previous)
                if append is None:
                    stop="append_failed"
                    break
                previous=read_source(where)
            vectors=vectors+append
            after=input_dir(work/f"round{i}",vectors,row["ports"])
            new=measure(row,missed,after,len(vectors))
            exposed.update(new)
            hist.append({"round":i,"cycles":len(vectors),"exposed":sorted(exposed),"new":sorted(new),"source":source})
    save(destination,{**result,"history":hist,"status":"complete","stop":stop,"cycles":len(vectors)})
    print(task,seed,cfg,len(vectors),len(exposed),stop,flush=True)


def ready(rows):
    expected=[trial(row,seed)/cfg/"result.json" for row in rows for seed in plan()["seeds"]
              for cfg in plan()["configs"]]
    missing=sum(not p.exists() for p in expected)
    if missing:
        raise ValueError(f"Generation matrix incomplete ({missing} missing)")
    return len(expected)


def main():
    argument=argparse.ArgumentParser(description=__doc__)
    argument.add_argument("dataset",type=Path)
    argument.add_argument("--workers",type=int,default=24)
    args=argument.parse_args()
    rows=public(args.dataset)
    jobs=[(r,s,c) for s in plan()["seeds"] for r in rows for c in plan()["configs"]]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda q:job(*q),jobs))
    assert ready(rows)==500


if __name__=="__main__":
    main()
