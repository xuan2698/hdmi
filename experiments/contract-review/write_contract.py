"""Generate and validate the initial contract for each frozen experiment cell."""

from core import case_inputs, case_path, decode_json, new_artifact, public, save
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
