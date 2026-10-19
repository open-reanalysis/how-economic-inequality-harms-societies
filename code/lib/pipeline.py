"""One stored-input historical reproduction path and explicit result barriers."""

import json

import pandas as pd

from lib import compute
from lib.paths import ROOT, resolve, sha256
from lib.readers import READERS
from lib.records import load_records, verify_files
from lib.runs import can_retain, code_digest, finish_run, start_run
from lib.schemas import validate_observations, validate_result_keys
from lib.spec import load_spec, require_current_gate
from lib.transform import prepare


def registries(root=ROOT) -> tuple[dict, dict]:
    """Return canonical membership and source-name aliases for each dataset."""
    members, aliases = {}, {}
    for dataset, filename in [("international", "countries.csv"), ("us_states", "us_states.csv")]:
        frame = pd.read_csv(root / "config/units" / filename, dtype=str).fillna("")
        if frame.unit_id.duplicated().any():
            raise ValueError("Duplicate registry ID")
        members[dataset] = set(frame.unit_id)
        aliases[dataset] = {}
        for row in frame.to_dict("records"):
            for name in [row["unit_id"], row["name"], *row["aliases"].split(";")]:
                if not name:
                    continue
                previous = aliases[dataset].setdefault(name, row["unit_id"])
                if previous != row["unit_id"]:
                    raise ValueError(f"Ambiguous registry alias: {name}")
    return members, aliases


def reproduce(spec_path, root=ROOT) -> str:
    """Execute one specification; current specifications require the milestone gate."""
    spec = load_spec(spec_path, root)
    if (
        spec.get("data_provenance") not in {"released", "reconstructed"}
        or spec["spec_id"].startswith("updated_")
        or any(item["path"].startswith("data/01_raw_current/") for item in spec.get("inputs", []))
    ):
        require_current_gate(spec_path, root)
        raise NotImplementedError("Current reproduction belongs to milestone 2")
    sources, acquisitions = load_records(root)
    missing = verify_files(acquisitions, root)
    requested_inputs = {item["path"] for item in spec.get("inputs", [])}
    expected_hashes = {
        file["path"]: file["sha256"]
        for acquisition in acquisitions
        for file in acquisition["files"]
        if file["path"] in requested_inputs
    }
    metadata_paths = {spec["catalogue"], "config/units/countries.csv", "config/units/us_states.csv"}
    metadata_paths.update(
        f"data/metadata/sources/{item['source_id']}.yaml" for item in spec.get("inputs", [])
    )
    expected_hashes.update({name: sha256(resolve(name, root)) for name in metadata_paths})
    code_hash = code_digest(root)
    environment_hash = sha256(root / "pixi.lock")
    output = root / f"outputs/tables/{spec['spec_id']}_results.csv"
    producer = None
    if requested_inputs.intersection(missing) and output.exists():
        for path in sorted((root / "outputs/runs").glob("*.json"), reverse=True):
            candidate = json.loads(path.read_text())
            for step in candidate["steps"]:
                if step["state"] != "computed":
                    continue
                for produced in step["outputs"]:
                    if produced["path"] == str(output.relative_to(root)) and produced[
                        "sha256"
                    ] == sha256(output):
                        matching_specs = [
                            s for s in candidate["specs"] if s["spec_id"] == spec["spec_id"]
                        ]
                        if matching_specs:
                            candidate_producer = {
                                "run_id": candidate["run_id"],
                                "spec_sha256": matching_specs[0]["sha256"],
                                "input_hashes": {i["path"]: i["sha256"] for i in step["inputs"]},
                                "code_sha256": candidate.get("code_sha256"),
                                "pixi_lock_sha256": candidate.get("pixi_lock_sha256"),
                                "output_sha256": produced["sha256"],
                                "outputs": step["outputs"],
                            }
                            if can_retain(
                                candidate_producer,
                                sha256(spec_path),
                                expected_hashes,
                                code_hash,
                                environment_hash,
                            ):
                                producer = candidate_producer
                                break
            if producer:
                break
    if producer:
        if can_retain(producer, sha256(spec_path), expected_hashes, code_hash, environment_hash):
            if sha256(output) != producer["output_sha256"]:
                raise ValueError("Retained output differs from its producer record")
            for item in producer["outputs"]:
                retained_path = resolve(item["path"], root)
                if not retained_path.exists() or sha256(retained_path) != item["sha256"]:
                    raise ValueError(f"Retained companion output changed: {item['path']}")
            run = start_run("replay", root)
            run["specs"] = [
                {
                    "spec_id": spec["spec_id"],
                    "version": spec["version"],
                    "sha256": sha256(spec_path),
                }
            ]
            run["missing_inputs"] = sorted(requested_inputs.intersection(missing))
            run["steps"].append(
                {
                    "target": f"reproduce:{spec['spec_id']}",
                    "state": "retained",
                    "producer_run": producer["run_id"],
                    "reason": "Restricted inputs absent; identical environment, code, specification and recorded input identities",
                    "inputs": [
                        {
                            "path": p,
                            "sha256": h,
                            "check": "file_verified" if p in metadata_paths else "record_matched",
                            "restricted": p not in metadata_paths,
                        }
                        for p, h in expected_hashes.items()
                    ],
                    "outputs": producer["outputs"],
                }
            )
            return finish_run(run, root)
    if requested_inputs.intersection(missing):
        raise ValueError(
            "No compatible producer for missing restricted inputs; "
            "recompute locally with the locked environment before publishing a new snapshot"
        )
    members, aliases = registries(root)
    frames, inputs = [], []
    inputs.extend(
        {
            "path": name,
            "sha256": sha256(resolve(name, root)),
            "check": "file_verified",
            "restricted": False,
        }
        for name in sorted(metadata_paths)
    )
    for item in spec.get("inputs", []):
        path = resolve(item["path"], root)
        if not path.exists():
            continue
        matching = [f for a in acquisitions for f in a["files"] if f["path"] == item["path"]]
        if len(matching) != 1:
            raise ValueError("Every replay input needs exactly one acquisition file record")
        source = dict(sources[item["source_id"]], input_path=item["path"])
        frames.append(READERS[item["reader"]](path, source, aliases[spec["dataset"]]))
        inputs.append(
            {
                "path": item["path"],
                "sha256": sha256(path),
                "check": "file_verified",
                "restricted": not matching[0]["redistributable"],
            }
        )
    catalogue = pd.read_csv(resolve(spec["catalogue"], root), dtype=str).fillna("")
    catalogue = catalogue[catalogue.dataset.eq(spec["dataset"])]
    sample = spec["samples"]["historical"]["units"]
    if set(sample) - members[spec["dataset"]]:
        raise ValueError("Specification contains unregistered units")
    values = pd.DataFrame(index=pd.Index(sorted(sample), name="unit_id"))
    if frames:
        observations = validate_observations(pd.concat(frames, ignore_index=True), members)
        if observations.provenance.eq("current").any():
            require_current_gate(spec_path, root)
            raise NotImplementedError("Current reproduction belongs to milestone 2")
        values = prepare(observations, spec, sample)
    if spec["index"].get("mode") == "rebuild" and spec["index"].get("status") != "UNRESOLVED":
        definition = dict(
            spec["index"],
            reference_units=spec["samples"][spec["index"]["standardisation_reference"]]["units"],
        )
        values["index"], _ = compute.index(values, definition)
    rows = []
    run = start_run("replay", root)
    run["missing_inputs"] = sorted(requested_inputs.intersection(missing))
    digest = sha256(spec_path)
    run["specs"] = [{"spec_id": spec["spec_id"], "version": spec["version"], "sha256": digest}]
    component_outputs = []
    if "index" in values and spec["index"].get("components"):
        component_rows = []
        index_targets = catalogue.loc[catalogue.indicator_or_index.eq("index"), "result_id"]
        for result_id in index_targets:
            for unit_id in sample:
                for component in spec["index"]["components"]:
                    available = component in values and pd.notna(values.loc[unit_id, component])
                    component_rows.append(
                        {
                            "result_id": result_id,
                            "variant_id": "historical",
                            "spec_id": spec["spec_id"],
                            "unit_id": unit_id,
                            "component": component,
                            "available": bool(available),
                            "used": bool(available and pd.notna(values.loc[unit_id, "index"])),
                        }
                    )
        component_path = root / f"outputs/tables/{spec['spec_id']}_components.csv"
        component_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(component_rows).to_csv(component_path, index=False)
        component_outputs.append(component_path)
    for target in catalogue.to_dict("records"):
        target_sample = spec["samples"][target.get("sample", "historical")]["units"]
        result = compute.correlation(
            values.reindex(target_sample), target["predictor"], target["indicator_or_index"]
        )
        reason = result["reason"]
        state = "not_produced" if reason else "computed"
        row = {
            "result_id": target["result_id"],
            "variant_id": "historical",
            "spec_id": spec["spec_id"],
            "spec_version": spec["version"],
            "spec_sha256": digest,
            "data_basis": "historical",
            "data_provenance": spec["data_provenance"],
            "access_label": spec["access_label"],
            "sample": "historical",
            "series_set": "original",
            "comparability": "historical",
            "method_deviations": spec["method_deviations"],
            "r": result["r"],
            "p": result["p"],
            "n": result["n"],
            "missing_units": ";".join(sorted(set(sample) - set(result["observations"].index))),
            "components_used": "",
            "components_missing": "",
            "input_access": "RESTRICTED INPUT"
            if any(i["restricted"] for i in inputs)
            else "PUBLIC INPUT"
            if frames
            else "UNAVAILABLE INPUT",
            "state": state,
            "reason": reason,
        }
        rows.append(row)
        # Obsolete public artifacts must not survive a barrier or a use restriction.
        publish = not reason and all(not i["restricted"] for i in inputs)
        if not publish:
            for directory, extension in [("observations", "csv"), ("figures", "png")]:
                stale = (
                    root
                    / f"outputs/{directory}/{spec['spec_id']}/historical"
                    / f"{target['result_id']}.{extension}"
                )
                stale.unlink(missing_ok=True)
        if publish:
            path = (
                root
                / f"outputs/observations/{spec['spec_id']}/historical/{target['result_id']}.csv"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            result["observations"].to_csv(path, index=True, float_format="%.17g")
            component_outputs.append(path)
            from lib.figures import scatter

            figure_path = (
                root / f"outputs/figures/{spec['spec_id']}/historical/{target['result_id']}.png"
            )
            scatter(
                result["observations"],
                target["predictor"],
                target["indicator_or_index"],
                figure_path,
                x_unit=next(
                    v["unit"] for v in spec["variables"] if v["variable_id"] == target["predictor"]
                ),
                y_unit=next(
                    (
                        v["unit"]
                        for v in spec["variables"]
                        if v["variable_id"] == target["indicator_or_index"]
                    ),
                    "index_score",
                ),
                period=next(
                    (
                        str(v["period"])
                        for v in spec["variables"]
                        if v["variable_id"] == target["indicator_or_index"]
                    ),
                    "component-specific",
                ),
            )
            component_outputs.append(figure_path)
    frame = pd.DataFrame(rows)
    validate_result_keys(frame)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False, float_format="%.17g")
    run["code_sha256"] = code_hash
    run["steps"].append(
        {
            "target": f"reproduce:{spec['spec_id']}",
            "state": "computed",
            "reason": "Result table includes explicit barriers for uncomputed comparisons",
            "inputs": inputs,
            "outputs": [
                {"path": str(p.relative_to(root)), "sha256": sha256(p)}
                for p in [output, *component_outputs]
            ],
        }
    )
    record = finish_run(run, root)
    print(
        json.dumps(
            {
                "spec": spec["spec_id"],
                "computed": int(frame.state.eq("computed").sum()),
                "not_produced": int(frame.state.eq("not_produced").sum()),
                "run_record": record,
            }
        )
    )
    return record
