# Phase 4 — Implementation: Deep Reference Guide

## Table of Contents
- [Purpose of Phase 4](#purpose-of-phase-4)
- [Sprint Planning Ceremony](#sprint-planning-ceremony)
- [Story Selection and Capacity](#story-selection-and-capacity)
- [Feature Branching Strategy](#feature-branching-strategy)
- [Test-Driven Story Development](#test-driven-story-development)
- [Code Review Standards](#code-review-standards)
- [Definition of Done](#definition-of-done)
- [Sprint Tracking](#sprint-tracking)
- [Handling Blockers](#handling-blockers)
- [Sprint Retrospective](#sprint-retrospective)
- [Continuous Integration](#continuous-integration)
- [When to Correct Course](#when-to-correct-course)

---

## Purpose of Phase 4

Phase 4 executes the plan built in Phases 1-3. Stories become working, tested code through disciplined sprint cycles. The key difference from ad-hoc development: every line of code traces back to a story, which traces back to a requirement, which traces back to a validated problem.

**Primary agent**: Developer (Dev) — writes code, tests, and maintains sprint status.

**Inputs**: Stories with acceptance criteria, Architecture document, project-context.md.

**Outputs**: Working code, test suites, sprint status updates, completed story files.

---

## Sprint Planning Ceremony

Sprint planning selects which stories to implement in the upcoming sprint.

### Planning Steps

1. **Review velocity**: Average points completed in the last 3 sprints (use team capacity for Sprint 1)
2. **Review the backlog**: Stories sorted by priority (Must > Should > Could) and dependency order
3. **Select stories**: Pull stories up to the velocity cap, respecting dependencies
4. **Validate dependencies**: Confirm all blocked-by stories are already complete
5. **Assign stories**: Each story gets a primary implementer
6. **Identify risks**: Flag stories with technical uncertainty
7. **Commit**: The selected stories form the sprint backlog

### Sprint Duration

BMAD recommends 1-2 week sprints for AI-assisted development. Shorter sprints enable faster course correction — critical when AI-generated code needs human review.

### Planning Output

Update the sprint tracking file (see Sprint Tracking section) with the selected stories, their assignees, and the sprint goal.

---

## Story Selection and Capacity

### Capacity Calculation

```
Sprint capacity = Velocity average - Risk buffer (10-20%)
```

For a team averaging 40 points per sprint:
- Available capacity: 40 - 4 (10% buffer) = 36 points
- Select stories totaling no more than 36 points

### Selection Priority

1. **Dependency order**: Stories that unblock other stories go first
2. **MoSCoW priority**: Must-have stories before Should-have
3. **Risk front-loading**: Tackle uncertain stories early in the sprint
4. **Value delivery**: Prefer stories that deliver demonstrable functionality

### Carry-Over Policy

Stories not completed in a sprint:
- Assess why: Was the estimate wrong? Was there a blocker?
- Re-estimate if the original estimate was off
- Carry over to the next sprint at the top of the backlog
- If a story has been carried over twice, split it

---

## Feature Branching Strategy

### Branch Naming Convention

```
[type]/[story-id]-[short-description]

Examples:
  feat/STORY-AUTH-001-user-registration
  fix/STORY-CART-003-quantity-validation
  chore/STORY-INFRA-002-database-migration
```

### Branch Types

| Type | Purpose |
|------|---------|
| `feat/` | New feature implementation |
| `fix/` | Bug fix for existing functionality |
| `chore/` | Infrastructure, tooling, configuration |
| `refactor/` | Code restructuring without behavior change |
| `docs/` | Documentation updates |

### Workflow

```
main (protected)
  └── develop (integration branch)
        ├── feat/STORY-AUTH-001-user-registration
        ├── feat/STORY-AUTH-002-password-complexity
        └── fix/STORY-CART-003-quantity-validation
```

1. Branch from `develop` (or `main` for simple projects)
2. Implement the story on the feature branch
3. Write and run tests
4. Open a pull request to `develop`
5. Pass code review and CI checks
6. Merge with squash commit
7. Delete the feature branch

### Commit Message Format

```
[STORY-ID] Brief description of change

Detailed explanation if necessary.

Acceptance criteria addressed:
- AC1: Given/When/Then verified
- AC2: Given/When/Then verified
```

---

## Test-Driven Story Development

### TDD Cycle for Each Story

1. **Read** the story's acceptance criteria
2. **Write failing tests** for each Given/When/Then criterion
3. **Implement** the minimum code to pass the tests
4. **Refactor** while keeping tests green
5. **Add edge case tests** beyond the explicit acceptance criteria
6. **Run the full test suite** to check for regressions

### Test Layers

| Layer | Scope | Coverage Target |
|-------|-------|----------------|
| Unit tests | Single function or method | 80%+ line coverage (NFR-MAINT-001) |
| Integration tests | Component interactions, API endpoints | All happy-path and primary error paths |
| End-to-end tests | Full user flows | Top 3 critical user journeys |

### Test File Organization

```
src/
  auth/
    register.ts
    register.test.ts       ← Unit tests co-located
tests/
  integration/
    auth.register.test.ts  ← Integration tests
  e2e/
    registration-flow.test.ts  ← E2E tests
```

### AI-Specific Testing Considerations

When AI generates code:
- Always review generated tests for correctness — AI may write tests that pass trivially
- Verify that tests actually exercise the stated acceptance criteria
- Check for missing error-path coverage
- Ensure tests do not duplicate implementation logic (testing tautologies)

---

## Code Review Standards

### Review Checklist

| Category | Check |
|----------|-------|
| **Correctness** | Does the code implement the story's acceptance criteria? |
| **Tests** | Do tests cover happy path, error paths, and edge cases? |
| **Architecture** | Does the code follow the architecture document and ADRs? |
| **Conventions** | Does the code follow project-context.md conventions? |
| **Security** | No hardcoded secrets, proper input validation, no SQL injection vectors |
| **Performance** | No N+1 queries, no unnecessary re-renders, proper pagination |
| **Readability** | Clear naming, appropriate comments, manageable function length |
| **Dependencies** | No unnecessary new dependencies; added deps are justified |

### Review Feedback Format

```
[REQUIRED] — Must be fixed before merge
[SUGGESTION] — Improvement that is not blocking
[QUESTION] — Clarification needed, not necessarily a change request
[PRAISE] — Something done well, worth noting for the team
```

### Review SLA

- Reviews should be completed within 4 working hours of request
- No PR should be open for more than 24 hours without feedback
- If the reviewer is blocked, reassign to another reviewer

---

## Definition of Done

A story is "done" when ALL of the following are true:

- [ ] All acceptance criteria pass (manual or automated verification)
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing (where applicable)
- [ ] Code review approved by at least one reviewer
- [ ] No linting errors or warnings
- [ ] No security vulnerabilities introduced (dependency scan passes)
- [ ] Documentation updated (API docs, comments, README if applicable)
- [ ] Feature branch merged to integration branch
- [ ] Story file status updated to `complete`
- [ ] Sprint tracking file updated

---

## Sprint Tracking

### sprint-status.yaml Format

```yaml
sprint:
  number: 3
  start_date: "2025-03-10"
  end_date: "2025-03-21"
  goal: "Complete user authentication and basic search"
  velocity_target: 34

stories:
  - id: STORY-AUTH-001
    title: User Registration with Email
    points: 5
    assignee: dev-agent
    status: complete        # draft | in-progress | review | complete | blocked
    completed_date: "2025-03-12"

  - id: STORY-AUTH-002
    title: Password Complexity Enforcement
    points: 3
    assignee: dev-agent
    status: in-progress
    blockers: []

  - id: STORY-SRCH-001
    title: Basic Search with Results
    points: 8
    assignee: dev-agent
    status: blocked
    blockers:
      - "STORY-INFRA-002 not yet complete"

totals:
  planned_points: 34
  completed_points: 18
  remaining_points: 16
  blocked_points: 8
```

### Status Transitions

```
draft → in-progress → review → complete
                   ↘ blocked → in-progress (when unblocked)
```

Update the sprint status file at least daily. This is the source of truth for sprint progress.

---

## Handling Blockers

### Blocker Classification

| Type | Description | Resolution Path |
|------|-------------|-----------------|
| **Dependency** | Another story must complete first | Prioritize the dependency; re-sequence the sprint |
| **Technical** | Unexpected complexity or missing capability | Spike investigation (time-boxed to 4 hours) |
| **External** | Waiting on third-party API, credentials, access | Escalate immediately; mock the dependency if possible |
| **Ambiguity** | Story or acceptance criteria unclear | Consult the PM agent; clarify before continuing |

### Blocker Protocol

1. **Identify**: As soon as progress halts, document the blocker in the sprint status file
2. **Classify**: Determine the blocker type
3. **Communicate**: Flag the blocker to the relevant agent (PM for ambiguity, Architect for technical)
4. **Mitigate**: If possible, work on an unblocked story while waiting
5. **Resolve**: Update the sprint status when the blocker is cleared
6. **Retrospect**: Add the blocker pattern to the retrospective for process improvement

---

## Sprint Retrospective

At the end of each sprint, conduct a brief retrospective.

### Retrospective Format

```markdown
# Sprint [N] Retrospective

## What Went Well
- [Item 1]
- [Item 2]

## What Could Improve
- [Item 1]
- [Item 2]

## Action Items
- [Specific action] — Owner: [who] — Due: [when]

## Metrics
- Velocity: [planned] → [actual]
- Stories completed: [N] of [M]
- Blockers encountered: [count]
- Carry-over stories: [list]
```

### Key Questions

- Were estimates accurate? If not, which stories were off and why?
- Were any blockers preventable with better planning?
- Did the architecture hold up, or were mid-sprint design changes needed?
- What can be improved for next sprint?

---

## Continuous Integration

### CI Pipeline Stages

```
1. Lint → 2. Unit Tests → 3. Build → 4. Integration Tests → 5. Security Scan → 6. Deploy Preview
```

### CI Requirements

- Pipeline runs on every push to a feature branch and on every PR
- All stages must pass before a PR can be merged
- Test results are reported on the PR
- Build artifacts are cached for performance
- Security scan checks for vulnerable dependencies

### CI Configuration Principles

- Fail fast: lint and unit tests run first (fastest feedback)
- Parallelize where possible: unit tests and security scan can run simultaneously
- Cache dependencies between runs
- Keep the total pipeline under 10 minutes for feature branches
- Full E2E suite runs on merge to integration branch (not on every push)

---

## When to Correct Course

### Signals That Require Course Correction

| Signal | Action |
|--------|--------|
| Velocity drops below 60% of target for 2 consecutive sprints | Re-estimate remaining stories; assess if architecture needs revision |
| 3+ stories blocked simultaneously | Review dependency map; consider re-sequencing the backlog |
| Same type of bug recurring across stories | Add a regression test suite; update coding conventions |
| NFR targets consistently missed | Escalate to Architect; may need architectural change (new ADR) |
| Scope creep — new requirements appearing mid-sprint | Invoke scope change protocol; defer new items to next sprint |
| Team capacity changed (member unavailable) | Re-plan sprint with reduced velocity |

### Correction Protocol

1. **Identify** the deviation from plan
2. **Quantify** the impact (points, timeline, risk level)
3. **Decide**: adjust sprint scope, extend timeline, or change approach
4. **Document** the correction in the sprint retrospective
5. **Update** the sprint status and backlog accordingly

### Sprint Failure Recovery

**[R8]** A sprint has failed when completed points are below 40% of the velocity target. Recovery protocol:

| Step | Action | Owner |
|------|--------|-------|
| 1 | Stop new story starts — stabilize in-progress work | Dev agent |
| 2 | Classify all incomplete stories: blocker, misestimate, or scope creep | PM agent |
| 3 | Re-estimate remaining stories using actuals from this sprint | Dev + PM |
| 4 | Carry over max 2 stories to next sprint; defer the rest to backlog | PM agent |
| 5 | Run a focused retrospective on failure causes before next sprint planning | Whole team |

### Velocity Anomaly Detection

Monitor these signals across sprints:

| Anomaly | Threshold | Likely Cause | Action |
|---------|-----------|-------------|--------|
| Velocity drop | >30% decline from 3-sprint average | Blockers, misestimates, or team capacity change | Root-cause analysis in retro |
| Velocity spike | >40% increase from average | Stories were over-estimated or scope was cut mid-sprint | Re-calibrate estimation baseline |
| High carry-over | >30% of planned points carried over for 2+ sprints | Systemic estimation bias or dependency issues | Re-estimate entire backlog with updated calibration |
| Blocked ratio | >25% of sprint points blocked at any time | Dependency mapping failure | Review and update dependency graph |

### When to Abort a Sprint

**[R9]** Abort the current sprint when ANY of these conditions are true:
1. A critical architecture flaw is discovered that invalidates 50%+ of sprint stories
2. External dependency becomes unavailable with no workaround and no ETA within the sprint
3. Requirements change so significantly that 50%+ of sprint stories are invalidated
4. Team capacity drops below 50% (key member unavailable) with no recovery within the sprint

**Abort procedure**: Document the reason, preserve all in-progress work on branches, return incomplete stories to backlog, and run an immediate retrospective before replanning.

### Escalation to Earlier Phases

Sometimes Phase 4 reveals that Phase 3 decisions were wrong:
- **Architecture change needed**: Write a new ADR, update architecture.md, re-estimate affected stories
- **Requirements change needed**: PM updates the PRD with `[SCOPE-CHANGE]` tag, affected stories are revised
- **Analysis gap found**: Document the gap, create a spike story, update the brief if necessary

The artifact chain is living — changes propagate upstream and downstream. Always update the source artifact, not just the code.

---

## Assumptions

- Implementation readiness gate has passed (PASS or CONDITIONAL PASS) before Phase 4 begins
- project-context.md is current and reflects all Phase 3 decisions
- At least one sprint's worth of stories exist with acceptance criteria before the first sprint starts

## Limits

- Phase 4 does NOT create new requirements — requirement gaps must be escalated to Phase 2
- Phase 4 does NOT make architecture decisions — those must be escalated to Phase 3 as new ADRs
- This guide does NOT cover production operations, incident response, or monitoring setup beyond what stories specify

## Edge Cases

- **First sprint with no velocity history**: Use team capacity estimate (e.g., 8 points per developer per sprint for AI-assisted development). Expect 30-50% variance. Calibrate after Sprint 1.
- **Solo developer doing all roles**: Combine sprint planning and retrospective into a single 15-minute journal entry. Skip formal ceremonies but keep the sprint-status.yaml updated.
- **Story acceptance criteria are ambiguous mid-implementation**: Stop implementation. Create a clarification request tagged `[AMBIGUITY]` in the sprint status. Do not guess — escalate to PM.

## Acceptance Criteria

- [ ] Sprint-status.yaml is updated at least daily during active sprints
- [ ] Every merged PR references a story ID in its commit message
- [ ] Definition of Done checklist passes for every completed story
- [ ] Retrospective is conducted at the end of every sprint with at least one action item

See also: `references/phase-3-solutioning.md`, `references/quick-flow.md`, `references/implementation-readiness-gate.md`, `references/progressive-context.md`
