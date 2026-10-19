# SPDX-License-Identifier: MIT
# Purpose: Summarise nonmissing flags and payload validity without exposing current values.
# Thread: outcome-data
# Reads: data/metadata/ and stored candidate current JSON responses
# Writes: outputs/tables/outcome_source_coverage.csv
# Network: none

"""Inspect only shape, periods and nonmissing flags, never associations or outcome magnitudes."""

import csv
import json

from lib.paths import ROOT, resolve, sha256
from lib.records import load_records, verify_files
from lib.runs import finish_run, start_run


def coverage(source: dict, path) -> list[dict]:
    """Return one presence record per provider row, or a specific payload barrier."""
    data = json.loads(path.read_text())
    rows = []
    if source["source_id"].startswith("worldbank-"):
        if not isinstance(data, list) or len(data) != 2 or not isinstance(data[1], list):
            raise ValueError("Provider response is not an indicator dataset")
        if data[0]["pages"] != 1:
            raise ValueError("Provider response needs additional pages")
        for item in data[1]:
            rows.append(
                {
                    "unit_id": item["countryiso3code"],
                    "period": str(item["date"]),
                    "available": item["value"] is not None,
                }
            )
    elif source["source_id"].startswith("census-"):
        if not isinstance(data, list) or not data or "state" not in data[0]:
            raise ValueError("Provider response is not a state dataset")
        columns = data[0]
        for item in data[1:]:
            entry = dict(zip(columns, item, strict=True))
            rows.append(
                {
                    "unit_id": entry["state"],
                    "period": "2025",
                    "available": entry.get("B19083_001E")
                    not in {None, "null", "-666666666", "-999999999", "-888888888"},
                }
            )
    return rows


if __name__ == "__main__":
    sources, acquisitions = load_records()
    verify_files(acquisitions)
    rows = []
    run = start_run("replay")
    inputs = []
    for acquisition in acquisitions:
        for file in acquisition["files"]:
            if not file["path"].startswith("data/01_raw_current/"):
                continue
            inputs.append(
                {
                    "path": file["path"],
                    "sha256": sha256(resolve(file["path"])),
                    "check": "file_verified",
                    "restricted": False,
                }
            )
            source = sources[file["source_ids"][0]]
            try:
                items = coverage(source, resolve(file["path"]))
                rows.extend(
                    {
                        "source_id": source["source_id"],
                        "file_path": file["path"],
                        "payload_status": "parsed",
                        "barrier": "",
                        **item,
                    }
                    for item in items
                )
            except (ValueError, KeyError, TypeError) as error:
                rows.append(
                    {
                        "source_id": source["source_id"],
                        "file_path": file["path"],
                        "payload_status": "invalid_or_unsupported",
                        "barrier": str(error),
                        "unit_id": "",
                        "period": "",
                        "available": False,
                    }
                )
    target = ROOT / "outputs/tables/outcome_source_coverage.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "source_id",
                "file_path",
                "unit_id",
                "period",
                "available",
                "payload_status",
                "barrier",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (r["source_id"], r["unit_id"], r["period"])))
    print(f"Wrote {len(rows)} presence flags; no current outcome values or associations emitted.")

    run["steps"].append(
        {
            "target": "current-coverage-flags",
            "state": "computed",
            "inputs": inputs,
            "outputs": [{"path": str(target.relative_to(ROOT)), "sha256": sha256(target)}],
        }
    )
    print(finish_run(run))
