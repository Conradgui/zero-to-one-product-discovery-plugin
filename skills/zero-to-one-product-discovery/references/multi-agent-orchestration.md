# Multi-Agent Orchestration Protocol

## Purpose

This reference defines the lightweight multi-agent operating model for `zero-to-one-product-discovery`.

The goal is better artifact quality and safer workflow control, not richer internal chatter. Use this protocol only when the main workflow routes to specialist artifact production, review, or implementation planning.

## Architecture

Use five roles:

| Role | Responsibility | Must Not |
|---|---|---|
| Workflow Rules | Define stages, gates, downgrade rules, and allowed outputs | Act like an agent or store runtime state |
| Controller Agent | Applies workflow rules, creates work orders, updates the runtime workbench, and decides next action | Produce unreviewed final artifacts or hide child-agent blockers |
| Producer Agents | Produce one bounded artifact or readiness review: Research, PRD, Roadmap, ADR, or Implementation Plan | Choose the next stage, call another producer, or resolve cross-artifact conflicts |
| Auditor Agent | Reviews producer output and controller decisions against gates, evidence, and consistency | Rewrite the artifact as the producer or make product decisions for the user |
| Runtime Workbench | Holds the current decision state shared by controller, producers, and auditor | Store full transcripts, long histories, or full artifacts |

The main workflow remains the user's single coherent interface. Agent roles may be real subagents or simulated specialist passes, depending on the host platform. Do not require Codex-, Claude-, or platform-specific subagent APIs.

## Strict Contract Layer

The Markdown templates in this file are the human-readable protocol. The strict validation layer lives in `evals/`:

| Contract | Schema |
|---|---|
| Agent Work Order | `evals/agent-work-order.schema.json` |
| Agent Return Packet | `evals/agent-return-packet.schema.json` |
| Audit Report | `evals/audit-report.schema.json` |
| Runtime Workbench | `evals/workbench.schema.json` |
| Pattern Index | `evals/pattern-index.schema.json` |
| Artifact Manifest | `evals/artifact-manifest.schema.json` |
| Execution Handoff | `evals/execution-handoff.schema.json` |
| Revision Index | `evals/revision-index.schema.json` |
| Revision Record | `evals/revision-record.schema.json` |
| Controller Actions | `evals/controller-actions.json` |

Strict mode is advisory for ordinary chat and required for eval fixtures, release checks, and any future executable runtime adapter. If Markdown and JSON disagree, the Controller must follow the stage gates and the schema-compatible interpretation.

Hard boundaries:

- Controller remains the only routing authority.
- Producers never hand off to other Producers and never accept their own output.
- Auditor reviews, blocks, or recommends revision; it does not rewrite the artifact as the Producer.
- Runtime Workbench stores current decision state only. Agent Work Orders, Return Packets, Audit Reports, full artifacts, and transcripts stay outside persisted workbench state.
- No external runtime framework is required. LangGraph, OpenAI Agents SDK, AutoGen, or A2A may be future adapters, not dependencies.

## Controller State Machine

The Controller reduces Producer and Auditor outputs to a small set of actions. These actions make the stage gate enforceable without changing the eight-stage workflow.

Controller action names are defined by `evals/controller-actions.json`. Schemas and scripts must read or validate against that registry rather than maintaining independent action enums.

| Input Signal | Preconditions | Allowed Controller Action | Must Not |
|---|---|---|---|
| `ready_for_review` | Output stayed inside work order boundaries | `route_to_audit` or controller-documented review | Accept final artifact without review when substantial |
| `ready_for_next_stage` | Audit passed or controller review found no blockers; user gate satisfied when required | `accept` then move to the next allowed stage | Let Producer choose the next stage |
| `needs_more_evidence` | Missing evidence is specific and decision-relevant | `request_evidence` or `ask_user` one question | Fill the gap with assumptions |
| `needs_main_skill_decision` | Trade-off, conflict, scope, or ADR qualification needs owner decision | `ask_user`, `downgrade`, `reroute`, or `escalate_to_adr` | Let Producer or Auditor decide for the user |
| `blocked` | Artifact would mislead, violate stage purity, or require invented facts | `block`, `downgrade`, or return to earlier stage | Hide blocker or continue artifact cascade |
| Audit `pass` | Boundary, evidence, and consistency checks pass | `accept` or continue through the next user gate | Skip required user acceptance |
| Audit `needs_revision` | Fixable blocker or non-blocking issue exists | `downgrade`, `request_evidence`, or reroute to same Producer | Auditor rewrites as Producer |
| Audit `blocked` | Output cannot be safely revised inside current stage | `block`, return to earlier stage, or stop | Repackage blocked output as final |

Stage transitions remain serial unless the task is a review-only pass over the same accepted workbench state:

| From | To | Required Controller Evidence |
|---|---|---|
| Diagnostic Start | Material Assimilation | User provides materials or identifies existing evidence |
| Diagnostic Start / Material Assimilation | Problem Framing | Facts, assumptions, risks, and unknowns are separated enough for one problem question |
| Problem Framing | Solution Exploration | Problem framing is accepted or conflict-free enough to compare solution directions |
| Solution Exploration | Feasibility Discovery | A candidate solution direction exists and feasibility risks are named |
| Feasibility Discovery | MVP Hypothesis | Feasibility blockers are named and MVP scope can be assumption-labeled |
| MVP Hypothesis | Planning Artifacts | Grounding Contract inputs are present or output is explicitly downgraded |
| Planning Artifacts | Implementation Planning | Planning artifacts are review-ready and technical decision gaps are named |
| Implementation Planning | Execution Bridge | Implementation Plan is review-ready and target format is requested |
| Planning Artifacts / Implementation Planning | Artifact Export | User requests stable files, delivery package, or File Workbench export |
| After Artifact Export | Revision Trace | Stable artifacts exist and user requests artifact diff or revision ledger |

## Runtime Workbench

The workbench serves current decisions only. It is not a meeting log.

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

## Evidence Maturity Summary
Total Items:
Verified Facts:
Maturity Level: Insufficient / Partial / Sufficient / Strong
Maturity Percentage:
Assumptions With Validation Plan:
Assumptions Validated This Session:

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

## Risk Board
Risk:
Severity:
Mitigation / Next Check:

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

### Workbench Limits

- Keep only concise, current-state summaries.
- Do not paste complete artifacts into the workbench.
- Do not record full agent-to-agent conversation.
- Do not use the workbench as a historical trace.
- If a retrospective is needed, generate a separate Trace Report after the stage or evaluation run.

### Workbench Persistence

Save the workbench state to `.z2o-state/workbench.json` on every stage transition, substantial artifact acceptance or downgrade, or explicit user save request. This ensures that long-running discovery workflows survive session interruptions.

The persisted state includes: workflow state (current stage, goal, output mode, depth mode), evidence snapshot (structured items with type, validation_status, validation_plan, source, plus summary counters for maturity tracking), artifact status (not_started / in_progress / ready_for_review / accepted), decision log, and skipped stages.

Do not persist full artifact text, conversation transcripts, Agent Work Orders, Agent Return Packets, or Audit Reports. The workbench is a decision board, not an archive.

On new session start, check for `.z2o-state/workbench.json`. If it exists and is less than 7 days old, offer the user a choice to resume or start fresh. If older than 7 days, default to starting fresh.

For detailed JSON schema and resume protocol, see `workflow.md` section "State Persistence".

## Agent Work Order

The controller uses a strict work order before routing to a producer.

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

## Return Format
Use Agent Return Packet.
```

## Agent Return Packet

Producer agents return concise decision material. They do not return full internal reasoning.

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
Accept, downgrade, request evidence, route to audit, ask the user one question, block, reroute, escalate to ADR, or stop.
```

Full artifacts may exist outside the workbench, but the controller should read the return packet first. Producer output cannot be accepted as final until the Controller checks the return packet against the current stage, work order, and audit requirement.

## Audit Report

The auditor produces a short report for the controller and, when useful, the user.

```markdown
# Audit Report

## Verdict
Pass / Needs Revision / Blocked

## Reviewed Item
Artifact, route, or controller decision reviewed.

## Blocking Issues
Issues that must be resolved before proceeding.

## Non-blocking Issues
Quality improvements that do not block the next step.

## Boundary Check
Stage purity, child-agent authority, and final-artifact gate check.

## Evidence Check
Fact / assumption / unknown / risk separation and evidence sufficiency.

## Consistency Check
Conflicts with other artifacts, decisions, constraints, or user goals.

## Recommended Next Action
Proceed, downgrade, ask for evidence, reroute, escalate to ADR, or stop.
```

Do not expose the auditor's full chain of thought. The report is a decision surface, not an internal transcript. The auditor must not rewrite the reviewed artifact as a producer; it may only identify issues and recommend the next Controller action.

## Execution Order

Default producer flow:

1. Research, when materials or evidence need synthesis.
2. PRD, after problem, solution direction, feasibility context, MVP hypothesis, risks, non-goals, and success/failure indicators are grounded enough for the requested output mode.
3. Roadmap, after PRD or PRD outline is accepted enough to sequence validation or delivery.
4. ADR, only when a durable architecture, platform, data, security, deployment, dependency, or maintainability decision is present.
5. Implementation Plan, only after planning artifacts and relevant technical decisions are review-ready.
6. Execution Bridge, only after a review-ready Implementation Plan exists and the user requests GitHub Issues, Claude Code tasks, Jira tickets, or a similar execution handoff.
7. Artifact Export, only when the user requests stable files, a delivery package, or File Workbench export. Export must mark unready artifacts as `NOT_READY` instead of inventing content.
8. Revision Trace, only after stable artifacts have been exported and the user requests artifact diff or revision ledger. It must stay outside Workbench and must not store full transcripts, hidden reasoning, full agent packets, or full audit reports.

Use stage-serial production and local parallel review. Producers should not race ahead from assumptions; auditors or consistency checks may run in parallel when they review the same accepted workbench state.

## User Gates

Ask the user only at meaningful gates:

- Stage upgrade to a later workflow phase.
- Acceptance of a final or review-ready planning artifact.
- Major conflict between artifacts or constraints.
- ADR-qualifying durable decision.
- Any missing information that blocks safe progress.

The one-question rule remains per turn, not per project. Continue the question loop until enough information exists to proceed safely.

## Trace Reports

Trace Reports are optional retrospective artifacts. Generate them only when the user asks for review, resume, portfolio material, or when an evaluation run needs evidence.

A Trace Report may summarize:

- Important controller decisions.
- Producer outputs and downgrades.
- Audit verdicts.
- User gates and decisions.
- Rejected approaches and why they were rejected.

Trace Reports must not be read as runtime state and must not replace the Runtime Workbench.
