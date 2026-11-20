"""Atomically persist progress for one sampled task and one pinned experiment plan."""

import fcntl
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


class TaskCheckpoint:
    def __init__(self, directory, task_id, plan):
        if not re.fullmatch(r"[a-zA-Z0-9_]+", task_id):
            raise ValueError("Invalid task ID")
        self.directory = Path(directory)
        self.task_id = task_id
        self.file = self.directory / f"{task_id}.json"
        content = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()
        self.plan_hash = hashlib.sha256(content).hexdigest()
        self._lock = None

    def __enter__(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        lock_dir = self.directory / ".locks"
        lock_dir.mkdir(exist_ok=True)
        self._lock = (lock_dir / self.task_id).open("a")
        fcntl.flock(self._lock, fcntl.LOCK_EX)
        return self

    def __exit__(self, *_):
        self._lock.close()
        self._lock = None

    def read(self):
        self._require_lock()
        if not self.file.is_file():
            return {}
        state = json.loads(self.file.read_text())
        if state["task_id"] != self.task_id or state["plan_sha256"] != self.plan_hash:
            raise ValueError(f"Checkpoint does not match the task and plan: {self.file}")
        return state["progress"]

    def save(self, progress):
        self._require_lock()
        self.read()
        data = {"task_id": self.task_id, "plan_sha256": self.plan_hash, "progress": progress}
        fd, path = tempfile.mkstemp(prefix=f".{self.task_id}.", dir=self.directory)
        try:
            with os.fdopen(fd, "w") as stream:
                json.dump(data, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(path, self.file)
        finally:
            Path(path).unlink(missing_ok=True)

    def _require_lock(self):
        if self._lock is None:
            raise RuntimeError("Use a task checkpoint as a context manager")
