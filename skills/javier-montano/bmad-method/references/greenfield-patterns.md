# Greenfield Patterns — Starting Fresh with BMAD

## Table of Contents
- [When to Use This Guide](#when-to-use-this-guide)
- [Full-Flow Walkthrough](#full-flow-walkthrough)
- [Recommended First Sprint Scope](#recommended-first-sprint-scope)
- [Bootstrapping from Zero](#bootstrapping-from-zero)
- [Technology Selection Without Bias](#technology-selection-without-bias)
- [Common Greenfield Mistakes](#common-greenfield-mistakes)
- [MVP Scoping](#mvp-scoping)
- [When to Use Quick Flow](#when-to-use-quick-flow)
- [Team Ramp-Up on BMAD](#team-ramp-up-on-bmad)

---

## When to Use This Guide

Use this guide when you are starting a new project from scratch — no existing code, no legacy constraints, no production users. Greenfield is where BMAD provides its maximum value because every artifact is built in order, every decision is documented from day one, and the implementation readiness gate has full coverage.

## Full-Flow Walkthrough

This section walks through the complete BMAD flow using a concrete example: building a task management API.

### Phase 1: Product Definition

**Participants**: Product Manager (PM) agent or human product owner.

**Step 1 — Product Brief**:
```markdown
Product: TaskFlow API
Problem: Development teams waste 30 minutes/day switching between
         task tools that don't integrate.
Solution: A unified REST API for task management with webhooks for
          integration with any tool.
Target users: Engineering teams (5-50 people) using 2+ task tools.
Success metric: Reduce daily tool-switching time by 50%.
```

**Step 2 — PRD Creation**:

The PM agent expands the brief into a full PRD:
- Problem statement with user research
- 3 user personas (Team Lead, Developer, Integration Engineer)
- 15 functional requirements (FR-001 through FR-015)
- Non-functional requirements (latency, scale, availability)
- Success metrics with baselines and targets
- Explicit out-of-scope items (no UI, no mobile app, API only)

**Step 3 — PRD Review**:

Review for completeness using the BMAD PRD checklist. Common findings at this stage:
- Missing edge case requirements (what happens when a task is assigned to a deactivated user?)
- Success metrics without baselines (how much time is currently spent?)
- Scope boundaries that are implicit rather than explicit

**Phase 1 output**: Committed PRD in `docs/prd.md`.

### Phase 2: Architecture

**Participants**: Architect agent or human architect.

**Step 1 — Architecture Draft**:

The Architect reads the PRD and proposes:
- Component diagram: API Gateway, Auth Service, Task Service, Webhook Service, PostgreSQL, Redis
- Technology choices: Node.js/Express, PostgreSQL 16, Redis 7, Docker
- Communication patterns: synchronous REST between API Gateway and services, async events for webhooks
- Data model: Users, Teams, Tasks, Webhooks, AuditLog

**Step 2 — Tech Stack Document**:
```markdown
Runtime: Node.js 20 LTS
Framework: Express 4.x with TypeScript
Database: PostgreSQL 16 (primary), Redis 7 (cache + queues)
Auth: JWT (RS256) with refresh tokens
Testing: Vitest (unit), Supertest (integration)
CI: GitHub Actions
Infrastructure: Docker Compose (dev), ECS Fargate (prod)
```

**Step 3 — Architecture Review**:

Cross-reference every PRD requirement against architecture components. Verify:
- FR-001 (Create task) -> Task Service + PostgreSQL
- FR-008 (Webhook notifications) -> Webhook Service + Redis queue
- NFR (p95 < 200ms) -> Redis caching layer justified

**Phase 2 output**: Committed architecture doc, tech stack, data model in `docs/`.

### Phase 3: Planning

**Participants**: PM agent (stories), Architect agent (gate review).

**Step 1 — Story Decomposition**:

Break the PRD into implementable stories. For TaskFlow:
- S-001: Project scaffolding and dev environment
- S-002: User registration and authentication
- S-003: Team creation and member management
- S-004: Task CRUD operations
- S-005: Task assignment and status transitions
- S-006: Task filtering and search
- S-007: Webhook registration
- S-008: Webhook event delivery
- S-009: API rate limiting
- S-010: Audit logging

Each story includes acceptance criteria in Given/When/Then format.

**Step 2 — Implementation Readiness Gate**:

Run the full 13-step gate (see `implementation-readiness-gate.md`). In greenfield projects, this often catches:
- Missing API contracts (Step 8) — stories reference endpoints not yet defined
- Incomplete data model (Step 9) — architecture shows entities but no field-level detail
- No rollback plan (Step 13) — easy to forget when there is no production system yet

**Step 3 — Gate Remediation**:

Fix any WARN or FAIL items. For greenfield, this typically means filling in the API contract document and adding field-level detail to the data model.

**Phase 3 output**: Story files in `docs/stories/`, gate report.

### Phase 4: Implementation

**Participants**: Developer agent or human developer.

Execute stories in dependency order:
1. S-001 (scaffolding) — no dependencies
2. S-002 (auth) — depends on S-001
3. S-003 (teams) — depends on S-002
4. S-004 (tasks) — depends on S-003
5. ... and so on

Each story implementation follows:
1. Load story + relevant architecture section + API contract
2. Implement code
3. Write tests matching acceptance criteria
4. Verify all acceptance criteria pass
5. Commit with story reference

## Recommended First Sprint Scope

For greenfield BMAD projects, the first sprint should be deliberately small to validate the flow:

**Sprint 1 scope** (1-2 weeks):
- Complete Phase 1 and Phase 2
- Write stories for the first 3-4 features only
- Pass the gate for those stories
- Implement S-001 (scaffolding) and S-002 (one core feature)

**Why this scope works**:
- The team experiences the full BMAD lifecycle in one sprint.
- Problems with templates, agents, or process surface early.
- The first demo shows working software, not just documents.
- Momentum builds from completing the full cycle, not from producing paperwork.

**What NOT to do in Sprint 1**:
- Do not write all stories for the entire product upfront.
- Do not try to perfect every document before implementing anything.
- Do not skip the gate "because we're just getting started."

## Bootstrapping from Zero

The literal first steps when starting a greenfield BMAD project:

### Step 1: Create the Repository

```
my-project/
  docs/
    prd.md                  (Phase 1 output)
    architecture.md         (Phase 2 output)
    tech-stack.md           (Phase 2 output)
    data-model.md           (Phase 2 output)
    api-contracts.md        (Phase 2 output)
    stories/
      S-001-scaffolding.md  (Phase 3 output)
      S-002-auth.md
      ...
  project-context.md        (always-load file, updated each phase)
  src/                      (Phase 4 output)
  tests/
```

### Step 2: Initialize project-context.md

Start with a minimal project-context.md:

```markdown
# Project Context — [Project Name]

## Overview
[One sentence: what this project will do]

## Current State
Phase 1 — Product Definition in progress.

## Technology Stack
To be determined in Phase 2.

## Architecture
To be determined in Phase 2.

## Key Decisions
(none yet)

## Artifact Links
- PRD: docs/prd.md (in progress)
```

This file grows with each phase. By Phase 4 it contains the full project summary.

### Step 3: Run Phase 1

Use the PM agent or work manually with the BMAD PRD template. Commit the PRD. Update project-context.md.

### Step 4: Continue Through Phases

Each phase produces artifacts that go into Git. project-context.md is updated at each phase boundary.

## MVP Scoping Framework

**[R30]** Use this framework to scope the MVP before entering Phase 3:

### Step 1: Classify All Requirements

Tag every FR in the PRD with a priority:
- **P0 (Ship-blocking)**: The product is useless without this. Absolute minimum for launch.
- **P1 (High-value)**: Significant user value but product functions without it.
- **P2 (Nice-to-have)**: Enhancement that can wait for a future sprint.

### Step 2: Apply the MVP Constraint

**[R31]** The MVP must satisfy ALL of these constraints:
- Contains only P0 requirements
- Can be implemented in 2-4 sprints (4-8 weeks)
- Has no more than 10 stories total
- Demonstrates the core value proposition to at least one user persona

### Step 3: Validate MVP Completeness

Ask: "Can a user of the primary persona accomplish their primary goal using only MVP features?" If no, a P1 requirement must be promoted to P0.

### First-Sprint Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|-------------|-------------|-----|
| Starting with UI before API | Backend contract changes cascade to UI rework | Build API + tests first, UI in Sprint 2 |
| All stories are 5+ points | No quick wins, morale risk, no early velocity signal | Include at least 2 stories at 1-2 points (scaffolding, config) |
| No infrastructure story | Dev environment is not reproducible | Sprint 1 always starts with STORY-INFRA-001 (project scaffolding) |
| Over-engineering auth | Building OAuth, MFA, social login for MVP | Start with email/password only. Add OAuth post-MVP. |
| Skipping the gate "because we just started" | Missing API contracts, undefined data model | Gate takes 30-60 minutes and saves days of rework. Run it. |

## Technology Selection Without Bias

Greenfield projects face a critical risk: technology selection driven by familiarity or hype rather than requirements.

### BMAD Approach to Tech Selection

1. **Start from NFRs, not preferences**. If the PRD requires sub-10ms response times, that constrains the technology. If it requires rapid prototyping, that constrains differently.

2. **Document the decision matrix** with explicit weights derived from project priorities:

```markdown
| Criterion (from PRD) | Weight | Option A: Node.js | Option B: Go | Option C: Python |
|---------------------|--------|-------------------|--------------|-----------------|
| Team expertise | 0.3 | 9 | 3 | 7 |
| Latency requirements | 0.25 | 7 | 9 | 5 |
| Ecosystem (libraries) | 0.2 | 8 | 6 | 9 |
| Hiring pool | 0.15 | 8 | 5 | 8 |
| Long-term maintenance | 0.1 | 7 | 8 | 6 |
| **Weighted Score** | | **7.85** | **5.75** | **6.9** |
```

3. **Record the decision in project-context.md** with rationale:
```
Decision 1: Node.js 20 for backend runtime.
Rationale: Highest weighted score driven by team expertise (0.3 weight)
and strong ecosystem. Go scored higher on latency but team has zero
Go experience, making the ramp-up cost prohibitive for MVP timeline.
```

4. **Revisit at scale milestones**, not continuously. The technology choice is settled until a predefined threshold forces re-evaluation (e.g., latency exceeds acceptable limits at 10x initial scale).

## Common Greenfield Mistakes

### Mistake 1: Over-Engineering

**Symptom**: Designing a microservice architecture for an application that will serve 100 users.
**BMAD guard**: The architecture review step cross-references NFRs. If the NFR says "support 100 concurrent users," a monolith with a single database is the correct architecture. The Architect agent should flag over-engineering.
**Fix**: Match architecture complexity to actual requirements, not imagined future requirements. Document scale triggers for when the architecture should evolve.

### Mistake 2: Premature Optimization

**Symptom**: Implementing Redis caching, CDN configuration, and database read replicas before the first user signs up.
**BMAD guard**: Stories should not include optimization work until the performance NFR is at risk. Optimization stories belong in a later sprint, triggered by actual performance data.
**Fix**: First sprint stories focus on correctness. Performance stories are created when load testing reveals bottlenecks.

### Mistake 3: Scope Creep in Phase 1

**Symptom**: The PRD grows from 15 requirements to 45 during review. Features keep getting added because "while we're at it, we should also..."
**BMAD guard**: The PRD has an explicit out-of-scope section. The PM agent should push back on additions that were not in the original product brief.
**Fix**: Maintain a "Future Considerations" section. Items can move to this section without being lost, but they do not enter the current scope.

### Mistake 4: Skipping the Gate

**Symptom**: The team is eager to code and skips the implementation readiness gate because "everything looks good."
**Consequence**: Missing API contracts, inconsistent data models, or undefined deployment strategy discovered mid-implementation.
**Fix**: The gate takes 30-60 minutes for a well-prepared project. This investment saves days of rework. Make the gate non-negotiable.

### Mistake 5: Gold-Plating Phase 1-2

**Symptom**: Spending 3 weeks on the PRD and architecture for an MVP that should ship in 4 weeks.
**BMAD guard**: Use the quick flow for small projects (see below). Phase 1-2 for an MVP should take 1-2 days, not weeks.
**Fix**: Timebox each phase. Phase 1: 1 day for MVP, 3 days for larger projects. Phase 2: 1 day for MVP, 3-5 days for larger projects.

## MVP Scoping

BMAD provides a structured approach to cutting scope without cutting corners.

### The MVP Funnel

```
Product Brief (broad vision)
  └─> PRD (all requirements, tagged by priority)
        └─> MVP PRD (P0 requirements only)
              └─> MVP Stories (minimum set for P0)
                    └─> MVP Implementation
```

### Priority Tagging in the PRD

Every functional requirement gets a priority tag:

- **P0 — Must have**: The product is unusable without this. Ship-blocking.
- **P1 — Should have**: Significant value but the product works without it. Next sprint.
- **P2 — Nice to have**: Enhances experience but can wait. Future sprint.

The MVP includes only P0 requirements. P1 and P2 stay in the PRD for later sprints but are excluded from Phase 3 story creation in the first iteration.

### Example MVP Scope (TaskFlow API)

Full PRD: 15 requirements. MVP scope: 6 requirements.

| Requirement | Priority | In MVP? |
|-------------|----------|---------|
| Create/read/update tasks | P0 | Yes |
| User authentication | P0 | Yes |
| Team creation | P0 | Yes |
| Task assignment | P0 | Yes |
| Task filtering | P1 | No |
| Webhook integration | P1 | No |
| Audit logging | P2 | No |
| Rate limiting | P1 | No |
| Task search (full-text) | P2 | No |

### MVP Gate Adaptation

The implementation readiness gate still applies to MVPs, but with adjusted expectations:
- Deployment strategy can be simplified (single environment is acceptable for MVP).
- Performance targets should reflect MVP scale, not production scale.
- Rollback plan can be "redeploy previous version" without elaborate data migration.

## When to Use Quick Flow

BMAD offers a quick flow variant for projects that do not need the full ceremony:

### Quick Flow Criteria

Use quick flow when ALL of these are true:
- Solo developer or pair
- Project scope is under 2 weeks
- No compliance or audit requirements
- No external stakeholders who need documentation
- The developer has strong domain expertise

### Quick Flow Steps

1. **Product brief** (30 min) — One page describing what you are building and why.
2. **Architecture sketch** (30 min) — Component list, tech stack, data model. No formal document.
3. **Story list** (30 min) — Numbered list with acceptance criteria. No individual story files.
4. **Mini gate** (15 min) — Quick pass through steps 1, 2, 8, 10 of the full gate (PRD, architecture, API contracts, security).
5. **Implement** — Build with story list as your guide.

### Quick Flow Limitations

- No retroactive traceability (hard to audit later).
- No multi-agent benefits (single person does everything).
- Difficult to hand off to another developer.
- Cannot be promoted to full BMAD flow without retroactive documentation.

### Quick Flow to Full BMAD Escalation

If a quick flow project grows beyond its original scope, escalate to full BMAD:
1. Convert the product brief to a proper PRD.
2. Formalize the architecture sketch into a document.
3. Break the story list into individual story files.
4. Run the full 13-step gate.
5. Continue with full BMAD from that point forward.

## Team Ramp-Up on BMAD

### For Solo Developers

1. Read the methodology overview (30 minutes).
2. Run through one greenfield project using quick flow (half day).
3. Run through one greenfield project using full flow (1-2 days).
4. You are now BMAD-proficient.

### For Small Teams (2-5)

1. One team member becomes the BMAD champion — reads all reference docs.
2. Champion walks the team through the methodology overview (1 hour meeting).
3. Team does a pilot project together using full BMAD flow (1 sprint).
4. Retrospective on the pilot — what worked, what needs customization.
5. Team adopts BMAD for all new work. Customize templates based on retro feedback.

### For Larger Teams (6+)

1. Identify BMAD champions (1 per 5 developers).
2. Champions complete solo ramp-up (see above).
3. Champions train their sub-teams.
4. Run parallel pilots — each sub-team does one BMAD project.
5. Cross-team retrospective to align on shared conventions.
6. Establish shared project-context.md and architecture patterns across teams.
7. See `enterprise-governance.md` for multi-team governance.

### Common Ramp-Up Mistakes

- **Reading everything before doing anything**: BMAD is learned by doing. Read the overview, then start a project.
- **Customizing before understanding**: Use BMAD as-is for your first project. Customize after you understand what each part does and why.
- **Treating BMAD as mandatory bureaucracy**: If a step does not add value for your context, it must be removed or simplified. See `references/customization-guide.md`.

### Technology Selection Decision Matrix (with default weights)

| Criterion | Default Weight | Justification for Weight |
|-----------|---------------|------------------------|
| Team expertise | 0.30 | Highest weight: unfamiliar tech adds 2-3x development time |
| Latency requirements (from NFRs) | 0.25 | Directly impacts user experience and NFR compliance |
| Ecosystem maturity (libraries, tools) | 0.20 | Affects development speed and maintainability |
| Hiring pool / community size | 0.15 | Impacts long-term team scaling |
| Long-term maintenance cost | 0.10 | Lower weight for MVP; increase for long-lived products |

**[R32]** Adjust weights based on project context. Document weight changes with rationale in the ADR. The sum of weights must equal 1.0.

---

## Assumptions

- The team is starting from zero — no existing code, no legacy constraints
- At least one team member has experience with the selected tech stack (or a spike story is planned)
- The project has a defined timeline (MVP deadline or sprint cadence)

## Limits

- This guide does NOT cover ongoing operations (monitoring, incident response, on-call)
- This guide does NOT cover multi-team coordination — see `references/enterprise-governance.md`
- Technology selection guidance here is framework-agnostic — no specific stack is recommended

## Edge Cases

- **Solo developer with no team to calibrate estimates**: Use 8 points per sprint as the initial capacity assumption. Calibrate after Sprint 1. Expect first-sprint velocity to be 50-70% of estimate.
- **Greenfield project with regulatory requirements from day one**: Do not use Quick Flow or MVP partial gate. Run full BMAD with all 13 gate steps. Add domain-specific gate steps per `references/customization-guide.md`.
- **Project scope changes dramatically after Phase 2**: Re-run Phase 1 with the new scope. Do not patch the existing PRD — create a new version (MAJOR version bump).

## Acceptance Criteria

- [ ] MVP scope is defined with only P0 requirements (P1/P2 explicitly deferred)
- [ ] Technology selection is documented in an ADR with a weighted decision matrix
- [ ] First sprint includes a scaffolding story (STORY-INFRA-001)
- [ ] Implementation readiness gate passes before Sprint 1 implementation begins
- [ ] project-context.md is initialized and updated at each phase boundary

See also: `references/methodology-overview.md`, `references/brownfield-patterns.md`, `references/customization-guide.md`, `references/implementation-readiness-gate.md`
