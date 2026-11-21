"""Source-located procedural and event probes with four-state replay."""

import re
from dataclasses import dataclass
from functools import lru_cache

from base import WORK
from guide import span
from hdl import compile_sim, observe
from mutations import signals
from pilot3_guidance import derive
from pyslang import syntax
from replay import SimulationError

ERRORS = (SimulationError, RuntimeError, ValueError, AttributeError, IndexError)


@dataclass(frozen=True)
class Site:
    mode: str
    original: tuple
    mutant: tuple
    lhs: str = ""
    before: str = ""
    after: str = ""
    width: str = "1"
    module: str = ""
    operands: tuple = ()


def interval(node):
    return node.sourceRange.start.offset, node.sourceRange.end.offset


def text(source, node):
    start, end = interval(node)
    return source[start:end]


def nodes(source):
    root = syntax.SyntaxTree.fromText(source).root
    found = []
    root.visit(lambda n: found.append(n) if isinstance(n, syntax.SyntaxNode) else None)
    return found


def touches(node, start, end):
    left, right = interval(node)
    return left <= start and end <= right


def module_of(node):
    while node and not isinstance(node, syntax.ModuleDeclarationSyntax):
        node = node.parent
    return str(node.header.name).strip() if node else ""


def changed_bounds(a, b, line):
    a_lines, b_lines = a.splitlines(keepends=True), b.splitlines(keepends=True)
    x, y = a_lines[line-1], b_lines[line-1]
    first = 0
    while first < min(len(x),len(y)) and x[first] == y[first]:
        first += 1
    tail = 0
    while tail < min(len(x), len(y))-first and x[-tail-1] == y[-tail-1]:
        tail += 1
    pos = sum(map(len, a_lines[:line-1]))
    return (pos+first,pos+len(x)-tail), (pos+first,pos+len(y)-tail)


def assignment(node):
    if isinstance(node, syntax.ExpressionStatementSyntax):
        expr = node.expr
        if isinstance(expr, syntax.BinaryExpressionSyntax) and str(expr.operatorToken).strip() in ("=", "<="):
            return expr
    if isinstance(node, syntax.ContinuousAssignSyntax):
        return next((e for e in node.assignments if isinstance(e,syntax.BinaryExpressionSyntax)), None)
    return None


def select_node(index, bounds, match):
    candidates = [node for node in index if match(node) and touches(node,*bounds)]
    return min(candidates,key=lambda node: interval(node)[1]-interval(node)[0],default=None)


@lru_cache(maxsize=512)
def locate(gold, mutant, line, rule, candidates):
    before, after = changed_bounds(gold,mutant,line)
    a, b = nodes(gold), nodes(mutant)
    event = lambda n: isinstance(n,syntax.TimingControlStatementSyntax) and isinstance(n.timingControl,syntax.EventControlWithExpressionSyntax)
    old_event, new_event = select_node(a,before,event),select_node(b,after,event)
    if (old_event is not None and new_event is not None
            and (touches(old_event.timingControl,*before) or rule in ("clock_edge","EdgeInsert","EdgeDelete","temporal_reset"))):
        return Site("event",interval(old_event.statement),interval(new_event.statement),module=module_of(old_event))
    pred = lambda n: isinstance(n,syntax.ConditionalStatementSyntax)
    old_if, new_if = select_node(a,before,pred),select_node(b,after,pred)
    if old_if is not None and new_if is not None and touches(old_if.predicate,*before):
        one,two=text(gold,old_if.predicate),text(mutant,new_if.predicate)
        ops=tuple(n for n in candidates if re.search(rf"\b{re.escape(n)}\b",one+" "+two))[:4]
        return Site("condition",interval(old_if),interval(new_if),before=one,after=two,module=module_of(old_if),operands=ops)
    old_assign = select_node(a,before,assignment)
    if old_assign is None:
        return None
    original = assignment(old_assign)
    lhs = text(gold,original.left)
    one = text(gold,original.right)
    mode = "continuous" if isinstance(old_assign,syntax.ContinuousAssignSyntax) else "value"
    new_assign = select_node(b,after,assignment)
    two, new_site = "", ()
    if new_assign is not None:
        updated=assignment(new_assign)
        if text(mutant,updated.left) != lhs:
            return None
        two=text(mutant,updated.right)
        new_site=interval(new_assign)
        if str(original.operatorToken).strip() != str(updated.operatorToken).strip():
            mode="schedule"
    elif rule == "NSubDelete":
        two=lhs
    elif rule.startswith("NSubInsert"):
        group = select_node(b,after,lambda n:isinstance(n,syntax.BlockStatementSyntax))
        if group is None:
            return None
        writes=[assignment(n) for n in b if touches(group,*interval(n)) and assignment(n) is not None]
        if not writes or any(text(mutant,what.left)!=lhs for what in writes):
            return None
        two=text(mutant,writes[-1].right)
        new_site=interval(group)
    else:
        return None
    operands=tuple(n for n in candidates if re.search(rf"\b{re.escape(n)}\b",one+" "+two))[:4]
    return Site(mode,interval(old_assign),new_site,lhs,one,two,f"$bits({lhs})",module_of(old_assign),operands)


def wrap(source, bounds, statement):
    start,end=bounds
    return source[:start]+"begin "+statement+" "+source[start:end]+" end"+source[end:]


def continuous(source, bounds, statement):
    _,end=bounds
    return source[:end]+"\nalways @* "+statement+"\n"+source[end:]


def value_call(site, raw=False):
    if site.mode == "condition":
        # Procedural if treats unknown as false. Keep the exact truth value
        # before applying this rule to the two branch decisions.
        before=f"((|({site.before})) === 1'b1)"
        after=f"((|({site.after})) === 1'b1)"
    else:
        before=f"{site.width}'({site.before})"
        after=f"{site.width}'({site.after})"
    if raw:
        return f'$display("RAWVALUE %0d %b %b", replay.cycle+1, {before}, {after});'
    operands=", ".join([*site.operands,*(["64'd0"]*(4-len(site.operands)))])
    return f"replay.record_value({site.width}, {before}, {after}, {operands});"


TRACK = """
integer executions=0, comparable=0, infections=0, first_infection=0, last_infection=0;
integer site_width=0;
reg [255:0] first_old=0, first_new=0;
integer seen [0:3];
reg [63:0] lo [0:3], hi [0:3];
integer k;
initial for(k=0;k<4;k=k+1) begin seen[k]=0;lo[k]='1;hi[k]=0; end
task automatic record_value(input integer width, input [255:0] a, b, input [63:0] p0,p1,p2,p3);
    reg diff, known;
    reg [63:0] operand;
    integer i;
    begin
        executions=executions+1;
        site_width=width;
        diff=0; known=0;
        if ((^a) !== 1'bx && (^b) !== 1'bx) begin
            known=1; diff=a!==b;
        end else begin
            for(i=0;i<width && i<256;i=i+1) begin
                if (a[i]===1'b0 || a[i]===1'b1) begin
                    known=1;
                    if (a[i]!==b[i]) diff=1;
                end
            end
        end
        if(known) comparable=comparable+1;
        if(diff) begin
            if(infections==0) begin
                first_infection=cycle+1; first_old=a; first_new=b;
            end
            last_infection=cycle+1; infections=infections+1;
        end
        for(i=0;i<4;i=i+1) begin
            case(i)
              0:operand=p0;
              1:operand=p1;
              2:operand=p2;
              3:operand=p3;
            endcase
            if((^operand)!==1'bx) begin
                seen[i]=seen[i]+1;
                if(operand<lo[i]) lo[i]=operand;
                if(operand>hi[i]) hi[i]=operand;
            end
        end
    end
endtask
integer changed_outputs=0;
always @(posedge phase, negedge phase) if(ref_bits !== mut_bits) changed_outputs=changed_outputs+1;
final begin
  $display("SITE %0d %0d %0d %0d %0d %0d %h %h %0d",executions,comparable,infections,
           first_infection,last_infection,site_width,first_old,first_new,changed_outputs);
  for(k=0;k<4;k=k+1) $display("OPERAND %0d %0d %0d %0d",k,seen[k],lo[k],hi[k]);
end
"""

EVENT = """
integer left_times[0:220000],right_times[0:220000];
integer event_index, left_total=0, right_total=0, first_delta=0, last_delta=0, event_deltas=0;
task automatic record_event(input integer tag);
    integer stamp;
    begin
        stamp=$time;
        if(tag==0) begin
            if ((^left_times[stamp])===1'bx) left_times[stamp]=0;
            left_times[stamp]=left_times[stamp]+1; left_total=left_total+1;
        end else begin
            if ((^right_times[stamp])===1'bx) right_times[stamp]=0;
            right_times[stamp]=right_times[stamp]+1; right_total=right_total+1;
        end
    end
endtask
final begin
    for(event_index=0;event_index<=cycles*11;event_index=event_index+1) begin
       if (left_times[event_index] !== right_times[event_index]) begin
           if(!event_deltas) first_delta=1+event_index/11;
           last_delta=1+event_index/11;
           event_deltas=event_deltas+1;
       end
    end
    $display("EVENT %0d %0d %0d %0d %0d",left_total,right_total,event_deltas,first_delta,last_delta);
end
"""


def run_extra(row, mutant, where, cycles, extra, gold=None):
    binary=compile_sim(gold if gold is not None else row["gold"],mutant,row["ports"],extra)
    return observe(binary,where,cycles)


def parse_line(result, pattern, base=10):
    match=re.search(pattern,result["text"],re.M)
    if not match:
        raise ValueError("probe output missing")
    return tuple(int(value,base) for value in match.groups())


def wave_extra(lhs, compare_delta=False):
    settle = "#0;" if compare_delta else "#0.001;"
    return f"""
integer wave_checks=0,wave_bad=0,wave_first=0,wave_end=0;
reg wave_live=0;
always @(golden.{lhs} or mutated.{lhs}) begin
  {settle}
  if ((^golden.{lhs})!==1'bx) begin
    wave_checks=wave_checks+1;
    if(golden.{lhs}!==mutated.{lhs}) begin
      if(!wave_bad) wave_first=cycle+1;
      wave_bad=wave_bad+1; wave_live=1;
    end else if(wave_live && wave_end==0) begin
      wave_end=cycle+1; wave_live=0;
    end
  end
end
final $display("WAVE %0d %0d %0d %0d",wave_checks,wave_bad,wave_first,wave_end);
"""


def local_trace(row, mutant, site, where, cycles, schedule=False):
    lhs=re.match(r"^[a-zA-Z_]\w*",site.lhs)
    if not lhs or site.module!=row["ports"]["top"]:
        return {}
    try:
        output=run_extra(row,mutant,where,cycles,wave_extra(lhs[0],schedule))
        count,bad,first,end=parse_line(output,r"^WAVE (\d+) (\d+) (\d+) (\d+)")
    except ERRORS:
        return {}
    return {"signal":lhs[0],"known_samples":count,"differing_samples":bad,"first_cycle":first or None,
            "equal_again_cycle":end or None,
            "cause":"局部信号重新一致，重新赋值与掩蔽未区分" if end else
                    "未观测到局部信号再一致" if bad else "未观测到已知位局部差异"}


def unavailable(reason, mode=None):
    return {"label":"诊断不可用","reason":reason,"mode":mode}


def diagnose(row, atom, where, cycles):
    gold, variant = row["gold"], span(row,atom)
    ports=row["ports"]
    available=tuple({**ports["input"], **ports["output"], **signals(gold,ports["input"],ports["output"])})
    try:
        site=locate(gold,variant,atom["line"],atom["rule"],available)
    except ERRORS as exc:
        return unavailable(f"语法定位异常 {str(exc)[-150:]}")
    if site is None:
        return unavailable("无法将变更映射到一个可比较的值、分支或事件站点")
    try:
        if site.mode=="event":
            original=wrap(gold,site.original,"replay.record_event(0);")
            edited=wrap(variant,site.mutant,"replay.record_event(1);")
            output=run_extra(row,edited,where,cycles,EVENT,original)
            left,right,delta,first,last=parse_line(output,r"^EVENT (\d+) (\d+) (\d+) (\d+) (\d+)")
            if output["samples"]:
                return unavailable("事件探针改变了公开比较",site.mode)
            labels="未传播" if delta else "未感染" if left or right else "未到达"
            return {"label":labels,"mode":site.mode,"executions":left,"mutant_executions":right,
                    "activation_delta_samples":delta,"first_cycle":first or None,"last_cycle":last or None}
        if site.mode=="schedule":
            probe=wrap(gold,site.original,value_call(site))
        else:
            insert=continuous if site.mode=="continuous" else wrap
            probe=insert(gold,site.original,value_call(site))
        output=run_extra(row,gold,where,cycles,TRACK,probe)
        match=re.search(r"^SITE (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\w+) (\w+) (\d+)",output["text"],re.M)
        if not match:
            return unavailable("值探针没有返回统计",site.mode)
        count,known,bad,first,last,width=map(int,match.groups()[:6])
        if output["samples"] or int(match[9]):
            return unavailable("值探针改变了公开输出的四态取值",site.mode)
        data={"mode":site.mode,"executions":count,"comparable":known}
        if not count:
            return {"label":"未到达",**data}
        local=local_trace(row,variant,site,where,cycles,schedule=site.mode=="schedule") if (bad or site.mode=="schedule") else {}
        if site.mode=="schedule":
            if local.get("differing_samples"):
                return {"label":"未传播","interval":local,**data}
            return unavailable("赋值调度差异没有足够的可证据化采样",site.mode)
        if width>256 or not known:
            return unavailable("表达式位宽或未知位阻止有效比较",site.mode)
        if bad:
            return {"label":"未传播","rhs_first":first,"rhs_last":last,"infections":bad,
                    "first_values_hex":[t[-max(1,(width+3)//4):] for t in match.groups()[6:8]],
                    "interval":local or {"signal":site.lhs or "predicate","first_cycle":first,
                                         "equal_again_cycle":None,"cause":"已观测表达式差异，后续消除位置未解析"},**data}
        ranges={}
        for k, hit, lo, hi in re.findall(r"^OPERAND (\d+) (\d+) (\d+) (\d+)",output["text"],re.M):
            if int(k)<len(site.operands) and int(hit):
                ranges[site.operands[int(k)]]=[int(lo),int(hi)]
        try:
            condition=derive({**atom,"orig":site.before,"changed":site.after},{**ports["input"],**ports["output"]})
        except ERRORS:
            condition=None
        return {"label":"未感染","condition":condition or f"有效位宽内 ({site.before}) 与 ({site.after}) 不同",
                "ranges":ranges,**data}
    except ERRORS as exc:
        return unavailable(str(exc).splitlines()[0][-200:],site.mode)
