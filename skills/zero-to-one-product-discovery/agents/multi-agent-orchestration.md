# Compact Multi-Agent Orchestration

This compact protocol is intended for quick loading from `agents/`. The full protocol lives in `../references/multi-agent-orchestration.md`.

## Strict Contracts

Markdown packets are the readable protocol. JSON Schemas in `../evals/` are the strict validation layer for release checks and future runtime adapters:

- `agent-work-order.schema.json`
- `agent-return-packet.schema.json`
- `audit-report.schema.json`
- `workbench.schema.json`
- `pattern-index.schema.json`
- `controller-actions.json`

The Controller remains the only routing authority. Producers do not hand off to other Producers or accept their own output. The Auditor does not rewrite artifacts as a Producer.

## Controller Actions

Controller action names are defined in `../evals/controller-actions.json`. Do not keep a separate action enum in compact docs, schemas, or scripts.

`ready_for_review` routes to audit or controller-documented review. `ready_for_next_stage` may proceed only after audit/review and required user gates. `needs_more_evidence`, `needs_main_skill_decision`, and `blocked` cannot be converted into final artifacts.

## Agent Work Order

The Controller must send a strict work order before routing to any Producer.

```markdown
# Agent Work Order

## Role
Research / PRD / Roadmap / ADR / Implementation Plan / Execution Bridge / Artifact Export / Revision Trace / Review

## Mission
This turn's single bounded job.

## Current Workflow State
Current Stage:
Current Goal:
Allowed Output Mode:
Do Not Cross:

## Input Context
Confirmed Facts:
Working Assumptions:
Unknowns:
Risks:
Relevant Decisions:

## Boundaries
Must Not:
Out Of Scope:
Do Not Decide:

## Required Output
Artifact Type:
Required Sections:
Evidence Labels Required:
Self-check Required:

## Stop Conditions
Return `needs_more_evidence` if:
Return `needs_main_skill_decision` if:
Return `blocked` if:
```

## Agent Return Packet

Producers return concise decision material, not internal reasoning.

```markdown
# Agent Return Packet

## Status
ready_for_review / ready_for_next_stage / needs_more_evidence / needs_main_skill_decision / blocked

## Output Summary
Concise artifact or readiness summary.

## Evidence Changes
New or changed facts, assumptions, unknowns, or risks.

## Blockers
Current blockers, if any.

## Conflicts
Conflicts with existing artifacts, assumptions, constraints, or decisions.

## Self-check
Producer's own boundary, evidence, and completeness check.

## Recommended Controller Action
One action from `../evals/controller-actions.json`.
```

## Runtime Workbench

Use Runtime Workbench only for concise current-state coordination.

```markdown
# Runtime Workbench

## Workflow State
Current Stage:
Current Goal:
Allowed Output Mode:
Do Not Cross:

## Evidence Snapshot
Confirmed Facts:
Working Assumptions:
Unknowns:
Risks:

## Artifact Status
Research:
PRD:
Roadmap:
ADR:
Implementation Plan:

## Dependency Board
Open Dependencies:
Owner:
Blocking Level:

## Conflict Board
Conflict:
Affected Artifacts:
Controller Resolution Needed:

## Audit Queue
Artifact:
Audit Type:
Status:
Required Before:

## Next Controller Action
Action:
Reason:
Expected Output:
```

Workbench must not contain full transcript, full history, complete artifacts, or long retrospective logs.

## Audit Report

Auditor output is a concise decision surface.

```markdown
# Audit Report

## Verdict
Pass / Needs Revision / Blocked

## Reviewed Item
Artifact, route, or controller decision reviewed.

## Blocking Issues
Issues that must be resolved before proceeding.

## Boundary Check
Stage purity, child-agent authority, and final-artifact gate check.

## Evidence Check
Fact / assumption / unknown / risk separation and evidence sufficiency.

## Consistency Check
Conflicts with other artifacts, decisions, constraints, or user goals.

## Recommended Next Action
Proceed, downgrade, ask for evidence, reroute, escalate to ADR, or stop.
```

Do not expose auditor chain-of-thought. Do not let the auditor rewrite producer artifacts as if it were the producer.
