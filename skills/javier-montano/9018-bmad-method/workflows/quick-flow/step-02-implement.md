---
stepNumber: 2
stepName: "Implement Change"
agent: "quick-flow-solo-dev"
inputs:
  - "Lightweight spec from Step 1"
  - "project-context.md"
outputs:
  - "Implemented code changes"
  - "Test suite for the change"
stepsCompleted: 1
currentStep: 2
nextStep: "step-03-verify.md"
---

# Step 2: Implement Change

## Step Goal

Implement the approved change with tests, following project conventions. Keep the implementation tightly scoped to the lightweight spec.

## Execution Rules

1. Continue as **Barry (Quick Flow Solo Dev)**.
2. Do not expand scope beyond the lightweight spec — if scope creep is detected, HALT.
3. Write tests that directly verify the acceptance criteria.
4. Follow existing code patterns found in project-context.md.

### Context from Previous Steps

- From Step 1: Lightweight spec — what to change, files to modify, acceptance criteria.

## Instructions

1. **Create a branch**: Name it `quick/<short-description>` following project conventions.

2. **Load existing code context**: Read the files identified in the spec. Understand current patterns, naming conventions, and test approaches.

3. **Write tests first**: For each acceptance criterion in the spec, write a test that will verify it. Tests should fail before implementation and pass after.

4. **Implement the change**: Modify only the files listed in the spec. Follow project-context.md coding conventions for naming, error handling, and structure.

5. **Run tests**: Execute the full test suite (not just new tests) to verify no regressions.

6. **Self-review**: Check your own changes against:
   - Does every acceptance criterion have a passing test?
   - Are there any unintended side effects?
   - Is error handling in place?
   - Are there any hardcoded values that should be configurable?

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Change requires touching more files     | HALT — scope exceeds quick flow              |
| Existing tests break                   | Fix regressions before proceeding            |
| Discovery of related bug               | Log it separately; do not fix in this change |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] Branch created with descriptive name
- [ ] Tests written for all acceptance criteria
- [ ] All tests pass (new and existing)
- [ ] Changes are limited to files listed in spec
- [ ] Self-review completed with no critical findings

### Output Validation

| Output            | Validation Rule                         | Pass/Fail |
|------------------|----------------------------------------|-----------|
| Code changes     | Only spec-listed files modified         | ____      |
| Test suite       | All acceptance criteria have tests      | ____      |
| Test results     | Full suite passes                       | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Tests are failing
> - Scope has expanded beyond the spec
> - Self-review found critical issues
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

1. `git checkout main` and delete the feature branch
2. If the change caused regressions caught after merge, revert the merge commit
3. Reassess scope — the issue may need full-flow treatment

## Skip Conditions

- **Never skip** — implementation is the core purpose of quick flow

## Time Box

**Maximum**: 4 hours. If implementation exceeds 4 hours, HALT — the scope has grown beyond quick-flow eligibility.

## Step Completion Criteria

- [ ] Feature branch exists with descriptive name
- [ ] Tests cover all acceptance criteria from the lightweight spec
- [ ] All tests pass (new and existing)
- [ ] Only spec-listed files were modified
- [ ] Self-review checklist completed

---

**Next step**: `step-03-verify.md`
