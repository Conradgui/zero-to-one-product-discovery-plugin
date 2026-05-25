# Zero-to-One Product Discovery Plugin

`zero-to-one-product-discovery-plugin` is a Codex plugin distribution wrapper for the `zero-to-one-product-discovery` workflow skill.

The core capability is still the skill. This repository exists to package that skill as a plugin with a manifest, install boundary, and validation checks, without mixing plugin distribution concerns back into the core workflow source repository.

## What This Plugin Does

This plugin provides a stage-gated AI product discovery workflow for early product, open-source, side-project, and startup ideas.

It is designed to prevent an AI assistant from prematurely producing final PRDs, Roadmaps, ADRs, or Implementation Plans before the problem, evidence, assumptions, risks, and MVP hypothesis are grounded.

The workflow supports:

- Diagnostic Start for vague ideas.
- Material Assimilation for existing notes, PRDs, sketches, feedback, or research.
- Problem Framing, Solution Exploration, Feasibility Discovery, and MVP Hypothesis.
- Planning Artifacts only after readiness gates.
- Implementation Planning only after review-ready planning artifacts.

## Repository Boundary

This repository is the plugin distribution layer.

```text
Core workflow skill
  -> installable skill package
  -> plugin distribution wrapper
  -> future MCP / UI / CLI extension, if needed
```

The bundled skill lives in:

```text
skills/zero-to-one-product-discovery/
```

The plugin manifest lives in:

```text
.codex-plugin/plugin.json
```

## What Is Not Included

This plugin intentionally does not include:

- `zero-to-one-product-discovery-eval-runs/`
- `dist/` release zip history
- temporary publish directories
- historical raw evaluation transcripts
- MCP server configuration
- app UI configuration
- LangGraph or Python runtime

Evaluation evidence should remain in the core project evidence archive. The plugin runtime should stay small and focused.

## Why Plugin Lite

The project started as a workflow skill because the core problem is behavior governance: when an AI agent should ask, downgrade, route, audit, or stop.

The plugin layer adds productized distribution:

- a plugin manifest;
- a clear install boundary;
- Codex plugin metadata;
- package validation;
- room for future MCP or UI extensions if real use cases require them.

It does not replace the skill and does not add fake complexity for presentation.

## Claim Boundary

Supported claim:

- This plugin packages an existing evidence-backed workflow skill for Codex distribution.

Unsupported claims:

- It is not production-grade validation.
- It does not prove cross-model superiority.
- It does not add a service runtime, MCP server, or app UI.
- It does not replace the core `zero-to-one-product-discovery` source repository.

## Validate

Run:

```bash
python3 scripts/validate-plugin-package.py
```

For Codex plugin schema validation, also run the plugin validator from the local `plugin-creator` skill when available:

```bash
python3 /Users/conrad/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/conrad/Desktop/zero-to-one-product-discovery-plugin
```

## Suggested Usage

After installing the plugin in Codex, try:

```text
I have a vague open-source product idea. Use zero-to-one product discovery and do not rush into PRD or code.
```

Or:

```text
Explore my early product idea and identify the riskiest assumptions before planning implementation.
```
