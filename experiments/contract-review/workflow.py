"""Generate the contract-review treatments using only public specifications."""

import argparse
import copy
import hashlib
import itertools
import re
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from base_think import run as make_base_think
from core import (ROOT, V3, atomic, case_inputs, case_path, check_prompt, check_rows, compact,
                  decode_json, decode_python, digest, ensure_frozen, ledger, llm, load, new_artifact,
                  protocol, public, save, tasks, token_use, vectors)
from schema import (REVIEW_INSTRUCTIONS, REVISION_INSTRUCTIONS, review_validate, revision_snapshots,
                    sentence_map, vs_validate)
from write_contract import write

STOP=threading.Event()
CONFIGS=protocol()["configs"]
INDEPENDENT=ThreadPoolExecutor(max_workers=48)


class ArtifactMissing(RuntimeError):
    pass


def supplied(value,stage):
    if value is None:
        raise ArtifactMissing(stage)
    return value


def relative(path):
    return str(path.relative_to(ROOT))


def root_path(name):
    return ROOT/name


def remaining_disputes(first,second,previous,recent):
    previous_rules={item["id"]:item for item in first["rules"]}
    current_rules={item["id"]:item for item in second["rules"]}
    refreshed={item["rule_id"] for item in recent}
    carried=[item for item in previous
             if item["rule_id"] not in refreshed and
             (first==second if item["rule_id"]=="global" else
              item["rule_id"] in current_rules and
              previous_rules.get(item["rule_id"])==current_rules[item["rule_id"]])]
    return [*carried,*recent]


class Cell:
    def __init__(self,task,rep,think):
        self.task=task
        self.rep=rep
        self.think=think
        self.case=case_path(task,rep)/("on" if think else "off")
        spec,self.interface=public(task)
        self.spec=spec["spec"]
        self.context=case_inputs(task,rep)
        self.inputs,self.outputs=self.interface[:2]
        self.vectors=vectors(task,rep)
        self.examples=[item for item in load(ROOT/"examples.json")[task] if item["vectors"]]
        self.diagnostics={}

    def generate_json(self,folder,prompt,validate,repair_draft=False):
        if STOP.is_set():
            raise ArtifactMissing("cancelled after model access error")
        return new_artifact(folder,prompt,self.think,decode_json,validate,repair_draft=repair_draft,
                            compact_after_truncation=True)

    def model(self,folder,prompt,required=None,attempts=3):
        if STOP.is_set():
            raise ArtifactMissing("cancelled after model access error")
        def verify(code):
            check_rows(code,self.outputs,self.vectors)
            if required:
                for key in required:
                    if not re.search(rf"(?m)#.*\b{re.escape(key)}\b",code):
                        raise ValueError(f"Missing rule-ID comment {key}")
        code=new_artifact(folder,prompt,self.think,decode_python,verify,attempts=attempts,compact_after_truncation=True)
        if code is not None:
            atomic(folder/"model.py",code)
        return code

    def contract_model(self,body,overrides=None,feedback=""):
        ids=[rule["id"] for rule in body["rules"]]
        prompt=(self.context+check_prompt()+"\nFollow the supplied contract. Mark every rule ID in a Python "
                "comment where it is implemented. Use named state and explicit transitions where useful. "
                "Do not hardcode complete stimulus sequences.\nContract JSON:\n"+compact(body))
        if overrides:
            prompt+="\nFor the listed unresolved fields apply these candidate interpretations instead:\n"+compact(overrides)
        if feedback:
            prompt+="\nRepair only the failure on contract example A. The contract remains fixed.\n"+feedback
        return prompt,ids

    def review(self,body,round_no):
        folder=self.case/"reviews"/f"r{round_no}-{digest(body)[:16]}"
        # Independent context contains neither earlier conversation nor tool outputs.
        prompt=(REVIEW_INSTRUCTIONS+"\nIndexed specification:\n"+compact(sentence_map(self.spec))+
                "\nContract JSON:\n"+compact(body))
        value=self.generate_json(folder,prompt,lambda data:review_validate(data,body,self.spec,self.interface))
        if value is not None:
            save(folder/"review.json",value)
        return folder,supplied(value,f"review {round_no} schema")

    def trace(self,body,report,folder):
        kept=[]
        records=[]
        deps=[]
        pending={}
        def trace_side(item,side):
            target=folder/item["issue_id"]/side
            override=([{"rule_id":item["rule_id"],"interpretation":item["alternative"]}]
                      if side=="alternative" else None)
            text,_=self.contract_model(body,override)
            code=self.model(target,text)
            if code is None:
                return None
            try:
                return check_rows(code,self.outputs,item["sequence"])
            except (RuntimeError,ValueError,TypeError,subprocess.TimeoutExpired):
                return None
        for item in report["issues"]:
            if item["type"]=="ambiguity" and not (folder/item["issue_id"]/"verdict.json").is_file():
                pending[item["issue_id"]]={side:INDEPENDENT.submit(trace_side,item,side)
                                          for side in ("original","alternative")}
        for item in report["issues"]:
            if item["type"]!="ambiguity":
                kept.append(item)
                continue
            target=folder/item["issue_id"]
            if (target/"verdict.json").is_file():
                verdict=load(target/"verdict.json")
            else:
                out={side:result for side,job in pending[item["issue_id"]].items()
                     if (result:=job.result()) is not None}
                if len(out)!=2:
                    verdict={"status":"not_executable","issue_id":item["issue_id"],"outputs":out,"differences":[]}
                else:
                    changed=[{"cycle":i,"original":a,"alternative":b} for i,(a,b) in
                             enumerate(zip(out["original"],out["alternative"],strict=True),1) if a!=b]
                    verdict={"status":"effect" if changed else "no_effect","issue_id":item["issue_id"],
                             "outputs":out,"differences":changed}
                save(target/"verdict.json",verdict)
            deps+=list(target.glob("*/calls.jsonl"))
            records.append({"issue":item,**verdict})
            if verdict["status"]!="no_effect":
                kept.append({**item,"tool_result":{k:verdict[k] for k in ("status","differences")}})
        save(folder/"trace.json",records)
        return kept,records,[p.parent for p in deps]

    def round(self,body,no,trace,route):
        position=self.case/route/f"round{no}"
        rev_dir=position/"revision"
        rev_dir.mkdir(parents=True,exist_ok=True)
        review_dir,review=self.review(body,no)
        if trace:
            kept,records,deps=self.trace(body,review,position/"adjudication")
        else:
            kept,records,deps=review["issues"],[],[]
        if kept:
            prompt=(self.context+REVISION_INSTRUCTIONS+"\nCurrent contract JSON:\n"+compact(body)+
                    "\nRetained issues in order:\n"+compact(kept))
            revise=self.generate_json(rev_dir,prompt,lambda x:revision_snapshots(body,x,kept,self.spec,self.interface),
                                      repair_draft=True)
            supplied(revise,f"{route} revision {no} schema")
            new,edits=revision_snapshots(body,revise,kept,self.spec,self.interface)
        else:
            revise={"responses":[]}
            new,edits=body,[]
        save(rev_dir/"revision.json",revise)
        save(rev_dir/"contract.json",new)
        save(rev_dir/"edit_snapshots.json",edits)
        metrics={"route":route,"round":no,"review":relative(review_dir/"review.json"),
                 "revision":relative(rev_dir/"revision.json"),"contract":relative(rev_dir/"contract.json"),
                 "trace":relative(position/"adjudication"/"trace.json") if trace else None,
                 "issues":len(review["issues"]),"retained":len(kept),
                 "no_effect":sum(row["status"]=="no_effect" for row in records),
                 "no_executable":sum(row["status"]=="not_executable" for row in records),
                 "accepted":sum(row["decision"]=="accept" for row in revise["responses"]),
                 "rebutted":sum(row["decision"]=="rebut" for row in revise["responses"])}
        save(position/"summary.json",metrics)
        self.diagnostics[relative(rev_dir)]=edits
        rebutted={r["issue_id"] for r in revise["responses"] if r["decision"]=="rebut"}
        return new,[item for item in kept if item["issue_id"] in rebutted],metrics,[review_dir,*deps,rev_dir]

    def compact_resolution(self,body,unresolved):
        body=copy.deepcopy(body)
        marked={item["rule_id"] for item in unresolved}
        for rule in body["rules"]:
            if rule["id"] in marked:
                rule["uncertain"]=True
        notes={}
        for item in body["uncertain"]:
            notes.setdefault(item["rule_id"],[]).extend(item["candidates"])
        for item in unresolved:
            alt=item.get("alternative")
            notes.setdefault(item["rule_id"],[])
            if alt:
                notes[item["rule_id"]].append(alt)
        return body,{k:list(dict.fromkeys(v)) for k,v in notes.items()}

    def variants(self,notes):
        keys=[k for k,options in notes.items() if options]
        choices=[[None,*notes[k]] for k in keys]
        take=protocol()["max_candidate_combinations"]
        combinations=list(itertools.islice(itertools.product(*choices),take))
        for combination in combinations:
            yield [{"rule_id":key,"interpretation":value} for key,value in zip(keys,combination,strict=True) if value]

    def compare_examples(self,code,examples):
        if code is None:
            return [{"reason":"model is not executable"}]
        failures=[]
        for example_no,item in enumerate(examples,1):
            try:
                predictions=check_rows(code,self.outputs,item["vectors"])
            except (RuntimeError,ValueError,TypeError,subprocess.TimeoutExpired) as exc:
                failures.append({"example":example_no,"reason":str(exc)[:180]})
                continue
            for cycle,(want,actual) in enumerate(zip(item["expected"],predictions,strict=True),1):
                wrong={key:{"expected":val,"actual":actual[key]} for key,val in want.items() if val!=actual[key]}
                if wrong:
                    failures.append({"example":example_no,"cycle":cycle,"difference":wrong})
        return failures

    def resolve(self,body,unresolved,folder,no_b=False):
        final,notes=self.compact_resolution(body,unresolved)
        choices=list(self.variants(notes)) if self.examples and not no_b else [[]]
        outputs=[]
        deps=[]
        submitted=[]
        for n,overrides in enumerate(choices):
            tag=self.case/"final_models"/digest({"contract":final,"overrides":overrides})[:20]
            text,ids=self.contract_model(final,overrides)
            deps.append(tag)
            submitted.append((n,overrides,tag,INDEPENDENT.submit(self.model,tag,text,ids)))
        for n,overrides,tag,job in submitted:
            code=job.result()
            errors=self.compare_examples(code,self.examples) if not no_b and self.examples else []
            outputs.append({"n":n,"path":relative(tag/"model.py") if code is not None else None,
                            "overrides":overrides,"spec_errors":errors})
        matches=[v["n"] for v in outputs if v["path"] and not v["spec_errors"]]
        has_dispute=bool(notes)
        chosen=0
        if no_b:
            status="skipped"
        elif not has_dispute:
            status="no_dispute"
        elif not self.examples or not matches:
            status="unresolved_no_example"
        elif len(matches)==1:
            chosen=matches[0]
            status="selected_by_spec_example" if chosen else "author_matches"
        else:
            status="author_tie_break"
        choice=outputs[chosen]
        metadata={"status":status,"candidates":outputs,"selected":chosen,"remaining_fields":notes,
                  "has_dispute":has_dispute,"B_rejected":sum(bool(v["spec_errors"]) for v in outputs),
                  "B_executable_examples":len(self.examples),"writer_model":outputs[0]["path"],
                  "raw_model":choice["path"]}
        final={**final,"remaining_uncertain_fields":notes,"selected_interpretations":choice["overrides"]}
        save(folder/"final_contract.json",final)
        save(folder/"B_resolution.json",metadata)
        return final,choice,metadata,deps

    def check_a(self,final,choice,active):
        raw=choice["path"]
        if raw is None:
            return None,{"status":"not_executable","blocked":0,"failed_examples":[]},[]
        if not active:
            return raw,{"status":"skipped","blocked":0,"failed_examples":[]},[]
        examples=[r["example"] for r in final["rules"]]
        model=root_path(raw)
        code=model.read_text()
        first=self.compare_examples(code,examples)
        failures=[first]
        deps=[]
        counter=0
        for attempt in range(1,protocol()["max_contract_A_repairs"]+1):
            if not failures[-1]:
                break
            counter+=1
            path=self.case/"a_repairs"/digest({"final":final,"raw":raw})[:20]/f"try{attempt}"
            prompt,ids=self.contract_model(final,choice["overrides"],compact(failures[-1][:12]))
            candidate=self.model(path,prompt,ids,attempts=1)
            deps.append(path)
            if candidate is not None:
                model=path/"model.py"
            failures.append(self.compare_examples(candidate,examples))
        return relative(model),{"status":"passed" if not failures[-1] else "failed_remaining",
                                "blocked":counter,"failed_examples":failures,
                                "first_model":raw,"examples":len(examples)},deps

    def result(self,cfg,model,paths,**fields):
        item={"config":cfg,"task":self.task,"rep":self.rep,
              "status":"ready" if model else "generation_failed","model":model,
              "call_folders":[relative(path) for path in dict.fromkeys(paths)],
              "usage":token_use(paths),**fields}
        folder=case_path(self.task,self.rep)/"configs"/cfg
        save(folder/"result.json",item)
        return item

    def finish(self,cfg,body,unresolved,paths,rounds):
        folder=case_path(self.task,self.rep)/"configs"/cfg
        folder.mkdir(parents=True,exist_ok=True)
        final,choice,meta,deps=self.resolve(body,unresolved,folder,cfg=="Ours-noB")
        model,checked,repairs=self.check_a(final,choice,cfg!="Ours-noA")
        save(folder/"A_check.json",checked)
        return self.result(cfg,model,[*paths,*deps,*repairs],rounds=rounds,A=checked,B=meta)

    def process(self):
        task,rep=self.task,self.rep
        author,initial=write(task,rep,self.think)
        if not initial:
            for cfg in (("Ours-think",) if self.think else
                        ("Ours","Ours-R0","Ours-R1","Ours-noTrace","Ours-noA","Ours-noB")):
                self.result(cfg,None,[author],reason="initial contract schema exhausted")
            return
        standard=[author]
        if not self.think:
            self.finish("Ours-R0",initial,[],standard,[])
        history=[]
        first=None
        try:
            first,issues,row,deps=self.round(initial,1,True,"trace")
            standard=standard+deps
            history=[row]
            if not self.think:
                self.finish("Ours-R1",first,issues,standard,history)
            second,last_issues,row,deps=self.round(first,2,True,"trace")
            # Rejected issues from the first round are still unresolved if the
            # disputed rule survived and was not changed by the second round.
            open_issues=remaining_disputes(first,second,issues,last_issues)
            standard=standard+deps
            history=[*history,row]
            self.finish("Ours-think" if self.think else "Ours",second,open_issues,standard,history)
            if not self.think:
                for cfg in ("Ours-noA","Ours-noB"):
                    self.finish(cfg,second,open_issues,standard,history)
        except ArtifactMissing as exc:
            configs=["Ours-think"] if self.think else ["Ours","Ours-noA","Ours-noB","Ours-R1"]
            for cfg in configs:
                if not (case_path(task,rep)/"configs"/cfg/"result.json").exists():
                    extra=[f.parent for path in (self.case/"trace",self.case/"reviews") for f in path.rglob("calls.jsonl")]
                    self.result(cfg,None,[*standard,*extra],reason=str(exc),rounds=history)
        if self.think:
            return
        no_trace=[author]
        history=[]
        try:
            first,issues,row,deps=self.round(initial,1,False,"no_trace")
            no_trace+=deps
            history=[row]
            second,final_open,row,deps=self.round(first,2,False,"no_trace")
            history.append(row)
            no_trace+=deps
            self.finish("Ours-noTrace",second,remaining_disputes(first,second,issues,final_open),no_trace,history)
        except ArtifactMissing as exc:
            extra=[f.parent for path in (self.case/"no_trace",self.case/"reviews") for f in path.rglob("calls.jsonl")]
            self.result("Ours-noTrace",None,[*no_trace,*extra],reason=str(exc),rounds=history)


def baseline(cell):
    original=V3/"initial"/cell.task/f"rep{cell.rep}"/"checker.py"
    value=original.read_text()
    check_rows(value,cell.outputs,cell.vectors)
    local=case_path(cell.task,cell.rep)/"configs"/"Base"/"model.py"
    atomic(local,value)
    cell.result("Base",relative(local),[],v3_checker_sha256=hashlib.sha256(value.encode()).hexdigest())


def verisure(cell):
    root=cell.case/"veri_sure"
    where=root/"contract"
    prompt=(cell.context+"Write a compact JSON Veri-Sure B.1 contract with module_name (top_module), "
            "io list with name, dir, width, description, clocking {clock:{name,edge} or null, "
            "reset:{name,active,kind} or null}, timing {outputs:{name:{latency_cycles:nonnegative integer}}}, "
            "functional_summary {overview, rules}. Public interface must match (include the clock in io).")
    data=cell.generate_json(where,prompt,lambda c:vs_validate(c,cell.interface))
    model=None
    if data is not None:
        save(where/"contract.json",data)
        model=cell.model(root/"checker",cell.context+check_prompt()+"\nVeri-Sure contract:\n"+compact(data))
    return cell.result("VS",relative(root/"checker/model.py") if model else None,[where,root/"checker"])


def cot(cell,goal,pilot):
    folder=cell.case/(f"cot_pilot_{goal}" if pilot else f"cot_{goal}")
    prior=""
    budgets=[]
    total=0
    topics=("edge and mid-input timing", "reset and power-up behavior", "state and output transitions",
            "port widths and boundary values", "a short distinguishing input example",
            "one possible implementation mistake")
    for step in range(1,49):
        remaining=goal-total
        if remaining<max(1000,len(cell.context)//3+750):
            break
        path=folder/f"analysis{step:02d}"
        words=int(max(150,min(650,(remaining-len(cell.context)/2-950)/2)))
        topic=topics[(step-1)%len(topics)]
        prompt=(cell.context+f"Analyze {topic} in prose. Limit this pass to {words} words and at most "
                "one short worked example. Focus on a useful point for the final Python checker, then stop. "
                "Discuss the public spec only. Do not return a contract or Python in this pass.\n"+prior[-2100:])
        archived=ledger(path)
        # A prior stream may already have used the requested budget before the
        # process was interrupted. Include the recorded attempt in this control.
        if not archived or (path/"status.json").is_file():
            prose=new_artifact(path,prompt,False,lambda x:x.strip(),lambda x:None,attempts=1)
            archived=ledger(path)
        else:
            prose=None
        if not prose:
            prose=next((row["response"] for row in reversed(archived)
                        if row.get("response")),None)
        if prose:
            prior=prose
        budgets.append(path)
        total=token_use(budgets)["tokens"]
    path=folder/"checker"
    code=cell.model(path,cell.context+check_prompt()+"\nAs optional reasoning notes, consider:\n"+prior[-6100:])
    item=cell.result("CoT",relative(path/"model.py") if code else None,[*budgets,path],token_target=goal)
    if pilot:
        save(folder/"pilot_result.json",item)
    return item


def batch_precision(cell):
    pairs={}
    for rdir,edits in cell.diagnostics.items():
        for item in edits:
            pair={key:digest(item[key])[:18] for key in ("before","after")}
            pairs.setdefault(rdir,[]).append({"issue":item["issue_id"],**pair})
    snapshots={}
    for edits in cell.diagnostics.values():
        for item in edits:
            for key in ("before","after"):
                snapshots[digest(item[key])[:18]]=item[key]
    models={}
    keys=list(snapshots)
    directory=cell.case/"precision"
    for i in range(0,len(keys),4):
        batch=keys[i:i+4]
        path=directory/"batches"/digest(batch)[:18]
        previous=directory/f"batch{i//4+1:02d}"
        if (previous/"status.json").is_file():
            selected=load(previous/"status.json")["selected"]
            if selected and set(decode_json((previous/selected).read_text())["models"])==set(batch):
                path=previous
        prompt=(cell.context+"For diagnosis, return JSON {models:{id: Python source string}}. "
                "For every assigned item, implement its exact state semantics independently with the same interface. "
                "Each string must define reference(vectors) returning every width-valid output each cycle. "
                "Follow v3 Python restrictions with no imports, no I/O, and no executable top-level code.\n"+
                compact({key:snapshots[key] for key in batch}))
        def validate(data):
            if set(data["models"])!=set(batch) or not all(isinstance(v,str) for v in data["models"].values()):
                raise ValueError("Every snapshot ID needs one model")
        value=cell.generate_json(path,prompt,validate)
        for key in batch:
            candidate=value["models"].get(key) if value else None
            try:
                if not candidate:
                    raise ValueError("Batch did not produce this model")
                check_rows(candidate,cell.outputs,cell.vectors)
            except (RuntimeError,ValueError,TypeError,subprocess.TimeoutExpired):
                prompt,ids=cell.contract_model(snapshots[key])
                candidate=cell.model(directory/"individual"/key,prompt,attempts=2)
            if candidate:
                target=path/f"{key}.py"
                atomic(target,candidate)
                models[key]=relative(target)
    save(directory/"index.json",{"models":models,"accepted":pairs})


def job(task,rep,think):
    if STOP.is_set():
        return
    cell=Cell(task,rep,think)
    try:
        if think:
            base_future=INDEPENDENT.submit(make_base_think,task,rep)
        else:
            baseline(cell)
            verisure(cell)
        cell.process()
        if think:
            folder,model=base_future.result()
            cell.result("Base-think",relative(folder/"model.py") if model else None,[folder],
                        **({"reason":"v3 A0 checker format or transport retries exhausted"} if not model else {}))
        batch_precision(cell)
        print(task,rep,"thinking" if think else "standard","complete",flush=True)
    except llm.LLMError:
        STOP.set()
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("pilot","full"))
    parser.add_argument("--workers",type=int,default=32)
    args=parser.parse_args()
    ensure_frozen()
    if load(ROOT/"reports"/"thinking_preflight.json")["status"]!="accepted":
        raise SystemExit("Frozen-model thinking preflight is required")
    pilot=args.phase=="pilot"
    if not pilot and (not (ROOT/"reports"/"pilot_gate.json").exists()
                      or load(ROOT/"reports"/"pilot_gate.json")["status"]!="passed"):
        raise SystemExit("Validate trial outputs before the full experiment")
    names=protocol()["pilot_tasks"] if pilot else [r["task_id"] for r in tasks()]
    reps=range(1,2) if pilot else range(1,6)
    jobs=[(task,rep) for rep in reps for task in names]
    with ThreadPoolExecutor(max_workers=args.workers) as pool, ThreadPoolExecutor(max_workers=20) as controls:
        records={pool.submit(job,task,rep,think):(task,rep,think) for task,rep in jobs for think in (False,True)}
        off_pending=len(jobs)
        cot_futures=[]
        for future in as_completed(records):
            future.result()
            if not records[future][2]:
                off_pending-=1
                if not off_pending and not STOP.is_set():
                    costs=[load(case_path(task,rep)/"configs"/"Ours"/"result.json")["usage"]["tokens"]
                           for task,rep in jobs]
                    goal=round(sum(costs)/len(costs))
                    save(ROOT/"reports"/f"{args.phase}_budget.json",
                         {"target":goal,"total_ours_tokens":sum(costs),"cases":len(costs)})
                    cot_futures=[controls.submit(cot,Cell(task,rep,False),goal,pilot) for task,rep in jobs]
        if STOP.is_set():
            raise SystemExit("Model access failed")
        for future in cot_futures:
            future.result()
    expected=len(jobs)*len(CONFIGS)
    result_paths=[case_path(task,rep)/"configs"/cfg/"result.json" for task,rep in jobs for cfg in CONFIGS]
    if sum(path.is_file() for path in result_paths)!=expected:
        raise ValueError("Generated matrix incomplete")
    save(ROOT/"reports"/f"{args.phase}_generation.json",{"matrix":expected,"tasks":names,"reps":list(reps)})
    print(args.phase,expected,"configuration checkpoints",flush=True)


if __name__=="__main__":
    main()
