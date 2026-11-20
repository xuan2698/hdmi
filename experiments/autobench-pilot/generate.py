import json
import re
from pathlib import Path

from llm import LOG_PATH, REASONING_EFFORT, call_llm

ROOT = Path(__file__).resolve().parent


def prompt_for(problem, role, feedback="", previous=""):
    interface = problem["module_header"]
    ports = re.findall(r"\b(input|output)\s+(?:(?:reg|wire|logic)\s+)?(\[[^\]]+\]\s*)?(\w+)",
                       interface)
    port_text = ", ".join(f"{direction} {width.strip()} {name}".replace("  ", " ")
                          for direction, width, name in ports)
    prefix = f"""Write only executable Python source. No imports, file access, prints or classes.
Use builtin types and functions, e.g. int, range, len, list, dict, enumerate, zip, min, max.
This is the complete public task specification and interface.
{problem["spec"]}
Interface: {port_text}. The harness supplies the clock and samples after each rising edge.
"""
    if role == "checker":
        instruction = """Implement exactly reference(vectors). Input is a list of dictionaries with
integer values for each nonclock input, one row per rising edge. Return a list of equally many
dictionaries with the expected integer values for ALL output ports after that edge. Model
sequential state independently using only the vectors and spec. Use None for an output only when
the specification cannot determine a value (for example, before initialization). Do not accept
observed output values as inputs or weaken checks in order to fit an ambiguous observation.
"""
    else:
        instruction = """Implement exactly stimulus(rng, cycles). Return exactly cycles dictionaries
with an integer value for EVERY nonclock input in each row. The harness supplies the clock.
rng is the seeded Python Random object and you may use rng.getrandbits, rng.randrange, rng.choice
and rng.random. Start in a known state using the reset as specified. Do not inspect any DUT output.
"""
        if role == "screen":
            instruction += """This is mutation-screening stimulus. Use independent pseudorandom input
bits across the full width at each cycle. Pulse reset randomly throughout the run with a moderate
probability, while allowing runs of several cycles without reset. Support a 2,000-cycle run.
"""
        else:
            instruction += """Use a mix of targeted and pseudorandom inputs within the supplied 96
cycle budget. Cover meaningful edge/state transitions and reset interactions implied by the public spec.
"""
    if previous:
        instruction += "\nPrevious source:\n" + previous + "\n"
    if feedback:
        instruction += "\nFeedback for this revision:\n" + feedback + "\n"
    return prefix + instruction


def generate(task_dir, problem, plan, role, code_path, feedback="", previous=""):
    if code_path.is_file():
        return code_path.read_text()
    log = task_dir / "calls.jsonl"
    token = LOG_PATH.set(log)
    effort = REASONING_EFFORT.set(plan.get("reasoning_effort"))
    code_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = prompt_for(problem, role, feedback, previous)
    try:
        answer = call_llm(plan["model"], prompt, plan["temperature"], plan["max_tokens"])
    finally:
        REASONING_EFFORT.reset(effort)
        LOG_PATH.reset(token)
    response = answer["response"]
    if not answer["complete"]:
        raise RuntimeError(f"Incomplete model output for {role}: {answer['finish_reason']}")
    fence = chr(96) * 3
    block = re.search(f"{fence}(?:python|py)?\\s*\\n(.*?){fence}", response, re.DOTALL)
    code = (block[1] if block else response).strip() + "\n"
    temp = code_path.with_suffix(".pending")
    temp.write_text(code)
    temp.replace(code_path)
    return code


def initial(task_id, cfg, plan):
    problem = json.loads((ROOT / "generation" / task_id / "problem.json").read_text())
    location = ROOT / "runs" / task_id / cfg
    roles = ("screen",) if cfg == "screen" else ("stimulus", "checker")
    for role in roles:
        generate(location, problem, plan, role, location / f"{role}_01.py")
