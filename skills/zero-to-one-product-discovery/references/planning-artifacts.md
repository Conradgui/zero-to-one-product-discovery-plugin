# Planning Artifact Routing

Use this reference after exploration has grounded the problem, solution direction, feasibility, and MVP hypothesis, or when the user explicitly requests Heavy Advisor mode.

This file is the routing and escalation layer. Detailed child skill contracts live in `artifact-adapters.md`; active local adapters live in `child-skills/`; copied upstream source snapshots live in `vendor/`.

For multi-agent producer, controller, auditor, Runtime Workbench, Agent Work Order, Agent Return Packet, Audit Report, and Trace Report rules, load `multi-agent-orchestration.md`.

## Routing Principle

The main skill owns orchestration. It decides:

- Which stage the project is in.
- Which specialist child skill or agent, if any, should receive the current context.
- Whether the child output is allowed to become a final artifact.
- Whether the output must be downgraded to an outline, decision surface, or blocking question.
- Whether a Decision Log entry or ADR escalation is required.

Child skills improve artifact quality. They do not bypass stage gates.

In multi-agent mode, the main workflow is not a single overloaded agent. Workflow rules define the gate; the Controller Agent applies those rules; Producer Agents create bounded artifacts; the Auditor Agent checks whether the output can be accepted, downgraded, or blocked.

## Orchestration Guardrails

- No router persona: do not create a separate child that decides which child should run next.
- No child-to-child invocation: child skills may recommend another capability, but only the main workflow may route to it.
- No external command mini-hubs as child skills unless wrapped by this routing layer.
- No direct route to `vendor/`; every copied source must pass through a local adapter in `child-skills/`.
- No final artifact from an unverified child result; the main workflow must accept, downgrade, or block it.
- No hidden stage jumps: every route must name current stage, requested capability, expected output mode, and readiness signal.
- No multi-artifact cascade in one ordinary turn. If several capabilities are relevant, route the first blocker or first highest-leverage artifact only, unless Heavy Advisor was explicitly requested.
- No full transcript workbench: the Runtime Workbench may hold current summaries, blockers, dependencies, conflicts, risks, audit queue, and next action only.
- No direct producer-to-producer control: Producer Agents may raise dependencies or conflicts, but only the Controller Agent resolves route order or asks the user.
- No unreviewed acceptance: substantial producer output must pass either an explicit Audit Report or a controller-documented review before it becomes final or review-ready.

## Entry Gate

Before routing to a final Planning Artifact, confirm every required input is grounded as a confirmed fact, inspected material, or accepted decision:

- Problem definition is grounded. If it is only assumption-labeled, the output must stay in outline or decision-surface mode.
- Solution direction is selected. If it is still a small set of options, the output must stay in decision-surface mode.
- Feasibility risks are named.
- MVP hypothesis exists as accepted working scope. Heavy Advisor requests do not satisfy this final-artifact gate.
- Meaningful trade-offs have a Decision Log target.
- The requested artifact has enough input to avoid inventing facts.

If any gate is missing, route to an outline, evidence gap review, decision surface, or the highest-leverage blocking question for the current turn instead of a final artifact. After the user answers, re-evaluate the gate and repeat the loop until the artifact is grounded or blocked.

## Grounding Contract

An artifact is grounded only when the main workflow can name the evidence status for each required input.

| Artifact | Minimum Grounded Inputs | If Missing |
|---|---|---|
| Research Brief | Materials exist and evidence type is known: first-party notes, interviews, feedback, public source, assumption, or contradiction | Ask for material or produce evidence inventory only |
| PRD | Problem definition, user/scenario hypothesis, solution direction, MVP hypothesis, success/failure indicators, risks, constraints, and non-goals | Produce PRD outline plus missing-evidence list |
| Roadmap | Confirmed PRD or PRD outline, MVP scope, non-goals, dependencies, risks, and validation gates | Produce sequencing decision surface |
| Milestone | Roadmap phase, deliverables, acceptance gate, dependencies, and exit condition | Produce milestone gate outline |
| User Stories | MVP slice, user scenario/job, PRD requirement, scope boundary, and acceptance target | Produce story-map decision surface |
| Acceptance Criteria | Specific requirement or story, expected behavior, failure/boundary cases, and verification method | Produce criteria gaps |
| ADR | Architecture/platform/data/security/privacy/deployment/module/dependency decision, options, drivers, validation method, and consequences | Record Decision Log entry and ADR escalation condition |
| Mermaid | Named entities, flows, dependencies, states, or decisions, plus reason a diagram helps | Produce assumption-labeled sketch or no diagram |
| Implementation Plan | Review-ready planning artifacts, accepted technical decisions, file/module boundaries, acceptance criteria, and verification commands | Produce planning readiness review |
| Review | Artifact or plan exists, review lens is named, and blocker definition is clear | Ask what artifact or lens to review |

## Routing Matrix

| User Request / State | Route | Allowed Output | Do Not Allow |
|---|---|---|---|
| Existing notes, PRD draft, feedback, research, or competitor material is unsynthesized | Research Brief contract | Evidence inventory, contradictions, demand triage, research gaps | Turning feedback directly into requirements |
| User asks for PRD before problem and MVP are grounded | PRD contract in outline mode | PRD skeleton, missing evidence, one blocking question | Final PRD, backlog, requirements invented from assumptions |
| Grounded problem, solution direction, feasibility, and MVP hypothesis exist | PRD contract | Final PRD or review-ready PRD draft | Implementation plan disguised as PRD |
| User asks for roadmap before PRD or MVP is grounded | Roadmap contract in decision-surface mode | Sequencing questions, validation gates, Now/Next/Later outline | Dated commitments or fake milestones |
| PRD is confirmed and sequencing is needed | Roadmap contract | Roadmap with validation gates, dependencies, risks, non-goals | Speculative future backlog as commitment |
| Roadmap phase needs concrete validation gate | Milestone contract | Milestone goal, deliverables, acceptance gate, dependencies | Engineering task breakdown before planning |
| MVP slice and scenario are confirmed | User Stories contract | Story map or initial release slice | Full speculative backlog |
| A requirement or story needs QA-ready behavior | Acceptance Criteria contract | Success, failure, boundary, verification criteria | New requirements invented through criteria |
| Decision is product sequencing or scope | Decision Log | Append-only product decision record | ADR by default |
| Decision shapes architecture, platform, data, security, privacy, deployment, module boundaries, major dependencies, or maintainability | ADR contract | ADR or ADR-ready decision surface | Treating early assumptions as accepted decisions |
| Known relationships need visualization | Mermaid contract | Purposeful diagram with assumption labels | Decorative or invented architecture diagrams |
| Planning artifacts are confirmed and engineering handoff is needed | Implementation Plan contract | Decision-complete implementation plan | Reopening product strategy without a contradiction |
| Artifact or plan needs critique | Review contract | Findings, blockers, risks, suggested changes | Style-only objections as blockers |

## Agent Work Order / Child Skill Handoff Packet

Before calling or simulating a child skill or Producer Agent, build a compact packet. Use the stricter Agent Work Order shape from `multi-agent-orchestration.md` when the output may affect PRD, Roadmap, ADR, or Implementation Planning.

```markdown
## Agent Work Order

### Role

### Mission

### Current Workflow State

### Input Context

### Boundaries

### Required Output

### Stop Conditions

### Return Format
Use Agent Return Packet.
```

For lightweight routes, the compact legacy shape remains acceptable:

```markdown
## Child Skill Handoff

### Current Stage
### Requested Capability
### Expected Output Mode
### Confirmed Facts
### Working Assumptions
### Unresolved Questions
### Key Risks / Constraints
### Existing Materials Inspected
### Out Of Scope / Do Not Cross
### Decision Log / ADR Context
```

## Runtime Workbench Use

During multi-agent routing, keep a short Runtime Workbench:

```markdown
## Workflow State
## Evidence Snapshot
## Artifact Status
## Dependency Board
## Conflict Board
## Risk Board
## Audit Queue
## Next Controller Action
```

Do not paste full artifacts or full agent discussions into the workbench. If a user asks for retrospective detail, generate a Trace Report after the stage instead of feeding historical logs back into the controller path.

## Readiness Signals

Child skills must return one readiness signal:

| Signal | Meaning | Main Skill Action |
|---|---|---|
| `ready_for_next_stage` | Artifact is grounded enough to support the next stage | Summarize the decision and ask the next main workflow question |
| `needs_more_evidence` | More material, validation, or specificity is needed | Ask the highest-leverage evidence question for this turn or request the single most important missing material |
| `needs_main_skill_decision` | A trade-off or boundary decision is needed | Present the trade-off and ask the highest-leverage decision question for this turn |
| `blocked` | Artifact would be misleading or unsafe to produce | Explain the blocker and return to the appropriate earlier stage |

## Decision Log And ADR

Use Decision Log for meaningful but not necessarily architecture-level decisions. It must be append-only and follow the record-style structure in `documentation-templates.md`.

Escalate to ADR only when the decision:

- Shapes architecture, platform, data, security, privacy, deployment, or module boundaries.
- Is hard to reverse.
- Adds a major dependency.
- Creates long-term maintenance obligations.
- Changes implementation planning constraints.

Do not create ADRs for ordinary product scope choices. Record those in Decision Log and include ADR escalation conditions only if the scope choice may lock architecture or platform strategy.

## UX Consistency Rules

- The user should feel one coherent workflow, not a handoff between unrelated agents.
- Use one short routing note before specialist output when helpful: "当前进入 PRD 子能力；我会只基于已确认结论输出，不补造缺失发现。"
- Ask only one highest-leverage question per turn unless the user explicitly requests a full review report. This is an iterative loop, not a total question limit: after the user answers, update the context and decide whether another question is needed.
- Keep assumption labels consistent: `Fact`, `Assumption`, `Unknown`, `Risk`, `Decision Surface`.
- End substantial routing work with the same Context Resume Packet shape.
- Preserve the user's constraints, including open-source, resume, learning, portfolio, or personal-project goals, across every child skill call.

## Heavy Advisor Routing

Heavy Advisor is a bundled routing mode, not permission to finalize everything.

When the user explicitly requests Heavy Advisor:

1. Warn that it costs more context and can harden assumptions too early.
2. Build a Runtime Workbench from known facts, assumptions, risks, and current blockers.
3. Build Agent Work Orders for only the relevant Producer Agents.
4. Route to multiple contracts only in outline / decision-surface mode unless grounded evidence exists.
5. Label every leaf-level claim as fact, assumption, unknown, risk, candidate, or decision surface.
6. Audit or controller-review substantial producer output before accepting it as review-ready.
7. End with one main-skill alignment question.

## Self-review Before Implementation Planning

Before routing to Implementation Plan, run or simulate review from:

- Product/value reviewer.
- UX or interaction reviewer when user experience matters.
- Conservative open-source maintainer.
- Engineering reviewer.
- Testing and verification reviewer.
- Long-term architecture reviewer.

Capture blockers separately from non-blocking improvements. Only proceed when blockers are resolved or explicitly accepted as risks.

## External Source Boundary

External PM and engineering skill projects may raise artifact quality, and selected source files may be copied into `vendor/`, but local routing rules win.

- Product-Manager-Skills is the PM depth benchmark.
- pm-skills is the skill decomposition and UX benchmark.
- agent-skills is the engineering governance benchmark.
- awesome-copilot is the ecosystem discovery and compatibility benchmark.

Copied external source must remain attributed in `source-attribution.md` and `vendor/MANIFEST.md`. Do not route external command wrappers directly; if a command is useful, copy it only as source material and expose a locally adapted child skill instead.
