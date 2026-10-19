"""Bounded acquisition preserving original response bytes and failure evidence."""

import os
from datetime import UTC, datetime
from urllib.parse import parse_qsl, urlsplit

import requests
import yaml

from lib.paths import ROOT, resolve, sha256

MAX_BYTES = 50 * 1024 * 1024


def acquire(
    source_ids: list[str], url: str, destination: str, *, redistributable: bool, root=ROOT
) -> dict:
    """Save one response of at most 50 MiB and record its exact request and outcome."""
    if os.environ.get("OFFLINE") == "1":
        raise RuntimeError("Network acquisition is disabled in offline mode")
    parsed = urlsplit(url)
    secret_fields = {
        "key",
        "api_key",
        "apikey",
        "token",
        "access_token",
        "password",
        "authorization",
    }
    if (
        parsed.username
        or parsed.password
        or any(name.lower() in secret_fields for name, _ in parse_qsl(parsed.query))
    ):
        raise ValueError(
            "Credential-bearing URLs must not enter public acquisition records; use the documented manual input route"
        )
    now = datetime.now(UTC)
    acquisition_id = "acq-" + now.strftime("%Y%m%dt%H%M%S%fz") + "-" + source_ids[0]
    record = {
        "acquisition_id": acquisition_id,
        "source_ids": source_ids,
        "method": "api" if "api" in url else "download",
        "request": url,
        "requested_utc": now.isoformat(),
        "response_status": None,
        "dataset_version": "unversioned",
        "status": "access_failed",
        "corrects": None,
        "retrieval_log": f"docs/source_verification/retrievals/{acquisition_id}.yaml",
        "notes": "",
        "files": [],
    }
    path = resolve(destination, root)
    if path.exists():
        raise FileExistsError(f"Immutable destination already exists: {destination}")
    try:
        with requests.get(
            url,
            stream=True,
            timeout=(15, 45),
            headers={"User-Agent": "open-reanalysis/0.1 (research source acquisition)"},
        ) as response:
            record["response_status"] = response.status_code
            final = urlsplit(response.url)
            if not any(
                name.lower() in secret_fields
                or "signature" in name.lower()
                or "credential" in name.lower()
                for name, _ in parse_qsl(final.query)
            ):
                record["resolved_url"] = response.url
            response.raise_for_status()
            content = bytearray()
            for chunk in response.iter_content(65536):
                content.extend(chunk)
                if len(content) > MAX_BYTES:
                    raise ValueError("Response exceeds the 50 MiB acquisition limit")
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(content)
            record["status"] = "acquired"
            record["files"] = [
                {
                    "path": destination,
                    "size_bytes": len(content),
                    "sha256": sha256(path),
                    "storage": "git" if redistributable else "local",
                    "redistributable": redistributable,
                    "source_ids": source_ids,
                }
            ]
    except (requests.RequestException, ValueError) as error:
        record["notes"] = str(error)
    log = resolve(record["retrieval_log"], root)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(yaml.safe_dump(record, sort_keys=False))
    metadata = root / "data/metadata/acquisitions" / f"{acquisition_id}.yaml"
    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text(yaml.safe_dump(record, sort_keys=False))
    return record
