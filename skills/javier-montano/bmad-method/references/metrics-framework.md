# BMAD Metrics Framework — Measuring Effectiveness

## Table of Contents
- [Framework Purpose](#framework-purpose)
- [Process Metrics](#process-metrics)
- [Quality Metrics](#quality-metrics)
- [Team Metrics](#team-metrics)
- [Measurement Methods](#measurement-methods)
- [Dashboards and Alerting](#dashboards-and-alerting)
- [Metric Formulas and Calculations](#metric-formulas-and-calculations)
- [Trend Analysis](#trend-analysis)
- [Metric Anti-Patterns](#metric-anti-patterns)

---

## Framework Purpose

Metrics exist to detect problems early — not to grade performance. Every metric in this framework answers a specific question about BMAD process health. If a metric does not drive a concrete action when it crosses a threshold, remove it.

**Three rules for BMAD metrics**:
1. Measure outcomes, not activity (lines of code is not a metric; defect escape rate is)
2. Trend matters more than absolute value (velocity of 20 is meaningless; velocity declining 15% per sprint is a signal)
3. Every metric must have an action threshold (if metric crosses X, do Y)

---

## Process Metrics

### PM-1: Cycle Time Per Phase

**Question**: How long does each phase take?

**Formula**:
```
Phase cycle time = Phase end date - Phase start date (in working days)
```

**Collection**: Record phase start/end dates in project-context.md or sprint-status.yaml.

**Benchmarks** (solo developer, medium-complexity project):
| Phase | Target | Warning | Critical |
|-------|--------|---------|----------|
| Phase 1 (Analysis) | 1-2 days | >3 days | >5 days |
| Phase 2 (Planning) | 2-3 days | >5 days | >7 days |
| Phase 3 (Solutioning) | 2-4 days | >6 days | >10 days |
| Phase 4 (per sprint) | 5-10 days | >14 days | >21 days |

**Action on critical**: Investigate which substep is consuming time. Common causes: Phase 1 — unbounded research; Phase 2 — stakeholder misalignment; Phase 3 — architecture indecision; Phase 4 — blockers or misestimation.

### PM-2: Gate Pass Rate

**Question**: What percentage of gate evaluations pass on the first attempt?

**Formula**:
```
First-pass rate = (Gates passing on first evaluation / Total gate evaluations) x 100
```

**Target**: >70% first-pass rate across 5+ gate evaluations.
**Warning**: 50-70% — review Phase 3 workflows for systemic gaps.
**Critical**: <50% — Phase 3 output quality is fundamentally insufficient. Add pre-gate checklists or training.

**Collection**: Track in each gate-result.json: add a `first_pass` boolean field.

### PM-3: Sprint Velocity Trend

**Question**: Is the team delivering consistently?

**Formula**:
```
Velocity = Completed story points in a sprint
Velocity trend = (Sprint N velocity - Sprint N-3 velocity) / Sprint N-3 velocity x 100
```

**Target**: Velocity trend within +/- 15% of the 3-sprint rolling average.
**Warning**: >15% decline for 1 sprint — investigate causes in retro.
**Critical**: >30% decline for 2 consecutive sprints — trigger root-cause analysis per [R8].

**Collection**: `sprint-status.yaml` → `metrics.velocity` field.

### PM-4: Carry-Over Rate

**Question**: How many planned stories are not completed in their sprint?

**Formula**:
```
Carry-over rate = (Stories carried to next sprint / Stories planned) x 100
```

**Target**: <20% carry-over rate per sprint.
**Warning**: 20-30% — re-calibrate estimation approach.
**Critical**: >30% for 2+ sprints — systemic estimation bias. Re-estimate entire backlog with actuals.

### PM-5: Artifact Freshness

**Question**: Are BMAD artifacts kept up to date?

**Formula**:
```
Artifact freshness = Days since last update to project-context.md
```

**Target**: Updated within the last sprint boundary (<=14 days for 2-week sprints).
**Warning**: 15-30 days stale.
**Critical**: >30 days stale — project-context.md is unreliable. Schedule an update session.

**Collection**: `git log -1 --format=%ci -- project-context.md`

---

## Quality Metrics

### QM-1: Rework Rate

**Question**: How many completed stories require re-implementation?

**Formula**:
```
Rework rate = (Stories re-opened after "done" / Total completed stories) x 100
```

**Target**: <10% rework rate.
**Warning**: 10-20% — acceptance criteria quality is insufficient. Review gate step 4.
**Critical**: >20% — fundamental gap in requirements or testing. Audit the last 5 reworked stories to identify root cause.

**Collection**: Track story status transitions in sprint-status.yaml. A story that moves `done → in-progress` is a rework event.

### QM-2: Defect Escape Rate

**Question**: How many defects reach production that existing tests and reviews did not catch?

**Formula**:
```
Defect escape rate = (Production defects / (Production defects + Defects caught pre-production)) x 100
```

**Target**: <5% escape rate.
**Warning**: 5-15% — review test coverage and code review effectiveness.
**Critical**: >15% — test strategy is fundamentally inadequate. Add integration and E2E test requirements to the Definition of Done.

**Collection**: Count production bug reports (Quick Flow fixes tagged as regressions) vs. bugs caught in CI, code review, or QA.

### QM-3: Requirement-to-Test Traceability

**Question**: What percentage of FRs have at least one automated test?

**Formula**:
```
Traceability coverage = (FRs with at least one linked test / Total FRs) x 100
```

**Target**: 100% for Must-have FRs, >80% for Should-have FRs.
**Warning**: <90% Must-have FR coverage.
**Critical**: <70% — traceability chain is broken. Run `check_artifact_flow.py` and create missing test stories.

**Collection**: Maintain a traceability matrix (see `references/artifact-flow-chain.md`). Map each FR to its test file(s).

### QM-4: Artifact Quality Score

**Question**: How complete and consistent are BMAD artifacts?

**Scoring rubric** (per artifact, 0-10 scale):
| Criterion | Score |
|-----------|-------|
| All required schema fields present | 0-3 |
| Cross-references are valid (FR-IDs exist, story-IDs resolve) | 0-3 |
| Content is specific and testable (no vague language) | 0-2 |
| Version and date are current | 0-2 |

**Target**: Average score >=8 across all active artifacts.
**Warning**: Average 6-7 — schedule a documentation cleanup sprint.
**Critical**: Average <6 — artifacts are unreliable. Downstream work is building on weak foundations.

**Collection**: Run `validate_project.py` for automated scoring of schema compliance. Manual review for content quality.

### QM-5: Gate Override Frequency

**Question**: How often are gate steps overridden instead of fixed?

**Formula**:
```
Override frequency = (Gate evaluations with overrides / Total gate evaluations) x 100
```

**Target**: <10% of gate evaluations include overrides.
**Warning**: 10-20% — review if gate criteria are too strict for the project type.
**Critical**: >20% — gates are being circumvented routinely. Either the gate criteria are misaligned with reality or the team is cutting corners. Investigate which. See [R22].

---

## Team Metrics

### TM-1: Onboarding Time

**Question**: How quickly can a new team member contribute?

**Formula**:
```
Onboarding time = Days from first access to first merged PR
```

**Target**: <3 days for a developer joining a BMAD project with current artifacts.
**Warning**: 3-7 days — project-context.md may be incomplete or stale.
**Critical**: >7 days — fundamental documentation gaps. The team is relying on tribal knowledge.

**Collection**: Track join date and first merge date per contributor.

### TM-2: Agent Utilization

**Question**: Which BMAD agents are actually being used?

**Collection**: Track which agents are invoked per sprint. An unused agent indicates either process bypass or a gap in the agent roster.

**Expected utilization** (full BMAD flow):
| Agent | Expected Usage | Low Usage Signal |
|-------|---------------|-----------------|
| Mary (Analyst) | Phase 1, new projects | OK if skipping Phase 1 for brownfield |
| John (PM) | Every PRD cycle, scope changes | Problem: requirements created ad-hoc |
| Sally (UX) | Phase 2 when UX is relevant | OK if backend-only project |
| Winston (Architect) | Phase 3, architecture changes | Problem: architecture decisions made without documentation |
| Bob (Scrum Master) | Sprint planning, retros | Problem: sprints running without structure |
| Amelia (Developer) | Every sprint | Problem: coding without agent guidance |
| Quinn (QA) | Code review, test planning | Problem: no quality checks |
| Barry (Quick Flow) | Small fixes, minor enhancements | Problem if overused: complexity creep |

### TM-3: Estimation Accuracy

**Question**: How accurate are story point estimates?

**Formula**:
```
Estimation accuracy = 1 - |Estimated points - Actual effort| / Estimated points
```

Where actual effort is measured as: did the story complete within the sprint (accurate) or carry over (inaccurate)?

**Simplified tracking**: For each story, record whether it completed in the sprint it was planned for:
```
Accuracy rate = (Stories completed in planned sprint / Total stories) x 100
```

**Target**: >75% accuracy rate.
**Warning**: 60-75% — estimation calibration needed. Compare actuals to estimates for the last 10 stories.
**Critical**: <60% — estimates are unreliable. Use actual completion data from the last 3 sprints to recalibrate.

---

## Measurement Methods

### Automated Collection

| Metric | Collection Method | Tool |
|--------|------------------|------|
| PM-3 Velocity | Parse sprint-status.yaml | `generate_sprint_status.py` |
| PM-5 Artifact freshness | `git log` timestamp | Shell script / CI job |
| QM-3 Traceability | Cross-reference stories vs PRD | `check_artifact_flow.py` |
| QM-4 Artifact quality | Schema validation | `validate_project.py` |
| PM-2 Gate pass rate | Parse gate-result.json history | Custom script |

### Manual Collection

| Metric | Collection Method | Frequency |
|--------|------------------|-----------|
| PM-1 Cycle time | Record phase dates in project-context.md | Per phase transition |
| QM-1 Rework rate | Track story status transitions | Per sprint |
| QM-2 Defect escape rate | Count production incidents vs caught-in-dev | Per sprint |
| TM-1 Onboarding time | Track join date → first merge | Per new member |
| TM-2 Agent utilization | Review session logs | Per sprint retro |

### Collection Cadence

| Cadence | Metrics to Review |
|---------|------------------|
| Daily | Sprint burndown, blocked stories count |
| Per sprint | PM-3, PM-4, QM-1, TM-3 |
| Per phase transition | PM-1, PM-2, QM-4 |
| Monthly | QM-2, QM-3, QM-5, TM-1, TM-2 |
| Quarterly | All metrics — trend review |

---

## Dashboards and Alerting

### Recommended Dashboard Layout

**Section 1 — Sprint Health** (updated daily):
- Current sprint velocity vs target (bar chart)
- Stories by status: todo / in-progress / review / done / blocked (kanban counts)
- Burndown chart (remaining points over time)

**Section 2 — Process Health** (updated per sprint):
- Velocity trend (line chart, last 6 sprints)
- Carry-over rate trend (line chart)
- Gate pass rate (cumulative percentage)

**Section 3 — Quality Health** (updated per sprint):
- Rework rate trend (line chart)
- Defect escape rate (bar chart per sprint)
- Traceability coverage (percentage gauge)

**Section 4 — Alerts** (real-time):
| Alert | Trigger | Severity |
|-------|---------|----------|
| Sprint at risk | <50% of points completed at sprint midpoint | Warning |
| Sprint failing | <40% velocity at sprint end | Critical |
| Gate blocked | Same step fails 3+ times | Warning |
| Artifact stale | project-context.md >14 days old | Warning |
| Traceability gap | Any Must-have FR has no linked story | Critical |
| High carry-over | >30% carry-over for current sprint | Warning |

### Minimal Dashboard (Solo Developer)

Track only: velocity trend, carry-over rate, rework rate, gate pass rate, artifact freshness. Five metrics total — each answers one question about process health.

---

## Metric Formulas and Calculations

### Worked Example: Sprint 3 Metrics

```
Sprint 3 data:
  Planned stories: 6 (total 34 points)
  Completed stories: 5 (28 points completed)
  Carried over: 1 story (6 points)
  Stories reworked: 1 (re-opened after "done")
  Gate evaluations this sprint: 0
  Production defects: 0
  Defects caught in review: 3

Calculations:
  PM-3 Velocity = 28 points
  PM-3 Velocity trend = (28 - 24) / 24 x 100 = +16.7% (Sprint 1 was 24)
  PM-4 Carry-over rate = 1/6 x 100 = 16.7% (within target)
  QM-1 Rework rate = 1/5 x 100 = 20% (at critical threshold)
  QM-2 Defect escape rate = 0/(0+3) x 100 = 0% (excellent)
  TM-3 Accuracy rate = 5/6 x 100 = 83% (within target)

Actions:
  - Rework rate at 20% → investigate the reworked story.
    Root cause: ambiguous acceptance criteria on STORY-AUTH-003.
    Fix: review AC quality during sprint planning (gate step 4 equivalent).
  - All other metrics within target — no action needed.
```

### Rolling Average Calculation

3-sprint rolling average: `V_avg = (V_n + V_n-1 + V_n-2) / 3`. Example: sprints 24, 30, 28 → V_avg = 27.3. Sprint 4 capacity = V_avg minus 10% buffer = 24.6, plan for ~25 points.

---

## Trend Analysis

### What Healthy Trends Look Like

| Metric | Healthy Trend | Unhealthy Trend |
|--------|--------------|-----------------|
| Velocity | Stable or gradually increasing (plateaus are fine) | Declining >15% over 3 sprints |
| Carry-over rate | Declining toward <10% | Increasing or consistently >20% |
| Rework rate | Declining toward <5% | Stable at >15% or increasing |
| Gate pass rate | Increasing toward >80% | Declining or stuck below 60% |
| Estimation accuracy | Converging toward >80% | Oscillating wildly between 40-90% |
| Onboarding time | Decreasing as docs improve | Increasing (docs are getting stale) |

### Correlation Analysis

Key metric pairs that move together: gate pass rate declining correlates with rework rate rising. Carry-over rate increasing correlates with estimation accuracy dropping. Artifact freshness degrading correlates with onboarding time increasing. Quick Flow count rising alongside rework rate indicates Quick Flows are too loosely scoped.

---

## Metric Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Vanity metrics | Measuring total stories completed (ever-increasing, never actionable) | Replace with rate-based metrics (per sprint, per phase) |
| Gaming velocity | Inflating estimates to look faster | Track estimation accuracy alongside velocity — gaming creates accuracy divergence |
| Ignoring trends | Reacting to single-sprint anomalies but ignoring 3-sprint trends | Always compare to 3-sprint rolling average before acting |
| Measuring everything | 20+ metrics nobody reviews | Start with the 5-metric minimal dashboard. Add metrics only when a specific question needs answering. |
| Punishing metrics | Using metrics to blame individuals | Metrics diagnose process problems, not people problems. Frame every metric review as "what can we improve?" |

---

## Assumptions

- Sprint-status.yaml is maintained and updated at least at sprint boundaries
- Gate results are stored in version control as JSON (see `references/schemas.md#9-gate-result-schema`)
- The team is willing to spend 15 minutes per sprint reviewing metrics

## Limits

- This framework does NOT prescribe specific dashboarding tools (Grafana, Notion, spreadsheet — any works)
- This framework does NOT cover business outcome metrics (revenue, user growth) — those are product metrics, not process metrics
- Benchmarks are calibrated for AI-assisted solo/small-team development — enterprise teams must recalibrate thresholds

## Acceptance Criteria

- [ ] Every metric has a formula, a target, a warning threshold, and a critical threshold
- [ ] Collection method is specified for every metric (automated or manual)
- [ ] At least one worked calculation example demonstrates the formulas
- [ ] Dashboard layout specifies what to display and at what cadence
- [ ] Metric anti-patterns are documented with fixes

See also: `references/phase-4-implementation.md`, `references/implementation-readiness-gate.md`, `references/artifact-flow-chain.md`, `references/enterprise-governance.md`
