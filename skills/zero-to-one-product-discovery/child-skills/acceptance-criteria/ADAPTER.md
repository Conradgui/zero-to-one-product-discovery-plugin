---
name: acceptance-criteria
description: Use when the main workflow has a specific story or requirement that needs testable acceptance criteria.
---

# Acceptance Criteria

## Role

Turn a confirmed story or requirement into testable acceptance criteria without inventing new requirements.

## Required Input

- Story or requirement.
- Expected user-visible behavior.
- Known constraints and non-goals.
- Failure and boundary conditions if known.
- Expected output mode.

## Output Contract

- Success criteria.
- Failure and boundary criteria.
- Verification notes.
- Assumptions and unknowns.
- The highest-leverage blocking question for the current turn if behavior is unclear.
- Readiness signal.
- Context Resume Packet.

## Boundaries

- Do not add implementation details unless the implementation is already chosen.
- Do not broaden product scope.
- Do not infer unstated requirements as facts.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
