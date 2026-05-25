# Artifact Adapter Contracts

This reference defines contracts for specialist child skills or agents. The main `zero-to-one-product-discovery` skill owns workflow orchestration, stage gates, context continuity, and user experience. Child skills own specialist artifact quality.

External projects may be copied into `vendor/` as source snapshots, but copied upstream files are not routeable children. Route only through local adapters in `child-skills/`, and preserve the local stage model, trade-off rules, record-style documents, and Context Resume Packet requirements.

For multi-agent execution, use this file for artifact-specific contracts and `multi-agent-orchestration.md` for Controller / Producer / Auditor protocols, Runtime Workbench rules, and Audit Report shape.

## Global Contract

### Main Skill Responsibilities

- Decide the current stage and whether an artifact route is allowed.
- Pass a bounded context packet or Agent Work Order to the child skill.
- Reject or downgrade child output that crosses stage boundaries.
- Decide whether the output can become a final artifact, an outline, a decision surface, or a blocking-question response.
- Keep the user's experience coherent across child skills.
- Keep the Runtime Workbench short and current-state only when multiple producer or audit passes are involved.

### Child Skill Responsibilities

- Produce one specialist artifact or one specialist review.
- Work only from the context packet provided by the main skill.
- Label facts, assumptions, unknowns, risks, and decision surfaces.
- Return readiness status instead of jumping to the next stage.
- End substantial work with a Context Resume Packet.
- When acting as a Producer Agent, return an Agent Return Packet summary before the controller accepts or audits the artifact.

### Auditor Responsibilities

- Review substantial producer output before it is accepted as final or review-ready.
- Check stage boundary, evidence sufficiency, assumption labeling, cross-artifact consistency, and user-gate requirements.
- Produce a concise Audit Report with verdict, blocking issues, non-blocking issues, boundary check, evidence check, consistency check, and recommended next action.
- Do not rewrite the artifact as the producer and do not expose full internal reasoning.

### Universal Child Skill Input

Every child skill invocation should receive:

1. Current stage.
2. Requested artifact or review.
3. Confirmed facts.
4. Working assumptions.
5. Unresolved questions.
6. Key risks and constraints.
7. Existing materials inspected.
8. Explicit out-of-scope and do-not-cross boundaries.
9. Relevant Decision Log / ADR context.
10. Expected output mode: final artifact, outline, decision surface, review, or blocking question.

For Research, PRD, Roadmap, ADR, and Implementation Plan producer routes, prefer the stricter Agent Work Order shape from `multi-agent-orchestration.md`.

### Universal Child Skill Output

Every child skill should return:

1. Artifact body, outline, decision surface, or review result.
2. Evidence status for important claims.
3. Assumptions and unknowns that must not be treated as facts.
4. The current highest-leverage blocking question, if any.
5. Decision Log candidates.
6. ADR candidates, only when architecture-level escalation may apply.
7. Readiness signal: `ready_for_next_stage`, `needs_more_evidence`, `needs_main_skill_decision`, or `blocked`.
8. Context Resume Packet.

For Producer Agent routes, also include the Agent Return Packet fields: status, output summary, evidence changes, blockers, conflicts, self-check, and recommended controller action.

### Universal Prohibitions

- Do not produce final artifacts from ungrounded assumptions.
- Do not paste vendored wording, examples, tables, or templates into user-facing output unless the copied source is explicitly attributed and the main workflow confirms the output mode allows it.
- Do not let a child skill choose the next workflow stage on its own.
- Do not let a child skill invoke another child skill. It may recommend a route; only the main workflow routes.
- Do not use external command-level mini-hubs as child skills unless they are wrapped by the main workflow.
- Do not allow child skills to ask multiple key questions in a single turn.
- Do not use artifact formats to invent missing discovery.
- Do not treat user feedback as requirements without demand triage.
- Do not interpret the per-turn highest-leverage-question rule as a total question limit. Child skills may surface the next highest-leverage blocker; the main workflow decides whether to ask another question in a later turn after updating context.
- Do not put full producer artifacts, transcripts, or long historical logs into the Runtime Workbench.
- Do not let a producer accept its own artifact as final. The controller must accept, downgrade, route to audit, or block it.

## Source Priority

| Source | Role In This Skill | Use For | Avoid |
|---|---|---|---|
| Dean Peters Product-Manager-Skills | PM depth benchmark | PRD depth, discovery reasoning, roadmap quality, story mapping, PM coaching quality | Direct template copying or excessive pedagogic output inside ordinary responses |
| product-on-purpose pm-skills | Productized skill UX benchmark | Skill decomposition, command/workflow structure, sample-output discipline, artifact naming | Replacing the local zero-to-one stage gates with a generic PM lifecycle |
| Addy Osmani agent-skills | Engineering governance benchmark | Spec, plan, build, test, review, ship, ADR hygiene, verification gates | Using engineering flow before product direction is grounded |
| GitHub awesome-copilot | Ecosystem discovery benchmark | Skill/agent inventory patterns, compatibility ideas, Copilot-oriented packaging | Treating community examples as quality authority without review |

## Capability Matrix

| Capability | Route When | Primary Quality Source | Output Mode When Ungrounded | Readiness Signal |
|---|---|---|---|---|
| Research Brief | Evidence exists but is not synthesized | Dean discovery/research; pm-skills interview synthesis | Evidence inventory and research questions | `needs_more_evidence` or `ready_for_next_stage` |
| PRD | Problem, solution direction, feasibility, and MVP hypothesis are grounded | Dean PRD; pm-skills PRD | PRD outline and blocking questions | `needs_main_skill_decision` or `ready_for_next_stage` |
| Roadmap | PRD or PRD outline is confirmed and sequencing is needed | Dean roadmap; pm-skills workflows | Now/Next/Later decision surface | `needs_main_skill_decision` |
| Milestone | Roadmap phase needs validation gates and deliverables | Dean epic hypothesis; pm-skills acceptance criteria | Milestone gate outline | `needs_main_skill_decision` |
| User Stories | MVP slice and scenario are confirmed | Dean user stories/story mapping; pm-skills user stories | Story-map decision surface | `needs_more_evidence` |
| Acceptance Criteria | Specific story or requirement exists | pm-skills acceptance criteria | Criteria checklist gaps | `needs_more_evidence` |
| ADR | A durable technical/platform decision is required | Addy agent-skills; pm-skills ADR | Decision Log entry plus ADR escalation condition | `needs_main_skill_decision` |
| Mermaid | Known entities, flows, dependencies, or decisions need visualization | pm-skills Mermaid; local diagram rules | Assumption-labeled sketch only | `needs_more_evidence` |
| Implementation Plan | Product and design artifacts are confirmed | Addy planning/task breakdown; superpowers writing-plans | Planning readiness review | `blocked` or `ready_for_next_stage` |
| Review | Artifact or plan needs quality gate | Addy review/verification; Dean PM critique | Review findings with blockers | `needs_main_skill_decision` |

## Active Adapter Locations

| Capability | Local Adapter | Vendored Sources |
|---|---|---|
| Research Brief | `child-skills/research-brief/ADAPTER.md` | `vendor/product-manager-skills/skills/jobs-to-be-done/`; `vendor/pm-skills/skills/discover-interview-synthesis/` |
| PRD | `child-skills/prd/ADAPTER.md` | `vendor/product-manager-skills/skills/prd-development/`; `vendor/pm-skills/skills/deliver-prd/` |
| Roadmap | `child-skills/roadmap/ADAPTER.md` | `vendor/product-manager-skills/skills/roadmap-planning/` |
| User Stories | `child-skills/user-stories/ADAPTER.md` | `vendor/product-manager-skills/skills/user-story/`; `vendor/product-manager-skills/skills/user-story-mapping/`; `vendor/pm-skills/skills/deliver-user-stories/` |
| Acceptance Criteria | `child-skills/acceptance-criteria/ADAPTER.md` | `vendor/pm-skills/skills/deliver-acceptance-criteria/` |
| ADR | `child-skills/adr-governance/ADAPTER.md` | `vendor/agent-skills/skills/documentation-and-adrs/`; `vendor/pm-skills/skills/develop-adr/`; `vendor/awesome-copilot/index/adr-generator.agent.md` |
| Mermaid | `child-skills/mermaid/ADAPTER.md` | `vendor/pm-skills/skills/utility-mermaid-diagrams/` |
| Implementation Plan | `child-skills/implementation-plan/ADAPTER.md` | `vendor/agent-skills/skills/planning-and-task-breakdown/`; `vendor/awesome-copilot/index/create-implementation-plan.UPSTREAM_SKILL.md` |
| Review | `child-skills/review/ADAPTER.md` | `vendor/agent-skills/skills/code-review-and-quality/`; `vendor/agent-skills/skills/test-driven-development/` |
| Context Handoff | `child-skills/context-handoff/ADAPTER.md` | `vendor/agent-skills/skills/context-engineering/` |

## Capability Contracts

### Research Brief

Route during Material Assimilation, Problem Framing, Solution Exploration, or Planning Artifacts when there are notes, interviews, feedback, competitor notes, market claims, support logs, screenshots, or other evidence.

The child skill must separate first-party evidence, user opinions, public claims, maintainer assumptions, contradictions, and gaps. It may recommend go / pivot / defer only when evidence supports the recommendation. It must not transform feedback directly into requirements. If multiple gaps exist, return the gap that most changes the next main workflow decision.

As a Producer Agent, Research should update the Evidence Snapshot and Dependency Board, not PRD or Roadmap commitments.

### PRD

Route to final PRD only after the main skill has grounded the problem definition, user/scenario hypothesis, solution direction, MVP hypothesis, success/failure indicators, risks, constraints, and non-goals. If any prerequisite is only assumption-labeled, route to outline or decision-surface mode instead.

If any prerequisite is missing, the child skill returns a PRD outline, a missing-evidence list, and the highest-leverage blocking question for the current turn. It must not create backlog detail, implementation tasks, or final requirements from assumptions.

As a Producer Agent, PRD must self-check whether every requirement is labeled as confirmed, assumption, or unknown before recommending audit or acceptance.

### Roadmap

Route after PRD confirmation when the project needs staged validation or delivery sequencing.

The child skill should prefer Now / Next / Later or phase gates unless dates are provided. It must connect each phase to a goal, validation signal, dependency, risk, and non-goal. It must not convert speculative future ideas into committed backlog.

As a Producer Agent, Roadmap must surface dependencies and conflicts with PRD scope instead of resolving them on its own.

### Milestone

Route after roadmap sequencing when a phase needs concrete validation gates, deliverables, dependencies, and exit conditions.

The child skill must define milestones as learning or delivery bets, not dates alone. It must keep engineering tasks out until Implementation Planning.

### User Stories

Route after the MVP slice, user scenario/job, and PRD requirement are confirmed.

The child skill may create an initial story map or release slice. It must not generate a full backlog before MVP scope is grounded, and it must label deferred stories as deferred rather than committed.

### Acceptance Criteria

Route when a story or requirement has expected user-visible behavior.

The child skill should produce success, failure, boundary, and verification criteria. It must not invent requirements or embed implementation details unless the implementation has already been chosen.

### ADR

Route only when a decision shapes architecture, platform, data, security, privacy, deployment, module boundaries, major dependencies, or long-term maintainability.

Ordinary product scope and sequencing decisions stay in the Decision Log. If the decision may become architecture-shaping, the child skill should produce a Decision Log entry plus explicit ADR escalation conditions.

As a Producer Agent, ADR Governance is conditionally triggered. It must downgrade to Decision Log when the decision is ordinary product scope or sequencing.

### Mermaid

Route when a diagram clarifies a known flow, dependency, architecture shape, decision tree, or evidence map.

The child skill must state the diagram purpose and label assumption nodes. It must not diagram unknown product or technical structure as fact.

### Implementation Plan

Route only after design direction and planning artifacts are confirmed.

The child skill must produce decision-complete tasks with validation steps and acceptance criteria. It should use engineering planning practices from Addy-style lifecycle skills and `superpowers:writing-plans` when available.

As a Producer Agent, Implementation Plan must block when PRD, Roadmap, acceptance criteria, or technical constraints are unreviewed or contradictory.

### Review

Route when a major artifact, implementation plan, or release candidate needs critique.

The child skill should review from product/value, user experience, open-source maintainer, engineering, testing, and long-term architecture perspectives as relevant. Findings must lead, blockers must be explicit, and stylistic preferences must not be treated as blockers.

Review can act as the Auditor Agent, but it must report through the Audit Report shape and must not become a second producer for the same artifact.

## Heavy Advisor Orchestration

Heavy Advisor may call multiple capability contracts in one response, but only as outlines, decision surfaces, and assumption clearings unless the product is already grounded.

The main skill should:

- Warn about context cost and assumption-hardening risk.
- Limit each child capability to its readiness signal and highest-risk open questions.
- Prevent a bundle of outlines from appearing as a committed PRD, Roadmap, Milestone plan, ADR set, or backlog.
- End with one main-skill alignment question.

## Context Resume Packet

Every substantial child output must include:

```markdown
## Context Resume Packet

### Current Stage

### Artifact / Capability Routed

### Confirmed Facts

### Working Assumptions

### Unresolved Questions

### Decision Log Candidates

### ADR Candidates

### Key Risks

### Readiness Signal

### Recommended Main Skill Action
```
