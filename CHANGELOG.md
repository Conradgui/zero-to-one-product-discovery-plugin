# Changelog

All notable changes to this plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-06-10

Synced bundled skill to source project `v0.4.0-rc.4` (Control Surface Hardening RC).

### Added

- **Execution Bridge** child-skill: converts review-ready Implementation Plans into host-executable dry-run handoffs (GitHub Issues, Claude Code tasks, Jira tickets).
- **Artifact Export** child-skill: exports stable PRD/Roadmap/User Stories/Implementation Plan/Workbench/Execution Handoff files to `z2o-artifacts/<project-slug>/`.
- **Revision Trace** child-skill: generates bounded revision ledger with hashes, diffs, and Controller metadata for exported artifacts.
- Quick Mode: independent mode switch for producing evidence-labeled drafts without interactive exploration loops.
- Evidence Maturity Dashboard: real-time evidence verification progress with four-level labels.
- File Workbench: current-state dashboard for workflow state, evidence, risks, and readiness.
- Risk Map: assumptions sorted by risk_weighted_priority with validation order recommendations.
- Readiness Spectrum: continuous readiness score (0.0-1.0) with gap analysis and fastest validation path.
- Pattern Library: cross-project discovery pattern extraction and matching.
- Auto-Persist: automatic Runtime Workbench state persistence to `.z2o-state/workbench.json`.
- Express Review: fast-track path for Material Assimilation with batch acceptance.
- Controller action registry (`evals/controller-actions.json`).
- 10 JSON Schema contracts: Agent Work Order, Agent Return Packet, Audit Report, Runtime Workbench, Pattern Index, Artifact Manifest, Execution Handoff, Revision Index, Revision Record, Controller Actions.
- Python scripts: `persist_workbench.py`, `generate_revision_trace.py`, `validate-contracts.py`.
- Plugin assets: `icon.png`, `logo.png`.
- CHANGELOG.md.

### Changed

- Updated `SKILL.md` with all P0/P1/P2 features and Core Rules from source project.
- Updated all `references/` files to match source project.
- Updated all `child-skills/ADAPTER.md` files to match source project.
- Updated `agents/README.md` with Execution Bridge, Artifact Export, and Revision Trace producers.
- Updated `plugin.json` to version 0.4.0 with full interface metadata.
- Updated `README.md` with spec-compliant Install, Configure, Use, Security, and Troubleshooting sections.

### Fixed

- `validate-plugin-package.py`: removed hardcoded version string, added comprehensive field validation.

## [0.2.1] - 2026-06-05

### Changed

- Multi-agent documentation structure patch.
- Synced bundled skill to source project `v0.2.1`.

## [0.2.0] - 2026-06-01

### Added

- Initial Codex plugin distribution wrapper.
- Plugin manifest (`.codex-plugin/plugin.json`).
- Bundled `zero-to-one-product-discovery` skill.
- Package validation script.
- MIT License.
