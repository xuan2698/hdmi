"""Check lexical source reach and infection by executing the original expression."""

import re

from guide import ASSIGN, IF, span
from hdl import compile_sim, observe
from mutations import signals
from pilot3_guidance import derive
from replay import SimulationError


def site(atom):
    original, candidate = (atom[k].split("//", 1)[0] for k in ("before", "after"))
    before, after = (ASSIGN.fullmatch(t) for t in (original, candidate))
    if before and after and (before[2], before[3]) == (after[2], after[3]) and before[4] != after[4]:
        lhs = before[2]
        # A slice or indexed write still has an execution site, but is not used
        # as a top-scope monitor signal.
        return before.span(4), before[4], after[4], lhs, f"$bits({lhs})"
    a, b = IF.search(original), IF.search(candidate)
    if a and b and a[1] != b[1]:
        return a.span(1), a[1], b[1], "", "1"
    return None


def make_probe(row, atom, edit):
    offset, orig, alt, lhs, size = edit
    ports, code = row["ports"], row["gold"]
    widths = {**ports["input"], **ports["output"], **signals(code, ports["input"], ports["output"])}
    names = list(dict.fromkeys(n for n in re.findall(r"\b[A-Za-z_]\w*\b", orig+" "+alt) if n in widths))[:8]
    declarations, updates, final = [], [], []
    arguments = ["$bits(" + lhs + ")'(" + expr + ")" if lhs else "1'(" + expr + ")" for expr in (orig, alt)]
    for i, n in enumerate(names):
        arguments.append(n)
        declarations.append(f"reg [63:0] audit_min{i}='1, audit_max{i}=0; integer audit_n{i}=0;")
        updates.append(f"""if ((^arg{i}) !== 1'bx) begin
            if (arg{i}<audit_min{i}) audit_min{i}=arg{i};
            if (arg{i}>audit_max{i}) audit_max{i}=arg{i};
            audit_n{i}=audit_n{i}+1;
        end""")
        final.append(f'$display("RANGE {n} %0d %0d %0d", audit_n{i}, audit_min{i}, audit_max{i});')
    params = ", ".join([f"input [{size}-1:0] old_value, new_value"] +
                       [f"input [63:0] arg{i}" for i in range(len(names))])
    probe_code = f"""
integer audit_reached=0, audit_known=0, audit_infected=0, audit_first=0, audit_last=0;
{chr(10).join(declarations)}
function automatic [{size}-1:0] audit_probe({params});
  integer bit_index;
  reg different;
  begin
    audit_probe=old_value;
    audit_reached=audit_reached+1;
    if ((^old_value) !== 1'bx && (^new_value) !== 1'bx) audit_known=audit_known+1;
    different=0;
    for(bit_index=0;bit_index<{size};bit_index=bit_index+1) begin
      if ((old_value[bit_index] === 1'b0 || old_value[bit_index] === 1'b1)
          && old_value[bit_index] !== new_value[bit_index]) different=1;
    end
    if(different) begin
      if(audit_infected==0) audit_first=replay.cycle+1;
      audit_last=replay.cycle+1; audit_infected=audit_infected+1;
    end
    {chr(10).join(updates)}
  end
endfunction
final begin
    $display("PROBE %0d %0d %0d %0d %0d", audit_reached, audit_known, audit_infected, audit_first, audit_last);
    {chr(10).join(final)}
end
"""
    lines = code.splitlines()
    n = atom["line"] - 1
    lines[n] = lines[n][:offset[0]] + "audit_probe(" + ", ".join(arguments) + ")" + lines[n][offset[1]:]
    last_module_start = max(i for i, line in enumerate(lines[:n+1]) if re.match(r"^\s*module\b", line))
    last_module_end = next(i for i, line in enumerate(lines[n:], n) if re.match(r"^\s*endmodule\b", line))
    in_top = bool(re.search(r"\bmodule\s+" + re.escape(ports["top"]) + r"\b", lines[last_module_start]))
    lines.insert(last_module_end, probe_code)
    return "\n".join(lines)+"\n", names, in_top


def internals(row, atom, where, cycles, signal):
    if not re.fullmatch(r"\w+", signal):
        return None
    resets = " || ".join(f"({n}=={v})" for n,v in row["ports"]["resets"].items()) or "0"
    extra = f"""
integer probe_begin=0, probe_end=0, probe_reset=0;
reg probe_active=0;
always @(golden.{signal} or mutated.{signal}) begin
    #0.001;
    if ((^golden.{signal}) !== 1'bx && golden.{signal} !== mutated.{signal}) begin
        if (!probe_active && !probe_begin) probe_begin=cycle+1;
        probe_active=1;
    end else if (probe_active && (^golden.{signal}) !== 1'bx) begin
        if (!probe_end) begin probe_end=cycle+1; probe_reset=({resets}); end
        probe_active=0;
    end
end
final $display("LOCAL %0d %0d %0d",probe_begin,probe_end,probe_reset);
"""
    try:
        result = observe(compile_sim(row["gold"], span(row, atom), row["ports"], extra), where, cycles)
        begin, end, reset = map(int, re.search(r"LOCAL (\d+) (\d+) (\d+)", result["text"]).groups())
    except (SimulationError, RuntimeError, AttributeError):
        return None
    if begin:
        return {"signal": signal, "first_cycle": begin, "equal_again_cycle": end or None,
                "cause": "复位期间收敛" if reset else "信号更新后收敛，重赋值与掩蔽未区分" if end else "运行末尾仍无输出传播"}
    return None


def diagnose(row, atom, where, cycles):
    edit = site(atom)
    if not edit:
        return {"label": "诊断不可用", "reason": "结构或边沿变异没有可单独求值的原/变异表达式"}
    try:
        probe, _, at_top = make_probe(row, atom, edit)
        result = observe(compile_sim(probe, row["gold"], row["ports"]), where, cycles)
    except (SimulationError, RuntimeError, ValueError, StopIteration) as exc:
        return {"label": "诊断不可用", "reason": str(exc).splitlines()[0][-180:]}
    if result["samples"]:
        return {"label": "诊断不可用", "reason": "探针改变了输出"}
    text = result["text"]
    match = re.search(r"^PROBE (\d+) (\d+) (\d+) (\d+) (\d+)", text, re.M)
    if not match:
        return {"label": "诊断不可用", "reason": "未取得执行记录"}
    reached, known, infected, first, last = map(int, match.groups())
    ranges = {n: [int(lo), int(hi)] for n, hits, lo, hi in
              re.findall(r"^RANGE (\w+) (\d+) (\d+) (\d+)", text, re.M) if int(hits)}
    _, orig, alt, lhs, size = edit
    if not reached:
        return {"label": "未到达", "executions": 0}
    if not infected and not known:
        return {"label": "诊断不可用", "reason": "到达但没有可比较的确定表达式值"}
    if not infected:
        try:
            condition = derive({**atom, "orig": orig, "changed": alt}, {**row["ports"]["input"], **row["ports"]["output"]})
        except (ValueError, KeyError, IndexError):
            condition = None
        return {"label": "未感染", "condition": condition or f"执行时 ({orig}) 与 ({alt}) 在有效位宽内不等",
                "ranges": ranges, "executions": reached}
    interval = internals(row, atom, where, cycles, lhs) if lhs and at_top else None
    return {"label": "未传播", "rhs_first": first, "rhs_last": last,
            "interval": interval or {"signal": lhs or "predicate", "first_cycle": first,
                                    "equal_again_cycle": None,
                                    "cause": "变异表达式有差异，局部覆盖或下游掩蔽无法区分"}}
