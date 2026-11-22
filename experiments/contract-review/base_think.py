"""Use the exact archived v3 A0 checker prompt with thinking enabled."""

import argparse

from core import (ROOT, V3, case_path, check_rows, decode_python, ensure_frozen,
                  ledger, load, new_artifact, public, save, vectors, llm, atomic)


def run(task,rep):
    _,interface=public(task)
    origin=V3/"initial"/task/f"rep{rep}"
    prompt=next(record["prompt"] for record in ledger(origin)
                if "Define reference(vectors)" in record["prompt"] or
                   "Implement reference(vectors)" in record["prompt"])
    folder=case_path(task,rep)/"on"/"base_think"
    code=new_artifact(folder,prompt,True,decode_python,
                      lambda value:check_rows(value,interface[1],vectors(task,rep)))
    if code is not None:
        atomic(folder/"model.py",code)
    return folder,code


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("task")
    p.add_argument("rep",type=int)
    args=p.parse_args()
    ensure_frozen()
    if not (ROOT/"examples.json").exists():
        raise SystemExit("Extract frozen spec examples first")
    output=ROOT/"reports"/"thinking_preflight.json"
    try:
        folder,code=run(args.task,args.rep)
    except llm.LLMError as error:
        folder=case_path(args.task,args.rep)/"on"/"base_think"
        records=ledger(folder)
        save(output,{"status":"rejected_or_unavailable","error":str(error),"last_http_status":
                     records[-1].get("http_status") if records else None})
        raise SystemExit(str(error)) from None
    info=load(folder/"status.json")
    proof=sum(r["reasoning_bytes"] for r in info["requests"])
    save(output,{"status":"accepted","task":args.task,"rep":args.rep,"native_reasoning_bytes":proof,
                 "checker_validated":code is not None,"requests":info["requests"]})
    print("DeepSeek thinking accepted",proof,"reasoning bytes, checker",bool(code),flush=True)


if __name__=="__main__":
    main()
