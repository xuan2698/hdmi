"""Assemble the archived equivalence subjects without modifying the pilot data."""

import hashlib
from pathlib import Path

from rare_mutants import BASE, REPO, CVDP, selected
from designs import interface, design_code, load, save
from pilot2_sim import interface_from

AUTO = REPO / "experiments" / "autobench-pilot"
CVDP_SPECIAL_BOUNDS = {"cvdp_copilot_digital_stopwatch_0017": 180_000_000_000}
CYCLES = 52


def identity(gold, mutant):
    return hashlib.sha256((gold + "\x00" + mutant).encode()).hexdigest()


def auto_ports(task):
    data = load(AUTO / "v2" / "generation" / task / "problem.json")
    ins, out, clk, edge = interface_from(data)
    resets = {n: (0 if n.lower().endswith(("_n", "resetn", "rstn")) else 1)
              for n in ins if "reset" in n.lower() or n.lower() == "rst"}
    if task == "m2014_q4c":
        resets["r"] = 1
    return {"input": ins, "output": out, "clock": clk, "resets": resets, "top": "top_module",
            "active_edge": edge}


def sources(dataset, cohort):
    cases = {}
    if cohort == "old":
        for version, key in (("v2", "mutants"), ("v3", "cases")):
            for p in sorted((AUTO / version / "eval").glob("*/prescreen.json")):
                row = load(p)
                task = row["task"]
                for item in row[key]:
                    if item["status"] != "suspected_equivalent":
                        continue
                    folder = AUTO / "v2" / "eval" / task
                    gold = (folder / "golden_rtl.v").read_text()
                    mutant = (folder / "official_mutants" / (item["id"] + ".v")).read_text()
                    tag = "H" + item["id"]
                    case = cases.setdefault((task, identity(gold, mutant)),
                                            make(task, tag, gold, mutant, auto_ports(task)))
                    case["sources"].append(f"autobench_{version}/{tag}")
    for row in selected(dataset):
        task = row["id"]
        if cohort == "old":
            record = load(CVDP / "eval" / "results" / f"{task}.json")
            entries = {tag: item for tag, item in record["H"].items() if item["status"] == "suspected_equivalent"}
            folder = CVDP / "eval" / "heldout" / task
        else:
            folder = BASE / "eval" / "new" / task
            entries = {tag: load(folder / tag / "mutation.json")
                       for tag in load(folder / "status.json")["candidates"]}
        gold = design_code(row)
        for tag, item in entries.items():
            mutant = (folder / tag / "rtl.sv").read_text()
            case = cases.setdefault((task, identity(gold, mutant)),
                                    make(task, tag, gold, mutant, interface(row)))
            case["metadata"] = {k: item[k] for k in ("bug", "trigger", "effect", "model") if k in item}
            case["sources"].append(f"cvdp_{cohort}/{tag}")
    return sorted(cases.values(), key=lambda case: (case["task"], case["tag"]))


def make(task, tag, golden, mutant, ports):
    return {"task": task, "tag": tag, "original": golden, "mutant": mutant, "ports": ports,
            "sources": [], "metadata": {}, "rtl_pair_sha256": identity(golden, mutant),
            "required_cycles": CVDP_SPECIAL_BOUNDS.get(task, CYCLES)}
