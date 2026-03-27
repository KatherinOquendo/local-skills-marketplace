---
stepNumber: 2
stepName: "Develop Stories"
agent: "dev"
inputs:
  - "sprint-status.yaml"
  - "Selected story files"
  - "architecture.md"
  - "project-context.md"
outputs:
  - "Implemented code per story"
  - "Test suites per story"
  - "Updated sprint-status.yaml"
stepsCompleted: 1
currentStep: 2
nextStep: "step-03-review.md"
---

# Step 2: Develop Stories

## Step Goal

Implement all selected stories following TDD practices, project conventions, and the architectural design. Update sprint tracking after each story.

## Execution Rules

1. Activate **Amelia (Developer)** agent persona.
2. Implement one story at a time — do not start the next until the current one is self-reviewed.
3. Write tests before or alongside implementation (TDD).
4. Follow project-context.md coding conventions strictly.
5. Update sprint-status.yaml after each story moves to IN-REVIEW.

### Context from Previous Steps

- From Step 1: sprint-status.yaml — selected stories, sprint goal.
- Pre-existing: architecture.md, project-context.md.

## Instructions

1. **Activate Amelia (Developer)**: Load `agents/amelia-developer.md`. Amelia is methodical, test-first, and quality-conscious.

2. **For each story in sprint order**:

   a. **Load story context**: Read the story file. Understand every acceptance criterion. Load related architecture sections (data model, API contracts, component design).

   b. **Create feature branch**: Name it `story/<story-id>-<slug>` following project conventions.

   c. **Write tests**: For each acceptance criterion, write a test that will verify it. Tests should initially fail (red phase of TDD).

   d. **Implement**: Write the minimum code needed to make tests pass (green phase). Follow project-context.md for naming, structure, error handling, and logging patterns.

   e. **Refactor**: Clean up the implementation without changing behavior (refactor phase). Remove duplication, improve naming, ensure consistency.

   f. **Run full test suite**: Execute all tests — not just the new ones. Fix any regressions immediately.

   g. **Self-review**: Before requesting review, check:
      - All acceptance criteria have corresponding tests
      - Code follows project conventions
      - Error handling is comprehensive
      - No hardcoded secrets or configuration values
      - Logging is appropriate

   h. **Update sprint-status.yaml**: Move story status from TODO to IN-REVIEW.

3. **Handle blockers**: If a story is blocked (external dependency, unclear requirement, technical impediment), mark it BLOCKED in sprint-status.yaml and move to the next story.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Test reveals acceptance criteria gap   | Update story file, notify Bob, then implement|
| Story is larger than estimated         | Notify Bob; consider splitting for next sprint|
| Architectural issue discovered         | Log for Winston; implement a workable solution|
| All stories blocked                    | HALT — escalate to user                      |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] All non-blocked stories are implemented
- [ ] Every implemented story has tests for all acceptance criteria
- [ ] Full test suite passes after each story
- [ ] sprint-status.yaml reflects current state
- [ ] Self-review completed for every story

### Output Validation

| Output              | Validation Rule                                | Pass/Fail |
|--------------------|-----------------------------------------------|-----------|
| Implemented code   | Tests pass for all IN-REVIEW stories           | ____      |
| sprint-status.yaml | Status is IN-REVIEW or BLOCKED for all stories | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Tests are failing for any IN-REVIEW story
> - sprint-status.yaml is not updated
> - All stories are BLOCKED with no path forward
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If a story implementation breaks existing tests:
1. `git stash` current work
2. Identify the breaking change via test output
3. Fix the regression before continuing implementation
4. If the regression is architectural, escalate before fixing

## Skip Conditions

- **Never skip** — development is the core delivery activity

## Time Box

**Maximum**: sprint duration (typically 1-2 weeks). Individual stories exceeding 2x their estimate should be split.

## Step Completion Criteria

- [ ] All non-blocked stories implemented with tests
- [ ] Full test suite passes after each story
- [ ] sprint-status.yaml reflects IN-REVIEW status for completed stories
- [ ] Self-review completed for every story before requesting review

---

**Next step**: `step-03-review.md`
