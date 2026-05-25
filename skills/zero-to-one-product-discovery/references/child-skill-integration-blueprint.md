# Child Skill Integration Blueprint

## Document Purpose

This document turns external-source review into an integration plan for the hub-and-spoke `zero-to-one-product-discovery` architecture.

The goal is copy-first, not install-first: copy high-value upstream source into `vendor/`, then expose only locally adapted child skills from `child-skills/`. The main workflow still preserves coherent user experience and prevents child skills from bypassing workflow control.

## Update Rules

- Append future source decisions instead of silently replacing old judgments.
- Record whether a candidate is a direct-install candidate, local rewrite candidate, benchmark only, or quality gate.
- Do not add an external child skill to the active workflow until its route gate, input packet, output contract, and eval scenario exist.
- Command-level mini-hubs are benchmarks unless explicitly wrapped by the main workflow.

## Integration Policy

### Do Install Or Rewrite

- Narrow specialist skills with one clear artifact or review job.
- Skills that can accept a bounded handoff packet.
- Skills that can return a readiness signal without choosing the next workflow stage.
- Engineering governance skills that operate after Planning Artifacts are grounded.

### Do Not Directly Install As Children

- External command layers that already orchestrate multiple skills.
- Skills that ask the user to restart product discovery from their own lifecycle.
- Skills that produce final PRD, Roadmap, ADR, backlog, or implementation plan without checking local stage gates.

### Copy-First Decision

Do not globally install external skills yet. Direct installation affects future Codex sessions and may change natural trigger behavior before the local contracts and pressure tests prove that the hub can control child boundaries.

Use copied local source snapshots first, then decide one of four integration modes per capability:

1. `vendored_with_local_adapter`
2. `local_rewrite_from_reference`
3. `benchmark_only`
4. `quality_gate_only`

Raw upstream files live under `vendor/`. Routeable local wrappers live under `child-skills/`.

## Product-Manager-Skills Candidates

| Candidate | Source Path | Capability | Integration Mode | Gate / Risk |
|---|---|---|---|---|
| `problem-framing-canvas` | `vendor/product-manager-skills/skills/problem-framing-canvas/UPSTREAM_SKILL.md` | Problem Framing / Research Brief | `vendored_with_local_adapter` | Must output problem hypothesis, assumptions, HMW, and evidence gaps without skipping Diagnostic Start. |
| `jobs-to-be-done` | `vendor/product-manager-skills/skills/jobs-to-be-done/UPSTREAM_SKILL.md` | Research Brief / Positioning / PRD input | `vendored_with_local_adapter` | Must label jobs as validated, assumed, or unknown. |
| `opportunity-solution-tree` | `/private/tmp/Product-Manager-Skills/skills/opportunity-solution-tree/SKILL.md` | Opportunity Mapping / Solution Options / Roadmap input | `local_rewrite_from_reference` | Spans outcome, solution, and experiment; split under local stage gates. |
| `pol-probe-advisor` | `/private/tmp/Product-Manager-Skills/skills/pol-probe-advisor/SKILL.md` | Validation Plan / Milestone evidence | `local_rewrite_from_reference` | Requires a clear hypothesis; unsafe for vague ideas. Not vendored in the first copy-first batch. |
| `prd-development` | `vendor/product-manager-skills/skills/prd-development/UPSTREAM_SKILL.md` | PRD | `vendored_with_local_adapter` | Eight-stage workflow may consume main hub responsibilities; extract quality checks and structure only. |
| `roadmap-planning` | `vendor/product-manager-skills/skills/roadmap-planning/UPSTREAM_SKILL.md` | Roadmap | `vendored_with_local_adapter` | Extract Now/Next/Later, outcome linkage, sequencing risk, and validation gates. |
| `user-story-mapping` | `vendor/product-manager-skills/skills/user-story-mapping/UPSTREAM_SKILL.md` | Milestone / User Stories / Release slicing | `vendored_with_local_adapter` | Only after validated opportunity or approved PRD. |
| `user-story` | `vendor/product-manager-skills/skills/user-story/UPSTREAM_SKILL.md` | User Stories | `vendored_with_local_adapter` | Requires persona, problem, desired outcome, and scope boundary. |
| `positioning-statement` / `positioning-workshop` | `/private/tmp/Product-Manager-Skills/skills/positioning-statement/SKILL.md`; `/private/tmp/Product-Manager-Skills/skills/positioning-workshop/SKILL.md` | Positioning / Product narrative | `local_rewrite_from_reference` | Positioning must not drive problem definition during Diagnostic Start. |
| `recommendation-canvas` | `/private/tmp/Product-Manager-Skills/skills/recommendation-canvas/SKILL.md` | Review / Decision Memo / Product Bet Review | `local_rewrite_from_reference` | Generalize beyond AI-only assumptions if used. |

### Benchmark-Only Commands

| Command | Source Path | Why Benchmark Only |
|---|---|---|
| `/discover` | `/private/tmp/Product-Manager-Skills/commands/discover.md` | It orchestrates multiple PM stages and can bypass this repository's main workflow. |
| `/write-prd` | `/private/tmp/Product-Manager-Skills/commands/write-prd.md` | It chains problem statement, persona, PRD, user story, and splitting, duplicating hub control. |
| `/plan-roadmap` | `/private/tmp/Product-Manager-Skills/commands/plan-roadmap.md` | It is useful for expected quality, but route authority must stay local. |

## agent-skills Candidates

| Candidate | Source Path | Capability | Integration Mode | Gate / Risk |
|---|---|---|---|---|
| Orchestration Patterns | `/private/tmp/agent-skills/references/orchestration-patterns.md` | Hub-and-spoke rules | `local_rewrite_from_reference` | Useful immediately; must reinforce that only the hub orchestrates. |
| Context Engineering | `vendor/agent-skills/skills/context-engineering/UPSTREAM_SKILL.md` | Context Engineering / handoff packets | `vendored_with_local_adapter` | Task-specific context pack waits until the task is known. |
| Spec-Driven Development | `/private/tmp/agent-skills/skills/spec-driven-development/SKILL.md` | Planning Artifacts Grounding | `local_rewrite_from_reference` | Should define grounded spec readiness, not replace product discovery. |
| Planning and Task Breakdown | `vendor/agent-skills/skills/planning-and-task-breakdown/UPSTREAM_SKILL.md` | Implementation Plan | `vendored_with_local_adapter` | Only after planning artifacts are review-ready. |
| Documentation and ADRs | `vendor/agent-skills/skills/documentation-and-adrs/UPSTREAM_SKILL.md` | ADR | `vendored_with_local_adapter` | Accepted ADR requires grounded technical decision context. |
| Source-Driven Development | `/private/tmp/agent-skills/skills/source-driven-development/SKILL.md` | Source policy / technical grounding | `local_rewrite_from_reference` | Specific implementation use waits for chosen stack/version. |
| Incremental Implementation | `/private/tmp/agent-skills/skills/incremental-implementation/SKILL.md` | Implementation execution discipline | `local_rewrite_from_reference` | Only for concrete plan tasks. Not vendored in the first copy-first batch. |
| Test-Driven Development / Test Engineer | `vendor/agent-skills/skills/test-driven-development/UPSTREAM_SKILL.md` | Test | `quality_gate_only` | Requires acceptance criteria and implementation target. |
| Code Review and Quality / Code Reviewer | `vendor/agent-skills/skills/code-review-and-quality/UPSTREAM_SKILL.md` | Review | `quality_gate_only` | Requires diff and spec/task intent. |

## pm-skills Vendored Candidates

| Candidate | Source Path | Capability | Integration Mode | Gate / Risk |
|---|---|---|---|---|
| `deliver-prd` | `vendor/pm-skills/skills/deliver-prd/UPSTREAM_SKILL.md` | PRD | `vendored_with_local_adapter` | Command wrapper is source only; local PRD adapter owns grounding and downgrade. |
| `deliver-user-stories` | `vendor/pm-skills/skills/deliver-user-stories/UPSTREAM_SKILL.md` | User Stories | `vendored_with_local_adapter` | Requires confirmed MVP slice and requirement context. |
| `deliver-acceptance-criteria` | `vendor/pm-skills/skills/deliver-acceptance-criteria/UPSTREAM_SKILL.md` | Acceptance Criteria | `vendored_with_local_adapter` | Must not create new requirements. |
| `develop-adr` | `vendor/pm-skills/skills/develop-adr/UPSTREAM_SKILL.md` | ADR | `vendored_with_local_adapter` | Must pass ADR escalation gate. |
| `discover-interview-synthesis` | `vendor/pm-skills/skills/discover-interview-synthesis/UPSTREAM_SKILL.md` | Research Brief | `vendored_with_local_adapter` | Must separate evidence, claims, assumptions, contradictions, and gaps. |
| `utility-mermaid-diagrams` | `vendor/pm-skills/skills/utility-mermaid-diagrams/UPSTREAM_SKILL.md` | Mermaid | `vendored_with_local_adapter` | Diagram only known or assumption-labeled structure. |

## awesome-copilot Vendored References

| Candidate | Source Path | Capability | Integration Mode | Gate / Risk |
|---|---|---|---|---|
| `adr-generator.agent.md` | `vendor/awesome-copilot/index/adr-generator.agent.md` | ADR reference | `benchmark_only` | Agent persona is not routeable; use only as ADR quality reference. |
| `create-implementation-plan.UPSTREAM_SKILL.md` | `vendor/awesome-copilot/index/create-implementation-plan.UPSTREAM_SKILL.md` | Implementation Plan reference | `benchmark_only` | Copilot packaging is not local workflow authority. |
| Shipping and Launch / Security Auditor | `/private/tmp/agent-skills/skills/shipping-and-launch/SKILL.md`; `/private/tmp/agent-skills/agents/security-auditor.md` | Ship / Release gate | `quality_gate_only` | Requires implemented scope, risk profile, and verification commands. |

## Next Implementation Order

1. Completed: Add explicit orchestration-pattern rules to `planning-artifacts.md`: no router persona, no child-to-child invocation, only hub-to-child routing.
2. Completed: Add a `Planning Artifacts Grounding` contract that defines what counts as grounded enough for PRD, Roadmap, User Stories, ADR, and Implementation Plan.
3. Completed: Add eval scenarios for direct-install candidates before installing them globally.
4. Completed: Run child-routing pressure test and boundary rerun.
5. Completed: Create first local wrappers in `child-skill-wrappers.md` for Problem Framing, ADR Governance, and Context Handoff.
6. Completed: Copy selected upstream source snapshots into `vendor/` and create routeable local adapters in `child-skills/`.
7. Completed: Add platform-agnostic multi-agent protocol in `references/multi-agent-orchestration.md`, including Controller Agent, Producer Agents, Auditor Agent, Runtime Workbench, Agent Work Order, Agent Return Packet, Audit Report, and Trace Report boundaries.
8. Completed structurally: Add multi-agent eval scenarios and hard failures for controller overreach, producer overreach, workbench overload, ADR condition gates, and user-gate omissions.
9. Deferred: Run copied-child-skill routing, attribution, UX consistency, and multi-agent protocol pressure tests before any global external skill installation, after the current documentation/state cleanup and rule convergence pass is complete.
10. Deferred: Create an extension SOP for applying the producer/auditor/workbench pattern to remaining adapters after the core five producer routes have fresh pressure evidence.

## Monitoring Rules

- If a candidate includes its own command workflow, treat it as benchmark only until wrapped.
- If a candidate asks multiple strategic questions in one turn, wrap it with the per-turn highest-leverage-question UX rule.
- If a candidate outputs final artifacts from assumptions, downgrade it to outline mode.
- If a candidate needs current external facts, route through source-driven research rules before artifact generation.
- If global installation changes natural trigger behavior, revert to local rewrite mode.
- If producer agents start communicating directly or accepting their own artifacts as final, route through the Controller Agent and Auditor Agent contract in `multi-agent-orchestration.md`.
- If Runtime Workbench starts accumulating transcript-like history, move retrospective material to a Trace Report outside the runtime path.
