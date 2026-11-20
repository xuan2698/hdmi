from collections import Counter

from mutations import candidate, diagnostic
from simulate import RunError, differences, known_int, mismatches


def stimulus_feedback(records, proxy, replay, misses, method):
    lines, details = [], {}
    for record in records:
        tag = record["id"]
        if tag not in misses:
            continue
        mutation = candidate(record)
        block = [mutation.feedback(tag)]
        if method == "O":
            try:
                finding = diagnostic(record, proxy, replay)
            except (RunError, KeyError, ValueError) as exc:
                finding = {"label": "诊断未完成", "cause": str(exc).splitlines()[0]}
            details[tag] = finding
            line = finding["label"]
            if "operands_binary" in finding:
                operands = ", ".join(f"{name}={values}" for name, values in
                                     finding["operands_binary"].items())
                line += f"（二进制操作数 {operands}）"
            if "first_infected" in finding:
                line += f"（第 {finding['first_infected']} 周期首次感染）"
            block.append(line)
            intervals = finding.get("intervals", [])
            if intervals:
                a = intervals[0]
                equal = a["equal_again"] if a["equal_again"] is not None else "未恢复"
                block.append(f"{a['signal']}: 第 {a['first']} 周期出现 → 第 {equal} 周期恢复，{a['cause']}")
            elif finding.get("cause"):
                block.append(finding["cause"])
        lines.extend(block)
    if not lines:
        return "", details
    return "Revise the stimuli to expose these still-hidden mutations under the specification.\n" + "\n".join(lines), details


def checker_feedback(problem, vectors, expected, proxies, mutants, method):
    checks = [mismatches(expected, trace) for trace in proxies]
    baseline = []
    for i, row in enumerate(expected):
        for name, prediction in row.items():
            if prediction is None:
                continue
            observations = [known_int(trace[i][name]) for trace in proxies]
            known = [value for value in observations if value is not None]
            if not known:
                continue
            vote, count = Counter(known).most_common(1)[0]
            if count >= 2 and vote != prediction:
                baseline.append({"cycle": i + 1, "signal": name, "input": vectors[i],
                                 "predicted": prediction, "R1_R2_R3": observations,
                                 "pass_by_proxy": [name not in mode[i] for mode in checks]})
    lines, additions = [], []
    if baseline:
        lines.append("Re-derive the reference model using the specification. Multiple proxies "
                     "disagree at these scenarios. Treat proxy votes as hypotheses.")
        lines.extend(str(row) for row in baseline[:8])
    if method == "O":
        for tag, trace in mutants.items():
            mode = mismatches(expected, trace)
            for i, name, a, b in differences(proxies[0], trace):
                if expected[i][name] is None:
                    continue
                proxy_fails = name in checks[0][i]
                mutant_fails = name in mode[i]
                if proxy_fails != mutant_fails:
                    continue
                example = {"mutant": tag, "cycle": i + 1, "signal": name, "input": vectors[i],
                           "R1_binary": a, "mutation_binary": b,
                           "both": "fail" if proxy_fails else "pass"}
                if proxy_fails:
                    example.update({
                        "R2_binary": proxies[1][i][name], "R3_binary": proxies[2][i][name],
                        "spec": problem["spec"],
                    })
                additions.append(example)
                break
        if additions:
            lines.append("Additional observations at exposed mutation sites. When both pass, add "
                         "the missing check if the spec determines the value. When both fail, "
                         "re-derive the expected value from the quoted spec. Treat all proxy "
                         "observations as evidence, and skip unspecified behaviors.")
            lines.extend(str(row) for row in additions)
    return "\n".join(lines), {"baseline": baseline, "additional": additions}
