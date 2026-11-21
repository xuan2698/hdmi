"""Re-score every archived v1 diagnosis and cross-check a fixed sample."""

import argparse
import random
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from base import ROOT, V1, WORK, load, plan, public, save
from diagnostic import (ERRORS, continuous, diagnose, locate, run_extra,
                        value_call, wave_extra, wrap)
from evaluate import replay_vectors
from guide import span
from hdl import input_dir
from mutations import signals

DEST = ROOT / "audits" / "diagnostic"
LABELS = {"未到达","未感染","未传播"}


def old_reason(old, atom):
    reason=old.get("reason","")
    if reason.startswith("iverilog"):
        return "probe_compile_type_cast"
    if "结构或边沿" not in reason:
        return "other_probe_failure"
    rule=atom["rule"]
    if rule.startswith("Assign"):
        return "blocking_vs_nonblocking"
    if rule.startswith("Edge") or rule in {"clock_edge","temporal_reset"}:
        return "event_control"
    if rule.startswith("NSub"):
        return "statement_insertion_or_deletion"
    if "if" in atom["before"] or "case" in atom["before"]:
        return "nested_or_indexed_predicate"
    if atom["before"].strip().startswith("assign"):
        return "continuous_assignment"
    if atom["before"].count(";")>1:
        return "multiple_statements_per_line"
    return "other_expression_or_site"


def crosscheck(row, atom, folder, cycles):
    """Raw trace per execution and independent Python classification."""
    gold, variant=row["gold"],span(row,atom)
    ports=row["ports"]
    names=tuple({**ports["input"],**ports["output"],**signals(gold,ports["input"],ports["output"])})
    try:
        site=locate(gold,variant,atom["line"],atom["rule"],names)
        if not site:
            return {"label":"诊断不可用","method":"no independent source site"}
        if site.mode=="event":
            marker="task rv_event(input integer side); $display(\"RAWEVENT %0d %0d\",side,$time); endtask"
            out=run_extra(row,wrap(variant,site.mutant,"replay.rv_event(1);"),folder,cycles,marker,
                          wrap(gold,site.original,"replay.rv_event(0);"))
            sides=[Counter(),Counter()]
            for left, stamp in re.findall(r"^RAWEVENT ([01]) (\d+)",out["text"],re.M):
                sides[int(left)][int(stamp)]+=1
            label="未传播" if sides[0]!=sides[1] else "未感染" if sides[0] else "未到达"
            return {"label":label,"method":"actual process entry event lists","executions":list(map(lambda x:sum(x.values()),sides))}
        if site.mode=="schedule":
            name=re.match(r"^[a-zA-Z_]\w*",site.lhs)
            statement='$display("RAWSITE");'
            out=run_extra(row,gold,folder,cycles,"",wrap(gold,site.original,statement))
            if not re.search(r"^RAWSITE$",out["text"],re.M):
                return {"label":"未到达","method":"raw original execution list"}
            if not name or site.module!=ports["top"]:
                return {"label":"诊断不可用","method":"local signal unavailable"}
            lhs=name[0]
            raw=f'''
always @(golden.{lhs} or mutated.{lhs}) begin
    #0; $display("RAWWAVE %0d %b %b",cycle+1,golden.{lhs},mutated.{lhs});
end
'''
            out=run_extra(row,variant,folder,cycles,raw)
            different=any("x" not in a and "z" not in a and a!=b
                          for a,b in re.findall(r"^RAWWAVE \d+ ([01xz]+) ([01xz]+)",out["text"],re.M))
            return {"label":"未传播" if different else "诊断不可用","method":"raw delta-cycle signal trace"}
        func=continuous if site.mode=="continuous" else wrap
        check=func(gold,site.original,value_call(site,raw=True))
        out=run_extra(row,gold,folder,cycles,"",check)
        if out["samples"]:
            return {"label":"诊断不可用","method":"raw probe output guard"}
        compared=0
        samples=0
        first=None
        for cycle, pre, post in re.findall(r"^RAWVALUE (\d+) ([01xz]+) ([01xz]+)",out["text"],re.M):
            samples+=1
            bits=[b!=a for a,b in zip(pre,post,strict=True) if a in "01"]
            compared+=bool(bits)
            if first is None and any(bits):
                first={"cycle":int(cycle),"original":pre,"mutant":post}
        label="未传播" if first else "未感染" if compared else "诊断不可用" if samples else "未到达"
        return {"label":label,"method":"raw expression trace, independent Python four-state comparison",
                "executions":samples,"comparable":compared,"first":first}
    except ERRORS as exc:
        return {"label":"诊断不可用","method":"raw trace failure","reason":str(exc).splitlines()[0][-140:]}


def entry(path, by_id, witness_entries):
    task,seed,config,current,_=path.relative_to(V1/"trial").parts
    seed=int(seed)
    round_no=int(current[5:])
    row=by_id[task]
    catalog=load(V1/"guidance"/task/"catalog.json")
    bank={item["id"]:item["edit"] for item in catalog["candidates"]}
    folder=WORK/"audit"/task/str(seed)/config/current
    result_path=DEST/task/str(seed)/config/(current+".json")
    old=load(path)
    vec=replay_vectors(row,seed,config,round_no-1)
    input_dir(folder,vec,row["ports"])
    records={}
    for key, evidence in old.items():
        if "diagnosis" not in evidence:
            continue
        atom=bank[key]
        former=evidence["diagnosis"]
        record={"old":former,"rule":atom["rule"],"line":atom["line"]}
        if former["label"] not in LABELS:
            record["old_category"]=old_reason(former,atom)
        record["new"]=diagnose(row,atom,folder,len(vec))
        if (str(path.relative_to(V1)),key) in witness_entries:
            record["crosscheck"]={**crosscheck(row,atom,folder,len(vec)),
                                  "original_line":atom["before"],"mutant_line":atom["after"]}
        records[key]=record
    save(result_path,records)
    return records


def aggregate(all_records):
    old, new, categories=Counter(),Counter(),Counter()
    remaining, transitions=Counter(),defaultdict(Counter)
    checked=[]
    examples=defaultdict(list)
    for (path,record) in all_records:
        for tag,item in record.items():
            old[item["old"]["label"]]+=1
            new[item["new"]["label"]]+=1
            transitions[item["old"]["label"]][item["new"]["label"]]+=1
            if item["new"]["label"] not in LABELS:
                remaining[item["new"]["reason"]]+=1
            category=item.get("old_category")
            if category:
                categories[category]+=1
                if len(examples[category])<2:
                    task=path.relative_to(V1/"trial").parts[0]
                    entries=load(V1/"guidance"/task/"catalog.json")["candidates"]
                    edit=next(e["edit"] for e in entries if e["id"]==tag)
                    examples[category].append({"record":str(path.relative_to(V1)),"G":tag,
                                                "line":item["line"],"rule":item["rule"],"example":item["old"],
                                                "original_line":edit["before"],"mutant_line":edit["after"]})
            if "crosscheck" in item:
                checked.append({"record":str(path.relative_to(V1)),"G":tag,"new":item["new"],**item["crosscheck"]})
    compared=[x for x in checked if x["label"] in LABELS and x["new"]["label"] in LABELS]
    stable=sum(new[x] for x in LABELS)
    total=sum(new.values())
    out={"total":total,"old_labels":dict(old),"new_labels":dict(new),"old_uncategorized_categories":dict(categories),
         "remaining_reasons":dict(remaining),"label_transitions":dict(transitions),
         "old_examples":dict(examples),"new_stable_fraction":stable/total,
         "crosscheck_size":len(checked),"crosscheck_compared":len(compared),
         "crosscheck_correct":sum(x["label"]==x["new"]["label"] for x in compared),
         "crosscheck_both_unavailable":sum(x["label"] not in LABELS and x["new"]["label"] not in LABELS for x in checked)}
    save(DEST/"sample.json",checked)
    save(DEST/"summary.json",out)
    print(out,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset",type=Path)
    parser.add_argument("--workers",type=int,default=3)
    parser.add_argument("--summary-only",action="store_true",help="summarize the existing archived replays")
    args=parser.parse_args()
    by_id={row["id"]:row for row in public(args.dataset)}
    paths=sorted(p for p in (V1/"trial").rglob("feedback.json") if p.parts[-3] in ("O","O+F"))
    if args.summary_only:
        files=((path, DEST/path.relative_to(V1/"trial").parent.with_suffix(".json")) for path in paths)
        aggregate((original,load(replayed)) for original,replayed in files)
        return
    population=[(str(p.relative_to(V1)),tag) for p in paths for tag,x in load(p).items() if "diagnosis" in x]
    selected=set(random.Random(plan()["audit_seed"]).sample(population,plan()["audit_sample_size"]))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        aggregate(zip(paths,pool.map(lambda p:entry(p,by_id,selected),paths)))


if __name__=="__main__":
    main()
