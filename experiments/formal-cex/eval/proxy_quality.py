"""Evaluate frozen proxies on archived reference-output replays, in the eval area."""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

from stage0 import ERRORS, interface, inventory
from common import get_vectors, public
import hdl

EVAL_WORK = ROOT / "eval" / "results"
hdl.WORK = EVAL_WORK / "compiled"


def available_official_tbs(folder, tasks):
    assets = {}
    for path in sorted(folder.glob("cvdp_*generation_*.jsonl")):
        for line in path.open(encoding="utf-8"):
            found = re.search(r'"id"\s*:\s*"([^"]+)"', line[:300])
            if not found or found[1] not in tasks or found[1] in assets:
                continue
            obj = json.loads(line)
            if "output" in obj:
                files = obj["output"].get("context", {})
            else:
                files = obj.get("patch", {})
            paths = [name for name in files if name.endswith((".v", ".sv"))]
            assets[found[1]] = {
                "reference_paths":paths,
                "present_sources":sum(isinstance(files[name],str) and bool(files[name].strip()) for name in paths)
            }
    return assets


def materialize(row, seed, cycles):
    archive = REPO / "stimulus-v2" / "trial" / row["id"] / str(seed) / "initial"
    vectors = get_vectors(archive,row,seed,cycles)
    stage = EVAL_WORK / "proxy_quality" / row["id"] / str(seed)
    return hdl.input_dir(stage,vectors,row["ports"])


def evaluate_one(reference, entry, directories, cycles, official):
    task, tag = entry["task"],entry["proxy"]
    output = {"task":task,"proxy":tag,"official_TB_verdict":"unavailable" if not official else "unverified",
              "differential_verdict":"not_run","first_seed":"","first_cycle":"","reason":""}
    if entry["status"]!="received":
        output.update(differential_verdict="unavailable",reason=entry["status"])
        return output
    ports=reference["ports"]
    source=(ROOT/entry["source"]).read_text()
    try:
        proxy=interface(source,ports["parameters"],task)
        for key in ("top","clock","input","output"):
            if proxy[key]!=ports[key]:
                raise ValueError(f"reference and proxy disagree on {key}")
    except ERRORS as exc:
        output.update(differential_verdict="interface_failure",reason=str(exc).splitlines()[0][-240:])
        return output
    try:
        # compile_sim uses a shared parameter map. A proxy with a declared,
        # static 16-bit interface is already bound at the selected IIR width.
        ref=reference["gold"]
        p=dict(ports)
        if proxy["parameters"]!=ports["parameters"]:
            p["parameters"]=proxy["parameters"]
        binary=hdl.compile_sim(ref,source,p)
        for seed,folder in directories:
            found=hdl.observe(binary,folder,cycles)
            if found["samples"]:
                output.update(differential_verdict="output_mismatch",first_seed=seed,first_cycle=found["first"])
                return output
    except ERRORS as exc:
        output.update(differential_verdict="simulation_failure",reason=str(exc).splitlines()[0][-240:])
    else:
        output["differential_verdict"]="pass"
    return output


def csv_out(name, rows):
    with (ROOT/"reports"/name).open("w",encoding="utf-8",newline="") as stream:
        out=csv.DictWriter(stream,list(rows[0]),lineterminator="\n")
        out.writeheader()
        out.writerows(rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset",type=Path)
    p.add_argument("upstream_dir",type=Path)
    args=p.parse_args()
    bank=inventory()
    rows={r["id"]:r for r in public(args.dataset)}
    setup=json.loads((REPO/"stimulus-v2/protocol.json").read_text())
    seeds=setup["seeds"][:5]
    cycles=setup["max_cycles"]
    assets=available_official_tbs(args.upstream_dir,rows)
    if set(assets)!=set(rows):
        raise ValueError("Upstream benchmark metadata missing for development tasks")
    comparisons={task:[(seed,materialize(row,seed,cycles)) for seed in seeds] for task,row in rows.items()}
    def submit(entry):
        task=entry["task"]
        return evaluate_one(rows[task],entry,comparisons[task],cycles,assets[task]["present_sources"])
    with ThreadPoolExecutor(max_workers=6) as pool:
        by_proxy=list(pool.map(submit,bank))
    stats=[]
    for task in rows:
        group=[x for x in by_proxy if x["task"]==task]
        values=Counter(x["differential_verdict"] for x in group)
        scored=values["pass"]+values["output_mismatch"]
        stats.append({"task":task,"slots":len(group),"official_gold_tb_available":assets[task]["present_sources"],
                      "proxy_diff_pass":values["pass"],"proxy_diff_scored":scored,
                      "proxy_diff_all_slot_rate":values["pass"]/len(group),
                      "proxy_diff_scored_rate":values["pass"]/scored if scored else "",
                      "output_mismatch":values["output_mismatch"],"interface_failure":values["interface_failure"],
                      "simulation_failure":values["simulation_failure"]})
    csv_out("proxy_eval.csv",by_proxy)
    csv_out("proxy_eval_by_task.csv",stats)
    print("Proxy differential archive written",len(by_proxy),flush=True)


if __name__=="__main__":
    main()
