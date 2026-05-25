# Documentation Templates

Use this reference when creating project-side planning or record documents.

## Record-Style Document Rule

All record-style documents must use this structure:

```markdown
# Document Title

## Document Purpose

Explain what this document is long-term, who reads it, and what problem it solves.

## Update Rules

Explain how future entries are appended and which historical facts must not be overwritten.

## Records

### YYYY-MM-DD: Entry Topic

Record the background, content, validation result, and follow-up notes for this entry.
```

Use the user's preferred Chinese headings when the project documentation is Chinese:

```markdown
# 文档标题

## 文档说明

说明这个文档长期是什么、给谁看、解决什么问题。

## 更新规则

说明以后怎么追加、哪些内容不能覆盖历史事实。

## 记录

### YYYY-MM-DD：本次主题

记录这一次的背景、内容、验证结果、后续注意。
```

Applies to:

- Project Log.
- Decision Log.
- Research Log.
- Validation Log.
- Deviation Log.
- Meeting Log.
- Experiment Log.

## Project Log Template

```markdown
# Project Log

## Document Purpose

Project Log records major context, stage outcomes, validation results, and follow-up notes so the project can be resumed across sessions, models, and time.

## Update Rules

- Append new entries; do not overwrite historical facts.
- Add an entry after each major stage, validation, or deviation.
- Put detailed decisions in Decision Log or ADR and link them here.

## Records

### YYYY-MM-DD: Entry Topic

#### Background

#### Work Completed

#### Validation Result

#### Risks And Issues

#### Follow-up Notes

#### Links
```

## Decision Log Template

```markdown
# Decision Log

## Document Purpose

Decision Log records meaningful product, technical, design, roadmap, scope, or execution trade-offs that influence the project but do not necessarily require a full ADR.

## Update Rules

- Append only; do not overwrite historical facts.
- Every meaningful trade-off must add an entry.
- Architecture-level, platform-level, security-sensitive, or hard-to-reverse decisions must be escalated to ADR.

## Records

### YYYY-MM-DD: Decision Topic

#### Background

#### Options

| Option | Pros | Cons | Cost | Risk |
|---|---|---|---|---|

#### Trade-off Review

| Dimension | Judgment |
|---|---|
| User value |  |
| Development cycle |  |
| Implementation cost |  |
| Technical risk |  |
| Dependency risk |  |
| Testability |  |
| Maintenance cost |  |
| Extensibility |  |
| Open-source value |  |
| Resume value |  |

#### Decision

#### Why This Option

#### Why Not The Others

#### Validation Method

#### Rollback Condition

#### Links
```

## ADR Template

```markdown
# ADR-0000: Decision Title

## Document Purpose

This ADR records one architecture-level or long-lived technical decision, including context, alternatives, trade-offs, consequences, and validation.

## Update Rules

- Do not rewrite historical context after acceptance.
- If replaced, mark this ADR as Superseded and create a new ADR.
- Link related PRD, Roadmap, Milestone, and Decision Log entries.

## Status

Proposed / Accepted / Superseded / Rejected

## Date

YYYY-MM-DD

## Background

## Problem

## Options

| Option | Description | Pros | Cons | Cost | Risk |
|---|---|---|---|---|---|

## Trade-off Matrix

| Dimension | Option A | Option B | Option C |
|---|---|---|---|
| User value |  |  |  |
| Development cycle |  |  |  |
| Implementation cost |  |  |  |
| Technical risk |  |  |  |
| Dependency risk |  |  |  |
| Testability |  |  |  |
| Maintenance cost |  |  |  |
| Extensibility |  |  |  |
| Open-source value |  |  |  |
| Resume value |  |  |  |

## Decision

## Consequences

## Validation Method

## Rollback Or Supersession Condition

## Links
```

## PRD, Roadmap, And Milestone

Keep these as planning artifacts rather than record logs, but include update records if they evolve over time.

Each must link to related Decision Log and ADR entries when scope, architecture, or roadmap trade-offs are made.

## Audit Report Template

Use Audit Report for user-visible review of substantial producer output. Keep it concise.

```markdown
# Audit Report

## Verdict
Pass / Needs Revision / Blocked

## Reviewed Item

## Blocking Issues

## Non-blocking Issues

## Boundary Check

## Evidence Check

## Consistency Check

## Recommended Next Action
```

## Trace Report Template

Use Trace Report only for retrospective review, resume material, or evaluation evidence. Do not feed it back into the Runtime Workbench as current state.

```markdown
# Trace Report

## Document Purpose

Summarize important workflow decisions, producer outputs, audits, user gates, and rejected approaches for review or portfolio use.

## Scope

Stage, date range, artifacts, or evaluation run covered.

## Key Decisions

## Producer Outputs

## Audit Results

## User Gates

## Rejected Approaches

## Remaining Risks

## Resume / Portfolio Notes
```
