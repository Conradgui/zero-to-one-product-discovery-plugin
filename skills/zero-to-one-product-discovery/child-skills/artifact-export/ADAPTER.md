---
name: artifact-export
description: Use when the main workflow has accepted or review-ready planning artifacts and the user asks to export stable files, delivery artifacts, or a file workbench.
---

# Artifact Export

## Role

Export Z2O planning artifacts into a stable file structure that a host agent can write into the user's project workspace.

Artifact Export is a packaging producer, not a discovery producer. It must not create new product claims, rewrite strategy, or mark incomplete artifacts as ready.

## Required Input

- Project slug or project name.
- Current Runtime Workbench summary.
- Artifact status for PRD, Roadmap, User Stories, and Implementation Plan.
- Accepted or review-ready artifact bodies when available.
- Execution Bridge output when available.
- Evidence snapshot, risk map, readiness spectrum, audit queue, and next controller action.

## Default Output Directory

Use the caller's project workspace, not the installed skill directory:

```text
z2o-artifacts/<project-slug>/
```

Do not place exported artifacts inside the installable skill package. Do not include `z2o-artifacts/` in the skill zip.

## Stable File Structure

```text
z2o-artifacts/<project-slug>/
├── manifest.json
├── README.md
├── prd.md
├── roadmap.md
├── user-stories.md
├── implementation-plan.md
├── workbench/
│   ├── workbench.md
│   ├── workbench.json
│   ├── evidence-dashboard.md
│   ├── risk-map.md
│   └── readiness-spectrum.md
├── execution/
│   ├── github-issues.md
│   ├── github-issues.json
│   ├── github-issue-bodies/
│   │   └── 001-<task-slug>.md
│   └── host-execution-checklist.md
└── revisions/
    ├── revision-index.json
    ├── revision-log.md
    ├── records/
    │   └── rev-<timestamp>.json
    └── diffs/
        └── rev-<timestamp>/
            └── <artifact>.diff
```

## Missing Artifact Rule

Keep every fixed file path even when an artifact is missing or not ready.

For a missing or unready artifact, write only:

```markdown
# NOT_READY: <Artifact Name>

## Status
<not_started | in_progress | ready_for_review | accepted>

## Blocker
<why this file cannot contain final content>

## Required Input
- <single missing input or decision>

## Controller Decision
<downgrade | request_evidence | ask_user | block>
```

Do not fill placeholders with invented requirements, stories, tasks, or evidence.

## Quick Mode Draft Rule

If the source artifact is a Quick Mode draft and the user has not returned to Standard Exploration to validate it, keep the fixed file path but make the draft status impossible to miss.

The exported Markdown file must start with:

```markdown
# QUICK_MODE_DRAFT: <Artifact Name>

This artifact was produced in Quick Mode. Treat `[Fact]`, `[Assumption]`, and `[Unknown]` labels as binding until the Controller validates the draft in Standard Exploration.
```

The matching manifest entry must use:

- `source_status: quick_mode_draft`
- `content_mode: quick_mode_draft`
- `status_guard: quick_mode_banner_required`

Do not mark a Quick Mode draft as `accepted_artifact` unless a later Controller/user gate accepted it outside Quick Mode.

## File Workbench

Export the workbench as both Markdown and JSON:

- `workbench/workbench.md`: human-readable dashboard.
- `workbench/workbench.json`: machine-readable current-state snapshot.

Both files may include artifact path references and one-line summaries. They must not include full transcripts, full artifact bodies, complete Agent Work Orders, complete Agent Return Packets, complete Audit Reports, or long history.

Required dashboard sections:

1. Workflow state.
2. Next controller action.
3. Evidence maturity.
4. Risk map.
5. Readiness spectrum.
6. Artifact status.
7. Audit queue.
8. Blockers.
9. Skipped stages.

## Manifest

`manifest.json` must follow `evals/artifact-manifest.schema.json` and include:

- Package version.
- Project slug.
- Export timestamp.
- Export status.
- Controller decision.
- Evidence summary.
- Stable artifact paths.
- `source_status`, `content_mode`, and `status_guard` for every artifact entry.
- Workbench refs.
- Execution handoff refs.
- Revision refs when a revision ledger exists.
- Blockers and required inputs for not-ready files.

## Boundaries

- Do not create or modify GitHub Issues, Jira tickets, project boards, branches, pull requests, or external tasks.
- Do not write runtime state into the installable skill folder.
- Do not put `.z2o-state/`, `.z2o-patterns/`, `z2o-artifacts/`, or eval-run archives into the skill zip.
- Do not treat exported files as more authoritative than the Workbench and Controller decision that produced them.
- Do not bypass Audit Report or Controller acceptance requirements.
- Do not put revision history into Workbench. Revision ledger files stay under `revisions/` and remain bounded to hashes, diffs, section summaries, and Controller-provided metadata.
- Do not export content as accepted when artifact status and content readiness disagree. Use `NOT_READY` or `blocked_status_content_mismatch` instead.

## Readiness Signal

Return `ready_for_next_stage` when all requested export files can be generated with accurate ready/not-ready markers.

Return `needs_more_evidence` when the export needs one missing source artifact or evidence snapshot to avoid misleading output.

Return `needs_main_skill_decision` when the user must choose project slug, output workspace, or export subset.

Return `blocked` when exporting would imply finality for unreviewed or contradictory artifacts.

## Context Resume Packet

After export, include:

- Export root path.
- Files written or planned.
- Not-ready files and blockers.
- Evidence maturity summary.
- Execution handoff mode, if present.
- Recommended next controller action.
