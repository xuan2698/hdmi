import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import zip_longest

from simulate import RunError, differences

OPERATION = {
    "+": ("-", "*"), "-": ("+", "*"), "*": ("+", "-"),
    "<<": (">>", "+"), ">>": ("<<", "-"),
    "&": ("|", "^", "&&"), "|": ("&", "^", "||"), "^": ("&", "|"),
    "&&": ("||", "^"), "||": ("&&", "^"), "~": ("!", "+"),
    "==": ("!=", ">="), "!=": ("==", ">"), "<": ("<=", ">"),
    ">": (">=", "<"), "<=": ("<", ">="), ">=": (">", "<="),
}
OPERATORS = re.compile("|".join(re.escape(x) for x in sorted(OPERATION, key=len, reverse=True)))
ASSIGNMENT = re.compile(r"^\s*(\w+)\s*(?:<=|=)\s*([^;]+);")
CONDITION = re.compile(r"\bif\s*\(([^()]+)\)")
STATE = re.compile(r"\b(?:localparam|parameter)\b[^;]*;")


@dataclass(frozen=True)
class Candidate:
    rule: str
    line: int
    before: str
    after: str
    orig: str
    changed: str
    guard: str
    lhs: str
    width: int

    def rtl(self, source):
        lines = source.splitlines(keepends=True)
        if lines[self.line - 1].rstrip("\r\n") != self.before:
            raise ValueError("Mutation source no longer matches proxy")
        lines[self.line - 1] = self.after + "\n"
        return "".join(lines)

    def feedback(self, tag):
        return f"{tag} L{self.line}: {self.before.strip()} → {self.after.strip()}"


def signals(source, inputs, outputs):
    internals = {}
    for hi, lo, name in re.findall(
        r"(?m)^\s*(?:reg|logic)\s+(?:\[(\d+):(\d+)\]\s*)?(\w+)\s*;", source
    ):
        if name not in inputs and name not in outputs:
            internals[name] = abs(int(hi) - int(lo)) + 1 if hi else 1
    return internals


def proposals(source, inputs, outputs):
    widths = {**inputs, **outputs, **signals(source, inputs, outputs)}
    buckets = defaultdict(list)
    seen = set()
    state_names = re.findall(r"\b([A-Za-z_]\w*)\s*=", " ".join(STATE.findall(source)))
    guard = "1'b1"
    predicate = None
    for index, line in enumerate(source.splitlines(), start=1):
        def add(rule, match, group, replacement, active=guard, lhs="", width=1):
            expression = match[group].strip()
            modified = line[:match.start(group)] + replacement + line[match.end(group):]
            identity = (index, modified)
            if identity not in seen and modified != line:
                seen.add(identity)
                buckets[rule].append(Candidate(
                    rule, index, line, modified, expression, replacement, active, lhs, width
                ))

        clock = re.search(r"\b(posedge)\s+clk", line)
        if clock:
            add("clock_edge", clock, 1, "negedge", active="1'b1")
            continue
        cond = CONDITION.search(line)
        if cond:
            predicate = cond[1].strip()
            for rule, replacement in (
                ("negated_condition", f"!({predicate})"),
                ("removed_condition", "1'b0"),
                ("removed_condition", "1'b1"),
                ("relation", f"({predicate}) == 1'b0"),
                ("relation", f"({predicate}) != 1'b0"),
            ):
                add(rule, cond, 1, replacement, active="1'b1")
            for name, width in inputs.items():
                if name == predicate:
                    continue
                bits = [name] if width == 1 else [f"{name}[0]", f"{name}[{width-1}]"]
                for bit in bits:
                    for op in ("&&", "||", "^"):
                        add("condition_operator", cond, 1, f"({predicate}) {op} {bit}", active="1'b1")
            guard = f"({predicate})"
            continue
        if re.search(r"\belse\b", line) and predicate:
            guard = f"!({predicate})"
            continue
        assign = ASSIGNMENT.search(line)
        if not assign:
            continue
        lhs, value = assign[1], assign[2].strip()
        width = widths.get(lhs, 1)

        def rhs(rule, replacement):
            add(rule, assign, 2, replacement, active=guard, lhs=lhs, width=width)

        for op in OPERATORS.finditer(value):
            for replacement in OPERATION[op[0]]:
                rhs("operator_replacement", value[:op.start()] + replacement + value[op.end():])
        if re.fullmatch(r"(?:\d+'[sS]?[bBdDhH])?[0-9]+", value):
            for amount in (-1, 1):
                sign = "+" if amount > 0 else "-"
                rhs("constant_offset", f"({value}) {sign} 1")
        for op in ("~", "!", "+", "-"):
            rhs("unary_operator", f"{op}({value})")
        for op in ("+", "-", "^", "&", "|", "<<", ">>"):
            rhs("arithmetic_or_bitwise", f"({value}) {op} 1")
        rhs("deleted_assignment", lhs)
        rhs("replaced_assignment", f"{width}'d0")
        rhs("replaced_assignment", f"{width}'d1")
        for name, bits in widths.items():
            if name not in {lhs, "clk"} and bits == width:
                rhs("replaced_assignment", name)
            if bits > 1 and re.search(rf"\b{name}\b", value):
                for op in ("<<", ">>"):
                    replacement = re.sub(rf"\b{name}\b", f"({name} {op} 1)", value, count=1)
                    rhs("bit_index_offset", replacement)
        for state in state_names:
            if value in state_names and state != value:
                rhs("state_transition", state)
    for group in zip_longest(*buckets.values()):
        yield from (item for item in group if item is not None)


def screen(source, inputs, outputs, replays, maximum=40):
    base = [rep.trace(source)[0] for rep in replays]
    variants = []
    invalid = []
    for proposal in proposals(source, inputs, outputs):
        text = proposal.rtl(source)
        try:
            traces = [rep.trace(text)[0] for rep in replays]
        except (RunError, ValueError) as exc:
            invalid.append({"candidate": asdict(proposal), "reason": str(exc)})
            continue
        changed = [len(differences(ref, obs)) for ref, obs in zip(base, traces, strict=True)]
        variants.append({"id": f"G{len(variants) + 1:02d}", **asdict(proposal),
                         "screen_differences": changed, "retained": any(changed)})
        if len(variants) >= maximum:
            break
    if len(variants) not in range(20, maximum + 1):
        raise RunError(f"Only {len(variants)} compilable mutants for the required 20–{maximum}")
    return {"variants": variants, "invalid": invalid,
            "retained": sum(v["retained"] for v in variants),
            "suspected_equivalent": sum(not v["retained"] for v in variants)}


def candidate(record):
    return Candidate(**{key: record[key] for key in Candidate.__dataclass_fields__})


def diagnostic(record, source, replay):
    change = candidate(record)
    names = signals(source, replay.inputs, replay.outputs)
    operands = [name for name in (*replay.inputs, *replay.outputs, *names)
                if re.search(rf"\b{name}\b", f"{change.orig} {change.changed} {change.guard}")]
    if change.rule == "clock_edge":
        return {"label": "未传播", "cause": "边沿变化没有改变当前采样输出", "intervals": []}
    tags = ("pilot_hit", "pilot_ref", "pilot_mut")
    probes = [f"reg [0:0] {tags[0]};", f"reg [{change.width-1}:0] {tags[1]}, {tags[2]};"]
    probes += [f"reg [{({**replay.inputs, **replay.outputs, **names})[name]-1}:0] pilot_arg_{name};"
               for name in operands]
    probes += ["always @(posedge clk) begin", f"{tags[0]} <= {change.guard};",
               f"{tags[1]} <= {change.orig};", f"{tags[2]} <= {change.changed};"]
    probes += [f"pilot_arg_{name} <= {name};" for name in operands]
    probes += ["end"]
    instrumented = re.sub(r"\bendmodule\b", "\n".join(probes) + "\nendmodule", source, count=1)
    trace, waves = replay.trace(instrumented, observe=(*tags, *names, *[f"pilot_arg_{n}" for n in operands]))
    reached = [i for i, wave in enumerate(waves) if wave["pilot_hit"] == "1"]
    infected = [i for i in reached if any(a in "01" and a != b
                for a, b in zip(waves[i]["pilot_ref"], waves[i]["pilot_mut"], strict=True))]
    if not reached:
        return {"label": "未到达", "reached": 0}
    if not infected:
        representative = [waves[i] for i in reached]
        values = {name: sorted({wave[f"pilot_arg_{name}"] for wave in representative})[:4]
                  for name in operands}
        return {"label": "未感染", "operands_binary": values, "reached": len(reached)}
    modified, state = replay.trace(change.rtl(source), observe=tuple(names))
    if differences(trace, modified):
        raise RunError("Instrumented diagnostic contradicted the original output classification")
    intervals = []
    for name in names:
        start = None
        for i, (a, b) in enumerate(zip(waves, state, strict=True)):
            differs = a[name] != b[name] and not set(a[name]) - {"0", "1"}
            if differs and start is None:
                start = i
            if not differs and start is not None:
                resets = [key for key in replay.inputs if key in ("r", "reset", "areset", "rst")]
                reason = ("被复位" if any(replay.vectors[i][key] == 1 for key in resets)
                          else "被重新赋值")
                intervals.append({"signal": name, "first": start + 1, "equal_again": i + 1,
                                  "cause": reason})
                start = None
        if start is not None:
            intervals.append({"signal": name, "first": start + 1, "equal_again": None,
                              "cause": "采样结束时仍存在，输出未观察到差异"})
    cause = "下游赋值未产生可观察的状态差异"
    return {"label": "未传播", "first_infected": infected[0] + 1,
            "intervals": intervals, "cause": cause}
