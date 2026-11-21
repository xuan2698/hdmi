"""Generate and checkpoint the fifty shared initial stimuli."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import generate, protocol, public, sample_path


def initial(job):
    row, seed = job
    vectors = generate(sample_path(row["id"], seed) / "initial", row, seed)
    print(row["id"], seed, "complete" if vectors is not None else "failed", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset", type=Path)
    args = p.parse_args()
    with ThreadPoolExecutor(max_workers=20) as pool:
        list(pool.map(initial, [(row, seed) for row in public(args.dataset) for seed in protocol()["seeds"]]))
