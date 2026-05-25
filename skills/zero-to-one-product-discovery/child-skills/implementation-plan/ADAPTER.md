---
name: implementation-plan
description: Use when product direction, planning artifacts, and design direction are confirmed and the main workflow needs decision-complete implementation tasks.
---

# Implementation Plan

## Role

Produce an implementation plan or implementation readiness review from confirmed planning artifacts.

## Required Input

- Confirmed PRD / roadmap / story context.
- Design direction if relevant.
- Technical constraints and known stack.
- Acceptance criteria.
- Verification expectations.
- Non-goals and boundaries.
- Expected output mode.

## Output Contract

- Ordered implementation tasks.
- Acceptance checks per task.
- Verification commands or scenarios.
- Risks, dependencies, and rollback notes when relevant.
- The highest-leverage blocking question for the current turn if planning artifacts are not ready.
- Decision Log / ADR candidates.
- Readiness signal.
- Context Resume Packet.

## Producer Agent Contract

When routed as the Implementation Plan Producer, accept an Agent Work Order and return an Agent Return Packet before tasks are treated as decision-complete.

### Workbench Updates

- Update Artifact Status with implementation plan mode: readiness review, decision-complete plan draft, blocked, or ready for engineering planning handoff.
- Update Dependency Board with missing PRD, roadmap, acceptance criteria, technical decision, file/module boundary, or verification command.
- Update Risk Board with implementation risks that affect sequencing, rollback, test strategy, or maintainer burden.
- Update Conflict Board when engineering tasks contradict product scope, non-goals, ADRs, or verification expectations.

### Self-check

- Are product direction, planning artifacts, acceptance criteria, and technical constraints review-ready?
- Does each task have acceptance checks and verification expectations?
- Did the output avoid choosing a new stack, architecture, or product scope?

## Boundaries

- Do not plan implementation from unreviewed product artifacts.
- Do not introduce a stack or architecture unless already chosen.
- Do not skip verification planning.
- Do not use implementation tasks to reopen product strategy unless a blocker or contradiction requires controller review.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
