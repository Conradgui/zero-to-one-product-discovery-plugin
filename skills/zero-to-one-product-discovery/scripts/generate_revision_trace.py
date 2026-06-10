#!/usr/bin/env python3
"""Generate a bounded Z2O artifact revision ledger."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_VERSION = "v0.4.0-rc.4"
SCHEMA_VERSION = "0.1.0"
STABLE_ARTIFACTS = {
    "prd": "prd.md",
    "roadmap": "roadmap.md",
    "user-stories": "user-stories.md",
    "implementation-plan": "implementation-plan.md",
}
FORBIDDEN_PARTS = {".z2o-state", ".z2o-patterns", "zero-to-one-product-discovery-eval-runs"}


class RevisionError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-root", required=True, help="Current z2o-artifacts/<project-slug> root.")
    parser.add_argument("--previous-root", help="Previous export root to diff against.")
    parser.add_argument("--metadata", help="Revision metadata JSON from the Controller.")
    return parser.parse_args()


def ensure_allowed_path(path: Path, label: str) -> None:
    parts = set(path.resolve().parts)
    forbidden = sorted(parts & FORBIDDEN_PARTS)
    if forbidden:
        raise RevisionError(f"{label} must not point inside forbidden runtime/history dirs: {forbidden}")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RevisionError(f"{path} must contain a JSON object")
    return data


def load_controller_actions() -> set[str]:
    data = load_json(ROOT / "evals" / "controller-actions.json")
    actions = data.get("actions")
    if not isinstance(actions, list) or not all(isinstance(item, str) for item in actions):
        raise RevisionError("controller-actions.json must contain an actions string array")
    return set(actions)


def normalize_string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RevisionError(f"metadata.{field} must be an array of strings")
    return value


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def read_text_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise RevisionError(f"Expected file, got directory: {path}")
    return path.read_text(encoding="utf-8")


def sha256_text(content: str | None) -> str | None:
    if content is None:
        return None
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def utc_now() -> tuple[str, str]:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    iso = now.isoformat().replace("+00:00", "Z")
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    return iso, f"rev-{stamp}"


def unique_revision_id(base_revision_id: str, records_dir: Path, diffs_root: Path) -> str:
    revision_id = base_revision_id
    suffix = 2
    while (records_dir / f"{revision_id}.json").exists() or (diffs_root / revision_id).exists():
        revision_id = f"{base_revision_id}-{suffix:02d}"
        suffix += 1
    return revision_id


def markdown_sections(content: str | None) -> dict[str, str]:
    if content is None:
        return {}
    sections: dict[str, list[str]] = {}
    current = "__document__"
    sections[current] = []
    for line in content.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            current = match.group(2).strip()
            sections.setdefault(current, [])
        sections[current].append(line)
    return {heading: "\n".join(lines).strip() for heading, lines in sections.items() if "\n".join(lines).strip()}


def summarize_sections(previous: str | None, current: str | None) -> list[dict[str, str]]:
    previous_sections = markdown_sections(previous)
    current_sections = markdown_sections(current)
    headings = sorted(set(previous_sections) | set(current_sections))
    summary: list[dict[str, str]] = []
    for heading in headings:
        if heading not in previous_sections:
            change_type = "added"
        elif heading not in current_sections:
            change_type = "removed"
        elif previous_sections[heading] == current_sections[heading]:
            change_type = "unchanged"
        else:
            change_type = "modified"
        summary.append({"heading": heading, "change_type": change_type})
    return summary


def unified_diff(previous: str | None, current: str | None, fromfile: str, tofile: str) -> str:
    previous_lines = [] if previous is None else previous.splitlines(keepends=True)
    current_lines = [] if current is None else current.splitlines(keepends=True)
    return "".join(difflib.unified_diff(previous_lines, current_lines, fromfile=fromfile, tofile=tofile))


def normalize_metadata(path: Path | None, export_root: Path) -> dict[str, Any]:
    if path is None:
        return {
            "project_slug": export_root.name,
            "controller_decision": "ask_user",
            "change_reason": None,
            "change_reason_status": "missing",
            "evidence_refs": [],
            "decision_refs": [],
            "audit_refs": [],
            "source_stage": "unknown",
        }

    ensure_allowed_path(path, "metadata")
    metadata = load_json(path)
    controller_actions = load_controller_actions()
    controller_decision = metadata.get("controller_decision", "ask_user")
    if controller_decision not in controller_actions:
        raise RevisionError(f"metadata.controller_decision must be one of {sorted(controller_actions)}")
    change_reason = metadata.get("change_reason")
    return {
        "project_slug": str(metadata.get("project_slug") or export_root.name),
        "controller_decision": controller_decision,
        "change_reason": change_reason if isinstance(change_reason, str) and change_reason.strip() else None,
        "change_reason_status": "provided" if isinstance(change_reason, str) and change_reason.strip() else "missing",
        "evidence_refs": normalize_string_list(metadata.get("evidence_refs", []), "evidence_refs"),
        "decision_refs": normalize_string_list(metadata.get("decision_refs", []), "decision_refs"),
        "audit_refs": normalize_string_list(metadata.get("audit_refs", []), "audit_refs"),
        "source_stage": str(metadata.get("source_stage") or "unknown"),
        "previous_revision_id": metadata.get("previous_revision_id"),
    }


def load_existing_index(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return load_json(path)


def build_revision(args: argparse.Namespace) -> dict[str, Path]:
    export_root = Path(args.export_root)
    previous_root = Path(args.previous_root) if args.previous_root else None
    metadata_path = Path(args.metadata) if args.metadata else None

    ensure_allowed_path(export_root, "export-root")
    if previous_root is not None:
        ensure_allowed_path(previous_root, "previous-root")
    if not export_root.exists() or not export_root.is_dir():
        raise RevisionError(f"export-root does not exist or is not a directory: {export_root}")
    if previous_root is not None and (not previous_root.exists() or not previous_root.is_dir()):
        raise RevisionError(f"previous-root does not exist or is not a directory: {previous_root}")

    metadata = normalize_metadata(metadata_path, export_root)
    created_at, base_revision_id = utc_now()
    revisions_dir = export_root / "revisions"
    records_dir = revisions_dir / "records"
    diffs_root = revisions_dir / "diffs"
    revision_id = unique_revision_id(base_revision_id, records_dir, diffs_root)
    diffs_dir = diffs_root / revision_id
    index_path = revisions_dir / "revision-index.json"
    record_path = records_dir / f"{revision_id}.json"
    log_path = revisions_dir / "revision-log.md"
    existing_index = load_existing_index(index_path)
    existing_artifacts = {
        item.get("artifact_name"): item
        for item in (existing_index or {}).get("artifacts", [])
        if isinstance(item, dict)
    }

    artifacts: list[dict[str, Any]] = []
    changed_artifacts: list[str] = []

    if previous_root is None:
        diffs_dir.mkdir(parents=True, exist_ok=True)
        (diffs_dir / "BASELINE.md").write_text(
            "Baseline revision: no previous export root was provided.\n", encoding="utf-8"
        )

    for artifact_name, relative_path in STABLE_ARTIFACTS.items():
        current_path = export_root / relative_path
        previous_path = previous_root / relative_path if previous_root is not None else None
        current = read_text_if_exists(current_path)
        previous = read_text_if_exists(previous_path) if previous_path is not None else None
        current_hash = sha256_text(current)
        previous_hash = sha256_text(previous)
        changed = current_hash != previous_hash
        if changed:
            changed_artifacts.append(artifact_name)

        diff_path: str | None = None
        if previous_root is not None and changed:
            diffs_dir.mkdir(parents=True, exist_ok=True)
            diff_file = diffs_dir / f"{artifact_name}.diff"
            diff_file.write_text(
                unified_diff(previous, current, f"previous/{relative_path}", f"current/{relative_path}"),
                encoding="utf-8",
            )
            diff_path = str(diff_file.relative_to(export_root))

        artifacts.append(
            {
                "artifact_name": artifact_name,
                "current_path": relative_path,
                "current_exists": current is not None,
                "current_content_hash": current_hash,
                "previous_content_hash": previous_hash,
                "changed": changed,
                "diff_path": diff_path,
                "section_summary": summarize_sections(previous, current),
            }
        )

    previous_revision_id = metadata.get("previous_revision_id")
    if previous_revision_id is None and existing_index:
        previous_revision_id = existing_index.get("latest_revision_id")

    record = {
        "schema_version": SCHEMA_VERSION,
        "package_version": PACKAGE_VERSION,
        "revision_id": revision_id,
        "project_slug": metadata["project_slug"],
        "created_at": created_at,
        "source_stage": metadata["source_stage"],
        "controller_decision": metadata["controller_decision"],
        "change_reason_status": metadata["change_reason_status"],
        "change_reason": metadata["change_reason"],
        "previous_revision_id": previous_revision_id,
        "baseline": previous_root is None,
        "changed_artifacts": changed_artifacts,
        "artifacts": artifacts,
        "evidence_refs": metadata["evidence_refs"],
        "decision_refs": metadata["decision_refs"],
        "audit_refs": metadata["audit_refs"],
        "prohibited_content": {
            "full_transcript": False,
            "full_agent_packets": False,
            "full_audit_reports": False,
            "hidden_reasoning": False,
        },
    }
    write_json(record_path, record)

    previous_records = []
    if existing_index:
        previous_records = [item for item in existing_index.get("records", []) if isinstance(item, dict)]
    records = previous_records + [
        {
            "revision_id": revision_id,
            "record_path": str(record_path.relative_to(export_root)),
            "created_at": created_at,
            "changed_artifacts": changed_artifacts,
        }
    ]

    artifact_index = []
    for item in artifacts:
        previous_entry = existing_artifacts.get(item["artifact_name"], {})
        previous_count = previous_entry.get("revision_count", 0)
        revision_count = previous_count + (1 if item["changed"] else 0)
        current_revision_id = revision_id if item["changed"] or not previous_entry else previous_entry.get("current_revision_id", revision_id)
        artifact_index.append(
            {
                "artifact_name": item["artifact_name"],
                "current_path": item["current_path"],
                "current_revision_id": current_revision_id,
                "current_content_hash": item["current_content_hash"],
                "revision_count": revision_count,
                "changed_in_latest_revision": item["changed"],
            }
        )

    index = {
        "schema_version": SCHEMA_VERSION,
        "package_version": PACKAGE_VERSION,
        "project_slug": metadata["project_slug"],
        "generated_at": created_at,
        "export_root": str(export_root),
        "latest_revision_id": revision_id,
        "latest_revision_record": str(record_path.relative_to(export_root)),
        "trace_store": {
            "mode": "skill_native_bounded",
            "ref": "revisions/",
        },
        "artifacts": artifact_index,
        "records": records,
    }
    write_json(index_path, index)
    write_revision_log(log_path, record, artifacts)
    return {"index": index_path, "record": record_path, "log": log_path}


def write_revision_log(path: Path, record: dict[str, Any], artifacts: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    changed = ", ".join(record["changed_artifacts"]) if record["changed_artifacts"] else "none"
    reason = record["change_reason"] if record["change_reason_status"] == "provided" else "MISSING"
    lines = [
        f"## {record['revision_id']}",
        "",
        f"- Created at: {record['created_at']}",
        f"- Source stage: {record['source_stage']}",
        f"- Controller decision: {record['controller_decision']}",
        f"- Change reason: {reason}",
        f"- Changed artifacts: {changed}",
        f"- Evidence refs: {', '.join(record['evidence_refs']) if record['evidence_refs'] else 'none'}",
        f"- Decision refs: {', '.join(record['decision_refs']) if record['decision_refs'] else 'none'}",
        f"- Audit refs: {', '.join(record['audit_refs']) if record['audit_refs'] else 'none'}",
        "",
        "| Artifact | Changed | Hash | Diff |",
        "|---|---:|---|---|",
    ]
    for artifact in artifacts:
        diff_path = artifact["diff_path"] or "-"
        content_hash = artifact["current_content_hash"] or "missing"
        lines.append(f"| {artifact['artifact_name']} | {artifact['changed']} | `{content_hash}` | {diff_path} |")
    lines.append("")

    if path.exists():
        previous = path.read_text(encoding="utf-8").rstrip()
        content = f"{previous}\n\n" + "\n".join(lines)
    else:
        content = "# Z2O Revision Log\n\n" + "\n".join(lines)
    path.write_text(content + "\n", encoding="utf-8")


def main() -> int:
    try:
        paths = build_revision(parse_args())
    except (OSError, json.JSONDecodeError, RevisionError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"OK revision index: {paths['index']}")
    print(f"OK revision record: {paths['record']}")
    print(f"OK revision log: {paths['log']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
