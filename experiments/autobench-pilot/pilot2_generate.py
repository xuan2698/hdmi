import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from llm import LOG_PATH, THINKING, TRANSPORT, call_llm

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "v2"


def load(path):
    return json.loads(path.read_text())


def settings():
    return load(ROOT / "pilot2.json")


def atomic(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".pending")
    temporary.write_text(body)
    temporary.replace(path)


def save(path, data):
    atomic(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def request(log, prompt, plan):
    if not os.environ.get("OPENCODE_GO_API_KEY", "").strip():
        raise RuntimeError("Missing OPENCODE_GO_API_KEY")
    overrides = [
        (LOG_PATH, LOG_PATH.set(log)),
        (THINKING, THINKING.set(plan["thinking"])),
        (TRANSPORT, TRANSPORT.set({**plan["transport"], "stream": plan["stream"]})),
    ]
    try:
        response = call_llm(plan["model"], prompt, plan["temperature"], plan["max_tokens"])
    finally:
        for key, token in reversed(overrides):
            key.reset(token)
    if not response["complete"]:
        raise RuntimeError(f"Completion did not finish normally: {response['finish_reason']}")
    text = response["response"]
    fence = chr(96) * 3
    block = re.search(f"{fence}(?:python|py)?\\s*\\n(.*?){fence}", text, re.DOTALL)
    return (block[1] if block else text).strip() + "\n"


def source(directory, filename, problem, interface, role, plan, feedback="", previous=""):
    path = directory / filename
    if path.is_file():
        return path.read_text()
    ins, outs, clock, edge = interface
    edge_name = "falling" if edge == "negedge" else "rising"
    public = f"""Implement this public hardware specification as executable Python. Output concise complete Python only.
Do not import anything, print, define classes, or access files. Common builtin functions are provided.
Omit comments and explanations. Never reproduce a waveform table or narrate a search.
Specification:
{problem['spec']}
Interface: nonclock inputs (name -> bits) {ins}; outputs (name -> bits) {outs}. Main clock is {clock or 'none'}.
Each dictionary represents one chronological sample. Inputs are driven before the active {edge_name} edge.
Sample values are observed after the edge and settling, or after settling directly on a combinational interface.
"""
    if role == "checker":
        instructions = """Define reference(vectors). For every input row return a dict with all output names
and the independently derived expected integer, bounded to the output width. Return a list of equal length.
Use None only when the public spec leaves that output value undefined, e.g. unknown power-up state.
Read the task carefully. Handle every required state and explicitly preserve bit widths. You receive no observed
device output at runtime. If proxy reports disagree, reason from the spec before deciding whether to change code.
"""
        if "simulation waveforms" in problem["spec"].lower():
            instructions += """Use the shortest state/output model supported by the public waveform. If the
waveform underdetermines a value, return None for that value. Keep the implementation under 50 lines.
"""
    else:
        instructions = """Define stimulus(rng, cycles) returning exactly cycles dictionaries with ONLY every listed
nonclock input and width-bounded integer values. The runner supplies the clock. Use rng.getrandbits,
rng.randrange, rng.choice or rng.random. Generate deterministic, targeted and varied sequences that cover
the public behavior, resets, boundaries and transitions. Drive inputs only.
"""
        if role == "append":
            instructions += """This source creates a new suffix of exactly the requested length.
The complete previous sequence is immutable and will run first. Add directed sequences for the feedback.
Use a new reset when necessary to reach the intended state. Do not regenerate the previous sequence.
"""
    if previous:
        instructions += "\nPrior source:\n" + previous + "\n"
    if feedback:
        instructions += "\nRevision evidence:\n" + feedback + "\n"
    generated = request(directory / "calls.jsonl", public + instructions, plan)
    atomic(path, generated)
    return generated


def warm_calibration(all_tasks, workers):
    from pilot2_sim import interface_from

    task_file = BASE / ("all_tasks.json" if all_tasks else "initial_tasks.json")
    plan = settings()

    def generate(task, role):
        problem = load(BASE / "generation" / task / "problem.json")
        interface = interface_from(problem)
        location = BASE / "runs" / "calibration" / task / "A0" / "rep1"
        source(location, f"{role}_01.py", problem, interface, role, plan)
        return task, role

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(generate, task["task_id"], role): (task["task_id"], role)
                   for task in load(task_file) for role in ("stimulus", "checker")}
        for item in as_completed(futures):
            try:
                print("ready", *item.result(), flush=True)
            except Exception as exc:
                print("generation pending", *futures[item], type(exc).__name__, str(exc), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    warm_calibration(args.all, args.workers)
