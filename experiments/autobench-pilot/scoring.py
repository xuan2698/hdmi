"""Isolated evaluation against the frozen reference assets."""

import json
from pathlib import Path

from simulate import RunError, differences, mismatches


def score_final(root, task_id, replay, expected):
    group = Path(root) / "eval" / task_id
    golden, _ = replay.trace((group / "golden_rtl.v").read_text())
    error_rows = mismatches(expected, golden)
    gold_errors = [i + 1 for i, row in enumerate(error_rows) if row]
    official = sorted((group / "official_mutants").glob("*.v"))
    cases = []
    for item in official:
        try:
            mutant, _ = replay.trace(item.read_text())
        except (RunError, ValueError) as exc:
            cases.append({"id": item.stem, "verdict": "simulation_error", "reason": str(exc)})
            continue
        check = mismatches(expected, mutant)
        observed = differences(golden, mutant)
        error_cycles = [i + 1 for i, row in enumerate(check) if row]
        new_errors = sum(len(row - gold) for row, gold in zip(check, error_rows, strict=True))
        verdict = ("detected" if error_cycles else
                   "checker_missed" if observed else "not_exposed")
        cases.append({
            "id": item.stem, "verdict": verdict, "mismatch_cycles": error_cycles,
            "mutant_only_mismatches": new_errors,
            "output_difference_cycles": sorted({i + 1 for i, *_ in observed}),
        })
    proxies = json.loads((group / "proxy_checks" / "results.json").read_text())
    return {
        "golden_pass": not gold_errors, "golden_error_cycles": gold_errors,
        "H_total": len(official), "H_detected": sum(c["verdict"] == "detected" for c in cases),
        "H_new_error": sum(bool(c.get("mutant_only_mismatches")) for c in cases),
        "H_not_exposed": sum(c["verdict"] == "not_exposed" for c in cases),
        "H_checker_missed": sum(c["verdict"] == "checker_missed" for c in cases),
        "H_simulation_errors": sum(c["verdict"] == "simulation_error" for c in cases),
        "H_cases": cases,
        "proxy_verdicts": {key: val["verdict"] for key, val in proxies.items()},
    }
