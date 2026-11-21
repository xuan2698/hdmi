import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from pilot2_generate import atomic, request, save
from pilot3_inputs import BASE, public, setup, tasks
from simulate import RunError, execute_code, expected_from, validate_rows


def driver_rows(code, ins, seed, cycles):
    rows = execute_code(code, "stimulus", seed=seed, cycles=cycles)
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise RunError("Return a list of input dictionaries")
    plain = [{key: value for key, value in row.items() if key != "mid"} for row in rows]
    validate_rows(plain, ins, cycles)
    for row in rows:
        if "mid" not in row:
            continue
        values = row["mid"]
        if not isinstance(values, dict) or not values.keys() <= ins.keys():
            raise RunError("A mid dictionary may only name input ports")
        validate_rows([values], {key: ins[key] for key in values}, 1)
    return rows


def check_rows(code, outs, vectors):
    rows = expected_from(code, outs, vectors)
    missing = [(i + 1, field) for i, row in enumerate(rows)
               for field, value in row.items() if value is None]
    if missing:
        raise RunError(f"{len(missing)} missing expected values; first cycle/output: {missing[:6]}")
    return rows


def generate(where, role, iteration, task, plan, seed, validator, *, evidence="", previous=""):
    spec, interface = public(task)
    ins, outs, clk, edge = interface
    limit = plan["check_regenerations"] if role == "checker" else plan["compile_repairs"]
    prefix = f"""Implement the public hardware specification in concise executable Python source.
Return code only, without imports, comments, prints, external files, or explanatory analysis.
Task specification:
{spec['spec']}
Ports other than the clock ({clk}): inputs {ins}; outputs {outs}.
Each supplied row is driven before the active {edge} edge and sampled after it settles. A row can
optionally include a dictionary named mid containing changes to some inputs AFTER that sample,
before the opposite edge. After the mid changes, inputs hold until the next row.
Protocol seed {seed}. Keep the implementation compact. Use loops, dictionaries and lists.
"""
    if role == "checker":
        instruction = """Implement reference(vectors), returning a list of exactly the same length with
a dict per row. Each dictionary MUST contain a width-bounded concrete integer for EVERY output at
EVERY row. Never return None or omit an output. Choose a concrete power-up assumption if needed.
Only the public spec defines the logic. Carry forward effects of asynchronous mid changes where prescribed.
For waveform tasks infer the smallest behavior consistent with the table and return only the model
function. Never transcribe the table or describe your search. Limit the function to 65 lines.
"""
    else:
        limit_cycles = plan["append_cycles"] if iteration > 1 else plan["stimulus_cycles"]
        instruction = f"""Implement stimulus(rng, cycles) and return exactly cycles input dictionaries.
The caller passes cycles={limit_cycles}. Every input needs a width-bounded integer. Inputs and the
optional mid dictionary are the only keys. Use rng.getrandbits, randrange, choice and random.
Generate varied targeted and random inputs using compact loop-based programs. At most 16 literal
rows. Keep the function under 45 lines and fill remaining rows with a loop. No DUT observations.
"""
        if iteration > 1:
            instruction += "Return only a new suffix. The previous sequence is immutable and runs first.\n"
    if previous:
        instruction += "\nPrior generated source:\n" + previous + "\n"
    if evidence:
        evidence = "\nRevision evidence:\n" + evidence + "\n"
    history = []
    last_code = ""
    for attempt in range(limit + 1):
        file = where / f"{role}_{iteration:02d}_try{attempt + 1}.py"
        try:
            if file.exists():
                code = file.read_text()
            else:
                repair = ("\nCorrect this generation or implementation failure without changing the interface: "
                          + history[-1] + "\n") if history else ""
                prior_attempt = "\nSource from the last attempt:\n" + last_code if last_code else ""
                code = request(where / "calls.jsonl",
                               prefix + instruction + (evidence if not attempt else "") + prior_attempt + repair,
                               plan)
                atomic(file, code)
            last_code = code
            result = validator(code)
        except (RuntimeError, ValueError) as exc:
            history.append(str(exc)[-650:])
            continue
        save(where / f"{role}_{iteration:02d}_validation.json",
             {"attempts": attempt + 1, "regenerations": attempt, "errors": history, "selected": file.name})
        return code, result, attempt
    save(where / f"{role}_{iteration:02d}_validation.json",
         {"attempts": limit + 1, "regenerations": limit, "errors": history, "selected": None})
    raise RunError(f"{role} exhausted its {limit} regeneration opportunities: {history[-1]}")


def initial(task, rep, seed, plan):
    folder = BASE / "initial" / task / f"rep{rep}"
    if (folder / "result.json").is_file():
        return folder
    _, interface = public(task)
    ins, outs = interface[:2]
    try:
        _, vectors, _ = generate(folder, "stimulus", 1, task, plan, seed,
                                 lambda code: driver_rows(code, ins, seed, plan["stimulus_cycles"]))
        save(folder / "vectors.json", vectors)
        code, predicted, _ = generate(folder, "checker", 1, task, plan, seed,
                                     lambda text: check_rows(text, outs, vectors))
        atomic(folder / "checker.py", code)
        save(folder / "expected.json", predicted)
    except RunError as exc:
        save(folder / "result.json", {"status": "generation_failed", "reason": str(exc), "seed": seed})
    else:
        save(folder / "result.json", {"status": "complete", "seed": seed})
    return folder


def warm(workers):
    plan = setup()
    arguments = [(task["task_id"], rep, seed) for rep, seed in enumerate(plan["repeat_seeds"], 1)
                 for task in tasks()]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(initial, *arg, plan) for arg in arguments]
        for future in as_completed(futures):
            print("initial checkpoint", future.result().relative_to(BASE), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=20)
    warm(parser.parse_args().workers)
