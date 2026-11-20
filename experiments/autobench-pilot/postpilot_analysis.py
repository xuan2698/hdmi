"""Analyze archived pilot 2 vectors and predictions without any model calls."""

import csv
import json
import random
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from evaluation_io import simulate
from pilot2_guidance import edit
from pilot2_sim import VectorReplay, interface_from, lower_proxy_enums
from postpilot_probes import H_SITES, exact_g_check, h_diagnosis
from simulate import differences, expected_from, known_int, mismatches

BASE = Path(__file__).resolve().parent / "v2"
DEST = BASE / "reports" / "postpilot"
CONFIGS = ("A0", "B-B", "B-O", "O-B", "O-O")
REQUESTED_G_SAMPLE = 20
SEED = 20261120
CAUSES = (
    "a_unchecked", "b_expected_matches_mutant", "c_shared_golden_and_mutant_mismatch",
)


def read(path):
    return json.loads(path.read_text())


def write(name, data, *, compact=False):
    formatting = {"separators": (",", ":")} if compact else {"indent": 2}
    (DEST / name).write_text(json.dumps(data, ensure_ascii=False, **formatting) + "\n")


def table(name, rows):
    with (DEST / name).open("w", newline="") as stream:
        columns = list(dict.fromkeys(key for row in rows for key in row))
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rate(top, bottom):
    return top / bottom if bottom else None


def task_scope(task):
    public = BASE / "generation" / task
    problem = read(public / "problem.json")
    return public, problem, interface_from(problem)


def summarize_scores(trials):
    results = []
    for config in CONFIGS:
        rows = [row for _, row in trials if row["config"] == config]
        denominator = sum(row["H_total"] for row in rows)
        passing = [row for row in rows if row["golden_pass"]]
        old_hits = sum(row["H_detected"] for row in rows)
        raw_passing = sum(c["raw_checker_failure"] for row in passing for c in row["H_cases"])
        if raw_passing != sum(row["H_detected"] for row in passing):
            raise ValueError("Raw and additional failures must agree once golden passes")
        false_positives = len(rows) - len(passing)
        results.append({
            "configuration": config, "TB_count": len(rows), "H_total": denominator,
            "old_H_detected": old_hits, "old_H_rate": rate(old_hits, denominator),
            "new_H_detected": raw_passing, "new_H_rate": rate(raw_passing, denominator),
            "discounted_old_hits": old_hits - raw_passing,
            "golden_failed": false_positives, "golden_false_positive_rate": rate(false_positives, len(rows)),
        })
    table("detection.csv", results)
    return results


def bottleneck_by_task(trials):
    by_task = defaultdict(Counter)
    for folder, run in trials:
        notes = by_task[run["task"]]
        notes["TB_count"] += 1
        if run["golden_pass"]:
            notes["golden_pass"] += 1
        predictions = read(folder / "final_expected.json")
        notes["all_None_TBs"] += all(value is None for row in predictions for value in row.values())
        for case in run["H_cases"]:
            notes["H_evaluations"] += 1
            notes["old_" + case["verdict"]] += 1
            if run["golden_pass"]:
                notes["golden_passing_H"] += 1
                notes["golden_passing_" + case["verdict"]] += 1
    fields = ("TB_count", "golden_pass", "all_None_TBs", "H_evaluations", "old_detected",
              "old_not_exposed", "old_checker_missed", "golden_passing_H",
              "golden_passing_detected", "golden_passing_not_exposed", "golden_passing_checker_missed")
    curves = [{"task": task, **{field: counts[field] for field in fields}}
              for task, counts in sorted(by_task.items())]
    table("bottleneck_by_task.csv", curves)
    return curves


def never_exposed(trials):
    by_mutant, by_task = defaultdict(list), defaultdict(list)
    for folder, result in trials:
        by_task[result["task"]].append((result, read(folder / "final_vectors.json")))
        for case in result["H_cases"]:
            by_mutant[(result["task"], case["id"])].append(case)
    subjects = sorted(key for key, cases in by_mutant.items()
                      if not any(case["exposed"] for case in cases))
    if set(subjects) != H_SITES.keys():
        raise ValueError("The official mutation list changed. Confirm explicit probe anchors.")
    detailed, rows = [], []
    for task, mutant in subjects:
        _, problem, interface = task_scope(task)
        src = BASE / "eval" / task
        result = h_diagnosis(task, mutant, (src / "golden_rtl.v").read_text(),
                             (src / "official_mutants" / f"{mutant}.v").read_text(),
                             interface, by_task[task])
        detailed.append(result)
        rows.append({
            "task_number": problem["task_number"], "task": task, "mutant": mutant,
            "runs": len(result["runs"]), "original": result["original"], "changed": result["changed"],
            "evaluation_label": result["classification"],
            "raw_output_difference": result["raw_output_difference"],
            "probe_executions": sum(r["executed"] for r in result["runs"]),
            "probe_local_differences": sum(r["infected"] for r in result["runs"]),
            "raw_before_active": sum(r["raw_different_cycles_pre_active_opposite"][0] for r in result["runs"]),
            "raw_at_active": sum(r["raw_different_cycles_pre_active_opposite"][1] for r in result["runs"]),
        })
    table("never_exposed_H.csv", rows)
    write("never_exposed_H_probes.json", detailed)
    return {
        "distinct_mutants": len(rows),
        "labels": Counter(row["evaluation_label"] for row in rows),
        "run_level_labels": Counter(probe["label"] for row in detailed for probe in row["runs"]),
    }


def individual_miss(folder, result, case, reference, prediction, bench, subject):
    result_rtl = (subject / "official_mutants" / f"{case['id']}.v").read_text()
    mutated, _ = bench.trace(result_rtl)
    detects = mismatches(prediction, mutated)
    baseline = mismatches(prediction, reference)
    if bool(any(detects)) != case["raw_checker_failure"] or any(
        a - b for a, b in zip(detects, baseline, strict=True)
    ):
        raise ValueError(f"Legacy miss does not reproduce in {folder}/{case['id']}")
    checked_outputs = {name for row in prediction for name, value in row.items() if value is not None}
    sites = defaultdict(list)
    for tick, signal, original, changed in differences(reference, mutated):
        expected = prediction[tick][signal]
        if expected is None:
            cause = CAUSES[0]
        elif expected == known_int(changed):
            cause = CAUSES[1]
        elif signal in detects[tick] and signal in baseline[tick]:
            cause = CAUSES[2]
        else:
            raise ValueError(f"Unexplained comparison for {folder}/{case['id']}/{signal}/{tick}")
        sites[cause].append({
            "cycle": tick + 1, "signal": signal, "golden_binary": original,
            "mutant_binary": changed, "expected": expected,
            "expected_somewhere_on_signal": signal in checked_outputs,
        })
    if not sites:
        raise ValueError(f"A stored exposed miss had no output differences: {folder}/{case['id']}")
    # Shared errors demonstrate a distinct reason for zero *new* alarms. In the
    # remaining mixed cases prioritize a checked value accepted by the oracle.
    primary = next(cause for cause in reversed(CAUSES) if cause in sites)
    return {
        "task": result["task"], "configuration": result["config"], "repeat": result["repeat"],
        "mutant": case["id"], "golden_pass": result["golden_pass"],
        "mutant_reported_any_error": case["raw_checker_failure"],
        "primary": primary,
        "sites_unchecked": len(sites[CAUSES[0]]), "sites_match_mutant": len(sites[CAUSES[1]]),
        "sites_shared_error": len(sites[CAUSES[2]]), "evidence": dict(sites),
    }


def profile_misses(trials):
    rows = []
    silent_unchecked_runs = set()
    for folder, result in trials:
        misses = [c for c in result["H_cases"] if c["verdict"] == "checker_missed"]
        if not misses:
            continue
        task = result["task"]
        _, _, interface = task_scope(task)
        bench = VectorReplay(interface, read(folder / "final_vectors.json"))
        prediction = read(folder / "final_expected.json")
        if all(value is None for row in prediction for value in row.values()):
            silent_unchecked_runs.add(str(folder.relative_to(BASE)))
        subject = BASE / "eval" / task
        original, _ = bench.trace((subject / "golden_rtl.v").read_text())
        rows.extend(individual_miss(folder, result, c, original, prediction, bench, subject) for c in misses)
    table("exposed_H_misses.csv", [{key: value for key, value in row.items() if key != "evidence"} for row in rows])
    write("exposed_H_difference_sites.json", rows, compact=True)
    examples = {}
    for cause in CAUSES:
        chosen, seen = [], set()
        for row in rows:
            key = row["task"], row["mutant"]
            if row["primary"] != cause or key in seen:
                continue
            seen.add(key)
            chosen.append({**{k: v for k, v in row.items() if k != "evidence"},
                           "difference_examples": row["evidence"][cause][:2]})
            if len(chosen) == 2:
                break
        examples[cause] = chosen
    write("miss_examples.json", examples)
    return {
        "legacy_exposed_miss_count": len(rows),
        "classes": Counter(row["primary"] for row in rows),
        "strictly_silent_classes": Counter(row["primary"] for row in rows if not row["mutant_reported_any_error"]),
        "golden_passing_classes": Counter(row["primary"] for row in rows if row["golden_pass"]),
        "site_level_counts": {cause: sum(len(row["evidence"].get(cause, [])) for row in rows) for cause in CAUSES},
        "all_None_checkers_among_miss_runs": sorted(silent_unchecked_runs),
    }


EDGE_CLAUSES = {
    "reset": "active high synchronous reset",
    "capture": "For each bit in a 32-bit vector, capture when the input signal changes from 1 in one clock cycle to 0 the next.",
    "hold": '"Capture" means that the output will remain 1 until the register is reset (active high synchronous reset).',
}
FSM_CLAUSES = {
    "reset": "Reset is active high synchronous.",
    "detect": "When the sequence is found, it should set start_shifting to 1, forever, until reset.",
    "latch": "When the sequence is found, it should set start_shifting to 1, forever, until reset.",
    "search": "Build a finite-state machine that searches for the sequence 1101 in an input bit stream.",
}


def spec_clause(task, cycle, vectors, r2, r3):
    if task == "edgecapture":
        now = vectors[cycle]
        falling = (vectors[cycle - 1]["in"] & ~now["in"]) if cycle else 0
        key = "reset" if now["reset"] else "capture" if (r2 ^ r3) & falling else "hold"
        return key, EDGE_CLAUSES[key]
    if task == "review2015_fsmseq":
        history = ""
        detected = False
        key = "search"
        for row in vectors[:cycle + 1]:
            if row["reset"]:
                history, detected, key = "", False, "reset"
            else:
                history = (history + str(row["data"]))[-4:]
                key = "latch" if detected else "detect" if history == "1101" else "search"
                detected |= history == "1101"
        # The public text gives detection and retention in a single clause.
        return ("detect_and_latch" if key in ("detect", "latch") else key), FSM_CLAUSES[key]
    raise ValueError(f"Map observable behavior of the new disagreement task {task} to its public spec")


def checker_source(folder, number):
    for step in range(number, 0, -1):
        options = sorted(folder.glob(f"checker_{step:02d}*.py"))
        if options:
            return options[-1].read_text()
    raise ValueError(f"Missing archived checker for {folder} at round {number}")


def deduplicate_disagreements(trials):
    groups = {}
    raw_totals = Counter()
    for folder, trial in trials:
        config, task = trial["config"], trial["task"]
        if config not in ("B-O", "O-O"):
            continue
        rounds = [(r, r.get("checker_diagnostics", {}).get("counts", {}).get("proxies_disagree_with_each_other", 0))
                  for r in trial["per_round"]]
        if not any(n for _, n in rounds):
            continue
        public, problem, interface = task_scope(task)
        rtl = [(public / f"R{i}.v").read_text() for i in range(1, 4)]
        guide = read(BASE / "guidance" / task / "catalog.json")
        records = {entry["id"]: entry for batch in guide["groups"] for entry in batch["candidates"]}
        snapshots = read(folder / "stimulus_snapshots.json")
        for measurement, original_count in rounds:
            if not original_count:
                continue
            round_number = measurement["round"]
            vectors = snapshots[round_number - 1]
            bench = VectorReplay(interface, vectors, proxy_compat=True)
            expected = expected_from(checker_source(folder, round_number), interface[1], vectors)
            r1, r2, r3 = [bench.trace(item)[0] for item in rtl]
            r1_errors = mismatches(expected, r1)
            total = 0
            for mutant in measurement["exposed"]:
                obs, _ = bench.trace(edit(rtl[0], records[mutant]))
                errors = mismatches(expected, obs)
                for cycle, signal, _, _ in differences(r1, obs):
                    left, right = known_int(r2[cycle][signal]), known_int(r3[cycle][signal])
                    if signal not in r1_errors[cycle] or signal not in errors[cycle]:
                        continue
                    if left is None or right is None or left == right:
                        continue
                    total += 1
                    clause, quote = spec_clause(task, cycle, vectors, left, right)
                    if quote not in problem["spec"]:
                        raise ValueError(f"Clause does not match the archived specification for {task}")
                    key = (task, signal, clause)
                    row = groups.setdefault(key, {
                        "task": task, "task_number": problem["task_number"], "signal": signal,
                        "spec_clause": clause, "quote": quote, "B-O": 0, "O-O": 0,
                        "example": {"configuration": config, "repeat": trial["repeat"], "round": round_number,
                                    "cycle": cycle + 1, "mutant": mutant, "R2": left, "R3": right},
                    })
                    row[config] += 1
            if total != original_count:
                raise ValueError(f"{folder}/{round_number} recovered {total} of {original_count} stored events")
            raw_totals[config] += total
    rows = list(groups.values())
    write("feedback_issue_points.json", rows)
    table("feedback_issue_points.csv", [
        {**{k: v for k, v in row.items() if k != "example"}, "total": row["B-O"] + row["O-O"]}
        for row in rows
    ])
    return {"event_counts": raw_totals, "issue_points": len(rows),
            "by_configuration": {config: sum(row[config] > 0 for row in rows) for config in raw_totals}}


def golden_proxy_result(directory, golden_tb, source_file):
    def run(rtl_file, path):
        try:
            result, _ = simulate(path, "tb", rtl_file, golden_tb)
        except RuntimeError:
            return {"verdict": "compile_error", "diagnostic": (path / "compile.log").read_text()}
        except subprocess.TimeoutExpired:
            return {"verdict": "timeout"}
        match = re.search(r"^Mismatches:\s+(\d+) in (\d+) samples", result.stdout, re.MULTILINE)
        if result.returncode or not match:
            return {"verdict": "simulation_error", "diagnostic": result.stdout[-1500:]}
        bad, size = map(int, match.groups())
        return {"verdict": "failed" if bad else "passed", "mismatches": bad, "samples": size}

    strict = run(source_file, directory / "strict")
    answer = {"strict": strict}
    if strict["verdict"] == "compile_error" and re.search(
        "requires an explicit cast|Enumeration name .* incorrectly sized", strict["diagnostic"]
    ):
        compatible = lower_proxy_enums(source_file.read_text())
        if compatible != source_file.read_text():
            lowered = directory / "compatible.v"
            lowered.write_text(compatible)
            answer["enum_compatible"] = run(lowered, directory / "relaxed")
    return answer


def proxies_by_task(trials):
    by_task = defaultdict(list)
    for where, result in trials:
        by_task[result["task"]].append(where)
    rows, details = [], {}
    with tempfile.TemporaryDirectory(prefix="pilot2-audit-proxies-") as temp:
        space = Path(temp)
        for task, stimuli in sorted(by_task.items()):
            public, problem, interface = task_scope(task)
            tb = BASE / "eval" / task / "golden_tb.v"
            measured = {f"R{i}": golden_proxy_result(space / task / f"R{i}", tb, public / f"R{i}.v")
                        for i in range(1, 4)}
            count = Counter()
            for folder in stimuli:
                bench = VectorReplay(interface, read(folder / "final_vectors.json"), proxy_compat=True)
                r2, r3 = [bench.trace((public / f"R{i}.v").read_text())[0] for i in (2, 3)]
                for left, right in zip(r2, r3, strict=True):
                    for signal in left:
                        a, b = left[signal], right[signal]
                        count["raw_positions"] += 1
                        count["raw_disagreements"] += a != b
                        if known_int(a) is None or known_int(b) is None:
                            count["unknown_pairs"] += 1
                            continue
                        count["known_pairs"] += 1
                        count["known_disagreements"] += a != b
            rows.append({
                "task": task, "task_number": problem["task_number"],
                **{f"{name}_strict": record["strict"]["verdict"] for name, record in measured.items()},
                **{f"{name}_enum_compatible": record.get("enum_compatible", {}).get("verdict")
                   for name, record in measured.items()},
                **{name: count[name] for name in ("known_pairs", "known_disagreements", "unknown_pairs",
                                                 "raw_positions", "raw_disagreements")},
                "known_disagreement_rate": rate(count["known_disagreements"], count["known_pairs"]),
                "four_state_disagreement_rate": rate(count["raw_disagreements"], count["raw_positions"]),
            })
            details[task] = measured
    table("proxy_correctness_disagreement.csv", rows)
    write("proxy_golden_TB_details.json", details)


def audit_g(trials):
    eligible = []
    for folder, result in trials:
        for measurement in result["per_round"]:
            for mutant, findings in measurement.get("stimulus_diagnostics", {}).items():
                for position, finding in enumerate(findings):
                    if finding["label"] in ("未到达", "未感染"):
                        eligible.append((folder, result, measurement["round"], mutant, position, finding["label"]))
    sample = random.Random(SEED).sample(eligible, min(len(eligible), REQUESTED_G_SAMPLE))
    unique = {(r["task"], mutant, atom) for _, r, _, mutant, atom, _ in eligible}
    rows = []
    for folder, trial, number, mutant, position, prior in sample:
        task = trial["task"]
        public, _, interface = task_scope(task)
        catalogue = read(BASE / "guidance" / task / "catalog.json")
        descriptor = next(r for batch in catalogue["groups"] for r in batch["candidates"] if r["id"] == mutant)
        atom = descriptor["edits"][position]
        exact = exact_g_check((public / "R1.v").read_text(), atom, interface,
                              read(folder / "stimulus_snapshots.json")[number - 1])
        rows.append({
            "task": task, "configuration": trial["config"], "repeat": trial["repeat"], "round": number,
            "mutant": mutant, "atom": position, "original": atom["before"].strip(),
            "mutated": atom["after"].strip(), "stored_label": prior, **exact,
            "matches": prior == exact["exact_label"],
        })
    write("G_label_audit.json", rows)
    return {"requested": REQUESTED_G_SAMPLE, "random_seed": SEED,
            "eligible_observations": len(eligible), "unique_eligible_sites": len(unique),
            "audited": len(rows), "labels_agree": sum(row["matches"] for row in rows),
            "observed_agreement": rate(sum(row["matches"] for row in rows), len(rows))}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    trials = [(p.parent, read(p)) for p in sorted((BASE / "runs" / "second").glob("*/*/*/result.json"))]
    if len(trials) != 60 or any(r["status"] != "complete" for _, r in trials):
        raise ValueError("The archived cohort is incomplete")
    result = {"scores": summarize_scores(trials), "bottlenecks": bottleneck_by_task(trials),
              "never_exposed": never_exposed(trials),
              "exposed_misses": profile_misses(trials)}
    print("Replayed H cases", flush=True)
    result["feedback"] = deduplicate_disagreements(trials)
    print("Reconstructed and deduplicated proxy-disagreement feedback", flush=True)
    proxies_by_task(trials)
    result["G_audit"] = audit_g(trials)
    write("summary.json", result)
    print(f"Analysis written to {DEST}")


if __name__ == "__main__":
    main()
