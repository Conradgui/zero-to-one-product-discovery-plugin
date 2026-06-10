#!/usr/bin/env python3
"""Validate the plugin package structure, manifest, and bundled skill.

Checks:
- .codex-plugin/plugin.json exists and is valid JSON
- Required manifest fields are present and correctly typed
- interface fields meet recommended completeness
- Bundled skill SKILL.md exists with correct frontmatter
- Skills directory structure is valid
- Assets exist (icon.png, logo.png)
- No forbidden content (eval-runs, dist, publish directories)
- Child-skills directory contains expected adapters
- Evals directory contains expected schema files
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "zero-to-one-product-discovery"
SKILL_MD = SKILL_DIR / "SKILL.md"

FORBIDDEN_PATH_PARTS = {
    "zero-to-one-product-discovery-eval-runs",
    "dist",
    "zero-to-one-product-discovery-publish",
}

REQUIRED_MANIFEST_FIELDS = ["name", "version", "description", "author", "skills", "interface"]
REQUIRED_INTERFACE_FIELDS = [
    "displayName", "shortDescription", "longDescription",
    "developerName", "category", "defaultPrompt",
]
RECOMMENDED_INTERFACE_FIELDS = [
    "capabilities", "brandColor", "composerIcon", "logo", "websiteURL",
]

EXPECTED_CHILD_SKILLS = [
    "acceptance-criteria", "adr-governance", "artifact-export",
    "context-handoff", "execution-bridge", "implementation-plan",
    "mermaid", "prd", "research-brief", "review", "revision-trace",
    "roadmap", "user-stories",
]

EXPECTED_EVAL_SCHEMAS = [
    "agent-work-order.schema.json", "agent-return-packet.schema.json",
    "audit-report.schema.json", "workbench.schema.json",
    "pattern-index.schema.json", "artifact-manifest.schema.json",
    "execution-handoff.schema.json", "revision-index.schema.json",
    "revision-record.schema.json", "eval-report.schema.json",
    "value-review.schema.json", "baseline-ab-report.schema.json",
    "controller-actions.json",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARN: {message}", file=sys.stderr)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_plugin_manifest() -> dict:
    require(PLUGIN_JSON.exists(), ".codex-plugin/plugin.json is missing")
    try:
        data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"plugin.json is invalid JSON: {exc}")
    require(isinstance(data, dict), "plugin.json must contain a JSON object")
    return data


def validate_plugin_manifest(data: dict) -> None:
    # Required fields
    for key in REQUIRED_MANIFEST_FIELDS:
        require(key in data, f"plugin.json missing required field: {key}")

    # Name must be kebab-case
    name = data["name"]
    require(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name), f"plugin name must be kebab-case: {name}")

    # Version must be SemVer-like
    version = data["version"]
    require(
        re.match(r"^\d+\.\d+\.\d+(-[\w.]+)?$", version),
        f"plugin version must be SemVer: {version}",
    )

    # Skills path
    require(data["skills"] == "./skills/", "plugin skills path must be ./skills/")

    # Author must be an object with name
    author = data["author"]
    require(isinstance(author, dict) and "name" in author, "author must be an object with 'name'")

    # Should not declare components that don't exist
    if "mcpServers" in data:
        warn("plugin declares mcpServers but no .mcp.json exists at root")
    if "apps" in data:
        warn("plugin declares apps but no .app.json exists at root")
    if "hooks" in data:
        warn("plugin declares hooks but no hooks/ directory exists at root")

    # Interface validation
    interface = data.get("interface")
    require(isinstance(interface, dict), "interface must be an object")

    for key in REQUIRED_INTERFACE_FIELDS:
        require(key in interface, f"interface missing required field: {key}")

    # defaultPrompt validation
    prompts = interface["defaultPrompt"]
    require(isinstance(prompts, list), "interface.defaultPrompt must be a list")
    require(1 <= len(prompts) <= 5, "interface.defaultPrompt must include 1-5 prompts")
    for prompt in prompts:
        require(isinstance(prompt, str) and prompt.strip(), "default prompts must be non-empty strings")
        require(len(prompt) <= 256, f"default prompt too long ({len(prompt)} chars, max 256): {prompt[:60]}...")

    # capabilities validation
    caps = interface.get("capabilities", [])
    require(isinstance(caps, list) and len(caps) > 0, "interface.capabilities should be a non-empty list")

    # Report recommended fields
    for key in RECOMMENDED_INTERFACE_FIELDS:
        if key not in interface:
            warn(f"interface missing recommended field: {key}")


def validate_skill_structure() -> None:
    require(SKILL_DIR.exists(), f"bundled skill directory missing: {SKILL_DIR}")
    require(SKILL_MD.exists(), "bundled skill SKILL.md is missing")

    # Validate frontmatter
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    require(match is not None, "bundled skill SKILL.md missing YAML frontmatter")
    frontmatter = match.group(1)
    require(
        re.search(r"^name:\s*zero-to-one-product-discovery\s*$", frontmatter, re.M) is not None,
        "skill frontmatter name mismatch",
    )
    require(
        re.search(r"^description:\s*\S", frontmatter, re.M) is not None,
        "skill frontmatter description missing",
    )


def validate_child_skills() -> None:
    child_skills_dir = SKILL_DIR / "child-skills"
    require(child_skills_dir.exists(), "child-skills/ directory missing from bundled skill")

    for name in EXPECTED_CHILD_SKILLS:
        skill_path = child_skills_dir / name
        require(skill_path.exists(), f"missing expected child-skill: {name}")
        adapter = skill_path / "ADAPTER.md"
        require(adapter.exists(), f"missing ADAPTER.md for child-skill: {name}")


def validate_evals() -> None:
    evals_dir = SKILL_DIR / "evals"
    require(evals_dir.exists(), "evals/ directory missing from bundled skill")

    for name in EXPECTED_EVAL_SCHEMAS:
        schema_path = evals_dir / name
        if not schema_path.exists():
            warn(f"missing expected eval schema: {name}")


def validate_assets() -> None:
    assets_dir = ROOT / "assets"
    require(assets_dir.exists(), "assets/ directory missing")

    icon = assets_dir / "icon.png"
    logo = assets_dir / "logo.png"
    require(icon.exists(), "assets/icon.png missing")
    require(logo.exists(), "assets/logo.png missing")

    # Check file sizes (should be > 0)
    require(icon.stat().st_size > 0, "assets/icon.png is empty")
    require(logo.stat().st_size > 0, "assets/logo.png is empty")


def validate_forbidden_content() -> None:
    for path in ROOT.rglob("*"):
        rel_parts = set(path.relative_to(ROOT).parts)
        overlap = rel_parts & FORBIDDEN_PATH_PARTS
        require(not overlap, f"forbidden package content found: {path.relative_to(ROOT)}")


def validate_required_files() -> None:
    require((ROOT / "README.md").exists(), "README.md missing from plugin root")
    require((ROOT / "CHANGELOG.md").exists(), "CHANGELOG.md missing from plugin root")
    require((ROOT / "LICENSE").exists(), "LICENSE missing from plugin root")


def main() -> None:
    print(f"Validating plugin at: {ROOT}")
    print()

    data = load_plugin_manifest()
    print(f"  name:    {data['name']}")
    print(f"  version: {data['version']}")
    print()

    validate_plugin_manifest(data)
    print("  [OK] plugin.json manifest")

    validate_skill_structure()
    print("  [OK] skill structure and SKILL.md frontmatter")

    validate_child_skills()
    print(f"  [OK] child-skills ({len(EXPECTED_CHILD_SKILLS)} adapters)")

    validate_evals()
    print("  [OK] eval schemas")

    validate_assets()
    print("  [OK] assets")

    validate_forbidden_content()
    print("  [OK] no forbidden content")

    validate_required_files()
    print("  [OK] required files (README, CHANGELOG, LICENSE)")

    print()
    print("Plugin package validation passed.")


if __name__ == "__main__":
    main()
