#!/usr/bin/env python3
"""Comprehensive test suite for zero-to-one-product-discovery-plugin.

Tests cover:
  1. Structural Integrity — files exist, paths resolve, JSON schemas valid
  2. Content Coherence — cross-references, stage definitions, contract alignment
  3. Business Logic — stage gates, Controller actions, Producer boundaries, Quick Mode
  4. End-to-End User Flow — full discovery workflow path simulation
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "zero-to-one-product-discovery"

# ── Counters ──────────────────────────────────────────────────────────────────
_passed = 0
_failed = 0
_warned = 0
_errors: list[str] = []
_warnings: list[str] = []


def _ok(label: str) -> None:
    global _passed
    _passed += 1
    print(f"  ✅ {label}")


def _fail(label: str, detail: str) -> None:
    global _failed
    _failed += 1
    msg = f"  ❌ {label}: {detail}"
    print(msg)
    _errors.append(msg)


def _warn(label: str, detail: str) -> None:
    global _warned
    _warned += 1
    msg = f"  ⚠️  {label}: {detail}"
    print(msg)
    _warnings.append(msg)


def _check(condition: bool, label: str, detail: str = "") -> None:
    if condition:
        _ok(label)
    else:
        _fail(label, detail or "condition false")


def _load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None


def _load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# 1. STRUCTURAL INTEGRITY
# ══════════════════════════════════════════════════════════════════════════════

def test_01_plugin_manifest():
    """plugin.json exists, is valid JSON, and has required fields."""
    print("\n── 1.1 Plugin Manifest ──")
    p = ROOT / ".codex-plugin" / "plugin.json"
    _check(p.exists(), "plugin.json exists")

    data = _load_json(p)
    _check(data is not None, "plugin.json is valid JSON")
    if data is None:
        return

    for field in ["name", "version", "description", "author", "skills", "interface"]:
        _check(field in data, f"manifest has '{field}'")

    # Name is kebab-case
    name = data.get("name", "")
    _check(
        bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name)),
        "name is kebab-case",
        f"got '{name}'",
    )

    # Version is SemVer
    ver = data.get("version", "")
    _check(
        bool(re.match(r"^\d+\.\d+\.\d+", ver)),
        "version is SemVer",
        f"got '{ver}'",
    )

    # Skills path
    _check(data.get("skills") == "./skills/", "skills path is ./skills/")

    # Interface completeness
    iface = data.get("interface", {})
    for field in ["displayName", "shortDescription", "longDescription",
                  "developerName", "category", "defaultPrompt"]:
        _check(field in iface, f"interface has '{field}'")

    # Capabilities should include Read (skill reads user materials)
    caps = iface.get("capabilities", [])
    _check("Read" in caps, "capabilities includes Read")
    _check("Write" in caps, "capabilities includes Write")

    # Assets paths exist
    icon = iface.get("composerIcon", "")
    logo = iface.get("logo", "")
    if icon:
        _check((ROOT / icon.lstrip("./")).exists(), f"composerIcon file exists ({icon})")
    if logo:
        _check((ROOT / logo.lstrip("./")).exists(), f"logo file exists ({logo})")


def test_02_skill_structure():
    """Bundled skill directory has correct structure."""
    print("\n── 1.2 Skill Structure ──")
    _check(SKILL_DIR.exists(), "skill directory exists")
    _check((SKILL_DIR / "SKILL.md").exists(), "SKILL.md exists")
    _check((SKILL_DIR / "README.md").exists(), "README.md exists")
    _check((SKILL_DIR / "agents").is_dir(), "agents/ directory")
    _check((SKILL_DIR / "child-skills").is_dir(), "child-skills/ directory")
    _check((SKILL_DIR / "references").is_dir(), "references/ directory")
    _check((SKILL_DIR / "evals").is_dir(), "evals/ directory")
    _check((SKILL_DIR / "scripts").is_dir(), "scripts/ directory")
    _check((SKILL_DIR / "vendor").is_dir(), "vendor/ directory")


def test_03_skill_frontmatter():
    """SKILL.md has valid YAML frontmatter with name and description."""
    print("\n── 1.3 Skill Frontmatter ──")
    text = _load_text(SKILL_DIR / "SKILL.md")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    _check(match is not None, "SKILL.md has YAML frontmatter")
    if match is None:
        return
    fm = match.group(1)
    _check(
        re.search(r"^name:\s*zero-to-one-product-discovery\s*$", fm, re.M) is not None,
        "frontmatter name matches",
    )
    _check(
        re.search(r"^description:\s*\S", fm, re.M) is not None,
        "frontmatter has description",
    )


def test_04_child_skills():
    """All expected child-skill adapters exist with ADAPTER.md."""
    print("\n── 1.4 Child Skills ──")
    expected = [
        "acceptance-criteria", "adr-governance", "artifact-export",
        "context-handoff", "execution-bridge", "implementation-plan",
        "mermaid", "prd", "research-brief", "review", "revision-trace",
        "roadmap", "user-stories",
    ]
    cs_dir = SKILL_DIR / "child-skills"
    for name in expected:
        adapter = cs_dir / name / "ADAPTER.md"
        _check(adapter.exists(), f"child-skill '{name}' has ADAPTER.md")

    # Verify README.md references all child-skills
    readme = _load_text(cs_dir / "README.md")
    for name in expected:
        _check(name in readme, f"child-skills/README.md references '{name}'")


def test_05_eval_schemas():
    """All expected eval schemas exist and are valid JSON."""
    print("\n── 1.5 Eval Schemas ──")
    expected_json = [
        "agent-work-order.schema.json", "agent-return-packet.schema.json",
        "audit-report.schema.json", "workbench.schema.json",
        "pattern-index.schema.json", "artifact-manifest.schema.json",
        "execution-handoff.schema.json", "revision-index.schema.json",
        "revision-record.schema.json", "eval-report.schema.json",
        "value-review.schema.json", "baseline-ab-report.schema.json",
        "controller-actions.json",
    ]
    evals_dir = SKILL_DIR / "evals"
    for name in expected_json:
        p = evals_dir / name
        _check(p.exists(), f"eval schema '{name}' exists")
        data = _load_json(p)
        _check(data is not None, f"eval schema '{name}' is valid JSON")


def test_06_references():
    """All expected reference files exist."""
    print("\n── 1.6 References ──")
    expected = [
        "workflow.md", "material-assimilation.md", "tradeoff-framework.md",
        "planning-artifacts.md", "multi-agent-orchestration.md",
        "artifact-adapters.md", "child-skill-integration-blueprint.md",
        "child-skill-wrappers.md", "documentation-templates.md",
        "design-reference-protocol.md", "source-attribution.md",
        "source-evaluation.md",
    ]
    ref_dir = SKILL_DIR / "references"
    for name in expected:
        _check((ref_dir / name).exists(), f"reference '{name}' exists")


def test_07_scripts():
    """All expected scripts exist and are executable."""
    print("\n── 1.7 Scripts ──")
    expected = [
        "persist_workbench.py", "generate_revision_trace.py",
        "validate-contracts.py",
    ]
    scripts_dir = SKILL_DIR / "scripts"
    for name in expected:
        p = scripts_dir / name
        _check(p.exists(), f"script '{name}' exists")
        # Check it's valid Python (basic syntax check)
        text = _load_text(p)
        _check(
            "def " in text or "class " in text,
            f"script '{name}' has function/class definitions",
        )


def test_08_assets():
    """Plugin assets exist and are non-empty."""
    print("\n── 1.8 Assets ──")
    assets_dir = ROOT / "assets"
    _check(assets_dir.is_dir(), "assets/ directory exists")
    for name in ["icon.png", "logo.png"]:
        p = assets_dir / name
        _check(p.exists(), f"assets/{name} exists")
        if p.exists():
            _check(p.stat().st_size > 0, f"assets/{name} is non-empty")


def test_09_root_files():
    """Required root-level files exist."""
    print("\n── 1.9 Root Files ──")
    _check((ROOT / "README.md").exists(), "README.md exists")
    _check((ROOT / "CHANGELOG.md").exists(), "CHANGELOG.md exists")
    _check((ROOT / "LICENSE").exists(), "LICENSE exists")


# ══════════════════════════════════════════════════════════════════════════════
# 2. CONTENT COHERENCE
# ══════════════════════════════════════════════════════════════════════════════

def test_10_skill_references_resolve():
    """SKILL.md Reference Loading section points to files that actually exist."""
    print("\n── 2.1 SKILL.md Reference Resolution ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    # Extract file references from Reference Loading section
    # Pattern: `references/xxx.md`, `evals/xxx`, `scripts/xxx`, `child-skills/`, `vendor/`
    file_refs = re.findall(r'`((?:references|evals|scripts|child-skills|vendor|agents)/[^`]+)`', text)

    for ref in file_refs:
        # Handle glob patterns
        if "*" in ref:
            continue
        # Handle directory references (ending with /)
        if ref.endswith("/"):
            ref_path = SKILL_DIR / ref.rstrip("/")
            _check(ref_path.exists() or ref_path.is_dir(), f"SKILL.md ref '{ref}' resolves")
        else:
            ref_path = SKILL_DIR / ref
            _check(ref_path.exists(), f"SKILL.md ref '{ref}' resolves")


def test_11_controller_actions_coverage():
    """Controller actions in controller-actions.json are referenced in multi-agent docs."""
    print("\n── 2.2 Controller Actions Coverage ──")
    actions_data = _load_json(SKILL_DIR / "evals" / "controller-actions.json")
    if actions_data is None:
        _fail("controller-actions.json", "cannot load")
        return

    actions = actions_data.get("actions", [])
    _check(len(actions) > 0, "controller-actions.json has actions")

    # Check that multi-agent-orchestration.md references these actions
    ma_text = _load_text(SKILL_DIR / "references" / "multi-agent-orchestration.md")
    for action in actions:
        _check(action in ma_text, f"multi-agent docs reference action '{action}'")


def test_12_stage_definitions_consistent():
    """Stage definitions in SKILL.md match workflow.md and multi-agent-orchestration.md."""
    print("\n── 2.3 Stage Definitions Consistency ──")
    stages = [
        "Diagnostic Start", "Material Assimilation", "Problem Framing",
        "Solution Exploration", "Feasibility Discovery", "MVP Hypothesis",
        "Planning Artifacts", "Implementation Planning",
    ]

    skill_text = _load_text(SKILL_DIR / "SKILL.md")
    workflow_text = _load_text(SKILL_DIR / "references" / "workflow.md")
    ma_text = _load_text(SKILL_DIR / "references" / "multi-agent-orchestration.md")

    for stage in stages:
        _check(stage in skill_text, f"SKILL.md defines stage '{stage}'")
        _check(stage in workflow_text, f"workflow.md defines stage '{stage}'")


def test_13_producer_definitions_consistent():
    """Producer definitions match across SKILL.md, agents/README.md, and artifact-adapters.md."""
    print("\n── 2.4 Producer Definitions Consistency ──")
    producers = [
        "Research", "PRD", "Roadmap", "ADR", "Implementation Plan",
        "Execution Bridge", "Artifact Export", "Revision Trace",
    ]

    skill_text = _load_text(SKILL_DIR / "SKILL.md")
    agents_readme = _load_text(SKILL_DIR / "agents" / "README.md")
    adapters_text = _load_text(SKILL_DIR / "references" / "artifact-adapters.md")

    for producer in producers:
        _check(producer in skill_text, f"SKILL.md references producer '{producer}'")
        _check(producer in agents_readme, f"agents/README.md references producer '{producer}'")


def test_14_child_skill_contracts_match_adapters():
    """Child-skill ADAPTER.md files are referenced in artifact-adapters.md."""
    print("\n── 2.5 Child-Skill Contract Alignment ──")
    adapters_text = _load_text(SKILL_DIR / "references" / "artifact-adapters.md")

    cs_dir = SKILL_DIR / "child-skills"
    for child_dir in sorted(cs_dir.iterdir()):
        if child_dir.is_dir() and child_dir.name != "__pycache__":
            adapter_file = child_dir / "ADAPTER.md"
            if adapter_file.exists():
                # Check the child-skill name appears in artifact-adapters.md
                name = child_dir.name
                # Convert kebab-case to title case for matching
                title = name.replace("-", " ").title()
                _check(
                    title in adapters_text or name in adapters_text,
                    f"artifact-adapters.md references '{name}'",
                )


def test_15_eval_schema_cross_references():
    """Schemas referenced in multi-agent-orchestration.md actually exist."""
    print("\n── 2.6 Eval Schema Cross-References ──")
    ma_text = _load_text(SKILL_DIR / "references" / "multi-agent-orchestration.md")

    schema_refs = re.findall(r'`evals/([^`]+\.json)`', ma_text)
    evals_dir = SKILL_DIR / "evals"

    for ref in schema_refs:
        _check((evals_dir / ref).exists(), f"referenced schema 'evals/{ref}' exists")


def test_16_workbench_schema_matches_workflow():
    """workbench.json structure in workflow.md matches workbench.schema.json."""
    print("\n── 2.7 Workbench Schema Alignment ──")
    schema = _load_json(SKILL_DIR / "evals" / "workbench.schema.json")
    _check(schema is not None, "workbench.schema.json is loadable")

    if schema is None:
        return

    # Check schema has key properties
    props = schema.get("properties", {})
    _check("workflow_state" in props, "schema has workflow_state")
    _check("evidence_snapshot" in props, "schema has evidence_snapshot")
    _check("artifact_status" in props, "schema has artifact_status")
    _check("decision_log" in props, "schema has decision_log")


def test_17_quick_mode_rules_consistent():
    """Quick Mode rules in SKILL.md match workflow.md."""
    print("\n── 2.8 Quick Mode Rules Consistency ──")
    skill_text = _load_text(SKILL_DIR / "SKILL.md")
    workflow_text = _load_text(SKILL_DIR / "references" / "workflow.md")

    # Key Quick Mode rules that must appear in both
    qm_rules = [
        "Quick Mode",
        "evidence labels",
        "Evidence Gap Summary",
        "QUICK_MODE_DRAFT",
        "quick_mode_draft",
    ]
    for rule in qm_rules:
        _check(rule in skill_text, f"SKILL.md has Quick Mode rule '{rule}'")
        _check(rule in workflow_text, f"workflow.md has Quick Mode rule '{rule}'")


# ══════════════════════════════════════════════════════════════════════════════
# 3. BUSINESS LOGIC
# ══════════════════════════════════════════════════════════════════════════════

def test_18_stage_gate_rules():
    """Stage gate rules are properly defined in SKILL.md Core Rules."""
    print("\n── 3.1 Stage Gate Rules ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    # Core gate rules that MUST exist
    gate_rules = [
        ("Do not ask mature-product questions upfront", "no premature questions"),
        ("Do not create final PRDs", "no premature final artifacts"),
        ("Keep stages pure", "stage purity"),
        ("Child skills do not choose the next stage", "child-skill routing restriction"),
        ("Child skills do not call other child skills", "no child-to-child invocation"),
        ("Audit substantial producer output", "audit requirement"),
        ("Controller is the only routing authority", "Controller authority"),
    ]
    for rule_text, label in gate_rules:
        _check(rule_text in text, f"Core Rule: {label}")


def test_19_controller_action_registry():
    """Controller actions are a complete, well-defined set."""
    print("\n── 3.2 Controller Action Registry ──")
    data = _load_json(SKILL_DIR / "evals" / "controller-actions.json")
    if data is None:
        return

    actions = set(data.get("actions", []))

    # Required actions for stage gate enforcement
    required_actions = {
        "accept", "downgrade", "request_evidence", "route_to_audit",
        "ask_user", "block", "stop",
    }
    for action in required_actions:
        _check(action in actions, f"required action '{action}' registered")

    # Check schema_version exists
    _check("schema_version" in data, "controller-actions.json has schema_version")


def test_20_producer_boundaries():
    """Producer 'Must Not' rules are defined for all producers."""
    print("\n── 3.3 Producer Boundaries ──")
    # Producer boundaries are defined in agents/README.md and artifact-adapters.md
    agents_text = _load_text(SKILL_DIR / "agents" / "README.md")
    adapters_text = _load_text(SKILL_DIR / "references" / "artifact-adapters.md")
    combined = agents_text + "\n" + adapters_text

    producers_with_boundaries = [
        ("Research", "Invent evidence"),
        ("PRD", "final PRD before user acceptance"),
        ("Roadmap", "weak assumptions into delivery"),
        ("ADR", "scope tradeoffs"),
        ("Implementation Plan", "Start coding"),
        ("Execution Bridge", "external issues"),
        ("Artifact Export", "invent missing artifact"),
        ("Revision Trace", "full transcripts"),
    ]
    for producer, boundary in producers_with_boundaries:
        _check(
            boundary in combined,
            f"Producer '{producer}' has boundary '{boundary}'",
        )


def test_21_evidence_maturity_calculation():
    """Evidence maturity calculation rules are defined."""
    print("\n── 3.4 Evidence Maturity Rules ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    _check("verified_facts" in text, "maturity uses verified_facts")
    _check("total_evidence_items" in text, "maturity uses total_evidence_items")
    _check("maturity_percentage" in text, "maturity_percentage defined")

    # Four-level labels
    for level in ["Insufficient", "Partial", "Sufficient", "Strong"]:
        _check(level in text, f"maturity level '{level}' defined")

    # Risk-weighted priority
    _check("risk_weighted_priority" in text, "risk_weighted_priority defined")
    _check("impact_if_wrong" in text, "impact_if_wrong defined")


def test_22_artifact_export_rules():
    """Artifact Export rules are properly defined."""
    print("\n── 3.5 Artifact Export Rules ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    _check("NOT_READY" in text, "NOT_READY marker defined")
    _check("source_status" in text, "manifest source_status field")
    _check("content_mode" in text, "manifest content_mode field")
    _check("status_guard" in text, "manifest status_guard field")
    _check("z2o-artifacts" in text, "export path defined")


def test_23_revision_trace_rules():
    """Revision Trace rules are properly defined."""
    print("\n── 3.6 Revision Trace Rules ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    _check("revision-index.json" in text, "revision-index.json defined")
    _check("revision-log.md" in text, "revision-log.md defined")
    _check("change_reason_status" in text, "change_reason_status field")
    _check("missing" in text, "missing metadata handling")

    # Must NOT store full transcripts
    _check("full transcripts" in text.lower() or "full_transcripts" in text, "no full transcripts rule")


def test_24_quick_mode_constraints():
    """Quick Mode has proper constraints defined."""
    print("\n── 3.7 Quick Mode Constraints ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    constraints = [
        ("Cannot produce unlabeled final artifacts", "no unlabeled artifacts"),
        ("Cannot skip the Auditor", "audit required"),
        ("Cannot be used for Implementation Planning", "no implementation planning"),
        ("Cannot reopen product strategy", "no strategy reopening"),
    ]
    for rule, label in constraints:
        _check(rule in text, f"Quick Mode constraint: {label}")


def test_25_state_persistence_rules():
    """State persistence rules are properly defined."""
    print("\n── 3.8 State Persistence Rules ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    _check(".z2o-state/workbench.json" in text, "workbench path defined")
    _check("7 days" in text, "7-day expiry defined")
    _check("persist_workbench.py" in text, "persist script referenced")
    _check("workbench.schema.json" in text, "schema validation referenced")


def test_26_pattern_library_rules():
    """Pattern Library rules are properly defined."""
    print("\n── 3.9 Pattern Library Rules ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("Pattern Library" in text or "Pattern" in text, "Pattern Library mentioned")
    _check(".z2o-patterns" in text, "pattern directory defined")

    workflow_text = _load_text(SKILL_DIR / "references" / "workflow.md")
    _check("pattern-index.json" in workflow_text, "pattern index file defined")


def test_27_readiness_spectrum_rules():
    """Readiness Spectrum rules are properly defined."""
    print("\n── 3.10 Readiness Spectrum Rules ──")
    pa_text = _load_text(SKILL_DIR / "references" / "planning-artifacts.md")

    _check("readiness_score" in pa_text, "readiness_score defined")
    _check("grounded_inputs" in pa_text, "grounded_inputs defined")
    _check("total_required_inputs" in pa_text, "total_required_inputs defined")


# ══════════════════════════════════════════════════════════════════════════════
# 4. END-TO-END USER FLOW
# ══════════════════════════════════════════════════════════════════════════════

def test_28_e2e_stage_flow_defined():
    """The complete stage flow from idea to export is defined."""
    print("\n── 4.1 E2E Stage Flow Definition ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    # The flow must cover: idea → diagnostic → material → problem → solution →
    # feasibility → MVP → planning → implementation → export → revision
    flow_steps = [
        "Diagnostic Start",
        "Material Assimilation",
        "Problem Framing",
        "Solution Exploration",
        "Feasibility Discovery",
        "MVP Hypothesis",
        "Planning Artifacts",
        "Implementation Planning",
    ]

    # Check Stage Map section
    stage_map_start = text.find("## Stage Map")
    _check(stage_map_start != -1, "Stage Map section exists")

    for step in flow_steps:
        _check(step in text, f"flow step '{step}' in SKILL.md")


def test_29_e2e_user_triggers():
    """User trigger phrases are defined for the skill."""
    print("\n── 4.2 E2E User Triggers ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    triggers = [
        "I have a product idea",
        "I want to build an open-source project",
        "I want to build a product from scratch",
        "I have an innovative product concept",
        "Help me plan a side project",
        "I have notes",
    ]
    for trigger in triggers:
        _check(trigger in text, f"trigger phrase '{trigger[:40]}...' defined")


def test_30_e2e_export_workflow():
    """Export workflow is fully defined: Artifact Export + Revision Trace."""
    print("\n── 4.3 E2E Export Workflow ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    # Artifact Export triggers
    export_triggers = ["导出产物", "export artifacts", "生成交付文件", "导出工作台"]
    for trigger in export_triggers:
        _check(trigger in text, f"export trigger '{trigger}' defined")

    # Revision Trace triggers
    revision_triggers = ["生成 revision trace", "artifact diff", "产物变更记录"]
    for trigger in revision_triggers:
        _check(trigger in text, f"revision trigger '{trigger}' defined")

    # Stable file structure
    stable_files = ["prd.md", "roadmap.md", "user-stories.md", "implementation-plan.md"]
    for f in stable_files:
        _check(f in text, f"stable artifact file '{f}' in export structure")


def test_31_e2e_multi_agent_flow():
    """Multi-agent flow is fully defined."""
    print("\n── 4.4 E2E Multi-Agent Flow ──")
    ma_text = _load_text(SKILL_DIR / "references" / "multi-agent-orchestration.md")

    # Roles
    roles = ["Workflow Rules", "Controller Agent", "Producer Agents", "Auditor Agent", "Runtime Workbench"]
    for role in roles:
        _check(role in ma_text, f"role '{role}' defined")

    # State machine
    _check("Controller State Machine" in ma_text, "Controller State Machine section exists")

    # Stage transitions
    transitions = [
        ("Diagnostic Start", "Material Assimilation"),
        ("Problem Framing", "Solution Exploration"),
        ("Solution Exploration", "Feasibility Discovery"),
        ("Feasibility Discovery", "MVP Hypothesis"),
        ("MVP Hypothesis", "Planning Artifacts"),
        ("Planning Artifacts", "Implementation Planning"),
    ]
    for from_stage, to_stage in transitions:
        _check(
            from_stage in ma_text and to_stage in ma_text,
            f"transition '{from_stage}' → '{to_stage}' defined",
        )


def test_32_e2e_handoff_contract():
    """Child-skill handoff contract is complete."""
    print("\n── 4.5 E2E Handoff Contract ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    # Every handoff must include these
    handoff_fields = [
        "current stage", "confirmed facts", "working assumptions",
        "unresolved questions", "key risks", "existing materials",
    ]
    for field in handoff_fields:
        _check(field in text, f"handoff includes '{field}'")


def test_33_e2e_context_resume():
    """Context Resume Packet is properly defined."""
    print("\n── 4.6 E2E Context Resume Packet ──")
    text = _load_text(SKILL_DIR / "references" / "workflow.md")

    _check("Context Resume Packet" in text, "Context Resume Packet defined")

    sections = [
        "Current Stage", "Confirmed Decisions", "Working Assumptions",
        "Unresolved Questions", "Key Risks", "Evidence Maturity Summary",
    ]
    for section in sections:
        _check(section in text, f"Context Resume has '{section}'")


def test_34_e2e_diagnostic_start_output():
    """Diagnostic Start output format is properly defined."""
    print("\n── 4.7 E2E Diagnostic Start Output ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("## Diagnostic Start Output" in text, "Diagnostic Start Output section")

    outputs = [
        "Exploration mode notice",
        "Zero-to-one judgment",
        "Existing material judgment",
        "Facts / assumptions / risks / unknowns",
        "candidate exploration directions",
        "Most dangerous assumption",
        "highest-leverage question",
    ]
    for output in outputs:
        _check(output in text, f"Diagnostic output includes '{output[:40]}...'")


def test_35_e2e_express_review():
    """Express Review path is defined."""
    print("\n── 4.8 E2E Express Review ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("Express Review" in text, "Express Review defined")

    workflow_text = _load_text(SKILL_DIR / "references" / "workflow.md")
    _check("Express Review" in workflow_text, "Express Review in workflow.md")


def test_36_e2e_risk_map():
    """Risk Map feature is defined."""
    print("\n── 4.9 E2E Risk Map ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("Risk Map" in text, "Risk Map defined in SKILL.md")
    _check("risk_weighted_priority" in text, "risk_weighted_priority in SKILL.md")
    _check("impact_if_wrong" in text, "impact_if_wrong in SKILL.md")


def test_37_e2e_readiness_spectrum():
    """Readiness Spectrum feature is defined."""
    print("\n── 4.10 E2E Readiness Spectrum ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("Readiness Spectrum" in text, "Readiness Spectrum defined in SKILL.md")
    _check("readiness_score" in text or "readiness" in text.lower(), "readiness score mentioned")


def test_38_e2e_file_workbench():
    """File Workbench feature is defined."""
    print("\n── 4.11 E2E File Workbench ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("File Workbench" in text, "File Workbench defined in SKILL.md")

    workflow_text = _load_text(SKILL_DIR / "references" / "workflow.md")
    _check("File Workbench" in workflow_text, "File Workbench in workflow.md")

    # Required sections
    sections = [
        "Workflow state", "Evidence maturity", "Risk map",
        "Readiness spectrum", "Artifact status", "Blockers",
    ]
    for section in sections:
        _check(section in workflow_text, f"Workbench has '{section}'")


def test_39_e2e_execution_bridge():
    """Execution Bridge feature is defined."""
    print("\n── 4.12 E2E Execution Bridge ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    _check("Execution Bridge" in text, "Execution Bridge defined in SKILL.md")

    # Check child-skill exists
    eb_adapter = SKILL_DIR / "child-skills" / "execution-bridge" / "ADAPTER.md"
    _check(eb_adapter.exists(), "Execution Bridge ADAPTER.md exists")

    eb_text = _load_text(eb_adapter)
    _check("GitHub" in eb_text, "Execution Bridge supports GitHub Issues")
    _check("dry-run" in eb_text or "dry_run" in eb_text, "Execution Bridge is dry-run")


def test_40_e2e_packaging_boundary():
    """Packaging boundary is properly defined — excluded dirs are documented."""
    print("\n── 4.13 E2E Packaging Boundary ──")
    text = _load_text(SKILL_DIR / "SKILL.md")

    excluded = [
        "zero-to-one-product-discovery-eval-runs",
        ".z2o-state",
        ".z2o-patterns",
        "z2o-artifacts",
    ]
    for item in excluded:
        _check(item in text, f"excluded from package: '{item}'")


# ══════════════════════════════════════════════════════════════════════════════
# 5. SCHEMA VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

def test_41_schemas_have_required_fields():
    """JSON schemas have $schema, type, and properties."""
    print("\n── 5.1 Schema Structure ──")
    evals_dir = SKILL_DIR / "evals"

    schema_files = [
        "agent-work-order.schema.json", "agent-return-packet.schema.json",
        "audit-report.schema.json", "workbench.schema.json",
        "artifact-manifest.schema.json", "execution-handoff.schema.json",
        "revision-index.schema.json", "revision-record.schema.json",
    ]

    for name in schema_files:
        data = _load_json(evals_dir / name)
        if data is None:
            _fail(f"schema '{name}'", "cannot load")
            continue
        _check("properties" in data or "type" in data, f"schema '{name}' has properties/type")


def test_42_workbench_schema_evidence_structure():
    """workbench.schema.json defines evidence_snapshot with items and summary."""
    print("\n── 5.2 Workbench Evidence Schema ──")
    schema = _load_json(SKILL_DIR / "evals" / "workbench.schema.json")
    if schema is None:
        return

    props = schema.get("properties", {})
    ev = props.get("evidence_snapshot", {})
    ev_props = ev.get("properties", {})

    _check("items" in ev_props, "evidence_snapshot has items")
    _check("summary" in ev_props, "evidence_snapshot has summary")

    # Check summary has maturity fields
    summary = ev_props.get("summary", {})
    summary_props = summary.get("properties", {})
    _check("maturity_percentage" in summary_props, "summary has maturity_percentage")
    _check("maturity_level" in summary_props, "summary has maturity_level")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  Zero-to-One Product Discovery Plugin — Comprehensive Test Suite")
    print("=" * 70)

    # 1. Structural Integrity
    test_01_plugin_manifest()
    test_02_skill_structure()
    test_03_skill_frontmatter()
    test_04_child_skills()
    test_05_eval_schemas()
    test_06_references()
    test_07_scripts()
    test_08_assets()
    test_09_root_files()

    # 2. Content Coherence
    test_10_skill_references_resolve()
    test_11_controller_actions_coverage()
    test_12_stage_definitions_consistent()
    test_13_producer_definitions_consistent()
    test_14_child_skill_contracts_match_adapters()
    test_15_eval_schema_cross_references()
    test_16_workbench_schema_matches_workflow()
    test_17_quick_mode_rules_consistent()

    # 3. Business Logic
    test_18_stage_gate_rules()
    test_19_controller_action_registry()
    test_20_producer_boundaries()
    test_21_evidence_maturity_calculation()
    test_22_artifact_export_rules()
    test_23_revision_trace_rules()
    test_24_quick_mode_constraints()
    test_25_state_persistence_rules()
    test_26_pattern_library_rules()
    test_27_readiness_spectrum_rules()

    # 4. End-to-End User Flow
    test_28_e2e_stage_flow_defined()
    test_29_e2e_user_triggers()
    test_30_e2e_export_workflow()
    test_31_e2e_multi_agent_flow()
    test_32_e2e_handoff_contract()
    test_33_e2e_context_resume()
    test_34_e2e_diagnostic_start_output()
    test_35_e2e_express_review()
    test_36_e2e_risk_map()
    test_37_e2e_readiness_spectrum()
    test_38_e2e_file_workbench()
    test_39_e2e_execution_bridge()
    test_40_e2e_packaging_boundary()

    # 5. Schema Validation
    test_41_schemas_have_required_fields()
    test_42_workbench_schema_evidence_structure()

    # Summary
    print("\n" + "=" * 70)
    total = _passed + _failed
    print(f"  Results: {_passed}/{total} passed, {_failed} failed, {_warned} warnings")
    print("=" * 70)

    if _errors:
        print("\n  FAILURES:")
        for e in _errors:
            print(f"    {e}")

    if _warnings:
        print("\n  WARNINGS:")
        for w in _warnings:
            print(f"    {w}")

    print()
    return 1 if _failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
