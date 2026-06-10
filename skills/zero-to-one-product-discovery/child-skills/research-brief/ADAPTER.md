---
name: research-brief
description: Use when the main zero-to-one workflow has evidence, notes, interviews, feedback, or market material that need synthesis before artifact generation.
---

# Research Brief

## Role

Synthesize supplied evidence into a bounded research brief. Separate evidence from assumptions before any PRD, roadmap, story, or implementation artifact is upgraded.

## Required Input

- Current stage.
- Confirmed facts.
- Working assumptions.
- Existing materials inspected.
- Unresolved questions.
- Risks and contradictions.
- Out-of-scope boundaries.
- Expected output mode.

## Output Contract

- Evidence inventory.
- Assumptions / unknowns / contradictions / gaps.
- Problem, job, or scenario hypotheses labeled by evidence status.
- Evidence Maturity Summary: total items, facts count, assumptions count, unknowns count, risks count, validated count, maturity level, maturity percentage.
- The highest-leverage blocking question for the current turn if evidence is insufficient.
- Decision Log candidates.
- ADR candidates only when research exposes durable technical decisions.
- Readiness signal.
- Context Resume Packet.

## Producer Agent Contract

When routed as the Research Producer, accept an Agent Work Order and return an Agent Return Packet before any downstream artifact is upgraded.

### Workbench Updates

- Update Evidence Snapshot items with structured evidence: each item gets id, content, type, validation_status, validation_plan, and source.
- Update Evidence Snapshot summary: recalculate total, facts, assumptions, unknowns, risks, validated, maturity_percentage, and maturity_level.
- Update Dependency Board with the one evidence gap that most affects the next workflow decision.
- Update Risk Board only when the evidence exposes product, market, feasibility, or credibility risk.

### Self-check

- Did every synthesized claim point to supplied material or an explicit assumption?
- Did feedback stay as evidence instead of becoming a requirement?
- Did the output avoid selecting MVP, roadmap, or implementation scope?

## Boundaries

- Do not turn feedback directly into requirements.
- Do not declare a target user, MVP, or roadmap as final.
- Do not resolve PRD, Roadmap, ADR, or Implementation Plan routes.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
