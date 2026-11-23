"""Run generated Python with the v3 sandbox and pure type introspection."""

import json
import subprocess
from functools import cache
from pathlib import Path

from pilot2_generate import atomic
from simulate import COMMAND_ENV, RunError, validate_rows

HERE = Path(__file__).resolve().parent


@cache
def worker_path():
    origin = HERE.parent / "autobench-pilot" / "model_worker.py"
    worker = origin.read_text()
    original = '"set", "sorted", "sum", "tuple", "zip")'
    if worker.count(original) != 1:
        raise ValueError("The inherited sandbox implementation changed")
    worker = worker.replace(original, '"set", "sorted", "sum", "tuple", "zip", "str", "isinstance")')
    output = HERE / ".work/checker_worker.py"
    atomic(output, worker)
    return output


def check_rows(source, widths, vectors):
    request = {"kind": "checker", "source": source, "vectors": vectors}
    args = ["bwrap", "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
            "--ro-bind", str(worker_path()), "/worker.py", "/usr/bin/python3", "-I", "-S", "/worker.py"]
    result = subprocess.run(args, input=json.dumps(request), capture_output=True, text=True,
                            env=COMMAND_ENV, timeout=12, cwd=HERE)
    if result.returncode:
        raise RunError("Generated Python failed: " + result.stderr[-1000:])
    try:
        rows = json.loads(result.stdout)
    except ValueError as error:
        raise RunError("Generated Python must return a JSON-compatible list") from error
    return validate_rows(rows, widths, len(vectors))
