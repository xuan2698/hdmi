"""Generate the frozen spec-only proxy cohort under Amendment 1."""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
AUTO = REPO / "experiments" / "autobench-pilot"
AMENDMENT = "de8bd6eab3cf54339da71f563d20ead732153d5e"
GEN = ROOT / "generation"
sys.path.insert(0, str(AUTO))
import llm
from pilot2_generate import atomic, load, save, settings

STOP = threading.Event()
CODE = re.compile(r"```(?:systemverilog|sv|verilog|v)?[ \t]*\n(.*?)```", re.I | re.S)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def development():
    return load(REPO / "stimulus-v1/split.json")["development"]


def export_specs(dataset):
    ids = development()
    table = pq.read_table(dataset, columns=["id", "spec_files", "instruction"],
                          filters=[("id", "in", ids)])
    rows = {}
    for row in table.to_pylist():
        specs = row["spec_files"]
        if not specs:
            prose = re.sub(r"```[^\n]*\n.*?```", "", row["instruction"], flags=re.S).strip()
            specs = [{"name":"instruction.prose", "content":prose}]
        if not all(part["content"].strip() for part in specs):
            raise ValueError(f"Missing published specification: {row['id']}")
        rows[row["id"]] = specs
    if set(rows) != set(ids):
        raise ValueError("Expected the frozen ten development task IDs")
    for task in ids:
        dest = GEN / task / "spec.json"
        data = json.dumps(rows[task], ensure_ascii=False, indent=2) + "\n"
        if dest.exists() and dest.read_text() != data:
            raise ValueError(f"Frozen spec changed: {task}")
        atomic(dest, data)


def make_prompt(specs, slot):
    return (f"Implement the hardware design defined by the supplied specification in synthesizable "
            f"SystemVerilog or Verilog. This is independent implementation sample {slot}.\n"
            "Preserve the exact module name, pin names and directions, reset and clock semantics, and "
            "configurable parameters from the spec. Return only the complete source for the design "
            "and any required synthesizable submodules. Do not include a testbench, comments about "
            "the process, assertions, file I/O, external includes, or placeholders. If the task prose asks "
            "for a testbench, use it only as the specification for the DUT it describes.\n\n"
            + "\n\n".join(part["content"] for part in specs))


def api_call(log, prompt):
    key = os.environ.get("OPENCODE_GO_API_KEY", "").strip()
    if not key:
        raise llm.LLMError("OPENCODE_GO_API_KEY is missing")
    llm.api_key = lambda: os.environ.get("OPENCODE_GO_API_KEY", "").strip()
    plan = settings()
    expected = load(REPO / "stimulus-v2/protocol.json")["model"]
    if plan["model"] != expected:
        raise ValueError("Locked inference model changed")
    overrides = [(llm.LOG_PATH, llm.LOG_PATH.set(log)),
                 (llm.THINKING, llm.THINKING.set(plan["thinking"])),
                 (llm.TRANSPORT, llm.TRANSPORT.set({**plan["transport"], "stream":plan["stream"]}))]
    try:
        result = llm.call_llm(expected, prompt, plan["temperature"], plan["max_tokens"])
    finally:
        for context, token in reversed(overrides):
            context.reset(token)
    if result["model_actual"] != expected:
        raise llm.LLMError("Provider returned a different model")
    if not result["complete"]:
        raise llm.LLMError("Model response ended without a complete source")
    generated = result["response"]
    if key in generated:
        raise llm.LLMError("Credential redacted from returned content")
    return generated


def proxy(job):
    task, slot = job
    work = GEN / task / f"P{slot:02d}"
    status = work / "status.json"
    if status.exists():
        return load(status)
    if STOP.is_set():
        return None
    work.mkdir(parents=True, exist_ok=True)
    source = work / "proxy.sv"
    if not source.exists():
        try:
            response = api_call(work / "calls.jsonl", make_prompt(load(work.parent / "spec.json"), slot))
        except llm.LLMError as exc:
            STOP.set()
            row = {"task":task,"proxy":work.name,"status":"api_failed","source":"","sha256":"",
                   "reason":str(exc)}
            save(status,row)
            return row
        matched = CODE.search(response)
        atomic(source, (matched[1] if matched else response).strip() + "\n")
    row = {"task":task,"proxy":work.name,"status":"received","source":str(source.relative_to(ROOT)),
           "sha256":sha(source.read_bytes()),"reason":""}
    save(status,row)
    print(task,work.name,row["sha256"],flush=True)
    return row


def manifest(jobs):
    rows = []
    for task, idx in jobs:
        name=f"P{idx:02d}"
        status=GEN/task/name/"status.json"
        row=load(status) if status.exists() else {"task":task,"proxy":name,"status":"unattempted",
                                                   "source":"","sha256":"","reason":""}
        if row["status"]=="received" and sha((ROOT/row["source"]).read_bytes())!=row["sha256"]:
            raise ValueError(f"Proxy content changed: {task} {name}")
        rows.append(row)
    with (GEN/"proxy_inventory.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset",type=Path)
    p.add_argument("--workers",type=int,default=8)
    args=p.parse_args()
    remote=subprocess.check_output(["git","ls-remote","--heads","origin","refs/heads/pilot-formal-cex"],
                                   cwd=REPO,text=True).split()
    if not remote or subprocess.run(["git","merge-base","--is-ancestor",AMENDMENT,remote[0]],cwd=REPO).returncode:
        raise SystemExit("The Amendment 1 commit must be pushed before any model call")
    if not os.environ.get("OPENCODE_GO_API_KEY","").strip():
        raise SystemExit("OPENCODE_GO_API_KEY is missing")
    export_specs(args.dataset)
    jobs=[(task,idx) for idx in range(1,11) for task in development()]
    first=proxy(jobs[0])
    if first and first["status"]=="received":
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(proxy,jobs[1:]))
    rows=manifest(jobs)
    complete=sum(r["status"]=="received" for r in rows)
    print(f"Proxy inventory: {complete}/{len(rows)} complete",flush=True)
    if complete != len(rows):
        raise SystemExit("Proxy cohort incomplete. Inspect the frozen slot statuses before continuing.")


if __name__=="__main__":
    main()
