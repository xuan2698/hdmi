"""Evaluate archived checkers and diagnostic artifacts on frozen RTL and H."""

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data import PLAN, case_path, checker_inputs, check_rows, interface, load, roster, save, vectors
from pilot2_sim import VectorReplay
from pilot3_evaluation import archive, upstream
from simulate import RunError
from cvdp import confirmed_h, gold_sources, replay_pair


def values(rows, masks, widths):
    return [{n: f"{row[n]:0{widths[n]}b}" for n in mask}
            for row, mask in zip(rows, masks, strict=True)]


def match_bits(expected, observed, mask):
    return all(m not in "01" or a == b for m, a, b in zip(mask, expected, observed, strict=True))


def differing(expected, observed, masks):
    return [tuple(n for n in mask if not match_bits(want[n], got[n], mask[n]))
            for want, got, mask in zip(expected, observed, masks, strict=True)]


def voting(models, out, rows):
    guesses = [check_rows(code, out, rows) for code in models]
    return [{n: Counter(row[n] for row in options).most_common(1)[0][0] for n in out}
            for options in zip(*guesses, strict=True)]


def model_predictions(item, out, rows):
    if item["status"] != "ready":
        return None
    if item.get("model"):
        return check_rows((ROOT / item["model"]).read_text(), out, rows)
    return voting([(ROOT / path).read_text() for path in item["members"]], out, rows)


class Evaluation:
    def __init__(self, group, task, seed, gold):
        self.group, self.task, self.seed = group, task, seed
        self.home = case_path(group, task, seed)
        self.ports = interface(group, task)
        self.out = self.ports["output"]
        self.fixed = vectors(group, task, seed, self.ports)
        self.cache = {}
        if group == "A":
            source = upstream(task)
            self.golden_rtl = (source / "golden_rtl.v").read_text()
            registry = load(archive(task) / "prescreen.json")
            self.held = {row["id"]: source / "official_mutants" / (row["id"] + ".v")
                         for row in registry["cases"] if row["status"] == "kept"}
            if len(self.held) != registry["kept"]:
                raise ValueError("AutoBench H registry changed")
        else:
            self.golden_rtl = gold[task]
            self.held = confirmed_h(task)

    def traces(self, stimulus, include_h=False):
        key = hashlib.sha256(json.dumps(stimulus, separators=(",", ":")).encode()).hexdigest()
        if key not in self.cache:
            if self.group == "A":
                port = self.ports
                bench = VectorReplay((port["input"], self.out, port["clock"], port["edge"]), stimulus)
                golden = bench.trace(self.golden_rtl)[0]
                replay = lambda source: bench.trace(source)[0]
            else:
                golden = replay_pair(self.golden_rtl, self.golden_rtl, self.ports, stimulus)[0]
                replay = lambda source: replay_pair(self.golden_rtl, source, self.ports, stimulus)[1]
            self.cache[key] = (golden, {}, replay)
        golden, held, replay = self.cache[key]
        if include_h and not held:
            for label, path in self.held.items():
                try:
                    held[label] = replay(path.read_text())
                except (ValueError, RuntimeError):
                    held[label] = None
        return golden, held

    def predicted(self, item, stimulus):
        return model_predictions(item, self.out, checker_inputs(self.group, stimulus))

    def score_mode(self, item, stimulus):
        result = {"golden_pass": None, "golden_failed_samples": None, "H_total": len(self.held),
                  "H_detected": 0, "H_simulation_errors": 0, "first_mismatch": None, "mutants": []}
        try:
            predictions = self.predicted(item, stimulus)
        except (ValueError, RunError, subprocess.TimeoutExpired) as error:
            result["execution_error"] = str(error)
            return result
        if predictions is None:
            return result
        gold, held = self.traces(stimulus, True)
        expect = values(predictions, gold, self.out)
        failed = differing(expect, gold, gold)
        passed = not any(failed)
        first = next((i for i, row in enumerate(failed) if row), None)
        result.update(golden_pass=passed, golden_failed_samples=sum(bool(row) for row in failed))
        if first is not None:
            result["first_mismatch"] = {"sample": first + 1, "golden": gold[first], "expected": predictions[first]}
        for label, observed in held.items():
            check = any(differing(expect, observed, gold)) if observed is not None else None
            hit = passed and check is True
            result["H_simulation_errors"] += check is None
            result["H_detected"] += hit
            result["mutants"].append({"id": label, "reported": check, "detected": hit})
        return result

    def diagnostic(self, source, scenes):
        out, examples = [], []
        for scene in scenes:
            rows = scene["vectors"]
            gold, _ = self.traces(rows)
            try:
                rm = check_rows(source, self.out, checker_inputs(self.group, rows))
            except (RunError, subprocess.TimeoutExpired) as error:
                out.append({"scene": scene["id"], "error": str(error)})
                continue
            tb = scene["expected"]
            rf = differing(values(rm, gold, self.out), gold, gold)
            tf = differing(values(tb, gold, self.out), gold, gold)
            separate = [a != b for a, b in zip(rm, tb, strict=True)]
            known = [any(bit in "01" for v in row.values() for bit in v) for row in gold]
            common = [bool(k and not disagree and a and b)
                      for k, disagree, a, b in zip(known, separate, rf, tf, strict=True)]
            stride = 2 if self.group == "B" else 1
            out.append({"scene": scene["id"], "compared_cycles": len(rows), "compared_samples": len(rm),
                        "disagreement_cycles": sum(any(separate[i:i + stride]) for i in range(0, len(separate), stride)),
                        "disagreement_samples": sum(separate), "known_samples": sum(known),
                        "TB_wrong_samples": sum(bool(f) for f in tf),
                        "RM_wrong_samples": sum(bool(f) for f in rf), "common_mode_samples": sum(common)})
            if (index := next((i for i, same in enumerate(common) if same), None)) is not None:
                examples.append({"scene": scene["id"], "sample": index + 1, "cycle": index // stride + 1,
                                 "quote": scene["spec_quote"], "input_history": checker_inputs(self.group, rows)[:index + 1],
                                 "RM": rm[index], "TB": tb[index], "golden": gold[index],
                                 "wrong_outputs": list(rf[index])})
        return {"scenes": out, "common_examples": examples}

    def judgments(self, route, scenes, limit):
        evaluations = []
        for count in range(1, limit + 1):
            folder = self.home / route / f"round{count}"
            initial = load(folder / "disagreements.json")
            result = load(folder / "outcome.json")
            decisions = {row["id"]: row for row in result["decisions"]}
            scenes_by_name = {row["id"]: row for row in scenes}
            changed_tb = {row["id"]: row for row in result["TB"]}
            revised = {}
            for pt in initial["selected"]:
                decision = decisions[pt["id"]]
                label = decision["label"]
                scene = scenes_by_name[pt["scene"]]
                if pt["scene"] not in revised:
                    revised[pt["scene"]] = check_rows(result["RM"], self.out,
                                                       checker_inputs(self.group, scene["vectors"]))
                gold, _ = self.traces(scene["vectors"])
                pos, n = pt["sample"] - 1, pt["output"]
                bits = gold[pos][n]
                def consistent(value):
                    return match_bits(f"{value:0{len(bits)}b}", bits, bits)
                rm_ok, tb_ok = consistent(pt["RM"]), consistent(pt["TB"])
                truth = ("TB" if rm_ok else "RM") if rm_ok != tb_ok else ("ambiguous" if rm_ok else "both_wrong")
                r_after = revised[pt["scene"]][pos][n]
                t_after = changed_tb[pt["scene"]]["expected"][pos][n]
                fixed = {"RM": r_after, "TB": t_after}.get(label)
                evaluations.append({**pt, "route": route, "round": count, "verdict": label,
                                    "spec_quote": decision.get("spec_quote"), "actual": truth,
                                    "correct": label == truth, "golden": bits, "revised_RM": r_after,
                                    "revised_TB": t_after, "repair_success": None if fixed is None or not any(
                                        c in "01" for c in bits) else consistent(fixed)})
            scenes = result["TB"]
        return evaluations

    def run(self, phase):
        source = self.home / "tb/value.json"
        scenes = load(source) if source.is_file() else None
        appended = self.fixed + [row for scene in scenes for row in scene["vectors"]] if scenes else None
        results = []
        for arm in PLAN["configs"]:
            item = load(self.home / "configs" / arm / "result.json")
            row = {**item, "primary": self.score_mode(item, self.fixed),
                   "secondary": self.score_mode(item, appended) if appended else None}
            if item.get("route") and item["status"] == "ready":
                src = (ROOT / item["model"]).read_text()
                row["final_diagnostic"] = self.diagnostic(src, item["scenes"])
                row["decisions"] = self.judgments(item["route"], scenes, item["last_round"])
            results.append(row)
        stages = {}
        paths = {"initial": self.home / "rm/model.py", "reviewed": self.home / "configs/Ours-noTB/model.py",
                 "final": self.home / "configs/Ours/model.py"}
        for name, path in paths.items():
            if path.is_file():
                signature = {"status": "ready", "model": str(path.relative_to(ROOT))}
                # Fixed-stimulus false positives are scored with the same masks as primary.
                fixed = self.score_mode(signature, self.fixed)
                stages[name] = {"golden_pass": fixed["golden_pass"],
                                "golden_failed_samples": fixed["golden_failed_samples"],
                                "directed": self.diagnostic(path.read_text(), scenes) if scenes else None}
        result = {"group": self.group, "task": self.task, "seed": self.seed,
                  "fixed_cycles": len(self.fixed), "stages": stages, "outcomes": results}
        save(ROOT / "eval" / phase / self.group / self.task / f"{self.seed}.json", result)
        print(self.group, self.task, self.seed, "evaluated", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase", choices=("pilot", "full"))
    p.add_argument("dataset", type=Path)
    p.add_argument("--workers", type=int, default=5)
    args = p.parse_args()
    generation = load(ROOT / "reports" / f"{args.phase}_generation.json")
    cases = roster(args.phase)
    if generation["configs"] != len(cases) * len(PLAN["configs"]):
        raise SystemExit("Freeze the generation matrix before scoring H")
    refs = gold_sources(args.dataset)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda case: Evaluation(*case, refs).run(args.phase), cases))


if __name__ == "__main__":
    main()
