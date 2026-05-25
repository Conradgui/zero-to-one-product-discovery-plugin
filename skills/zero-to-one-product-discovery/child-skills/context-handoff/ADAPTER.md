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
- Working assumptions.
- Unresolved questions.
- Decisions and trade-offs.
- Risks and constraints.
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
- Readiness Signal.
- Recommended Main Skill Action.

## Boundaries

- Do not add new product claims.
- Do not choose the next stage beyond the provided recommended action.
- Do not hide uncertainty.

