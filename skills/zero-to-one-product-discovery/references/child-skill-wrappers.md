# Local Child Skill Wrappers

## Document Purpose

This document defines the first local wrappers for specialist child capabilities. A wrapper is the local contract that lets the main workflow benefit from an external skill's quality without giving that external skill routing authority.

These wrappers are local adapters over copied or referenced source material. Upstream text may be preserved under `vendor/`, but routeable wrapper behavior is rewritten into local stage gates, handoff packets, output boundaries, readiness signals, and UX rules.

## Update Rules

- Add a wrapper only after route gate, input packet, output contract, prohibited behavior, and eval coverage exist.
- Keep each wrapper narrow. If it starts orchestrating other wrappers, split it or route that orchestration back to the main skill.
- Do not use command-level mini-hubs as wrappers.
- Record external source influence in `source-attribution.md`.
- If a wrapper uses copied upstream material, keep the copied source in `vendor/` and keep the wrapper itself in `child-skills/`.

## Wrapper Matrix

| Wrapper | External Quality Influence | Main Stage | Allowed Output | Readiness Signal |
|---|---|---|---|---|
| Problem Framing Wrapper | Product-Manager-Skills `problem-framing-canvas` | Problem Framing | Problem hypothesis, assumptions, overlooked perspectives, HMW candidate, evidence gaps | `ready_for_next_stage`, `needs_more_evidence`, or `needs_main_skill_decision` |
| ADR Governance Wrapper | agent-skills `documentation-and-adrs` | Planning Artifacts / Implementation Planning | ADR readiness review, proposed ADR, accepted ADR only when grounded | `ready_for_next_stage`, `needs_main_skill_decision`, or `blocked` |
| Context Handoff Wrapper | agent-skills `context-engineering` | Any substantial transition | Context pack / Context Resume Packet quality review | `ready_for_next_stage` or `needs_more_evidence` |

Expanded copy-first adapters now live in `child-skills/`. This file keeps the higher-level wrapper policy and the first three wrapper contracts that were pressure-tested before the copy-first expansion.

## Universal Wrapper UX Rules

- End with exactly one `Recommended Main Skill Action`.
- The recommended action must be the single highest-leverage question or material request for the current turn, not both.
- This is a per-turn rule, not a total question limit. After the user answers, the main workflow updates facts / assumptions / risks / gaps and may ask the next highest-leverage question in a later turn.
- If several gaps exist, choose the one that most changes the next stage decision.
- Do not append an extra question after the recommended action.
- Keep wrapper output compact enough that the main workflow remains the user's perceived interface.

## Problem Framing Wrapper

### Route When

Use after Diagnostic Start when the main workflow needs a clearer problem statement before Solution Exploration.

Good inputs:

- Vague product idea with symptoms but no confirmed problem.
- Stakeholder or user request that may be solution-first.
- Existing notes that contain pains, assumptions, user groups, or conflicting interpretations.
- Product direction that needs bias-resistant reframing before PRD or Roadmap.

### Do Not Route When

- The user asks for a narrow implementation task.
- The problem is already validated and the next decision is MVP scope or Planning Artifacts.
- The request is skill maintenance or source governance.
- The user asks for a solution brainstorm before the main workflow has accepted the problem framing stage.

### Required Input Packet

```markdown
## Problem Framing Handoff

### Current Stage

### Initial Problem / Symptom

### Confirmed Facts

### Working Assumptions

### User / Stakeholder Signals

### Existing Evidence

### Constraints / Non-goals

### Known Bias Or Premature Solution Risk

### Expected Output Mode
problem hypothesis / evidence gap review / blocking question
```

### Output Contract

Return:

1. Initial framing in the user's words.
2. Assumptions and biases to challenge.
3. Who may experience the problem and who may be missing from current evidence.
4. Consequences and contexts, labeled by evidence status.
5. Reframed problem hypothesis.
6. HMW candidate, labeled as candidate, not final strategy.
7. Evidence gaps blocking Solution Exploration.
8. Decision Log candidates, if a product framing trade-off appears.
9. Readiness signal.
10. Context Resume Packet.

### Quality Bar

- Preserve the difference between symptom, problem, stakeholder request, and solution idea.
- Do not invent personas as confirmed facts.
- Do not generate MVP scope, roadmap, PRD, or implementation tasks.
- Ask at most one high-leverage question per turn.
- Do not include both a recommended evidence request and an additional key question.
- Prefer a compact reframing over a workshop transcript.

## ADR Governance Wrapper

### Route When

Use when a decision may shape architecture, platform, data, security, privacy, deployment, module boundaries, major dependencies, or long-term maintainability.

Good inputs:

- Platform or data model decision.
- Durable integration or extension mechanism.
- Public API shape.
- Build/deployment/infrastructure choice.
- Security or privacy boundary.

### Do Not Route When

- The decision is ordinary product sequencing or scope.
- Options and drivers are unknown and the decision is not architecture-level.
- The output would accept an ADR before validation method and consequences are clear.

### Required Input Packet

```markdown
## ADR Governance Handoff

### Current Stage

### Decision Topic

### Why This Might Need ADR

### Confirmed Constraints

### Options Known So Far

### Decision Drivers

### Validation Method

### Rollback / Supersession Concern

### Decision Log Context

### Expected Output Mode
ADR readiness review / ADR-ready decision surface / proposed ADR / accepted ADR
```

### Output Contract

Return:

1. ADR qualification judgment.
2. Decision drivers.
3. Options and trade-off matrix when enough options exist.
4. Proposed decision only if evidence is sufficient.
5. Consequences and follow-up checks.
6. Validation method.
7. Rollback or supersession condition.
8. Links to PRD, Roadmap, Milestone, or Decision Log context.
9. Readiness signal.

### Quality Bar

- Do not create ADRs for normal product scope choices.
- Do not accept an ADR with only one unchallenged option unless the reason is explicit.
- Do not delete or rewrite accepted ADR history; supersede instead.
- Keep accepted decisions separate from proposed decision surfaces.

## Context Handoff Wrapper

### Route When

Use at stage transitions, long-session handoffs, child-skill returns, global installation preparation, or before starting implementation planning.

Good inputs:

- Substantial discovery progress.
- Multiple child outputs that need a coherent handoff.
- A new window or new agent will continue the work.
- The user asks for project status, next action, or a resume packet.

### Do Not Route When

- The turn is a narrow answer that does not change project state.
- The context packet would repeat the whole conversation instead of compressing decisions.
- The request is source-governance meta-work and only needs a maintenance summary.

### Required Input Packet

```markdown
## Context Handoff Input

### Current Stage

### Confirmed Decisions

### Working Assumptions

### Unresolved Questions

### Candidate Directions

### Excluded Directions

### Key Risks

### Verified Evidence

### Unverified Claims

### Linked Artifacts

### Recommended Next Action
```

### Output Contract

Return a compact Context Resume Packet that:

1. Names current stage and next safe action.
2. Separates confirmed decisions from assumptions.
3. Names unresolved questions and blockers.
4. Lists linked artifacts and evidence used.
5. Preserves user constraints such as personal open-source, resume, learning, or non-commercial goals.
6. Avoids copying large prior content.
7. Tells the next agent what not to do.

### Quality Bar

- Short enough to paste into a new session.
- Specific enough to prevent wrong-stage work.
- No stale recommendations that contradict newer decisions.
- No hidden secrets or environment values.

## Wrapper Installation Policy

These wrappers are active local contracts. They do not require global installation of external skills.

Before installing an external skill globally:

1. Add or update its wrapper here.
2. Add eval scenarios for route, downgrade, source boundary, and UX consistency.
3. When the test phase resumes, run a fresh pressure test with 0 hard failures.
4. When installation is being considered, confirm natural trigger behavior will not conflict with the main workflow.
