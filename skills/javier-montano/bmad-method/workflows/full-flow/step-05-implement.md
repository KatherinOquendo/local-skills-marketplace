---
stepNumber: 5
stepName: "Execute Sprint — Implement Stories"
agent: "dev + qa + sm"
inputs:
  - "project-context.md"
  - "architecture.md"
  - "Sprint backlog (selected stories)"
  - "sprint-status.yaml"
outputs:
  - "Implemented code per story"
  - "Test suites per story"
  - "Code review reports"
  - "Updated sprint-status.yaml"
stepsCompleted: 4
currentStep: 5
nextStep: "step-06-retro.md"
---

# Step 5: Execute Sprint — Implement Stories

## Step Goal

Execute a development sprint: implement selected stories with test-driven development, perform code reviews, and track progress in `sprint-status.yaml`. Every story must meet its acceptance criteria before being marked done.

## Execution Rules

1. **Bob (Scrum Master)** runs sprint planning, **Amelia (Developer)** implements, **Quinn (QA)** reviews.
2. One story at a time — complete a story fully before starting the next.
3. Every story must have tests written before or alongside the implementation (TDD).
4. Code reviews are mandatory — no story is done without Quinn's review.
5. Update `sprint-status.yaml` after each story completes.

### Context from Previous Steps

- From Step 1: `project-context.md` — coding conventions, tech stack.
- From Step 4: `architecture.md` — system design, data model, APIs.
- From Step 4: Story files — acceptance criteria, dependencies.

## Instructions

1. **Sprint planning with Bob**: Load `agents/bob-scrum-master.md`. Select stories for the sprint based on priority and dependencies. Define a sprint goal. Create `sprint-status.yaml` using `sprint-status.yaml.tmpl`.

2. **Per-story implementation with Amelia**: For each story in the sprint:
   a. Load `agents/amelia-developer.md` persona.
   b. Read the story file — understand acceptance criteria fully.
   c. Load relevant architecture sections (data model, APIs, component design).
   d. Create a feature branch (naming: `story/<story-id>-<slug>`).
   e. Write tests first (or alongside) that verify acceptance criteria.
   f. Implement the code following project-context.md conventions.
   g. Run tests — all must pass.
   h. Self-review: check against the code-review-checklist.md template.

3. **Code review with Quinn**: For each completed story:
   a. Load `agents/quinn-qa.md` persona.
   b. Review code against acceptance criteria — every criterion must be covered.
   c. Check code quality: naming, structure, error handling, logging.
   d. Verify test coverage and test quality.
   e. Check for security issues and performance concerns.
   f. Produce a review report: APPROVED, CHANGES-REQUESTED, or BLOCKED.

4. **Handle review feedback**: If CHANGES-REQUESTED, switch back to Amelia, address feedback, re-submit. If BLOCKED, escalate to user.

5. **Update sprint status**: After each story reaches DONE, update `sprint-status.yaml` with completion status, actual effort, and any notes.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Story is blocked by external dependency| Mark BLOCKED in sprint-status, skip to next  |
| Tests reveal acceptance criteria gap   | Update story file, then implement            |
| Code review finds architectural issue  | Escalate to Winston for ADR update           |
| Sprint goal at risk                    | Re-negotiate scope with Bob                  |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] All selected stories have been implemented or explicitly deferred
- [ ] Every completed story has passing tests
- [ ] Every completed story has a code review report
- [ ] sprint-status.yaml is up to date with final statuses
- [ ] No story is marked DONE without passing review

### Output Validation

| Output                | Validation Rule                                | Pass/Fail |
|----------------------|-----------------------------------------------|-----------|
| Implemented stories  | Tests pass for all DONE stories                | ____      |
| Review reports       | Every DONE story has APPROVED review           | ____      |
| sprint-status.yaml   | All stories have final status recorded         | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - A story is marked DONE but has failing tests
> - A story is marked DONE without code review
> - sprint-status.yaml does not reflect actual state
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If a story implementation introduces regressions:
1. Revert the feature branch (do not revert main)
2. Identify the regression cause from test failures
3. Fix in the feature branch and re-submit for review
4. If the issue is architectural, escalate to Winston before proceeding

## Skip Conditions

- **Never skip this step** — implementation is the core delivery phase
- If no stories are ready for implementation, return to Step 4 for story refinement

## Time Box

**Maximum**: 2 weeks per sprint. If a single story exceeds its estimate by more than 2x, HALT and split it.

## Step Completion Criteria

- [ ] All committed stories are implemented or explicitly deferred with justification
- [ ] Every completed story has passing tests covering all acceptance criteria
- [ ] Every completed story has an APPROVED code review
- [ ] sprint-status.yaml reflects the actual final state
- [ ] No DONE stories have failing tests

---

**Next step**: `step-06-retro.md`
