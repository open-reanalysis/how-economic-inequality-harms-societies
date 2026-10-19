"""Validate source/acquisition records and verify stored file identities."""

import json
import re

import yaml

from lib.paths import ROOT, resolve, sha256


def load_records(root=ROOT) -> tuple[dict, list]:
    """Load YAML metadata and reject duplicate source or acquisition identifiers."""
    sources = {}
    acquisitions = []
    ids = set()
    for path in sorted((root / "data/metadata/sources").glob("*.yaml")):
        record = yaml.safe_load(path.read_text())
        key = record["source_id"]
        if key in sources or path.stem != key:
            raise ValueError(f"Duplicate or mismatched source ID: {key}")
        for field in [
            "provider",
            "series_code",
            "title",
            "definition",
            "unit",
            "geography",
            "licence",
            "terms_url",
            "redistributable",
        ]:
            if field not in record:
                raise ValueError(f"Missing source field {field}: {path}")
        sources[key] = record
    file_paths = set()
    for path in sorted((root / "data/metadata/acquisitions").glob("*.yaml")):
        record = yaml.safe_load(path.read_text())
        key = record["acquisition_id"]
        if key in ids or path.stem != key:
            raise ValueError(f"Duplicate or mismatched acquisition ID: {key}")
        ids.add(key)
        if set(record["source_ids"]) - sources.keys():
            raise ValueError(f"Unknown acquisition sources: {key}")
        if record["status"] not in {
            "acquired",
            "user_supplied",
            "awaiting_user",
            "access_failed",
            "not_downloaded_restricted",
            "removed",
        }:
            raise ValueError(f"Unknown acquisition status: {key}")
        if record["status"] in {"acquired", "user_supplied"} and not record["files"]:
            raise ValueError(f"Acquired response has no files: {key}")
        if not resolve(record["retrieval_log"], root).is_file():
            raise ValueError(f"Missing retrieval log: {key}")
        for file in record["files"]:
            resolve(file["path"], root)
            if file["path"] in file_paths:
                raise ValueError(f"Duplicate raw file path: {file['path']}")
            file_paths.add(file["path"])
            if not re.fullmatch(r"[0-9a-f]{64}", file["sha256"]):
                raise ValueError("Invalid SHA-256")
            if set(file["source_ids"]) - set(record["source_ids"]):
                raise ValueError("File source not declared by acquisition")
            if file["storage"] not in {"git", "local"} or file["size_bytes"] < 0:
                raise ValueError("Invalid file metadata")
            if not file["redistributable"] and file["storage"] != "local":
                raise ValueError("Nonredistributable raw file must stay local")
        acquisitions.append(record)
    return sources, acquisitions


def verify_files(acquisitions: list, root=ROOT) -> list[str]:
    """Hash present files, fail on missing public files, and list missing local inputs."""
    missing = []
    for acquisition in acquisitions:
        for file in acquisition["files"]:
            path = resolve(file["path"], root)
            if not path.exists():
                if file["storage"] == "local":
                    missing.append(file["path"])
                    continue
                raise ValueError(f"Missing published file: {path}")
            if path.stat().st_size != file["size_bytes"] or sha256(path) != file["sha256"]:
                raise ValueError(f"File checksum or size mismatch: {path}")
    return missing


def write_json(path, content) -> None:
    """Write a stable UTF-8 JSON document with a trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
