"""Audit the archived v2 schedule, prompts, and shared prefixes."""

import argparse
import json
import random
import subprocess
from collections import Counter
from pathlib import Path

from base import FROZEN, ROOT, V1, digest, load, plan, public, save, trial
from pilot3_generate import driver_rows
from run import ready


def verify(dataset):
    rows=public(dataset)
    count=ready(rows)
    design=plan()
    split=load(V1/"split.json")
    tasks={r["id"]:r for r in rows}
    assert set(tasks)==set(split["development"])
    assert len(split["final_test"])==15
    assert set(p.name for p in (ROOT/"trial").iterdir())==set(tasks)
    for name in ("README.md","protocol.json"):
        path=ROOT/name
        original=subprocess.check_output(["git","show",f"{FROZEN}:stimulus-v2/{name}"],cwd=ROOT)
        assert path.read_bytes()==original
    budgets=Counter()
    altered=0
    for row in rows:
        for seed in design["seeds"]:
            root=trial(row,seed)
            starting_G={}
            for cfg in design["configs"]:
                state=load(root/cfg/"result.json")
                sizes=[stage["cycles"] for stage in state["history"]]
                if state["status"]=="initial_failed":
                    assert not sizes and state["cycles"]==0
                else:
                    assert sizes[0]==4000 and sizes[-1]==state["cycles"]
                    assert sizes==sorted(set(sizes))
                    assert not any(set(a["exposed"])-set(b["exposed"]) for a,b in
                                   zip(state["history"],state["history"][1:]))
                    if cfg=="A0":
                        assert sizes==[4000]
                    elif cfg=="A0-long":
                        assert sizes==[4000,20000]
                    else:
                        assert sizes==list(range(4000,state["cycles"]+1,4000))
                    starting_G[cfg]=state["history"][0]["exposed"]
                budgets[(cfg,state["cycles"],state["stop"])]+=1
            assert len({tuple(v) for v in starting_G.values()})<=1
    for p in (ROOT/"trial").rglob("calls.jsonl"):
        for line in p.read_text().splitlines():
            r=json.loads(line)
            assert r["model_requested"]==design["model"]
            assert (r.get("model_actual") or design["model"])==design["model"]
            assert not any(f in r["prompt"] for f in ("/eval/","equiv-audit/","evaluation/"))
            altered+=1
    checks=[]
    locations=sorted(p for p in (ROOT/"trial").rglob("status.json") if load(p)["status"]=="complete")
    for path in random.Random(design["audit_seed"]).sample(locations,12):
        status=load(path)
        task=path.relative_to(ROOT/"trial").parts[0]
        code=(path.parent/status["source"]).read_text()
        vectors=driver_rows(code,tasks[task]["ports"]["input"],status["seed"],status["cycles"])
        assert digest(vectors)==status["vector_sha256"]
        checks.append(str(path.relative_to(ROOT)))
    summary={"frozen_commit":FROZEN,"checkpoints":count,"initials":100,"final_test_ids_only":15,
             "request_attempts_checked":altered,"reconstructed_segments":checks,
             "budgets":[{"config":cfg,"cycles":size,"stop":stop,"runs":n}
                        for (cfg,size,stop),n in sorted(budgets.items())]}
    save(ROOT/"reports"/"verification.json",summary)
    print(summary,flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset",type=Path)
    args=parser.parse_args()
    verify(args.dataset)
