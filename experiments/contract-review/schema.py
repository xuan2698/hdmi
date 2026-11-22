"""Deterministic validation of contracts, reviews, and per-issue edits."""

import copy
import re

from core import validate_input

ISSUE_TYPES=("coverage","grounding","consistency","ambiguity","spec_example")


def require(condition,message):
    if not condition:
        raise ValueError(message)


def text_is(value):
    return isinstance(value,str) and bool(value.strip())


def quoted(value,spec):
    return text_is(value) and " ".join(value.split()) in " ".join(spec.split())


def exact_int(value,width):
    return type(value) is int and 0<=value<1<<width


def verify_examples(example,ins,outs,must_include):
    sequence=example["vectors"]
    expected=example["expected"]
    require(isinstance(sequence,list) and 2<=len(sequence)<=4,"Rule example requires 2–4 cycles")
    validate_input(sequence,ins)
    require(isinstance(expected,list) and len(expected)==len(sequence),"Example lengths differ")
    for i,row in enumerate(expected):
        if len(must_include)==1 and type(row) is int:
            row={next(iter(must_include)):row}
            expected[i]=row
        require(isinstance(row,dict) and must_include<=row.keys()<=outs.keys(),"Output coverage differs in example")
        require(all(exact_int(v,outs[k]) for k,v in row.items()),"Example output outside width")


def contract_validate(data,spec,interface):
    ins,outs,clock,_=interface
    require(data["ports"]=={"inputs":ins,"outputs":outs,"clock":clock},"Public ports or widths changed")
    states=data["states"]
    require(isinstance(states,list),"states must be a list")
    for entry in states:
        require(all(text_is(entry[key]) for key in ("name","meaning","update_time")) and
                type(entry["update_during_reset"]) is bool,"Invalid implicit state")
    rules=data["rules"]
    require(isinstance(rules,list) and len(rules)>0,"At least one rule required")
    found=set()
    keys=set()
    unsupported=set()
    for row in rules:
        rule_id=row["id"]
        pins=row["outputs"]
        require(isinstance(rule_id,str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*",rule_id)
                and rule_id not in keys,"Invalid or duplicate rule ID")
        keys.add(rule_id)
        require(isinstance(pins,list) and bool(pins) and set(pins)<=outs.keys(),"Unknown rule outputs")
        found.update(pins)
        require(text_is(row["condition"]) and row["edge"] in ("posedge","negedge","combinational","asynchronous")
                and row["visible"] in ("same_cycle","next_cycle")
                and type(row["priority"]) is int and type(row["uncertain"]) is bool,
                "Invalid rule condition, timing, priority, or uncertain flag")
        if not quoted(row["spec_quote"],spec):
            unsupported.add(rule_id)
            require(row["uncertain"],f"{rule_id} missing verbatim spec quote, set uncertain")
        verify_examples(row["example"],ins,outs,set(pins))
    require(set(outs)==found,"Every output needs a rule")
    reset=data["reset"]
    require(reset["kind"] in ("none","sync","async","unspecified")
            and reset["active"] in ("high","low","none","unspecified")
            and text_is(reset["first_released_cycle"]) and isinstance(reset["values"],dict),
            "Invalid reset section")
    require(reset["name"] is None or reset["name"] in ins,"Reset must name a public input")
    require(all(key in outs and (v is None or exact_int(v,outs[key])) for key,v in reset["values"].items()),
            "Reset values must be width-valid or explicitly unspecified")
    require(text_is(data["mid"]),"Specify mid handling")
    uncertain=data["uncertain"]
    require(isinstance(uncertain,list),"uncertain must be a list")
    notes=set()
    for entry in uncertain:
        key=entry["rule_id"]
        require(key in keys|{"global"} and isinstance(entry["candidates"],list) and len(entry["candidates"])>=1
                and all(text_is(word) for word in entry["candidates"]),"Uncertain field needs candidate interpretations")
        notes.add(key)
    require({row["id"] for row in rules if row["uncertain"]}<=notes and unsupported<=notes,
            "Each uncertain rule needs an uncertain entry with candidates")


CONTRACT_INSTRUCTIONS = """Write a rigorous JSON behavior contract, not executable code. Use these keys:
ports {inputs:{name:width},outputs:{name:width},clock:name or null}.
states [{name,meaning,update_time,update_during_reset:boolean}].
rules [{id,outputs:[names],condition,edge:"posedge"|"negedge"|"combinational"|"asynchronous",
visible:"same_cycle"|"next_cycle",priority:integer,spec_quote,uncertain:boolean,
example:{vectors:[input rows],expected:[output rows]}}].
Every output must appear in some rule. Each rule has one example of 2–4 cycles. Vectors contain every
nonclock input with a width-valid unsigned integer and may contain "mid" with changed inputs.
Expected contains each rule output on EVERY row (all outputs are allowed). Use unsigned integers.
A spec_quote is a short verbatim substring of the supplied spec. If missing or ungrounded it MUST be
marked uncertain, and the uncertain list MUST have an entry for that rule. An interface or protocol timing
sentence is not design evidence. For a waveform-only task use a verbatim printed row or mark the inference uncertain.
reset {kind:"none"|"sync"|"async"|"unspecified",name:input or null,active:"high"|"low"|"none"|"unspecified",
values:{output:value or null},first_released_cycle:string}.
mid:string. uncertain [{rule_id,note,candidates:[distinct interpretation strings]}].
Use compact JSON; keep independent rules concise and do not invent specification text."""


def sentence_map(spec):
    blocks=[]
    for line in spec.splitlines():
        if not line.strip():
            continue
        pieces=re.split(r"(?<=[.!?])\s+(?=[A-Z])",line.strip())
        blocks.extend(part for part in pieces if part)
    return {f"S{n:02d}":part for n,part in enumerate(blocks,1)}


def review_validate(review,data,spec,interface):
    ids={row["id"] for row in data["rules"]}
    require(set(review["coverage"])==set(sentence_map(spec)),"Coverage must include every indexed spec segment")
    for value in review["coverage"].values():
        require(isinstance(value,list) and bool(value) and set(value)<=ids|{"unrelated","missing"},
                "Coverage values must be rule IDs, unrelated, or missing")
    require(isinstance(review["issues"],list),"issues must be a list")
    known=set()
    for item in review["issues"]:
        require(isinstance(item["issue_id"],str) and re.fullmatch(r"[A-Za-z0-9_-]+",item["issue_id"])
                and item["issue_id"] not in known,"Issue IDs must be unique and filename-safe")
        known.add(item["issue_id"])
        require(item["rule_id"] in ids|{"global"} and item["type"] in ISSUE_TYPES
                and item["severity"] in ("high","medium","low"),"Invalid issue key, type or severity")
        require(text_is(item["detail"]) and isinstance(item["spec_evidence"],str),"Issue detail or evidence missing")
        require(not item["spec_evidence"] or quoted(item["spec_evidence"],spec),"Review evidence must be verbatim")
        if item["type"]=="ambiguity":
            require(text_is(item["alternative"]),"Provide an alternative interpretation")
            validate_input(item["sequence"],interface[0])


REVIEW_INSTRUCTIONS = """Independently audit this contract against the indexed spec only.
Check (1) every spec segment mapped to a rule or marked unrelated/missing, (2) absent verbatim
evidence without uncertain, (3) contradictions between rule fields and examples, (4) plausible
alternative semantics with a concrete distinguishing chronological input sequence, and (5) derive
outputs for any explicit spec waveform/table/examples and compare. Report distinct material issues.
Return JSON {coverage:{Sxx:[rule IDs or "unrelated"/"missing"]},issues:[
{issue_id,rule_id (or "global"),type:"coverage"|"grounding"|"consistency"|"ambiguity"|"spec_example",
severity:"high"|"medium"|"low",detail,spec_evidence (verbatim spec or ""),alternative,sequence}]}.
For ambiguity the alternative must be specific; sequence must be a nonempty list of complete
width-valid nonclock input rows (optional mid) using the contract ports. For other types alternative
can be an empty string and sequence can be []. Code and prose outside JSON are not needed."""


def apply_edit(data,edit):
    path=edit["path"]
    value=edit["value"]
    require(isinstance(path,list) and bool(path),"Patch path required")
    if path[0]=="rules":
        require(len(path) in (2,3) and isinstance(path[1],str),"Rules patch must give its rule ID")
        index=next((i for i,rule in enumerate(data["rules"]) if rule["id"]==path[1]),None)
        if len(path)==3:
            require(index is not None and path[2] in {"condition","edge","visible","priority","spec_quote",
                                                       "uncertain","example","outputs"},"Invalid rule field edit")
            data["rules"][index][path[2]]=copy.deepcopy(value)
            return
        require(value is None and index is not None or isinstance(value,dict) and value.get("id")==path[1],
                "Rule patch ID mismatch")
        if value is None:
            data["rules"].pop(index)
        elif index is None:
            data["rules"].append(copy.deepcopy(value))
        else:
            data["rules"][index]=copy.deepcopy(value)
    elif path[0]=="states" and len(path)==3:
        require(path[2] in {"meaning","update_time","update_during_reset"},"Invalid implicit state field")
        state=next((item for item in data["states"] if item["name"]==path[1]),None)
        require(state is not None,"Unknown implicit state")
        state[path[2]]=copy.deepcopy(value)
    elif path[0]=="reset" and len(path)==2:
        require(path[1] in {"kind","name","active","values","first_released_cycle"},"Invalid reset field")
        data["reset"][path[1]]=copy.deepcopy(value)
    else:
        require(len(path)==1 and path[0] in {"states","reset","mid","uncertain"},"Illegal patch target")
        data[path[0]]=copy.deepcopy(value)


def revision_snapshots(old,revision,issues,spec,interface):
    responses=revision["responses"]
    expected=[item["issue_id"] for item in issues]
    require(isinstance(responses,list) and [r["issue_id"] for r in responses]==expected,
            "Respond to all retained issues in the provided order")
    current=copy.deepcopy(old)
    pairs=[]
    for response in responses:
        decision=response["decision"]
        edits=response.get("edits",[]) if decision=="rebut" else response["edits"]
        require(decision in ("accept","rebut") and text_is(response["reason"]) and isinstance(edits,list),
                "Invalid decision, reason or edits")
        if decision=="rebut":
            require(not edits and quoted(response["spec_quote"],spec),"Rebuttal needs a verbatim spec quote")
            continue
        before=copy.deepcopy(current)
        require(bool(edits),f"{response['issue_id']}: accepted issue must make edits")
        for edit in edits:
            apply_edit(current,edit)
        if before==current:
            original=copy.deepcopy(old)
            for edit in edits:
                apply_edit(original,edit)
            require(original!=old,f"{response['issue_id']}: accepted edits did not change the contract; rebut if no change is needed")
            response["already_applied_by_earlier_issue"]=True
            continue
        try:
            contract_validate(current,spec,interface)
        except (ValueError,KeyError,TypeError) as error:
            raise ValueError(f"{response['issue_id']}: {error}") from error
        pairs.append({"issue_id":response["issue_id"],"before":before,"after":copy.deepcopy(current)})
    return current,pairs


REVISION_INSTRUCTIONS = """Respond to EVERY supplied issue in order with compact JSON {responses:[
{issue_id,decision:"accept"|"rebut",reason,spec_quote,edits:[{path:[strings],value}]}]}.
For rebut, use an exact spec quotation and no edits. Use rebut when the contract already has the
proposed value or its existing example already expresses the rule. Compare against Current contract
before writing an edit. An accept must actually change a field. Prefer a small edit such as
["rules","rule_ID","condition"], ["states","state_name","meaning"], or ["reset","first_released_cycle"].
Whole fields may also be replaced as ["rules","rule_ID"], ["states"], ["reset"], ["mid"], ["uncertain"].
A whole rule may add or delete by id (delete with null). Preserve the current schema, including reset
kind none, sync, async or unspecified, reset name a public input or null, and exact same_cycle /
next_cycle strings. Put initial-value clarification without a physical reset in state meaning or an
explicit uncertain field rather than making up a reset kind. EVERY rule example remains 2–4 cycles.
Include all issue responses in order, including those unchanged from any previous attempt. No port changes."""


def vs_validate(contract,interface):
    ins,outs,clock,_=interface
    require(text_is(contract["module_name"]),"module_name required")
    io={item["name"]:(item["dir"],item["width"]) for item in contract["io"]}
    pins={n:("input",w) for n,w in ins.items()}|{n:("output",w) for n,w in outs.items()}
    if clock:
        pins[clock]=("input",1)
    require(io==pins,"VS contract io must match the public interface")
    require(isinstance(contract["clocking"],dict) and "clock" in contract["clocking"] and
            "reset" in contract["clocking"],"VS clocking requires clock and reset keys")
    outputs=contract["timing"]["outputs"]
    require(set(outputs)==set(outs) and all(type(outputs[n]["latency_cycles"]) is int and
                                           outputs[n]["latency_cycles"]>=0 for n in outs),"Invalid per-output VS latency")
    require(isinstance(contract["functional_summary"],dict),"functional_summary must be an object")
