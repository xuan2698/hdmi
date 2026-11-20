from collections import Counter

from simulate import differences, known_int, mismatches


CASE_NAMES = ("r1_bug", "both_proxies_disagree_with_checker", "proxies_disagree_with_each_other")


def feedback(problem, vectors, expected, proxies, mutants, method):
    modes = [mismatches(expected, trace) for trace in proxies]
    base = []
    for i, row in enumerate(expected):
        for output, guess in row.items():
            if guess is None:
                continue
            votes = [known_int(trace[i][output]) for trace in proxies]
            known = [v for v in votes if v is not None]
            if not known:
                continue
            prediction, count = Counter(known).most_common(1)[0]
            if count > 1 and prediction != guess:
                base.append({"cycle": i + 1, "signal": output, "input": vectors[i],
                             "expected": guess, "proxy_values": votes})
    counters = dict.fromkeys(CASE_NAMES, 0)
    details = {case: [] for case in CASE_NAMES}
    ambiguous_sites = set()
    if method == "O":
        for label, trace in mutants.items():
            mode = mismatches(expected, trace)
            for i, output, original, changed in differences(proxies[0], trace):
                guess = expected[i][output]
                if guess is None or output not in modes[0][i] or output not in mode[i]:
                    continue
                r2, r3 = (known_int(proxy[i][output]) for proxy in proxies[1:])
                if r2 is None or r3 is None:
                    continue
                item = {"cycle": i + 1, "signal": output, "mutant": label, "expected": guess,
                        "R1_binary": original, "mutant_binary": changed, "R2": r2, "R3": r3}
                if r2 == r3 == guess:
                    case = "r1_bug"
                elif r2 == r3:
                    case = "both_proxies_disagree_with_checker"
                else:
                    case = "proxies_disagree_with_each_other"
                    ambiguous_sites.add((i + 1, output))
                counters[case] += 1
                if len(details[case]) < 12:
                    details[case].append(item)
    base = [row for row in base if (row["cycle"], row["signal"]) not in ambiguous_sites]
    text = []
    if base:
        text.append("Two proxies disagree with the checker in these examples. Re-derive from the public specification.")
        text.extend(str(row) for row in base[:6])
    if details["both_proxies_disagree_with_checker"]:
        text += ["Re-derive these cases using this specification:", problem["spec"]]
        text.extend(str(item) for item in details["both_proxies_disagree_with_checker"][:6])
    if details["proxies_disagree_with_each_other"]:
        text += ["Independently review the expected behavior from this specification:", problem["spec"]]
    if text:
        text.append("Only change the checker if the specification justifies it.")
    return "\n".join(text), {"counts": counters, "diagnostics": details, "baseline": base[:12]}
