# Artifact Flow Chain — Dependency Model

## Table of Contents
- [Overview](#overview)
- [The Full Chain](#the-full-chain)
- [What Each Artifact Provides Downstream](#what-each-artifact-provides-downstream)
- [Cross-Referencing Rules](#cross-referencing-rules)
- [Traceability Matrix](#traceability-matrix)
- [Impact Analysis](#impact-analysis)
- [Orphan Detection](#orphan-detection)
- [Validation Procedures](#validation-procedures)
- [Visual Flow Diagram](#visual-flow-diagram)

---

## Overview

The BMAD artifact flow chain is a directed dependency graph where each artifact builds upon its predecessors. This chain ensures traceability from business problem to working code — every line of code can be traced back to a requirement, which traces back to a validated user need.

**Core principle**: Upstream artifacts are the source of truth. When a conflict exists between artifacts at different levels, the upstream artifact wins unless a formal change propagates through the chain.

**Integrity rule**: No artifact in the chain should exist without its upstream dependency. A story without an epic is an orphan. An epic without PRD coverage is unjustified. Code without a story is rogue.

---

## The Full Chain

```
Phase 1          Phase 2          Phase 3                    Phase 4
────────         ────────         ────────                   ────────

Product    ───→  PRD        ───→  Architecture Doc    ───→   Sprint Code
Brief            Personas         ADRs                       Test Suites
                 UX Spec          Epics                      Sprint Status
                                  Stories
                                  project-context.md
```

### Chain Links

| From | To | Relationship |
|------|----|-------------|
| Product Brief | PRD | Brief's problem, users, and scope become PRD requirements |
| Product Brief | Personas | Brief's target users become detailed persona files |
| PRD | Architecture Doc | FRs and NFRs drive architectural decisions |
| PRD | Epics | FR groups become epics |
| PRD | UX Spec | UX requirements expand into interaction design |
| Architecture Doc | ADRs | Technology choices documented as decision records |
| Architecture Doc | project-context.md | Stack, conventions, constraints extracted |
| Epics | Stories | Each epic decomposes into implementable stories |
| Stories | Code | Each story becomes a feature branch with tests |
| ADRs | project-context.md | Decisions inform conventions and constraints |
| project-context.md | Code | All code must comply with project context |

---

## What Each Artifact Provides Downstream

### Product Brief → PRD

| Brief Section | PRD Usage |
|---------------|-----------|
| Problem Statement | Grounds the PRD introduction; provides the "why" |
| Target Users | Expanded into full persona documents |
| Success Metrics | Refined with SMART criteria in the PRD |
| Scope Boundaries | Directly copied and potentially expanded |
| Key Risks | Inherited and assigned to specific FRs or NFRs |
| Open Questions | Must be resolved or explicitly deferred in the PRD |
| Research Summary | Informs requirement prioritization |

### PRD → Architecture Document

| PRD Section | Architecture Usage |
|-------------|-------------------|
| Functional Requirements | Drive component design and API surface |
| Non-Functional Requirements | Shape technology selection, scaling strategy, security model |
| User Personas | Inform UX-impacting architectural decisions |
| Dependencies | Identify external systems for Context diagram (C4 Level 1) |
| Success Metrics | Inform monitoring and observability requirements |

### PRD → Epics

| PRD Section | Epic Usage |
|-------------|-----------|
| FR groups (by area code) | Each group becomes an epic |
| FR priorities (MoSCoW) | Epic ordering and sprint assignment |
| NFRs | Cross-cutting epics (e.g., EPIC-PERF, EPIC-SEC) |
| Scope boundaries | Out-of-scope items excluded from epic decomposition |

### Architecture Doc → Stories

| Architecture Section | Story Usage |
|---------------------|------------|
| Component design | Stories reference which components they affect |
| API design | Stories include API contract details |
| Data model | Stories reference entity schemas |
| ADRs | Stories cite ADRs when implementing decided patterns |

### Stories → Code

| Story Element | Code Usage |
|---------------|-----------|
| Acceptance criteria | Test cases (Given/When/Then maps to test structure) |
| Technical notes | Implementation guidance (libraries, patterns, constraints) |
| Dependencies | Build order and branch strategy |
| FR traceability | Code comments and commit messages reference FRs |

### project-context.md → Code

| Context Section | Code Usage |
|----------------|-----------|
| Tech Stack | Language, framework, library choices |
| Conventions | Naming, file organization, API patterns |
| Constraints | Hard limits on performance, bundle size, etc. |
| Exclusion Zones | Files the developer must not modify |

---

## Cross-Referencing Rules

### Rule 1: Forward References Use IDs

When an upstream artifact references a downstream artifact, use the artifact's ID:

```markdown
## In the PRD:
This requirement will be implemented in EPIC-AUTH.
See STORY-AUTH-001 through STORY-AUTH-005 for implementation details.
```

### Rule 2: Backward References Use Section Links

When a downstream artifact references an upstream artifact, cite the specific section:

```markdown
## In a Story file:
This story implements FR-AUTH-001 and FR-AUTH-002 from the PRD (Section 3.1).
Password hashing follows ADR-003.
```

### Rule 3: Cross-References Are Bidirectional

If Story A references FR-001, then FR-001's tracking should reflect that Story A implements it. This bidirectional linking enables impact analysis.

### Rule 4: Use Consistent ID Formats

| Artifact | ID Format | Example |
|----------|-----------|---------|
| Functional Requirement | FR-[AREA]-[NNN] | FR-AUTH-001 |
| Non-Functional Requirement | NFR-[CAT]-[NNN] | NFR-PERF-001 |
| Epic | EPIC-[AREA] | EPIC-AUTH |
| Story | STORY-[AREA]-[NNN] | STORY-AUTH-001 |
| ADR | ADR-[NNN] | ADR-003 |

### Rule 5: Never Reference by Position

Bad: "See the third requirement in Section 3."
Good: "See FR-AUTH-003."

Position-based references break when content is reordered.

---

## Traceability Matrix

The traceability matrix maps every FR to its implementing artifacts across the chain.

### Matrix Format

```
| FR ID        | Epic       | Story(ies)          | ADR(s)  | Status    |
|--------------|------------|---------------------|---------|-----------|
| FR-AUTH-001  | EPIC-AUTH  | STORY-AUTH-001      |         | Complete  |
| FR-AUTH-002  | EPIC-AUTH  | STORY-AUTH-001      | ADR-003 | Complete  |
| FR-AUTH-003  | EPIC-AUTH  | STORY-AUTH-002      |         | In Sprint |
| FR-SRCH-001  | EPIC-SRCH  | STORY-SRCH-001, 002| ADR-005 | Planned   |
| FR-SRCH-002  | EPIC-SRCH  | STORY-SRCH-003      |         | Planned   |
| NFR-PERF-001 | EPIC-INFRA | STORY-INFRA-004     | ADR-002 | Complete  |
```

### Matrix Rules

- Every FR must appear in at least one row
- Every story must trace to at least one FR
- NFRs can map to infrastructure stories or be cross-cutting constraints
- Status reflects the lowest-status implementing story
- The matrix is the single view for "are we building what we said we would?"

### Maintaining the Matrix

- Created during Phase 3 (story decomposition)
- Updated during Phase 4 (as stories move through sprints)
- Reviewed at sprint boundaries to catch drift
- Stored as `docs/traceability-matrix.md` or in a YAML format for automation

---

## Impact Analysis

When an upstream artifact changes, the impact must be traced through the chain.

### Change Propagation Rules

```
Brief changes → Review PRD (may need updates) → Review Architecture → Review Stories
PRD changes → Review Architecture → Review affected Stories → Review affected Code
Architecture changes → New ADR → Review affected Stories → Review affected Code
Story changes → Review implementing Code → Update traceability matrix
```

### Impact Analysis Template

```markdown
# Impact Analysis: [Change Description]

## Change Origin
Artifact: [e.g., PRD]
Section: [e.g., FR-AUTH-003]
Nature of change: [Added | Modified | Removed]

## Direct Impact
- [Artifact 1]: [What needs to change and why]
- [Artifact 2]: [What needs to change and why]

## Indirect Impact
- [Downstream artifact]: [Potential cascade effects]

## Affected Stories
| Story ID | Impact | Action Required |
|----------|--------|-----------------|
| STORY-AUTH-002 | AC modified | Update acceptance criteria |
| STORY-AUTH-005 | New story needed | Write new story for added FR |

## Risk Assessment
- Severity: [Low | Medium | High]
- Sprint impact: [None | Current sprint affected | Future sprints affected]
- Recommendation: [Proceed | Pause and re-plan]
```

### Impact Analysis Algorithm

**[R17]** When an upstream artifact changes, execute this algorithm:

1. **Identify changed artifact** and the specific section/field that changed
2. **Lookup downstream dependencies** using the Chain Links table above
3. **For each downstream artifact**: determine if the change invalidates, modifies, or has no effect on that artifact
4. **Score severity**: Count affected stories. 0 = Low, 1-3 = Medium, 4+ = High
5. **Generate impact report** using the template above
6. **Route to responsible agent**: PM for PRD changes, Architect for architecture changes, Dev for story/code changes
7. **Track resolution**: Every impact analysis must be resolved (all downstream artifacts updated) before the next sprint boundary

### Common Change Scenarios

| Scenario | Impact Path | Typical Severity |
|----------|-------------|-----------------|
| New FR added to PRD | New story needed; may need new epic | Medium |
| FR removed from PRD | Stories become orphans; remove from sprint | Low |
| NFR target tightened | Architecture may need revision; stories re-estimated | High |
| Technology swapped (new ADR) | project-context.md updated; affected stories revised | High |
| Persona updated | PRD priorities may shift; story ordering may change | Low-Medium |
| Scope boundary moved | FRs added or removed; cascade through chain | Medium-High |

### Versioning Rules for Artifacts

**[R18]** Every artifact in the chain must use semantic versioning in its frontmatter:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Typo fix, formatting, clarification | PATCH | PRD 1.0.0 -> 1.0.1 |
| New FR/NFR added, scope change, persona updated | MINOR | PRD 1.0.1 -> 1.1.0 |
| Problem statement changed, architecture style changed, fundamental redesign | MAJOR | PRD 1.1.0 -> 2.0.0 |

**[R19]** MAJOR version bumps in upstream artifacts require re-validation of ALL downstream artifacts. MINOR bumps require re-validation of directly dependent artifacts only. PATCH bumps require no downstream action.

### Conflict Resolution When Artifacts Diverge

When two artifacts at the same level contain contradictory information:

| Conflict Type | Resolution Rule |
|--------------|-----------------|
| PRD says Feature X is in-scope, architecture does not address it | Architecture must be updated to address Feature X (PRD wins for scope) |
| Architecture specifies PostgreSQL, project-context.md says MongoDB | Resolve immediately. The ADR that decided the database is the tie-breaker. Update the incorrect artifact. |
| Story acceptance criteria contradict PRD FR | PRD FR wins. Update the story AC to match. If the FR is wrong, update the FR first via scope change protocol. |
| Two stories implement the same FR with different approaches | PM decides which approach wins. Archive the other story. |

---

## Orphan Detection

Orphans are artifacts that have lost their upstream justification. They indicate chain breaks.

### Types of Orphans

| Orphan Type | Description | Detection |
|-------------|-------------|-----------|
| **Orphan Story** | Story that traces to no FR, or traces to a removed FR | Scan stories for FR references; cross-check against PRD |
| **Orphan Epic** | Epic with no associated FRs remaining | Check epic FR-coverage lists against current PRD |
| **Orphan Code** | Code implementing a story that was removed or never existed | Check feature branches and commits against story IDs |
| **Orphan ADR** | ADR for a technology no longer in the stack | Compare ADR technology references against project-context.md |
| **Unjustified FR** | FR that traces to no brief section or stakeholder need | Scan FRs for source references |

### Orphan Detection Protocol

Run at sprint boundaries and phase transitions:

1. **Forward scan**: For each FR in the PRD, verify at least one story implements it
2. **Backward scan**: For each story in the backlog, verify its FRs still exist in the PRD
3. **Code scan**: For each feature branch, verify its story ID exists and is active
4. **ADR scan**: For each ADR, verify the decision is still relevant

### Orphan Resolution

| Orphan | Resolution |
|--------|-----------|
| Orphan Story | Archive (do not delete) with note explaining why it was orphaned |
| Orphan Epic | Archive if all FRs removed; consolidate if FRs moved |
| Orphan Code | Revert or remove in a dedicated cleanup PR |
| Orphan ADR | Mark status as "Deprecated" with explanation |
| Unjustified FR | Either add upstream justification or remove from PRD |

---

## Validation Procedures

### Chain Integrity Validation

Run this checklist at the Phase 3 gate and at each sprint boundary:

```markdown
## Artifact Chain Validation

### Completeness (no gaps)
- [ ] Every brief section is addressed by at least one PRD section
- [ ] Every FR maps to at least one epic
- [ ] Every epic has at least one story
- [ ] Every story has acceptance criteria
- [ ] Every NFR has an architectural response in the architecture doc

### Consistency (no contradictions)
- [ ] Tech Stack in project-context.md matches architecture doc
- [ ] FR priorities in PRD match epic/story ordering
- [ ] NFR targets in PRD match constraints in project-context.md
- [ ] ADR decisions are reflected in project-context.md conventions

### Traceability (bidirectional links)
- [ ] Traceability matrix exists and is current
- [ ] Every FR can be traced forward to at least one story
- [ ] Every story can be traced backward to at least one FR
- [ ] No orphan stories exist in the backlog

### Currency (up-to-date)
- [ ] All artifacts reflect the latest changes
- [ ] No pending impact analyses are unresolved
- [ ] Open questions from brief are resolved or deferred in PRD
- [ ] Sprint status file reflects actual progress
```

### Automated Validation (Advanced)

For teams using BMAD at scale, validation can be scripted:

```
validate-chain.sh:
  1. Parse all FR IDs from prd.md
  2. Parse all STORY IDs from stories/ directory
  3. Cross-reference: every FR has a story, every story has an FR
  4. Report orphans and gaps
  5. Exit non-zero if validation fails (CI gate)
```

---

## Visual Flow Diagram

### ASCII Representation

```
┌──────────────┐
│ Product Brief │  Phase 1: ANALYSIS
│  - Problem    │
│  - Users      │
│  - Scope      │
│  - Risks      │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌────────────┐     ┌──────────┐
│     PRD      │────→│  Personas  │     │ UX Spec  │  Phase 2: PLANNING
│  - FRs       │     │  - Goals   │     │ - Flows  │
│  - NFRs      │     │  - Pains   │     │ - Wires  │
│  - Metrics   │     └────────────┘     └──────────┘
│  - Scope     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────┐     ┌─────────────────┐
│ Architecture │────→│   ADRs   │────→│project-context.md│  Phase 3: SOLUTIONING
│  - C4 Model  │     │ - Why?   │     │  - Stack         │
│  - Data Model│     │ - Alts   │     │  - Constraints   │
│  - API       │     └──────────┘     │  - Conventions   │
└──────┬───────┘                      └─────────────────┘
       │
       ▼
┌──────────────┐
│    Epics     │  (FR groups → Epics)
│  - EPIC-AUTH │
│  - EPIC-SRCH │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Stories    │  (Epics → Stories)
│  - AC: G/W/T │
│  - Points    │
│  - Deps      │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌────────────┐
│    Code      │────→│   Tests    │  Phase 4: IMPLEMENTATION
│  - Features  │     │ - Unit     │
│  - Branches  │     │ - Integ    │
│  - Commits   │     │ - E2E      │
└──────────────┘     └────────────┘
```

### Dependency Direction

Arrows flow downward: upstream artifacts constrain downstream artifacts. Changes propagate upward through impact analysis and downward through revision.

### Feedback Loops

While the primary flow is top-down, Phase 4 discoveries create feedback:
- Technical infeasibility discovered during implementation triggers architecture revision
- Missing requirements discovered during story implementation trigger PRD amendments
- User testing results (post-launch) feed back into the product brief for the next cycle

These feedback loops are formal — they follow the change propagation protocol, not ad-hoc modifications.

---

## Assumptions

- All artifacts are stored in Git and versioned with semantic versioning in frontmatter
- A traceability matrix is maintained and updated at sprint boundaries
- Cross-referencing uses stable IDs (FR-XXX, STORY-XXX), not positional references

## Limits

- This document does NOT prescribe how to organize artifact files on disk — see `references/project-context-guide.md` for directory structure
- This document does NOT cover runtime dependencies between services — only dependencies between documentation artifacts
- Automated validation scripts are recommended but not required; manual validation is acceptable for small projects

## Edge Cases

- **Brief was skipped (Quick Flow or abbreviated entry)**: The chain starts at the PRD level. Stories must still trace to FRs, but FRs do not trace to a brief section. Document this gap as `Source: Quick Flow entry` on affected FRs.
- **Legacy artifact with no version history**: Assign version 1.0.0 and begin versioning from that point. Do not attempt to reconstruct historical versions.
- **Artifact chain is broken mid-project (orphans discovered)**: Run the full orphan detection protocol. Resolve all orphans before the next gate evaluation. Do not proceed to Phase 4 with known orphans.

## Acceptance Criteria

- [ ] Traceability matrix exists and is current (updated within the last sprint)
- [ ] Every FR maps to at least one story (forward scan passes)
- [ ] Every story maps to at least one FR (backward scan passes)
- [ ] No orphan artifacts exist in the active backlog
- [ ] Impact analysis has been performed for every upstream artifact change since last review

See also: `references/methodology-overview.md`, `references/implementation-readiness-gate.md`, `references/schemas.md`
