---
name: context-handoff
description: Use when the main workflow needs to preserve or transfer product-discovery context across stages, sessions, tools, or child-skill handoffs.
---

# Context Handoff

## Role

Create a compact Context Resume Packet that lets the main workflow or another tool resume without losing stage, evidence, and boundary context.

## Required Input

- Current stage.
- Confirmed facts.
- Working assumptions with validation plans (if any).
- Unresolved questions.
- Decisions and trade-offs.
- Risks and constraints.
- Active validation plans.
- Active artifact routes.
- Next recommended main workflow action.

## Output Contract

- Current Stage.
- Artifact / Capability Routed.
- Confirmed Facts.
- Working Assumptions.
- Unresolved Questions.
- Decision Log Candidates.
- ADR Candidates.
- Key Risks.
- Assumption Validation Bindings: for each assumption with a validation plan (experiment, success criteria, timeline, status).
- Evidence Maturity Summary: total items, facts count, assumptions count, unknowns count, risks count, validated count, maturity level, maturity percentage.
- Readiness Signal.
- Recommended Main Skill Action.

## Boundaries

- Do not add new product claims.
- Do not choose the next stage beyond the provided recommended action.
- Do not hide uncertainty.

