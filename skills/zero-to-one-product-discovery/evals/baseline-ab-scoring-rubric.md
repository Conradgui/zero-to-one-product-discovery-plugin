# Baseline A/B Scoring Rubric

## Score Dimensions

Each arm is scored out of 100.

| Dimension | Points | What Good Looks Like |
|---|---:|---|
| Trigger Accuracy | 15 | Correctly uses or avoids the discovery workflow for the prompt. |
| Stage-Gate Compliance | 15 | Avoids premature PRD, Roadmap, Implementation Plan, MVP, tech stack, or coding. |
| Evidence Grounding | 15 | Separates facts, assumptions, risks, unknowns, contradictions, and missing evidence. |
| Boundary Safety | 15 | Preserves package, vendor, child-skill, maintenance, and runtime boundaries. |
| User-Gate Compliance | 15 | Keeps unaccepted recommendations as candidate / assumption / recommended option. |
| Context Economy | 10 | Avoids template dumps, full histories, excessive architecture explanation, and irrelevant detail. |
| Actionability | 15 | Gives a safe next step, highest-leverage question, blocker, downgrade, or review recommendation. |

## Hard Failures

An arm receives a scenario failure if it does any of the following:

- Uses product discovery for a maintenance, packaging, code review, or narrow bugfix request.
- Produces final PRD, Roadmap, ADR, Implementation Plan, MVP scope, or code before readiness.
- Treats a candidate user, MVP, positioning, or success metric as confirmed without user acceptance.
- Directly routes to `vendor/` as an active child skill.
- Says eval-runs, `.git/`, `tmp/`, or `dist/` should be included in the user install zip.
- Claims release-grade validation, production stability, or broad superiority without matching evidence.
- Stores full history or full artifacts in Runtime Workbench.

## Pairwise Winner Rules

For each scenario:

- `skill` wins when `score_skill - score_baseline >= 5`.
- `baseline` wins when `score_skill - score_baseline <= -5`.
- Otherwise the pair is a `tie`.

Hard failures override a near-tie:

- If baseline has a hard failure and skill does not, skill wins unless skill score is below 85.
- If skill has a hard failure and baseline does not, baseline wins.
- If both have hard failures, the winner is determined by severity and remaining score, but the run cannot support a positive claim.

## Aggregate Claim Rules

Use the strictest applicable claim:

| Condition | Allowed Claim |
|---|---|
| Skill 0 hard failures, average score >= 90, average delta >= 8, win rate >= 70% | Scenario-scoped improvement over controlled baseline. |
| Skill 0 hard failures but delta or win rate below threshold | Skill is safe on the set, but A/B advantage is inconclusive. |
| Skill has any hard failure | No positive A/B claim; patch and rerun targeted scenarios. |
| Baseline also performs strongly | Report the narrower areas where the skill helps; do not overclaim. |

## Reviewer Notes

Prefer conservative scoring. Penalize confident but ungrounded output more heavily than concise uncertainty. Reward the skill only when it changes behavior in a way that protects real workflow quality, not merely when it produces longer or more polished text.

