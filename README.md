# Zero-to-One Product Discovery Plugin

A Codex plugin for early-stage product discovery with stage-gated workflow, multi-agent governance, evidence maturity tracking, artifact export, and revision trace.

## What It Does

This plugin wraps the [`zero-to-one-product-discovery`](https://github.com/Conradgui/zero-to-one-product-discovery) workflow skill as a Codex plugin. It helps agents handle early product, open-source, side-project, and startup ideas through evidence-aware stage gates instead of prematurely producing PRDs, roadmaps, ADRs, or implementation plans.

Core workflow:

1. **Diagnostic Start** — evaluate the idea: facts, assumptions, risks, unknowns.
2. **Material Assimilation** — absorb existing notes, PRDs, sketches, feedback, research.
3. **Problem Framing** — define the problem space with grounded evidence.
4. **Solution Exploration** — explore candidate solutions and trade-offs.
5. **Feasibility Discovery** — assess technical and product feasibility.
6. **MVP Hypothesis** — form a testable MVP hypothesis.
7. **Planning Artifacts** — produce PRD, Roadmap, User Stories, ADRs (only when evidence is sufficient).
8. **Implementation Planning** — engineering plan with verification strategy.
9. **Artifact Export** — stable file package with manifest and readiness markers.
10. **Revision Trace** — bounded artifact change ledger.

## Components

### Skills

- `zero-to-one-product-discovery` — main workflow skill with stage gates, Quick Mode, Evidence Maturity Dashboard, Risk Map, Readiness Spectrum, Pattern Library, and Auto-Persist.

### Child Skills (14 adapters)

| Child Skill | Purpose |
|---|---|
| `research-brief` | Synthesize interviews, feedback, competitors, notes |
| `prd` | Produce PRD with Risk Map and Readiness Spectrum |
| `roadmap` | Now/Next/Later roadmap with validation gates |
| `user-stories` | User stories, story mapping, release slices |
| `acceptance-criteria` | Acceptance criteria for confirmed requirements |
| `adr-governance` | Decision Log vs ADR for durable technical decisions |
| `mermaid` | Mermaid diagrams from known structure |
| `implementation-plan` | Engineering plan from review-ready artifacts |
| `review` | Multi-perspective artifact review |
| `context-handoff` | Context Resume Packet for session continuity |
| `execution-bridge` | Implementation Plan → GitHub Issues / Claude Code tasks / Jira tickets |
| `artifact-export` | Stable file export with manifest and NOT_READY markers |
| `revision-trace` | Bounded artifact revision ledger with hashes and diffs |

### Eval Schemas (19 contracts)

JSON Schema contracts for Agent Work Order, Agent Return Packet, Audit Report, Runtime Workbench, Pattern Index, Artifact Manifest, Execution Handoff, Revision Index, Revision Record, eval reports, and Value Review.

### Scripts

| Script | Purpose |
|---|---|
| `persist_workbench.py` | Schema-validated atomic Workbench persistence |
| `generate_revision_trace.py` | Deterministic revision ledger generation |
| `validate-contracts.py` | Release-check contract and packaging validation |
| `validate-plugin-package.py` | Plugin package structure and manifest validation |

## Install

### From Codex Plugin Directory

Open Codex → Plugins → Browse → search for "Zero-to-One Product Discovery" → Install.

### From Git Repository

Add this repository as a Git-backed marketplace source:

```json
{
  "name": "zero-to-one-product-discovery-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/Conradgui/zero-to-one-product-discovery-plugin.git",
    "path": "./",
    "ref": "main"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

### Manual Local Install

```bash
# Clone the plugin
git clone https://github.com/Conradgui/zero-to-one-product-discovery-plugin.git

# Copy to Codex plugins directory
mkdir -p ~/.codex/plugins
cp -R zero-to-one-product-discovery-plugin ~/.codex/plugins/zero-to-one-product-discovery-plugin
```

Restart Codex after installation.

## Configure

This plugin requires no external configuration, API keys, or environment variables. It operates entirely through the host agent's built-in file reading, search, and planning tools.

No MCP servers, App connectors, or Hooks are bundled.

## Use

### Basic Usage

After installation, trigger the skill naturally:

```text
我有一个很模糊的开源产品想法。请使用 zero-to-one product discovery，不要急着写 PRD 或代码。
```

Or in English:

```text
Explore my early product idea without rushing into PRD.
```

### Quick Mode

If you have sufficient materials (complete PRD draft, detailed notes, competitor analysis):

```text
我有一份详细的 PRD 草稿，直接进入快速模式帮我审查并补全。
```

### Evidence Dashboard

View evidence verification progress:

```text
evidence dashboard
给我看证据成熟度
```

### Risk Map

See which assumptions are most dangerous:

```text
risk map
哪些假设最危险
```

### Readiness Spectrum

Check distance to PRD/roadmap readiness:

```text
readiness
准备度
还差多少
```

### Artifact Export

Export stable artifact files:

```text
导出产物
export artifacts
```

### Revision Trace

Generate artifact change ledger:

```text
生成 revision trace
产物变更记录
```

## Security

### Read/Write Scope

- **Read**: This plugin reads user-provided materials (notes, PRDs, sketches, feedback, research) through the host agent's file reading tools.
- **Write**: This plugin may create files in the user's project workspace when exporting artifacts (`z2o-artifacts/`), persisting workbench state (`.z2o-state/`), or saving patterns (`.z2o-patterns/`).

### No External Network Calls

This plugin does not make external API calls, telemetry, analytics, or network requests. All processing is local through the host agent.

### No Credentials

This plugin does not require, store, or transmit API keys, tokens, or credentials.

### Hook Safety

No hooks are bundled. If hooks are added in the future, they will use `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` for path resolution and will not perform silent network calls, install dependencies, or modify user files without explicit trust.

### Artifact Boundaries

- Exported artifacts with insufficient evidence are marked `NOT_READY`, not fabricated.
- Quick Mode drafts retain `QUICK_MODE_DRAFT` markers and cannot be exported as final.
- The Revision Trace stores only bounded metadata (hashes, diffs, section summaries), never full transcripts or hidden reasoning.

## Troubleshooting

### Skill not triggering

- Ensure the plugin is installed and enabled in Codex → Plugins.
- Restart Codex after installation.
- Check that `skills/zero-to-one-product-discovery/SKILL.md` exists in the plugin directory.

### Skill triggers but stages seem skipped

- This is by design for Quick Mode. Say "回到标准模式" to return to interactive exploration.
- If not in Quick Mode, the skill enforces stage gates — provide more evidence to proceed.

### Artifact export produces NOT_READY files

- This is expected when evidence is insufficient. Review the Evidence Maturity Dashboard (`evidence dashboard`) to see what's missing.
- Provide additional materials or answer key questions to advance readiness.

### Workbench state not persisting

- Ensure the host agent has file write permissions.
- Check that `.z2o-state/workbench.json` is not blocked by `.gitignore` or permissions.

### Validation script fails

```bash
python scripts/validate-plugin-package.py
```

Common issues:
- Missing `assets/icon.png` or `assets/logo.png`.
- Invalid `plugin.json` structure.
- Forbidden content detected (eval-runs, dist, publish directories).

## Repository Structure

```text
zero-to-one-product-discovery-plugin/
├── .codex-plugin/
│   └── plugin.json                          # Plugin manifest
├── assets/
│   ├── icon.png                             # Composer icon
│   └── logo.png                             # Plugin logo
├── scripts/
│   ├── validate-plugin-package.py           # Plugin package validator
│   └── generate_assets.py                   # Asset generation helper
├── skills/
│   └── zero-to-one-product-discovery/       # Bundled skill
│       ├── SKILL.md                         # Main workflow
│       ├── README.md                        # Skill documentation
│       ├── agents/                          # Multi-agent protocol
│       ├── child-skills/                    # 14 specialist adapters
│       ├── references/                      # Workflow rules and protocols
│       ├── evals/                           # 19 JSON Schema contracts
│       ├── scripts/                         # Python helper scripts
│       └── vendor/                          # Upstream source snapshots
├── README.md                                # This file
├── CHANGELOG.md                             # Version history
└── LICENSE                                  # MIT License
```

## Source Transparency

The bundled skill originates from [`zero-to-one-product-discovery`](https://github.com/Conradgui/zero-to-one-product-discovery). This plugin repository is the distribution wrapper only. Core workflow behavior changes happen in the source repository first, then sync to this plugin.

`vendor/` contains upstream source snapshots with mixed licenses (CC BY-NC-SA 4.0, Apache-2.0, MIT). See `vendor/MANIFEST.md` and `references/source-attribution.md` for details.

## License

MIT — see [LICENSE](LICENSE).
