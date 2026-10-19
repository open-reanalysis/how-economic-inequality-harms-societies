"""Load versioned analysis specifications and enforce the current-result gate."""

import yaml

from lib.paths import ROOT, resolve, sha256


def load_spec(path, root=ROOT) -> dict:
    """Read a YAML specification and validate the implemented computation contract."""
    spec = yaml.safe_load(path.read_text())
    for key in [
        "spec_id",
        "version",
        "dataset",
        "unit_type",
        "catalogue",
        "samples",
        "variables",
        "index",
        "statistics",
    ]:
        if key not in spec:
            raise ValueError(f"Missing specification key: {key}")
    if spec["version"] < 1 or spec["dataset"] not in {"international", "us_states"}:
        raise ValueError("Invalid specification identity")
    if spec["statistics"] != ["pearson_r", "p_value", "n"]:
        raise ValueError("Unsupported statistic contract")
    variables = [v["variable_id"] for v in spec["variables"]]
    for sample in spec["samples"].values():
        if "units" in sample and len(sample["units"]) != len(set(sample["units"])):
            raise ValueError("Duplicate sample unit")
    if len(variables) != len(set(variables)):
        raise ValueError("Duplicate specification variable")
    resolve(spec["catalogue"], root)
    for variable in spec["variables"]:
        if variable.get("status") == "UNRESOLVED":
            continue
        for key in [
            "sources",
            "period",
            "unit",
            "conversion",
            "transformation",
            "direction",
            "rationale",
        ]:
            if key not in variable:
                raise ValueError(f"Missing variable setting {key}")
    return spec


def require_current_gate(spec_path, root=ROOT) -> None:
    """Require a matching merged lock and approved milestone tag before current analysis."""
    import subprocess

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    lock = yaml.safe_load((root / "config/reproduction_lock.yaml").read_text())
    if lock.get("status") != "approved":
        raise PermissionError("Current associations are gated: lock is not approved")
    for name, expected in lock["files"].items():
        if sha256(resolve(name, root)) != expected:
            raise PermissionError(f"Locked file changed: {name}")
    if str(spec_path.relative_to(root)) not in lock["files"]:
        raise PermissionError("Current specification is absent from the lock")
    approved = git("rev-parse", lock["milestone_tag"] + "^{commit}")
    merged_lock = git("show", approved + ":config/reproduction_lock.yaml")
    if yaml.safe_load(merged_lock) != lock:
        raise PermissionError("Milestone tag does not identify this approved lock")
    main = git("rev-parse", "origin/main")
    subprocess.run(["git", "merge-base", "--is-ancestor", approved, main], cwd=root, check=True)
