"""Audit generation prompts against the held-out evaluation assets."""

import hashlib
import json
import random
import re
from pathlib import Path


def normalize(text):
    return " ".join(text.split())


def distinctive_fragments(path, legitimate):
    source = path.read_text()
    lines = [normalize(line) for line in source.splitlines()
             if len(normalize(line)) > 8 and not line.strip().startswith("//")]
    passages = {normalize(source)}
    passages.update(" ".join(lines[i:i + 3]) for i in range(len(lines) - 2))
    return {p for p in passages if len(p) >= 32 and p not in legitimate}


def audit(root, seed, count=10):
    root = Path(root)
    allowed = "\n".join(p.read_text() for p in (root / "generation").rglob("*") if p.is_file())
    allowed = normalize(allowed)
    tags = {}
    for folder in (root / "eval").iterdir():
        assets = (folder / "golden_rtl.v", folder / "golden_tb.v",
                  *sorted((folder / "official_mutants").glob("*.v")))
        tags[folder.name] = {str(path.relative_to(root)): distinctive_fragments(path, allowed)
                              for path in assets}
    entries = []
    for path in sorted((root / "runs").glob("*/*/calls.jsonl")):
        task, cfg = path.parent.parent.name, path.parent.name
        if cfg == "screen":
            continue
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            row = json.loads(line)
            entries.append((task, cfg, lineno, row["prompt"]))
    sampled = random.Random(seed).sample(entries, count)
    results = []
    for task, cfg, lineno, source in sampled:
        prompt = normalize(source)
        hits = [path for path, parts in tags[task].items() if any(part in prompt for part in parts)]
        path_hit = re.search(r"(?i)\beval[/\\]", source) is not None
        results.append({"task": task, "configuration": cfg, "line": lineno,
                        "role": "checker" if "Implement exactly reference(vectors)" in source else "stimulus",
                        "prompt_sha256": hashlib.sha256(source.encode()).hexdigest(),
                        "contains_evaluation_path": path_hit, "asset_fragment_matches": hits,
                        "passed": not (path_hit or hits)})
    return {"selection_seed": seed, "sampled": len(results), "eligible": len(entries),
            "passed": sum(row["passed"] for row in results), "results": results}
