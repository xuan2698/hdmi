"""Archive the termination phases from the v1 local SBY work logs."""

import hashlib
import re
from collections import Counter
from pathlib import Path

from base import ROOT, V1, load, save


def historical_phase(root):
    path=root/"proof"/"logfile.txt"
    if not path.exists():
        return {"phase":"missing_log"}
    raw=path.read_bytes()
    lines=raw.decode(errors="replace").splitlines()
    assertions=[int(match[1]) for line in lines
                if (match:=re.search(r"Checking assertions in step (\d+)",line))]
    if assertions:
        stage="checking_assertions"
    else:
        stage="synthesis"
        for indicator,name in (("prep: starting","formal_prep"),("smt2: starting","smt_export"),
                               ("engine_0: starting","engine_launched")):
            if any(indicator in line for line in lines):
                stage=name
    return {"phase":stage,"last_checked_formal_step":max(assertions,default=None),
            "termination_note":next((line for line in lines if "Reached TIMEOUT" in line),None),
            "log_sha256":hashlib.sha256(raw).hexdigest()}


def main():
    source=V1/".work"/"formal"
    found=[]
    for p in sorted((V1/"guidance").glob("*/formal/*.json")):
        old=load(p)
        if old["status"]=="TIMEOUT":
            task,tag=old["task"],old["id"]
            found.append({"task":task,"G":tag,**historical_phase(source/task/tag)})
    assert len(found)==49
    if any(r["phase"]=="missing_log" for r in found):
        raise ValueError("v1 local SBY logs are required for archiving termination phases")
    counts=Counter(r["phase"] for r in found)
    save(ROOT/"audits"/"v1_formal_timeout_phases.json",{"counts":dict(counts),"timeouts":found})


if __name__=="__main__":
    main()
