# Skill Evaluation Rubric Template

## Purpose

This template defines a repeatable scoring and evidence-value process for `zero-to-one-product-discovery`.

Use it after raw responses or JSONL traces have been captured. Do not patch the skill while scoring.

## Scoring Summary

| Level | Meaning |
|---:|---|
| 90-100 | Candidate for install/release only if there are zero hard failures and value review supports the claim |
| 85-89 | Baseline pass; patch or rerun if any high-risk weakness remains |
| 70-84 | Needs skill, scenario, or rubric revision |
| <70 | Fails; do not install or release |

Any hard failure makes the scenario fail even if the numeric score is high.

## Global Hard Failures

Check every scenario for these failures:

- `wrong_trigger_decision`: skill is used when it should not be, or not used when it should be.
- `asks_mature_product_question_upfront`: response asks for target user, MVP, tech stack, or business model before candidate interpretation.
- `produces_later_stage_artifacts`: response creates PRD, Roadmap, Milestones, ADRs, MVP scope, tech choices, scaffolding, or implementation plan too early.
- `asks_multiple_key_questions`: response asks more than one key question in the same turn.
- `generic_response`: response gives generic advice without grounding in the prompt or materials.
- `child_skill_stage_bypass`: a child skill produces or commits an artifact without main workflow prerequisites and readiness validation.
- `vendor_boundary_bypass`: response treats `vendor/` files as active routeable child skills or commands.
- `controller_overreach`: Controller accepts, finalizes, or changes an artifact without required gate, audit, or user decision.
- `producer_overreach`: Producer chooses next stage, calls another producer, resolves cross-artifact conflicts, or accepts its own output as final.
- `workbench_overload`: Runtime Workbench stores full transcripts, full artifacts, or long histories instead of current-state summaries.
- `missing_user_gate`: response skips required user confirmation for stage upgrade, final artifact acceptance, major conflict, or ADR decision.
- `no_actionable_findings_claimed_as_evidence`: evaluator claims a run is meaningful evidence even though it found no substantive issue, confidence change, release decision, or improvement direction.

Scenario-specific hard failures are defined in `evals.json`.

## Scorecard

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger / boundary correctness | 15 |  |  |
| Stage-gate control | 15 |  |  |
| Evidence grounding | 15 |  |  |
| Protocol / artifact integrity | 15 |  |  |
| User value and question quality | 10 |  |  |
| Context economy | 10 |  |  |
| Deterministic-check compliance | 10 |  |  |
| Recovery and next action | 10 |  |  |
| Total | 100 |  |  |

## Dimension Guide

### Trigger / Boundary Correctness

Scores whether the skill activates for true zero-to-one product discovery and stays inactive for mature-product changes, narrow implementation tasks, or skill-maintenance work.

### Stage-Gate Control

Scores whether the response prevents premature PRD, Roadmap, ADR, Implementation Plan, MVP scope, tech-stack choice, or coding before prerequisites are grounded.

### Evidence Grounding

Scores whether facts, assumptions, risks, unknowns, contradictions, and evidence gaps are separated and tied to the user's actual materials.

### Protocol / Artifact Integrity

Scores whether child-skill routing, multi-agent work orders, return packets, Audit Reports, Trace Reports, and Runtime Workbench boundaries are preserved.

### User Value And Question Quality

Scores whether the response asks one highest-leverage question when needed, or returns a clear readiness/blocker signal when a question is not appropriate.

### Context Economy

Scores whether the response avoids template dumping, full transcript storage, repeated summaries, excessive internal architecture exposition, and unnecessary reference loading.

### Deterministic-Check Compliance

Scores whether concrete checks from `evals.json` pass. These checks should be easy to inspect from raw response text, JSONL trace, or produced artifacts.

### Recovery And Next Action

Scores whether failures or blockers lead to a safe downgrade, user gate, audit request, patch recommendation, or rerun plan rather than silent continuation.

## Evidence Value Review

After scoring the suite, judge whether the run is worth preserving.

### Valuable Run

A run is valuable when it does at least one of the following:

- Finds a substantive issue or regression.
- Confirms a previously unverified high-risk release gate.
- Produces a concrete improvement direction for skill instructions, references, child adapters, eval scenarios, packaging, or release criteria.
- Adds a realistic failure case that should become a regression scenario.

### Not Valuable As Evidence

A run is not valuable when it only:

- Says the suite passed without changing a decision.
- Repeats expected behavior.
- Gives generic praise or generic concerns.
- Produces no actionable patch, rerun, scenario, or release decision.

Such runs can be discarded or retained as a minimal note only when they close a named release question.

## Scenario Result Template

```markdown
## Scenario: scenario_id

### Prompt

Paste the scenario prompt.

### Expected Mode

Paste `expected_mode`.

### Actual Response Or Trace

Paste or link to raw response / JSONL trace.

### Hard Failure Check

- [ ] wrong_trigger_decision
- [ ] asks_mature_product_question_upfront
- [ ] produces_later_stage_artifacts
- [ ] asks_multiple_key_questions
- [ ] generic_response
- [ ] child_skill_stage_bypass
- [ ] vendor_boundary_bypass
- [ ] controller_overreach
- [ ] producer_overreach
- [ ] workbench_overload
- [ ] missing_user_gate
- [ ] no_actionable_findings_claimed_as_evidence
- [ ] scenario-specific hard failure

### Deterministic Checks

| Check ID | Pass | Evidence |
|---|---|---|

### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger / boundary correctness | 15 |  |  |
| Stage-gate control | 15 |  |  |
| Evidence grounding | 15 |  |  |
| Protocol / artifact integrity | 15 |  |  |
| User value and question quality | 10 |  |  |
| Context economy | 10 |  |  |
| Deterministic-check compliance | 10 |  |  |
| Recovery and next action | 10 |  |  |
| Total | 100 |  |  |

### Verdict

Pass / Fail.

### Patch Needed

Describe exact changes needed in `SKILL.md`, `references/`, `child-skills/`, `evals/`, packaging, or release criteria.
```

## Suite Report Template

```markdown
# Evaluation Run: YYYY-MM-DD-run-XX

## Environment

- Agent:
- Model:
- Skill version:
- Evaluation file:
- Git status:

## Summary

| Scenario | Category | Risk | Score | Hard Failure | Verdict |
|---|---|---|---:|---|---|

## Aggregate

- Average score:
- Median score:
- Lowest score:
- Hard failure count:
- Suite pass:
- Install candidate:

## Findings

### Substantive Issues

### Improvement Directions

### Regression Risks

### Required Patches

### Required Reruns
```

## Value Review Template

```markdown
# Value Review: YYYY-MM-DD-run-XX

## Value Verdict

valuable / not-valuable

## Substantive Findings

## Improvement Directions

## Product Impact

## Promotion Decision

promote / minimal-note / discard-full-run

## Required Next Action

patch / rerun / no-action

## Rationale
```
