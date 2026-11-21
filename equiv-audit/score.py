"""Recompute exposure from archived inputs and formally audited cohorts."""

import argparse
import csv
import sys
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean

from corpus import AUTO, BASE, CVDP, sources
from designs import config as cvdp_config, load, save
from pilot2_sim import VectorReplay
from pilot3_generate import driver_rows
from pilot3_inputs import public
from replay import compare, compile_pair, prepare_vectors, reset_rows
from simulate import differences

EQUIV = {"bounded_equivalent", "fully_equivalent"}
REPORTS = BASE / "reports"


def outcomes(cohort):
    return {(r["task"], r["tag"]): r for r in (load(p) for p in
            (REPORTS / f"{cohort}_cases").glob("*/*/result.json"))}


def csv_out(name, rows):
    if not rows:
        return
    with (REPORTS / name).open("w", newline="") as f:
        cols = tuple(dict.fromkeys(k for row in rows for k in row))
        writer = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def auto_addback(cases, formal):
    base = AUTO / "v3" / "reports" / "postpilot" / "H_exposure_per_mutant.csv"
    runs = defaultdict(list)
    with base.open() as f:
        for row in csv.DictReader(f):
            if row["configuration"] == "A0":
                runs[row["task_id"], int(row["repeat"])].append(row["final_exposed"] == "True")
    added = defaultdict(list)
    for case in cases:
        key = case["task"], case["tag"]
        if formal[key]["status"] == "non_equivalent" and any("autobench_v3/" in v for v in case["sources"]):
            added[case["task"]].append(case)
    before, after, detail = defaultdict(list), defaultdict(list), []
    for (task, rep), values in sorted(runs.items()):
        exposed = []
        if added[task]:
            vectors = load(AUTO / "v3" / "runs" / task / "A0" / f"rep{rep}" / "final_vectors.json")
            _, interface = public(task)
            bench = VectorReplay(interface, vectors)
            golden, _ = bench.trace(added[task][0]["original"])
            for case in added[task]:
                muted, _ = bench.trace(case["mutant"])
                exposed.append(bool(differences(golden, muted)))
                detail.append({"task": task, "mutant": case["tag"], "repeat": rep, "exposed": exposed[-1]})
        before[task].append(sum(values) / len(values))
        after[task].append((sum(values) + sum(exposed)) / (len(values) + len(exposed)))
    csv_out("autobench_v3_addback_runs.csv", detail)
    table = [{"task": task, "added": len(added[task]), "A0_before": mean(before[task]), "A0_after": mean(after[task])}
             for task in sorted(before)]
    csv_out("autobench_v3_addback.csv", table)
    return {"original": mean(r["A0_before"] for r in table), "with_addback": mean(r["A0_after"] for r in table),
            "added": sum(r["added"] for r in table), "tasks": len(table)}


def cvdp_stimuli(task, ports, plan):
    n = plan["random_cycles"]
    vectors = {f"random_{s}": reset_rows(ports, s, n) for s in plan["random_seeds"]}
    for seed in plan["stimulus_seeds"]:
        where = CVDP / "generation" / task / str(seed)
        if load(where / "status.json")["status"] != "complete":
            continue
        vec = where / "vectors.json"
        vectors[f"a0_{seed}"] = (load(vec) if vec.exists() else
                                 driver_rows((where / "stimulus.py").read_text(), ports["input"], seed, n))
    return vectors


def cvdp_eval(task, cases, formal, plan):
    if not cases:
        return []
    n = plan["random_cycles"]
    ports = cases[0]["ports"]
    vectors = cvdp_stimuli(task, ports, plan)
    out = []
    with tempfile.TemporaryDirectory(prefix="equiv-headroom-") as temp:
        folder = Path(temp)
        prepare_vectors(folder, vectors, ports)
        for case in cases:
            tag = case["tag"]
            sim = compile_pair(folder / tag, case["original"], case["mutant"], ports, n)
            runs = {seed: compare(sim, folder / seed, n, ports["output"]) for seed in vectors}
            out.append({"task": task, "mutant": tag, "formal": formal[(task, tag)]["status"],
                        **case["metadata"], "runs": runs})
    return out


def evaluate_cvdp(cases, formal, plan):
    by_task = defaultdict(list)
    for case in cases:
        by_task[case["task"]].append(case)
    with ThreadPoolExecutor(max_workers=4) as pool:
        return [row for batch in pool.map(lambda group: cvdp_eval(group[0], group[1], formal, plan),
                                         sorted(by_task.items())) for row in batch]


def exposed(row, run):
    return bool(row.get("runs", {}).get(run, {}).get("known_difference_samples", 0))


def cvdp_score(old_cases, new_cases, old_formal, new_formal):
    plan = cvdp_config()
    old = [c for c in old_cases if c["task"].startswith("cvdp_")
           and old_formal[(c["task"], c["tag"])]["status"] == "non_equivalent"]
    new = [c for c in new_cases if new_formal[(c["task"], c["tag"])]["status"] not in EQUIV | {"compile_failure"}]
    plus = evaluate_cvdp(old, old_formal, plan)
    rare = evaluate_cvdp(new, new_formal, plan)
    save(REPORTS / "cvdp_addback_exposure.json", plus)
    save(REPORTS / "cvdp_rare_exposure.json", rare)
    table = []
    a0 = [f"a0_{s}" for s in plan["stimulus_seeds"]]
    random = [f"random_{s}" for s in plan["random_seeds"]]
    for task in (x["task_id"] for x in load(CVDP / "reports" / "selection.json")["selected"]):
        original = load(CVDP / "eval" / "results" / f"{task}.json")
        h = sum(row["status"] == "kept" for row in original["H"].values())
        orig = {seed: len(original["runs"].get(seed, {}).get("exposed", [])) for seed in a0 + random}
        p = [row for row in plus if row["task"] == task]
        rr = [row for row in rare if row["task"] == task]
        decisive = [r for r in rr if r["formal"] == "non_equivalent"]
        valid = [seed for seed in a0 if seed in original["runs"]]
        def score(group, keys):
            return mean(sum(exposed(x, seed) for x in group) / len(group) for seed in keys) if group else None
        table.append({"task": task, "original_H": h, "confirmed_addback": len(p),
                      "original_A0": mean(orig[s] / h for s in a0),
                      "original_random": mean(orig[s] / h for s in random),
                      "addback_A0": mean((orig[s] + sum(exposed(x, s) for x in p)) / (h + len(p)) for s in a0),
                      "addback_random": mean((orig[s] + sum(exposed(x, s) for x in p)) / (h + len(p)) for s in random),
                      "rare_formal_confirmed": len(decisive), "rare_unresolved": len(rr) - len(decisive),
                      "rare_A0": score(rr, a0), "rare_A0_valid": score(rr, valid), "rare_random": score(rr, random),
                      "rare_confirmed_A0": score(decisive, a0), "rare_confirmed_random": score(decisive, random)})
    csv_out("cvdp_exposure_comparison.csv", table)
    misses = []
    for row in rare:
        misses_a = [seed for seed in a0 if seed in row["runs"] and not exposed(row, seed)]
        misses_b = [seed for seed in random if not exposed(row, seed)]
        if not misses_a and not misses_b:
            continue
        misses.append({"task": row["task"], "mutant": row["mutant"], "formal": row["formal"],
                       "any_A0_exposed": any(exposed(row, s) for s in a0),
                       "any_random_exposed": any(exposed(row, s) for s in random),
                       "A0_valid_misses": "|".join(misses_a), "long_random_misses": "|".join(misses_b),
                       "expected_trigger": row["trigger"], "bug": row["bug"], "effect": row["effect"]})
    csv_out("cvdp_rare_unexposed.csv", misses)
    keys = ("original_A0", "original_random", "addback_A0", "addback_random", "rare_A0", "rare_A0_valid",
            "rare_random", "rare_confirmed_A0", "rare_confirmed_random")
    values = {k: [r[k] for r in table if r[k] is not None] for k in keys}
    return {"rates": {k: mean(v) if v else None for k, v in values.items()},
            "task_counts": {k: len(v) for k, v in values.items()},
            "evaluated": len(rare), "formal_confirmed": sum(r["formal"] == "non_equivalent" for r in rare),
            "formal_unknown": sum(r["formal"] == "unknown" for r in rare),
            "missed_by_all_A0": sum(not any(exposed(x, s) for s in a0) for x in rare),
            "missed_by_all_random": sum(not any(exposed(x, s) for s in random) for x in rare),
            "missed_by_both": sum(not any(exposed(x, s) for s in a0 + random) for x in rare)}


def formal_report(cohort, formal):
    items = sorted(formal.values(), key=lambda row: (row["task"], row["tag"]))
    table, lengths = [], Counter()
    for row in items:
        t = {k: v for k, v in row.items() if not isinstance(v, (dict, list))}
        t["sources"] = "|".join(row["sources"])
        for key in ("bug", "trigger", "effect"):
            t[key] = row["metadata"].get(key)
        t["terminal_inputs_binary"] = str(row.get("terminal_inputs_binary", ""))
        t["different_outputs"] = str(row.get("different_outputs", ""))
        table.append(t)
        if row["status"] == "non_equivalent":
            lengths[row["counterexample_cycles"]] += 1
    csv_out(f"{cohort}_formal.csv", table)
    if lengths:
        csv_out(f"{cohort}_counterexample_distribution.csv", [{"cycles": x, "count": n} for x, n in sorted(lengths.items())])
    by_source = defaultdict(Counter)
    for row in items:
        for source in {item.split("/", 1)[0] for item in row["sources"]}:
            by_source[source][row["status"]] += 1
    return {"class_counts": dict(Counter(r["status"] for r in items)),
            "by_source": {key: dict(counts) for key, counts in sorted(by_source.items())},
            "counterexample_cycles": dict(sorted(lengths.items()))}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    args = p.parse_args()
    old, new = (sources(args.dataset, kind) for kind in ("old", "new"))
    old_formal, new_formal = (outcomes(kind) for kind in ("old", "new"))
    for items, results in ((old, old_formal), (new, new_formal)):
        if {(c["task"], c["tag"]) for c in items} != set(results):
            raise ValueError("The formal audit is not complete for the selected cohort")
    summary = {"old": formal_report("old", old_formal), "new": formal_report("new", new_formal),
               "autobench_v3": auto_addback(old, old_formal),
               "cvdp": cvdp_score(old, new, old_formal, new_formal)}
    save(REPORTS / "summary.json", summary)
    import json
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
