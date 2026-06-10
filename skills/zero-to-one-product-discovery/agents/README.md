# Multi-Agent Role Protocol

This directory is the entry point for the skill's multi-agent operating model.

It does not define separately installable agents. The main `SKILL.md` remains the user's single interface. Agent roles may be implemented as real subagents when the host supports them, or simulated as bounded specialist passes inside one assistant session.

## Files

| File | Purpose |
|---|---|
| `openai.yaml` | Codex UI metadata only: display name, short description, and default prompt. It is not the multi-agent runtime protocol. |
| `multi-agent-orchestration.md` | Compact role protocol for Controller, Producers, Auditor, and Runtime Workbench. |

For the full reference, see `../references/multi-agent-orchestration.md`.

Controller action names are defined in `../evals/controller-actions.json`; compact docs and scripts must not keep separate action enums.

## Role Model

| Role | Responsibility | Must Not |
|---|---|---|
| Workflow Rules | Define stages, gates, downgrade rules, allowed outputs, and user gates. | Act like an agent, store state, or accept artifacts. |
| Controller Agent | Applies workflow rules, creates work orders, updates the Runtime Workbench, and decides the next safe action. | Produce unreviewed final artifacts or hide producer/auditor blockers. |
| Producer Agents | Produce one bounded artifact or readiness review from a controller work order. | Choose the next stage, call another producer, or accept their own output as final. |
| Auditor Agent | Checks boundary compliance, evidence quality, cross-artifact consistency, and acceptance readiness. | Rewrite the artifact as the producer or make product decisions for the user. |
| Runtime Workbench | Holds concise current decision state shared by controller, producers, and auditor. | Store full transcripts, long histories, or complete artifacts. |

## Core Producers

| Producer | Trigger | Output | Must Not |
|---|---|---|---|
| Research | Materials, feedback, PRDs, notes, or market/user evidence need synthesis. | Evidence snapshot, contradictions, assumptions, gaps, risks. | Invent evidence or mark assumptions as facts. |
| PRD | Problem, solution direction, MVP hypothesis, risks, and success/failure indicators are grounded enough. | PRD draft, PRD outline, or readiness review. | Produce final PRD before user acceptance or evidence readiness. |
| Roadmap | PRD or PRD outline is accepted enough to sequence validation or delivery. | Now/Next/Later, phases, milestones, validation gates. | Turn weak assumptions into delivery commitments. |
| ADR | Durable architecture/platform/data/security/dependency decision appears. | Decision Log entry or ADR candidate. | Escalate ordinary scope tradeoffs into unnecessary ADRs. |
| Implementation Plan | Planning artifacts and relevant technical decisions are review-ready. | Engineering plan, verification plan, sequencing, risks. | Start coding or scaffold repositories before readiness. |
| Execution Bridge | Review-ready Implementation Plan exists and execution handoff is requested. | Host-executable dry-run handoff or target task format. | Create external issues/tickets directly or invent tasks. |
| Artifact Export | Stable files, delivery package, or File Workbench export is requested. | Fixed artifact package with ready/not-ready markers and manifest guard fields. | Mark missing artifacts or Quick Mode drafts as final, or store full history in Workbench. |
| Revision Trace | Stable artifacts have been exported and artifact diff/history is requested. | Bounded revision ledger with hashes, diffs, and Controller refs. | Store transcripts, hidden reasoning, or use revision count as maturity. |

## Execution Order

Default flow is stage-serial production with local parallel review:

```text
Workflow Rules
  -> Controller Agent
  -> Agent Work Order
  -> Producer Agent
  -> Agent Return Packet
  -> Runtime Workbench update
  -> Auditor Agent, when substantial output needs review
  -> Controller Decision
  -> User Gate, when required
```

The Controller owns routing. Producers and auditors report findings; they do not decide stage upgrades.

## Runtime Boundaries

- Do not require a specific host subagent API.
- Do not expose internal helper skills or host-specific tools unless the user explicitly invokes them.
- Do not route directly to `vendor/`; only local `child-skills/` adapters are routeable.
- Do not store full transcripts or complete artifacts in Runtime Workbench.
- Do not let producer agents call each other.
- Do not accept substantial artifacts as final without controller review and, when needed, Audit Report.
- Do not perform external side effects such as creating GitHub Issues or Jira tickets from Z2O itself; prepare host-executable handoff and require explicit user approval in the host agent.
