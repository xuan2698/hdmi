"""Incremental formal search for G, with original-RTL state replay."""

import argparse
import re
import subprocess
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from base import ROOT, V1, WORK, load, plan, public, save
from diagnostic import ERRORS, syntax
from formal_g import assertion, compressed, config, module, vcd_rows, vectors_from_witness
from guide import span
from hdl import bind_params, compile_sim, input_dir, observe
from pyslang import ast
from replay import rename

LOCK = threading.Lock()
LOCKS = {}
SOLVER_SLOTS = threading.BoundedSemaphore(2)
PREP_TIMEOUT = 8


def command(args, work, timeout):
    start=time.monotonic()
    try:
        p=subprocess.run(args,cwd=work,capture_output=True,text=True,timeout=timeout)
        return p.returncode, p.stdout+p.stderr, round(time.monotonic()-start,3)
    except subprocess.TimeoutExpired as exc:
        log=exc.stdout.decode(errors="replace") if exc.stdout else ""
        return None,log,round(time.monotonic()-start,3)


def prepare(row, variant, work, normalize=False):
    ports=row["ports"]
    params=ports["parameters"].copy()
    ram=ports["top"]=="custom_byte_enable_ram"
    if ram:
        params["LINES"]=8
    gold=row["gold"]
    if normalize:
        gold,variant=(re.sub(r"\balways_comb\b","always @*",s) for s in (gold,variant))
        if row["id"].endswith("word_change_detector_0012"):
            gold,variant=(re.sub(r"\bchange_pulse\s*<=\s*[^;]+;",";",s) for s in (gold,variant))
    claim=assertion(ports)
    if ram:
        claim=claim.replace("endmodule","always @* assume ((in_addr_a < 8) && (in_addr_b < 8));\nendmodule")
    for name,source in (("golden",rename(gold,"cvdp_r_")),("mutant",rename(variant,"cvdp_m_")),
                        ("miter",bind_params(module(ports),ports["top"],params)),("assertion",claim)):
        (work/(name+".sv")).write_text(source)
    script=config(9).split("[script]\n",1)[1].split("[files]",1)[0]+"""
opt_merge -share_all
opt_clean -purge
chformal -lower
formalff -setundef -clk2ff -ff2anyinit -hierarchy
opt_clean -purge
setundef -undriven -anyseq
stat
write_smt2 -wires model.smt2
"""
    (work/"prepare.ys").write_text(script)
    code,log,seconds=command(["yosys","-Q","-T","-s","prepare.ys"],work,PREP_TIMEOUT)
    (work/"prepare.log").write_text(log)
    reason=next((line.partition("ERROR:")[2].strip() for line in log.splitlines() if "ERROR:" in line),"")
    status="timeout" if code is None else "error" if code else "ready"
    return {"phase":"synthesis","status":status,"seconds":seconds,"reason":reason,
            "normalized":normalize,"subset":ram}


def state_signals(row, atom):
    ports=row["ports"]
    compilation=ast.Compilation()
    compilation.addSyntaxTree(syntax.SyntaxTree.fromText(row["gold"]))
    top=next((instance for instance in compilation.getRoot().topInstances
              if instance.name==ports["top"]),None)
    if top is None:
        return []
    declared={symbol.name:symbol.type.bitWidth for symbol in top.body
              if isinstance(symbol,(ast.VariableSymbol,ast.NetSymbol)) and symbol.type.isIntegral}
    keyword=re.compile(r"state|counter|cnt|shift_reg|second|minute|hour|prescal|divider|pulse|token|_reg$",re.I)
    relevant=atom["before"]+" "+atom["after"]
    names=sorted((sig for sig,width in declared.items()
                 if sig not in ports["input"] and sig not in ports["output"] and width<=64),
                 key=lambda sig:(not bool(keyword.search(sig)),not bool(re.search(rf"\b{sig}\b",relevant)),sig))
    return [n for n in names if keyword.search(n) or re.search(rf"\b{n}\b",relevant)][:8]


def state_replay(row, variant, atom, folder, cycles, first):
    names=state_signals(row,atom)
    # Capture both instances immediately before the sampled edge updates state.
    args=["cycle+1","phase","ref_bits","mut_bits"]
    for sig in names:
        args.extend((f"golden.{sig}",f"mutated.{sig}"))
    fmt="STATE %0d %b"+" %b"*(len(args)-2)
    hook=f'always @(posedge phase, negedge phase) $display("{fmt}", {", ".join(args)});'
    try:
        report=observe(compile_sim(row["gold"],variant,row["ports"],hook),folder,cycles)
    except ERRORS:
        return {"signals":names,"samples":[],"reason":"无法在原始 RTL 层次中读取全部候选状态"}
    states=[]
    for line in report["text"].splitlines():
        if not line.startswith("STATE "):
            continue
        _, cyc,phase,a,b,*words=line.split()
        if not max(1,first-1)<=int(cyc)<=first:
            continue
        states.append({"cycle":int(cyc),"edge":"posedge" if phase=="1" else "negedge",
                       "golden_outputs_binary":a,"mutant_outputs_binary":b,
                       "internal":{n:{"gold":x,"mutant":y}
                                   for n,x,y in zip(names,words[::2],words[1::2],strict=True)}})
    return {"signals":names,"samples":states}


def replay(row, variant, atom, work, trace):
    phases=vcd_rows(trace)
    vectors=vectors_from_witness(phases,row["ports"]["input"])
    folder=input_dir(work/"concrete",vectors,row["ports"])
    output=observe(compile_sim(row["gold"],variant,row["ports"]),folder,len(vectors))
    if not output["samples"]:
        return None
    first=output["first"]
    return {"cycles":first,"compressed":compressed(vectors,first),"concrete_inputs":vectors,
            "state":state_replay(row,variant,atom,folder,len(vectors),first)}


def solve(row, item, work, parameters):
    start=time.monotonic()
    work.mkdir(parents=True,exist_ok=True)
    variant=span(row,item["edit"])
    result={"task":row["id"],"id":item["id"],"attempts":[]}
    attempts=result["attempts"]
    p=prepare(row,variant,work)
    attempts.append(p)
    if p["status"]=="error" and any(term in p["reason"] for term in
                                    ("Latch inferred", "Assert", "Multiple edge sensitive")):
        p=prepare(row,variant,work,normalize=True)
        attempts.append(p)
    final=p["status"]
    if final=="ready":
        bounded=0
        saw_unverified=False
        for depth,limit in zip(parameters["formal_depths"],parameters["formal_stage_seconds"],strict=True):
            trace=work/(f"trace{depth}.vcd")
            trace.unlink(missing_ok=True)
            code,log,seconds=command(["yosys-smtbmc","-s","boolector","-t",str(4*depth+1),
                                     "--dump-vcd",trace.name,"model.smt2"],work,limit)
            (work/(f"solve{depth}.log")).write_text(log)
            status=("timeout" if code is None else "candidate" if "Status: FAILED" in log else
                    "bounded_pass" if "Status: PASSED" in log else "error")
            stage={"phase":"BMC","cycles":depth,"status":status,"seconds":seconds}
            attempts.append(stage)
            final=status
            if status=="candidate":
                try:
                    witness=replay(row,variant,item["edit"],work,trace) if trace.exists() else None
                except (*ERRORS, KeyError) as exc:
                    witness=None
                    stage["replay_error"]=str(exc)[-240:]
                if witness:
                    result.update(witness)
                    final="witness"
                    break
                stage["status"]="unverified"
                saw_unverified=True
                final="unverified"
            elif status=="bounded_pass":
                bounded=depth
            elif status=="error":
                stage["error"]=log.splitlines()[-1] if log.splitlines() else str(code)
                break
        if final=="bounded_pass" and (p["normalized"] or p["subset"]):
            final="restricted_pass"
        if final=="bounded_pass" and saw_unverified:
            final="unverified"
        result["bounded_cycles_completed"]=bounded
    result.update(status=final,solve_wall_seconds=round(time.monotonic()-start,3))
    return result


def evidence(row, item):
    task=row["id"]
    directory=ROOT/"formal"/task
    path=directory/(item["id"]+".json")
    with LOCK:
        lock=LOCKS.setdefault((task,item["id"]),threading.Lock())
    with lock:
        if path.exists():
            return load(path)
        with SOLVER_SLOTS:
            result=solve(row,item,WORK/"formal"/task/item["id"],plan())
        save(path,result)
        return result


def previous_error(record, newer):
    status=record["status"]
    reason=record.get("reason","")
    if status=="TIMEOUT":
        if newer["attempts"][0]["subset"]:
            return "旧项超时，原 RAM 8192 地址导致展开规模较大"
        return "旧项达到 10 秒总时限，历史回执未区分综合与求解"
    if "!enc.driven" in reason:
        return "Yosys xprop 不接受已有多驱动"
    if "Multiple edge" in reason:
        return "Yosys 不能降低该多边沿触发块"
    if "Latch inferred" in reason:
        return "always_comb 的变异分支被推断为锁存器"
    return reason


def audit(dataset):
    rows={r["id"]:r for r in public(dataset)}
    jobs=[]
    for task,row in rows.items():
        catalog=load(V1/"guidance"/task/"catalog.json")
        by_tag={entry["id"]:entry for entry in catalog["candidates"]}
        for old in sorted((V1/"guidance"/task/"formal").glob("*.json")):
            jobs.append((row,by_tag[old.stem],load(old)))
    def work(job):
        row,item,old=job
        newer=evidence(row,item)
        record={"task":row["id"],"id":item["id"],"v1":old["status"],"v2":newer["status"],
                "cause":previous_error(old,newer),"previous_seconds":old["solve_wall_seconds"],
                "seconds":newer["solve_wall_seconds"],"witness_cycles":newer.get("cycles"),
                "state_signals":newer.get("state",{}).get("signals",[]),"attempts":newer["attempts"]}
        print(record["task"],record["id"],record["v1"],record["v2"],record["seconds"],flush=True)
        return record
    with ThreadPoolExecutor(max_workers=2) as pool:
        records=list(pool.map(work,jobs))
    save(ROOT/"audits"/"formal.json",records)
    print("v1",Counter(r["v1"] for r in records),"v2",Counter(r["v2"] for r in records),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset",type=Path)
    args=parser.parse_args()
    audit(args.dataset)
