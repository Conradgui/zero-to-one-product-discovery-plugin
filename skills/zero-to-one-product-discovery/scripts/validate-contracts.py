#!/usr/bin/env python3
"""Validate Z2O contract schemas and release-critical metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"

SCHEMA_FILES = [
    "agent-work-order.schema.json",
    "agent-return-packet.schema.json",
    "audit-report.schema.json",
    "workbench.schema.json",
    "pattern-index.schema.json",
    "artifact-manifest.schema.json",
    "execution-handoff.schema.json",
    "revision-index.schema.json",
    "revision-record.schema.json",
]

REQUIRED_SCENARIOS = {
    "quick_mode_labeled_draft",
    "dashboard_evidence_maturity_read_only",
    "assumption_validation_plan_binding",
    "material_assimilation_express_review",
    "risk_map_prioritizes_high_impact_assumptions",
    "readiness_spectrum_non_prd_artifact",
    "pattern_library_advisory_packaging_boundary",
    "multi_agent_contract_packet_completeness",
    "multi_agent_auditor_blocks_without_rewrite",
    "multi_agent_workbench_schema_no_transcript",
    "execution_bridge_github_issues_e2e",
    "execution_bridge_claude_tasks_e2e",
    "execution_bridge_jira_tickets_e2e",
    "workbench_corrupted_summary_rejected",
    "artifact_status_content_mismatch_blocked",
    "quick_mode_export_warning_preserved",
    "controller_action_registry_consistency",
}

CONTROLLER_ACTION_FIELDS = {
    "controller_decision",
    "recommended_controller_action",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_type(value: Any, expected: Any, path: str) -> None:
    if isinstance(expected, list):
        if not any(type_matches(value, item) for item in expected):
            raise ValidationError(f"{path}: expected one of {expected}, got {type(value).__name__}")
        return
    if not type_matches(value, expected):
        raise ValidationError(f"{path}: expected {expected}, got {type(value).__name__}")


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValidationError(f"unsupported schema type: {expected}")


def resolve_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/$defs/"):
        raise ValidationError(f"unsupported $ref: {ref}")
    key = ref.rsplit("/", 1)[1]
    try:
        return schema["$defs"][key]
    except KeyError as exc:
        raise ValidationError(f"missing $defs entry for {ref}") from exc


def validate_instance(instance: Any, subschema: dict[str, Any], root_schema: dict[str, Any], path: str) -> None:
    if "$ref" in subschema:
        validate_instance(instance, resolve_ref(root_schema, subschema["$ref"]), root_schema, path)
        return

    if "const" in subschema and instance != subschema["const"]:
        raise ValidationError(f"{path}: expected const {subschema['const']!r}")

    if "type" in subschema:
        assert_type(instance, subschema["type"], path)

    if "enum" in subschema and instance not in subschema["enum"]:
        raise ValidationError(f"{path}: {instance!r} not in enum")

    if "pattern" in subschema and isinstance(instance, str):
        if not re.search(subschema["pattern"], instance):
            raise ValidationError(f"{path}: {instance!r} does not match pattern")

    if "minLength" in subschema and isinstance(instance, str):
        if len(instance) < subschema["minLength"]:
            raise ValidationError(f"{path}: string shorter than minLength")

    if "minItems" in subschema and isinstance(instance, list):
        if len(instance) < subschema["minItems"]:
            raise ValidationError(f"{path}: array shorter than minItems")

    if isinstance(instance, dict):
        required = subschema.get("required", [])
        for key in required:
            if key not in instance:
                raise ValidationError(f"{path}: missing required property {key!r}")

        properties = subschema.get("properties", {})
        additional_properties = subschema.get("additionalProperties")
        if additional_properties is False:
            extra = set(instance) - set(properties)
            if extra:
                raise ValidationError(f"{path}: unexpected properties {sorted(extra)}")

        for key, value in instance.items():
            if key in properties:
                validate_instance(value, properties[key], root_schema, f"{path}.{key}")
            elif isinstance(additional_properties, dict):
                validate_instance(value, additional_properties, root_schema, f"{path}.{key}")

    if isinstance(instance, list) and "items" in subschema:
        for index, item in enumerate(instance):
            validate_instance(item, subschema["items"], root_schema, f"{path}[{index}]")


def validate_schema_file(path: Path) -> None:
    schema = load_json(path)
    for key in ("$schema", "title", "type", "required", "properties"):
        if key not in schema:
            raise ValidationError(f"{path.name}: missing top-level {key}")
    if schema["type"] != "object":
        raise ValidationError(f"{path.name}: top-level type must be object")
    for index, example in enumerate(schema.get("examples", [])):
        validate_instance(example, schema, schema, f"{path.name}.examples[{index}]")


def find_controller_action_enums(subschema: Any, path: str = "$") -> list[tuple[str, list[str]]]:
    matches: list[tuple[str, list[str]]] = []
    if isinstance(subschema, dict):
        properties = subschema.get("properties")
        if isinstance(properties, dict):
            for key, value in properties.items():
                if key in CONTROLLER_ACTION_FIELDS and isinstance(value, dict):
                    enum = value.get("enum")
                    if not isinstance(enum, list) or not all(isinstance(item, str) for item in enum):
                        raise ValidationError(f"{path}.properties.{key}: missing string enum")
                    matches.append((f"{path}.properties.{key}", enum))
                matches.extend(find_controller_action_enums(value, f"{path}.properties.{key}"))
        defs = subschema.get("$defs")
        if isinstance(defs, dict):
            for key, value in defs.items():
                matches.extend(find_controller_action_enums(value, f"{path}.$defs.{key}"))
        items = subschema.get("items")
        if isinstance(items, dict):
            matches.extend(find_controller_action_enums(items, f"{path}.items"))
    elif isinstance(subschema, list):
        for index, value in enumerate(subschema):
            matches.extend(find_controller_action_enums(value, f"{path}[{index}]"))
    return matches


def validate_controller_action_registry() -> None:
    registry = load_json(EVALS / "controller-actions.json")
    actions = registry.get("actions")
    if not isinstance(actions, list) or not actions or not all(isinstance(item, str) for item in actions):
        raise ValidationError("controller-actions.json: actions must be a non-empty string array")
    if len(actions) != len(set(actions)):
        raise ValidationError("controller-actions.json: actions must be unique")
    if registry.get("package_version") != "v0.4.0-rc.4":
        raise ValidationError("controller-actions.json: expected package_version v0.4.0-rc.4")

    expected = sorted(actions)
    for filename in SCHEMA_FILES:
        schema = load_json(EVALS / filename)
        for enum_path, enum in find_controller_action_enums(schema):
            if sorted(enum) != expected:
                raise ValidationError(
                    f"{filename}:{enum_path}: controller action enum does not match controller-actions.json"
                )


def validate_evals() -> None:
    evals = load_json(EVALS / "evals.json")
    version = evals.get("current_package_version")
    if version != "v0.4.0-rc.4":
        raise ValidationError(f"evals.json: expected current_package_version v0.4.0-rc.4, got {version!r}")
    scenario_ids = {scenario.get("id") for scenario in evals.get("scenarios", [])}
    missing = sorted(REQUIRED_SCENARIOS - scenario_ids)
    if missing:
        raise ValidationError(f"evals.json: missing required scenarios {missing}")
    if len(scenario_ids) < 39:
        raise ValidationError("evals.json: expected at least 39 scenarios after RC expansion")


def validate_packaging_boundary() -> None:
    forbidden_dirs = [ROOT / ".z2o-state", ROOT / ".z2o-patterns", ROOT / "z2o-artifacts"]
    present = [str(path.relative_to(ROOT)) for path in forbidden_dirs if path.exists()]
    if present:
        raise ValidationError(f"runtime state directories must not ship in skill folder: {present}")


def main() -> int:
    try:
        for filename in SCHEMA_FILES:
            validate_schema_file(EVALS / filename)
        validate_controller_action_registry()
        validate_evals()
        validate_packaging_boundary()
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("OK: contract schemas, eval coverage, and packaging boundary validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
