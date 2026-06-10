# 子 Skill 说明

这个目录保存 `zero-to-one-product-discovery` 主控 workflow 可以路由的本地子能力。普通使用者不需要直接调用这里的文件；他们应该只感觉自己在使用一个连续的产品发现流程。

## 目录关系

- `SKILL.md` 是主控入口，负责阶段判断、上下文连续性、子能力路由和最终输出验收。
- `child-skills/` 是本地修整后的专业能力模块，例如 PRD、Roadmap、ADR、用户故事和实施计划。
- `vendor/` 只保存上游项目的原始快照、许可证和来源记录，不是可直接调用的子 skill。
- `references/` 保存主控规则、路由协议、评测规则和来源治理说明。

## 边界规则

- 子 skill 只能由主控 workflow 路由，不能由用户直接当作独立流程使用。
- 子 skill 不能决定下一个产品发现阶段，只能返回 readiness signal。
- 子 skill 不能互相调用；如果需要另一个能力，只能建议主控 workflow 重新路由。
- 子 skill 必须基于主控传入的上下文工作，不能自行补造事实。
- 当子 skill 作为 Producer Agent 使用时，必须接收 Agent Work Order，并以 Agent Return Packet 摘要返回状态、证据变化、阻塞、冲突、自检和建议动作。
- 重要产物不能由 producer 自行接受为 final；必须由 Controller Agent 接受、降级、阻塞，或交给 Auditor Agent 审核。
- Runtime Workbench 只保存当前状态摘要；不要把完整产物、完整讨论或长历史写入工作台。
- Artifact Export 只能导出稳定文件和 File Workbench 视图；不能把缺失产物补造为 ready，也不能把 Quick Mode draft 伪装成 final，还必须在 manifest 中记录 `source_status`、`content_mode` 和 `status_guard`。
- Revision Trace 只能记录稳定 artifact 的 bounded ledger；不能保存 full transcript、完整 agent packet、完整 audit report、hidden reasoning 或版本化替代文件。
- 子 skill 的重要输出必须包含假设 / 未知 / 阻塞项、readiness signal 和 Context Resume Packet。
- `vendor/` 中的上游 command、模板或 mini-hub 只能作为质量参考，不能绕过本地 adapter 和主控阶段门禁。

## 当前本地子能力

| 子能力 | 主要参考来源 | 主控路由阶段 |
|---|---|---|
| `research-brief` | Product-Manager-Skills JTBD；pm-skills interview synthesis | Material Assimilation / Problem Framing |
| `prd` | Product-Manager-Skills PRD；pm-skills deliver-prd | Planning Artifacts |
| `roadmap` | Product-Manager-Skills roadmap planning | Planning Artifacts |
| `user-stories` | Product-Manager-Skills user story / story mapping；pm-skills deliver-user-stories | Planning Artifacts |
| `acceptance-criteria` | pm-skills deliver-acceptance-criteria | Planning Artifacts |
| `adr-governance` | agent-skills documentation-and-adrs；pm-skills develop-adr | Planning Artifacts / Implementation Planning |
| `mermaid` | pm-skills utility-mermaid-diagrams | Planning Artifacts |
| `implementation-plan` | agent-skills planning-and-task-breakdown；awesome-copilot implementation-plan references | Implementation Planning |
| `review` | agent-skills code-review-and-quality / test-driven-development | Artifact Review / Implementation Review |
| `context-handoff` | agent-skills context-engineering | 任何需要跨轮次或跨会话交接的阶段 |
| `execution-bridge` | 本地新建；GitHub Issues host handoff / Claude Code task / Jira ticket 格式转换 | Implementation Planning（需 review-ready Implementation Plan + 用户主动请求执行交接） |
| `artifact-export` | 本地新建；稳定文件结构、File Workbench、manifest | 已有 accepted 或 review-ready artifacts，且用户请求导出产物或工作台 |
| `revision-trace` | 本地新建；artifact hash / diff / revision ledger | 稳定 artifacts 已导出，且用户请求 artifact diff 或产物变更记录 |

## 使用原则

当主控 workflow 判断某个产物已经具备足够前置条件时，才会路由到对应子能力输出正式或 review-ready artifact。如果条件不足，子能力只能输出 outline、decision surface、evidence gap，或当前轮次最高杠杆的阻塞问题。

核心 producer 的默认顺序是 Research -> PRD -> Roadmap -> ADR 条件判断 -> Implementation Plan。审核和一致性检查可以局部并行，但产物生成不能从未验证假设中并行抢跑。
