"""Render the pilot and full reports from the archived evaluation summaries."""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"reports"


def load(name):
    return json.loads((REPORTS/name).read_text())


def csv_rows(name):
    path=REPORTS/name
    if not path.is_file():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def ratio(n,d):
    return f"{n/d:.2%}" if d else "—"


def pct(v):
    return f"{v:.2%}" if v is not None else "—"


def table(columns,rows):
    line=lambda values:"| "+" | ".join(map(str,values))+" |"
    return "\n".join([line(columns),line(["---"]*len(columns)),*(line(values) for values in rows)])


def show_metrics(summary):
    keys=("false_positive_macro","false_positive_pooled","H_macro","H_pooled")
    return table(("配置","计划运行","golden 可评分","生成失败","误报宏平均","误报 pooled","H 宏平均","H pooled",
                  "归属 Token","Go 用量 USD"),[
        [r["config"],r["runs"],r["golden_scored"],r["generation_failures"],*(pct(r[k]) for k in keys),
         f"{r['tokens']:,}",f"{r['go_usd']:.6f}"] for r in summary["macro"]])


def native(summary):
    modes={"Base":("Base","Base-think"),"Ours":("Ours","Ours-think")}
    runs={r["config"]:r for r in summary["macro"]}
    rows=[]
    for label,pair in modes.items():
        for switched,c in zip(("关","开"),pair,strict=True):
            r=runs[c]
            rows.append((label,switched,pct(r["false_positive_macro"]),pct(r["false_positive_pooled"]),
                         pct(r["H_macro"]),pct(r["H_pooled"]),f"{r['comparable_tokens']:,}",
                         f"{r['comparable_go_usd']:.6f}",f"{r['comparable_charged_usd']:.6f}"))
    return table(("方法","思考","误报宏平均","误报 pooled","H 宏平均","H pooled","可比 Token","Go USD","额外扣费 USD"),rows)


def paired(summary):
    rows=[]
    for rec in summary["paired"]:
        if rec["p"] is None:
            rows.append((rec["left"],rec["right"],rec["metric"],0,"—","—","—","—"))
            continue
        rows.append((rec["left"],rec["right"],rec["metric"],rec["task_pairs"],
                     f"{rec['difference_pp']:+.2f}",
                     f"[{rec['ci_low_pp']:+.2f}, {rec['ci_high_pp']:+.2f}]",
                     f"{rec['p']:.4g}",f"{rec['holm_p']:.4g}"))
    return table(("左侧","右侧","指标","题对","差值 pp","95% CI pp","Wilcoxon p","Holm p"),rows)


def diagnoses(phase,summary):
    reviews=csv_rows(f"{phase}_reviews.csv")
    by=defaultdict(Counter)
    keys=("issues","coverage","grounding","consistency","ambiguity","spec_example","tool_ambiguities",
          "tool_executable","no_effect","accepted","rebutted","retained")
    for r in reviews:
        k=(r["config"],r["round"])
        by[k]["rounds"]+=1
        by[k].update({key:int(r.get(key) or 0) for key in keys})
    rows=[]
    for (name,no), values in sorted(by.items()):
        rows.append((name,no,values["rounds"],values["issues"],
                     "/".join(str(values[key]) for key in keys[1:6]),
                     ratio(values["no_effect"],values["tool_executable"]),
                     ratio(values["accepted"],values["retained"]),
                     ratio(values["rebutted"],values["retained"])))
    blocks=csv_rows(f"{phase}_checks.csv")
    check_rows=[]
    m={r["config"]:r for r in summary["macro"]}
    for cfg in m:
        for check in ("A","B"):
            vals=[r for r in blocks if r["config"]==cfg and r["check"]==check]
            outcomes=Counter(r["effect"] for r in vals)
            if vals or m[cfg][f"{check}_blocked"]:
                check_rows.append((cfg,check,m[cfg][f"{check}_blocked"],len(vals),
                                   outcomes["false_positive_removed"],outcomes["false_positive_introduced"],
                                   outcomes["unscored"]))
    precision=csv_rows(f"{phase}_reviewer_precision.csv")
    precision_rows=[]
    for on in ("False","True"):
        for method in ("trace","no_trace"):
            included=[r for r in precision if r["think"]==on and f"/{method}/" in r["route"]]
            if included:
                counts=Counter(r["effect"] for r in included)
                precision_rows.append(("开" if on=="True" else "关",method,len(included),
                    *(counts[k] for k in ("decreased","unchanged","increased","unscored"))))
    flags=csv_rows(f"{phase}_resolution.csv")
    unresolved=[]
    for c in m:
        included=[r for r in flags if r["config"]==c and r["has_dispute"]=="True" and r["resolution"]!="skipped"]
        if included:
            not_resolved=sum(r["resolution"]=="unresolved_no_example" for r in included)
            unresolved.append((c,not_resolved,len(included),ratio(not_resolved,len(included))))
    links=" · ".join(f"[{k}]({phase}_{k}.csv)" for k in ("reviews","reviewer_precision","checks","resolution")
                     if (REPORTS/f"{phase}_{k}.csv").is_file())
    return [
        "## 审查、检查 A/B 和剩余分歧",
        "问题的五类顺序为覆盖 / 可追溯 / 一致性 / 歧义 / spec 例子。no_effect 分母为可执行的工具裁决，"
        "接受与反驳以保留的问题计。按配置报告时，共用的审查节点在各自方法口径中出现。",
        table(("配置","轮","轮次样本","问题","五类计数","no_effect","接受","反驳"),rows) if rows else "无完成的审查。",
        "逐条接受修改的前后模型均由 API 生成。减少、不变、增加按固定激励下 golden 不一致周期数判断。"
        "不可评分的编辑单列。诊断测量也可能受参考模型生成波动影响。",
        table(("思考","分支","编辑","减少","不变","增加","不可评分"),precision_rows)
        if precision_rows else "没有可归档的逐编辑比较。",
        table(("配置","检查","拦下","有前后对照的单元","误报消除","引入误报","不可评分"),check_rows)
        if check_rows else "未观察到拦截。",
        table(("配置","unresolved_no_example","有分歧单元","比例"),unresolved) if unresolved else "无可计算的剩余分歧。",
        links,
    ]


def false_cases():
    out=[]
    for task_dir in sorted((ROOT/"eval"/"full").iterdir()):
        for result in sorted(task_dir.glob("rep*.json")):
            entry=json.loads(result.read_text())
            ours=next(r for r in entry["outcomes"] if r["config"]=="Ours")
            if ours["golden_pass"] is not False:
                continue
            cycle=ours["first_golden_mismatches"][0]
            matched=[]
            for k in ("prior_golden","next_golden"):
                patterns=cycle.get(k)
                if patterns and all(all(b not in "01" or v==b for b,v in zip(patterns[name],
                    f"{want:0{len(patterns[name])}b}")) and any(bit in "01" for bit in patterns[name])
                    for name,want in cycle["expected"].items()):
                    matched.append(k)
            out.append({"task":entry["task"],"rep":entry["rep"],"cycle":cycle,
                        "neighbor_match":matched,
                        "final_contract":str((ROOT/"runs"/entry["task"]/f"rep{entry['rep']}"/
                                              "configs/Ours/final_contract.json").relative_to(ROOT))})
    (REPORTS/"false_positive_cases.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    return out


def render(phase):
    summary=load(f"{phase}_summary.json")
    archive=csv_rows(f"{phase}_by_run.csv")
    matched=load(f"{phase}_budget.json")
    pilot=phase=="pilot"
    sections=["# Contract-review "+("三题试运行" if pilot else "全量实验"),
              f"评测归档覆盖 {len(archive)} 个配置运行。所有激励均来自 v3 A0 初稿，保留 mid，"
              "Base 的 RTL 评分与 v3 A0 对照逐项一致。H 源码只由 eval 脚本读取。",
              "[预注册](../PREREG.md) · [逐次结果]("+phase+"_by_run.csv) · [逐题结果]("+phase+"_by_task.csv)",
              "## 两项主指标",show_metrics(summary),"## Base/Ours × 思考模式",native(summary),
              "可比用量为该配置所归属的合同、审查、裁决及检查器生成用量。Base 使用历史 A0 检查器调用的计量，"
              "本实验零新增调用。共享阶段在配置列可重复出现，整批账单按请求编号去重。",
              "## 题级配对",paired(summary)]
    if pilot:
        sections += ["三个题级配对的结果只用于检查流程，不用于解释主假设。",
                     "[契约、问题、裁决及回应样例](pilot_examples.json) · [流程门槛](pilot_gate.json)"]
    else:
        effects={(r["left"],r["right"],r["metric"]):r for r in summary["paired"]}
        for (label,left,right) in (("H1（对 Base）","Ours","Base"),("H1（对 CoT）","Ours","CoT"),
                                    ("H2","Ours","Ours-R0"),("H3","Ours","Ours-noTrace"),
                                    ("H4","Ours-think","Base-think")):
            entry=effects[left,right,"false_positive"]
            wording="缺少可配数据" if entry["p"] is None else (
                f"误报左减右 {entry['difference_pp']:+.2f} pp，"
                f"未校正 p={entry['p']:.4g}，Holm p={entry['holm_p']:.4g}。")
            if label.startswith("H1"):
                h=effects[left,right,"H"]
                if h["p"] is not None:
                    wording+=f"H 点差 {h['difference_pp']:+.2f} pp，95% CI [{h['ci_low_pp']:+.2f}, {h['ci_high_pp']:+.2f}]。"
            sections.append(f"- {label}。{wording}")
    sections.extend(diagnoses(phase,summary))
    cot=next(r for r in summary["macro"] if r["config"]=="CoT")
    actual=cot["tokens"]/cot["runs"] if cot["runs"] else 0
    gap=f"{(actual-matched['target'])/matched['target']:+.2%}" if matched["target"] else "—"
    u=summary["usage"]
    sections += ["## 用量、费用和例子",
                 f"CoT 目标 {matched['target']:,} token/运行，实测 {actual:,.1f}，偏差 "
                 f"{gap}。"
                 f"归档中去重后共 {u['calls']:,} 次逻辑调用、{u['attempts']:,} 次传输尝试、{u['tokens']:,} token，"
                 f"Go 用量 USD {u['go_usd']:.6f}、额外扣费 USD {u['charged_usd']:.6f}。",
                 "[每题例子长度](spec_examples.csv) · [五个抽查样例](spec_examples_review.json) · "
                 f"[原始统计]({phase}_summary.json)"]
    if not pilot:
        errors=false_cases()
        sections += ["## 完整案例与残余误报",
                     f"归档了 {summary['examples']} 个包含初始契约、两轮反馈、修订、最终模型及 golden 结果的案例。"
                     f"全量 Ours 的首个误报采样共 {len(errors)} 个，其中 {sum(bool(e['neighbor_match']) for e in errors)} 个"
                     "与相邻采样的已知位相符。这是时序错拍的线索。其余需要结合对应的状态、优先级或复位条款定位。",
                     "[完整案例](ten_cases.json) · [误报采样](false_positive_cases.json)"]
    (REPORTS/("PILOT.md" if pilot else "REPORT.md")).write_text("\n\n".join(s for s in sections if s)+"\n")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase",choices=("pilot","full"))
    render(p.parse_args().phase)
