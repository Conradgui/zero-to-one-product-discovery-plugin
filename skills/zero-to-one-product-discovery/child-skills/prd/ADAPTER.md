---
name: prd
description: Use when the main zero-to-one workflow has a grounded problem, solution direction, feasibility context, and MVP hypothesis that need a PRD artifact.
---

# PRD

## Role

Produce a PRD artifact, PRD outline, or PRD readiness review from the main workflow's handoff packet.

## Required Input

- Current stage and requested output mode.
- Confirmed problem definition.
- User / scenario / job hypothesis.
- Solution direction.
- MVP hypothesis.
- Success and failure indicators.
- Constraints, non-goals, and risks.
- Existing materials inspected.

## Output Contract

- PRD body or outline.
- Evidence status for major claims.
- Requirements separated from assumptions.
- Non-goals and scope boundaries.
- The highest-leverage blocking question for the current turn if prerequisites are missing.
- Decision Log candidates.
- ADR candidates only for durable technical decisions.
- Readiness signal.
- Context Resume Packet.

## Producer Agent Contract

When routed as the PRD Producer, accept an Agent Work Order and return an Agent Return Packet before the controller accepts the PRD as final or review-ready.

### Workbench Updates

- Update Artifact Status with PRD mode: final candidate, review-ready draft, outline, readiness review, or blocked.
- Update Dependency Board with missing inputs such as success indicators, non-goals, constraints, or unresolved user/scenario assumptions.
- Update Conflict Board when requirements conflict with known risks, non-goals, roadmap assumptions, or ADR constraints.

### Self-check

- Is each requirement labeled as confirmed, assumption, unknown, or out of scope?
- Are success and failure indicators grounded enough for the requested output mode?
- Did the output avoid backlog, engineering tasks, and next-stage route decisions?

## Boundaries

- Do not create a final PRD from ungrounded assumptions.
- Do not generate implementation tasks or a full backlog.
- Do not choose the next stage.
- Do not accept your own PRD as final; recommend audit or controller acceptance.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
