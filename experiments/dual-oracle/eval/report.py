"""Report pre-registered comparisons and independently scored diagnostics."""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from api import ledger, usage
from data import EVALUATION, PLAN, REPORTS, RUNS, TOKEN_PLAN, case_path, interface, load, roster, save
from pilot3_report import exact_signed_rank

CONTRASTS = ("Base-think", "Vote-think", "Ours-noTB", "Ours-noArbiter")
DIAG_FIELDS = ("compared_cycles", "compared_samples", "known_samples", "disagreement_cycles",
               "disagreement_samples", "TB_wrong_samples", "RM_wrong_samples", "common_mode_samples")


def csv_file(phase, name, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (REPORTS / f"{phase}_{name}.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def proportion(a, b):
    return a / b if b else None


def rate(rows, metric):
    if all(r["status"] == "not_run_gate" for r in rows):
        return None
    if metric == "H":
        return proportion(sum(r["H_detected"] for r in rows), sum(r["H_total"] for r in rows))
    scored = sum(r["golden_pass"] is not None for r in rows)
    return proportion(sum(r["golden_pass"] is False for r in rows),
                      len(rows) if metric == "FP_planned" else scored)


def gather(cases, phase):
    runs, mutants, scenes, judges, stages = [], [], [], [], []
    for case in cases:
        ids = {k: case[k] for k in ("group", "task", "seed")}
        for arm in case["outcomes"]:
            prefix = {**ids, "config": arm["config"]}
            for mode in ("primary", "secondary"):
                if (rec := arm[mode]) is None:
                    continue
                runs.append({**prefix, "mode": mode, "status": arm["status"], "failure": arm.get("failure"),
                             "fixed_cycles": case["fixed_cycles"], **arm["usage"],
                             **{f"historical_{k}": v for k,v in arm.get("historical_usage", {}).items()},
                             **{k: rec[k] for k in ("golden_pass", "golden_failed_samples", "H_total",
                                                    "H_detected", "H_simulation_errors")},
                             "execution_error": rec.get("execution_error")})
                mutants.extend({**prefix, "mode": mode, **r} for r in rec["mutants"])
            scenes.extend({**prefix, "stage": "final", **r} for r in arm.get("final_diagnostic", {}).get("scenes", []))
            judges.extend({**prefix, **r, "input_history": json.dumps(r["input_history"])} for r in arm.get("decisions", []))
        for stage, rec in case["stages"].items():
            stages.append({**ids, "stage": stage, "golden_pass": rec["golden_pass"],
                           "golden_failed_samples": rec["golden_failed_samples"]})
            scenes.extend({**ids, "config": "RM-stages", "stage": stage, **r}
                          for r in (rec["directed"] or {}).get("scenes", []))
    for name, rows in (("by_run", runs), ("by_mutant", mutants), ("scene_metrics", scenes),
                       ("judgments", judges), ("rm_stages", stages)):
        csv_file(phase, name, rows)
    return runs, scenes, judges, stages


def phase_artifacts(phase):
    limit = load(REPORTS / f"{phase}_generation.json")["N"]
    for group, task, seed in roster(phase):
        home = case_path(group, task, seed)
        for log in sorted(home.rglob("calls.jsonl")):
            path = log.parent
            relative = path.relative_to(home)
            if relative.parts[0] == "vote" and int(relative.name.removeprefix("rm")) > limit:
                continue
            yield group, task, seed, path, relative


def generation_paths(phase):
    rows = []
    for group, task, seed, path, relative in phase_artifacts(phase):
        records = ledger(path)
        if not records:
            continue
        if any(r.get("max_tokens") != TOKEN_PLAN["max_tokens"] or r.get("model_requested") != PLAN["model"]
               or r.get("thinking") != PLAN["thought"] for r in records):
            raise ValueError(f"Mixed inference settings in {path.relative_to(RUNS)}")
        status = load(path / "status.json") if (path / "status.json").is_file() else None
        rows.append({"group": group, "task": task, "seed": seed, "path": relative.as_posix(),
                     "status": "unfinished" if status is None else ("ready" if status["ok"] else "failed"),
                     "last_error": "; ".join(status["errors"][-1:]) if status else None,
                     "truncated_transports": sum(r.get("truncated", False) for r in records),
                     "transport_failures": sum(r["status"] != "received" for r in records),
                     **usage([path])})
    csv_file(phase, "generation_paths", rows)
    counts = {key: sum(r["status"] == key for r in rows) for key in ("ready", "failed", "unfinished")}
    counts["terminal"] = counts["ready"] + counts["failed"]
    counts["failure_rate"] = proportion(counts["failed"], counts["terminal"])
    return counts


def by_task_diagnostics(phase, scenes, judgments):
    scene_groups, judgment_groups, points = defaultdict(list), defaultdict(list), defaultdict(dict)
    for row in scenes:
        key = (row["group"], row["task"], row["config"], row["stage"])
        scene_groups[key].append(row)
    for row in judgments:
        if not row["spec_quote"]:
            continue
        fields = ("group", "task", "config")
        key = tuple(row[f] for f in fields)
        judgment_groups[key].append(row)
        point = (*key, row["seed"], row["scene"], row["sample"], row["output"], row["input_history"])
        if row["round"] in points[point]:
            raise ValueError(f"Repeated adjudication in the same round: {point[:-1]}")
        points[point][row["round"]] = row
    common, scored, repeat, flips = [], [], defaultdict(list), []
    for key, rows in scene_groups.items():
        group, task, config, stage = key
        known = sum(r.get("known_samples", 0) for r in rows)
        wrong = sum(r.get("common_mode_samples", 0) for r in rows)
        common.append({"group": group, "task": task, "config": config, "stage": stage,
                       "known_samples": known, "common_mode_samples": wrong, "rate": proportion(wrong, known)})
    for point, both in points.items():
        if set(both) != {1, 2}:
            continue
        before, after = both[1], both[2]
        changed = before["verdict"] != after["verdict"]
        repeat[point[:3]].append(changed)
        if changed:
            flips.append({"group": point[0], "task": point[1], "config": point[2], "seed": point[3],
                          "scene": point[4], "sample": point[5], "output": point[6], "input_history": point[7],
                          "round1": before["verdict"], "round2": after["verdict"],
                          "candidate_values_changed": (before["RM"], before["TB"]) != (after["RM"], after["TB"]),
                          "round1_correct": before["correct"], "round2_correct": after["correct"]})
    for key, rows in judgment_groups.items():
        labels = ("all", "RM", "TB", "ambiguous")
        for label in labels:
            chosen = [r for r in rows if label == "all" or r["verdict"] == label]
            valid = [r["correct"] for r in chosen if r["correct"] is not None]
            scored.append({"group": key[0], "task": key[1], "config": key[2], "label": label,
                           "judged": len(chosen), "scored": len(valid), "correct": sum(valid),
                           "accuracy": proportion(sum(valid), len(valid)),
                           "judged_both_rounds": len(repeat[key]) if label == "all" else None,
                           "flips": sum(repeat[key]) if label == "all" else None})
    csv_file(phase, "common_mode_by_task", common)
    csv_file(phase, "judgment_by_task", scored)
    csv_file(phase, "judgment_flips", flips)
    save(REPORTS / f"{phase}_judgment_flips.json", flips)
    return common, scored


def summaries(runs, phase):
    by_task, by_arm = defaultdict(list), defaultdict(list)
    for r in runs:
        key = r["group"], r["mode"], r["config"]
        by_arm[key].append(r)
        by_task[(*key, r["task"])].append(r)
    task = {}
    for (group, mode, arm, title), values in by_task.items():
        task[group, mode, arm, title] = {"group": group, "mode": mode, "config": arm, "task": title,
            "scored": sum(x["golden_pass"] is not None for x in values), "planned": len(values),
            **{metric: rate(values, metric) for metric in ("FP", "FP_planned", "H")}}
    result = []
    for (group, mode, arm), values in by_arm.items():
        row = {"group": group, "mode": mode, "config": arm, "scored": sum(x["golden_pass"] is not None for x in values),
               "planned": len(values), "failures": sum(x["status"]=="generation_failed" for x in values),
               "stopped": sum(x["status"]=="not_run_gate" for x in values),
               "tokens": sum(x["tokens"] for x in values), "go_usd": sum(x["go_usd"] for x in values),
               "charged_usd": sum(x["charged_usd"] for x in values),
               "historical_tokens": sum(x.get("historical_tokens",0) for x in values)}
        for field in ("FP", "H"):
            observed = [r[field] for k,r in task.items() if k[:3]==(group,mode,arm) and r[field] is not None]
            row.update({field+"_macro": mean(observed) if observed else None, field+"_pooled": rate(values,field),
                        field+"_macro_tasks":len(observed)})
        result.append(row)
    csv_file(phase,"by_task",list(task.values()))
    csv_file(phase,"summary",result)
    return task,result


def paired(task, phase):
    exports = []
    for group in ("A","B"):
        names = sorted({k[3] for k in task if k[0]==group})
        official = []
        for mode in ("primary","secondary"):
            for right in CONTRASTS:
                for metric in ("FP","H"):
                    for scope in ("planned","jointly_scoreable"):
                        deltas = []
                        for name in names:
                            a = task.get((group,mode,"Ours",name))
                            b = task.get((group,mode,right,name))
                            if a is None or b is None or (scope=="jointly_scoreable" and not (a["scored"] and b["scored"])):
                                continue
                            field = "FP_planned" if scope=="planned" and metric=="FP" else metric
                            if a[field] is not None and b[field] is not None:
                                deltas.append(round(a[field]-b[field],12))
                        row = {"group":group,"mode":mode,"control":right,"metric":metric,"scope":scope,
                               "pairs":len(deltas)}
                        if deltas:
                            d = np.array(deltas)
                            stat,p,n = exact_signed_rank(d)
                            rng = np.random.default_rng(PLAN["bootstrap_seed"])
                            draws = rng.choice(d,size=(PLAN["bootstrap_draws"],len(d)),replace=True).mean(axis=1)
                            q1,q2 = np.percentile(draws*100,[2.5,97.5])
                            row.update(delta_pp=float(d.mean()*100),ci_low_pp=float(q1),ci_high_pp=float(q2),
                                       p=p,stat=stat,nonzero=n)
                            if mode=="primary" and ((metric=="FP" and scope=="jointly_scoreable") or
                                                     (metric=="H" and scope=="planned")):
                                official.append(row)
                        exports.append(row)
        running = 0
        for i,row in enumerate(sorted(official,key=lambda r:r["p"])):
            running = max(running,min(1,row["p"]*(len(official)-i)))
            row["holm_p"] = running
    csv_file(phase,"paired",exports)
    return exports


def diagnostics(data, judgments, stages, phase):
    grouped = defaultdict(list)
    for row in data:
        grouped[row["group"],row["config"],row["stage"]].append(row)
    scene = []
    for (group,arm,stage),rows in grouped.items():
        metrics={k:sum(r.get(k,0) for r in rows) for k in DIAG_FIELDS}
        known=metrics["known_samples"]
        scene.append({"group":group,"config":arm,"stage":stage,**metrics,
                      "disagreement":proportion(metrics["disagreement_cycles"],metrics["compared_cycles"]),
                      "common_mode":proportion(metrics["common_mode_samples"],known),
                      "TB_accuracy":proportion(known-metrics["TB_wrong_samples"],known)})
    decisions, stage_result = [], []
    for group in ("A","B"):
        for stage in ("initial","reviewed","final"):
            items=[r["golden_pass"] for r in stages if (r["group"],r["stage"])==(group,stage)]
            scored=sum(x is not None for x in items)
            stage_result.append({"group":group,"stage":stage,"scored":scored,
                                 "FPR":proportion(sum(x is False for x in items),scored)})
        chosen=[r for r in judgments if r["group"]==group and r["config"]=="Ours"]
        for by in ("verdict","actual"):
            for label in ("RM","TB","ambiguous","both_wrong","untraceable"):
                subset=[r for r in chosen if r[by]==label]
                rated=[r["correct"] for r in subset if r["correct"] is not None]
                repairs=[r["repair_success"] for r in subset if r["repair_success"] is not None]
                decisions.append({"group":group,"classified_by":by,"label":label,"count":len(subset),
                                  "scored":len(rated),"correct":sum(rated),
                                  "confirmed_rate":proportion(sum(rated),len(rated)),
                                  "repairs_scored":len(repairs),"repair_success":proportion(sum(repairs),len(repairs))})
    for name,rows in (("diagnostic_summary",scene),("judgment_summary",decisions),("rm_stage_summary",stage_result)):
        csv_file(phase,name,rows)
    return scene,decisions,stage_result


def examples(cases,phase):
    samples,common,wrong,complete={},[],[],[]
    for case in cases:
        group,task,seed = (case[x] for x in ("group","task","seed"))
        ids={"group":group,"task":task,"seed":seed}
        h=case_path(group,task,seed)
        ours=next(row for row in case["outcomes"] if row["config"]=="Ours")
        rm,review,reply,tb = [h/p for p in ("rm/model.py","review/value.json","review_reply.json","tb/value.json")]
        if rm.is_file():
            samples.setdefault("RM",{**ids,"source":rm.read_text()})
        if review.is_file() and load(review):
            response=load(reply)["responses"] if reply.is_file() else None
            if "review" not in samples or (response and not samples["review"]["responses"]):
                samples["review"]={**ids,"issues":load(review),"responses":response}
        if tb.is_file():
            samples.setdefault("TB",{**ids,"scene":load(tb)[0]})
        rounds=[]
        for folder in sorted((h/"standard").glob("round*")):
            before,after=folder/"disagreements.json",folder/"outcome.json"
            pre_repair = folder / "arbiter/value.json"
            if before.is_file() and load(before)["points"]:
                samples.setdefault("disagreement",{**ids,**load(before)["points"][0]})
            if pre_repair.is_file() and load(pre_repair):
                samples.setdefault("judgment",{**ids,**load(pre_repair)[0]})
            if after.is_file():
                result=load(after)
                rounds.append({"round":folder.name,"before":load(before),"after":result})
                if result["decisions"]:
                    samples.setdefault("judgment",{**ids,**result["decisions"][0]})
                if any(x["label"]!="ambiguous" for x in result["decisions"]):
                    samples.setdefault("repair",{**ids,**result})
        common.extend({**ids,"stage":"Ours-final",**r}
                      for r in ours.get("final_diagnostic",{}).get("common_examples",[]))
        if phase=="pilot":
            for stage in ("initial","reviewed"):
                directed=case["stages"].get(stage,{}).get("directed") or {}
                common.extend({**ids,"stage":stage,**r} for r in directed.get("common_examples",[]))
            mid=next(row for row in case["outcomes"] if row["config"]=="Ours-R1")
            common.extend({**ids,"stage":"Ours-R1",**r}
                          for r in mid.get("final_diagnostic",{}).get("common_examples",[]))
        wrong.extend({**ids,**r} for r in ours.get("decisions",[]) if r["correct"] is False)
        if ours["status"]=="ready" and rounds and all(p.is_file() for p in (rm,review,reply,tb)):
            complete.append({**ids,"spec_excerpt":interface(group,task)["spec"][:1800],
                "initial_RM":rm.read_text(),"review":load(review),"response":load(reply),"TB":load(tb),
                "rounds":rounds,"final_RM":(ROOT/ours["model"]).read_text(),"golden_and_H":ours["primary"]})
    save(REPORTS/f"{phase}_examples.json",samples)
    if phase=="pilot":
        save(REPORTS/"pilot_common_mode_examples.json",common)
        save(REPORTS/"pilot_arbiter_error_examples.json",wrong)
    if phase=="full":
        picked=[]
        for group in ("A","B"):
            unique={}
            for r in complete:
                if r["group"]==group:
                    unique.setdefault(r["task"],r)
            picked.extend(list(unique.values())[:5])
        picked.extend(r for r in complete if r not in picked)
        save(REPORTS/"ten_cases.json",picked[:10])
        save(REPORTS/"common_mode_examples.json",common)
        save(REPORTS/"arbiter_error_examples.json",wrong)
    return {"complete":len(complete),"common":len(common),"arbitration_error":len(wrong),
            "sample_stages":list(samples)}


def pct(value):
    return "—" if value is None else f"{value:.2%}"


def table(header,rows):
    return "\n".join(["| "+" | ".join(header)+" |","| "+" | ".join("---" for _ in header)+" |",
                      *["| "+" | ".join(map(str,row))+" |" for row in rows]])


def render(phase,summary,pairs,diag,judgments,stages,samples,paths,by_task):
    gen=load(REPORTS/f"{phase}_generation.json")
    bill=usage(path for _, _, _, path, _ in phase_artifacts(phase))
    vote = f"Vote-think 使用 {gen['N']} 个独立成员。" if gen["N"] else "Vote-think 的 N 未完成标定。"
    stop = f"{gen['stopped']} 个配置因停止规则封存。" if gen.get("stopped") else ""
    text=["# Dual-oracle "+("五题试运行" if phase=="pilot" else "全量结果"),
          f"计划 {gen['configs']} 个配置，{gen['failures']} 个生成失败"
          f"（{gen['failures']/gen['configs']:.2%}，门槛用此口径）。"+stop+vote+
          "CVDP golden 自回放在 50 份冻结输入上通过。",
          f"独立生成路径有 {paths['failed']}/{paths['terminal']} 条失败（{pct(paths['failure_rate'])}），"
          f"另有 {paths['unfinished']} 条未达终态。按独立产物目录统计，重试只计一路。"
          f"[逐路径数据]({phase}_generation_paths.csv) · [接口核对](../TOKEN_LIMIT.md)",
          "[预注册](../../PREREG.md) · [逐次结果]("+phase+"_by_run.csv) · [逐题结果]("+phase+"_by_task.csv)",
          "## 主指标和追加场景评测",
          "误报率基于可评分检查器。生成失败保留在 H 的计划分母并计零检出。所有单元均在门槛处封存的配置显示为空。"
          "部分封存时 H 为已观测的计划分母下界。追加评测沿同一场景输入顺序接到 A0 之后。",
          table(("组","配置","激励","可评分/计划","误报 macro","误报 pooled","H macro","H pooled","新增 Token","Go USD"),[
            (r["group"],r["config"],r["mode"],f'{r["scored"]}/{r["planned"]}',pct(r["FP_macro"]),pct(r["FP_pooled"]),
             pct(r["H_macro"]),pct(r["H_pooled"]),r["tokens"],f'{r["go_usd"]:.5f}') for r in summary]),
          "## 题级配对",
          "误报的主比较使用双方均可评分的题，H 主比较使用全部计划题。计划分母误报下界和共同可评分 H 另列在 CSV。"
          "正差意味着 Ours 较高。A/B 分别做主比较 Holm 校正。",
          table(("组","对照","指标","题对","差值 pp","95% CI pp","Wilcoxon p","Holm p"),[
            (r["group"],r["control"],r["metric"],r["pairs"],f'{r["delta_pp"]:+.2f}',
             f'[{r["ci_low_pp"]:+.2f}, {r["ci_high_pp"]:+.2f}]',f'{r["p"]:.4g}',f'{r["holm_p"]:.4g}')
             for r in pairs if "holm_p" in r]),"[全部配对]("+phase+"_paired.csv)",
          "## 共模错误和裁决",
          "共模错误分母为至少一个已知 golden 位的采样点。裁决表中的 ambiguous 表示 golden 已知位无法区分候选。"
          "此标签只衡量观测值。两边都错误时单列。",
          table(("组","配置","阶段","分歧拍率","共模错误","TB 准确率","已知采样"),[
            (r["group"],r["config"],r["stage"],pct(r["disagreement"]),pct(r["common_mode"]),pct(r["TB_accuracy"]),
             r["known_samples"]) for r in diag]),
          table(("组","核对分组","类别","点数","可追溯","核对率","修正可评分","修正成功率"),[
            (r["group"],r["classified_by"],r["label"],r["count"],r["scored"],pct(r["confirmed_rate"]),r["repairs_scored"],
             pct(r["repair_success"])) for r in judgments]),
          table(("组","RM 阶段","可评分","误报率"),[(r["group"],r["stage"],r["scored"],pct(r["FPR"])) for r in stages]),
          "## 用量和案例",
          f"本阶段配置使用的收据去重后共 {bill['calls']:,} 次逻辑调用、{bill['attempts']:,} 次传输、{bill['tokens']:,} token，"
          f"Go 用量 USD {bill['go_usd']:.6f}，额外扣费 USD {bill['charged_usd']:.6f}。"
          "历史 Base-think 用量在原始结果中单列。共享节点在配置归属用量中可重复出现。",
          f"可归档完整 Ours 单元 {samples['complete']} 个，共模错误场景 {samples['common']} 个，"
          f"裁决与观测不符 {samples['arbitration_error']} 个点。"]
    if phase=="pilot":
        text.append("[试运行各阶段样例](pilot_examples.json) · [共模错误](pilot_common_mode_examples.json) · "
                    "[裁决错误](pilot_arbiter_error_examples.json) · [门槛](pilot_gate.json)")
        if gen.get("stopped"):
            text.append("停止前的场景归档发现了 ID 碰撞。配对按输入历史和原 TB 值追溯，不能唯一定位的点单列。"
                        "碰撞路径上的 TB 定点修正不计成功率。原始生成产物保持归档。")
    else:
        common, scored = by_task
        calibration = load(REPORTS / "pilot_vote_budget.json")
        method_tokens = {
            arm: sum(row["tokens"] for row in summary if row["mode"] == "primary" and row["config"] == arm)
            / gen["cases"] for arm in ("Ours", "Vote-think")
        }
        text.append(
            f"正式 N={gen['N']}。五题标定中 Ours 平均 {calibration['target']:,.1f} token，"
            f"同一 N 的投票平均 {calibration['mean_tokens']:,.1f}。全量 Ours 平均 "
            f"{method_tokens['Ours']:,.1f}，全量 Vote-think 平均 {method_tokens['Vote-think']:,.1f}。"
            "[标定候选](pilot_vote_budget.json)"
        )
        totals = {(x["group"], x["task"]): x for x in common if x["config"] == "Ours" and x["stage"] == "final"}
        judge = {(x["group"], x["task"]): x for x in scored if x["config"] == "Ours" and x["label"] == "all"}
        task_list = sorted({(group, task) for group, task, _ in roster("full")})
        text += ["## 逐题共模错误和裁决翻转",
                 table(("组","题","共模错误/已知采样","裁决正确/可评分","翻转/两轮均裁决"),[
                   (g,t,f'{m.get("common_mode_samples",0)}/{m.get("known_samples",0)}',
                    f'{j.get("correct",0)}/{j.get("scored",0)}',
                    f'{j.get("flips",0)}/{j.get("judged_both_rounds",0)}')
                   for g,t in task_list for m,j in [(totals.get((g,t),{}),judge.get((g,t),{}))]]),
                 f"[逐题共模 CSV]({phase}_common_mode_by_task.csv) · [逐题裁决 CSV]({phase}_judgment_by_task.csv) · "
                 f"[翻转明细]({phase}_judgment_flips.json)"]
        text.append("[完整案例](ten_cases.json) · [共模错误案例](common_mode_examples.json) · [裁决错误案例](arbiter_error_examples.json)")
    (REPORTS/("PILOT.md" if phase=="pilot" else "REPORT.md")).write_text("\n\n".join(text)+"\n")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase",choices=("pilot","full"))
    phase=p.parse_args().phase
    cases=[load(EVALUATION/phase/g/t/f"{s}.json") for g,t,s in roster(phase)]
    rows,scenes,judges,stages=gather(cases,phase)
    task,summary=summaries(rows,phase)
    pairs=paired(task,phase)
    diag,verdict,stage=diagnostics(scenes,judges,stages,phase)
    samples=examples(cases,phase)
    paths=generation_paths(phase)
    per_task=by_task_diagnostics(phase,scenes,judges)
    render(phase,summary,pairs,diag,verdict,stage,samples,paths,per_task)
    save(REPORTS/f"{phase}_analysis.json",{"summary":summary,"diagnostics":diag,"judgments":verdict,
                                           "stages":stage,"samples":samples,"generation_paths":paths})
