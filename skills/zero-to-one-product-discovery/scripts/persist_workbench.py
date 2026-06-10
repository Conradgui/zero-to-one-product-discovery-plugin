#!/usr/bin/env python3
"""Validate and atomically persist a Z2O Runtime Workbench state file."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import tempfile
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "evals" / "workbench.schema.json"
DEFAULT_STATE_PATH = Path(".z2o-state") / "workbench.json"


class PersistError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Workbench JSON file to validate and persist.")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="Target state path.")
    return parser.parse_args()


def load_validator_module() -> Any:
    validator_path = ROOT / "scripts" / "validate-contracts.py"
    spec = importlib.util.spec_from_file_location("z2o_validate_contracts", validator_path)
    if spec is None or spec.loader is None:
        raise PersistError(f"Unable to load validator module from {validator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def ensure_target_allowed(path: Path) -> None:
    if is_relative_to(path, ROOT):
        raise PersistError("Refusing to write Runtime Workbench state inside the installable skill directory")


def expected_maturity_level(percentage: float) -> str:
    if percentage > 75:
        return "strong"
    if percentage >= 50:
        return "sufficient"
    if percentage >= 25:
        return "partial"
    return "insufficient"


def validate_evidence_summary(workbench: dict[str, Any]) -> None:
    snapshot = workbench["evidence_snapshot"]
    items = snapshot["items"]
    summary = snapshot["summary"]

    counts = {
        "total": len(items),
        "facts": 0,
        "assumptions": 0,
        "unknowns": 0,
        "risks": 0,
        "validated": 0,
        "critical_impact_items": 0,
        "high_impact_items": 0,
    }
    highest_risk_id = None
    highest_risk_priority = None
    seen_ids: set[str] = set()

    for item in items:
        item_id = item["id"]
        if item_id in seen_ids:
            raise PersistError(f"Duplicate evidence item id: {item_id}")
        seen_ids.add(item_id)

        item_type = item["type"]
        if item_type == "fact":
            counts["facts"] += 1
            if item["validation_status"] == "verified":
                counts["validated"] += 1
        elif item_type == "assumption":
            counts["assumptions"] += 1
        elif item_type == "unknown":
            counts["unknowns"] += 1
        elif item_type == "risk":
            counts["risks"] += 1

        if item.get("impact_if_wrong") == "critical":
            counts["critical_impact_items"] += 1
        if item.get("impact_if_wrong") == "high":
            counts["high_impact_items"] += 1

        priority = item["risk_weighted_priority"]
        if priority > 0 and (highest_risk_priority is None or priority > highest_risk_priority):
            highest_risk_priority = priority
            highest_risk_id = item_id

    for key, expected in counts.items():
        actual = summary[key]
        if actual != expected:
            raise PersistError(f"evidence_snapshot.summary.{key} expected {expected}, got {actual}")

    expected_maturity = 0 if counts["total"] == 0 else round((counts["validated"] / counts["total"]) * 100, 2)
    if abs(float(summary["maturity_percentage"]) - expected_maturity) > 0.01:
        raise PersistError(
            "evidence_snapshot.summary.maturity_percentage "
            f"expected {expected_maturity}, got {summary['maturity_percentage']}"
        )

    expected_level = expected_maturity_level(expected_maturity)
    if summary["maturity_level"] != expected_level:
        raise PersistError(f"evidence_snapshot.summary.maturity_level expected {expected_level}, got {summary['maturity_level']}")

    if summary["highest_risk_item_id"] != highest_risk_id:
        raise PersistError(
            "evidence_snapshot.summary.highest_risk_item_id "
            f"expected {highest_risk_id!r}, got {summary['highest_risk_item_id']!r}"
        )


def validate_workbench(workbench: Any) -> dict[str, Any]:
    if not isinstance(workbench, dict):
        raise PersistError("Workbench input must be a JSON object")
    validator = load_validator_module()
    schema = validator.load_json(SCHEMA_PATH)
    validator.validate_instance(workbench, schema, schema, "workbench")
    validate_evidence_summary(workbench)
    return workbench


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".workbench.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    args = parse_args()
    try:
        target = Path(args.state_path)
        ensure_target_allowed(target)
        workbench = validate_workbench(load_json(Path(args.input)))
        atomic_write_json(target, workbench)
    except (OSError, json.JSONDecodeError, PersistError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"OK persisted workbench: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
