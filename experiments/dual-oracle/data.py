"""Load only frozen public specifications, vectors, and previous generated checkers."""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
AUTO = ROOT.parent / "autobench-pilot"
V3 = AUTO / "v3"
CVDP = REPO / "cvdp-headroom"
V2 = REPO / "stimulus-v2"
sys.path.insert(0, str(AUTO))

from pilot2_generate import atomic, load, save
from pilot3_generate import driver_rows
from pilot3_inputs import public, setup, tasks
from simulate import validate_rows
from sandbox import check_rows

PREREG = "bd908835da383229dace363008f2ba74aa2192c4"
PLAN = load(ROOT / "protocol.json")


def archived(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)


def verify_protocol():
    prefix = ROOT.relative_to(REPO)
    original = archived(PREREG, prefix / "PREREG.md")
    if not (ROOT / "PREREG.md").read_bytes().startswith(original):
        raise ValueError("Original preregistration changed")
    if (ROOT / "protocol.json").read_bytes() != archived(PREREG, prefix / "protocol.json"):
        raise ValueError("Frozen protocol changed")
    if setup()["model"] != PLAN["model"] or setup()["repeat_seeds"] != PLAN["seeds"]:
        raise ValueError("Model or v3 seed registry changed")


def behavioral_excerpt(text):
    """Preserve published wording while skipping task-wrapper sections."""
    mark = re.compile(r"(?m)^##\s+([^\n]+)$")
    blocks = list(mark.finditer(text))
    selected = []
    description = any("description" in block[1].lower() for block in blocks)
    for index, block in enumerate(blocks):
        title = re.sub(r"[*_#]", "", block[1]).strip().lower()
        if ("module interface" in title and description) or not re.search(
                r"description|design under test|input and output|module interface|functionality|behavior|behaviour",
                title):
            continue
        end = blocks[index + 1].start() if index + 1 < len(blocks) else len(text)
        selected.append(text[block.start():end].strip())
    explicit_behavior = any(re.search(r"functionality|behavior|behaviour", part.splitlines()[0], re.I)
                            for part in selected)
    return "\n\n".join(selected) if explicit_behavior and len(selected) >= 2 else text


def extract_public(dataset):
    import pyarrow.parquet as pq
    split = load(REPO / "stimulus-v1/split.json")
    permitted = split["development"]
    selected = {r["task_id"]: r for r in load(CVDP / "reports/selection.json")["selected"]}
    want = load(CVDP / "reports/dataset_audit.json")["sha256"]
    if hashlib.sha256(dataset.read_bytes()).hexdigest() != want:
        raise ValueError("Use the audited CVDP-ECov dataset revision")
    table = pq.read_table(dataset, columns=["id", "spec_files", "instruction"], filters=[("id", "in", permitted)])
    records = {}
    for row in table.to_pylist():
        name = row["id"]
        text = "\n\n".join(part["content"] for part in row["spec_files"]).strip()
        source = "spec_files" if text else "instruction"
        prose = text or row["instruction"]
        prose = re.sub(r"(?ms)^[ \t]*```[^\n]*\n.*?^[ \t]*```[ \t]*$", "", prose)
        prose = re.sub(r"(?ms)^[ \t]*module[ \t]+[^\n]*.*?^[ \t]*endmodule\b[^\n]*$", "", prose).strip()
        if not prose or re.search(r"(?m)^\s*(module\s+\w+|endmodule\b)", prose):
            raise ValueError(f"Public behavioral prose unavailable for {name}")
        records[name] = {
            "spec": prose,
            "spec_source": source,
            "model_spec": behavioral_excerpt(prose) if source == "instruction" else prose,
            **selected[name],
            "parameters": split["parameters"][name],
        }
    if set(records) != set(permitted) or len(records) != 10:
        raise ValueError("CVDP public input differs from the development split")
    save(ROOT / "public_b.json", records)


def roster(phase):
    if phase == "pilot":
        groups, seeds = PLAN["pilot_tasks"], [PLAN["pilot_seed"]]
    else:
        groups = {
            "A": [r["task_id"] for r in tasks()],
            "B": load(REPO / "stimulus-v1/split.json")["development"],
        }
        seeds = PLAN["seeds"]
    return [(group, task, seed) for group, names in groups.items() for task in names for seed in seeds]


def interface(group, name):
    if group == "A":
        problem, ports = public(name)
        ins, outs, clock, edge = ports
        return {"spec": problem["spec"], "input": ins, "output": outs, "clock": clock, "edge": edge}
    result = load(ROOT / "public_b.json")[name]
    if not result["spec"].strip():
        raise ValueError(f"Missing public specification for {name}")
    return result


def case_path(group, task, seed):
    return ROOT / "runs" / group / task / str(seed)


def vectors(group, task, seed, ports):
    if group == "A":
        rep = PLAN["seeds"].index(seed) + 1
        return load(V3 / "initial" / task / f"rep{rep}/vectors.json")
    home = V2 / "trial" / task / str(seed) / "initial"
    receipt = load(home / "status.json")
    if receipt["status"] != "complete":
        raise ValueError(f"Archived A0 stimulus unavailable for {task}/{seed}")
    code = (home / receipt["source"]).read_text()
    rows = driver_rows(code, ports["input"], seed, receipt["cycles"])
    serialized = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(serialized).hexdigest() != receipt["vector_sha256"]:
        raise ValueError(f"Archived A0 stimulus checksum changed for {task}/{seed}")
    return rows[:load(V2 / "protocol.json")["round_cycles"]]


def checker_inputs(group, rows):
    if group == "A":
        return rows
    return [edge for row in rows for edge in (
        {**{key: value for key, value in row.items() if key != "mid"}, "edge": "posedge"},
        {**{key: value for key, value in row.items() if key != "mid"}, **row.get("mid", {}), "edge": "negedge"},
    )]


def archived_base(task, seed):
    rep = PLAN["seeds"].index(seed) + 1
    prefix = Path("experiments/contract-review/runs") / task / f"rep{rep}"
    result = json.loads(archived(PLAN["contract_review_commit"], prefix / "configs/Base-think/result.json"))
    if result["status"] != "ready":
        return None, result["usage"]
    src = Path("experiments/contract-review") / result["model"]
    return archived(PLAN["contract_review_commit"], src).decode(), result["usage"]


def original_base_prompt(task, seed):
    rep = PLAN["seeds"].index(seed) + 1
    lines = (V3 / "initial" / task / f"rep{rep}/calls.jsonl").read_text().splitlines()
    return next(row["prompt"] for line in lines if
                ("Define reference(vectors)" in (row := json.loads(line))["prompt"] or
                 "Implement reference(vectors)" in row["prompt"]))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    verify_protocol()
    extract_public(args.dataset)
