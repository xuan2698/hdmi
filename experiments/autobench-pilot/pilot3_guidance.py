import argparse
import operator
import re
from concurrent.futures import ThreadPoolExecutor
from itertools import product

from mutations import candidate, diagnostic, signals
from pilot2_generate import load, save
from pilot2_guidance import build_catalog, edit
from pilot2_sim import VectorReplay
from pilot3_inputs import BASE, PREVIOUS, public, setup, tasks
from simulate import RunError, differences

CONST = r"(?:\d+'[bBdDhHoO][0-9a-fA-F_]+|\d+)"
VARIABLE = r"[A-Za-z_]\w*(?:\[\d+(?::\d+)?\])?"
COMPARISON = re.compile(rf"^({VARIABLE})\s*(==|!=|<=|>=|<|>)\s*({CONST})$")
OFFSET = re.compile(rf"^({VARIABLE})(?:\s*([+-])\s*({CONST}))?$")
COMPARE = {"==": operator.eq, "!=": operator.ne, "<": operator.lt, ">": operator.gt,
           "<=": operator.le, ">=": operator.ge}
ARITHMETIC = {
    "+": operator.add, "-": operator.sub, "*": operator.mul,
    "&": operator.and_, "|": operator.or_, "^": operator.xor,
    "&&": lambda a, b: int(bool(a) and bool(b)), "||": lambda a, b: int(bool(a) or bool(b)),
}
TERM = rf"(?:{VARIABLE}|{CONST})"
BINARY = re.compile(rf"^({TERM})\s*([+*^-]|&&|\|\||&|\|)\s*({TERM})$")
UNARY = re.compile(rf"^([~!+-])\s*({TERM})$")


def number(token):
    if "'" in token:
        _, body = token.split("'", 1)
        base = {"b": 2, "o": 8, "d": 10, "h": 16}[body[0].lower()]
        return int(body[1:].replace("_", ""), base)
    return int(token)


def simple_expression(text):
    terms = re.fullmatch(TERM, text)
    if terms:
        return ("term", text)
    binary = BINARY.fullmatch(text)
    if binary:
        return ("binary", *binary.groups())
    unary = UNARY.fullmatch(text)
    if unary:
        return ("unary", *unary.groups())
    return None


def evaluate_expr(expr, env):
    def value(token):
        if re.fullmatch(CONST, token):
            return number(token)
        name, bracket, segment = token.partition("[")
        raw = env[name]
        if not bracket:
            return raw
        ends = [int(i) for i in segment[:-1].split(":")]
        return (raw >> min(ends)) & ((1 << (abs(ends[0] - ends[-1]) + 1)) - 1)

    kind, *parts = expr
    if kind == "term":
        return value(parts[0])
    if kind == "unary":
        sign, operand = parts
        return {"!": lambda x: int(not x), "~": operator.invert,
                "+": operator.pos, "-": operator.neg}[sign](value(operand))
    left, op, right = parts
    return ARITHMETIC[op](value(left), value(right))


def sufficient_witness(before, after, widths, output_bits):
    parsed = [simple_expression(text) for text in (before, after)]
    if None in parsed:
        return None
    operands = sorted({token.split("[")[0] for expr in parsed for token in expr[1:]
                       if re.fullmatch(VARIABLE, token)})
    if len(operands) > 2 or any(key not in widths for key in operands):
        return None
    samples = []
    for key in operands:
        mx = (1 << widths[key]) - 1
        samples.append(sorted({v for v in (0, 1, 2, 3, mx >> 1, mx - 1, mx) if 0 <= v <= mx}))
    mask = (1 << output_bits) - 1
    for row in product(*samples):
        env = dict(zip(operands, row))
        a, b = (evaluate_expr(expr, env) & mask for expr in parsed)
        if a != b:
            return "sufficient example at the reached site: " + (
                ", ".join(f"{k}={v}" for k, v in env.items()) or "constant values differ"
            )
    return None


def derive(atom, widths):
    before, after = (re.sub(r"[()]", "", atom[key]).strip() for key in ("orig", "changed"))
    lhs, rhs = (COMPARISON.fullmatch(text) for text in (before, after))
    if lhs and rhs and lhs[1] == rhs[1]:
        var = lhs[1]
        a, b = number(lhs[3]), number(rhs[3])
        base, _, slice_text = var.partition("[")
        if slice_text:
            bits = [int(n) for n in slice_text[:-1].split(":")]
            width = abs(bits[0] - bits[-1]) + 1
        else:
            width = widths.get(base)
        if width:
            maximum = (1 << width) - 1
            cuts = sorted({0, maximum + 1, *[x for x in (a, a + 1, b, b + 1) if 0 < x <= maximum]})
            bands = []
            for first, following in zip(cuts, cuts[1:]):
                last = following - 1
                if COMPARE[lhs[2]](first, a) != COMPARE[rhs[2]](first, b):
                    bands.append(f"{var} == {first}" if first == last else f"{first} <= {var} <= {last}")
            return " or ".join(bands) or None
    lhs, rhs = (OFFSET.fullmatch(text) for text in (before, after))
    if lhs and rhs and lhs[1] == rhs[1]:
        offsets = [number(m[3]) * (-1 if m[2] == "-" else 1) if m[3] else 0 for m in (lhs, rhs)]
        if (offsets[0] - offsets[1]) % (1 << atom["width"]):
            return f"site executes with {lhs[1]} known (offsets differ modulo output width)"
    if re.fullmatch(CONST, before) and re.fullmatch(CONST, after):
        if (number(before) - number(after)) % (1 << atom["width"]):
            return "assignment site executes"
    return sufficient_witness(before, after, widths, atom["width"])


def prepare(task, plan):
    group = BASE / "guidance" / task
    pointer = group / "anchor.json"
    if pointer.exists() and (group / "catalog.json").exists():
        name = load(pointer)["anchor"]
        return (BASE / "proxies" / task / f"{name}.v").read_text(), load(group / "catalog.json")
    code = (PREVIOUS / "protocol" / "screen_vectors.py").read_text()
    spec, interface = public(task)
    ins = interface[0]
    dry = VectorReplay(interface, [{key: int(i == 0 and "reset" in key) for key in ins}
                                   for i in range(8)], proxy_compat=True)
    proxies = BASE / "proxies" / task
    preferred = [proxies / f"gpt4o_{i}.v" for i in range(1, 4)]
    errors = {}
    for candidate_file in (*preferred, *sorted(set(proxies.glob("*.v")) - set(preferred))):
        rtl = candidate_file.read_text()
        try:
            dry.trace(rtl)
        except (RunError, ValueError) as exc:
            errors[candidate_file.stem] = str(exc)
            continue
        catalog = build_catalog(task, spec, interface, rtl, code, plan, destination=group / "catalog.json")
        save(pointer, {"anchor": candidate_file.stem, "unavailable_before_anchor": errors})
        return rtl, catalog
    raise RunError(f"No runnable archived guidance proxy for {task}")


def added_feedback(records, rtl, bench, exposed, method):
    missed = [record for record in records if record["id"] not in exposed]
    if not missed:
        return "", {}
    lines, results = [], {}
    timing_bench = VectorReplay((bench.inputs, bench.outputs, bench.clock, bench.edge),
                               bench.vectors, all_edges=True, proxy_compat=True)
    reference = timing_bench.trace(rtl)[0] if method == "O" else None
    widths = {**bench.inputs, **bench.outputs, **signals(rtl, bench.inputs, bench.outputs)}
    for record in missed:
        tag = record["id"]
        lines.append(" | ".join(candidate(atom).feedback(tag) for atom in record["edits"]))
        if method != "O":
            continue
        known = []
        for atom in record["edits"]:
            try:
                finding = diagnostic(atom, rtl, bench)
            except (RunError, KeyError, ValueError) as exc:
                finding = {"label": "probe unavailable", "reason": str(exc).splitlines()[0]}
            if finding["label"] == "未感染":
                finding["infection_condition"] = derive(atom, widths)
            known.append(finding)
        brief = []
        for finding in known:
            clause = finding["label"]
            if finding["label"] == "未感染":
                clause += "; infection condition " + (finding["infection_condition"] or "could not derive")
                ranges = finding.get("operand_ranges", {})
                if ranges:
                    clause += "; observed ranges " + ", ".join(
                        f"{name}={values['min']}..{values['max']}" for name, values in ranges.items()
                    )
            elif finding.get("intervals"):
                clause += " " + str(finding["intervals"][0])
            brief.append(clause)
        lines.append(" | ".join(brief))
        obs, _ = timing_bench.trace(edit(rtl, record))
        timing = {}
        for phase, name in ((0, "before active edge"), (2, "after opposite edge")):
            contrasts = differences(reference[phase::3], obs[phase::3])
            if contrasts:
                timing[name] = {"samples": len(contrasts),
                                "first_cycle": contrasts[0][0] + 1, "signal": contrasts[0][1]}
        if timing:
            lines.append(f"Difference between scored edges: {timing}. Try toggling the relevant input via mid.")
        results[tag] = {"sites": known, "between_edge_differences": timing}
    return "\n".join(lines), results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    plan = setup()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        work = pool.map(lambda task: prepare(task["task_id"], plan), tasks())
        for _, catalog in work:
            print(catalog["task"], [item["retained"] for item in catalog["groups"]], flush=True)
