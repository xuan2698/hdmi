"""Freeze the user-supplied sequential sample and elaborate its RTL interfaces."""

import hashlib
import json
import random
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

import pyarrow.parquet as pq
from pyslang.ast import Compilation
from pyslang.syntax import SyntaxTree

from audit_sources import COMMENTS

ROOT = Path(__file__).resolve().parent
IDENT = r"[A-Za-z_]\w*"
EVENT = re.compile(r"\balways(?:_ff)?\s*@\s*\(([^)]*)\)")
EDGE = re.compile(rf"\b(posedge|negedge)\s+({IDENT})")


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False) as stream:
        json.dump(obj, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    Path(stream.name).replace(path)


def load(path):
    return json.loads(path.read_text())


def config():
    return load(ROOT / "protocol.json")


def design_code(row):
    return "\n\n".join(f["content"] for f in row["rtl_files"])


def interface(row):
    compiler = Compilation()
    for f in row["rtl_files"]:
        compiler.addSyntaxTree(SyntaxTree.fromText(f["content"]))
    module, = [d for d in compiler.getRoot().topInstances if d.name == row["dut_module_name"]]
    ports = {"In": {}, "Out": {}}
    for p in module.body.portList:
        assert p.type.isIntegral and not p.type.isUnpackedArray
        ports[str(p.direction).rsplit(".", 1)[-1]][p.name] = p.type.bitWidth
    code = COMMENTS.sub("", design_code(row))
    edges = [m.groups() for prop in EVENT.finditer(code) for m in EDGE.finditer(prop[1])]
    reset = {n: int(e == "posedge") for e, n in edges if n in ports["In"]
             and re.search(r"(rst|reset)", n, re.I)}
    for n in ports["In"]:
        if n not in reset and re.search(r"(rst|reset)", n, re.I):
            reset[n] = int(not re.search(r"(?:_n|_b|rstn|resetn)$", n, re.I))
    clocks = list(dict.fromkeys(n for _, n in edges if n in ports["In"] and n not in reset))
    assert len(clocks) == 1 and ports["In"][clocks[0]] == 1, (row["id"], clocks)
    del ports["In"][clocks[0]]
    return {"input": ports["In"], "output": ports["Out"], "clock": clocks[0], "resets": reset,
            "top": row["dut_module_name"]}


def select(dataset):
    digest = hashlib.sha256(dataset.read_bytes()).hexdigest()
    if digest != load(ROOT / "reports" / "dataset_audit.json")["sha256"]:
        raise ValueError("Dataset differs from the audited CVDP-ECov release")
    all_rows = pq.read_table(dataset).to_pylist()
    by_suffix = {r["id"].split("_", 2)[-1].casefold(): r for r in all_rows}
    candidates, eligible = [], []
    for name in (ROOT / "candidates.txt").read_text().splitlines():
        row = by_suffix.get(name.casefold())
        if row is None:
            candidates.append({"candidate": name, "status": "not_found"})
            continue
        edge_blocks = list(dict.fromkeys(m[1] for m in EVENT.finditer(COMMENTS.sub("", design_code(row)))
                                        if EDGE.search(m[1])))
        candidates.append({"candidate": name, "task_id": row["id"], "edge_blocks": edge_blocks,
                           "status": "sequential" if edge_blocks else "no_edge_triggered_logic"})
        if edge_blocks:
            eligible.append(row)
    plan = config()
    selected = random.Random(plan["selection_seed"]).sample(sorted(eligible, key=lambda r: r["id"]),
                                                            min(plan["selection_count"], len(eligible)))
    save(ROOT / "reports" / "selection.json", {"seed": plan["selection_seed"], "eligible": len(eligible),
         "dataset_sha256": digest,
         "candidates": candidates, "selected": [{"task_id": row["id"], **interface(row)} for row in selected]})
    return selected
