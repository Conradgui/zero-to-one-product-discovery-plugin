# Zero-to-One Product Discovery Plugin

`zero-to-one-product-discovery-plugin` 是 `zero-to-one-product-discovery`
workflow skill 的 Codex plugin 分发包装层。

核心能力仍然来自 bundled skill。这个仓库只负责把该 skill 以 Codex plugin 的形式发布，提供
manifest、安装边界、README、验证脚本和未来分发入口。它不是核心 skill 的替代仓库，也不应把
plugin 分发层的约束反向污染核心 workflow 源仓库。

这个仓库解决的是产品化分发问题，而不是重新发明 workflow：当一个 AI discovery skill 从个人安装走向可被他人浏览、安装和复用时，最容易出错的地方不是多写一个功能，而是边界变得含糊。plugin 层把可安装入口、manifest metadata、runtime 包内容和验证脚本固定下来，让使用者看到的是一个清晰的 Codex plugin，而维护者仍然能把核心行为演进留在源 skill 仓库中。

## 这个 Plugin 做什么

这个 plugin 提供一个面向早期产品、开源项目、side project 和 startup idea 的分阶段 AI product
discovery workflow。

它的重点不是快速生成 PRD、Roadmap、ADR 或 Implementation Plan，而是先让 AI assistant
围绕问题、证据、假设、风险和 MVP hypothesis 做足 grounding，避免在信息不足时过早进入规划或编码。

对使用者来说，它提供的是一个更容易被 Codex 发现和触发的产品发现入口；对维护者来说，它是一层分发边界，明确哪些文件属于 runtime，哪些证据、zip 历史或临时产物不应该进入 plugin 包。

workflow 支持：

- Diagnostic Start：处理非常模糊的 idea。
- Material Assimilation：吸收已有 notes、PRD、sketches、feedback 或 research。
- Problem Framing、Solution Exploration、Feasibility Discovery 和 MVP Hypothesis。
- Planning Artifacts：只在 readiness gates 通过后生成。
- Implementation Planning：只在 planning artifacts 达到 review-ready 后推进。

## 仓库边界

这个仓库是 Plugin Lite 分发层：

```text
Core workflow skill
  -> installable skill package
  -> plugin distribution wrapper
  -> future MCP / UI / CLI extension, if needed
```

bundled skill 位于：

```text
skills/zero-to-one-product-discovery/
```

plugin manifest 位于：

```text
.codex-plugin/plugin.json
```

除非是在修复分发包复制错误，否则不要在这个仓库里改核心 workflow 行为。核心 skill 的演进应在核心项目中完成，再同步到本分发仓库。

## 不包含什么

这个 plugin 有意不包含：

- `zero-to-one-product-discovery-eval-runs/`
- `dist/` release zip history
- 临时 publish directories
- 历史 raw evaluation transcripts
- MCP server configuration
- app UI configuration
- LangGraph 或 Python runtime

evaluation evidence 应继续保留在核心项目的 evidence archive 中。plugin runtime 应保持小而清晰。

## 为什么是 Plugin Lite

这个项目最初是 workflow skill，因为核心问题是行为治理：AI agent 什么时候应该提问、降级输出、切换阶段、审计或停止。

plugin 层增加的是产品化分发能力：

- plugin manifest；
- 清晰的安装边界；
- Codex plugin metadata；
- package validation；
- 为未来 MCP 或 UI 扩展预留空间。

这里刻意保持 Plugin Lite，而不是直接加入 MCP server、app UI、LangGraph runtime 或额外 CLI。原因是当前产品风险不在“缺少更多界面”，而在“分发形态是否让边界更清楚”：plugin 应该让 skill 更容易安装和识别，但不应该把尚未验证的 runtime 能力包装成已经存在的产品能力。

## Claim Boundary

支持的 claim：

- 这个 plugin 将一个已有、带 evidence 支撑的 workflow skill 打包为 Codex plugin 分发形态。

不支持的 claim：

- 它不是 production-grade validation。
- 它不证明跨模型优越性。
- 它没有新增 service runtime、MCP server 或 app UI。
- 它不替代核心 `zero-to-one-product-discovery` 源仓库。

## 安装和使用

公开使用时，以 Codex app 的 Plugins 入口为准：在 Codex 左上角打开 Plugins，浏览或添加 plugin。当前 README 不写未经验证的 CLI 安装命令。

安装后可以这样使用：

```text
我有一个很模糊的开源产品想法。请使用 zero-to-one product discovery，不要急着写 PRD 或代码。
```

或者：

```text
探索我的早期产品想法，先找出最有风险的假设，再讨论是否进入实现规划。
```

## 本地验证

运行自定义 package 验证：

```bash
python3 scripts/validate-plugin-package.py
```

运行 Codex plugin schema 验证：

```bash
python3 /Users/conrad/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/conrad/Desktop/zero-to-one-product-discovery-plugin
```

## 维护原则

- 保持小而可 review 的 diff。
- plugin 分发层只维护 manifest、README、验证脚本、安装边界和未来分发元数据。
- 不在这里新增 analytics、telemetry 或网络调用。
- 不声明 `mcpServers`、`apps` 或 `hooks`，除非对应的配置和 runtime 真实存在。
- 核心 workflow 行为变更应先在核心 skill 项目中完成，再同步到本仓库。

## License

MIT
