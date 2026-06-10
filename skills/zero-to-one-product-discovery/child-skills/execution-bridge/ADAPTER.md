---
name: execution-bridge
description: Use when the main workflow has a review-ready Implementation Plan and the user needs a host-executable dry-run handoff for GitHub Issues, Claude Code tasks, or Jira tickets.
---

# Execution Bridge

## Role

Convert a review-ready Implementation Plan into host-executable downstream handoff formats while preserving evidence labels, acceptance criteria, and verification commands.

Execution Bridge prepares payloads and instructions for the host agent. It does not directly create GitHub Issues, Jira tickets, project items, branches, pull requests, or external tasks.

## Required Input

- Review-ready Implementation Plan with ordered tasks, acceptance checks, and verification commands.
- Target format: GitHub Issues, Claude Code tasks, or Jira tickets.
- Repository context when relevant: repo URL, project board, labels, assignees.
- Evidence snapshot: which inputs are facts, assumptions, or unknowns.
- Explicit user approval is required before any host agent performs external side effects.

## Output Contract

For each task in the Implementation Plan, produce one output unit in the target format.

Default mode is `dry_run`. If the host agent later creates external issues after explicit user approval, record only external refs (issue number, URL, created_at) back into the workbench.

### GitHub Issues Host Handoff

```markdown
## Title
[Task title from Implementation Plan]

## Description
[Task description with context from PRD and Implementation Plan]

## Acceptance Criteria
- [ ] [Criterion 1 from Implementation Plan]
- [ ] [Criterion 2 from Implementation Plan]

## Evidence Context
- Source: [PRD section / User Story / ADR reference]
- Assumption status: [Fact / Assumption / Unknown]
- Validation needed: [Yes/No, what if yes]

## Labels
- evidence-[fact/assumption/unknown]
- priority-[high/medium/low]
- component-[name]

## Verification Commands
[Commands or scenarios from Implementation Plan]

## Dependencies
[Blocking tasks or external dependencies]

## Host Execution
- Mode: dry_run
- Requires explicit user approval: yes
- Suggested command:
  `gh issue create --repo <owner/repo> --title "<title>" --body-file <body-file> --label <label>`
```

Also produce `github-issues.json` following `evals/execution-handoff.schema.json` and one Markdown body file per issue:

```text
execution/github-issues.md
execution/github-issues.json
execution/github-issue-bodies/001-<task-slug>.md
execution/host-execution-checklist.md
```

GitHub Issues are the P0 host-executable target. Claude Code tasks and Jira tickets remain format conversions unless a future host runtime provides approved connectors.

### Claude Code Tasks Format

```markdown
## Task
[Task description]

## Context
- PRD: [relevant PRD section summary]
- User Story: [if applicable]
- ADR: [if applicable]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Evidence Labels
- [Fact/Assumption/Unknown]: [what]

## Verification
[Commands or scenarios to verify completion]

## Boundaries
- Non-goals: [from Implementation Plan]
- Constraints: [from Implementation Plan]
```

### Jira Tickets Format

```markdown
## Summary
[Task title]

## Description
[Task description with context]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Evidence Context
Source: [PRD / User Story / ADR]
Assumption status: [Fact / Assumption / Unknown]

## Definition of Done
- [All acceptance criteria met]
- [Verification commands pass]
- [Evidence labels reviewed]

## Labels
evidence-[status], priority-[level], component-[name]
```

## Boundaries

- Only accept review-ready Implementation Plans as input. Do not convert PRD, Roadmap, or User Stories directly to execution format.
- Do not modify the Implementation Plan content. Transcode and restructure only.
- Every output unit must preserve evidence labels from the source artifacts.
- Do not invent tasks, acceptance criteria, or verification commands that are not in the Implementation Plan.
- Do not assign tasks to specific people unless the user provides assignment information.
- If the Implementation Plan has gaps, report them as blockers rather than filling them with assumptions.
- Do not perform network calls, GitHub API calls, Jira API calls, telemetry, analytics, or `gh issue create` execution from inside Z2O.
- Do not claim GitHub Issues or Jira tickets were created unless the host agent actually executed them after explicit user approval.
- Do not treat external issue status as internal product evidence. Store only external refs in the workbench.

## Readiness Signal

Return `ready_for_next_stage` when all tasks are converted to the target handoff format and host execution remains dry-run or separately approved.

Return `needs_more_evidence` if the Implementation Plan has gaps that prevent conversion (missing acceptance criteria, missing verification commands, unclear task boundaries).

Return `needs_main_skill_decision` if the user needs to choose between conflicting target formats or if task prioritization is unclear.

Return `blocked` if the Implementation Plan is not review-ready.

## Context Resume Packet

After conversion, include:

- Number of tasks converted.
- Evidence distribution: how many tasks are fact-grounded vs assumption-labeled.
- Gaps found in the Implementation Plan during conversion.
- Handoff mode: dry_run or host_executed.
- External refs recorded, if host execution was separately approved and completed.
- Recommended next action.
