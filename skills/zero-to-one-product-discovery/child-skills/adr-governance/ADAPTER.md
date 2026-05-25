---
name: adr-governance
description: Use when the main workflow has a durable technical, platform, architecture, data, security, deployment, or maintainability decision to record or review.
---

# ADR Governance

## Role

Decide whether a technical decision belongs in the Decision Log or should be upgraded into an ADR, then produce the appropriate artifact mode.

## Required Input

- Decision context.
- Options considered.
- Known constraints.
- Product and implementation implications.
- Reversibility and longevity.
- Existing Decision Log / ADR context.
- Expected output mode.

## Output Contract

- Decision Log entry, ADR outline, ADR artifact, or ADR readiness review.
- Consequences and trade-offs.
- Assumptions and unknowns.
- Escalation / downgrade rationale.
- The highest-leverage blocking question for the current turn if decision context is missing.
- Readiness signal.
- Context Resume Packet.

## Producer Agent Contract

When routed as the ADR Producer, accept an Agent Work Order and return an Agent Return Packet before any decision is recorded as accepted.

### Workbench Updates

- Update Artifact Status with ADR mode: not qualified, Decision Log candidate, ADR decision surface, ADR draft, accepted ADR candidate, or blocked.
- Update Dependency Board with missing options, drivers, validation method, rollback condition, or consequence analysis.
- Update Conflict Board when a proposed technical decision conflicts with PRD scope, Roadmap sequencing, privacy constraints, deployment assumptions, or maintainability goals.

### Self-check

- Does the decision qualify as architecture, platform, data, security, deployment, dependency, or long-term maintainability?
- Are ordinary product scope choices downgraded to Decision Log?
- Are options, drivers, consequences, validation method, and rollback/supersession concerns explicit enough for the requested output mode?

## Boundaries

- Do not turn ordinary product scope choices into ADRs.
- Do not accept an ADR without grounded technical decision context.
- Do not choose architecture on behalf of the main workflow.
- Do not mark an ADR as accepted without controller or user gate approval.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
