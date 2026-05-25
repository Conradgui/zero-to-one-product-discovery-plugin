# AI Product Discovery Workflow Skill with Multi-Agent Governance and Quantitative Evals

`zero-to-one-product-discovery` 是一个面向早期产品想法的 AI workflow skill：从一句模糊想法开始，逐步完成问题澄清、材料吸收、MVP 假设、规划产物和实施准备。

它适合个人开源项目、作品集项目、内部工具、side project 和 startup MVP 的早期探索。核心目标不是“快速套一个 PRD 模板”，而是防止 AI 在证据不足时过早进入 PRD、Roadmap、ADR 或编码阶段。

> Status: `v0.2.1 Portfolio Release`。这是可安装、可展示的作品集版本：已完成多 agent workflow、stage gates、评测协议、Windows relay evidence 和 baseline A/B evidence；仍不声明 release-grade validation、production stability 或跨模型全面优越性。

## Highlights

- **Stage-gated workflow**：由 `SKILL.md` 控制阶段门禁、上下文连续性、子能力路由和最终输出验收。
- **Multi-agent governance**：Workflow 规则负责阶段门禁，Controller Agent 负责路由，Producer Agents 负责产物，Auditor Agent 负责独立审核，Runtime Workbench 只保存当前决策状态。
- **Quantitative evals**：包含 strict suite、Windows relay、targeted rerun、Baseline A/B、hard failures、Value Gate 和机器可读 schema。
- **中文优先体验**：默认面向中文产品探索和协作场景，同时保留英文 artifact 名称以兼容常见 PM / engineering 术语。
- **一轮一个关键问题**：每轮只问当前最高杠杆问题；用户回答后再更新 facts / assumptions / risks / gaps。
- **防止过早产物化**：信息不足时只能输出 outline、decision surface、evidence gap 或 blocking question，不能伪造成最终 PRD。
- **专业子能力**：PRD、Roadmap、User Stories、Acceptance Criteria、ADR、Mermaid、Implementation Plan 等由本地 child skill adapter 承担。

## Evaluation Dashboard

| Evidence | Scenarios | Result | Hard failures | What It Supports |
|---|---:|---|---:|---|
| `v0.1.5` full strict suite | 22 | 22/22 pass, avg 93.73, lowest 90 | 0 | Core trigger, stage-gate, boundary, audit, context-economy regression confidence |
| `v0.1.6` Windows relay | 8 | 8 pass | 0 | Clean-install relay surfaced Windows/package/runtime-context issues |
| `v0.1.7` targeted rerun | 5 | 4 pass, 1 partial, avg 89 | 0 | Confirmed maintenance and helper-skill drift fixes; found final user-gate/doc gaps |
| `v0.1.9` Baseline A/B | 10 paired | skill avg 95.7 vs baseline avg 68.4, delta +27.3 | 0 skill hard failures | Scenario-scoped improvement in stage gates, boundary safety, and user-gate behavior |

Supported claim: this project has evidence-backed workflow governance for the tested early product discovery scenarios.

Unsupported claim: this is not release-grade validation, production-stability proof, cross-model superiority, or long-term real-user validation.

Portfolio case study: see the repository root file [`PORTFOLIO-CASE-STUDY.md`](../PORTFOLIO-CASE-STUDY.md) on GitHub.

## When To Use

适合：

- 只有一个初步产品、工具、开源项目或 startup 想法。
- 已有笔记、PRD 草稿、用户反馈、竞品研究或路线图，但缺少系统化发现过程。
- 想先确认问题、用户场景、MVP、风险、非目标和成功标准，再进入开发。
- 想把探索过程沉淀成可复盘、可展示的产品发现记录。

不适合：

- 已明确需求的小功能实现。
- bug fix、局部 UI 调整、纯 code review。
- 已有成熟产品的增长、运营或迭代优化。
- 在没有 grounded context 的情况下直接生成最终 PRD、Roadmap 或 Implementation Plan。

## Install

### Option 1: Install From GitHub With Codex

仓库公开后，可以在 Codex 中使用 `$skill-installer` 直接安装：

```text
$skill-installer install https://github.com/Conradgui/zero-to-one-product-discovery/tree/main/zero-to-one-product-discovery
```

这个仓库根目录同时包含 `dist/` 和 `zero-to-one-product-discovery-eval-runs/`，所以安装时必须指向 `zero-to-one-product-discovery/` 子目录，而不是仓库根 URL。如果未来把这个 skill 放进某个 monorepo 的其他子目录，也使用 GitHub tree 路径：

```text
$skill-installer install https://github.com/<your-name>/<your-repo>/tree/main/zero-to-one-product-discovery
```

安装后重启 Codex，让 skill 被重新发现。

### Option 2: Manual Install For Codex

从当前 workspace 复制到 Codex 的个人 skill 目录：

```bash
mkdir -p ~/.codex/skills
cp -R zero-to-one-product-discovery ~/.codex/skills/zero-to-one-product-discovery
```

然后重启 Codex。

### Option 3: Manual Install For Other SKILL.md-Compatible Agents

如果你的 agent 支持 `SKILL.md` 目录格式，把整个 `zero-to-one-product-discovery/` 文件夹复制到对应的 skills 目录即可。常见目录形态包括：

```text
~/.codex/skills/zero-to-one-product-discovery
~/.claude/skills/zero-to-one-product-discovery
.codex/skills/zero-to-one-product-discovery
.claude/skills/zero-to-one-product-discovery
```

不同客户端的目录名和重启方式可能不同，以你的客户端文档为准。

## Usage

自然语言触发：

```text
我有一个从零开始的开源产品想法，想先梳理问题和 MVP，不要急着写代码。
```

显式触发：

```text
Use $zero-to-one-product-discovery as the main workflow to explore this early product idea.
```

一个典型协作节奏：

1. 用户提出初步想法。
2. skill 输出 Diagnostic Start：事实、假设、风险、未知、候选探索方向和当前最高杠杆问题。
3. 用户逐轮回答关键问题或提供材料。
4. skill 吸收材料并推进 Problem Framing、Solution Exploration、Feasibility Discovery 和 MVP Hypothesis。
5. 当前置条件满足后，主控 workflow 路由到 PRD、Roadmap、User Stories、ADR 或 Implementation Plan 子能力。

## Workflow

```text
Diagnostic Start
  -> Material Assimilation
  -> Problem Framing
  -> Solution Exploration
  -> Feasibility Discovery
  -> MVP Hypothesis
  -> Planning Artifacts
  -> Implementation Planning
```

阶段不是死板 checklist，而是防止 AI 跳步的 guardrail。显式要求“直接给完整 PRD”也不能绕过门禁；如果前置条件不足，输出必须降级。

## Multi-Agent Model

这个 skill 的多 agent 设计保持平台无关，不要求特定客户端支持真实子代理。实现时可以是真实 subagent，也可以是同一 agent 内的专业角色模拟。入口文档见 `agents/README.md`，完整协议见 `references/multi-agent-orchestration.md`。

```text
Workflow Rules -> Controller Agent -> Producer Agent -> Runtime Workbench -> Auditor Agent -> Controller Decision
```

| Role | Responsibility | Must Not |
|---|---|---|
| Workflow Rules | 定义 stages、gates、downgrade rules、allowed outputs 和 user gates。 | 充当 agent、保存 runtime state 或接受 artifact。 |
| Controller Agent | 应用 workflow rules，创建 Agent Work Order，更新 Runtime Workbench，并决定下一步安全动作。 | 产出未经审核的 final artifact，或隐藏 producer / auditor blocker。 |
| Producer Agents | 根据 Controller 提供的 bounded work order 产出一个 artifact 或 readiness review。 | 选择下一阶段、调用其他 producer、接受自己的输出为 final。 |
| Auditor Agent | 独立检查 boundary、evidence quality、cross-artifact consistency 和 acceptance readiness。 | 替 producer 重写 artifact，或替用户做产品决策。 |
| Runtime Workbench | 保存当前决策状态：证据快照、产物状态、依赖、冲突、风险、审核队列和下一步动作。 | 保存 full transcript、full history、完整 artifact 或复盘长日志。 |

核心 Producer：

| Producer | Trigger | Output | Must Not |
|---|---|---|---|
| `Research` | 材料、反馈、PRD、笔记或市场/用户证据需要综合时。 | Evidence snapshot、contradictions、assumptions、gaps、risks。 | 编造 evidence，或把 assumptions 标成 facts。 |
| `PRD` | problem、solution direction、MVP hypothesis、risks、success/failure indicators 足够 grounded 时。 | PRD draft、PRD outline 或 readiness review。 | 在用户接受和 evidence readiness 前产出 final PRD。 |
| `Roadmap` | PRD 或 PRD outline 已足够确认，可以排序验证或交付时。 | Now/Next/Later、phases、milestones、validation gates。 | 把弱假设变成 delivery commitment。 |
| `ADR` | 出现 durable architecture、platform、data、security、dependency 或 maintainability 决策时。 | Decision Log entry 或 ADR candidate。 | 把普通 scope tradeoff 升级成不必要 ADR。 |
| `Implementation Plan` | planning artifacts 和相关 technical decisions 达到 review-ready 时。 | Engineering plan、verification plan、sequencing、risks。 | 在 readiness 前开始 coding 或 scaffold repo。 |

运行顺序：

```text
Workflow Rules
  -> Controller Agent
  -> Agent Work Order
  -> Producer Agent
  -> Agent Return Packet
  -> Runtime Workbench update
  -> Auditor Agent, when substantial output needs review
  -> Controller Decision
  -> User Gate, when required
```

默认采用 stage-serial production + local parallel audit：产物生产按证据链串行推进，审核和一致性检查可以在同一 accepted workbench state 上局部并行。复盘材料通过 `Audit Report` 或阶段性 `Trace Report` 生成，不进入实时主控路径。

## Repository Layout

```text
zero-to-one-product-discovery/
├── README.md                # GitHub 展示与安装说明
├── SKILL.md                 # 主控 workflow skill
├── agents/
│   ├── openai.yaml          # Codex UI metadata，不是 agent runtime protocol
│   ├── README.md            # Multi-agent role protocol 入口
│   └── multi-agent-orchestration.md
├── child-skills/            # 本地子能力 adapter，只能由主控路由
├── references/              # 阶段规则、路由协议、多 agent 协议、来源治理和文档模板
├── vendor/                  # 上游 skill/source 快照和许可证，不可直接路由
└── evals/                   # 可复用评测场景、rubric 和测试协议
```

历史 raw responses、scored reports 和 handoff 记录不放入安装包；维护者可以在本地外部归档中保存它们，例如：

```text
zero-to-one-product-discovery-eval-runs/
├── archive/
├── current/
├── design-records/
├── handoffs/
└── tmp/
```

普通 skill 使用不需要加载这些归档。新测试先写入 `tmp/<run-id>/`；只有发现实质问题、暴露回归、确认关键 release gate，或产生可执行改进方向的测评，才通过 Value Gate 提升到 `current/<version>/<run-id>/` 或版本化 archive。被提升的 eval-runs 可以随 GitHub 仓库提交，作为公开验证证据；它们不是 runtime context，也绝不能进入用户安装的 skill zip。

## Child Skills

`child-skills/` 中的模块是本地 adapter，不是用户直接调用的独立流程。

| Child skill | Purpose |
|---|---|
| `research-brief` | 综合访谈、反馈、竞品、笔记，区分 evidence / assumption / contradiction / gap |
| `prd` | 在 grounded context 下输出 PRD；信息不足时只输出 PRD outline 和缺口 |
| `roadmap` | 生成 Now / Next / Later、阶段化路线图和验证门禁 |
| `user-stories` | 生成用户故事、故事地图和 release slice |
| `acceptance-criteria` | 为已确认需求或故事生成验收标准 |
| `adr-governance` | 判断 Decision Log vs ADR，处理长期技术决策 |
| `mermaid` | 基于已知结构生成 Mermaid 图 |
| `implementation-plan` | 从 review-ready planning artifacts 进入工程实施计划 |
| `review` | 从产品、UX、工程、测试和架构角度审查 artifact |
| `context-handoff` | 生成跨轮次或跨会话的 Context Resume Packet |

主控规则：

- child skill 不能自行跳阶段。
- child skill 不能调用其他 child skill。
- child skill 不能从 `vendor/` 直接执行上游 command。
- child skill 不能把假设包装成事实。
- producer agent 不能直接调用其他 producer agent；只能通过 Controller 和 Runtime Workbench 提交依赖或冲突。
- 重要产物在接受为 final 或 review-ready 前需要 Controller review 或 Audit Report。
- 重要输出必须带 readiness signal 和 Context Resume Packet。

## Source Transparency

`vendor/` 保存外部来源快照、许可证和参考实现，用于来源透明和 adapter 质量参考。它不是本项目的核心能力卖点，也不是运行时 route target。

主要参考来源：

- [Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)：PM 深度、PRD、Roadmap、JTBD、故事地图。
- [pm-skills](https://github.com/product-on-purpose/pm-skills)：artifact skill 组织、PRD、ADR、Mermaid、用户故事、验收标准。
- [agent-skills](https://github.com/addyosmani/agent-skills)：工程治理、ADR、计划拆解、测试、review。
- [awesome-copilot](https://github.com/github/awesome-copilot)：生态索引和补充参考。

`vendor/` 是来源库，不是 route target。所有用户可感知行为必须经过 `child-skills/` 和主控 stage gate。

See also:

- `vendor/MANIFEST.md`
- `references/source-attribution.md`
- `references/source-evaluation.md`

## Evaluation

可复用评测协议保存在 `evals/`：

- `evals/evals.json`：v0.1.5 strict suite、deterministic checks、rubric checks、hard failures 和 Value Gate 元数据；`v0.1.9` 继续复用该套核心回归场景。
- `evals/eval-rubric-template.md`：评分 rubric 和 Evidence Value Review 模板。
- `evals/claude-code-pressure-test-protocol.md`：五阶段 pressure test 协议：raw generation、deterministic checks、rubric grading、value review、promotion decision。
- `evals/eval-report.schema.json`：结构化评分报告 schema。
- `evals/value-review.schema.json`：测试后价值判定 schema。
- `evals/baseline-ab-template.md`：baseline-vs-skill A/B 模板。
- `evals/baseline-ab-scoring-rubric.md`：paired A/B 评分细则。
- `evals/baseline-ab-report.schema.json`：A/B 结构化报告 schema。
- `evals/evaluation-package.md`：当前证据、限制和安全 claim。

当前可以谨慎声明：

- 历史 runs 解释了早期架构演进，但不能作为 `v0.2.0` release-grade 证据。
- `v0.1.5` 已有严格测评体系、结构化 schema 和 Value Gate；`v0.1.6` 是面向 Windows 干净环境验证的交接版本；`v0.1.7` 是吸收 Windows run-01 发现问题后的收尾补丁版本；`v0.1.8` 是吸收 v0.1.7 targeted rerun 发现问题后的最终收官补丁版本；`v0.1.9` 新增受控本地 baseline A/B 方法论和证据。
- multi-agent workflow protocol 已完成结构化设计和 strict suite 扩展。
- `current/v0.1.5/2026-05-12-run-01/` 是首轮 fresh pressure evidence：它发现了 package/eval boundary 表达不清、vendor-boundary 回复轻微漂移、PRD draft/final 规格不够细的问题，因此不能单独作为 install-candidate 证据。
- `current/v0.1.5/2026-05-14-run-02/` 是 targeted rerun evidence：它验证 package/eval boundary 和 vendor-boundary drift 已被补丁关闭，但仍不是 full-suite install-candidate 证据。
- `current/v0.1.5/2026-05-14-run-03/` 是补丁后的 full strict-suite rerun：22 个场景全部通过，0 hard failure，最低分 90；它证明补丁后的核心场景回归通过，但仍不是干净安装触发证据。推荐先读该 run 的 `summary-report.md`，再查看结构化 JSON 评分。
- `current/v0.1.6/2026-05-14-windows-clean-install-handoff/` 是 Windows clean-install validation handoff：它提供测试包和回传模板。
- `current/v0.1.6/2026-05-17-windows-clean-install-run-01/` 是第一轮 Windows clean-install relay evidence：8 个场景通过、0 hard failure，同时发现维护请求污染测试环境、安装说明和评测协议需要补丁。
- `current/v0.1.7/2026-05-18-targeted-rerun-01/` 是 v0.1.7 targeted Windows rerun evidence：它确认维护污染和 helper-skill 外显问题已关闭，同时发现 packaging `dist/` 文档、eval metadata 和 PRD Draft user-gate 仍需最终补丁。
- `current/v0.1.9/2026-05-18-baseline-ab-run-01/` 是 v0.1.9 controlled local baseline A/B evidence：10 个 paired scenarios 中 skill average 95.7、baseline average 68.4、average delta +27.3、skill hard failures 0；该结果只支持场景内改进，不支持跨模型全面优越性。
- 任何新测试只有通过 Value Gate，才会作为 GitHub 项目证据沉淀；用户安装 skill zip 时不会下载这些 run artifacts。

当前不能声明：

- release-grade validation。
- install candidate 状态。
- 跨客户端、重启后的自然触发可靠性。
- 完整多轮 workflow 质量。
- 本地 source adapter 相对旧 artifact adapter 的系统性 A/B 优势。
- release-grade multi-agent workflow 稳定性。

## Versioning

当前版本：`v0.2.1`。

版本管理规则：

- Git tag、GitHub Release 名称、zip 文件名必须使用同一个版本号。
- `v0.1.0-draft` 保留为早期历史草稿版本；multi-agent workflow 属于较大的架构升级，从 `v0.1.5` 开始记录。
- `v0.1.6` 是 Windows clean-install validation handoff 和第一轮 relay evidence 版本；`v0.1.7` 是 Windows 收尾补丁版本；`v0.1.8` 是最终收官补丁版本；`v0.1.9` 是 Baseline A/B evidence 版本；它们都不移动或改写已经发布的历史 tag。
- `v0.2.0` 是 Portfolio Release：整理 GitHub 展示、证据 dashboard、安装包和面试材料，但仍不声明 production-grade 或 release-grade。
- `v0.2.1` 是 multi-agent documentation structure patch：把 agent role protocol 放入 `agents/`，并强化 README 的 Multi-Agent Model 展示。
- Draft 状态和 release-grade validation 状态用文档说明，不再把这批 multi-agent 改动继续补在 `v0.1.0-draft` 后面。
- 每次打包前确认 `README.md`、`SKILL.md`、`agents/openai.yaml`、`references/`、`child-skills/`、`evals/` 已同步。
- 临时发布目录如 `zero-to-one-product-discovery-publish.*` 不进入仓库；可发布包以 `dist/zero-to-one-product-discovery-skill-<version>.zip` 为准。

## Packaging

推荐发布包只包含：

```text
zero-to-one-product-discovery/
```

不要把本地外部归档打进 skill 安装包，例如：

```text
zero-to-one-product-discovery-eval-runs/
```

边界规则：

- GitHub 仓库可以保留通过 Value Gate promoted 的 eval-runs，用来说明本项目如何验证真实可用性。
- 用户安装 zip 只能包含 `zero-to-one-product-discovery/` runtime 目录；不要包含 `zero-to-one-product-discovery-eval-runs/`、`.git/`、`tmp/`、`dist/` 或发布临时目录。
- 当某次 run 没有实质发现，只能按 `minimal-note` 或 `discard-full-run` 处理，不能用完整 raw/report 制造虚假的强证据。

本地打包命令必须带版本号。当前版本是 `v0.2.1`：

```bash
VERSION=v0.2.1
mkdir -p dist
zip -r "dist/zero-to-one-product-discovery-skill-${VERSION}.zip" zero-to-one-product-discovery \
  -x '*/.DS_Store' \
  -x '*/__pycache__/*'
```

Windows PowerShell:

```powershell
$Version = "v0.2.1"
New-Item -ItemType Directory -Force -Path dist | Out-Null
Compress-Archive -Path zero-to-one-product-discovery -DestinationPath "dist/zero-to-one-product-discovery-skill-$Version.zip" -Force
```

后续上传 GitHub Release、手动分发或本地归档时，zip 文件名、release 名称和 git tag 应使用同一个版本号。

解压后应能看到：

```text
zero-to-one-product-discovery/SKILL.md
zero-to-one-product-discovery/README.md
zero-to-one-product-discovery/child-skills/
zero-to-one-product-discovery/references/
zero-to-one-product-discovery/vendor/
zero-to-one-product-discovery/evals/
```

## License And Attribution

This repository is intended for personal open-source / portfolio use and non-commercial trial while it is still in draft.

The `vendor/` directory contains copied upstream snapshots with mixed licenses, including CC BY-NC-SA 4.0, Apache-2.0, and MIT. For source transparency and attribution, review:

- `vendor/MANIFEST.md`
- `references/source-attribution.md`
- upstream repository licenses

Local workflow and adapter text should remain clearly separated from verbatim upstream source snapshots. `vendor/` is a source snapshot library, not an active child skill or original runtime capability.
