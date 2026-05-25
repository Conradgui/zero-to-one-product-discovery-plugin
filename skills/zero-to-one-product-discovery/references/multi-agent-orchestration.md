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

## Agent Work Order

The controller uses a strict work order before routing to a producer.

```markdown
# Agent Work Order

## Role
Research / PRD / Roadmap / ADR / Implementation Plan

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
Accept, downgrade, request evidence, route to audit, ask the user one question, or stop.
```

Full artifacts may exist outside the workbench, but the controller should read the return packet first.

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

Do not expose the auditor's full chain of thought. The report is a decision surface, not an internal transcript.

## Execution Order

Default producer flow:

1. Research, when materials or evidence need synthesis.
2. PRD, after problem, solution direction, feasibility context, MVP hypothesis, risks, non-goals, and success/failure indicators are grounded enough for the requested output mode.
3. Roadmap, after PRD or PRD outline is accepted enough to sequence validation or delivery.
4. ADR, only when a durable architecture, platform, data, security, deployment, dependency, or maintainability decision is present.
5. Implementation Plan, only after planning artifacts and relevant technical decisions are review-ready.

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

