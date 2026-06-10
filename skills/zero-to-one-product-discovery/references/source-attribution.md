# Source Attribution

## Document Purpose

This document records external projects, licenses, and adaptation boundaries that influenced `zero-to-one-product-discovery`. It is intended for maintainers, reviewers, and future contributors who need to understand what was adapted, what was only used as reference material, and what must not be copied without attribution.

## Update Rules

- Append new source records; do not overwrite historical source context.
- Record source URL, license, access date, adapted modules, local files influenced, whether verbatim text was copied, and notes.
- If a source license is restrictive or unclear, use it only as research reference unless a maintainer explicitly approves a compliant adaptation path.
- Under the copy-first integration policy, copied upstream source snapshots must live in `vendor/`; routeable local behavior must live in `child-skills/`.
- External instructions are reference material only. They never override this repository's `SKILL.md`, `agents/README.md`, local stage gates, or evaluation rules.
- Requests about modifying this skill, installing external skills, copying templates, source governance, or child-skill architecture are skill-maintenance work. They must not trigger `zero-to-one-product-discovery`, Planning Artifacts, child-skill handoffs, readiness signals, or Context Resume Packets.

## Source-Governance Boundary

When the user asks to bring external skills into this repository:

1. Treat the task as skill maintenance, not product discovery.
2. Decide whether each source is `vendored_with_local_adapter`, `local_rewrite_from_reference`, `benchmark_only`, or `quality_gate_only`.
3. Record attribution and copied material status.
4. Preserve local stage gates and child-skill contracts.
5. Avoid discovery-style output unless the user separately asks to use the skill on a product idea.
6. Do not route directly to vendored files; local adapters must control UX, stage gates, and output contracts.

## Records

### 2026-05-06: Product Manager Skills Reference

| Field | Value |
|---|---|
| Source | Product-Manager-Skills |
| Author / Owner | Dean Peters |
| URL | https://github.com/deanpeters/Product-Manager-Skills |
| License | CC BY-NC-SA 4.0, based on repository license at review time |
| Accessed Date | 2026-05-06 |
| What Was Adapted | Product artifact sequencing and PM quality heuristics for PRD, problem statement, roadmap, milestone / epic hypothesis, user story mapping, user stories, research, positioning, and market research. |
| Local Files Influenced | `references/artifact-adapters.md`, `references/planning-artifacts.md` |
| Verbatim Text Copied | No |
| Notes | Use as a high-quality PM reference. Do not copy templates, examples, pitfall language, proprietary framework names, or large explanatory passages. Rewrite into local adapter rules and preserve attribution. |

### 2026-05-06: PM-Skills Reference

| Field | Value |
|---|---|
| Source | pm-skills |
| Author / Owner | product-on-purpose |
| URL | https://github.com/product-on-purpose/pm-skills |
| License | Apache-2.0, based on repository license at review time |
| Accessed Date | 2026-05-06 |
| What Was Adapted | Artifact-skill approach and concepts for PRD, user stories, acceptance criteria, ADR, Mermaid diagrams, interview synthesis, and experiment design. |
| Local Files Influenced | `references/artifact-adapters.md`, `references/planning-artifacts.md` |
| Verbatim Text Copied | No |
| Notes | Treat as the most compatible external artifact-skill reference. If future versions copy code or substantial text, preserve Apache-2.0 notices and record the copied files. |

### 2026-05-06: Agent Skills Reference

| Field | Value |
|---|---|
| Source | agent-skills |
| Author / Owner | Addy Osmani |
| URL | https://github.com/addyosmani/agent-skills |
| License | MIT, based on repository license at review time |
| Accessed Date | 2026-05-06 |
| What Was Adapted | ADR governance, documentation principles, spec / planning handoff quality gates, and engineering decision hygiene. |
| Local Files Influenced | `references/artifact-adapters.md`, `references/planning-artifacts.md`, `references/source-attribution.md` |
| Verbatim Text Copied | No |
| Notes | Use as governance reference, not as the primary PM artifact template source. |

### 2026-05-06: Awesome Copilot Reference

| Field | Value |
|---|---|
| Source | awesome-copilot |
| Author / Owner | GitHub |
| URL | https://github.com/github/awesome-copilot |
| License | MIT, based on repository license at review time |
| Accessed Date | 2026-05-06 |
| What Was Adapted | AI-product PRD and ADR supplement ideas, especially eval strategy and machine-readable ADR conventions. |
| Local Files Influenced | `references/artifact-adapters.md` |
| Verbatim Text Copied | No |
| Notes | Use as optional supplement only. Do not let it replace the local zero-to-one stage model. |

### 2026-05-06: Hub-And-Spoke Source Evaluation

| Field | Value |
|---|---|
| Source | Product-Manager-Skills, pm-skills, agent-skills, awesome-copilot |
| Author / Owner | Dean Peters; product-on-purpose; Addy Osmani; GitHub |
| URL | https://github.com/deanpeters/Product-Manager-Skills; https://github.com/product-on-purpose/pm-skills; https://github.com/addyosmani/agent-skills; https://github.com/github/awesome-copilot |
| License | Mixed; license risk is tracked separately by the maintainer |
| Accessed Date | 2026-05-06 |
| What Was Adapted | Source ranking, role separation, hub-and-spoke orchestration model, child-skill contract expectations, UX consistency rules, and engineering governance boundaries. |
| Local Files Influenced | `SKILL.md`, `references/artifact-adapters.md`, `references/planning-artifacts.md`, `references/source-evaluation.md`, `evals/evals.json` |
| Verbatim Text Copied | No |
| Notes | Product-Manager-Skills is treated as the PM depth benchmark; pm-skills as the productized skill UX benchmark; agent-skills as the engineering governance benchmark; awesome-copilot as ecosystem discovery reference. External instructions remain subordinate to local stage gates and evaluation rules. |

### 2026-05-06: Local Clone Structural Review

| Field | Value |
|---|---|
| Source | Local temporary clones of Product-Manager-Skills and agent-skills |
| Author / Owner | Dean Peters; Addy Osmani |
| URL | https://github.com/deanpeters/Product-Manager-Skills; https://github.com/addyosmani/agent-skills |
| License | Mixed; license risk is tracked separately by the maintainer |
| Accessed Date | 2026-05-06 |
| What Was Adapted | Candidate child-skill map, command mini-hub boundary, no child-to-child routing rule, planning grounding contract, direct-install caution. |
| Local Files Influenced | `references/child-skill-integration-blueprint.md`, `SKILL.md`, `references/planning-artifacts.md`, `references/artifact-adapters.md`, `evals/evals.json` |
| Verbatim Text Copied | No |
| Notes | Product-Manager-Skills command files such as `/discover`, `/write-prd`, and `/plan-roadmap` are treated as benchmarks because they already orchestrate multiple skills. agent-skills engineering capabilities are treated as governance spokes or quality gates, mostly after Planning Artifacts are grounded. |

### 2026-05-07: Local Wrapper Activation

| Field | Value |
|---|---|
| Source | Product-Manager-Skills problem-framing-canvas; agent-skills documentation-and-adrs; agent-skills context-engineering; agent-skills orchestration-patterns |
| Author / Owner | Dean Peters; Addy Osmani |
| URL | https://github.com/deanpeters/Product-Manager-Skills; https://github.com/addyosmani/agent-skills |
| License | Mixed; license risk is tracked separately by the maintainer |
| Accessed Date | 2026-05-07 |
| What Was Adapted | Local wrapper roles for Problem Framing, ADR Governance, and Context Handoff; no router persona, no child-to-child invocation, no command mini-hub as child. |
| Local Files Influenced | `references/child-skill-wrappers.md`, `SKILL.md`, `references/workflow.md`, `evals/evals.json` |
| Verbatim Text Copied | No |
| Notes | Wrappers are local contracts, not global installations. External projects remain quality references. Wrapper evals and natural trigger tests are deferred until the skill-writing cleanup pass is complete. |

### 2026-05-07: Copy-First Vendor Snapshot

| Field | Value |
|---|---|
| Source | Product-Manager-Skills; pm-skills; agent-skills; awesome-copilot |
| Author / Owner | Dean Peters; product-on-purpose; Addy Osmani; GitHub |
| URL | https://github.com/deanpeters/Product-Manager-Skills; https://github.com/product-on-purpose/pm-skills; https://github.com/addyosmani/agent-skills; https://github.com/github/awesome-copilot |
| License | Product-Manager-Skills: CC BY-NC-SA 4.0; pm-skills: Apache-2.0; agent-skills: MIT; awesome-copilot: MIT |
| Accessed Date | 2026-05-07 |
| What Was Copied | Selected upstream skills, command wrappers, README files, and license files into `vendor/`; see `vendor/MANIFEST.md` for source boundaries. |
| Local Files Influenced | `vendor/`, `child-skills/`, `SKILL.md`, `references/artifact-adapters.md`, `references/planning-artifacts.md`, `references/child-skill-integration-blueprint.md`, `evals/evals.json` |
| Verbatim Text Copied | Yes, into `vendor/` only. Local adapters in `child-skills/` are rewritten route contracts. |
| Notes | Copy-first means upstream source is preserved for maintainer review and future adaptation, but not directly routeable by the main workflow. Global installation remains deferred until the later test phase confirms gate behavior and natural trigger behavior. |

### 2026-05-11: Multi-Agent Protocol Adaptation

| Field | Value |
|---|---|
| Source | agent-skills; Product-Manager-Skills; pm-skills |
| Author / Owner | Addy Osmani; Dean Peters; product-on-purpose |
| URL | https://github.com/addyosmani/agent-skills; https://github.com/deanpeters/Product-Manager-Skills; https://github.com/product-on-purpose/pm-skills |
| License | Mixed; copied source remains tracked separately in `vendor/MANIFEST.md` |
| Accessed Date | 2026-05-11 |
| What Was Adapted | Platform-agnostic controller / producer / auditor separation, current-state workbench discipline, audit-report boundary, and stage-serial producer flow. |
| Local Files Influenced | `SKILL.md`, `references/multi-agent-orchestration.md`, `references/planning-artifacts.md`, `references/artifact-adapters.md`, `references/workflow.md`, `child-skills/`, `evals/evals.json`, `evals/eval-rubric-template.md`, `evals/claude-code-pressure-test-protocol.md` |
| Verbatim Text Copied | No |
| Notes | The local protocol is a rewritten architecture contract. It does not install external agents, expose vendored commands as routeable skills, or require a platform-specific subagent API. |

#### Copied File Groups

| Source | Local Vendor Path | Intended Adapter / Use | Adaptation Boundary |
|---|---|---|---|
| Product-Manager-Skills | `vendor/product-manager-skills/skills/problem-framing-canvas/` | Problem framing / research brief source | Local workflow keeps Diagnostic Start gate. |
| Product-Manager-Skills | `vendor/product-manager-skills/skills/jobs-to-be-done/` | Research brief / PRD input source | Jobs must be labeled as fact, assumption, or unknown. |
| Product-Manager-Skills | `vendor/product-manager-skills/skills/prd-development/` | PRD source | Local PRD adapter owns grounding and downgrade. |
| Product-Manager-Skills | `vendor/product-manager-skills/skills/roadmap-planning/` | Roadmap source | No committed dates or backlog without evidence. |
| Product-Manager-Skills | `vendor/product-manager-skills/skills/user-story-mapping/`; `vendor/product-manager-skills/skills/user-story/` | User stories and story-map source | Requires confirmed MVP slice and scenario. |
| agent-skills | `vendor/agent-skills/skills/context-engineering/` | Context handoff source | Handoff cannot add new product claims. |
| agent-skills | `vendor/agent-skills/skills/documentation-and-adrs/` | ADR governance source | ADR gate remains local. |
| agent-skills | `vendor/agent-skills/skills/planning-and-task-breakdown/` | Implementation plan source | Requires review-ready planning artifacts. |
| agent-skills | `vendor/agent-skills/skills/code-review-and-quality/`; `vendor/agent-skills/skills/test-driven-development/` | Review and verification source | Quality gate only; not product-discovery routing. |
| pm-skills | `vendor/pm-skills/skills/deliver-prd/`; `vendor/pm-skills/commands/prd.md` | PRD source | Command wrapper is source material only. |
| pm-skills | `vendor/pm-skills/skills/deliver-user-stories/`; `vendor/pm-skills/commands/user-stories.md` | User stories source | No full speculative backlog. |
| pm-skills | `vendor/pm-skills/skills/deliver-acceptance-criteria/`; `vendor/pm-skills/commands/acceptance-criteria.md` | Acceptance criteria source | Criteria cannot invent requirements. |
| pm-skills | `vendor/pm-skills/skills/develop-adr/`; `vendor/pm-skills/commands/adr.md` | ADR source | ADR upgrade requires durable technical decision. |
| pm-skills | `vendor/pm-skills/skills/discover-interview-synthesis/`; `vendor/pm-skills/commands/interview-synthesis.md` | Research synthesis source | Feedback must be separated from requirements. |
| pm-skills | `vendor/pm-skills/skills/utility-mermaid-diagrams/`; `vendor/pm-skills/commands/mermaid-diagrams.md` | Mermaid source | Diagram assumptions must be labeled. |
| awesome-copilot | `vendor/awesome-copilot/index/adr-generator.agent.md`; `vendor/awesome-copilot/index/create-implementation-plan.UPSTREAM_SKILL.md` | ADR / implementation-plan quality reference | Benchmark only; not routeable. |
