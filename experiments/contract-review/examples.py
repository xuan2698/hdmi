"""Extract only examples with explicit values from frozen v3 public specs."""

import re
from collections import deque

from core import ROOT, ensure_frozen, public, save, tasks


def source_lines(spec):
    return [(i,re.sub(r"^\s*//\s?","",line).strip()) for i,line in enumerate(spec.splitlines(),1)]


def waveform(lines, ins, outs, clock, edge):
    if not clock:
        return []
    header=next(((i,line.split()) for i,line in lines if line.split()[:1]==["time"]),None)
    if not header:
        return []
    keys=header[1][1:]
    rows=[]
    for i,line in lines:
        words=line.split()
        if i<=header[0] or not words or not re.match(r"^\d+(?:\.\d+)?\s*(?:ns|ps|us)$",words[0]):
            continue
        if len(words)==len(keys)+1:
            rows.append((i,dict(zip(keys,words[1:],strict=True))))
    phase=1 if edge=="posedge" else 0
    examples=[]
    vectors=[]
    expected=[]
    unsafe=False
    prior=None
    for line,now in rows:
        if prior and prior.get(clock)==str(1-phase) and now.get(clock)==str(phase):
            saved={name:prior.get(name) for name in ins}
            known=all(value is not None and value.isdecimal() and 0<=int(value)<1<<ins[name]
                      for name,value in saved.items())
            unsafe|=not known
            if known:
                record={name:int(value) for name,value in saved.items()}
                mid={name:int(now[name]) for name in ins
                     if now.get(name,"").isdecimal() and now[name]!=saved[name]}
                if mid:
                    record["mid"]=mid
                vectors.append(record)
                expected.append({name:int(now[name]) for name in outs if now.get(name,"").isdecimal()
                                 and int(now[name])<1<<outs[name]})
        prior=now
    if rows:
        examples.append({"type":"waveform","line":header[0],"source_rows":len(rows),
                         "length":len(vectors),"vectors":vectors if not unsafe else [],
                         "expected":expected if not unsafe else [],
                         "reason":"unknown input prefix" if unsafe else
                                  "drive prior sample, current timestamp changes use mid"})
    return examples


def tables(lines, spec, ins, outs):
    if not any("|" in s for _,s in lines):
        return []
    raw=[(i,[cell.strip() for cell in line.split("|")]) for i,line in lines if "|" in line]
    header=raw[0]
    rows=raw[1:]
    if set(ins)=={"x","y"} and set(outs)=={"Y0","z"} and "Y[2:0]" in header[1][1]:
        result=[]
        for i,cells in rows:
            if len(cells)!=3 or not re.fullmatch(r"[01]{3}",cells[0]):
                continue
            targets=[part.strip() for part in cells[1].split(",")]
            if len(targets)!=2 or any(not re.fullmatch(r"[01]{3}",v) for v in targets) or cells[2] not in ("0","1"):
                continue
            for x,value in enumerate(targets):
                result.append({"type":"state_assigned_table","line":i,"source_rows":1,"length":1,
                               "vectors":[{"x":x,"y":int(cells[0],2)}],
                               "expected":[{"Y0":int(value[-1]),"z":int(cells[2])}]})
        return result
    reset_match=re.search(r"active high reset that resets the FSM to state ([A-Z])",spec)
    if reset_match and "reset" in ins and len(ins)==2 and len(outs)==1:
        data_pin=next(n for n in ins if n!="reset")
        output=next(iter(outs))
        transitions={}
        for i,cells in rows:
            if len(cells)==3 and re.fullmatch(r"[A-Z]",cells[0]) and cells[2] in ("0","1"):
                dest=tuple(x.strip() for x in cells[1].split(","))
                if len(dest)==2:
                    transitions[cells[0]]=(i,dest,int(cells[2]))
        start=reset_match[1]
        if start in transitions and all(d in transitions for _,ds,_ in transitions.values() for d in ds):
            routes={start:[]}
            queue=deque([start])
            while queue:
                state=queue.popleft()
                for bit,dest in enumerate(transitions[state][1]):
                    if dest not in routes:
                        routes[dest]=routes[state]+[bit]
                        queue.append(dest)
            found=[]
            for state,route in routes.items():
                for bit in (0,1):
                    current=start
                    data=[{"reset":1,data_pin:0}]
                    want=[{output:transitions[start][2]}]
                    for value in route+[bit]:
                        current=transitions[current][1][value]
                        data.append({"reset":0,data_pin:value})
                        want.append({output:transitions[current][2]})
                    found.append({"type":"reset_reachable_moore_table","line":transitions[state][0],
                                  "source_rows":len(rows),"length":len(data),"vectors":data,"expected":want})
            return found
    return [{"type":"symbolic_table","line":header[0],"source_rows":len(rows),"length":len(rows),
             "vectors":[],"expected":[],"reason":"no unambiguous external encoding"}]


def prose_candidates(lines):
    return [{"type":"prose_sequence","line":i,"source_rows":1,"length":0,"vectors":[],"expected":[],
             "reason":"partial or narrative input/output sequence"}
            for i,line in lines if re.search(r"(?:timing diagram|for example|example[: ]|cycle \d+.*cycle \d+)",line,re.I)]


def extract(task):
    problem,interface=public(task)
    spec=problem["spec"]
    lines=source_lines(spec)
    ins,outs,clock,edge=interface
    explicit=waveform(lines,ins,outs,clock,edge)+tables(lines,spec,ins,outs)
    return explicit or prose_candidates(lines)


def main():
    ensure_frozen()
    examples={item["task_id"]:extract(item["task_id"]) for item in tasks()}
    save(ROOT/"examples.json",examples)
    print({task:(len(cases),sum(bool(c["vectors"]) for c in cases)) for task,cases in examples.items()})


if __name__=="__main__":
    main()
