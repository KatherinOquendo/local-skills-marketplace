# Story Readiness Checklist (Definition of Ready)

**Purpose**: Verify a story is ready to enter a sprint and begin development.
**Gate owner**: PM agent (John) or Scrum Master agent (Bob).
**Rule**: A story that fails any item must not be pulled into a sprint. Fix the gap first.

---

## INVEST Criteria

- [ ] **Independent** — the story can be developed and delivered without waiting on another in-progress story (all `blocked-by` dependencies are `done`)
- [ ] **Negotiable** — the story describes desired behavior, not a specific implementation; the developer has room to choose the technical approach
- [ ] **Valuable** — the story delivers observable value to a user or to the system (no "setup-only" stories without a testable outcome)
- [ ] **Estimable** — the team understands the story well enough to assign points; no open technical questions that would change the estimate by more than 1 Fibonacci step
- [ ] **Small** — story points are in {1, 2, 3, 5, 8}; if estimated at 13+, the story must be split before entering a sprint
- [ ] **Testable** — acceptance criteria are specific enough to write automated tests directly from them

## Acceptance Criteria

- [ ] **All ACs written in Given/When/Then format** — each criterion has a precondition, action, and expected outcome
- [ ] **Error and edge cases covered** — at least one AC addresses what happens when input is invalid, a dependency is unavailable, or a boundary condition is hit
- [ ] **`acceptance-criteria-count` in frontmatter matches** the actual number of Given/When/Then blocks in the story body

## Metadata

- [ ] **Dependencies identified** — `blocked-by` stories listed in frontmatter; all are status `done` or will be `done` before this story starts
- [ ] **Technical notes from architect** — if the story touches architecture-sensitive areas (new API endpoint, data model change, auth flow), the architect has added implementation guidance in the story body or referenced the relevant ADR
- [ ] **No unresolved blockers** — the `blockers` section (if any) in sprint-status.yaml has no open items for this story

---

**Reference**: `references/phase-3-solutioning.md`, `references/schemas.md` (User Story Schema)
