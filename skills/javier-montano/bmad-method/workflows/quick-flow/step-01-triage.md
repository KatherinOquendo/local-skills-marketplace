---
stepNumber: 1
stepName: "Triage Request"
agent: "quick-flow-solo-dev"
inputs:
  - "User request or bug report"
  - "project-context.md (if exists)"
outputs:
  - "Triage decision (quick-flow appropriate: YES/NO)"
  - "Lightweight spec (if YES)"
stepsCompleted: 0
currentStep: 1
nextStep: "step-02-implement.md"
---

# Step 1: Triage Request

## Step Goal

Evaluate the incoming request to confirm it qualifies for quick flow (small scope, no architectural changes, well-understood). Produce a lightweight spec if approved.

## Execution Rules

1. Activate the **Barry (Quick Flow Solo Dev)** agent persona.
2. If the request requires architectural changes or new system components, reject for quick flow and redirect to full flow.
3. The lightweight spec must fit in a single file — if it cannot, the scope is too large.

### Context from Previous Steps

- None — this is the first step of quick flow.

## Instructions

1. **Activate Barry (Quick Flow)**: Load `agents/barry-quick-flow.md`. Barry is pragmatic, fast, and scope-conscious.

2. **Evaluate scope criteria**: Check the request against quick-flow eligibility:
   - Touches fewer than 5 files
   - No new database tables or API endpoints
   - No changes to authentication or authorization
   - No new external dependencies
   - Estimated effort under 2 hours
   - Existing test patterns can be reused

3. **If NOT eligible**: Inform the user that this request exceeds quick-flow scope. Recommend the appropriate workflow (full-flow, planning-only, or sprint-cycle). HALT this workflow.

4. **Write lightweight spec**: If eligible, create a brief spec covering:
   - What changes (1-3 sentences)
   - Why (link to bug report, user request, or improvement goal)
   - Files to modify (list)
   - Acceptance criteria (3-5 items)
   - Risk assessment (LOW/MEDIUM)

5. **Confirm with user**: Present the lightweight spec and get explicit approval before implementation.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Request touches > 5 files              | Reject quick flow — redirect to sprint-cycle |
| Request needs new API endpoint         | Reject quick flow — redirect to full flow    |
| Request is unclear                     | Ask clarifying questions before triaging     |
| Risk assessment is MEDIUM              | Proceed with caution; extra review in Step 3 |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] Triage decision is explicitly recorded (YES or NO)
- [ ] If YES: lightweight spec exists with acceptance criteria
- [ ] If NO: user is informed with redirect recommendation
- [ ] User has approved the spec before proceeding

### Output Validation

| Output            | Validation Rule                                  | Pass/Fail |
|------------------|------------------------------------------------|-----------|
| Triage decision  | Explicit YES/NO with reasoning                   | ____      |
| Lightweight spec | Acceptance criteria defined (if YES)             | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Triage decision is NO (redirect to appropriate workflow)
> - User has not approved the lightweight spec
> - Risk assessment is HIGH
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and recommended alternative workflow.

## Rollback Procedure

Triage decisions are lightweight — if a wrong triage occurs:
1. If quick-flow was approved but scope grew, HALT during Step 2 and redirect to full flow
2. Archive the lightweight spec as context for the full-flow story creation

## Skip Conditions

- **Skip if**: The change is a 1-line typo fix with zero risk (commit directly)
- **Do NOT skip if**: Any uncertainty exists about scope or risk

## Time Box

**Maximum**: 15 minutes. If triage takes longer, the request is probably too complex for quick flow.

## Step Completion Criteria

- [ ] Triage decision is explicitly YES or NO with written reasoning
- [ ] If YES: lightweight spec has scope description, files list, and acceptance criteria
- [ ] If NO: user is informed with specific redirect (full-flow, sprint-cycle, etc.)
- [ ] User has approved before proceeding

---

**Next step**: `step-02-implement.md`
