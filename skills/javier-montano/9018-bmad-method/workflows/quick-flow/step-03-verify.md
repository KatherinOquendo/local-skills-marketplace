---
stepNumber: 3
stepName: "Verify and Close"
agent: "quick-flow-solo-dev"
inputs:
  - "Implemented code changes"
  - "Test results"
  - "Lightweight spec"
outputs:
  - "Verification report"
  - "Merged code (or merge-ready branch)"
stepsCompleted: 2
currentStep: 3
nextStep: "DONE"
---

# Step 3: Verify and Close

## Step Goal

Perform final verification that the implementation meets all acceptance criteria, update any affected documentation, and prepare for merge.

## Execution Rules

1. Continue as **Barry (Quick Flow Solo Dev)**.
2. Every acceptance criterion must be explicitly verified — not assumed.
3. Documentation must be updated if the change affects user-facing behavior or APIs.

### Context from Previous Steps

- From Step 1: Lightweight spec — acceptance criteria.
- From Step 2: Implemented code, test results.

## Instructions

1. **Run full test suite**: Execute all tests one final time to confirm everything passes in a clean state.

2. **Verify acceptance criteria**: Go through each criterion in the lightweight spec one by one. For each:
   - Describe how it is verified (test name, manual check, or observation)
   - Mark as PASS or FAIL
   - If FAIL, return to Step 2

3. **Update documentation**: If the change affects:
   - README or user-facing docs: update them
   - API contracts: update the spec
   - Configuration: update examples or defaults
   - If no docs affected, explicitly state "No documentation changes needed"

4. **Prepare merge summary**: Write a brief summary of:
   - What was changed and why
   - Files modified
   - Tests added or modified
   - Any follow-up items identified during implementation

5. **Present to user**: Share the verification report and merge summary. Get approval to merge or deliver.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| An acceptance criterion fails          | Return to Step 2 for fix                     |
| Follow-up items discovered             | Log them; do not include in this change      |
| User requests additional changes       | Evaluate scope; start new quick-flow if large|
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] Full test suite passes
- [ ] All acceptance criteria are individually verified as PASS
- [ ] Documentation is updated (or explicitly noted as not needed)
- [ ] Merge summary is written
- [ ] User has approved the final result

### Output Validation

| Output               | Validation Rule                              | Pass/Fail |
|---------------------|---------------------------------------------|-----------|
| Test results        | Full suite passes                            | ____      |
| Acceptance criteria | All items marked PASS                        | ____      |
| Documentation       | Updated if applicable                        | ____      |

## HALT Conditions

> **HALT**: Do not proceed if any of these conditions exist:
>
> - Any acceptance criterion is marked FAIL
> - Tests are failing
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and return to Step 2.

## Rollback Procedure

If verification fails:
1. Return to Step 2 to fix the failing acceptance criteria
2. Do not merge a branch with failing verifications
3. If the fix reveals deeper issues, escalate to full flow

## Skip Conditions

- **Never skip** — verification is the quality gate for quick flow

## Time Box

**Maximum**: 30 minutes. Verification is a check, not a rework session.

## Step Completion Criteria

- [ ] Full test suite passes
- [ ] Every acceptance criterion individually verified as PASS
- [ ] Documentation updated (or explicitly noted as not needed)
- [ ] Merge summary written with changes, files, and follow-ups
- [ ] User has approved the final result

---

**Next step**: `DONE` — Quick flow complete.
