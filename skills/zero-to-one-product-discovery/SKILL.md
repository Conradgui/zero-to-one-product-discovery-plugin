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
- Treat Agent Work Order, Agent Return Packet, Audit Report, Runtime Workbench, Pattern Index, Artifact Manifest, Execution Handoff, Revision Index, and Revision Record schemas in `evals/` as the strict validation layer for release checks and future runtime adapters. Keep Markdown templates as the readable protocol. Treat `evals/controller-actions.json` as the single source of truth for Controller action names.
- The Controller is the only routing authority. Controller action names must come from `evals/controller-actions.json`; do not maintain a separate action enum in docs, schemas, or scripts.
- Producer status values (`ready_for_review`, `ready_for_next_stage`, `needs_more_evidence`, `needs_main_skill_decision`, `blocked`) are signals, not decisions. The Controller maps them to allowed actions after checking stage gates, user gates, and audit requirements.
- Route core producer work stage-serially by default: Research when evidence must be synthesized, PRD after grounding, Roadmap after PRD readiness, ADR only for durable technical decisions, Implementation Plan only after review-ready planning artifacts, Execution Bridge only after a review-ready Implementation Plan, Artifact Export only for accepted/review-ready artifacts with explicit ready/not-ready markers, and Revision Trace only after stable artifacts have been exported.
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
- Persist Runtime Workbench state to `.z2o-state/workbench.json` on every stage transition, substantial artifact acceptance or downgrade, or explicit user save request. Validate the workbench against `evals/workbench.schema.json` before persistence; when file writes are available, use `scripts/persist_workbench.py` for schema validation, evidence-summary consistency checks, and atomic temp-file replace. On new session start, check for persisted state and offer to resume if the state is less than 7 days old. Do not store full artifact text in the persisted state; store only summaries, evidence snapshot, artifact status, and decision log. Exclude `.z2o-state/` from the installable skill zip.
- When the user asks "工作台" / "workbench", show the current-state File Workbench dashboard. When the user asks "导出工作台", route Artifact Export to write `workbench/workbench.md` and `workbench/workbench.json` under `z2o-artifacts/<project-slug>/` while keeping full artifacts outside the workbench.
- When the user asks "导出产物" / "export artifacts" / "生成交付文件", route Artifact Export to create the stable `z2o-artifacts/<project-slug>/` structure. Keep fixed file paths even for missing or not-ready artifacts, but fill them only with `NOT_READY`, blocker, required input, and Controller decision. The manifest must record `source_status`, `content_mode`, and `status_guard` for every artifact entry.
- When the user asks "生成 revision trace" / "artifact diff" / "产物变更记录", route Revision Trace to create a bounded revision ledger under `z2o-artifacts/<project-slug>/revisions/`. Revision Trace may record hashes, unified diffs, section summaries, Controller decision, evidence refs, decision refs, audit refs, and supplied change rationale. It must not store full transcripts, full artifact history, full agent packets, hidden reasoning, or raw prompt history.
- Track evidence maturity using structured items in the workbench state (schema defined in `workflow.md` State Persistence). On every stage transition, append a one-line evidence summary. On user request, show the full Evidence Maturity Dashboard.
- When identifying an assumption, suggest a validation plan (experiment, success criteria, timeline) unless the user explicitly declines. Do not force validation — the suggestion is advisory. Bind the validation plan to the assumption in the workbench state so the dashboard can track it.
- When identifying an assumption, also assess its impact if wrong (low/medium/high/critical) and provide a one-line rationale. Calculate risk_weighted_priority = impact_score × (1 - confidence_score). On user request, show the Risk Map sorted by risk_weighted_priority descending.
- When routing to any Planning Artifact, calculate and show the readiness_score (grounded_inputs / total_required_inputs). Show the Readiness Spectrum with gap analysis and fastest validation path when the user says "readiness" / "准备度" / "还差多少". The readiness score is advisory and does not bypass the Entry Gate.
- On completing Implementation Planning, extract discovery patterns (evidence patterns, decision patterns, stage gate patterns) and save to `.z2o-patterns/`. On starting a new project, check `.z2o-patterns/` for matching patterns and offer to enrich the current discovery context. Pattern matching is advisory — the user decides whether to apply patterns.

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
- Execution capabilities: Execution Bridge for preparing host-executable dry-run handoffs from Implementation Plans into GitHub Issues first, plus Claude Code task and Jira ticket formats. Z2O does not directly create external issues or tickets.
- Export capabilities: Artifact Export for stable PRD / Roadmap / User Stories / Implementation Plan files, File Workbench views, and Execution Bridge handoff files under `z2o-artifacts/<project-slug>/`.
- Revision capabilities: Revision Trace for bounded artifact hashes, diffs, section summaries, and Controller-linked rationale under `z2o-artifacts/<project-slug>/revisions/`. Full trace UI and runtime history stores remain future LangGraph/runtime scope.
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

### Quick Mode

Quick Mode is an independent mode switch, not a depth level. It can be activated at any stage.

Use when the user says "快速模式", "Quick Mode", "直接出 PRD", "直接给我 draft", or when the system detects that the user has provided sufficient materials (complete PRD draft, detailed notes, competitor analysis, etc.) and the user confirms.

Quick Mode skips interactive exploration loops and produces draft artifacts with explicit evidence labels:

- Output format: `[Quick Mode Draft]`
- Every section is labeled `[Fact]`, `[Assumption]`, or `[Unknown]`
- Ends with an Evidence Gap Summary listing missing evidence and suggested validation paths, ordered by priority (most urgent validation first)
- Skipped stages are marked as "unverified" in the gap summary, not "completed"

After receiving a Quick Mode draft, the user may say "给我一份 evidence assessment" to receive a standalone assessment table (dimension / status / explanation / suggested validation path). This is optional — the user is not forced to read an assessment before seeing the draft.

Quick Mode cannot produce unlabeled final artifacts. It cannot skip the Auditor's evidence check (simplified to inline check). It cannot be used for Implementation Planning. It cannot reopen product strategy decisions that were already accepted in a previous stage.

If a Quick Mode draft is exported before the user returns to Standard Exploration and validates it, the exported artifact must keep a top `QUICK_MODE_DRAFT` marker and the manifest entry must use `content_mode: quick_mode_draft` with `status_guard: quick_mode_banner_required`. Do not present it as final or accepted.

To exit Quick Mode, say "回到标准模式" or "回到探索". The workflow resumes from the stage before Quick Mode was activated.

### Evidence Maturity Dashboard

The Evidence Maturity Dashboard gives the user a real-time view of evidence verification progress.

Show the dashboard when the user says "evidence dashboard" / "证据成熟度" / "evidence 状态" / "给我看 dashboard".

On every stage transition, append a one-line evidence summary without expanding the full dashboard: `[Evidence: X facts, Y assumptions, Z unknowns, W risks | Maturity: <level> (<percentage>%)]`

Maturity calculation: only verified facts count as mature. `maturity_percentage = verified_facts / total_evidence_items × 100`. Display with four-level labels: Insufficient (<25%), Partial (25-50%), Sufficient (50-75%), Strong (>75%). Format: `Evidence Maturity: Partial (42%)`.

The dashboard is read-only. It does not modify evidence state. It does not replace the one-question-per-turn rule. Unverified assumptions are never counted as "mature" even if accepted by the user.

### File Workbench

The File Workbench is the user-facing current-state dashboard for day-to-day use.

Show it when the user says "工作台" / "workbench" / "当前状态". Export it when the user says "导出工作台".

Required sections:

- Workflow state.
- Next controller action.
- Evidence maturity.
- Risk map.
- Readiness spectrum.
- Artifact status.
- Audit queue.
- Blockers.
- Skipped stages.

Exported views live under `z2o-artifacts/<project-slug>/workbench/`:

- `workbench.md` for human reading.
- `workbench.json` for machine-readable current state.
- `evidence-dashboard.md`, `risk-map.md`, and `readiness-spectrum.md` for focused views.

The File Workbench may reference artifact paths and one-line summaries. It must not store full transcripts, full artifact bodies, complete Agent Work Orders, complete Agent Return Packets, complete Audit Reports, or long history.

### Revision Trace

Revision Trace is a bounded ledger for exported artifact changes.

Show or generate it when the user says "生成 revision trace" / "artifact diff" / "产物变更记录" / "产物版本记录".

Revision material lives outside Workbench:

- `revisions/revision-index.json`
- `revisions/revision-log.md`
- `revisions/records/<revision-id>.json`
- `revisions/diffs/<revision-id>/*.diff`

Compare only stable artifact files: `prd.md`, `roadmap.md`, `user-stories.md`, and `implementation-plan.md`. Do not create `prd-v1.md`, `prd-v2.md`, `final-final.md`, or any versioned replacement for stable artifact paths.

Revision Trace may record mechanical hashes, unified diffs, Markdown heading summaries, Controller decision, evidence refs, decision refs, audit refs, and Controller-supplied change rationale. It must not infer semantic rationale from text diffs. Missing metadata is recorded as `change_reason_status: missing`.

Revision count is not evidence maturity, readiness, or quality. Workbench, manifest, artifact status, Controller decision, and evidence refs remain authoritative.

### Risk Map

The Risk Map shows assumptions sorted by impact if wrong, helping the user prioritize which assumptions to validate first.

Show the risk map when the user says "risk map" / "风险地图" / "哪些假设最危险" / "先验证什么".

Each assumption has an `impact_if_wrong` level (low/medium/high/critical) and a `risk_weighted_priority` score. The risk map displays items sorted by risk_weighted_priority descending, with a recommended validation order.

PRD artifacts automatically include a Risk Map at the end. The risk map does not replace the one-question-per-turn rule.

The risk map is read-only. It does not modify evidence state.

### Pattern Library

The Pattern Library stores discovery patterns from completed projects and applies them to new projects.

**Pattern extraction**: On completing Implementation Planning, extract three types of patterns from the current project:
- **Evidence patterns**: which evidence items were validated, which assumptions were confirmed/invalidated, which evidence combinations appeared frequently
- **Decision patterns**: which trade-offs were made, what rationale was used, which decision patterns repeat
- **Stage gate patterns**: what evidence maturity level each stage passed at, which inputs were on the critical path

Save extracted patterns to `.z2o-patterns/pattern-index.json`.

**Pattern matching**: On starting a new project (Diagnostic Start), check `.z2o-patterns/` for matching patterns based on the user's initial description. If a match is found, show: "发现相似项目 pattern：[项目名]。是否参考其 evidence/decision/stage gate pattern？" The user decides whether to apply.

**Restrictions**:
- Pattern matching is advisory. The user decides whether to apply patterns.
- Patterns do not bypass stage gates or the Entry Gate.
- Patterns are project-local (`.z2o-patterns/` directory, not in the installable skill zip).
- Patterns do not contain full artifact text — only metadata and structure.

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
2. Material Assimilation, only if the user provides notes, PRDs, sketches, feedback, research, roadmaps, or requirement lists. Offers Express Review option for batch-accepting extraction results.
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
- `evals/*-schema.json`: strict contract schemas for Agent Work Order, Agent Return Packet, Audit Report, Runtime Workbench, Pattern Index, Artifact Manifest, Execution Handoff, Revision Index, Revision Record, and eval report files. Use for release checks or future executable runtime adapters; ordinary chat can stay Markdown-first.
- `evals/controller-actions.json`: Controller action registry. Load when adding, renaming, validating, or documenting Controller actions.
- `scripts/persist_workbench.py` and `scripts/generate_revision_trace.py`: standard-library file helpers for atomic Workbench persistence and bounded revision ledger generation when the host can write files.
- `references/artifact-adapters.md`: child-skill contracts for PRD, Roadmap, Milestones, ADRs, User Stories, Acceptance Criteria, Mermaid diagrams, Research Briefs, Implementation Plans, Reviews, Execution Bridge, Artifact Export, and Revision Trace.
- `references/child-skill-integration-blueprint.md`: external child-skill candidate map, integration modes, install policy, and drift monitoring rules.
- `references/child-skill-wrappers.md`: active local wrappers for Problem Framing, ADR Governance, and Context Handoff.
- `child-skills/`: internal specialist capability modules created from copy-first source review. These are routeable by the main workflow; ordinary users should not need to think about this directory.
- `vendor/`: internal upstream source library containing copied source snapshots, licenses, and attribution material. It is not routeable on its own and should only influence outputs through local child-skill adapters.
- `references/documentation-templates.md`: record-style document structure and templates.
- `references/design-reference-protocol.md`: how to analyze visual, interaction, brand, or website references without copying them.
- `references/source-attribution.md`: external source, license, and adaptation boundary records.
- `.z2o-state/workbench.json`: persisted Runtime Workbench state from previous sessions. Load on new session start to check for resumable discovery context. If absent or older than 7 days, start fresh.
- `.z2o-patterns/pattern-index.json`: cross-project discovery pattern library. Load on Diagnostic Start to check for matching patterns from completed projects. If absent, skip pattern matching.

## Handoff

When product direction and design are confirmed, use `superpowers:brainstorming` for design approval if available. After design approval, use `superpowers:writing-plans` for implementation planning if available.
