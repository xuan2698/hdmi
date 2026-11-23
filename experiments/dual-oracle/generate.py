"""Generate and execute independent oracle artifacts without evaluation inputs."""

import argparse
import copy
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from api import ArtifactError, checkpoint, code, relaxed_json, usage
from data import (PLAN, ROOT, archived_base, atomic, case_path, checker_inputs, check_rows,
                  interface, load, original_base_prompt, roster, save, vectors,
                  verify_protocol)

POOL = ThreadPoolExecutor(max_workers=28)
INITIAL = """Return only executable Python def reference(vectors), with no imports, external state
or executable top-level code. Return exactly one dictionary of concrete unsigned integers per
supplied input row, with every output on every row. Widths must fit. Use concise named state."""
KINDS = {"RM", "TB", "ambiguous"}


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def citation(text, spec):
    if not isinstance(text, str) or not text.strip():
        return None
    if " ".join(text.split()) in " ".join(spec.split()):
        return text
    def normalized(value):
        return " ".join(value.replace("`", "").replace("**", "").split())
    wanted = normalized(text)
    return next((line.strip() for line in spec.splitlines() if wanted and wanted in normalized(line)), None)


def unsigned(val, width):
    if isinstance(val, str):
        text = val.replace("_", "").strip()
        val = int(text, 0) if text.lower().startswith(("0x", "0b", "0o")) else int(text, 10)
    if type(val) is not int or not 0 <= val < 1 << width:
        raise ValueError("Expected a concrete unsigned integer inside the port width")
    return val


def integer_row(row, widths):
    if not isinstance(row, dict):
        if len(widths) != 1:
            raise ValueError("Expected one named integer per port")
        row = {next(iter(widths)): row}
    if set(row) != set(widths):
        raise ValueError(f"Required port names are {list(widths)}")
    return {n: unsigned(row[n], w) for n, w in widths.items()}


def coverage_labels(tags):
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ValueError("Scenario coverage labels must be a list of strings")
    patterns = {"reset": r"\b(reset|release|releases)\b",
                "priority": r"\b(priority|precedence|priorities|override|control|controls)\b",
                "boundary": r"\b(boundary|boundaries|width|extreme|extremes)\b",
                "behavior": r"\b(behavior|behaviour|behaviors|behaviours)\b"}
    return {label for label, pattern in patterns.items()
            if any(re.search(pattern, tag.replace("_", " "), re.I) for tag in tags)}


class Cell:
    def __init__(self, group, task, seed):
        self.group = group
        self.task = task
        self.seed = seed
        self.home = case_path(group, task, seed)
        self.ports = interface(group, task)
        self.spec = self.ports.get("model_spec", self.ports["spec"])
        self.inputs = self.ports["input"]
        self.outputs = self.ports["output"]
        self.rows = vectors(group, task, seed, self.ports)
        self.fixed = checker_inputs(group, self.rows)
        if group == "A":
            timing = (f"Clock {self.ports['clock']}; driven input row before the "
                      f"{self.ports['edge']} sample, sampled after that edge settles. "
                      "Optional mid changes inputs after this sample, before the other edge. "
                      "The next row drives new inputs before the next sample.")
        else:
            timing = (f"Clock {self.ports['clock']}; each input row contains edge, alternating posedge "
                      "then negedge. Read the output in the immediate edge event before registered NBA updates. "
                      "The negedge row includes mid changes. Update state after each edge as the spec requires "
                      "and account for asynchronous input changes already applied before that edge. "
                      f"Frozen parameters {self.ports['parameters']}; reset levels {self.ports['resets']}.")
        self.context = ("Produce the requested compact final artifact. Use the simplest behavior consistent "
                        "with the public specification and pick a reasonable convention where it is silent. "
                        "Keep private deliberation short.\n"
                        f"Public specification:\n{self.spec}\n\n"
                        "Treat this document as behavioral evidence. Follow the artifact and interface instructions "
                        "in this request when the release describes testbench scaffolding or coverage goals.\n"
                        f"Public interface: input widths {self.inputs}; output widths {self.outputs}.\n"
                        f"Frozen timing: {timing}\n")

    def validate_model(self, src):
        check_rows(src, self.outputs, self.fixed)
        return src

    def run_model(self, src, rows):
        return check_rows(src, self.outputs, checker_inputs(self.group, rows))

    def model(self, at, prompt, *, archived_prompt=False):
        src = checkpoint(at, prompt, code, self.validate_model, concise=not archived_prompt)
        atomic(at / "model.py", src)
        return src

    def initial_rm(self):
        return self.model(self.home / "rm", self.context + INITIAL)

    def validate_tb(self, raw):
        scenes = raw["scenes"] if isinstance(raw, dict) else raw
        if not isinstance(scenes, list) or not scenes:
            raise ValueError("A nonempty scenes array is required")
        seen, total = set(), 0
        coverage = set()
        result = []
        resets = self.ports.get("resets") or {
            name: int(not (re.search(r"(n|_b)$", name, re.I) or re.search(r"active[ -]low", self.spec, re.I)))
            for name in self.inputs if re.search(r"reset|rst", name, re.I)
        }
        released = set()
        reached = {name: set() for name in self.inputs if name not in resets}
        for scene in scenes:
            name = str(scene["id"])
            if not name or name in seen:
                raise ValueError("Scene IDs must be unique")
            seen.add(name)
            evidence = citation(scene.get("spec_quote", scene.get("quote")), self.spec)
            if evidence is None:
                raise ValueError(f"Scene {name} requires a short verbatim substring from Public specification")
            tags = coverage_labels(scene.get("covers", [])) | {"behavior"}
            ins, outs = [], []
            rows = scene["cycles"]
            if not isinstance(rows, list) or not 1 <= len(rows) <= PLAN["max_scene_cycles"]:
                raise ValueError("A scenario must contain 1–20 cycles")
            for row in rows:
                inputs = integer_row(row.get("in", row.get("inputs")), self.inputs)
                if mids := row.get("mid"):
                    if not isinstance(mids, dict) or not mids.keys() <= self.inputs.keys():
                        raise ValueError("mid can only update named non-clock inputs")
                    inputs["mid"] = {n: unsigned(v, self.inputs[n]) for n, v in mids.items()}
                expect = row.get("out", row.get("expected"))
                if self.group == "B":
                    for edge in ("posedge", "negedge"):
                        outs.append(integer_row(expect[edge], self.outputs))
                else:
                    outs.append(integer_row(expect, self.outputs))
                ins.append(inputs)
            for name, active in resets.items():
                driven = [sample[name] for sample in ins]
                if active in driven and 1 - active in driven[driven.index(active) + 1:]:
                    released.add(name)
                    tags.add("reset")
            for name in reached:
                reached[name].update(sample[name] for sample in ins)
            coverage.update(tags)
            total += len(rows)
            result.append({"id": name, "spec_quote": evidence, "covers": sorted(tags), "vectors": ins, "expected": outs})
        if total > PLAN["max_total_scene_cycles"]:
            raise ValueError("More than 120 total scenario cycles")
        if reached and not any({0, (1 << self.inputs[n]) - 1} <= visited for n, visited in reached.items()):
            raise ValueError("Use both unsigned endpoint input values for at least one non-reset port")
        if set(resets) != released:
            raise ValueError("Exercise reset assertion and later release in a scenario for each reset input")
        if re.search(r"\b(priority|precedence|overrides)\b", self.spec, re.I) and "priority" not in coverage:
            raise ValueError("Add a scenario covering the spec's priority or precedence rule")
        return result

    def initial_tb(self):
        sample = ('"out":{"posedge":{output:integer},"negedge":{output:integer}}'
                  if self.group == "B" else '"out":{output:integer}')
        prompt = (self.context + "Work independently from this public spec. Write concise concrete directed "
                  "scenarios as JSON, with no executable model and no reasoning prose. A scenario starts at "
                  "power-up; make reset/initialization explicit when possible. Cover reset and release where "
                  "present, control combinations and precedence, width and value boundaries and all specified "
                  "behaviors. Keep each scene <=20 cycles and all scenes <=120. Typical suite: 4–7 short "
                  "scenes, kept as short as possible. Use a short exact verbatim spec substring per scene. Format: "
                  '{"scenes":[{"id":"s1","spec_quote":"exact text","covers":["behavior","boundary"],'
                  '"cycles":[{"in":{input:integer},optional "mid":{input:integer},' + sample + "}]}]}. "
                  "Use the coverage tags reset, priority, boundary, behavior. Write bit patterns as "
                  "unsigned integer values.")
        return checkpoint(self.home / "tb", prompt, relaxed_json, self.validate_tb)

    def review_rm(self, source):
        def validate(raw):
            issues = raw["issues"] if isinstance(raw, dict) else raw
            if not isinstance(issues, list):
                raise ValueError("Return an issues array")
            out, seen = [], set()
            for item in issues:
                key = str(item["id"])
                at = item.get("location", item.get("line"))
                quote = citation(item.get("spec_quote", item.get("quote")), self.spec)
                if key in seen or not at or not item.get("fix") or not quote:
                    raise ValueError("Each review item requires unique id, code location, fix, and exact source quote")
                seen.add(key)
                out.append({"id": key, "location": at, "spec_quote": quote, "fix": item["fix"]})
            return out
        prompt = (self.context + "Independently audit the Python code against each behavioral claim in the "
                  "spec, prioritizing material errors. Return compact JSON {issues:[{id,location,spec_quote,fix}]} "
                  "with exact spec quotes and code line location or fragment. Return an empty list if there "
                  "is no supported issue. Source:\n" + source)
        issues = checkpoint(self.home / "review", prompt, relaxed_json, validate)
        if not issues:
            save(self.home / "review_reply.json", {"responses": [], "source": source})
            return source

        def reply(raw):
            by_id = {str(row["id"]): row for row in raw["responses"]}
            if set(by_id) != {row["id"] for row in issues}:
                raise ValueError("Give one response to every review issue")
            approved = False
            for row in by_id.values():
                status = row["decision"]
                if status not in ("accept", "rebut") or not row.get("reason"):
                    raise ValueError("Each response requires decision and reason")
                if status == "rebut":
                    quote = citation(row.get("spec_quote"), self.spec)
                    if not quote:
                        raise ValueError("Rebuttal requires a short verbatim public specification quote")
                    row["spec_quote"] = quote
                approved |= status == "accept"
            result = self.validate_model(code(raw["source"]))
            if (result.strip() != source.strip()) != approved:
                raise ValueError("Accepted issues require code changes; all rebuttals preserve the RM")
            return {"responses": list(by_id.values()), "source": result}

        prompt = (self.context + INITIAL + "\nRespond to every review issue as JSON "
                  "{responses:[{id,decision:accept|rebut,reason,spec_quote}],source:complete Python string}. "
                  "Rebut only with a verbatim spec quote. Modify accepted issues. Current RM:\n" + source
                  + "\nReview issues:\n" + compact(issues))
        fixed = checkpoint(self.home / "review_repair", prompt, relaxed_json, reply)
        save(self.home / "review_reply.json", fixed)
        return fixed["source"]

    def disagreement(self, source, scenes):
        details, compared, cycles = [], {}, 0
        for scene in scenes:
            name, ins, expected = scene["id"], scene["vectors"], scene["expected"]
            got = self.run_model(source, ins)
            compared[name] = got
            cycles += len(got)
            for at, (rm, tb) in enumerate(zip(got, expected, strict=True)):
                for output in self.outputs:
                    if rm[output] == tb[output]:
                        continue
                    clk_cycle = at // 2 if self.group == "B" else at
                    history = checker_inputs(self.group, ins)[:at + 1]
                    if self.group == "A" and "mid" in history[-1]:
                        history[-1] = {key: val for key, val in history[-1].items() if key != "mid"}
                    details.append({"id": f"{name}/{at + 1}/{output}", "scene": name,
                                    "sample": at + 1, "cycle": clk_cycle + 1, "output": output,
                                    "input_history": history, "RM": rm[output], "TB": tb[output]})
        return details, compared, cycles

    def pick(self, details):
        selected, limits = [], {}
        for point in details:
            n = limits.get(point["scene"], 0)
            if n < PLAN["arbiter_points_per_scene"]:
                selected.append(point)
                limits[point["scene"]] = n + 1
        return selected

    def arbitrate(self, path, selected):
        def validate(raw):
            rows = raw.get("verdicts", raw) if isinstance(raw, dict) else raw
            actual = {}
            for r in rows:
                key, label = r["id"], r.get("label", r.get("verdict"))
                label = {"rm": "RM", "rm wrong": "RM", "tb": "TB", "tb wrong": "TB",
                         "ambiguous": "ambiguous", "spec ambiguous": "ambiguous"}.get(
                             str(label).lower().replace("_", " "), label)
                quote = citation(r.get("spec_quote"), self.spec)
                if key in actual or label not in KINDS or not quote:
                    raise ValueError("Each verdict requires unique id, RM/TB/ambiguous label, and exact spec quote")
                actual[key] = {"id": key, "label": label, "spec_quote": quote}
            if set(actual) != {p["id"] for p in selected}:
                raise ValueError("Exactly one verdict for each supplied id is required")
            return [actual[p["id"]] for p in selected]

        prompt = (self.context + "Independently derive the disputed output from the input history. "
                  "Decide which party is incorrect, or mark ambiguous if the spec does not decide. Return "
                  "compact JSON {verdicts:[{id,label:RM|TB|ambiguous,spec_quote}]}. Copy one exact short "
                  "spec substring for each verdict, including the relevant incomplete clause for ambiguity. "
                  "Inputs and candidate values:\n" + compact(selected))
        return checkpoint(path, prompt, relaxed_json, validate)

    def fix_tb(self, folder, scenes, evidence):
        def apply(raw):
            patches = raw["patches"] if isinstance(raw, dict) else raw
            targets = {p["id"]: p for p in evidence}
            if not isinstance(patches, list) or len(patches) != len(targets):
                raise ValueError("Provide every requested patch once")
            out = copy.deepcopy(scenes)
            index = {scene["id"]: scene for scene in out}
            for patch in patches:
                point = targets.pop(patch["id"])
                pin = point["output"]
                num = unsigned(patch["value"], self.outputs[pin])
                index[point["scene"]]["expected"][point["sample"] - 1][pin] = num
            return out

        prompt = (self.context + "Review only the disputed TB expectations below; infer corrected concrete "
                  "values from the spec and history. Do not alter the stimulus. Output compact JSON "
                  "{patches:[{id,value}]} containing every requested id once. Evidence:\n" + compact(evidence))
        return checkpoint(folder, prompt, relaxed_json, apply)

    def iterate(self, source, scenes, route, round_no):
        folder = self.home / route / f"round{round_no}"
        details, before, count = self.disagreement(source, scenes)
        selected = self.pick(details)
        save(folder / "disagreements.json", {"points": details, "selected": selected,
                                              "compared_samples": count, "RM": before})
        if not selected:
            save(folder / "outcome.json", {"decisions": [], "RM": source, "TB": scenes})
            return source, scenes, False
        if route == "no_arbiter":
            decisions = [{"id": p["id"], "label": "RM", "source": "TB assumed correct per baseline"}
                         for p in selected]
        else:
            # Historical context is one prefix per point and never includes RM source.
            decisions = self.arbitrate(folder / "arbiter", selected)
        judgments = {row["id"]: row for row in decisions}
        rm_work = [{**p, "judgment": judgments[p["id"]]} for p in selected if judgments[p["id"]]["label"] == "RM"]
        tb_work = [{**p, "judgment": judgments[p["id"]]} for p in selected if judgments[p["id"]]["label"] == "TB"]

        if rm_work:
            revised = self.model(folder / "rm_repair", self.context + INITIAL
                                + "\nKeep supported behaviors. Fix concrete disagreements based only on "
                                "the quoted specification and input traces below. Current model:\n" + source
                                + "\nEvidence:\n" + compact(rm_work))
        else:
            revised = source
        repaired_scenes = self.fix_tb(folder / "tb_repair", scenes, tb_work) if tb_work else scenes
        save(folder / "outcome.json", {"decisions": decisions, "RM": revised, "TB": repaired_scenes})
        return revised, repaired_scenes, bool(rm_work or tb_work)

    def output(self, arm, src, scenes=None, *, folders=(), **extra):
        dest = self.home / "configs" / arm
        if src:
            file = dest / "model.py"
            atomic(file, src)
        answer = {"group": self.group, "task": self.task, "seed": self.seed, "config": arm,
                  "status": "ready" if src else "generation_failed",
                  "model": str(file.relative_to(ROOT)) if src else None,
                  "scenes": scenes, "usage": usage(folders), **extra}
        save(dest / "result.json", answer)
        return answer

    def base(self):
        try:
            if self.group == "A":
                source, historic = archived_base(self.task, self.seed)
                if source is not None:
                    self.validate_model(source)
                    return self.output("Base-think", source, historical_usage=historic, reused=True)
                source = self.model(self.home / "base", original_base_prompt(self.task, self.seed), archived_prompt=True)
            else:
                source = self.model(self.home / "base", self.context + INITIAL)
            return self.output("Base-think", source, folders=[self.home / "base"], reused=False)
        except ArtifactError as error:
            return self.output("Base-think", None, folders=[self.home / "base"], failure=str(error))

    def start(self):
        src_job = POOL.submit(self.initial_rm)
        tb_job = POOL.submit(self.initial_tb)
        base_job = POOL.submit(self.base)
        try:
            source = src_job.result()
        except ArtifactError:
            source = None
        try:
            scenes = tb_job.result()
        except ArtifactError:
            scenes = None
        base_job.result()
        return source, scenes

    def run(self):
        source, scenes = self.start()
        reviewed = None
        review_error = "initial RM generation failed"
        if source is not None:
            try:
                reviewed = self.review_rm(source)
            except ArtifactError as error:
                review_error = str(error)
        base_paths = [self.home / x for x in ("rm", "review", "review_repair")]
        self.output("Ours-noTB", reviewed, folders=base_paths, **({"failure": review_error} if not reviewed else {}))

        def route(arm, name, model, count, shared):
            current = model
            scene = copy.deepcopy(scenes)
            stage = 0
            deps = [*shared, self.home / "tb"]
            error = None
            if model is None or scenes is None:
                error = review_error if model is None else "independent TB generation failed"
            else:
                try:
                    for round_no in range(1, count + 1):
                        position = self.home / name / f"round{round_no}"
                        deps += [position / leaf for leaf in ("arbiter", "rm_repair", "tb_repair")]
                        if (position / "outcome.json").is_file():
                            cached = load(position / "outcome.json")
                            current, scene = cached["RM"], cached["TB"]
                            changes = any(r["label"] != "ambiguous" for r in cached["decisions"])
                        else:
                            current, scene, changes = self.iterate(current, scene, name, round_no)
                        stage = round_no
                        if arm == "Ours" and round_no == 1:
                            self.output("Ours-R1", current, scene, folders=deps, route=name, last_round=stage)
                        if not changes:
                            break
                except ArtifactError as issue:
                    error = str(issue)
            if arm == "Ours" and not (self.home / "configs/Ours-R1/result.json").is_file():
                self.output("Ours-R1", None if error else current, scene, folders=deps, route=name,
                            last_round=stage, **({"failure": error} if error else {}))
            return self.output(arm, None if error else current, scene, folders=deps, route=name,
                               last_round=stage, **({"failure": error} if error else {}))

        with ThreadPoolExecutor(max_workers=3) as parallel:
            jobs = [parallel.submit(route, "Ours", "standard", reviewed, 2, base_paths),
                    parallel.submit(route, "Ours-noReview", "no_review", source, 2, [self.home / "rm"]),
                    parallel.submit(route, "Ours-noArbiter", "no_arbiter", reviewed, 2, base_paths)]
            for job in jobs:
                job.result()
        print(self.group, self.task, self.seed, "routes complete", flush=True)

    def vote_member(self, n):
        path = self.home / "vote" / f"rm{n:02d}"
        try:
            return self.model(path, self.context + INITIAL +
                              "\nImplement an independent solution using only the supplied public specification.")
        except ArtifactError:
            return None

    def vote(self, n, members):
        paths = [self.home / "vote" / f"rm{i:02d}" for i in range(1, n + 1)]
        scores = [str((path / "model.py").relative_to(ROOT))
                  for path, candidate in zip(paths, members[:n], strict=True) if candidate is not None]
        answer = self.output("Vote-think", None, folders=paths, members=scores, planned_members=n)
        if len(scores) > n // 2:
            answer["status"] = "ready"
            save(self.home / "configs/Vote-think/result.json", answer)
        else:
            answer["failure"] = "fewer than half of the independent members are executable"
            save(self.home / "configs/Vote-think/result.json", answer)


def vote_members(cells, lo, hi, acquired):
    submitted = {POOL.submit(cell.vote_member, index): (cell, index)
                 for cell in cells for index in range(lo, hi + 1)}
    for future in as_completed(submitted):
        cell, i = submitted[future]
        acquired[cell][i - 1] = future.result()


def calibrate(cells):
    target = sum(load(c.home / "configs/Ours/result.json")["usage"]["tokens"] for c in cells) / len(cells)
    acquired = {cell: [None] * 31 for cell in cells}
    previous = 0
    points = []
    for n in range(1, 32, 2):
        vote_members(cells, previous + 1, n, acquired)
        mean = sum(usage(c.home / "vote" / f"rm{i:02d}" for i in range(1, n + 1))["tokens"]
                   for c in cells) / len(cells)
        points.append({"N": n, "mean_tokens": mean})
        if mean >= target or (n >= 3 and mean == points[-2]["mean_tokens"]):
            break
        previous = n
    chosen = min(points, key=lambda item: (abs(item["mean_tokens"] - target), item["N"]))
    return chosen["N"], acquired, {"target": target, "candidates": points, **chosen}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("initial", "pilot", "full"))
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    verify_protocol()
    if load(ROOT / "reports/cvdp_self_replay.json")["status"] != "passed":
        raise SystemExit("The CVDP self-replay gate must pass first")
    phase = "pilot" if args.phase == "initial" else args.phase
    if phase == "full":
        amendment = load(ROOT / "amendment.json")
        if load(ROOT / "reports/pilot_gate.json")["status"] != "passed":
            raise SystemExit("Pilot generation gate did not pass")
        from data import REPO
        import subprocess
        committed = subprocess.check_output(["git", "show", f"HEAD:{(ROOT / 'amendment.json').relative_to(REPO)}"], cwd=REPO)
        if committed != (ROOT / "amendment.json").read_bytes():
            raise SystemExit("Commit Amendment before full generation")
        prereg = ROOT / "PREREG.md"
        if (f"Vote-think 的 N = {amendment['N']}。" not in prereg.read_text() or
                subprocess.check_output(["git", "show", f"HEAD:{prereg.relative_to(REPO)}"], cwd=REPO)
                != prereg.read_bytes()):
            raise SystemExit("The N selection must be stated in the committed PREREG.md Amendment")
    cells = [Cell(*row) for row in roster(phase)]
    with ThreadPoolExecutor(max_workers=args.workers) as jobs:
        list(jobs.map(lambda cell: cell.start() if args.phase == "initial" else cell.run(), cells))
    if args.phase == "initial":
        return
    if phase == "pilot":
        n, acquired, budget = calibrate(cells)
        save(ROOT / "reports/pilot_vote_budget.json", budget)
    else:
        n = amendment["N"]
        acquired = {c: [None] * n for c in cells}
        vote_members(cells, 1, n, acquired)
    for cell in cells:
        cell.vote(n, acquired[cell])
    rows = [load(c.home / "configs" / arm / "result.json") for c in cells for arm in PLAN["configs"]]
    failures = sum(r["status"] != "ready" for r in rows)
    save(ROOT / "reports" / f"{phase}_generation.json",
         {"cases": len(cells), "configs": len(rows), "failures": failures, "N": n})
    if phase == "pilot":
        save(ROOT / "reports/pilot_gate.json", {"status": "passed" if failures / len(rows) <= PLAN["max_pilot_generation_failure"]
             else "repair_required", "failures": failures, "planned": len(rows), "N": n})
    print(phase, len(rows), "configs", failures, "unusable", flush=True)


if __name__ == "__main__":
    main()
