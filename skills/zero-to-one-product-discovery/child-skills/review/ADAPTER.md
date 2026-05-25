---
name: review
description: Use when the main workflow has an artifact, plan, diff, or release candidate that needs a focused quality review.
---

# Review

## Role

Review artifacts or implementation plans for correctness, stage fit, evidence quality, boundary control, and verification readiness.

## Required Input

- Review target.
- Intended stage and artifact mode.
- Source materials.
- Acceptance criteria or rubric.
- Known risks and constraints.
- Out-of-scope boundaries.

## Output Contract

- Findings first, ordered by severity.
- Evidence for each finding.
- Missing tests or validation gaps.
- Decision Log / ADR candidates.
- Readiness signal.
- Context Resume Packet.

## Boundaries

- Do not rewrite the artifact unless explicitly requested.
- Do not treat style preferences as blockers.
- Do not approve stage bypass.

