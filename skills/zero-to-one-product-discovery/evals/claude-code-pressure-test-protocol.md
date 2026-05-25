# Claude Code Pressure Test Protocol

## Purpose

This protocol defines a strict, reproducible pressure test for `zero-to-one-product-discovery`.

It follows a five-pass loop:

```text
raw response generation -> deterministic checks -> rubric grading -> value review -> promotion decision
```

The goal is not to produce flattering scores. The goal is to catch regressions, explain failures, and preserve only evidence that improves the product.

## Files Under Test

Repository-relative paths:

- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/references/`
- `zero-to-one-product-discovery/child-skills/`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- `zero-to-one-product-discovery/evals/eval-report.schema.json`
- `zero-to-one-product-discovery/evals/value-review.schema.json`

## Scientific Controls

Use these controls for every run:

- Start from a fresh agent session when possible.
- Do not paste prior self-eval conclusions into the raw generation pass.
- Do not edit the skill during evaluation.
- Do not use web search unless a scenario explicitly requires current external facts.
- Save raw responses or JSONL trace before scoring.
- Record model, agent, date, repository state, scenario set, and skill version.
- Verify repository state with `pwd`, `git rev-parse --show-toplevel`, and `git status --short` when available.
- Record the exact model name if exposed. If unavailable, write `not exposed by CLI`; do not guess.

## Output Layout

Start every run in:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/
```

Expected files:

```text
raw.md or trace.jsonl
scored-report.json
value-review.json
promotion-decision.md
```

Promote the folder only after the value gate passes.

## Pass 1: Raw Response Generation

Goal: generate one response per scenario without reading expected answers.

Rules:

- Read `SKILL.md`.
- Read `evals.json` only for `id`, `category`, `risk_level`, and `prompt`.
- Load references only when the skill says they are needed.
- Do not inspect `must_pass_checks`, `hard_failures`, `deterministic_checks`, `rubric_checks`, `why_this_matters`, or `value_signal`.
- Do not patch the skill.
- Save raw output before scoring.

Output:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/raw.md
```

When using `codex exec --json`, save JSONL to:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/trace.jsonl
```

## Pass 2: Deterministic Checks

Goal: run concrete checks over raw responses, traces, or artifacts.

Examples:

- Response did not produce a PRD during Diagnostic Start.
- Response asked at most one highest-leverage question.
- Runtime Workbench did not contain full transcripts or full artifacts.
- Controller did not treat audit pass as user acceptance.
- Producer did not call another producer directly.
- Skill-maintenance prompts did not trigger product discovery.

Use `deterministic_checks` from `evals.json`. Record each check as pass/fail with evidence.

## Pass 3: Rubric Grading

Goal: score each scenario using `eval-rubric-template.md`.

Rules:

- Read the full `evals.json`.
- Check global and scenario-specific hard failures before assigning verdict.
- Any hard failure means the scenario fails.
- Score all dimensions with cited evidence from raw response, trace, or artifact.
- Write the result using `eval-report.schema.json`.

Output:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/scored-report.json
```

## Pass 4: Value Review

Goal: decide whether this run is useful project evidence.

Use `value-review.schema.json`.

A run is valuable when it finds a substantive issue, exposes a regression, confirms a previously unverified high-risk release gate, or produces a concrete improvement direction.

A run is not valuable evidence when it only says the suite passed, repeats expected behavior, gives generic praise, or produces no actionable patch, rerun, scenario, or release decision.

Output:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/value-review.json
```

## Pass 5: Promotion Decision

Goal: decide what to keep.

Use one of:

- `promote`: move the run to `zero-to-one-product-discovery-eval-runs/current/<tested-version>/<run-id>/`.
- `minimal-note`: keep a short note only, when the run closes a named release question without needing full raw evidence.
- `discard-full-run`: do not retain the full run as project evidence.

Output:

```text
zero-to-one-product-discovery-eval-runs/tmp/<run-id>/promotion-decision.md
```

Do not promote a run that fails the value gate.

## Structured Report Requirements

`scored-report.json` must include:

- environment metadata.
- one result per scenario.
- deterministic-check results.
- rubric-check results.
- hard failures.
- aggregate score.
- substantive findings.
- improvement directions.
- promotion recommendation.

`value-review.json` must include:

- value verdict.
- substantive findings.
- improvement directions.
- product impact.
- promotion decision.
- required next action.
- rationale.

## Claude Code Copy-Paste Prompt

Use this from the repository root:

```markdown
You are evaluating the draft skill `zero-to-one-product-discovery`.

Do not install the skill globally. Do not modify `SKILL.md`, references, child-skills, or eval files during this evaluation.

Before generating responses, record:

- `pwd`
- `git rev-parse --show-toplevel`
- `git status --short`
- exact model name if exposed; otherwise write `not exposed by CLI`
- run ID in the form `YYYY-MM-DD-run-XX`

Read:

- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- `zero-to-one-product-discovery/evals/eval-report.schema.json`
- `zero-to-one-product-discovery/evals/value-review.schema.json`

Pass 1:
Read only each scenario's `id`, `category`, `risk_level`, and `prompt`.
Generate the exact response you would give to the user in a normal session.
Save responses to `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/raw.md`.

Pass 2:
Read each scenario's `deterministic_checks`.
Evaluate each deterministic check with evidence from the raw response.

Pass 3:
Read the full `evals.json` and `eval-rubric-template.md`.
Score every scenario and save `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/scored-report.json` using `eval-report.schema.json`.

Pass 4:
Write `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/value-review.json` using `value-review.schema.json`.
Decide whether the run found substantive issues, concrete improvement directions, release-relevant confidence, or new regression scenarios.

Pass 5:
Write `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/promotion-decision.md`.
Choose one decision: `promote`, `minimal-note`, or `discard-full-run`.

Do not apply patches in this run. Only report them.
```

## Expected Interpretation

- Average score >= 90 and zero hard failures can only support install candidacy if value review also supports the claim.
- Any hard failure requires a patch and rerun of the failed scenario plus adjacent scenarios.
- A clean run with no substantive findings is not strong evidence unless it closes a named release question.
- Non-trigger failures take priority because over-triggering pollutes ordinary work.
