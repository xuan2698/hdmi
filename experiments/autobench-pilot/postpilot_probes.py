"""Evaluation-only dynamic probes for the archived v2 evidence."""

from collections import Counter
from dataclasses import asdict
from difflib import unified_diff
import re

from mutations import Candidate, candidate, diagnostic
from pilot2_sim import VectorReplay
from simulate import RunError, differences


H_SITES = {
    ("2014_q3c", "03"): ("case", "default: Y0 = 1'bx;", "default: Y0 = 1'bz;"),
    ("2014_q3c", "10"): ("case", "default: Y0 = 1'bx;", "default: Y0 = 0;"),
    ("count_clock", "05"): ("compare", "ss[7:0]==8'h59,", "ss[7:0]==8'h58,"),
    ("ece241_2014_q5a", "10"): (
        "async", "always @(posedge clk, posedge areset) begin", "always @(posedge clk) begin",
    ),
}


def find_line(source, needle):
    rows = [(n, line) for n, line in enumerate(source.splitlines(), 1) if needle in line]
    if len(rows) != 1:
        raise ValueError(f"Expected a unique source anchor: {needle}")
    return rows[0]


def insert_once(source, needle, changed):
    find_line(source, needle)
    return source.replace(needle, changed, 1)


def label(reached, infected):
    return "未到达" if not reached else "未感染" if not infected else "未传播"


def h_diagnosis(task, mutant, golden, changed, interface, trials):
    kind, old, new = H_SITES[(task, mutant)]
    line, before = find_line(golden, old)
    find_line(changed, new)
    if kind == "case":
        original = old.split("=", 1)[1].strip(" ;")
        alternate = new.split("=", 1)[1].strip(" ;")
        guard = "({y[2:0], x} >= 4'hA)"
        marker = f'$display("PROBE %b %b %b %b", 1\'({original}), 1\'({alternate}), y, x);'
        annotated = insert_once(
            golden, old, f"default: begin {marker} Y0 = {original}; end"
        )
        cause = "Y0 未定义时发生四态输出差异，评分只比较 golden 已知位。"
    elif kind == "compare":
        original, alternate = old.rstrip(","), new.rstrip(",")
        guard = "1'b1"
        marker = (f'always @(posedge clk) $display("PROBE %b %b %b %b %b", '
                  f'{original}, {alternate}, ss, reset, ena);')
        annotated = insert_once(golden, "endmodule", marker + "\nendmodule")
        cause = "检查秒计数比较器的阈值，并区分采样后的值与时钟沿更新前的值。"
    else:
        original, alternate, guard = "posedge areset", "posedge clk only", "1'b1"
        marker = '$display("PROBE %b %b %b", clk, areset, state);'
        annotated = insert_once(golden, old, f"{old}\n\t\t{marker}")
        cause = "异步复位的效应可出现在主评分采样前，同步变异体最迟在时钟沿复位。"

    mutation = Candidate("clock_edge" if kind == "async" else "evaluation_probe", line,
                         before, before.replace(old, new), original, alternate, guard, "", 1)
    results = []
    for trial, stimuli in trials:
        bench = VectorReplay(interface, stimuli)
        full = VectorReplay(interface, stimuli, all_edges=True)
        ref, _ = bench.trace(golden)
        obs, _ = bench.trace(changed)
        if differences(ref, obs):
            raise ValueError(f"{task}/{mutant} has a scored exposure")
        events = []
        instrumented, _ = full.trace(annotated, probes=events)
        full_ref, _ = full.trace(golden)
        full_obs, _ = full.trace(changed)
        if full_ref != instrumented or full_ref[1::3] != ref or full_obs[1::3] != obs:
            raise ValueError(f"Probe or sampling changed observable behavior for {task}/{mutant}")
        try:
            old_result = diagnostic(asdict(mutation), golden, bench)["label"]
        except (RunError, KeyError, ValueError) as exc:
            old_result = f"探针无法解释：{str(exc).splitlines()[0]}"
        if kind == "async":
            executed = [row for row in events if row[:2] == ["0", "1"]]
            infected = [row for row in executed if row[2] != "00"]
            witnessed = [{"clock": a, "reset": b, "state_before": c} for a, b, c in infected[:3]]
        else:
            executed = events
            infected = [row for row in executed if row[0] != row[1]]
            witnessed = [row for row in infected[:3]]
        thresholds = None
        if kind == "compare":
            thresholds = sum(row["ss"] in ("01011000", "01011001") for row in full_ref)
            if thresholds and not infected:
                raise ValueError("Comparator changed outside the instrumented consumer edge")
        raw = [sum(a != b for a, b in zip(full_ref[i::3], full_obs[i::3], strict=True))
               for i in range(3)]
        known = [len(differences(full_ref[i::3], full_obs[i::3])) for i in range(3)]
        results.append({
            "configuration": trial["config"], "repeat": trial["repeat"],
            "label": label(len(executed), len(infected)), "legacy_probe_label": old_result,
            "executed": len(executed), "infected": len(infected), "probe_examples": witnessed,
            "raw_different_cycles_pre_active_opposite": raw,
            "known_difference_positions_pre_active_opposite": known,
            "threshold_samples": thresholds,
        })
    return {
        "task": task, "mutant": mutant, "site_line": line, "original": old, "changed": new,
        "classification": label(sum(r["executed"] for r in results), sum(r["infected"] for r in results)),
        "raw_output_difference": any(any(row["raw_different_cycles_pre_active_opposite"]) for row in results),
        "cause_scope": cause, "runs": results,
        "patch": list(unified_diff(golden.splitlines(), changed.splitlines(),
                                  fromfile="golden", tofile=mutant, lineterm="")),
    }


def exact_g_check(source, atom, interface, stimuli):
    if atom["lhs"] != "current_state" or "current_state <= STATE_IDLE;" not in atom["before"]:
        raise ValueError("Unsupported audited site. Add an explicit instrumentation anchor.")
    width = re.search(r"typedef enum (?:logic|reg)\s*\[(\d+):(\d+)\]", source)
    bits = abs(int(width[1]) - int(width[2])) + 1
    emit = f'$display("PROBE %b %b", {bits}\'({atom["orig"]}), {bits}\'({atom["changed"]}));'
    before = atom["before"]
    marked = insert_once(source, before, emit + "\n" + before)
    replay = VectorReplay(interface, stimuli, proxy_compat=True)
    raw, _ = replay.trace(source)
    observed, _ = replay.trace(candidate(atom).rtl(source))
    witnesses = []
    trace, _ = replay.trace(marked, probes=witnesses)
    if trace != raw:
        raise ValueError("Explicit reach probe changed R1 output")
    if differences(raw, observed):
        raise ValueError("Audited G mutant has a scored difference this round")
    pairs = Counter(f"{old}→{new}" for old, new in witnesses)
    changed_count = sum(a != b for a, b in witnesses)
    return {"exact_label": label(len(witnesses), changed_count), "executions": len(witnesses),
            "infected": changed_count, "value_pairs_binary": dict(pairs), "probe_width": bits}
