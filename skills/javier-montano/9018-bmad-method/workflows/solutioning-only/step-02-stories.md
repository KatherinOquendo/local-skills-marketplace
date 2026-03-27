---
stepNumber: 2
stepName: "Decompose into Epics and Stories"
agent: "sm"
inputs:
  - "architecture.md"
  - "PRD.md"
  - "ADR files"
outputs:
  - "Epic files"
  - "User story files"
  - "Dependency map"
stepsCompleted: 1
currentStep: 2
nextStep: "step-03-gate.md"
---

# Step 2: Decompose into Epics and Stories

## Step Goal

Break the architecture and requirements into implementable epics and user stories. Each story must be small enough to complete in a single sprint and have clear acceptance criteria.

## Execution Rules

1. Activate **Bob (Scrum Master)** agent persona.
2. Stories must follow INVEST criteria: Independent, Negotiable, Valuable, Estimable, Small, Testable.
3. Every story must have acceptance criteria — no exceptions.
4. Dependencies between stories must be explicitly mapped.

### Context from Previous Steps

- From Step 1: architecture.md — components, data model, APIs.
- From Step 1: ADR files — technology decisions.
- Pre-existing: PRD.md — functional requirements.

## Instructions

1. **Activate Bob (Scrum Master)**: Load `agents/bob-scrum-master.md`. Bob thinks in deliverable increments and dependency chains.

2. **Identify epics**: Group related functionality into epics. Each epic should represent a coherent feature area. Use `epic.md.tmpl` for each:
   - Epic ID (EPIC-001, EPIC-002, ...)
   - Title and description
   - Related FRs from the PRD
   - Related architectural components
   - Estimated story count

3. **Decompose into stories**: For each epic, create user stories using `user-story.md.tmpl`:
   - Story ID (STORY-001, STORY-002, ...)
   - Title in "As a [user], I want [action], so that [benefit]" format
   - Description with technical context from architecture.md
   - Acceptance criteria (Given/When/Then or checklist format)
   - Estimation: S (< 2h), M (2-4h), L (4-8h)
   - Dependencies: list other story IDs this story depends on
   - Parent epic ID

4. **Validate INVEST criteria**: For each story, check:
   - **Independent**: Can it be implemented without completing other in-progress stories?
   - **Valuable**: Does it deliver user or technical value on its own?
   - **Small**: Is estimation S or M? If L, consider splitting.
   - **Testable**: Can acceptance criteria be verified with automated tests?

5. **Map dependencies**: Create a dependency document listing:
   - Story ID -> depends on [Story IDs]
   - Critical path (longest dependency chain)
   - Foundation stories (no dependencies, should be done first)

6. **Sequence stories**: Propose an implementation order respecting dependencies and maximizing early value delivery.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Story is too large (L estimation)      | Split into smaller stories                   |
| Circular dependency detected           | Refactor stories to break the cycle          |
| FR has no corresponding story          | Create missing story or document as deferred |
| More than 50 stories                   | Recommend MVP cut; mark stories as P0/P1/P2  |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] All epics have at least one story
- [ ] Every story has acceptance criteria
- [ ] Every story has an estimation (S/M/L)
- [ ] Dependencies are mapped with no circular references
- [ ] Critical path is identified
- [ ] All FRs from PRD are covered by at least one story

### Output Validation

| Output            | Validation Rule                                   | Pass/Fail |
|------------------|--------------------------------------------------|-----------|
| Epic files       | Each has ID, description, related FRs              | ____      |
| Story files      | Each has ID, acceptance criteria, estimation       | ____      |
| Dependency map   | No circular references; critical path documented   | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Stories exist without acceptance criteria
> - Circular dependencies are detected
> - FRs from PRD have no story coverage
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If circular dependencies are detected:
1. Map the dependency cycle visually
2. Identify which story can be split to break the cycle
3. Create the split stories and re-map dependencies
4. Verify no new cycles were introduced

## Skip Conditions

- **Skip if**: Epics and stories already exist with complete acceptance criteria AND all FRs are covered
- **Do NOT skip if**: The architecture has been modified since stories were written

## Time Box

**Maximum**: 3 hours. If story count exceeds 50, HALT and recommend MVP scoping before continuing decomposition.

## Step Completion Criteria

- [ ] All epics have at least one story
- [ ] Every story has acceptance criteria and estimation (S/M/L)
- [ ] Dependencies mapped with no circular references
- [ ] Critical path identified
- [ ] All FRs from PRD are covered by at least one story

---

**Next step**: `step-03-gate.md`
