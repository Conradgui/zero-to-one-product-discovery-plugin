---
name: roadmap
description: Use when a confirmed PRD or PRD outline needs validation sequencing, release phases, or Now/Next/Later planning.
---

# Roadmap

## Role

Create a roadmap decision surface or roadmap artifact that connects sequencing to outcomes, validation signals, dependencies, and risks.

## Required Input

- Confirmed PRD or PRD outline.
- MVP slice and scope boundary.
- Known dependencies.
- Constraints and non-goals.
- Evidence confidence by phase.
- Expected output mode.

## Output Contract

- Now / Next / Later or phase-gate roadmap.
- Goal, validation signal, dependency, risk, and non-goal for each phase.
- Assumptions and unknowns.
- The highest-leverage blocking question for the current turn if sequencing is premature.
- Decision Log candidates.
- Readiness signal.
- Context Resume Packet.

## Producer Agent Contract

When routed as the Roadmap Producer, accept an Agent Work Order and return an Agent Return Packet before the controller treats sequencing as committed.

### Workbench Updates

- Update Artifact Status with roadmap mode: decision surface, phase-gate draft, review-ready roadmap, or blocked.
- Update Dependency Board with unconfirmed PRD scope, validation gates, or sequencing prerequisites.
- Update Conflict Board when roadmap phases conflict with MVP boundaries, non-goals, feasibility risks, or ADR constraints.

### Self-check

- Does each phase connect to a goal, validation signal, dependency, risk, and non-goal?
- Are dates absent unless supplied or explicitly requested?
- Did the output avoid turning speculative future ideas into committed backlog?

## Boundaries

- Do not convert speculative ideas into commitments.
- Do not add dates unless dates were supplied or explicitly requested.
- Do not create engineering tasks before Implementation Planning.
- Do not resolve PRD or ADR conflicts without controller decision.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
