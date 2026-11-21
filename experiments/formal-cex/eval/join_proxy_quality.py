"""Link evaluator-only proxy outcomes to formal diagnostics for reporting."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT/"reports"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, choices=(2,3), default=2)
    args=parser.parse_args()
    categories={}
    for path in (ROOT/"stage0"/f"round{args.round}").glob("*/*/G*.json"):
        record=json.loads(path.read_text())
        key=(record["task"],record["proxy"])
        counts=categories.setdefault(key,Counter())
        counts["completed"]+=1
        counts["verified_counterexamples"]+=int(record["replayable"])
        counts["certified_bounded"]+=int(record["category"]=="bounded_equivalent")
    with (REPORTS/"proxy_eval.csv").open() as f:
        records=list(csv.DictReader(f))
    counts_by_quality={}
    for r in records:
        quality=r["differential_verdict"]
        total=counts_by_quality.setdefault(quality,Counter())
        total["proxy_count"]+=1
        total.update(categories.get((r["task"],r["proxy"]),{}))
    fields=("round","differential_proxy_verdict","proxy_count","completed","verified_counterexamples",
            "certified_bounded")
    with (REPORTS/"proxy_eval_formal_join.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.writer(stream,lineterminator="\n")
        writer.writerow(fields)
        for name,counts in sorted(counts_by_quality.items()):
            writer.writerow([args.round,name,*(counts[key] for key in fields[2:])])


if __name__=="__main__":
    main()
