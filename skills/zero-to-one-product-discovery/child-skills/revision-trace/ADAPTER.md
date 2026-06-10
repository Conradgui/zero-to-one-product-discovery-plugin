---
name: revision-trace
description: Use when stable Z2O artifacts have been exported and the user asks for artifact diff, revision trace, revision ledger, or product change history.
---

# Revision Trace

## Role

Create a bounded artifact revision ledger for exported Z2O artifacts.

Revision Trace is observability for exported artifacts. It is not a discovery producer, not a Workbench replacement, and not a full history database.

## Required Input

- Current export root: `z2o-artifacts/<project-slug>/`.
- Previous export root, or explicit baseline revision decision.
- Controller metadata: controller decision, change reason, source stage, evidence refs, decision refs, and audit refs.
- Artifact status for PRD, Roadmap, User Stories, and Implementation Plan.

## Stable Artifact Files

Compare only these stable files:

```text
prd.md
roadmap.md
user-stories.md
implementation-plan.md
```

Do not create `prd-v1.md`, `prd-v2.md`, `final-final.md`, or any other replacement for stable artifact paths.

## Output Directory

Write revision material under the caller's export root:

```text
z2o-artifacts/<project-slug>/revisions/
├── revision-index.json
├── revision-log.md
├── records/
│   └── rev-<timestamp>.json
└── diffs/
    └── rev-<timestamp>/
        ├── prd.diff
        ├── roadmap.diff
        ├── user-stories.diff
        └── implementation-plan.diff
```

## What To Record

- Current artifact hashes.
- Changed artifact list.
- Mechanical section-level summary from Markdown headings.
- Per-artifact unified diff when a previous export root exists.
- Controller decision.
- Change reason supplied by Controller metadata.
- Evidence refs, decision refs, and audit refs supplied by Controller metadata.

If metadata is missing, set `change_reason_status` to `missing`. Do not infer product rationale from the diff.

## Boundaries

- Do not store full transcripts, raw prompt history, hidden reasoning, full Agent Work Orders, full Agent Return Packets, full Audit Reports, or long discussion history.
- Do not put revision data into Runtime Workbench. Workbench stays current-state only.
- Do not use revision count as evidence maturity, readiness, or artifact quality.
- Do not let Producer metadata mark a revision accepted. Acceptance must come from Controller decision.
- Do not treat diff output as source of truth. Workbench, manifest, artifact status, Controller decision, and evidence refs remain authoritative.
- Do not place `z2o-artifacts/`, `.z2o-state/`, `.z2o-patterns/`, or eval-run archives into the installable skill zip.

## Script

Use `scripts/generate_revision_trace.py` when the host agent can write files:

```bash
python3 zero-to-one-product-discovery/scripts/generate_revision_trace.py \
  --export-root z2o-artifacts/<project-slug> \
  --previous-root <previous-export-root> \
  --metadata <revision-metadata.json>
```

The script uses only Python standard library and generates mechanical hashes, diffs, section summaries, `revision-index.json`, a revision record, and `revision-log.md`.

## Readiness Signal

Return `ready_for_next_stage` when the revision ledger can be generated without violating Workbench or history boundaries.

Return `needs_more_evidence` when metadata is missing and the user expects semantic rationale.

Return `needs_main_skill_decision` when the user must choose previous export root or baseline revision.

Return `blocked` when the request requires full transcript storage, hidden reasoning, or replacing stable artifact paths with versioned artifact files.

## Context Resume Packet

After creating or planning a revision trace, include:

- Export root.
- Revision ID.
- Changed artifacts.
- Missing metadata, if any.
- Evidence refs / decision refs / audit refs included.
- Recommended next controller action.
