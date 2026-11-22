"""Public-only inputs, frozen API settings, and the v3 Python sandbox."""

import contextvars
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
AUTO = ROOT.parent / "autobench-pilot"
V3 = AUTO / "v3"
RUNS = ROOT / "runs"
FROZEN = "841955391e5e8383c64c9726a0a636ed1ae51b81"
sys.path.insert(0, str(AUTO))

import llm
from pilot2_generate import atomic, load, save
from pilot3_inputs import public, setup, tasks
from pilot3_generate import check_rows
from simulate import RunError, validate_rows

llm.api_key = lambda: os.environ.get("OPENCODE_GO_API_KEY", "").strip()
_legacy_stream = llm.read_stream
_reasoning_bytes = contextvars.ContextVar("reasoning_bytes", default=0)
API_SLOTS = threading.BoundedSemaphore(36)


def read_stream(response):
    def observe():
        for line in response:
            if line.startswith(b"data:") and line[5:].strip() != b"[DONE]":
                try:
                    event=json.loads(line[5:])
                    for choice in event.get("choices", []):
                        delta=choice.get("delta", {})
                        value=delta.get("reasoning_content") or delta.get("reasoning") or ""
                        if isinstance(value,str):
                            _reasoning_bytes.set(_reasoning_bytes.get()+len(value.encode()))
                except (ValueError,AttributeError):
                    pass
            yield line
    return _legacy_stream(observe())


llm.read_stream = read_stream


def protocol():
    return load(ROOT / "protocol.json")


def ensure_frozen():
    for name in ("protocol.json","PREREG.md"):
        recorded=subprocess.check_output(["git","show",f"{FROZEN}:experiments/contract-review/{name}"],cwd=REPO)
        if recorded!=(ROOT/name).read_bytes():
            raise ValueError(f"Frozen experiment file changed: {name}")


def seed_for(rep):
    return setup()["repeat_seeds"][rep-1]


def input_file(task,rep):
    return V3/"initial"/task/f"rep{rep}"/"vectors.json"


def vectors(task,rep):
    return load(input_file(task,rep))


def case_path(task,rep):
    return RUNS/task/f"rep{rep}"


def case_inputs(task, rep):
    spec, interface=public(task)
    return context(spec["spec"],interface,seed_for(rep))


def context(spec,interface,seed):
    inputs,outputs,clock,edge=interface
    return (f"Public specification:\n{spec}\n\nInput widths {inputs}; output widths {outputs}. "
            f"Clock {clock}; sample after the {edge} edge has settled. Each row's values are driven before "
            "the sampled edge. Optional mid input changes occur AFTER sampling, before the other edge, and "
            f"are carried to the start of the next row. Protocol seed {seed}.\n")


def check_prompt():
    return ("Return only executable Python with function reference(vectors). For each row return a dictionary "
            "with every output and a concrete unsigned integer within that output's bit width, even when power-up "
            "is unspecified. Preserve timing and process mid changes at the correct point. No imports, classes, "
            "prints, external files or executable code outside functions. Comments may label the contract rules.")


def decode_json(response):
    response=strip_thought(response)
    fence=re.search(r"```(?:json)?\s*\n(.*?)```",response,re.S|re.I)
    if fence:
        response=fence[1]
    try:
        value=json.loads(response)
    except ValueError:
        match=re.search(r"[{\[]",response)
        if not match:
            raise ValueError("Expected a JSON object") from None
        value,_=json.JSONDecoder().raw_decode(response[match.start():])
    if not isinstance(value,dict):
        raise ValueError("Expected a JSON object")
    return value


def strip_thought(value):
    return re.sub(r"<think>.*?</think>","",value,flags=re.S|re.I).strip()


def decode_python(response):
    response=strip_thought(response)
    fence=re.search(r"```(?:python|py)?\s*\n(.*?)```",response,re.S|re.I)
    return (fence[1] if fence else response).strip()+"\n"


def call(folder,prompt,think):
    plan=setup()
    if plan["model"]!="deepseek-v4.1-flash" or not llm.api_key():
        raise llm.LLMError("Expected frozen DeepSeek and environment OPENCODE_GO_API_KEY")
    folder.mkdir(parents=True,exist_ok=True)
    for bad in ("/eval/","official_mutants/","golden_rtl.v","golden_tb.v"):
        if bad in prompt:
            raise ValueError("A generation prompt contains an evaluation path")
    overridden=[(llm.LOG_PATH,llm.LOG_PATH.set(folder/"calls.jsonl")),
                (llm.THINKING,llm.THINKING.set("enabled" if think else plan["thinking"])),
                (llm.TRANSPORT,llm.TRANSPORT.set({**plan["transport"],"stream":plan["stream"]})),
                (_reasoning_bytes,_reasoning_bytes.set(0))]
    try:
        with API_SLOTS:
            result=llm.call_llm(plan["model"],prompt,plan["temperature"],plan["max_tokens"])
        reasoning=_reasoning_bytes.get()
    finally:
        for var,token in reversed(overridden):
            var.reset(token)
    log=ledger(folder)
    status={"actual_model":result["model_actual"],"requested_thinking":think,"reasoning_bytes":reasoning,
            "finish_reason":result["finish_reason"],"session":log[-1]["session"]}
    if result["model_actual"]!=plan["model"]:
        raise llm.LLMError("Unexpected API model ID")
    if not result["complete"]:
        raise RunError(f"Incomplete API output: {result['finish_reason']}")
    if llm.api_key() in result["response"]:
        raise llm.LLMError("Credential detected and redacted in the API response")
    return result["response"],status


def ledger(folder):
    log=folder/"calls.jsonl"
    return [json.loads(l) for l in log.read_text().splitlines()] if log.is_file() else []


def compact(value):
    return json.dumps(value,ensure_ascii=False,separators=(",",":"))


def digest(value):
    return hashlib.sha256(compact(value).encode()).hexdigest()


def token_use(folders):
    rows={row["session"]+":"+str(row["attempt"]):row for folder in set(folders) for row in ledger(folder)}
    return {"calls":len({r["session"] for r in rows.values()}),"attempts":len(rows),
            "tokens":sum(r.get("usage",{}).get("total_tokens",0) for r in rows.values()),
            "go_usd":sum(r.get("allowance") or 0 for r in rows.values()),
            "charged_usd":sum(r.get("charged_usd") or 0 for r in rows.values())}


def new_artifact(folder,prompt,think,decode,validator,attempts=3,repair_draft=False,compact_after_truncation=False):
    """Checkpoint complete raw responses and only reuse artifacts after validation."""
    state=folder/"status.json"
    if state.is_file():
        record=load(state)
        if record["selected"] is None:
            return None
        return decode((folder/record["selected"]).read_text())
    errors=[]
    metadata=[]
    draft=""
    folder.mkdir(parents=True,exist_ok=True)
    for i in range(1,attempts+1):
        target=folder/f"response{i:02d}.txt"
        previous=prompt
        if errors:
            previous+="\nFix the following format or execution issue and return the requested complete artifact:\n"+errors[-1]
            if compact_after_truncation and "Incomplete API output: length" in errors[-1]:
                previous+=("\nKeep any deliberation brief. Produce a compact complete final artifact with all "
                           "required fields before the response limit.")
            if repair_draft and draft:
                previous+="\nYour previous attempt (for format repair only):\n"+draft[:14000]
        try:
            if not target.exists():
                raw,meta=call(folder,previous,think)
                atomic(target,raw)
                save(target.with_suffix(".meta.json"),meta)
            meta_path=target.with_suffix(".meta.json")
            if meta_path.is_file():
                metadata.append(load(meta_path))
            draft=target.read_text()
            value=decode(draft)
            validator(value)
        except llm.LLMError as exc:
            receipts=ledger(folder)
            last=receipts[-1] if receipts else {}
            status=last.get("http_status")
            if (last.get("status")=="received" or not receipts or
                (status is not None and 400<=status<500 and status not in (408,429))):
                raise
            errors.append(str(exc)[:500])
        except (ValueError,TypeError,KeyError,AttributeError,IndexError,RunError,subprocess.TimeoutExpired) as exc:
            errors.append(str(exc)[:500])
        else:
            save(state,{"selected":target.name,"errors":errors,"requests":metadata})
            return value
    save(state,{"selected":None,"errors":errors,"requests":metadata})
    return None


def validate_input(sequence,ins):
    if not isinstance(sequence,list) or not sequence:
        raise ValueError("Input sequence must be a nonempty list")
    plain=[{k:v for k,v in row.items() if k!="mid"} for row in sequence]
    validate_rows(plain,ins,len(sequence))
    for row in sequence:
        if "mid" in row:
            values=row["mid"]
            if not isinstance(values,dict) or not values.keys() <= ins.keys():
                raise ValueError("Mid keys must be input ports")
            validate_rows([values],{k:ins[k] for k in values},1)
