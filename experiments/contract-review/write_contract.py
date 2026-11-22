"""Generate and validate the initial contract for each frozen experiment cell."""

import argparse
from concurrent.futures import ThreadPoolExecutor

from core import (case_inputs, case_path, decode_json, ensure_frozen, new_artifact, protocol, public, save, tasks)
from schema import CONTRACT_INSTRUCTIONS, contract_validate


def write(task,rep,think):
    folder=case_path(task,rep)/("on" if think else "off")/"author"
    spec,interface=public(task)
    value=new_artifact(folder,case_inputs(task,rep)+CONTRACT_INSTRUCTIONS,think,decode_json,
                       lambda data:contract_validate(data,spec["spec"],interface),repair_draft=True)
    if value is not None:
        contract_validate(value,spec["spec"],interface)
        save(folder/"contract.json",value)
    return folder,value


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot",action="store_true")
    p.add_argument("--workers",type=int,default=12)
    args=p.parse_args()
    ensure_frozen()
    selected=protocol()["pilot_tasks"] if args.pilot else [t["task_id"] for t in tasks()]
    jobs=[(task,rep,think) for task in selected for rep in (range(1,2) if args.pilot else range(1,6))
          for think in (False,True)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for folder,value in pool.map(lambda q:write(*q),jobs):
            print(folder.name,str(folder.parent.parent),bool(value),flush=True)
