"""Repository-relative paths and stable file digests."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def resolve(path: str, root: Path = ROOT) -> Path:
    """Resolve a repository path, rejecting escape outside root."""
    result = (root / path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {path}")
    return result


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of the complete file bytes."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
