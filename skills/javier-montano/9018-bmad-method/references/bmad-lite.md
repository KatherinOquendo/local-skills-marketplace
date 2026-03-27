# BMAD Lite — Simplified BMAD for Solo Developers

## Table of Contents
- [What is BMAD Lite](#what-is-bmad-lite)
- [What to Keep vs What to Skip](#what-to-keep-vs-what-to-skip)
- [Compressed Workflow](#compressed-workflow)
- [Solo Agent Model](#solo-agent-model)
- [Gate Simplification](#gate-simplification)
- [Artifact Templates (Lite)](#artifact-templates-lite)
- [When to Upgrade to Full BMAD](#when-to-upgrade-to-full-bmad)
- [Concrete Example: Weekend Project](#concrete-example-weekend-project)
- [BMAD Lite vs Quick Flow](#bmad-lite-vs-quick-flow)

---

## What is BMAD Lite

BMAD Lite is the minimum viable subset of BMAD for solo developers working on small-scope projects (1-4 week timeline, single developer, no compliance requirements). It preserves the core value propositions — documentation-first, constrained generation, traceability — while eliminating multi-agent coordination overhead.

**Target audience**: Solo developers building personal projects, MVPs, weekend experiments, internal tools, or proof-of-concepts.

**Core guarantee**: Even at minimum BMAD, every line of code traces to a requirement, and every requirement traces to a stated problem. This traceability costs 30-60 minutes of planning and saves hours of rework.

**What BMAD Lite is NOT**: An excuse to skip thinking. Lite reduces ceremony, not rigor. The planning that remains is the planning that matters most.

---

## What to Keep vs What to Skip

### Must Keep (non-negotiable in any BMAD variant)

| Element | Why It Cannot Be Skipped |
|---------|-------------------------|
| project-context.md | Without it, the AI has no constraints. Every session starts from zero. |
| Combined Brief+PRD (Lite PRD) | Without requirements, you are doing prompt-and-pray (AP-01). |
| Stories with acceptance criteria | Without testable AC, you cannot verify what "done" means. |
| Git-based artifact versioning | Without version control, you lose the ability to revert, trace, and audit. |
| Definition of Done | Without DoD, stories accumulate as "mostly done" forever. |

### Skip or Compress

| Full BMAD Element | Lite Treatment | Rationale |
|-------------------|---------------|-----------|
| Phase 1 (Analysis) | Skip entirely | Solo dev already understands the problem. If you don't, you need Full BMAD, not Lite. |
| Separate Product Brief | Merge into Lite PRD | One document instead of two. The brief's problem statement becomes the PRD's introduction. |
| Personas / UX Spec | Skip unless user-facing | Internal tools and APIs do not need persona documents. |
| Full Architecture Document | Replace with Architecture Section in project-context.md | A solo project's architecture fits in 20-30 lines. No separate document needed. |
| ADRs | Skip for projects with <3 technology decisions. Keep for decisions you might question later. | If you chose Next.js and PostgreSQL and that is your entire stack, no ADR is needed. If you chose an unusual pattern, document why. |
| Epics | Skip entirely | Epics organize multi-team work. Solo projects have 5-15 stories max — flat backlog is sufficient. |
| 13-Step Gate | Replace with 5-Step Lite Gate | 8 of the 13 steps address multi-team concerns (deployment strategy, rollback plan, risk register) that solo projects handle implicitly. |
| Sprint ceremonies | Replace with a 10-minute daily journal entry | No standup, no formal retro. Just: what did I do, what is next, any blockers? |
| Multiple agent personas | Replace with Solo Agent Model (role cycling) | One person, one AI session. Cycle through perspectives instead of switching agents. |
| Sprint-status.yaml | Keep but simplified — 3 fields per story | Status tracking matters even solo. |
| Traceability matrix | Implicit — story `fr-refs` provide traceability | No separate matrix file needed if stories reference FRs correctly. |
| Enterprise governance | Skip entirely | No compliance, no multi-team coordination needed. |

---

## Compressed Workflow

BMAD Lite compresses 4 phases into 3 stages:

```
Stage 1: DEFINE (replaces Phase 1 + Phase 2)
  Time: 30-60 minutes
  Output: Lite PRD + project-context.md

Stage 2: DESIGN (replaces Phase 3)
  Time: 30-60 minutes
  Output: Stories with AC + Architecture section in project-context.md
  Lite Gate: 5-step check before coding

Stage 3: BUILD (replaces Phase 4)
  Time: Remainder of project
  Output: Working code with tests
  Cycle: Pick story → Write tests → Implement → Self-review → Mark done
```

### Stage 1: DEFINE

**Session setup**: Start a new AI session. Load nothing (project does not exist yet).

**Step 1 — Write the Lite PRD** (20-40 minutes):
1. State the problem in 2-3 sentences
2. List the target user (1 persona, 3-5 bullet points)
3. Write 5-15 functional requirements as "The system SHALL..." statements
4. Write 2-5 non-functional requirements with specific numbers
5. Define scope boundaries: what is explicitly out of scope (at least 3 items)
6. Define 2-3 measurable success metrics

**Step 2 — Write project-context.md** (10-20 minutes):
1. Project name and one-line description
2. Tech stack with versions
3. Architecture overview (component list, 1 line each)
4. Constraints (performance, security, budget, time)
5. Conventions (naming, file structure, code style)
6. Links to Lite PRD and story files

### Stage 2: DESIGN

**Session setup**: Load project-context.md and Lite PRD.

**Step 1 — Write stories** (20-40 minutes):
1. Decompose FRs into 5-15 stories (no epics — flat backlog)
2. Each story: title, 1-3 acceptance criteria in Given/When/Then, points (1-5), fr-refs
3. Order stories by dependency, then priority
4. Verify: every FR has at least one story; every story has at least one FR

**Step 2 — Architecture section** (10-20 minutes):
1. Add to project-context.md: component list, data model summary, API surface
2. If >2 technology choices were non-obvious, write a brief ADR (5-10 lines each)

**Step 3 — Run the Lite Gate** (5 minutes):
1. See [Gate Simplification](#gate-simplification) below

### Stage 3: BUILD

**Session setup**: Load project-context.md and the current story file only.

**Per-story cycle**:
1. Read the story and its acceptance criteria
2. Write failing tests from the AC (TDD)
3. Implement the minimum code to pass tests
4. Run the full test suite
5. Self-review using the Quick Flow checklist (see `references/quick-flow.md#self-review-checklist`)
6. Commit with story ID in the message
7. Update sprint-status.yaml (change story status to `done`)
8. Pick the next story

**End-of-project**: Review all stories. Verify all are `done`. Run the full test suite one final time.

---

## Solo Agent Model

Instead of switching between 8 agents, the solo developer cycles through 3 perspectives within a single session:

### Perspective 1: Planner (combines Mary + John + Sally)
**Activate when**: Writing the Lite PRD, defining requirements, setting scope
**Mindset**: "What problem am I solving? For whom? What does done look like?"
**Constraints**: Do not think about implementation. Do not pick technologies. Focus only on WHAT, not HOW.

### Perspective 2: Architect (combines Winston + Bob)
**Activate when**: Writing stories, choosing technologies, designing the data model
**Mindset**: "How will I build this? What are the trade-offs? What could go wrong?"
**Constraints**: Do not write code. Do not skip stories. Document every non-obvious technology choice.

### Perspective 3: Builder (combines Amelia + Quinn + Barry)
**Activate when**: Writing tests, implementing code, self-reviewing
**Mindset**: "Does this code satisfy the acceptance criteria? Is it tested? Does it follow conventions?"
**Constraints**: Do not add features not in a story. Do not modify the PRD or architecture. If something is missing, stop and go back to Perspective 2.

### How to Cycle

```
Session 1: Perspective 1 → Output: Lite PRD, project-context.md
Session 2: Perspective 2 → Output: Stories, architecture section
Session 3+: Perspective 3 → Output: Code, tests, completed stories
```

**Rule**: Never mix perspectives within a single session. If you are coding (Builder) and realize a requirement is missing, stop coding. Start a new session as Planner. Add the requirement to the Lite PRD. Then start a new Builder session.

---

## Gate Simplification

The 13-step gate compresses to 5 steps for BMAD Lite. Each step takes <1 minute.

### Lite Gate (5 Steps)

| # | Check | PASS If | FAIL If |
|---|-------|---------|---------|
| 1 | **Requirements exist** | Lite PRD has 5+ FRs, all in "SHALL" format, all testable | Missing FRs, vague language, no measurable NFRs |
| 2 | **Stories cover requirements** | Every FR maps to at least 1 story; every story maps to at least 1 FR | Orphan stories or uncovered FRs exist |
| 3 | **Acceptance criteria are testable** | Every story has Given/When/Then criteria with specific values | Subjective criteria ("should work well") |
| 4 | **Tech stack is defined** | project-context.md lists languages, frameworks, database, and versions | Undecided technology choices remain |
| 5 | **Scope boundaries are clear** | Lite PRD lists at least 3 out-of-scope items | No out-of-scope section, or it is empty |

### Lite Gate Rules

- All 5 steps must PASS. There is no WARN state in Lite — only PASS or FAIL.
- If any step FAILs, fix it before writing any code. This takes 5-15 minutes, not hours.
- No override procedure exists in Lite. If you cannot pass 5 simple checks, you are not ready to code.
- No gate report file is generated. The gate is a mental checklist, not an artifact.

---

## Artifact Templates (Lite)

### Lite PRD Template

```markdown
# [Project Name] — Lite PRD

## Problem
[2-3 sentences: what problem does this solve and for whom?]

## User
[Single persona: name, role, 3-5 bullet points about their needs and constraints]

## Functional Requirements
| ID | Requirement | Priority |
|----|------------|----------|
| FR-001 | The system SHALL [verb] [object] when [condition] | Must |
| FR-002 | ... | Must |
| FR-003 | ... | Should |

## Non-Functional Requirements
| ID | Category | Target |
|----|----------|--------|
| NFR-001 | Performance | API response < 200ms p95 |
| NFR-002 | Security | All inputs validated, no SQL injection |

## Out of Scope
- [Specific feature or capability NOT being built]
- [Another exclusion]
- [Another exclusion]

## Success Metrics
- [Metric 1 with target number]
- [Metric 2 with target number]
```

### Lite Story Template

```markdown
---
story-id: S-001
title: [Short title]
status: draft
points: [1-5]
fr-refs:
  - FR-001
---

# S-001: [Short title]

## Acceptance Criteria

### AC1: [Name]
- **Given** [precondition with specific value]
- **When** [user action or system event]
- **Then** [expected result with specific value]

### AC2: [Name]
- **Given** [precondition]
- **When** [action]
- **Then** [result]
```

### Lite Sprint Status

```yaml
# sprint-status.yaml (Lite)
project: [Project Name]
stories:
  - id: S-001
    title: [Title]
    status: todo  # todo | doing | done
  - id: S-002
    title: [Title]
    status: doing
```

---

## When to Upgrade to Full BMAD

Upgrade from Lite to Full BMAD when ANY of these conditions become true:

| Signal | Why It Requires Full BMAD |
|--------|--------------------------|
| A second developer joins | Multi-person coordination requires explicit agent roles, shared artifacts, and formal ceremonies |
| Project exceeds 15 stories | Flat backlog becomes unwieldy. Epics provide necessary structure. |
| Architecture has 5+ components | Simple architecture section is insufficient. A full architecture document with C4 diagrams is needed. |
| Project has compliance requirements | SOC2, HIPAA, or audit requirements need enterprise governance artifacts |
| Rework rate exceeds 20% | Lite planning was insufficient. Full BMAD's deeper analysis and gate prevent rework. |
| Project timeline exceeds 4 weeks | Multi-sprint projects need velocity tracking, carry-over management, and retrospectives |
| 3+ ADRs are needed | Many technology decisions indicate architectural complexity beyond Lite scope |
| A Quick Flow fix introduces a regression | The project has reached complexity where Quick Flow is insufficient for changes |

### Upgrade Protocol

Export current Lite PRD as starting point for full PRD. Group existing stories into epics. Expand architecture section into a full document. Create a traceability matrix. Run the full 13-step gate. Switch from solo perspective cycling to proper agent activation. Stories keep their IDs throughout the upgrade.

---

## Concrete Example: Weekend Project

### Project: Personal Bookmark Manager API

**Timeline**: Saturday + Sunday (16 hours total)
**Developer**: Solo
**Stack**: Node.js + Express + SQLite

#### Stage 1: DEFINE (45 minutes, Saturday morning)

**Lite PRD**:
```markdown
# Bookmark Manager API — Lite PRD

## Problem
I have bookmarks scattered across 4 browsers and 3 devices.
I need a single API to store, tag, and search bookmarks.

## User
Dev (me): Full-stack developer who wants a REST API to
manage bookmarks from any device via curl or a future UI.

## Functional Requirements
| ID | Requirement | Priority |
|----|------------|----------|
| FR-001 | The system SHALL create a bookmark with URL, title, and optional tags | Must |
| FR-002 | The system SHALL list all bookmarks with pagination (20 per page) | Must |
| FR-003 | The system SHALL search bookmarks by title substring (case-insensitive) | Must |
| FR-004 | The system SHALL filter bookmarks by tag | Must |
| FR-005 | The system SHALL delete a bookmark by ID | Must |
| FR-006 | The system SHALL update a bookmark's title and tags | Should |
| FR-007 | The system SHALL export all bookmarks as JSON | Should |

## Non-Functional Requirements
| ID | Category | Target |
|----|----------|--------|
| NFR-001 | Performance | All endpoints < 100ms for 1000 bookmarks |
| NFR-002 | Data | SQLite database, single file, portable |
| NFR-003 | Validation | All inputs validated, URL format enforced |

## Out of Scope
- User authentication (single-user, local only)
- Frontend UI (API only for now)
- Browser extension
- Import from browser bookmark files

## Success Metrics
- API handles 1000 bookmarks without degradation
- All 7 FRs implemented and tested within 16 hours
```

**project-context.md**: Vision (1 line), Tech Stack (Node 20.x, Express 4.x, SQLite via better-sqlite3, Vitest, zod), Architecture (4 components: API Layer, Service Layer, Data Layer, Validation — each with file path), Constraints (no auth, single SQLite file, no ORM), Conventions (TypeScript strict, kebab-case files, /api/bookmarks/* routes, standard error object).

#### Stage 2: DESIGN (30 minutes, Saturday morning)

**Stories** (7 stories, 16 total points, flat backlog):

| ID | Title | Pts | FR | Key AC |
|----|-------|-----|-----|--------|
| S-001 | Create bookmark endpoint | 3 | FR-001 | POST /api/bookmarks with {url, title, tags[]} returns 201; invalid URL returns 400 |
| S-002 | List with pagination | 2 | FR-002 | GET ?page=1 returns 20 items + next link; page=2 returns remainder |
| S-003 | Search by title | 2 | FR-003 | GET ?q=react returns only title-matching bookmarks (case-insensitive) |
| S-004 | Filter by tag | 2 | FR-004 | GET ?tag=dev returns only dev-tagged bookmarks |
| S-005 | Delete bookmark | 1 | FR-005 | DELETE /1 returns 204; DELETE /999 returns 404 |
| S-006 | Update bookmark | 2 | FR-006 | PATCH /1 with {title: "New"} returns 200 with updated object |
| S-007 | Export as JSON | 1 | FR-007 | GET /export returns full array, no pagination |

Each story file contains full Given/When/Then AC with specific values (not shown here for brevity).

**Lite Gate** (5 minutes):
1. Requirements exist: 7 FRs, all in SHALL format, all testable. PASS.
2. Stories cover requirements: All 7 FRs mapped. No orphans. PASS.
3. AC are testable: All Given/When/Then with specific values. PASS.
4. Tech stack defined: Node.js 20.x, Express 4.x, SQLite, Vitest. PASS.
5. Scope boundaries: 4 explicit exclusions. PASS.

Gate result: PASS. Begin implementation.

#### Stage 3: BUILD (14 hours, Saturday afternoon through Sunday)

Implementation order follows dependencies: S-001 (setup + create, 2h) then S-002 (list, 1.5h) then S-005 (delete, 45m) on Saturday. S-003 (search, 1h), S-004 (filter, 1h), S-006 (update, 1h) on Sunday morning. S-007 (export, 30m) + final test suite + cleanup (1h) on Sunday afternoon. Total: ~9 hours implementation with 5 hours buffer.

---

## BMAD Lite vs Quick Flow

| Dimension | BMAD Lite | Quick Flow |
|-----------|-----------|------------|
| Scope | Entire small project (5-15 stories) | Single change (1-3 files) |
| Planning | Lite PRD + stories upfront | Rapid spec per change |
| Duration | 1-4 weeks | Minutes to 2 hours |
| Architecture | Simplified but documented | None (works within existing) |
| Gate | 5-step Lite Gate | Self-review checklist |
| When to use | New projects, MVPs, proof-of-concepts | Fixes and small enhancements to existing projects |

Quick Flow is a change-level tool. BMAD Lite is a project-level framework. They are complementary: use Lite for the initial build, then use Quick Flow for subsequent small changes.

---

## Assumptions

- The developer is working alone (no multi-person coordination required)
- The project is small enough to hold the full architecture in project-context.md (<30 lines)
- No compliance, regulatory, or audit requirements apply
- The developer has basic familiarity with agile concepts (stories, acceptance criteria)

## Limits

- BMAD Lite does NOT scale to teams — upgrade to Full BMAD when a second developer joins
- BMAD Lite does NOT provide enterprise governance artifacts (audit trails, compliance records)
- BMAD Lite does NOT include formal retrospectives — the solo developer relies on self-assessment
- BMAD Lite does NOT produce gate report files — the gate is a mental checklist

## Acceptance Criteria

- [ ] A solo developer can complete Stage 1 (DEFINE) in under 60 minutes
- [ ] A solo developer can complete Stage 2 (DESIGN) in under 60 minutes
- [ ] The Lite Gate takes under 5 minutes to evaluate
- [ ] Every story produced in Lite still has fr-refs (traceability preserved)
- [ ] The concrete example demonstrates end-to-end Lite BMAD for a real project
- [ ] Upgrade signals are clear and actionable (not "when it feels complex")

See also: `references/methodology-overview.md`, `references/quick-flow.md`, `references/customization-guide.md`, `references/progressive-context.md`, `references/project-context-guide.md`
