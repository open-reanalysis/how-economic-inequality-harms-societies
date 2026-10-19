# SPDX-License-Identifier: MIT
# Purpose: Check repository metadata and optionally verify stored input files.
# Thread: scaffold
# Reads: config/, data/metadata/, docs/, outputs/runs/, ownership and git history
# Writes: none
# Network: none

"""Validate metadata contracts without reading raw files unless full mode is requested."""

import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

from lib.paths import ROOT, resolve, sha256
from lib.pipeline import registries
from lib.records import load_records, verify_files
from lib.spec import load_spec


def table(path: Path) -> list[dict]:
    """Read a canonical CSV table and reject rows with the wrong column count."""
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if len(reader.fieldnames or []) != len(set(reader.fieldnames or [])):
            raise ValueError(f"Duplicate columns: {path}")
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError(f"Invalid CSV row length: {path}")
        return rows


def check(mode: str, root=ROOT, base: str | None = None) -> None:
    """Check identifiers, references, specs, runs and immutable base-branch file entries."""
    sources, acquisitions = load_records(root)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    ownership = {}
    for path in (root / "docs/ownership").glob("*.csv"):
        ownership[path.stem] = [r["path_pattern"] for r in table(path)]
    for name in filter(None, tracked):
        if name.endswith(".gitkeep"):
            continue
        owners = []
        for owner, patterns in ownership.items():
            if any(
                re.fullmatch(
                    re.escape(p)
                    .replace(r"\*\*", ".*")
                    .replace(r"\*", "[^/]*")
                    .replace(r"\?", "[^/]"),
                    name,
                )
                for p in patterns
            ):
                owners.append(owner)
        if len(owners) != 1:
            raise ValueError(f"File needs exactly one owner: {name}: {owners}")
    for row in table(root / "docs/goal_traceability.csv"):
        if any(
            not row[key]
            for key in ["owner", "threads", "milestone", "output_paths", "acceptance_test"]
        ):
            raise ValueError("Goal lacks an owner, output, acceptance test or milestone")
        if set(row["threads"].split(";")) - ownership.keys():
            raise ValueError("Goal references an unknown thread")
    members, _ = registries(root)
    catalogue = table(root / "config/results_catalogue.csv")
    ids = [r["result_id"] for r in catalogue]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate catalogue result_id")
    lineage = table(root / "docs/source_lineage.csv")
    keys = [(r["dataset"], r["variable_id"]) for r in lineage]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate lineage variable")
    for row in lineage:
        if row["historical_source"] not in sources:
            raise ValueError(f"Unknown historical source: {row['historical_source']}")
        if row["current_source"] and row["current_source"] not in sources:
            raise ValueError("Unknown current source")
        if row["comparability_class"] not in {
            "EXACT_SUCCESSOR",
            "CONCEPTUAL_SUCCESSOR",
            "SUBSTITUTE",
            "NO_CURRENT_EQUIVALENT",
            "NOT_YET_VERIFIED",
        }:
            raise ValueError("Invalid comparability class")
        if (
            row["comparability_class"]
            in {"SUBSTITUTE", "NO_CURRENT_EQUIVALENT", "NOT_YET_VERIFIED"}
            and not row["deviation_reason"]
        ):
            raise ValueError("Comparability barrier has no reason")
    for row in catalogue:
        for var in [row["predictor"], row["indicator_or_index"]]:
            if var != "index" and (row["dataset"], var) not in keys:
                raise ValueError(f"Catalogue variable absent from lineage: {var}")
        if not row["source_reference"]:
            raise ValueError("Catalogue target lacks source locator")
        if not row["reported_value"] and not row["notes"]:
            raise ValueError("Missing numeric benchmark needs a reason")
    for path in (root / "config/specs").glob("*.yaml"):
        spec = load_spec(path, root)
        if set(spec["samples"]["historical"]["units"]) - members[spec["dataset"]]:
            raise ValueError("Unknown specification sample member")
        for variable in spec["variables"]:
            if set(variable.get("sources", [])) - sources.keys():
                raise ValueError("Unknown specification source")
    lock_path = root / "config/reproduction_lock.yaml"
    if lock_path.exists():
        import yaml

        lock = yaml.safe_load(lock_path.read_text())
        if lock.get("status") == "approved":
            for name, expected in lock["files"].items():
                if sha256(resolve(name, root)) != expected:
                    raise ValueError(f"Locked input/specification changed: {name}")
                if (
                    name.startswith("config/specs/")
                    and load_spec(resolve(name, root), root).get("status") == "draft"
                ):
                    raise ValueError("An approved lock cannot contain a draft specification")
    for path in (root / "outputs/runs").glob("*.json"):
        record = json.loads(path.read_text())
        if path.stem != record["run_id"]:
            raise ValueError("Run filename does not match identity")
        for step in record["steps"]:
            if step["state"] not in {"computed", "retained", "not_produced"}:
                raise ValueError("Invalid run state")
            if step["state"] == "retained" and not step.get("producer_run"):
                raise ValueError("Retained output lacks producer run")
            if step["state"] != "computed" and not step.get("reason"):
                raise ValueError("Uncomputed step needs a reason")
            for item in step["inputs"] + step["outputs"]:
                resolve(item["path"], root)
    if base:
        for acquisition in acquisitions:
            path = f"data/metadata/acquisitions/{acquisition['acquisition_id']}.yaml"
            previous = subprocess.run(
                ["git", "show", f"{base}:{path}"], cwd=root, capture_output=True, text=True
            )
            if previous.returncode:
                continue
            import yaml

            earlier = yaml.safe_load(previous.stdout)
            old = {f["path"]: f for f in earlier["files"]}
            new = {f["path"]: f for f in acquisition["files"]}
            for name, file in old.items():
                if name not in new or any(
                    new[name][key] != file[key] for key in ["path", "sha256", "size_bytes"]
                ):
                    raise ValueError(f"Immutable file identity changed: {name}")
        changed = subprocess.check_output(
            [
                "git",
                "diff",
                "--name-status",
                base,
                "--",
                "data/00_original_released",
                "data/00_original_reconstruction",
                "data/01_raw_current",
                "data/04_controversy_test_data",
            ],
            cwd=root,
            text=True,
        )
        for line in changed.splitlines():
            state, *paths = line.split("\t")
            if state != "A" and not all(p.endswith(".gitkeep") for p in paths):
                raise ValueError(f"Existing raw file changed: {line}")
    missing = verify_files(acquisitions, root) if mode == "full" else []
    print(
        f"Contracts {mode}: {len(sources)} sources, {len(acquisitions)} acquisitions, {len(catalogue)} targets, {len(lineage)} lineage rows; missing restricted files: {len(missing)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["metadata", "full"], default="metadata")
    parser.add_argument("--base")
    args = parser.parse_args()
    check(args.mode, base=args.base)
