# Baseline A/B Evaluation Template

## Purpose

Use this template to compare ordinary assistant behavior against the `zero-to-one-product-discovery` workflow on the same early product discovery scenarios.

The goal is not to prove broad model superiority. The goal is to measure whether the skill adds scenario-scoped value by improving trigger decisions, stage gates, evidence grounding, boundary safety, user gates, and actionable next steps.

## Methodology References

This protocol follows these evaluation principles:

- Define success criteria before grading.
- Capture raw outputs before reading expected checks.
- Score paired responses with deterministic checks and a structured rubric.
- Preserve limitations and claim boundaries in the final report.
- Promote only runs that create product-relevant evidence or decision value.

Primary references:

- OpenAI Agent Evals: https://platform.openai.com/docs/guides/agent-evals
- OpenAI Trace Grading: https://platform.openai.com/docs/guides/trace-grading
- Anthropic Evaluation Tool: https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
- Google DeepMind FACTS Grounding benchmark: https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/

## A/B Arms

| Arm | Description | Allowed Context | Disallowed Context |
|---|---|---|---|
| A: Baseline | Ordinary assistant behavior without this skill | Scenario prompt only | `SKILL.md`, child-skill docs, eval rubrics, expected checks, prior run reports |
| B: Skill | Assistant behavior with `zero-to-one-product-discovery` loaded | Scenario prompt + `SKILL.md` | Expected checks, hard failures, prior run reports, scoring rubric during raw generation |

If a clean external baseline is unavailable, label the run as `controlled local baseline` and state that the result supports only scoped comparison, not broad model superiority.

## Scenario Set

Use a small paired set, usually 8-12 scenarios. Include:

- Positive trigger scenarios.
- Negative non-trigger scenarios.
- Stage-gate pressure scenarios.
- Evidence-grounding scenarios.
- Packaging or source-boundary scenarios.
- At least one user-gate scenario where recommendations must remain assumptions.

Each scenario must include:

- `id`
- `category`
- `risk_level`
- `prompt`
- `expected_skill_boundary`
- `primary_risk`

## Raw Generation Rules

1. Generate all baseline raw responses before scoring.
2. Generate all skill raw responses before scoring.
3. Do not patch the skill during raw generation.
4. Do not expose expected checks to either arm.
5. Save raw outputs as:
   - `baseline-raw.md`
   - `skill-raw.md`
6. Every raw section must start with `## <scenario id>`.

## Scoring Rules

Score each pair after both raw files exist.

Each scenario receives:

- `score_baseline`: 0-100.
- `score_skill`: 0-100.
- `delta`: `score_skill - score_baseline`.
- `winner`: `skill`, `baseline`, or `tie`.
- `baseline_hard_failures`: array.
- `skill_hard_failures`: array.
- `notes`: concise scenario-specific rationale.

Winner threshold:

- `delta >= 5`: `skill`.
- `delta <= -5`: `baseline`.
- Otherwise: `tie`.

Any hard failure makes that arm fail the scenario regardless of numeric score.

## Aggregate Decision Rules

The A/B run supports a scoped improvement claim only if all are true:

- Skill arm has 0 hard failures.
- Skill average score is at least 90.
- Average delta is at least +8.
- Skill win rate is at least 70%.
- Skill is not worse than baseline by more than 5 points on any critical scenario.

The run does not support:

- Release-grade validation.
- Production stability.
- Broad superiority over ordinary models.
- Claims beyond the tested scenario set.

## Required Outputs

Store promoted A/B evidence under:

```text
zero-to-one-product-discovery-eval-runs/current/<tested-version>/<run-id>/
```

Required files:

- `scenario-set.json`
- `baseline-raw.md`
- `skill-raw.md`
- `baseline-ab-scored-report.json`
- `value-review.json`
- `summary-report.md`
- `promotion-decision.md`
