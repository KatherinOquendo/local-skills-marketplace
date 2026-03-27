---
stepNumber: 3
stepName: "Review Stories"
agent: "qa"
inputs:
  - "Implemented stories (IN-REVIEW status)"
  - "Story files with acceptance criteria"
  - "project-context.md"
outputs:
  - "Code review reports per story"
  - "Updated sprint-status.yaml"
stepsCompleted: 2
currentStep: 3
nextStep: "step-04-retro.md"
---

# Step 3: Review Stories

## Step Goal

Perform thorough code review on all implemented stories, verifying acceptance criteria coverage, code quality, test adequacy, and security/performance considerations.

## Execution Rules

1. Activate **Quinn (QA)** agent persona.
2. Every acceptance criterion must be independently verified — not assumed from test names.
3. Review feedback must be structured: APPROVED, CHANGES-REQUESTED, or BLOCKED.
4. If CHANGES-REQUESTED, Amelia must address feedback and resubmit.

### Context from Previous Steps

- From Step 2: Implemented code, test suites, sprint-status.yaml with IN-REVIEW stories.
- Pre-existing: Story files, project-context.md.

## Instructions

1. **Activate Quinn (QA)**: Load `agents/quinn-qa.md`. Quinn is detail-oriented, standards-driven, and constructive.

2. **For each IN-REVIEW story**:

   a. **Load story and diff**: Read the story file for acceptance criteria. Read the code changes (diff from main branch).

   b. **Verify acceptance criteria**: For each criterion:
      - Identify the test that covers it
      - Verify the test actually validates the criterion (not just superficially)
      - Check edge cases: what about empty input, null values, boundary conditions?

   c. **Check code quality**: Against project-context.md standards:
      - Naming conventions followed
      - Code structure is consistent with existing patterns
      - Error handling is comprehensive (not just happy path)
      - Logging is present and appropriate
      - No dead code or commented-out blocks

   d. **Review tests**:
      - Test names are descriptive
      - Tests are independent (no shared state)
      - Both positive and negative cases covered
      - Test data is realistic

   e. **Security check**:
      - No hardcoded secrets or credentials
      - Input validation is present
      - SQL injection / XSS protections (if applicable)
      - Authentication/authorization enforced where needed

   f. **Performance check**:
      - No obvious N+1 queries
      - Large data sets handled with pagination
      - Expensive operations are async where appropriate

   g. **Produce review report**: For each story, state:
      - Result: APPROVED / CHANGES-REQUESTED / BLOCKED
      - Per-criterion verification status
      - Findings with severity (CRITICAL, MAJOR, MINOR, SUGGESTION)
      - Required changes (if any)

3. **Handle CHANGES-REQUESTED**: Return to Amelia (developer) for fixes. After fixes, re-review the specific items.

4. **Update sprint-status.yaml**: Move APPROVED stories to DONE. Leave CHANGES-REQUESTED stories as IN-REVIEW.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Critical security finding              | BLOCKED — must fix before approval           |
| Minor style issues only                | APPROVED with SUGGESTION notes               |
| Acceptance criterion not fully covered | CHANGES-REQUESTED — must add coverage        |
| Architectural concern discovered       | Log for retrospective; approve if functional |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] Every IN-REVIEW story has a review report
- [ ] All DONE stories have APPROVED review status
- [ ] Review reports include per-criterion verification
- [ ] No CRITICAL findings remain unresolved
- [ ] sprint-status.yaml reflects final statuses

### Output Validation

| Output              | Validation Rule                                | Pass/Fail |
|--------------------|-----------------------------------------------|-----------|
| Review reports     | Each has result + per-criterion status          | ____      |
| sprint-status.yaml | DONE stories match APPROVED reviews             | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - CRITICAL findings remain unresolved
> - DONE stories lack APPROVED reviews
> - sprint-status.yaml does not match review results
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If a CRITICAL finding is discovered after approval:
1. Revert the story status from DONE to IN-REVIEW
2. Create a follow-up review focused on the specific finding
3. Amend the review report with the new finding

## Skip Conditions

- **Never skip** — code review is mandatory for every story
- Even single-developer projects benefit from structured self-review using this checklist

## Time Box

**Maximum**: 30 minutes per story review. If review takes longer, the story may be too large.

## Step Completion Criteria

- [ ] Every IN-REVIEW story has a completed review report
- [ ] All DONE stories have APPROVED review status
- [ ] No CRITICAL findings remain unresolved
- [ ] sprint-status.yaml reflects final statuses (DONE or BLOCKED)

---

**Next step**: `step-04-retro.md`
