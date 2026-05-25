#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
SKILL_MD = ROOT / "skills" / "zero-to-one-product-discovery" / "SKILL.md"
FORBIDDEN_PATH_PARTS = {
    "zero-to-one-product-discovery-eval-runs",
    "dist",
    "zero-to-one-product-discovery-publish.kA4KBo",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


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
    for key in ["name", "version", "description", "author", "skills", "interface"]:
        require(key in data, f"plugin.json missing required field: {key}")
    require(data["name"] == "zero-to-one-product-discovery-plugin", "plugin name mismatch")
    require(data["version"] == "0.2.1", "plugin version should match the seeded skill release")
    require(data["skills"] == "./skills/", "plugin skills path must be ./skills/")
    require("mcpServers" not in data, "plugin must not declare mcpServers without .mcp.json")
    require("apps" not in data, "plugin must not declare apps without .app.json")
    require("hooks" not in data, "plugin must not declare unsupported hooks")
    interface = data["interface"]
    require(isinstance(interface, dict), "interface must be an object")
    for key in ["displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"]:
        require(key in interface, f"interface missing required field: {key}")
    prompts = interface["defaultPrompt"]
    require(isinstance(prompts, list), "interface.defaultPrompt must be a list")
    require(1 <= len(prompts) <= 3, "interface.defaultPrompt must include one to three prompts")
    for prompt in prompts:
        require(isinstance(prompt, str) and prompt.strip(), "default prompts must be non-empty strings")
        require(len(prompt) <= 128, "default prompts must be at most 128 characters")


def validate_skill_frontmatter() -> None:
    require(SKILL_MD.exists(), "bundled skill SKILL.md is missing")
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    require(match is not None, "bundled skill SKILL.md missing YAML frontmatter")
    frontmatter = match.group(1)
    require(re.search(r"^name:\s*zero-to-one-product-discovery\s*$", frontmatter, re.M) is not None, "skill frontmatter name mismatch")
    require(re.search(r"^description:\s*\S", frontmatter, re.M) is not None, "skill frontmatter description missing")


def validate_forbidden_content() -> None:
    for path in ROOT.rglob("*"):
        rel_parts = set(path.relative_to(ROOT).parts)
        overlap = rel_parts & FORBIDDEN_PATH_PARTS
        require(not overlap, f"forbidden package content found: {path.relative_to(ROOT)}")


def main() -> None:
    data = load_plugin_manifest()
    validate_plugin_manifest(data)
    validate_skill_frontmatter()
    validate_forbidden_content()
    print("plugin package validation ok")


if __name__ == "__main__":
    main()
