"""Seal a stopped pilot without issuing API calls."""

from collections import Counter
from math import floor

from api import usage
from data import PLAN, ROOT, load, roster, save

ARM_ROUTES = {"Ours": "standard", "Ours-R1": "standard",
              "Ours-noReview": "no_review", "Ours-noArbiter": "no_arbiter"}


def case_path(group, task, seed):
    return ROOT / "runs" / group / task / str(seed)


def seal_failed():
    jobs = roster("pilot")
    planned = len(jobs) * len(PLAN["configs"])
    archived = [load(p) for g,t,s in jobs for p in case_path(g,t,s).glob("configs/*/result.json")]
    known_failures = sum(row["status"] == "generation_failed" for row in archived)
    maximum = floor(planned * PLAN["max_pilot_generation_failure"])
    if known_failures <= maximum:
        raise SystemExit("The recorded failures do not yet make the pilot threshold unreachable")
    repairs = (ROOT / "reports/REPAIRS.md").read_text().count("## 第 ")
    if repairs != PLAN["max_workflow_repairs"]:
        raise SystemExit("Stop under this rule only after the allowed repairs")

    for group,task,seed in jobs:
        base = case_path(group,task,seed)
        for arm in PLAN["configs"]:
            path = base / "configs" / arm / "result.json"
            if path.exists():
                continue
            is_vote = arm == "Vote-think"
            folders = [p.parent for p in (base/"vote").rglob("calls.jsonl")] if is_vote else []
            stub = {"group":group,"task":task,"seed":seed,"config":arm,"status":"not_run_gate",
                    "model":None,"scenes":None,"usage":usage(folders),
                    "failure":"N not calibrated under the stopping rule" if is_vote else
                              "An open correction stage was stopped at the pilot threshold"}
            if arm in ARM_ROUTES:
                stub["route"] = ARM_ROUTES[arm]
                rounds = [p for p in (base/stub["route"]).glob("round*/outcome.json")]
                stub["last_round"] = len(rounds)
                folders = [base / n for n in ("rm","tb","review","review_repair")]
                folders.extend(p.parent for p in (base/stub["route"]).rglob("calls.jsonl"))
                stub["usage"] = usage(folders)
            if is_vote:
                stub["exploratory_candidates"] = sum(load(p)["ok"] for p in (base/"vote").glob("*/status.json"))
            save(path,stub)
    rows = [load(p) for g,t,s in jobs for p in case_path(g,t,s).glob("configs/*/result.json")]
    totals = Counter(r["status"] for r in rows)
    if len(rows) != planned:
        raise ValueError("The sealed pilot does not have the planned number of slots")
    summary = {"cases":len(jobs),"configs":planned,"failures":totals["generation_failed"],
               "ready":totals["ready"],"stopped":totals["not_run_gate"],"N":None}
    save(ROOT/"reports/pilot_generation.json",summary)
    save(ROOT/"reports/pilot_gate.json",{**summary,"status":"failed_after_3_repairs",
         "threshold":PLAN["max_pilot_generation_failure"],"maximum_failures":maximum,
         "observed_generation_failure_lower_bound":totals["generation_failed"]/planned,
         "repairs":repairs,"vote_calibrated":False,"full_started":False})
    print(summary,flush=True)


if __name__ == "__main__":
    seal_failed()
