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
from dataclasses import asdict
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


def interface(source, parameters, task=""):
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
    parameters=parameters.copy()
    declared={p.name for p in top.body.parameters}
    if task.endswith("IIR_filter_0012") and "WIDTH" not in declared and parameters.get("WIDTH")==16:
        data_pins={**{n:w for n,w in pins["In"].items() if re.fullmatch(r"in_[123]",n)},
                   **{n:w for n,w in pins["Out"].items() if re.fullmatch(r"out_[123]",n)}}
        if len(data_pins)==6 and set(data_pins.values())=={16}:
            # The task's selected parameter width is already hard-coded in the
            # independently generated source. No proxy text is changed.
            parameters.pop("WIDTH")
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
        if data.get("reason")!="frozen parameters absent from proxy: WIDTH":
            return data
        prior=out.with_name("catalog_pre_width_repair.json")
        if not prior.exists():
            save(prior,data)
    source=(ROOT/row["source"]).read_text() if row["source"] else ""
    data={"task":task,"proxy":proxy,"proxy_sha256":row["sha256"],"status":"ready","reason":"",
          "ports":None,"candidates":[],"rejected":[]}
    if not source:
        data.update(status="other",reason="no archived API source")
    else:
        try:
            ports=interface(source,limits[task],task)
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
                data["candidates"].append({"id":f"G{len(data['candidates'])+1:02d}",
                                           "mutant_sha256":sha(mutant.encode()),"edit":asdict(candidate)})
            if not data["candidates"]:
                data.update(status="other",reason="no syntactically usable rule edits")
    save(out,data)
    return data


def formal_design(source, mutant, ports, work, repair, restricted=False, normalized=False):
    if normalized:
        source=re.sub(r"\balways_comb\b","always @*",source)
        mutant=re.sub(r"\balways_comb\b","always @*",mutant)
    parameters=ports["parameters"].copy()
    if restricted:
        parameters["LINES"]=8
    miter=hdl.bind_params(module(ports),ports["top"],parameters)
    assertion_source=assertion(ports)
    if restricted:
        bounds=" && ".join(f"(in_{name} < 8)" for name in ("addr_a","addr_b"))
        assertion_source=assertion_source.replace("endmodule",f"always @* assume ({bounds});\nendmodule")
    for name,content in (("reference.sv",rename(source,"cvdp_r_")),
                         ("mutant.sv",rename(mutant,"cvdp_m_")),
                         ("miter.sv",miter),("assertion.sv",assertion_source)):
        (work/name).write_text(content)


def internal_state(source, ports):
    compiler=ast.Compilation()
    compiler.addSyntaxTree(syntax.SyntaxTree.fromText(source))
    top=next(instance for instance in compiler.getRoot().topInstances if instance.name==ports["top"])
    pins={*ports["input"],*ports["output"],ports["clock"]}
    return {p.name:p.type.bitWidth for p in top.body
            if isinstance(p,(ast.VariableSymbol,ast.NetSymbol)) and p.name not in pins
            and re.fullmatch(r"[A-Za-z_]\w*",p.name) and p.type.isIntegral
            and not p.type.isUnpackedArray and 0<p.type.bitWidth<=64}


def state_property(source, mutant, ports, work):
    original=internal_state(source,ports)
    modified=internal_state(mutant,ports)
    shared={k:v for k,v in original.items() if modified.get(k)==v}
    if not shared or sum(shared.values())>1024:
        return None
    enriched={**ports,"output":{**ports["output"],**shared}}
    (work/"miter.sv").write_text(module(enriched))
    (work/"assertion.sv").write_text(assertion(enriched))
    tops=[prefix+ports["top"] for prefix in ("cvdp_r_","cvdp_m_")]
    parameters=" ".join(f"-set {k} {v}" for k,v in ports["parameters"].items())
    bind="\n".join(f"chparam {parameters} {top}" for top in tops) if parameters else ""
    select=" ".join(f"{top}/w:{name}" for top in tops for name in shared)
    return f"read_verilog -sv -formal reference.sv mutant.sv\n{bind}\nproc\nexpose {select}\nread_verilog -sv -formal miter.sv"


def reap_orphans(job):
    """SBY can leave a tool from a nested shell after a time limit."""
    for process in Path("/proc").iterdir():
        if not process.name.isdecimal():
            continue
        try:
            state, parent, *_=(process/"stat").read_text().rsplit(")",1)[1].split()
            if state=="Z" or parent!="1" or not (process/"cwd").resolve(strict=True).is_relative_to(job):
                continue
            exe=(process/"exe").resolve(strict=True).name
            if exe in {"yosys","boolector","z3","python3.12","python3.11","dash","bash"}:
                os.kill(int(process.name),signal.SIGKILL)
        except (PermissionError,FileNotFoundError,ProcessLookupError):
            continue


def run_sby(work, label, engine, limit, step, repair, mode="bmc", keep_memory=False, front=None):
    file=work/(label+".sby")
    engine_line=f"smtbmc {'--nopresat ' if repair else ''}{engine}"
    cfg=config(step,mode=mode,engine=engine_line,timeout=max(1,round(limit)))
    cfg=cfg.replace("golden.sv","reference.sv")
    if front:
        cfg=cfg.replace("read_verilog -sv -formal reference.sv mutant.sv miter.sv",front)
    if repair:
        cfg=cfg.replace("opt -keepdc", "opt -full -keepdc\nopt_merge -share_all")
    if keep_memory:
        cfg=cfg.replace("memory_map", "memory -nomap")
    file.write_text(cfg)
    start=time.monotonic()
    options=["--smtbmc",str(ROOT/"tools/grouped_smtbmc")] if repair and mode=="bmc" else []
    process=subprocess.Popen(["sby",*options,"-f",file.name],cwd=work,stdout=subprocess.PIPE,
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
    reap_orphans(folder)
    (work/(label+".log")).write_text(logfile)
    status_path=folder/"status"
    status=status_path.read_text().split()[0] if status_path.exists() else "TIMEOUT"
    trace=next(folder.glob("engine_*/trace.vcd"),None)
    points=[int(m[2] or m[1]) for m in re.finditer(r"Checking assertions in steps? (\d+)(?: to (\d+))?",logfile)]
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


def solve(row,candidate,repair,quick=False):
    task,proxy,tag=row["task"],row["proxy"],candidate["id"]
    out=RESULTS/f"round{repair}"/task/proxy/(tag+".json")
    if out.exists():
        return load(out)
    for earlier in reversed(range(repair)):
        old=RESULTS/f"round{earlier}"/task/proxy/(tag+".json")
        if old.exists():
            prior=load(old)
            if prior["category"] in {"counterexample","bounded_equivalent"}:
                result={**prior,"reused_round_result":earlier}
                save(out,result)
                return result
    quick_file=RESULTS/f"quick{repair}"/task/proxy/(tag+".json")
    initial=load(quick_file) if quick_file.exists() else None
    if quick and initial is not None:
        return initial
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
    attempts=initial["attempts"][:] if initial else []
    spent=initial["seconds"] if initial else 0
    category="timeout"
    formal_success=False
    sequence=None
    reason=""
    def attempt(label,engine,stage_limit,step,mode="bmc",restricted=False,keep_memory=False,front=None):
        nonlocal category,formal_success,sequence,reason,trace
        limit=min(stage_limit,BUDGET-spent-(time.monotonic()-start)-0.75)
        if limit<1:
            return False
        status,maybe_trace,note,took,last=run_sby(work,label,engine,limit,step,repair,mode,keep_memory,front)
        attempts.append({"solver":engine,"mode":mode,"status":status,"seconds":took,
                         "restricted":restricted,"strengthened_state_property":bool(front),"last_formal_step":last,
                         "levels_reached":[b for b in BOUNDS if last is not None and last>=4*b],
                         "reason":note})
        if status=="PASS" and not restricted and (mode=="prove" or step==4*BOUNDS[-1]+1):
            formal_success=True
            category="bounded_equivalent"
            attempts[-1]["levels_certified"]=list(BOUNDS)
            return True
        if front:
            return False
        if status=="FAIL" and maybe_trace is not None:
            category,reason,sequence=check_witness(source,mutant,ports,work,maybe_trace)
            if not restricted or sequence is not None:
                formal_success=True
            if sequence is not None:
                trace=maybe_trace
                return True
        elif status=="ERROR":
            reason=note
            if re.search("not supported|unsupported|Multiple edge|Latch inferred|Assert .*failed|async2sync",note,re.I):
                category="unsupported_syntax"
            elif re.search("syntax|parse|cannot|module|port",note,re.I):
                category="parse_or_elab_failure"
            else:
                category="other"
            return not restricted and bool(note)
        return False

    trace=None
    ram=repair and ports["parameters"].get("LINES",0)>64 and {"addr_a","addr_b"}<=ports["input"].keys()
    complete=False
    if ram and not initial:
        formal_design(source,mutant,ports,work,repair,restricted=True)
        complete=attempt("boolector_small_ram","boolector",4,4*BOUNDS[0]+1,restricted=True)
        if not complete:
            formal_design(source,mutant,ports,work,repair)
    if repair and not complete and not ram and not initial:
        # A proof by induction also certifies each of the requested finite
        # bounds. A failed induction never counts as a concrete witness.
        complete=attempt("boolector_induction","boolector",4,16,mode="prove")
    if repair>=2 and not complete and not ram and not initial:
        try:
            front=state_property(source,mutant,ports,work)
        except (ValueError,StopIteration,AttributeError):
            front=None
        if front:
            complete=attempt("boolector_state_induction","boolector",8,16,mode="prove",front=front)
            if not complete:
                formal_design(source,mutant,ports,work,repair)
    # One incremental search covers each preregistered checkpoint without
    # restarting synthesis and the solver at depths 20 and 40.
    if not complete and not quick:
        for engine,allocation in (("boolector",75),("z3",120)):
            if attempt(engine,engine,allocation,4*BOUNDS[-1]+1,keep_memory=ram):
                break
    result={"task":task,"proxy":proxy,"G":tag,"category":category,"formal_success":formal_success,
            "replayable":sequence is not None,"cycles":len(sequence) if sequence else None,
            "reset_cycles":1 if ports["resets"] else 0,"reason":reason,
            "seconds":round(spent+time.monotonic()-start,3),"attempts":attempts}
    if sequence:
        result["inputs"]=sequence
        result["trace_sha256"]=hashlib.sha256(trace.read_bytes()).hexdigest()
    if quick and not complete:
        result["category"]="pending_full_bmc"
        save(quick_file,result)
    else:
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
    p.add_argument("--task")
    p.add_argument("--summarize",action="store_true")
    p.add_argument("--quick",action="store_true")
    p.add_argument("--repair",type=int,choices=range(3),default=0)
    args=p.parse_args()
    limits=load(REPO/"stimulus-v1/split.json")["parameters"]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        sources=[row for row in inventory() if not args.task or row["task"]==args.task]
        catalogs=list(pool.map(lambda r:catalog(r,limits),sources))
        jobs=[(r,c) for r in catalogs for c in r["candidates"]]
        print("Frozen proxy-derived G",len(jobs),dict(Counter(r["status"] for r in catalogs)),flush=True)
        if args.catalog_only:
            return
        if args.summarize:
            found=[RESULTS/f"round{args.repair}"/r["task"]/r["proxy"]/(c["id"]+".json") for r,c in jobs]
            aggregate(catalogs,[load(path) for path in found],args.repair)
            return
        work=[pool.submit(solve,r,c,args.repair,args.quick) for r,c in sorted(jobs,key=lambda job:
              sha(f"{job[0]['task']}/{job[0]['proxy']}/{job[1]['id']}".encode()))]
        results=[]
        for i,future in enumerate(as_completed(work),1):
            results.append(future.result())
            if i%100==0:
                print("Checked formal pairs",i,"/",len(work),flush=True)
        if not args.task and not args.quick:
            aggregate(catalogs,sorted(results,key=lambda r:(r["task"],r["proxy"],r["G"])),args.repair)


if __name__=="__main__":
    main()
