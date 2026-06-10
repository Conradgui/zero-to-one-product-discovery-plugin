# Material Assimilation

Use this reference when the user provides existing notes, PRDs, sketches, user feedback, competitor research, roadmaps, requirement lists, screenshots, or partial planning documents but there is no complete product or runnable MVP.

## Principle

Existing material is input, not truth. Understand it before improving it.

Do not restart from blank. Do not assume the material is complete, correct, or aligned with the user's current goals.

## Process

1. Inventory the materials.
2. Extract facts, assumptions, decisions, open questions, and contradictions into the Extraction Table.
3. Present the Extraction Table to the user with a summary: "已从你的材料中提取 N 项：X Facts, Y Assumptions, Z Decisions, W Risks, V Contradictions."
4. Ask the user: "一键接受并继续" (Express Review) or "逐项审视" (Standard Review).
   - **Express Review**: batch-accept all items except contradictions (which require user confirmation). Proceed to step 5.
   - **Standard Review**: discuss each item with the user. Proceed to step 5.
5. Identify what exploration stages are already partially covered.
6. Identify missing or weak areas.
7. Ask the highest-leverage question for the current turn before revising or extending.
8. Continue from the missing stage instead of replaying the whole workflow.

### Express Review

Express Review lets the user batch-accept extraction results instead of discussing each item individually.

**When to offer**: After extraction is complete and the Extraction Table has been presented.

**How it works**:
1. AI presents the Extraction Table with item counts.
2. User says "一键接受" / "Express Review" / "直接继续".
3. AI batch-accepts all items except contradictions.
4. Contradictions are flagged and require user confirmation: "[材料 A] 说 X，[材料 B] 说 Y。哪个更接近当前状态？"
5. After user confirms contradictions, continue to stage coverage analysis.

**What Express Review skips**: Individual discussion of each fact, assumption, decision, and risk.

**What Express Review does NOT skip**: Contradiction confirmation, stage coverage analysis, missing area identification, and the highest-leverage question.

**Difference from Quick Mode**:
- Quick Mode is a global mode switch that skips all interactive exploration loops across all stages.
- Express Review is stage-specific: it only applies to Material Assimilation's extraction discussion, not to other stages.

## Extraction Table

| Category | What To Capture | Validation Suggestion |
|---|---|---|
| Facts | Concrete statements supported by material or evidence | Source verification if needed |
| Assumptions | Claims that may be true but are not verified | Experiment design, success criteria, timeline |
| Decisions | Choices already made, explicit or implicit | Stakeholder confirmation if implicit |
| Risks | Product, technical, legal, platform, design, or execution risks | Risk mitigation plan |
| Contradictions | Conflicts across documents or within the same document | Source reconciliation |
| Gaps | Missing context needed for the next stage | Research or interview plan |

For assumptions, the validation suggestion should include:
- **Experiment**: What to do to verify (e.g., user interview, A/B test, prototype test)
- **Success Criteria**: What confirms or invalidates the assumption
- **Timeline**: When to validate by (e.g., before PRD, before Roadmap)

## Demand Triage Lite

When materials contain user feedback, feature requests, or internal wishes, classify each item before treating it as a requirement:

| Type | Meaning | Response |
|---|---|---|
| Real problem | A repeated or high-impact pain with context | Preserve and validate |
| Solution request | User asks for a specific feature | Ask what problem it solves |
| Emotional signal | Frustration, anxiety, excitement, confusion | Identify underlying job or blocker |
| Edge case | Valid but rare or low-impact scenario | Track, but avoid MVP capture unless critical |
| False demand | Requested feature does not map to a real problem or goal | Challenge or defer |
| Strategic noise | Interesting but not relevant to current stage | Record outside MVP |
| Valid opportunity | Plausible unmet need needing evidence | Convert to validation question |

Do not directly convert a feature request into a product requirement.

## Output

Keep output focused:

1. Material inventory.
2. Facts / assumptions / risks / contradictions / gaps with validation suggestions.
3. Assumption Validation Bindings: for each assumption, suggested experiment, success criteria, and timeline.
4. Which stages are already partially covered.
5. What should be kept, questioned, revised, or deferred.
6. Evidence Maturity Summary: total items, facts count, assumptions count, unknowns count, risks count, validated count, maturity level, maturity percentage.
7. The highest-leverage alignment question for the current turn.
