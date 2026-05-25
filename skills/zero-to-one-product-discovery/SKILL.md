---
name: zero-to-one-product-discovery
description: Use when the user has an early-stage product, app, tool, open-source, startup, or side-project idea without a complete product or runnable MVP, including cases with notes, PRDs, sketches, user feedback, competitor research, or roadmap drafts that still need discovery, feasibility analysis, MVP scoping, planning artifacts, or implementation planning before coding.
---

# Zero-to-One Product Discovery

Use this skill to orchestrate early product discovery from vague idea to implementation readiness without prematurely coding or over-fitting to unvalidated assumptions.

This is the main workflow skill. It controls stage gates, context continuity, child-skill routing, and user experience consistency. Specialist child skills or agents may produce PRDs, Roadmaps, Milestones, ADRs, research briefs, user stories, acceptance criteria, diagrams, implementation plans, or reviews only after this skill provides a bounded handoff and validates that the output is allowed for the current stage.

## Platform Compatibility

This skill is tool-agnostic. Use the host agent's normal file reading, repository inspection, search, and planning tools.

Do not assume a specific runtime such as Codex or Claude Code inside the workflow. Codex-specific UI metadata may live in `agents/openai.yaml`; multi-agent role protocol entrypoints may live in `agents/`; Claude Code can use this `SKILL.md` and `references/` content directly.

## When To Use

Use when the user says or implies:

- "I have a product idea."
- "I want to build an open-source project."
- "I want to build a product from scratch."
- "I have an innovative product concept."
- "Help me plan a side project / app / tool / startup MVP."
- "I have notes / a PRD / sketches / feedback / research, but no runnable MVP yet."

Use this skill even when materials already exist, as long as there is no complete product or runnable MVP. Existing materials should be read, understood, questioned, and upgraded before filling gaps.

## Do Not Use

Do not use by default when the project already has a complete product or runnable MVP. Suggest a future product-improvement workflow instead, unless the user explicitly asks to revisit the product from first principles.

Do not use for narrow bug fixes, small code edits, pure code review, implementation of an already-decided feature, or routine UI polishing.

Do not use for meta-work on this skill, skill authoring, external source integration, license/source-governance questions, installing external skills, or changing this repository's skill architecture. Handle those as skill-maintenance tasks. Do not output Diagnostic Start, Planning Artifacts, child-skill handoffs, readiness signals, or Context Resume Packets for those meta-work requests.

## Core Rules

- Do not ask mature-product questions upfront, such as "Who is the target user?", "What is the MVP?", "What tech stack do you want?", or "What is the business model?"
- Generate candidate interpretations first, then ask the highest-leverage question for the current turn.
- Use a question loop, not a question limit: ask one decisive question per turn, absorb the answer, update facts / assumptions / risks / gaps, then decide whether another decisive question is needed or the stage is grounded enough to proceed.
- Ground every response in the user's actual words, materials, constraints, and stated goals. Do not give generic product advice.
- Keep stages pure. Do not mix later-stage artifacts into early exploration.
- Do not treat user-requested features as product requirements without light demand triage.
- Do not create final PRDs, roadmaps, milestones, ADRs, or implementation plans before the relevant stage is grounded. If the user explicitly requests one before grounding is complete, downgrade to an outline, decision surface, assumption clearing, evidence gap review, or the current highest-leverage blocking question.
- During Planning Artifacts, use local child-skill contracts before producing PRD, Roadmap, Milestones, ADRs, User Stories, Acceptance Criteria, Mermaid diagrams, Research Briefs, Implementation Plans, or Reviews.
- Child skills do not choose the next stage. They return readiness signals; this main skill decides whether to proceed, ask for evidence, downgrade output, or return to an earlier stage.
- Child skills do not call other child skills. They may recommend a next route, but this main workflow performs all routing.
- In multi-agent work, treat the workflow rules as the authority, the Controller Agent as the executor, Producer Agents as bounded artifact creators, and the Auditor Agent as an independent gate. Do not collapse these roles into one unchecked output.
- Use a lightweight Runtime Workbench for current decision state only. Do not store full transcripts, complete artifacts, or long history in the workbench.
- Route core producer work stage-serially by default: Research when evidence must be synthesized, PRD after grounding, Roadmap after PRD readiness, ADR only for durable technical decisions, and Implementation Plan only after review-ready planning artifacts.
- Audit substantial producer output before accepting it as final or review-ready. User-visible audit should be a concise Audit Report, not the auditor's full internal reasoning.
- Treat external command-level mini-hubs as benchmarks unless they are explicitly wrapped by local routing rules.
- Every child-skill handoff must include current stage, confirmed facts, working assumptions, unresolved questions, key risks, existing materials, out-of-scope boundaries, and expected output mode.
- Every substantial child-skill result must return assumptions / unknowns / blockers, Decision Log or ADR candidates, readiness signal, and Context Resume Packet.
- Record meaningful trade-offs in the project Decision Log; architecture-level or long-lived technical decisions need ADRs.
- If the user mentions open-source, resume, portfolio, learning, or public credibility goals, preserve them as evaluation constraints without jumping to Roadmap or implementation.
- If the user provides visual or interaction references during early discovery, acknowledge them as later design inputs but do not analyze them during Diagnostic Start.
- Keep host-specific helper skills or tools invisible unless the user explicitly invokes them. Do not present optional helpers such as `superpowers:*` as required parts of this workflow.
- Treat strong recommendations as candidate directions until the user accepts them. Do not upgrade a suggested segment, MVP angle, or positioning choice into PRD facts before a user gate.
- In PRD Drafts, keep unaccepted target users, MVP scope, positioning, and workflow recommendations explicitly labeled as `candidate`, `assumption`, or `recommended option`. Do not place them in confirmed-fact sections such as Target Users, MVP Scope, or Positioning unless the user has accepted them or provided direct evidence.
- Keep project evidence and runtime packaging separate: promoted `zero-to-one-product-discovery-eval-runs/current/<version>/<run-id>/` records may be committed to the GitHub repository as public validation evidence, but they are never part of the installable skill zip or runtime context.

## Orchestration Model

Use a hub-and-spoke model with lightweight multi-agent roles:

- Main workflow skill: Diagnostic Start, Material Assimilation, Problem Framing, Solution Exploration, Feasibility Discovery, MVP Hypothesis, Planning Artifacts, Implementation Planning.
- Workflow rules: stage gates, downgrade rules, readiness signals, and user-gate criteria.
- Controller Agent: applies workflow rules, builds Agent Work Orders, updates the Runtime Workbench, and decides the next safe action.
- Producer Agents: Research, PRD, Roadmap, ADR, and Implementation Plan producers create bounded artifacts or readiness reviews from controller-provided context.
- Auditor Agent: independently checks boundary compliance, evidence quality, cross-artifact consistency, and whether the output may be accepted, downgraded, or blocked.
- Runtime Workbench: current-state decision board for workflow state, evidence snapshot, artifact status, dependencies, conflicts, risks, audit queue, and next controller action. It is not a historical transcript.
- PM specialist capabilities: Research Brief, PRD, Roadmap, Milestone, positioning, user stories, story mapping, and product critique.
- Engineering governance capabilities: ADR, implementation plan, verification plan, review, and ship-readiness gates.
- Utility capabilities: Acceptance Criteria, Mermaid diagrams, Context Resume Packet, source attribution, and artifact self-review.
- Internal local adapters in `child-skills/`: routeable specialist capability contracts. Ordinary users should experience these as one coherent workflow, not as separate tools.
- Internal upstream source library in `vendor/`: copied source snapshots and licenses used to improve adapter quality. It is never a routing target.

For a quick multi-agent role entrypoint, see `agents/README.md`. For the full protocol, see `references/multi-agent-orchestration.md`.

Preferred quality references:

1. Dean Peters Product-Manager-Skills for PM depth and artifact quality.
2. product-on-purpose pm-skills for skill decomposition, workflow UX, commands, and sample-output discipline.
3. Addy Osmani agent-skills for engineering lifecycle, ADR discipline, verification, review, and ship-readiness.
4. GitHub awesome-copilot for ecosystem discovery and compatibility patterns.

External sources may be referenced or preserved in `vendor/`, but they do not override this skill's stage gates, child-skill contracts, or local evaluation rules.

When the user asks to modify this skill, package this skill, inspect evaluation archives, or integrate external skills, stay in skill-maintenance mode. Give source-governance, packaging, or architecture guidance directly; do not activate product discovery stages. For `vendor/` boundary questions, stop after explaining that `vendor/` is a source snapshot library and local `child-skills/` adapters are the only routeable surface. Do not ask PRD readiness or product-discovery follow-up questions unless the user explicitly pivots back to a product artifact request.

## Exploration Depth

When this skill triggers, default to Diagnostic Start and explicitly mention that deeper modes are available.

Do not stop to make the user choose unless the user asks for options. Proceed with Diagnostic Start by default.

| Mode | Use When | Cost |
|---|---|---|
| Diagnostic Start | The idea is vague, early, or under-specified | Shortest; needs multiple turns to mature |
| Standard Exploration | The user wants structured exploration of problem, solution, and feasibility | Longer response and more context |
| Heavy Advisor | The user explicitly wants full strategic planning artifacts early | Highest context use; longer thinking time; risk of over-structuring assumptions |

Heavy Advisor is not inherently better. It trades context and flexibility for a broader early view.

If the user requests Heavy Advisor but the product domain is still under-specified, simulate multiple child-skill routes as artifact outlines, decision surfaces, and assumption clearings. Label every leaf-level claim as an assumption, decision surface, candidate, or unknown. Do not present complete PRD, Roadmap, Milestones, ADRs, implementation plans, or backlogs as final artifacts.

## Diagnostic Start Output

Keep this stage pure. Do not include candidate users, user scenarios, MVP scope, technology choices, PRD outline, Roadmap, Milestones, or ADR candidates unless the user explicitly asks for a deeper mode.

Prefer concise, information-dense output. For ordinary short prompts, 300-900 Chinese characters is usually enough; exceed that only when the user provides long materials or explicitly asks for a deeper mode. Do not compress away specific facts, risks, or trade-offs just to hit a character target.

Output only:

1. Exploration mode notice.
2. Zero-to-one judgment.
3. Existing material judgment.
4. Facts / assumptions / risks / unknowns.
5. Two or three candidate exploration directions.
6. Most dangerous assumption.
7. The highest-leverage question for this turn and why it matters.

If the user says materials exist but does not provide them, this turn's highest-leverage question may ask the user to provide or identify the material to inspect before continuing.

## Stage Map

Use these stages as a flexible map, not a rigid checklist:

1. Diagnostic Start.
2. Material Assimilation, only if the user provides notes, PRDs, sketches, feedback, research, roadmaps, or requirement lists.
3. Problem Framing.
4. Solution Exploration.
5. Feasibility Discovery.
6. MVP Hypothesis.
7. Planning Artifacts, using child-skill contracts.
8. Implementation Planning, only after review-ready planning artifacts.

User hypotheses are not a standalone mandatory stage. Consider them inside Problem Framing and Solution Exploration only when they materially affect the decision.

## Reference Loading

Load references only when needed:

- `references/workflow.md`: detailed stage flow, stage purity, depth modes, and context resume packets.
- `references/material-assimilation.md`: how to read, challenge, and upgrade existing PRDs, notes, sketches, feedback, research, or roadmap drafts.
- `references/tradeoff-framework.md`: decision dimensions and recording rules for product, technical, design, scope, and roadmap trade-offs.
- `references/planning-artifacts.md`: routing, upgrade, downgrade, Decision Log / ADR escalation, and UX consistency rules for specialist child skills.
- `references/multi-agent-orchestration.md`: Controller / Producer / Auditor roles, Runtime Workbench, Agent Work Order, Agent Return Packet, Audit Report, execution order, user gates, and Trace Report rules.
- `agents/README.md`: quick multi-agent role entrypoint and relationship to `openai.yaml`; use when inspecting repository structure or explaining the role model.
- `agents/multi-agent-orchestration.md`: compact Agent Work Order, Agent Return Packet, Runtime Workbench, and Audit Report templates.
- `references/artifact-adapters.md`: child-skill contracts for PRD, Roadmap, Milestones, ADRs, User Stories, Acceptance Criteria, Mermaid diagrams, Research Briefs, Implementation Plans, and Reviews.
- `references/child-skill-integration-blueprint.md`: external child-skill candidate map, integration modes, install policy, and drift monitoring rules.
- `references/child-skill-wrappers.md`: active local wrappers for Problem Framing, ADR Governance, and Context Handoff.
- `child-skills/`: internal specialist capability modules created from copy-first source review. These are routeable by the main workflow; ordinary users should not need to think about this directory.
- `vendor/`: internal upstream source library containing copied source snapshots, licenses, and attribution material. It is not routeable on its own and should only influence outputs through local child-skill adapters.
- `references/documentation-templates.md`: record-style document structure and templates.
- `references/design-reference-protocol.md`: how to analyze visual, interaction, brand, or website references without copying them.
- `references/source-attribution.md`: external source, license, and adaptation boundary records.

## Handoff

When product direction and design are confirmed, use `superpowers:brainstorming` for design approval if available. After design approval, use `superpowers:writing-plans` for implementation planning if available.
