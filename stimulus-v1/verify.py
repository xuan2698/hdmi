"""Verify the split, frozen protocol, shared prefixes, and simulation monitor."""

import argparse
import json
import random
import re
import subprocess
from pathlib import Path

from common import REPO, ROOT, digest, get_vectors, load, protocol, public, sample_path, save, source_vectors
from guide import catalog_path, span
from hdl import WORK, compile_sim, input_dir, observe


def run(dataset, require_complete):
    rows, plan = public(dataset), protocol()
    split = load(ROOT/"split.json")
    assert set(row["id"] for row in rows) == set(split["development"])
    assert len(set(split["final_test"])) == 15 and not set(split["development"]) & set(split["final_test"])
    actual = {p.name for p in (ROOT/"trial").iterdir() if p.is_dir()}
    assert actual == set(split["development"])
    frozen = "1fe1add7be34a292429f5708b2f64e5b3cbfc5f3"
    for filename in ("README.md","split.json","protocol.json"):
        committed = subprocess.check_output(["git","show",f"{frozen}:stimulus-v1/{filename}"], cwd=REPO)
        assert (ROOT/filename).read_bytes() == committed, filename
    comparisons = []
    checkpoints = 0
    for row in rows:
        task = row["id"]
        catalog = load(catalog_path(task))
        assert len(catalog["candidates"]) == plan["G_per_task"]
        assert len({span(row,a["edit"]) for a in catalog["candidates"]}) == plan["G_per_task"]
        for seed in plan["seeds"]:
            base = sample_path(task,seed)
            shared = load(base/"initial"/"status.json")
            assert shared["status"] == "complete"
            starting_G = None
            for cfg in plan["configs"]:
                path = base/cfg/"result.json"
                if not path.exists():
                    assert not require_complete, path
                    continue
                result = load(path)
                hist = result["history"]
                assert hist and len(hist)<=plan["max_rounds"]
                assert [r["cycles"] for r in hist] == [plan["round_cycles"]*n for n in range(1,len(hist)+1)]
                assert hist[-1]["cycles"] <= plan["max_cycles"]
                if starting_G is None:
                    starting_G = hist[0]["exposed"]
                assert hist[0]["exposed"] == starting_G
                assert all(set(x["exposed"]) <= set(y["exposed"]) for x,y in zip(hist,hist[1:]))
                if cfg=="A0":
                    assert len(hist)==1
                checkpoints += 1
        seed = plan["seeds"][0]
        initial = get_vectors(sample_path(task,seed)/"initial",row,seed,plan["round_cycles"])
        where = input_dir(WORK/"checks"/task,initial[:256],row["ports"])
        out = compile_sim(row["gold"],row["gold"],row["ports"])
        assert not observe(out,where,256)["samples"]
        item = catalog["candidates"][0]
        trace = r'''
always @(posedge phase, negedge phase) $display("MASKCHECK %b %b", ref_bits, mut_bits);
'''
        primary = observe(compile_sim(row["gold"],span(row,item["edit"]),row["ports"],trace),where,256)
        matched = re.findall(r"^MASKCHECK ([01xz]+) ([01xz]+)$",primary["text"],re.M)
        assert len(matched)==512
        assert not any("z" in a for a,b in matched)
        explicit = sum(any(x in "01" and x!=y for x,y in zip(a,b,strict=True)) for a,b in matched)
        assert explicit==primary["samples"]
        comparisons.append({"task":task,"known_difference_samples":explicit,"samples":len(matched)})
    logs = 0
    for path in (ROOT/"trial").rglob("calls.jsonl"):
        for line in path.read_text().splitlines():
            r = json.loads(line)
            prompt = r["prompt"]
            assert not any(fragment in prompt for fragment in ("equiv-audit/", "/eval/", "evaluation/"))
            assert r["model_requested"]==plan["model"]
            assert (r.get("model_actual") or plan["model"])==plan["model"]
            logs += 1
    task_map = {row["id"]:row for row in rows}
    segments = sorted(p for p in (ROOT/"trial").rglob("status.json") if load(p)["status"] == "complete")
    rebuilt = []
    for path in random.Random(plan["G_seed"]).sample(segments, 12):
        status = load(path)
        row = task_map[path.relative_to(ROOT/"trial").parts[0]]
        assert digest(source_vectors(path.parent, row, status["seed"], status["cycles"])) == status["vector_sha256"]
        rebuilt.append(str(path.relative_to(ROOT)))
    payload = {"protocol_commit":frozen,"development_tasks":len(rows),"untouched_final_test_ids":15,
               "shared_initials":len(rows)*len(plan["seeds"]),"verified_checkpoints":checkpoints,
               "dual_edge_monitor_validation":comparisons,"prompt_records_checked":logs,
               "source_reconstruction_samples":rebuilt}
    save(ROOT/"reports"/"verification.json",payload)
    print(json.dumps(payload,ensure_ascii=False),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset",type=Path)
    p.add_argument("--require-complete",action="store_true")
    a=p.parse_args()
    run(a.dataset,a.require_complete)
