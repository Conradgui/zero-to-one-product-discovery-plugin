# Evaluation Package

## Purpose

This document summarizes the current evaluation system for `zero-to-one-product-discovery`.

The goal is not to collect large amounts of run output. The goal is to make failures explainable, turn real misses into regression scenarios, and preserve only evidence that improves release, install, architecture, or quality decisions.

## Design Reference

This evaluation system follows the core pattern from OpenAI's "Testing Agent Skills Systematically with Evals":

```text
prompt -> captured run trace / artifacts -> deterministic checks -> structured rubric -> comparable score
```

For this skill, deterministic checks protect hard workflow boundaries, while rubric grading covers qualitative behavior such as evidence grounding, user-question quality, and multi-agent separation.

## Package Boundary

The installable skill keeps only reusable evaluation assets:

- `evals.json`: strict scenario suite, success checks, hard failures, and scoring metadata.
- `eval-rubric-template.md`: scoring and value-review template.
- `claude-code-pressure-test-protocol.md`: five-pass pressure-test protocol.
- `eval-report.schema.json`: structured report schema.
- `value-review.schema.json`: post-test value-gate schema.
- `baseline-ab-template.md`: reusable baseline-vs-skill A/B protocol.
- `baseline-ab-scoring-rubric.md`: paired A/B scoring rubric and claim thresholds.
- `baseline-ab-report.schema.json`: machine-readable A/B report schema.
- `evaluation-package.md`: concise evidence interpretation and release boundary.

Raw responses, JSONL traces, scored reports, audit notes, handoff records, and design records stay outside the skill package in `zero-to-one-product-discovery-eval-runs/`.

Promoted records in `zero-to-one-product-discovery-eval-runs/current/<version>/<run-id>/` may be committed with the GitHub repository as public project evidence. They must not be included in the installable skill zip and must not be loaded during ordinary runtime use.

## Current Version

Current package version: `v0.2.1-multi-agent-docs`.

`v0.1.0-draft` remains the early historical draft. The multi-agent workflow architecture is tracked as the larger `v0.1.5` upgrade. `v0.1.6` packaged the Windows clean-install validation handoff, `v0.1.7` closed the first relay findings, `v0.1.8` applies the final documentation-boundary and PRD Draft user-gate patch, and `v0.1.9` adds a controlled local baseline-vs-skill A/B methodology and evidence run. `v0.2.0` is the portfolio release that packages the installable showcase and evidence dashboard. `v0.2.1` expands the discoverable multi-agent documentation entrypoint under `agents/`. None of these replace the `v0.1.5` strict-suite evidence.

## Strict Suite Shape

The `v0.1.5` suite is intentionally smaller and stricter than the earlier scenario set. It prioritizes high-risk failures over broad but shallow coverage.

Scenario categories:

- `trigger_boundary`
- `stage_gate`
- `evidence_grounding`
- `child_skill_routing`
- `multi_agent_orchestration`
- `audit_user_gate`
- `context_economy`
- `multi_turn_continuity`
- `negative_control`

Every scenario must define:

- `must_pass_checks`: required behaviors.
- `hard_failures`: fail-fast conditions.
- `deterministic_checks`: concrete checks that can be inspected from text, trace, or artifacts.
- `rubric_checks`: qualitative checks for structured grading.
- `why_this_matters`: the real product risk protected by the scenario.
- `value_signal`: what improvement a failure should produce.

## Evidence Value Gate

New run output starts in `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/`.

After scoring, the evaluator must create a value review. A run becomes project evidence only if it finds a substantive issue, exposes a regression, confirms a previously unverified release gate, or produces a concrete improvement direction.

No-actionable-finding runs must not be presented as strong evidence. They can be discarded or preserved as a minimal note only when they close a specific release question.

## Current Evidence Summary

| Area | Status | Interpretation |
|---|---|---|
| Initial trigger and stage-purity checks | Historical evidence in `archive/pre-v0.1.5/` | Useful baseline only; predates later architecture changes. |
| Child-skill routing and wrapper behavior | Historical evidence in `archive/pre-v0.1.5/` | Supports prior refactor decisions, but is not fresh evidence for `v0.1.5`. |
| Source-adapter boundary | Historical evidence in `archive/pre-v0.1.5/` | Supports source-governance direction, with historical limitations. |
| Multi-agent workflow protocol | Structural design documented in `design-records/v0.1.5/` | Architecture is documented and has initial strict-suite pressure evidence. |
| `v0.1.5` strict suite | `current/v0.1.5/2026-05-12-run-01/` | Fresh run found one failed package-boundary scenario and two improvement points; it is valuable evidence but not install-candidate proof. |
| Targeted boundary rerun | `current/v0.1.5/2026-05-14-run-02/` | Five adjacent scenarios passed after patch; closes the package/vendor boundary regression, but does not replace a full-suite rerun. |
| Patched full strict-suite rerun | `current/v0.1.5/2026-05-14-run-03/` | 22 scenarios passed with 0 hard failures and lowest score 90; supports core regression confidence, but not clean install trigger reliability. |
| Windows clean-install handoff | `current/v0.1.6/2026-05-14-windows-clean-install-handoff/` | Test packet and relay template for external Windows Codex validation; status now points to the first returned relay run. |
| Windows clean-install relay run | `current/v0.1.6/2026-05-17-windows-clean-install-run-01/` | 8 relay scenarios passed with 0 hard failures; found actionable follow-up patches for maintenance test contamination, install docs, and version-aware eval paths. |
| v0.1.7 targeted Windows rerun | `current/v0.1.7/2026-05-18-targeted-rerun-01/` | Confirmed maintenance mutation and helper-skill visibility fixes; found final follow-up issues in packaging docs, eval metadata, and PRD Draft user-gate wording. |
| v0.1.9 baseline A/B | `current/v0.1.9/2026-05-18-baseline-ab-run-01/` | Controlled local 10-scenario A/B: skill average 95.7, baseline average 68.4, average delta +27.3, 0 skill hard failures; supports scenario-scoped improvement only. |
| v0.2.0 portfolio release | Repository README, portfolio case study, and install zip | Converts prior architecture and evaluation evidence into an installable showcase package; does not add new release-grade validation. |
| v0.2.1 multi-agent docs | `agents/README.md` and compact orchestration entrypoint | Makes the multi-agent role model visible in the skill body without changing runtime behavior or evaluation claims. |

## Allowed Claims

The current evidence supports these claims:

- The skill has a reusable, strict scenario-based evaluation harness.
- The harness defines deterministic checks, rubric checks, hard failures, and a post-test value gate.
- Historical runs helped shape the current architecture, but they are not release-grade validation for `v0.1.5`.
- The `v0.1.5` multi-agent architecture is structurally documented and has passed a patched full strict-suite rerun.
- The first fresh strict-suite run produced actionable findings, the targeted boundary rerun confirmed the package/vendor boundary patch, and the patched full rerun confirmed no hard failures across the 22 core scenarios.
- `v0.1.6` prepared external Windows clean-install validation through a structured relay test packet.
- `v0.1.7` incorporates the first Windows clean-install relay follow-up patches after 8 scenarios passed with no hard failures.
- `v0.1.8` incorporates the targeted rerun follow-up patch for packaging docs, eval metadata clarity, and PRD Draft user-gate wording.
- `v0.1.9` adds baseline-vs-skill methodology and a controlled local 10-scenario A/B run showing scenario-scoped improvement in stage gates, boundary safety, and user-gate behavior.
- `v0.2.0` is an installable portfolio release that organizes the evidence dashboard, package boundary, and project case study.
- `v0.2.1` clarifies the multi-agent documentation structure by adding `agents/` role-protocol entrypoints while preserving platform-agnostic behavior.

## Unsupported Claims

Do not claim:

- Release-grade validation.
- Production-grade stability.
- Cross-client natural trigger reliability after restart.
- Stable multi-agent runtime behavior in real model runs.
- Complete real-user multi-turn workflow quality.
- Broad or cross-model superiority over baseline model behavior.

## Next Evidence Needed

Before stronger release claims, run and value-review:

1. External or multi-model baseline A/B if stronger superiority claims are needed.
2. Real raw multi-turn discovery trace through Research Brief -> PRD -> Roadmap -> Implementation Plan readiness.
3. Long-horizon real-user usage evidence before any release-grade or production-stability claim.
