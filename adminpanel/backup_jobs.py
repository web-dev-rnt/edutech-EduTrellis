"""Backups and restores run in a background thread; the backup page polls their progress.

A web request may run for only 120 seconds on the live server (gunicorn --timeout), and backing up or
restoring a database of a few hundred MB takes longer, so these used to fail halfway. A job writes its
progress to a small JSON file in the temp folder, so whichever server process answers the page's poll
can report it. Only one backup or restore runs at a time.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
import threading
import time
import uuid

from django.conf import settings
from django.core import signing

logger = logging.getLogger(__name__)

TOKEN_SALT = "backup-job"
TOKEN_MAX_AGE = 12 * 60 * 60
# A job that has not reported progress for this long died with its server process (deploy/restart).
STALE_SECONDS = 10 * 60
KEEP_FINISHED_SECONDS = 24 * 60 * 60

_start_lock = threading.Lock()


class JobBusy(Exception):
    def __init__(self, job):
        super().__init__("Another backup or restore is still running.")
        self.job = job


def _job_dir() -> str:
    path = getattr(settings, "BACKUP_JOB_DIR", "") or os.path.join(tempfile.gettempdir(), "site-backup-jobs")
    os.makedirs(path, exist_ok=True)
    return path


def _job_path(job_id: str) -> str:
    return os.path.join(_job_dir(), f"{job_id}.json")


def read(job_id: str) -> dict | None:
    if not job_id or not job_id.isalnum():
        return None
    job = None
    for attempt in range(10):
        try:
            with open(_job_path(job_id), encoding="utf-8") as fh:
                job = json.load(fh)
            break
        except FileNotFoundError:
            return None
        except (OSError, ValueError):  # being replaced right now (Windows): try again
            time.sleep(0.05 * (attempt + 1))
    if job is None:
        return None
    if job.get("status") == "running" and time.time() - job.get("updated", 0) > STALE_SECONDS:
        job.update(status="error", error="The server restarted while this was running. Please try again.")
    return job


def _write(job: dict, attempts: int = 20) -> bool:
    """Save the job file atomically (a poll never reads half a file). Returns False if it could not.

    On Windows the replace fails while another request has the file open for reading, so it is retried.
    """
    path = _job_path(job["id"])
    part = f"{path}.{os.getpid()}.{threading.get_ident()}.part"
    try:
        with open(part, "w", encoding="utf-8") as fh:
            json.dump(job, fh)
        for attempt in range(attempts):
            try:
                os.replace(part, path)
                return True
            except PermissionError:
                time.sleep(0.05 * (attempt + 1))
    except OSError as exc:
        logger.warning("Could not save backup job progress: %s", exc)
    try:
        os.remove(part)
    except OSError:
        pass
    return False


def active_job() -> dict | None:
    """The backup or restore that is running right now, if any (and tidy up old job files)."""
    running = None
    for entry in os.scandir(_job_dir()):
        if not entry.name.endswith(".json"):
            continue
        job = read(entry.name[:-5])
        if job is None:
            continue
        if job["status"] == "running":
            running = job
        elif time.time() - job.get("updated", 0) > KEEP_FINISHED_SECONDS:
            try:
                os.remove(entry.path)
            except OSError:
                pass
    return running


class Progress:
    """Handed to the work function; every call updates the job file the page polls."""

    def __init__(self, job: dict):
        self.job = job
        self._last_write = 0.0

    def __call__(self, stage=None, *, done=None, total=None, message=None, force=False):
        job = self.job
        if stage is not None and stage != job.get("stage"):
            job["stage"] = stage
            job.setdefault("stages", [])
            if stage not in job["stages"]:
                job["stages"].append(stage)
            force = True
        if done is not None:
            job["done_bytes"] = done
        if total is not None:
            job["total_bytes"] = total
        if message is not None:
            job["message"] = message
        total_bytes = job.get("total_bytes") or 0
        job["percent"] = round(min(job.get("done_bytes", 0) / total_bytes * 100, 100), 1) if total_bytes else None
        job["updated"] = time.time()
        # Byte counters change many times a second; write at most twice a second unless the stage changed.
        if force or job["updated"] - self._last_write >= 0.5:
            self._last_write = job["updated"]
            _write(job, attempts=5)  # progress only: never let a busy file stop the backup/restore


def start(kind: str, user, work, **params) -> dict:
    """Run work(progress, **params) in a background thread. Returns the new job (raises JobBusy)."""
    with _start_lock:
        busy = active_job()
        if busy:
            raise JobBusy(busy)
        now = time.time()
        job = {
            "id": uuid.uuid4().hex, "kind": kind, "status": "running", "stage": "Starting", "stages": [],
            "done_bytes": 0, "total_bytes": 0, "percent": None, "message": "", "result": None, "error": None,
            "email": getattr(user, "email", ""), "started": now, "updated": now, "params": params,
        }
        if not _write(job):
            raise RuntimeError("Could not create the job file in the server's temp folder.")
    if getattr(settings, "BACKUP_JOBS_INLINE", False):  # tests: run in this thread
        _run(job, work, params)
        return read(job["id"])
    threading.Thread(target=_run, args=(job, work, params), name=f"backup-{kind}", daemon=True).start()
    return job


def _run(job: dict, work, params: dict) -> None:
    from django.db import connections

    progress = Progress(job)
    try:
        result = work(progress, **params)
        job.update(status="done", percent=100, result=result, stage="Finished", updated=time.time())
    except Exception as exc:
        logger.exception("Backup job %s (%s) failed", job["id"], job["kind"])
        job.update(status="error", error=str(exc) or exc.__class__.__name__, updated=time.time())
    finally:
        _write(job, attempts=100)  # the final state must land
        connections.close_all()  # this thread's database connections


def token(job: dict) -> str:
    return signing.dumps({"id": job["id"], "email": job.get("email", "")}, salt=TOKEN_SALT)


def from_token(value: str) -> dict | None:
    try:
        data = signing.loads(value, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE)
    except signing.BadSignature:
        return None
    job = read(data.get("id", ""))
    if job and job.get("email") == data.get("email"):
        return job
    return None


def public(job: dict) -> dict:
    """What the page may see (no e-mail address or parameters)."""
    keys = ("id", "kind", "status", "stage", "stages", "done_bytes", "total_bytes", "percent", "message",
            "result", "error", "started", "updated")
    return {key: job.get(key) for key in keys}
