# Trade-off Framework

Use this reference for meaningful product, technical, design, roadmap, scope, documentation, or implementation decisions.

## Required Dimensions

Evaluate major options across these dimensions:

| Dimension | Question |
|---|---|
| User value | Does this solve a real, strong, frequent problem? |
| Development cycle | Can this be validated within the current time horizon? |
| Implementation cost | What engineering, learning, integration, or operational cost does it add? |
| Technical risk | Does it depend on unstable, unfamiliar, or hard-to-debug technology? |
| Dependency risk | Does it rely on external platforms, devices, accounts, APIs, reviews, or policies? |
| Testability | Can it be verified manually or automatically? |
| Maintenance cost | Will future changes stay understandable and contained? |
| Extensibility | Does it support plausible next versions? |
| Open-source value | Does it show engineering judgment, documentation quality, or useful tooling? |
| Resume value | Can the result be explained as clear outcomes, trade-offs, and evidence? |

## Recording Rule

Every meaningful trade-off must be recorded in the project Decision Log.

Architecture-level, platform-level, security-sensitive, or long-lived technical decisions must create or update an ADR.

Do not treat trade-off analysis as disposable chat output.

## Decision Log Entry Shape

Use this shape in the project-side Decision Log:

```markdown
### YYYY-MM-DD: Decision Topic

#### Background

#### Options

| Option | Pros | Cons | Cost | Risk |
|---|---|---|---|---|

#### Trade-off Review

| Dimension | Judgment |
|---|---|
| User value |  |
| Development cycle |  |
| Implementation cost |  |
| Technical risk |  |
| Dependency risk |  |
| Testability |  |
| Maintenance cost |  |
| Extensibility |  |
| Open-source value |  |
| Resume value |  |

#### Decision

#### Why This Option

#### Why Not The Others

#### Validation Method

#### Rollback Condition
```

## ADR Escalation

Escalate from Decision Log to ADR when the decision:

- Shapes architecture or module boundaries.
- Is hard to reverse.
- Affects platform or deployment strategy.
- Changes security, privacy, data, or permissions.
- Adds a major dependency.
- Creates long-term maintenance obligations.
