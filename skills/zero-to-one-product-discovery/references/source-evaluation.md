# Source Evaluation

## Document Purpose

This document evaluates external skill projects as quality references for the `zero-to-one-product-discovery` hub-and-spoke redesign. Copied upstream source snapshots live in `vendor/`, while license and attribution records live in `source-attribution.md`.

## Update Rules

- Append new evaluations when source projects materially change.
- Separate quality judgment from license judgment.
- Record access date, source URL, useful modules, risks, and local integration role.
- Treat external projects as quality sources only; local stage gates and evaluation rules remain authoritative.

## Evaluation Summary

| Rank | Source | Best Role | Quality Judgment | UX Judgment | Local Integration |
|---:|---|---|---|---|---|
| 1 | Product-Manager-Skills | PM depth benchmark | Strongest product-management reasoning and artifact depth | Strong but potentially verbose | Use as quality bar for PRD, Roadmap, discovery, story mapping, positioning, and PM critique |
| 2 | pm-skills | Productized skill UX benchmark | Good artifact coverage and lifecycle breadth | Strongest modular skill/workflow UX | Use for child-skill structure, commands, workflow bundles, sample outputs, and naming discipline |
| 3 | agent-skills | Engineering governance benchmark | Strong engineering lifecycle and gates | Strong for coding-agent workflows | Use for ADR, spec/plan/build/test/review/ship discipline, implementation planning, and verification |
| 4 | awesome-copilot | Ecosystem discovery benchmark | Mixed because it is a broad community collection | Strong discovery and compatibility catalog | Use for compatibility ideas, agent/skill inventory patterns, and Copilot packaging references |

## Source Records

### Product-Manager-Skills

| Field | Evaluation |
|---|---|
| URL | https://github.com/deanpeters/Product-Manager-Skills |
| Accessed Date | 2026-05-06 |
| Observed Shape | A broad product-management skill library with many skills, command workflows, release packaging, and Codex/Claude-oriented install paths. |
| Best Local Use | PM artifact quality benchmark and specialist skill inspiration. |
| Strong Modules To Study | PRD, roadmap, opportunity / discovery, story mapping, user stories, positioning, customer research, PM critique. |
| UX Strength | Strong onboarding and command layer; useful model for "main workflow plus specialist skills". |
| UX Risk | Pedagogic style can be too heavy for users who want concise workflow progress. |
| Boundary Risk | Deep PM content can override the local stage model if copied wholesale. |
| Local Decision | Use as the top PM-depth source. Preserve selected snapshots in `vendor/`, but route only through local child-skill contracts and concise UX rules. |

### pm-skills

| Field | Evaluation |
|---|---|
| URL | https://github.com/product-on-purpose/pm-skills |
| Accessed Date | 2026-05-06 |
| Observed Shape | A productized PM skill system with skills, commands, workflows, templates, sample outputs, validation utilities, and cross-agent setup guidance. |
| Best Local Use | Skill decomposition, workflow UX, command-oriented usage, sample-output discipline, and skill lifecycle governance. |
| Strong Modules To Study | PRD, hypothesis, user stories, acceptance criteria, interview synthesis, experiment design, Mermaid diagrams, workflows, skill validation. |
| UX Strength | Best model for consistent user-facing skill invocation and modular artifact production. |
| UX Risk | Lifecycle phases may not match this repository's zero-to-one stage gates exactly. |
| Boundary Risk | A generic PM lifecycle can dilute the local Diagnostic Start and MVP Hypothesis gates. |
| Local Decision | Use as the primary productized-skill UX source and secondary artifact-quality source. Preserve selected snapshots in `vendor/`, but route only through local adapters. |

### agent-skills

| Field | Evaluation |
|---|---|
| URL | https://github.com/addyosmani/agent-skills |
| Accessed Date | 2026-05-06 |
| Observed Shape | Engineering skills organized around define, plan, build, verify, review, and ship. |
| Best Local Use | Implementation Planning, ADR hygiene, verification, review, and ship-readiness governance. |
| Strong Modules To Study | idea refinement, spec-driven development, planning/task breakdown, TDD, context engineering, source-driven development, review, ship. |
| UX Strength | Clear lifecycle commands and quality gates for coding agents. |
| UX Risk | Can pull the workflow toward engineering before product direction is grounded. |
| Boundary Risk | Engineering artifacts may look authoritative even when product discovery is still unresolved. |
| Local Decision | Use after Planning Artifacts and for technical governance only; do not use to replace product discovery stages. Preserve selected snapshots in `vendor/`, but keep route authority local. |

### awesome-copilot

| Field | Evaluation |
|---|---|
| URL | https://github.com/github/awesome-copilot |
| Accessed Date | 2026-05-06 |
| Observed Shape | A community catalog of Copilot agents, instructions, skills, hooks, workflows, plugins, docs, and machine-readable listings. |
| Best Local Use | Ecosystem discovery, compatibility patterns, and packaging references. |
| Strong Modules To Study | Skill inventory patterns, Copilot instruction patterns, agent organization, workflow cataloging. |
| UX Strength | Broad discoverability and search-oriented catalog experience. |
| UX Risk | Quality varies because it is a broad community collection. |
| Boundary Risk | Interesting examples can create scope creep if adopted without quality review. |
| Local Decision | Use as discovery catalog only, not as a primary artifact-quality source. |

## Integration Guidance

- Keep `zero-to-one-product-discovery` as the main workflow hub.
- Convert local artifact rules into child-skill contracts instead of embedding full templates in `SKILL.md`.
- Use specialist child skills for depth only after the main skill confirms input prerequisites.
- Keep a single UX grammar across all child skills: routing note, assumption labels, one highest-leverage question per turn, readiness signal, Context Resume Packet.
- Use agent-skills-style governance as inspiration for controller / producer / auditor separation, but keep the local multi-agent protocol platform-agnostic and subordinate to `SKILL.md`.
- Keep Runtime Workbench current-state only; use Audit Report or Trace Report for review and retrospective needs.
- Prefer copy-first source preservation plus local quality adaptation: copied upstream material may live in `vendor/`, but user-facing behavior must come through local adapters and main workflow gates.

## Watch Items

- Source projects may change counts, packaging, names, or license terms.
- When vendored source snapshots change, update `source-attribution.md` and `vendor/MANIFEST.md` with exact copied files and notices.
- `child-skills/` now contains local adapter directories. Add or update eval scenarios whenever an adapter becomes routeable or materially changes behavior.
- `references/multi-agent-orchestration.md` is structurally documented but still needs fresh pressure evidence before release-grade claims.
