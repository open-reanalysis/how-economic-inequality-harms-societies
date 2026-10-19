"""Source-specific presence flags and compatible public replay of restricted inputs."""

import csv
import json

import pandas as pd

from lib.paths import ROOT, resolve, sha256
from lib.records import load_records, verify_files
from lib.runs import code_digest, finish_run, start_run


def coverage(source: dict, path) -> list[dict]:
    """Read periods and nonmissing flags without transforming or exposing outcome values."""
    format_name = source.get("coverage_format", "")
    if format_name == "stata":
        frame = pd.read_stata(path, convert_categoricals=False)
        return [
            dict(
                unit_id=r[source["country_column"]],
                period=source["period_label"],
                available=pd.notna(r[source["value_column"]]),
            )
            for r in frame.to_dict("records")
        ]
    if format_name == "excel_rows":
        layout = source["reader_layout"]
        frame = pd.read_excel(path, sheet_name=layout["sheet"], header=layout["header_row"])
        for column, value in layout["filters"].items():
            frame = frame.loc[frame[column].eq(value)]
        frame = frame.loc[frame[layout["year_column"]].ge(layout["minimum_year"])]
        keys = [layout["country_column"], layout["year_column"]]
        if frame.duplicated(keys).any():
            raise ValueError("Duplicate country-period after declared coverage filters")
        return [
            dict(
                unit_id=r[layout["country_column"]],
                period=str(r[layout["year_column"]]),
                available=pd.notna(pd.to_numeric(r[layout["value_column"]], errors="coerce")),
            )
            for r in frame.to_dict("records")
        ]
    data = json.loads(path.read_text())
    if format_name == "who_odata":
        if (
            not isinstance(data, dict)
            or not isinstance(data.get("value"), list)
            or data.get("@odata.nextLink")
        ):
            raise ValueError("Incomplete WHO indicator response")
        return [
            dict(
                unit_id=r["SpatialDim"],
                period=str(r["TimeDim"]),
                available=r["NumericValue"] is not None,
            )
            for r in data["value"]
            if all(r.get(k) == v for k, v in source["coverage_filters"].items())
        ]
    if format_name == "pip_income":
        return [
            dict(
                unit_id=r["country_code"],
                period=str(r["survey_year"]),
                available=all(r.get(f"decile{i}") is not None for i in [1, 2, 9, 10]),
            )
            for r in data
            if r["welfare_type"] == "income"
            and r["reporting_level"] == "national"
            and r["survey_coverage"] == "national"
            and r["is_interpolated"] is False
            and r["reporting_year"] == r["survey_year"]
        ]
    if source["source_id"].startswith("worldbank-"):
        if not isinstance(data, list) or len(data) != 2 or not isinstance(data[1], list):
            raise ValueError("Provider response is not an indicator dataset")
        if data[0]["pages"] != 1:
            raise ValueError("Provider response needs additional pages")
        return [
            dict(
                unit_id=r["countryiso3code"],
                period=str(r["date"]),
                available=r["value"] is not None,
            )
            for r in data[1]
        ]
    if source["source_id"].startswith("census-"):
        if not isinstance(data, list) or not data or "state" not in data[0]:
            raise ValueError("Provider response is not a state dataset")
        rows = []
        for item in data[1:]:
            entry = dict(zip(data[0], item, strict=True))
            rows.append(
                dict(
                    unit_id=entry["state"],
                    period=source.get("reference_period", "2025"),
                    available=entry.get("B19083_001E")
                    not in {None, "null", "-666666666", "-999999999", "-888888888"},
                )
            )
        return rows
    raise ValueError("No declared coverage reader for this source")


def build_coverage(root=ROOT) -> str:
    """Produce or retain the complete source-linked presence table with run evidence."""
    sources, acquisitions = load_records(root)
    verify_files(acquisitions, root)
    files = [
        f
        for a in acquisitions
        for f in a["files"]
        if f["path"].startswith("data/01_raw_current/")
        and sources[f["source_ids"][0]].get("record_role")
        not in {"verification_page", "unit_catalogue"}
    ]
    metadata = {f"data/metadata/sources/{f['source_ids'][0]}.yaml" for f in files}
    identities = {f["path"]: f["sha256"] for f in files}
    identities.update({p: sha256(resolve(p, root)) for p in metadata})
    restricted = {f["path"]: not f["redistributable"] for f in files}
    inputs = [
        dict(
            path=p,
            sha256=h,
            check="file_verified" if resolve(p, root).exists() else "record_matched",
            restricted=restricted.get(p, False),
        )
        for p, h in sorted(identities.items())
    ]
    missing = [f["path"] for f in files if not resolve(f["path"], root).exists()]
    target = root / "outputs/tables/outcome_source_coverage.csv"
    code_hash, environment = code_digest(root), sha256(root / "pixi.lock")
    producer = None
    if missing:
        for path in sorted((root / "outputs/runs").glob("*.json"), reverse=True):
            record = json.loads(path.read_text())
            if (
                record.get("code_sha256") != code_hash
                or record.get("pixi_lock_sha256") != environment
            ):
                continue
            for step in record["steps"]:
                if (
                    step["target"] == "current-coverage-flags"
                    and step["state"] == "computed"
                    and {r["path"]: r["sha256"] for r in step["inputs"]} == identities
                    and target.exists()
                    and step["outputs"][0]["sha256"] == sha256(target)
                ):
                    producer = record["run_id"]
                    break
            if producer:
                break
        if not producer:
            raise ValueError("No compatible producer for restricted current coverage")
    run = start_run("replay", root)
    run["code_sha256"] = code_hash
    run["missing_inputs"] = missing
    if not producer:
        rows = []
        for file in files:
            source = sources[file["source_ids"][0]]
            try:
                items = coverage(source, resolve(file["path"], root))
                if not items:
                    raise ValueError("No rows match the requested indicator dimensions")
                rows.extend(
                    dict(
                        source_id=source["source_id"],
                        file_path=file["path"],
                        payload_status="parsed",
                        barrier="",
                        **item,
                    )
                    for item in items
                )
            except (ValueError, KeyError, TypeError) as error:
                rows.append(
                    dict(
                        source_id=source["source_id"],
                        file_path=file["path"],
                        payload_status="invalid_or_unsupported",
                        barrier=str(error),
                        unit_id="",
                        period="",
                        available=False,
                    )
                )
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
            writer.writerows(
                sorted(
                    rows, key=lambda r: (r["source_id"], r["unit_id"], r["period"], r["file_path"])
                )
            )
    step = dict(
        target="current-coverage-flags",
        state="retained" if producer else "computed",
        inputs=inputs,
        outputs=[dict(path=str(target.relative_to(root)), sha256=sha256(target))],
    )
    if producer:
        step.update(
            producer_run=producer,
            reason="Restricted input absent; environment, code, metadata and recorded raw identities match",
        )
    run["steps"].append(step)
    return finish_run(run, root)
