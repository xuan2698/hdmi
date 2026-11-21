"""Export hashes of earlier development references without exporting any RTL."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(dataset, output):
    expected = json.loads((REPO / "cvdp-headroom/reports/dataset_audit.json").read_text())["sha256"]
    data_hash = sha(dataset.read_bytes())
    if data_hash != expected:
        raise ValueError("Unexpected published CVDP revision")
    split = json.loads((REPO / "stimulus-v1/split.json").read_text())["development"]
    table = pq.read_table(dataset, columns=["id", "rtl_files"], filters=[("id", "in", split)])
    rows = {row["id"]:row["rtl_files"] for row in table.to_pylist()}
    if set(rows) != set(split):
        raise ValueError("Published development rows differ from the frozen split")
    fields = ["task", "release_file", "release_sha256", "joined_rtl_sha256", "dataset_sha256",
              "guidance_catalog", "guidance_catalog_sha256", "G_count", "archived_proxies"]
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fields, lineterminator="\n")
        writer.writeheader()
        for task in split:
            files = rows[task]
            joined = sha("\n\n".join(file["content"] for file in files).encode())
            catalog = Path("stimulus-v1") / "guidance" / task / "catalog.json"
            raw = (REPO / catalog).read_bytes()
            count = len(json.loads(raw)["candidates"])
            for file in files:
                writer.writerow({"task":task, "release_file":file["name"], "release_sha256":sha(file["content"].encode()),
                                 "joined_rtl_sha256":joined, "dataset_sha256":data_hash, "guidance_catalog":catalog,
                                 "guidance_catalog_sha256":sha(raw), "G_count":count, "archived_proxies":0})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("published_dataset", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/v2_source_manifest.csv")
    args = parser.parse_args()
    run(args.published_dataset, args.output)
