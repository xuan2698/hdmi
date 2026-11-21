"""Replay the frozen v3 pilot and audit evaluation without model calls."""

import argparse
import ast
import json
import random
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher, unified_diff
from itertools import combinations
from statistics import mean

import numpy as np
from scipy import stats

from pilot2_generate import load, save
from pilot2_guidance import edit
from pilot2_sim import VectorReplay
from pilot3_evaluation import archive, check_differences, table, upstream
from pilot3_generate import check_rows, driver_rows
from pilot3_inputs import BASE, public, setup, tasks
from pilot3_report import exact_signed_rank
from simulate import RunError, differences

DEST = BASE / "reports" / "postpilot"
PHASES = ("before_active", "after_active", "after_opposite")
SAMPLE_SEED = 20261121
MUTATION_NOTES = {
    (10, "07"): ("给同步触发器的敏感列表新增复位上升沿", "新增异步事件。G 可以翻转已有边沿、去掉已有异步复位项或改条件，没有给同步敏感列表添加复位沿的规则。"),
    (31, "01"): ("Q 上电初值由 0 改为 1", "上电初始化。G 的赋值规则检测行首普通赋值，不检测 `initial` 语句。第一个活跃沿覆盖 Q。"),
    (31, "05"): ("移除 Q 的上电初值，初始变为 X", "上电初始化。G 不删除 `initial` 语句。第一个活跃沿覆盖 Q。"),
    (40, "05"): ("从敏感列表移除异步复位上升沿，保留复位分支", "已有异步事件被删除，与 G 的 temporal_reset 同类。需要跨评分沿的异步复位序列。"),
    (76, "02"): ("给正沿 DFF 敏感列表新增复位上升沿", "新增异步事件，G 无对应新增规则。活跃沿重新按当前输入赋值。"),
    (99, "04"): ("给下降沿 DFF 敏感列表新增复位下降沿", "新增异步事件，G 无对应新增规则。活跃沿重新按当前输入赋值。"),
    (154, "05"): ("秒进位比较常量由 BCD 59 改成 58", "与 G 的 ±1 思路相近，位置是嵌套比较字面量。G 的 ±1 规则针对整个常量右值，没有对该嵌套比较执行字面量替换。"),
    (156, "02"): ("百位进位条件由低两位 BCD 99 改成 98", "与 G 的 ±1 思路相近，目标是进位向量里的比较字面量。G 的 ±1 规则针对整个常量右值。"),
}


def export(name, rows):
    table(DEST / (name + ".csv"), rows, tuple(dict.fromkeys(k for row in rows for k in row)))


def selected(path, role, stage):
    record = load(path / f"{role}_{stage:02d}_validation.json")
    return (path / record["selected"]).read_text(), record


def score(expected, trace):
    misses = check_differences(expected, trace, trace)
    return not any(misses), sum(map(bool, misses))


def score_h(expected, golden, traces):
    passed, failed_cycles = score(expected, golden)
    exposures, alarms, positions = {}, {}, {}
    for tag, trace in traces.items():
        positions[tag] = len(differences(golden, trace))
        exposures[tag] = bool(positions[tag])
        alarms[tag] = any(check_differences(expected, trace, golden))
    return {"golden_pass": passed, "golden_failed_cycles": failed_cycles,
            "exposure": exposures, "alarm": alarms, "positions": positions,
            "H_detected": sum(alarms.values()) if passed else 0}


def edits(a, b):
    counts = Counter()
    for op, i, j, x, y in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        counts["removed"] += j - i if op in ("replace", "delete") else 0
        counts["added"] += y - x if op in ("replace", "insert") else 0
    return counts["removed"], counts["added"]


def compare(a, b):
    vec_a, code_a, pred_a = a
    vec_b, code_b, pred_b = b
    # Vectors are execution order, so count altered rows at the same cycle plus the suffix.
    changed = sum(x != y for x, y in zip(vec_a, vec_b))
    extra = len(vec_b) - len(vec_a)
    removed, added = edits(code_a.splitlines(), code_b.splitlines())
    return {"stimulus_different": bool(changed or extra), "stimulus_changed_overlap_rows": changed,
            "stimulus_only_left_rows": max(-extra, 0), "stimulus_only_right_rows": max(extra, 0),
            "stimulus_different_rows": changed + abs(extra), "checker_source_different": code_a != code_b,
            "checker_removed_lines": removed, "checker_added_lines": added,
            "checker_diff_lines": removed + added,
            "checker_ast_different": ast.dump(ast.parse(code_a)) != ast.dump(ast.parse(code_b)),
            "expected_different_overlap_rows": sum(x != y for x, y in zip(pred_a, pred_b))}


def original_notes(task, case, problem):
    """Use a task-specific spec citation for each residual mismatch, when available."""
    signal, inputs = case["signal"], case["inputs"]
    clauses = {
        "edgecapture": "For each bit in a 32-bit vector, capture when the input signal changes from 1 in one clock cycle to 0 the next.",
        "m2014_q4c": problem["spec"],
        "circuit9": "// 5ns             1               1               4",
        "review2015_fsmseq": "When the sequence is found, it should set start_shifting to 1, forever, until reset.",
        "history_shift": "When a branch prediction is made (predict_valid = 1), shift in predict_taken from the LSB side to update the branch history for the predicted branch.",
        "mt2015_muxdff": "//         q <= {q[1] ^ q[2], q[0], q[2]};",
        "gshare": "When a branch prediction is requested (predict_valid = 1) for a given pc, the branch predictor produces the predicted branch direction and state of the branch history register used to make the prediction.",
        "lemmings4": "If a Lemming falls for more than 20 clock cycles then hits the ground, it will splatter and cease walking, falling, or digging (all 4 outputs become 0), forever (Or until the FSM gets reset).",
        "countbcd": "For digits [3:1], also output an enable signal indicating when each of the upper three digits should be incremented." if signal == "ena" else "Each decimal digit is encoded using 4 bits: q[3:0] is the ones digit, q[7:4] is the tens digit, etc.",
        "dff8r": problem["spec"],
        "ece241_2014_q5a": "The input (x) is a series of bits (one per clock cycle) beginning with the least-significant bit of the number, and the output (Z) is the 2's complement of the input.",
        "count_clock": "hh, mm, and ss are two BCD (Binary-Coded Decimal) digits each for hours (01-12), minutes (00-59), and seconds (00-59).",
        "fsm3s": "// State | Next state in=0, Next state in=1 | Output",
        "dff8p": problem["spec"],
        "count10": "Build a decade counter that counts from 0 through 9, inclusive, with a period of 10.",
        "circuit10": "The output of the flip-flop has been made observable through the output state." if signal == "state" else "Read the simulation waveforms to determine what the circuit does, then implement it.",
    }
    if task == "2014_q3c":
        state = f"{inputs['y']:03b}"
        for line in problem["spec"].splitlines():
            if line.startswith(f"// {state} |"):
                return line
        return f"Present state y={state} is outside the five rows of the public state table."
    return clauses[task]


def matches_number(value, bits, mask):
    return all(k not in "01" or a == b for a, b, k in zip(f"{value:0{len(mask)}b}", bits, mask, strict=True))


def reset_flags(task, vectors, asynchronous):
    pins = []
    for name in vectors[0]:
        lower = name.lower()
        if "reset" in lower or (task == "m2014_q4c" and name == "r"):
            pins.append((name, not lower.endswith(("resetn", "reset_n"))))
    flags, seen = [], False
    for row in vectors:
        active = any(row[n] == polarity for n, polarity in pins)
        mid_active = any(row.get("mid", {}).get(n, row[n]) == polarity for n, polarity in pins)
        flags.append("during_reset" if active else "before_first_reset" if pins and not seen else "")
        seen |= active or (asynchronous and mid_active)
    return flags


def failure(task, problem, interface, vectors, expected, phases):
    active = phases["after_active"]
    mismatches = check_differences(expected, active, active)
    first = next((i for i, names in enumerate(mismatches) if names), None)
    if first is None:
        return None
    flags = reset_flags(task, vectors, "asynchronous" in problem["spec"].lower())
    positions = []
    for signal in interface[1]:
        if signal not in mismatches[first]:
            continue
        original = active[first][signal]
        value = expected[first][signal]
        prev = active[first - 1][signal] if first else None
        after = active[first + 1][signal] if first + 1 < len(active) else None
        matches_prev = prev is not None and matches_number(value, prev, original)
        matches_next = after is not None and matches_number(value, after, original)
        category = "a" if flags[first] else "b" if matches_prev or matches_next else "c"
        row = {"cycle": first + 1, "signal": signal, "category": category,
               "reset_phase": flags[first], "expected_decimal": value,
               "expected_bits": f"{value:0{len(original)}b}", "golden_bits": original,
               "previous_bits": prev, "next_bits": after, "matches_previous": matches_prev,
               "matches_next": matches_next, "inputs": vectors[first]}
        if category == "c":
            row["spec_clause"] = original_notes(task, row, problem)
        positions.append(row)
    outside_reset_pass = not any(names for names, flag in zip(mismatches, flags, strict=True) if not flag)
    aligned = {f"{name}_passes": score(expected, trace)[0] for name, trace in phases.items()}
    corrected = {}
    for shift in (-1, 1):
        start, stop = int(shift == -1), len(active) - int(shift == 1)
        corrected["global_previous_passes" if shift == -1 else "global_next_passes"] = all(
            matches_number(value, active[i + shift][name], active[i + shift][name])
            for i in range(start, stop) for name, value in expected[i].items())
    return {**positions[0], "same_cycle_site_count": len(positions), "all_first_cycle_sites": positions,
            "skip_reset_windows_passes": outside_reset_pass, **aligned, **corrected}


def stage_audit(path, scope, history, start_bundle, final_bundle, interface, run, plan, trace_for):
    vectors, checker, expected = start_bundle
    changes = []
    for here, after in zip(history, history[1:]):
        stage = after["round"]
        if here["stimulus_sent"]:
            source, validation = selected(path, "stimulus", stage)
            vectors = vectors + driver_rows(source, interface[0], run["seed"] + here["round"], plan["append_cycles"])
            if validation["regenerations"]:
                changes.append({**scope, "stage": stage, "role": "stimulus", "proxy_feedback": False,
                                "feedback_sent": True, "selected_try": validation["regenerations"] + 1,
                                "selected_evidence_present": False})
        file = path / f"checker_{stage:02d}_validation.json"
        if not file.exists():
            if here["checker_sent"]:
                raise ValueError(f"Missing selected checker in {path} stage {stage}")
            expected = check_rows(checker, interface[1], vectors)
            continue
        revised, validation = selected(path, "checker", stage)
        proposed = check_rows(revised, interface[1], vectors)
        golden = trace_for(vectors)["after_active"]
        prefix = len(expected)
        old_prefix = check_rows(checker, interface[1], vectors[:prefix])
        revised_prefix = check_rows(revised, interface[1], vectors[:prefix])
        previous_pass, previous_failures = score(old_prefix, golden[:prefix])
        revised_pass, revised_failures = score(revised_prefix, golden[:prefix])
        try:
            old = check_rows(checker, interface[1], vectors)
            old_pass, old_failures = score(old, golden)
        except (RunError, ValueError):
            old = []
            old_pass = old_failures = None
        new_pass, new_failures = score(proposed, golden)
        changes.append({**scope, "stage": stage, "role": "checker", "proxy_feedback": here["checker_sent"],
                        "feedback_sent": True, "selected_try": validation["regenerations"] + 1,
                        "selected_evidence_present": validation["regenerations"] == 0,
                        "previous_cycles": prefix, "fixed_cycles": len(vectors),
                        "code_changed": checker != revised,
                        "ast_changed": ast.dump(ast.parse(checker)) != ast.dump(ast.parse(revised)),
                        "expected_changed_rows": sum(x != y for x, y in zip(old, proposed)) if old else None,
                        "golden_before_fixed": old_pass, "golden_after_fixed": new_pass,
                        "golden_failed_cycles_before_fixed": old_failures, "golden_failed_cycles_after_fixed": new_failures,
                        "golden_before_prefix": previous_pass, "golden_after_prefix": revised_pass,
                        "golden_failed_cycles_before_prefix": previous_failures,
                        "golden_failed_cycles_after_prefix": revised_failures})
        checker, expected = revised, proposed
    if (vectors, checker, expected) != final_bundle:
        raise ValueError(f"Selected versions do not reconstruct final bundle {path}")
    return changes


def audit_block(entry, rep, seed, plan):
    task = entry["task_id"]
    problem, interface = public(task)
    source = upstream(task)
    original = (source / "golden_rtl.v").read_text()
    group = {row["id"]: (source / "official_mutants" / (row["id"] + ".v")).read_text()
             for row in load(archive(task) / "prescreen.json")["cases"] if row["status"] == "kept"}
    cached, variants = {}, {}
    guidance = BASE / "guidance" / task
    selected_anchor = load(guidance / "anchor.json")["anchor"]
    anchor = (BASE / "proxies" / task / (selected_anchor + ".v")).read_text()
    catalog = load(guidance / "catalog.json")
    guide_rtls = [(row["id"], edit(anchor, row)) for batch in catalog["groups"]
                  for row in batch["candidates"] if row["retained"]]
    guide_traces = {}

    def key(vectors):
        return json.dumps(vectors, sort_keys=True, separators=(",", ":"))

    def reference(vectors):
        token = key(vectors)
        if token not in cached:
            trace = VectorReplay(interface, vectors, all_edges=True).trace(original)[0]
            cached[token] = {name: trace[i::3] for i, name in enumerate(PHASES)}
        return cached[token]

    def assess(vectors, expected):
        golden = reference(vectors)["after_active"]
        token = key(vectors)
        if token not in variants:
            bench = VectorReplay(interface, vectors)
            variants[token] = {tag: bench.trace(rtl)[0] for tag, rtl in group.items()}
        return score_h(expected, golden, variants[token])

    def exposed_g(vectors, size):
        token = key(vectors)
        bench = VectorReplay(interface, vectors, proxy_compat=True)
        if token not in guide_traces:
            guide_traces[token] = bench.trace(anchor)[0], {}
        ref, exposed = guide_traces[token]
        for tag, rtl in guide_rtls[:size]:
            if tag not in exposed:
                exposed[tag] = bool(differences(ref, bench.trace(rtl)[0]))
        return {tag for tag, _ in guide_rtls[:size] if exposed[tag]}

    initial = BASE / "initial" / task / f"rep{rep}"
    start = load(initial / "vectors.json"), (initial / "checker.py").read_text(), load(initial / "expected.json")
    raw_driver, _ = selected(initial, "stimulus", 1)
    raw_checker, _ = selected(initial, "checker", 1)
    if (driver_rows(raw_driver, interface[0], seed, plan["stimulus_cycles"]) != start[0]
            or raw_checker != start[1] or check_rows(raw_checker, interface[1], start[0]) != start[2]):
        raise ValueError(f"Shared initial bundle mismatch at {initial}")
    beginning = assess(start[0], start[2])
    scope = {**entry, "repeat": rep, "seed": seed}
    bundles, rows, scores, failures, stage_rows, mutants, migration = {}, [], {}, [], [], [], []
    for cfg in plan["configs"]:
        path = BASE / "runs" / task / cfg / f"rep{rep}"
        frozen = load(path / "result.json")
        if (frozen["status"], frozen["seed"], frozen["initial"]) != ("complete", seed, str(initial.relative_to(BASE))):
            raise ValueError(f"Wrong run identity: {path}")
        final = load(path / "final_vectors.json"), (path / "final_checker.py").read_text(), load(path / "final_expected.json")
        vectors, checker, expected = final
        if vectors[:len(start[0])] != start[0] or check_rows(checker, interface[1], vectors) != expected:
            raise ValueError(f"Final bundle fails prefix or expected reconstruction: {path}")
        end = assess(vectors, expected)
        for field in ("golden_pass", "golden_failed_cycles", "H_detected"):
            if frozen[field] != end[field]:
                raise ValueError(f"Metric {field} does not reproduce for {path}")
        observed = {case["id"]: (case["exposed"], case["checker_reported"], case["known_difference_positions"])
                    for case in frozen["H_outcomes"]}
        if observed != {k: (v, end["alarm"][k], end["positions"][k]) for k, v in end["exposure"].items()}:
            raise ValueError(f"Individual H results do not reproduce for {path}")
        if not {k for k, v in beginning["exposure"].items() if v} <= {k for k, v in end["exposure"].items() if v}:
            raise ValueError(f"Initial H exposure regressed at {path}")
        case = {**scope, "configuration": cfg}
        rounds = frozen["guidance"]
        if rounds[-1]["cycles"] != len(vectors) or len(vectors) != frozen["cycles"]:
            raise ValueError(f"Wrong final round length in {path}")
        stage_rows.extend(stage_audit(path, case, rounds, start, final, interface, frozen, plan, reference))
        bundles[cfg], scores[cfg] = final, end
        row = {**case, "initial_cycles": len(start[0]), "final_cycles": len(vectors), "H_total": len(group),
               "initial_H_exposed": sum(beginning["exposure"].values()), "final_H_exposed": sum(end["exposure"].values()),
               **{f"initial_{k}": beginning[k] for k in ("golden_pass", "golden_failed_cycles", "H_detected")},
               **{f"final_{k}": end[k] for k in ("golden_pass", "golden_failed_cycles", "H_detected")},
               **compare(start, final)}
        rows.append(row)
        mutants.extend({**case, "mutant": tag, "initial_exposed": beginning["exposure"][tag],
                        "final_exposed": exposed, "initial_positions": beginning["positions"][tag],
                        "final_positions": end["positions"][tag]} for tag, exposed in end["exposure"].items())
        issue = failure(task, problem, interface, vectors, expected, reference(vectors))
        if issue:
            failures.append({**case, **issue})
        if "O" in cfg:
            g = rounds[-1]["fixed_G"]
            if any(r["fixed_G"] != g for r in rounds) or g != rounds[-1]["active_G"]:
                raise ValueError(f"Malformed fixed G cohort in {path}")
            before, after = rounds[0]["fixed_G_exposed"], rounds[-1]["fixed_G_exposed"]
            replayed_before = exposed_g(start[0], g)
            replayed_after = exposed_g(vectors, g)
            if (len(replayed_before) != before or len(replayed_after) != after
                    or not replayed_before <= replayed_after or replayed_after != set(rounds[-1]["exposed"])):
                raise ValueError(f"Invalid G exposure at {path}")
            migration.append({**case, "G_fixed_total": g, "G_exposed_initial": before, "G_exposed_final": after,
                              "G_gain_pp": 100 * (after - before) / g,
                              "H_total": len(group), "H_exposed_initial": row["initial_H_exposed"],
                              "H_exposed_final": row["final_H_exposed"],
                              "H_gain_pp": 100 * (row["final_H_exposed"] - row["initial_H_exposed"]) / len(group)})
    pairs = [{**scope, "left": a, "right": b, **compare(bundles[a], bundles[b]),
              "golden_left": scores[a]["golden_pass"], "golden_right": scores[b]["golden_pass"]}
             for a, b in combinations(plan["configs"], 2)]
    outcomes = {cfg: scores[cfg]["golden_pass"] for cfg in plan["configs"]}
    agreement = {**scope, **outcomes, "unanimous": len(set(outcomes.values())) == 1,
                 "distinct_stimuli": len({key(x[0]) for x in bundles.values()}),
                 "distinct_checker_sources": len({x[1] for x in bundles.values()})}
    return rows, pairs, [agreement], failures, stage_rows, mutants, migration


def exposure_report(trials, plan):
    indexed = defaultdict(list)
    for row in trials:
        indexed[row["task_id"], row["configuration"]].append(row)
    per_task, macro = [], []
    for task in tasks():
        for cfg in plan["configs"]:
            subset = indexed[task["task_id"], cfg]
            h = sum(r["H_total"] for r in subset)
            start, final = (sum(r[key] for r in subset) for key in ("initial_H_exposed", "final_H_exposed"))
            per_task.append({**task, "configuration": cfg, "runs": len(subset), "H_opportunities": h,
                             "initial_H_exposed": start, "final_H_exposed": final,
                             "initial_exposure_rate": start / h, "final_exposure_rate": final / h,
                             "gain_pp": 100 * (final - start) / h})
    for cfg in plan["configs"]:
        rows = [row for row in per_task if row["configuration"] == cfg]
        macro.append({"configuration": cfg, "tasks": len(rows), **{key: sum(r[key] for r in rows)
                      for key in ("H_opportunities", "initial_H_exposed", "final_H_exposed")},
                      **{key: mean(r[key] for r in rows)
                       for key in ("initial_exposure_rate", "final_exposure_rate", "gain_pp")}})
    registry = {(row["task_id"], row["configuration"]): row for row in per_task}
    pairs, pair_tasks = [], []
    for index, (left, right) in enumerate((("O-B", "B-B"), ("O-O", "B-O"))):
        for metric, scale in (("initial_exposure_rate", 100), ("final_exposure_rate", 100), ("gain_pp", 1)):
            delta = []
            for task in tasks():
                k = task["task_id"]
                a, b = registry[k, left][metric] * scale, registry[k, right][metric] * scale
                delta.append(round(a - b, 12))
                pair_tasks.append({**task, "left": left, "right": right, "metric": metric,
                                   "left_percent_or_pp": a, "right_percent_or_pp": b, "difference_pp": delta[-1]})
            w, p, nonzero = exact_signed_rank(delta)
            rng = np.random.default_rng(plan["bootstrap_seed"] + index)
            draws = rng.choice(delta, size=(plan["bootstrap_draws"], len(delta)), replace=True).mean(axis=1)
            low, high = np.percentile(draws, [2.5, 97.5])
            pairs.append({"left": left, "right": right, "metric": metric, "task_pairs": len(delta),
                          "nonzero_pairs": nonzero, "W": w, "two_sided_p": p, "mean_delta_pp": mean(delta),
                          "bootstrap_95_low_pp": float(low), "bootstrap_95_high_pp": float(high)})
    for name, rows in (("H_exposure_per_task", per_task), ("H_exposure_macro", macro),
                       ("H_exposure_paired", pairs), ("H_exposure_paired_tasks", pair_tasks)):
        export(name, rows)
    return macro, pairs


def agreement_report(pairs, agreements, stages, plan):
    metrics = ("stimulus_different", "checker_source_different", "checker_ast_different",
               "expected_different_overlap_rows")
    pair_counts = [{"left": a, "right": b, "task_seeds": len(group),
                    **{k: sum(bool(r[k]) for r in group) for k in metrics},
                    "golden_same": sum(r["golden_left"] == r["golden_right"] for r in group)}
                   for a, b in combinations(plan["configs"], 2)
                   for group in [[r for r in pairs if (r["left"], r["right"]) == (a, b)]]]
    export("pairwise_TB_difference_summary", pair_counts)
    revisions = []
    for cfg in ("all", *plan["configs"]):
        records = [r for r in stages if r["role"] == "checker" and r["proxy_feedback"]
                   and (cfg == "all" or r["configuration"] == cfg)]
        fixed = [r for r in records if r["golden_before_fixed"] is not None]
        revisions.append({"configuration": cfg, "checker_feedback_stages": len(records),
                          "checker_source_changed": sum(r["code_changed"] for r in records),
                          "checker_AST_changed": sum(r["ast_changed"] for r in records),
                          "checker_expected_changed_fixed_rows": sum(bool(r["expected_changed_rows"]) for r in fixed),
                          "fixed_input_comparable": len(fixed),
                          "golden_changed_fixed": sum(r["golden_before_fixed"] != r["golden_after_fixed"] for r in fixed),
                          "golden_fail_to_pass_fixed": sum(not r["golden_before_fixed"] and r["golden_after_fixed"] for r in fixed),
                          "golden_pass_to_fail_fixed": sum(r["golden_before_fixed"] and not r["golden_after_fixed"] for r in fixed),
                          "golden_changed_old_prefix": sum(r["golden_before_prefix"] != r["golden_after_prefix"] for r in records),
                          "selected_repair_omitted_feedback": sum(not r["selected_evidence_present"] for r in records)})
    export("checker_feedback_summary", revisions)
    return {"task_seed_groups": len(agreements), "golden_unanimous": sum(r["unanimous"] for r in agreements),
            "unanimous_pass": sum(r["unanimous"] and r["A0"] for r in agreements),
            "unanimous_fail": sum(r["unanimous"] and not r["A0"] for r in agreements),
            "all_stimuli_identical_groups": sum(r["distinct_stimuli"] == 1 for r in agreements),
            "all_checkers_identical_groups": sum(r["distinct_checker_sources"] == 1 for r in agreements),
            "checker_feedback": revisions,
            "selected_repair_omitted_feedback": dict(Counter(r["role"] for r in stages
                                                             if not r["selected_evidence_present"]))}


def failure_report(failures, plan):
    counts, examples = [], {}
    for cfg in ("all", *plan["configs"]):
        subset = [r for r in failures if cfg == "all" or r["configuration"] == cfg]
        counts.extend({"configuration": cfg, "category": label, "tb_count": len(subset),
                       "count": sum(row["category"] == label for row in subset),
                       "rate": sum(row["category"] == label for row in subset) / len(subset)}
                      for label in "abc")
    for category in "abc":
        examples[category] = []
        choices = [r for r in failures if r["category"] == category]
        if category == "a":
            choices.sort(key=lambda r: r["reset_phase"] != "before_first_reset")
        elif category == "b":
            choices.sort(key=lambda r: r["matches_previous"] == r["matches_next"])
        for row in choices:
            if any(row["task_id"] == x["task_id"] for x in examples[category]):
                continue
            examples[category].append(row)
            if len(examples[category]) == 2:
                break
    export("false_positive_categories", counts)
    save(DEST / "false_positive_examples.json", examples)
    return {"total": len(failures), "counts": {label: sum(r["category"] == label for r in failures) for label in "abc"},
            "reset_context": dict(Counter(r["reset_phase"] for r in failures if r["reset_phase"])),
            "multiple_first_cycle_outputs": sum(r["same_cycle_site_count"] > 1 for r in failures),
            "mixed_categories_at_first_cycle": sum(len({p["category"] for p in r["all_first_cycle_sites"]}) > 1
                                                   for r in failures),
            "skip_reset_windows_rescued": sum(r["skip_reset_windows_passes"] for r in failures),
            "before_active_rescued": sum(r["before_active_passes"] for r in failures),
            "after_opposite_rescued": sum(r["after_opposite_passes"] for r in failures),
            "global_shift_rescued": sum(r["global_previous_passes"] or r["global_next_passes"] for r in failures),
            "any_counterfactual_rescued": sum(r["skip_reset_windows_passes"] or r["before_active_passes"]
                                               or r["after_opposite_passes"] or r["global_previous_passes"]
                                               or r["global_next_passes"] for r in failures)}


def official_report():
    rows = []
    for task in tasks():
        raw = (upstream(task["task_id"]) / "golden_tb.v").read_text()
        lines = raw.splitlines()
        # Select the scoring monitor following its comparator, not stimulus/reset diagnostic monitors.
        declaration = next(i for i, line in enumerate(lines) if "assign tb_match" in line)
        comparator = re.sub(r"\s+", "", lines[declaration])
        if not re.fullmatch(r"assigntb_match=\((\{[^}]+\})===\(\1\^\{[^}]+\}\^\1\)\);", comparator):
            raise ValueError(f"Unexpected official X-mask formula for {task['task_id']}")
        scoring = next(i for i in range(declaration + 1, len(lines)) if "always @" in lines[i])
        body = "\n".join(lines[scoring:])
        if "stats1.clocks++" not in body or "if (!tb_match)" not in body:
            raise ValueError(f"Unexpected official scoring monitor for {task['task_id']}")
        signature = re.search(r"always @\(([^)]*)\)", lines[scoring])[1]
        direct_reset_gate = not bool(re.search(r"stats1\.clocks\+\+;\s*if \(!tb_match\)", body))
        rows.append({**task, "official_comparator_line": declaration + 1,
                     "official_monitor_line": scoring + 1, "official_monitor_events": signature,
                     "official_comparator_semantics": "reference === (reference ^ dut ^ reference)",
                     "official_has_post_edge_delay": bool(re.search(r"#\s*\d|\$strobe", body)),
                     "official_reset_gate": direct_reset_gate,
                     "official_ref_x_wildcard": True,
                     "official_ref_z_is_wildcard": False,
                     "pilot_edge": public(task["task_id"])[1][3]})
    export("official_TB_comparison", rows)
    return {"task_count": len(rows), "monitor_events": dict(Counter(r["official_monitor_events"] for r in rows)),
            "post_edge_delay_count": sum(r["official_has_post_edge_delay"] for r in rows),
            "reset_gate_count": sum(r["official_reset_gate"] for r in rows)}


def migration_report(migration):
    results = []
    for cfg in ("all_O", "stimulus_O", "B-O", "O-B", "O-O"):
        rows = [r for r in migration if cfg == "all_O" or cfg == r["configuration"]
                or cfg == "stimulus_O" and r["configuration"].startswith("O-")]
        x, y = [r["G_gain_pp"] for r in rows], [r["H_gain_pp"] for r in rows]
        correlated = len(set(x)) > 1 and len(set(y)) > 1
        results.append({"configuration": cfg, "runs": len(rows), "mean_G_gain_pp": mean(x),
                        "mean_H_gain_pp": mean(y), "runs_with_G_gain": sum(a > 0 for a in x),
                        "runs_with_H_gain": sum(b > 0 for b in y),
                        "runs_with_both_gains": sum(a > 0 and b > 0 for a, b in zip(x, y, strict=True)),
                        "pearson_r": float(stats.pearsonr(x, y).statistic) if correlated else None,
                        "spearman_rho": float(stats.spearmanr(x, y).statistic) if correlated else None})
    export("G_to_H_correlations", results)
    return results


def never_exposed(mutants):
    groups = defaultdict(list)
    for row in mutants:
        groups[row["task_number"], row["task_id"], row["mutant"]].append(row)
    results, edit_diffs, phase_rows = [], [], []
    for (number, task, mutant), group in sorted(groups.items()):
        if any(r["final_exposed"] for r in group):
            continue
        source = upstream(task)
        base = (source / "golden_rtl.v").read_text()
        variant = (source / "official_mutants" / (mutant + ".v")).read_text()
        base_lines = [line.rstrip() for line in base.splitlines()]
        variant_lines = [line.rstrip() for line in variant.splitlines()]
        diff = "\n".join(unified_diff(base_lines, variant_lines, n=0,
                                     fromfile="golden", tofile=f"{task}/H{mutant}", lineterm=""))
        edit_diffs.append(diff)
        catalog = load(BASE / "guidance" / task / "catalog.json")
        rules = Counter(atom["rule"] for batch in catalog["groups"] for record in batch["candidates"]
                        if record["retained"] for atom in record["edits"])
        _, interface = public(task)
        phase_counts = Counter()
        for row in group:
            vector_file = BASE / "runs" / task / row["configuration"] / f"rep{row['repeat']}" / "final_vectors.json"
            bench = VectorReplay(interface, load(vector_file), all_edges=True)
            ref, _ = bench.trace(base)
            candidate, _ = bench.trace(variant)
            phases = {phase: len(differences(ref[i::3], candidate[i::3])) for i, phase in enumerate(PHASES)}
            if phases["after_active"]:
                raise ValueError(f"Extra-phase replay changed the active result for {task} H{mutant}")
            phase_counts.update({phase: int(bool(sites)) for phase, sites in phases.items()})
            phase_rows.append({**row, **{f"{s}_different_positions": n for s, n in phases.items()}})
        summary, comparison = MUTATION_NOTES[number, mutant]
        results.append({"task_number": number, "task": task, "mutant": "H" + mutant,
                        "runs": len(group), "mutation": summary, "difference_from_G": comparison,
                        "runs_with_known_phase_difference": dict(phase_counts),
                        "G_retained_catalog_rules": dict(sorted(rules.items()))})
    # Exact held-out RTL differences stay on the evaluation side.
    destination = BASE / "eval" / "postpilot"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "never_exposed_H.diff").write_text("\n\n".join(edit_diffs) + "\n")
    export("never_exposed_H_phases", phase_rows)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    plan = setup()
    jobs = [(entry, rep, seed, plan) for entry in tasks()
            for rep, seed in enumerate(plan["repeat_seeds"], 1)]
    columns = [[] for _ in range(7)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, block in enumerate(pool.map(lambda job: audit_block(*job), jobs), 1):
            for column, rows in zip(columns, block, strict=True):
                column.extend(rows)
            if i % 5 == 0:
                print(f"Verified {i}/{len(jobs)} task/seed blocks", flush=True)
    trials, pairs, agreements, failures, stages, mutants, migration = columns
    sample = random.Random(SAMPLE_SEED).sample(trials, 10)
    for name, rows in (("TB_initial_final", trials), ("pairwise_TB_differences", pairs),
                       ("golden_by_task_seed", agreements), ("draft_final_random_sample", sample),
                       ("checker_revisions", stages), ("H_exposure_per_mutant", mutants),
                       ("G_to_H_per_run", migration)):
        export(name, rows)
    export("false_positive_first_sites", [{k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                                           for k, v in row.items()} for row in failures])
    macro, paired = exposure_report(trials, plan)
    never = never_exposed(mutants)
    save(DEST / "never_exposed_H.json", never)
    summary = {"generation_calls_added": 0, "replayed_trials": len(trials), "random_sample_seed": SAMPLE_SEED,
               "flow": agreement_report(pairs, agreements, stages, plan), "exposure_macro": macro,
               "exposure_paired": paired, "false_positives": failure_report(failures, plan),
               "official": official_report(), "migration": migration_report(migration),
               "never_exposed_H_mutants": len(never)}
    save(DEST / "summary.json", summary)


if __name__ == "__main__":
    main()
