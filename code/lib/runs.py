"""Immutable execution records and conservative retained-output validation."""

import hashlib
import subprocess
from datetime import UTC, datetime

from lib.paths import ROOT, sha256
from lib.records import write_json


def timestamp() -> str:
    """Return an ISO UTC timestamp for run metadata only."""
    return datetime.now(UTC).isoformat()


def start_run(mode: str, root=ROOT) -> dict:
    """Identify the checked-out code, locked environment and start of one run."""

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    commit = git("rev-parse", "HEAD")
    return {
        "run_id": datetime.now(UTC).strftime("%Y%m%dt%H%M%S%fz") + "-" + commit[:8],
        "started_utc": timestamp(),
        "finished_utc": None,
        "commit": commit,
        "tree_clean": not bool(git("status", "--porcelain")),
        "pixi_lock_sha256": sha256(root / "pixi.lock"),
        "mode": mode,
        "specs": [],
        "steps": [],
        "missing_inputs": [],
        "skipped_steps": [],
    }


def finish_run(record: dict, root=ROOT) -> str:
    """Save a new run record without replacing any earlier record."""
    record["finished_utc"] = timestamp()
    path = root / "outputs/runs" / f"{record['run_id']}.json"
    if path.exists():
        raise FileExistsError(path)
    write_json(path, record)
    return str(path.relative_to(root))


def can_retain(
    producer: dict, spec_hash: str, input_hashes: dict, code_hash: str, environment_hash: str
) -> bool:
    """Allow reuse only for identical specs, input identities, code and locked environment."""
    return (
        producer.get("spec_sha256") == spec_hash
        and producer.get("input_hashes") == input_hashes
        and producer.get("code_sha256") == code_hash
        and producer.get("pixi_lock_sha256") == environment_hash
    )


def code_digest(root=ROOT) -> str:
    """Fingerprint repository Python sources conservatively for restricted replay."""
    return hashlib.sha256(
        b"".join(
            path.relative_to(root).as_posix().encode() + path.read_bytes()
            for path in sorted((root / "code").rglob("*.py"))
        )
    ).hexdigest()
