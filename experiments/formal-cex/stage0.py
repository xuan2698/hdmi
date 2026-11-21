"""Build rule G from frozen proxies and check the development toolchain gate."""

import argparse
import csv
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from inputs import ROOT, REPO, GEN, development, load, save, sha

sys.path.insert(0, str(REPO / "stimulus-v1"))
import hdl
from formal_g import assertion, config, module, vcd_rows, vectors_from_witness
from guide import variants
from mutations import Candidate
from pyslang import ast, syntax
from replay import SimulationError, rename

WORK = ROOT / ".work"
hdl.WORK = WORK / "proxy_sim"
G = GEN / "G"
RESULTS = ROOT / "stage0"
BUDGET = 120
BOUNDS = (20, 40, 80)
PROXY_LIMIT = 24
ERRORS = (SimulationError, RuntimeError, ValueError, KeyError, OSError)
CLOCK = re.compile(r"\b(?:pos|neg)edge\s+([A-Za-z_]\w*)")
RESET = re.compile(r"rst|reset", re.I)
ACTIVE_LOW = re.compile(r"(?:_n|_b|rstn|resetn|nreset)$", re.I)
FORBIDDEN = re.compile(r'`\s*include\b|\bDPI\b|\$(?:fopen|fread|fwrite|readmem\w*|writemem\w*|system|sformatf)\b')


def inventory():
    ledger=GEN/"proxy_inventory.csv"
    name=str(ledger.relative_to(REPO))
    immutable=subprocess.check_output(["git","show",f"HEAD:{name}"],cwd=REPO)
    if immutable != ledger.read_bytes():
        raise ValueError("Commit the proxy inventory before deriving any G")
    with ledger.open() as handle:
        rows=list(csv.DictReader(handle))
    if len(rows)!=100 or set(r["task"] for r in rows)!=set(development()):
        raise ValueError("Expected 100 slots in the frozen CVDP proxy inventory")
    for row in rows:
        if row["status"]!="received":
            continue
        file=ROOT/row["source"]
        if sha(file.read_bytes())!=row["sha256"]:
            raise ValueError(f"Proxy hash changed: {file}")
        if sha(subprocess.check_output(["git","show",f"HEAD:{file.relative_to(REPO)}"],cwd=REPO))!=row["sha256"]:
            raise ValueError(f"Proxy file is not frozen: {file}")
    return rows


def interface(source, parameters):
    if FORBIDDEN.search(source):
        raise ValueError("unsupported external system task or include")
    compiler=ast.Compilation()
    compiler.addSyntaxTree(syntax.SyntaxTree.fromText(source))
    instances=list(compiler.getRoot().topInstances)
    if len(instances)!=1:
        raise ValueError("expected one elaborated top module")
    top=instances[0]
    pins={"In":{},"Out":{}}
    for p in top.body.portList:
        direction=str(p.direction).rsplit(".",1)[-1]
        if direction not in pins or not p.type.isIntegral or p.type.isUnpackedArray:
            raise ValueError(f"unsupported port type or direction: {p.name}")
        pins[direction][p.name]=p.type.bitWidth
    if not pins["Out"]:
        raise ValueError("expected an output port")
    source=re.sub(r"//[^\n]*|/\*.*?\*/","",source,flags=re.S)
    edge_pins=set(CLOCK.findall(source)) & pins["In"].keys()
    resets={name for name in pins["In"] if RESET.search(name)}
    clocks=sorted(edge_pins-resets)
    if len(clocks)!=1:
        named=[p for p in pins["In"] if re.fullmatch(r"(?:i_)?(?:clk|clock)(?:_in)?",p,re.I)]
        if len(named)==1:
            clocks=named
    if len(clocks)!=1 or pins["In"][clocks[0]]!=1:
        raise ValueError("unable to identify one scalar primary clock")
    clock=clocks[0]
    reset_polarity={}
    for name in resets:
        if pins["In"][name]!=1:
            continue
        pattern=rf"\b(posedge|negedge)\s+{re.escape(name)}\b"
        edges=set(re.findall(pattern,source))
        if len(edges)==1:
            reset_polarity[name]=int(edges=={"posedge"})
        else:
            reset_polarity[name]=int(not ACTIVE_LOW.search(name))
    # Parameter omissions are interface failures, rather than silently altering
    # the already frozen parameter configuration.
    declared={p.name for p in top.body.parameters}
    if missing:=sorted(set(parameters)-declared):
        raise ValueError("frozen parameters absent from proxy: "+", ".join(missing))
    return {"top":top.name,"clock":clock,"input":{k:v for k,v in pins["In"].items() if k!=clock},
            "output":pins["Out"],"resets":reset_polarity,"parameters":parameters}


def catalog(row, limits):
    task,proxy=row["task"],row["proxy"]
    out=G/task/proxy/"catalog.json"
    if out.exists():
        data=load(out)
        if data["proxy_sha256"]!=row["sha256"]:
            raise ValueError(f"Stale G catalog {task}/{proxy}")
        return data
    source=(ROOT/row["source"]).read_text() if row["source"] else ""
    data={"task":task,"proxy":proxy,"proxy_sha256":row["sha256"],"status":"ready","reason":"",
          "ports":None,"candidates":[],"rejected":[]}
    if not source:
        data.update(status="other",reason="no archived API source")
    else:
        try:
            ports=interface(source,limits[task])
            example=hdl.reset_rows(ports,20261121,12)
            local=hdl.input_dir(WORK/"catalog"/task/proxy,example,ports)
            ref=hdl.compile_sim(source,source,ports)
            if hdl.observe(ref,local,len(example))["samples"]:
                raise ValueError("self-comparison failed under proxy I/O harness")
        except ERRORS as exc:
            reason=str(exc).splitlines()[0][-350:]
            data.update(status="unsupported_syntax" if "unsupported" in reason else "parse_or_elab_failure",
                        reason=reason)
        else:
            data["ports"]=ports
            for candidate in variants({"id":task,"gold":source,"ports":ports}):
                if len(data["candidates"])==PROXY_LIMIT:
                    break
                try:
                    mutant=candidate.rtl(source)
                    build=hdl.compile_sim(source,mutant,ports)
                    hdl.observe(build,local,len(example))
                except ERRORS as exc:
                    data["rejected"].append({"rule":candidate.rule,"line":candidate.line,
                                             "reason":str(exc).splitlines()[0][-200:]})
                    continue
                from dataclasses import asdict
                data["candidates"].append({"id":f"G{len(data['candidates'])+1:02d}",
                                           "mutant_sha256":sha(mutant.encode()),"edit":asdict(candidate)})
            if not data["candidates"]:
                data.update(status="other",reason="no syntactically usable rule edits")
    save(out,data)
    return data


def formal_design(source, mutant, ports, work, repair):
    if repair>=1:
        source=re.sub(r"\balways_comb\b","always @*",source)
        mutant=re.sub(r"\balways_comb\b","always @*",mutant)
    miter=hdl.bind_params(module(ports),ports["top"],ports["parameters"])
    assertion_source=assertion(ports)
    for name,content in (("reference.sv",rename(source,"cvdp_r_")),
                         ("mutant.sv",rename(mutant,"cvdp_m_")),
                         ("miter.sv",miter),("assertion.sv",assertion_source)):
        (work/name).write_text(content)


def run_sby(work, label, engine, limit, step, repair):
    file=work/(label+".sby")
    cfg=config(step,engine=f"smtbmc {engine}",timeout=max(1,round(limit)))
    cfg=cfg.replace("golden.sv","reference.sv")
    if repair>=2:
        cfg=cfg.replace("opt -keepdc\nread_verilog -formal assertion.sv",
                        "opt -keepdc\nopt_merge -share_all\nopt_clean -purge\nread_verilog -formal assertion.sv")
    file.write_text(cfg)
    start=time.monotonic()
    process=subprocess.Popen(["sby","-f",file.name],cwd=work,stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,text=True,start_new_session=True)
    try:
        logfile,_=process.communicate(timeout=limit+0.5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:
            pass
        logfile,_=process.communicate()
    folder=work/label
    (work/(label+".log")).write_text(logfile)
    status_path=folder/"status"
    status=status_path.read_text().split()[0] if status_path.exists() else "TIMEOUT"
    trace=next(folder.glob("engine_*/trace.vcd"),None)
    points=[int(m[1]) for m in re.finditer(r"Checking assertions in step (\d+)",logfile)]
    reason=next((line.partition("ERROR:")[2].strip() for line in logfile.splitlines() if "ERROR:" in line),"")
    return status, trace, reason, round(time.monotonic()-start,3), max(points,default=None)


def check_witness(source, mutant, ports, work, trace):
    try:
        seq=vectors_from_witness(vcd_rows(trace),ports["input"])
    except ERRORS as exc:
        return "conversion_failure",str(exc)[-250:],None
    if not seq or any(seq[0].get(name)!=value for name,value in ports["resets"].items()):
        return "reset_mismatch","converted first cycle does not assert the declared reset",None
    try:
        local=hdl.input_dir(work/"concrete",seq,ports)
        replay=hdl.observe(hdl.compile_sim(source,mutant,ports),local,len(seq))
    except ERRORS as exc:
        return "conversion_failure",str(exc)[-250:],None
    if not replay["samples"]:
        return "conversion_failure","no output difference under the dual-edge proxy replay",None
    return "counterexample","",seq[:replay["first"]]


def solve(row,candidate,repair):
    task,proxy,tag=row["task"],row["proxy"],candidate["id"]
    out=RESULTS/f"round{repair}"/task/proxy/(tag+".json")
    if out.exists():
        return load(out)
    start=time.monotonic()
    path=GEN/task/proxy/"proxy.sv"
    source=path.read_text()
    mutant=Candidate(**candidate["edit"]).rtl(source)
    if sha(mutant.encode())!=candidate["mutant_sha256"]:
        raise ValueError(f"Derived G checksum drift: {task}/{proxy}/{tag}")
    ports=row["ports"]
    work=WORK/"formal"/f"round{repair}"/task/proxy/tag
    work.mkdir(parents=True,exist_ok=True)
    formal_design(source,mutant,ports,work,repair)
    attempts=[]
    category="timeout"
    formal_success=False
    sequence=None
    reason=""
    # One incremental search covers each preregistered checkpoint without
    # restarting synthesis and the solver at depths 20 and 40.
    for engine,allocation in (("boolector",75),("z3",120)):
        limit=min(allocation,BUDGET-(time.monotonic()-start)-0.75)
        if limit<1:
            break
        status,trace,reason,took,step=run_sby(work,engine,engine,limit,4*BOUNDS[-1]+1,repair)
        attempts.append({"solver":engine,"status":status,"seconds":took,"last_formal_step":step,
                         "levels_reached":[bound for bound in BOUNDS if step is not None and step>=4*bound],
                         "reason":reason})
        if status=="PASS":
            formal_success=True
            category="bounded_equivalent"
            break
        if status=="FAIL" and trace is not None:
            formal_success=True
            category,reason,sequence=check_witness(source,mutant,ports,work,trace)
            if sequence is not None:
                break
            continue
        if status=="ERROR":
            if re.search("not supported|unsupported|Multiple edge|Latch inferred|Assert .*failed|async2sync",reason,re.I):
                category="unsupported_syntax"
            elif re.search("syntax|parse|cannot|module|port",reason,re.I):
                category="parse_or_elab_failure"
            else:
                category="other"
            if reason:
                break
    result={"task":task,"proxy":proxy,"G":tag,"category":category,"formal_success":formal_success,
            "replayable":sequence is not None,"cycles":len(sequence) if sequence else None,
            "reset_cycles":1 if ports["resets"] else 0,"reason":reason,
            "seconds":round(time.monotonic()-start,3),"attempts":attempts}
    if sequence:
        result["inputs"]=sequence
        result["trace_sha256"]=hashlib.sha256(trace.read_bytes()).hexdigest()
    save(out,result)
    return result


def aggregate(catalogs,results,repair):
    folder=ROOT/"reports"
    path=folder/f"stage0_round{repair}_pairs.csv"
    keys=["task","proxy","G","category","formal_success","replayable","cycles","reset_cycles","seconds","reason"]
    with path.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,keys,extrasaction="ignore",lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    categories=Counter(r["category"] for r in results)
    jobs=len(results)
    available=sum(c["status"]=="ready" for c in catalogs)
    success=sum(r["formal_success"] for r in results)
    usable=sum(r["replayable"] or r["category"]=="bounded_equivalent" for r in results)
    summary={"round":repair,"proxy_slots":len(catalogs),"ready_proxies":available,
             "proxy_failures":dict(Counter(c["status"] for c in catalogs if c["status"]!="ready")),
             "pairs":jobs,"categories":dict(categories),"formal_success":success,
             "formal_success_rate":success/jobs if jobs else None,
             "replay_or_bounded_success_rate":usable/jobs if jobs else None,
             "replayable":sum(r["replayable"] for r in results),
             "seconds_sum":round(sum(r["seconds"] for r in results),3)}
    save(folder/f"stage0_round{repair}.json",summary)
    print(summary,flush=True)
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workers",type=int,default=6)
    p.add_argument("--catalog-only",action="store_true")
    p.add_argument("--repair",type=int,choices=range(3),default=0)
    args=p.parse_args()
    limits=load(REPO/"stimulus-v1/split.json")["parameters"]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        catalogs=list(pool.map(lambda r:catalog(r,limits),inventory()))
        jobs=[(r,c) for r in catalogs for c in r["candidates"]]
        print("Frozen proxy-derived G",len(jobs),dict(Counter(r["status"] for r in catalogs)),flush=True)
        if args.catalog_only:
            return
        work=[pool.submit(solve,r,c,args.repair) for r,c in jobs]
        results=[]
        for i,future in enumerate(as_completed(work),1):
            results.append(future.result())
            if i%100==0:
                print("Checked formal pairs",i,"/",len(work),flush=True)
        aggregate(catalogs,sorted(results,key=lambda r:(r["task"],r["proxy"],r["G"])),args.repair)


if __name__=="__main__":
    main()
