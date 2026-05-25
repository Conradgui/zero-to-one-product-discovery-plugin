# Vendor Manifest

This directory contains copied upstream source snapshots for copy-first child-skill integration.

Vendored files are source material, not active workflow routes. Active routes live under
`../child-skills/` and must preserve the main `zero-to-one-product-discovery` stage gates.

## Sources

| Source | Upstream URL | License | Vendored Scope |
|---|---|---|---|
| Product-Manager-Skills | https://github.com/deanpeters/Product-Manager-Skills | CC BY-NC-SA 4.0 | Selected PM skills for problem framing, JTBD, PRD, roadmap, story mapping, and user stories |
| agent-skills | https://github.com/addyosmani/agent-skills | MIT | Selected engineering governance skills for context, ADRs, planning, review, and TDD |
| pm-skills | https://github.com/product-on-purpose/pm-skills | Apache-2.0 | Selected artifact skills and command wrappers for PRD, user stories, acceptance criteria, ADR, interview synthesis, and Mermaid |
| awesome-copilot | https://github.com/github/awesome-copilot | MIT | Narrow ADR and implementation-plan references only |

## Boundary Rules

- Do not execute vendored command wrappers directly from the main workflow.
- Do not expose vendored source as a child route without a local adapter in `../child-skills/`.
- Do not let vendored source override local grounding, readiness, or UX rules.
- Preserve upstream license files and source attribution whenever copied files are updated.

