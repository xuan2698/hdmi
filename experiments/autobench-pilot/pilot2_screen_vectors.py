import re

from pilot2_generate import BASE, atomic, request
from simulate import execute_code, validate_rows


def generator(plan):
    folder = BASE / "protocol"
    target = folder / "screen_vectors.py"
    if not target.is_file():
        text = request(folder / "calls.jsonl", """Write just executable Python source with no imports.
Define screen_vectors(rng, cycles, widths, resets). widths maps input port names to widths, resets maps
reset names to asserted values 0 or 1, and the RNG implements getrandbits, random, and randrange.
Return exactly cycles dictionaries mapping every name in widths to an unsigned value that fits.
Draw independent unbiased random bits for nonreset inputs of all widths. Assert each reset at the
first sample and randomly on later samples with probability 1/32. Otherwise deassert it. The code
must handle any mapping, including an empty one. It must not inspect RTL, outputs or external files.
""", plan)
        atomic(target, text)
    return target.read_text()


def reset_levels(problem, widths):
    resets = {}
    for port in widths:
        name = port.lower()
        if widths[port] != 1:
            continue
        if name in ("resetn", "reset_n", "rst_n", "aresetn", "areset_n", "rstn"):
            resets[port] = 0
        elif name in ("reset", "rst", "areset", "srst", "ar") or (
            name == "r" and re.search(r"\breset\b", problem["spec"], re.I)
        ):
            resets[port] = 0 if re.search(r"\bactive[- ]low\b", problem["spec"], re.I) else 1
    return resets


def random_rows(code, problem, inputs, plan):
    resets = reset_levels(problem, inputs)
    cycles = plan["screen_cycles"]
    for seed in plan["screen_seeds"]:
        result = execute_code(code, "screen", seed=seed, cycles=cycles, widths=inputs, resets=resets)
        yield validate_rows(result, inputs, cycles)
