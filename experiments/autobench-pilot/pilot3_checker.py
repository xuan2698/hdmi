from collections import Counter
from pathlib import Path
import re

from pilot2_checker import feedback as baseline_feedback
from pilot3_inputs import BASE
from simulate import RunError, differences, known_int, mismatches

FAMILIES = ("gpt4o", "gpt4omini", "claude35sonnet")


def bank(task, bench, width, method):
    names = [f"{family}_{i}" for family in (FAMILIES if method == "O" else FAMILIES[:1])
             for i in range(1, 4)]
    unavailable, traces = {}, []
    unknown = {port: "x" * bits for port, bits in width.items()}
    for name in names:
        source = BASE / "proxies" / task / f"{name}.v"
        try:
            traces.append(bench.trace(source.read_text())[0])
        except (RunError, ValueError) as exc:
            unavailable[name] = str(exc)
            traces.append([unknown] * len(bench.vectors))
    return traces, unavailable


def clause(task, spec, signal, row, index, vectors):
    if task == "2014_q3c":
        state = f"{row['y']:03b}"
        found = next((text.strip() for text in spec.splitlines() if
                      re.match(rf"\s*//\s*{state}\s*\|", text)), None)
        if found:
            return found
    if task == "edgecapture":
        if row["reset"]:
            return "active high synchronous reset"
        if index and vectors[index - 1]["in"] & ~row["in"]:
            return "For each bit in a 32-bit vector, capture when the input signal changes from 1 in one clock cycle to 0 the next."
        return '"Capture" means that the output will remain 1 until the register is reset (active high synchronous reset).'
    if task == "review2015_fsmseq":
        return ("Reset is active high synchronous." if row["reset"] else
                "When the sequence is found, it should set start_shifting to 1, forever, until reset.")
    if re.search(r"(//.*\btime\b|simulation waveforms)", spec, re.I):
        return "Public waveform table for " + signal + " (attached in the specification above)."
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", spec) if s.strip()
                 and not s.strip().startswith(("//", "module"))]
    if any(value and "reset" in name.lower() and not name.lower().endswith(("resetn", "reset_n"))
           or not value and name.lower().endswith(("resetn", "reset_n"))
           for name, value in row.items() if isinstance(value, int)):
        reset = next((s for s in sentences if "reset" in s.lower()), None)
        if reset:
            return reset
    explicit = [s for s in sentences if re.search(rf"(?<!\w){re.escape(signal)}(?!\w)", s, re.I)]
    return (explicit or sentences or [spec])[0]


def issue_feedback(task, spec, vectors, expected, proxies, anchor, mutants, issued, threshold):
    issues = {}
    anchor_misses = mismatches(expected, anchor)
    pair_failures = set()
    for trace in mutants.values():
        wrong = mismatches(expected, trace)
        pair_failures.update((cycle, signal) for cycle, signal, _, _ in differences(anchor, trace)
                             if signal in anchor_misses[cycle] and signal in wrong[cycle])
    bug_findings = set()
    for cycle, row in enumerate(expected):
        for signal, prediction in row.items():
            values = [known_int(trace[cycle][signal]) for trace in proxies]
            votes = Counter(value for value in values if value is not None)
            if not votes:
                continue
            favorite, size = votes.most_common(1)[0]
            accepted = size >= threshold
            if favorite == prediction and accepted:
                if (cycle, signal) in pair_failures:
                    bug_findings.add((signal, clause(task, spec, signal, vectors[cycle], cycle, vectors)))
                continue
            if not any(value != prediction for value in votes):
                continue
            quote = clause(task, spec, signal, vectors[cycle], cycle, vectors)
            key = signal, quote
            if key in issued:
                continue
            record = {"signal": signal, "clause": quote, "cycle": cycle + 1,
                      "expected": prediction, "votes": dict(votes), "available": sum(votes.values()),
                      "accepted": accepted, "vote_count": size, "consensus_value": favorite}
            if key not in issues or (accepted, size) > (issues[key]["accepted"], issues[key]["vote_count"]):
                issues[key] = record
    records = list(issues.values())
    for item in records:
        issued.add((item["signal"], item["clause"]))
    lines = []
    if records:
        lines.append("Review each independent signal/spec issue below. Change the checker only if warranted by the spec.")
    for item in records:
        lines.append(f"{item['signal']} | {item['clause']}")
        if item["accepted"]:
            lines.append(f"Cycle {item['cycle']}, checker {item['expected']}, "
                         f"{item['vote_count']}/9 proxies agree on {item['consensus_value']}.")
    return "\n".join(lines), {"issues": records, "accepted": sum(x["accepted"] for x in records),
                              "not_accepted": sum(not x["accepted"] for x in records),
                              "R1_bug_points": [list(x) for x in sorted(bug_findings)]}


def feedback(task, problem, vectors, expected, proxies, anchor, mutants, method, issued, plan):
    if method == "B":
        text, baseline = baseline_feedback(problem, vectors, expected, proxies, {}, "B")
        return text, {"baseline": baseline}
    return issue_feedback(task, problem["spec"], vectors, expected, proxies, anchor, mutants, issued,
                          plan["minimum_proxy_votes"])
