---
stepNumber: 3
stepName: "Implementation Readiness Gate"
agent: "gate-reviewer"
inputs:
  - "All Phase 2 artifacts (PRD.md, ux-spec.md)"
  - "All Phase 3 artifacts (architecture.md, ADRs, epics, stories)"
  - "project-context.md"
outputs:
  - "gate-report.md"
  - "Gate result: PASS / CONCERNS / FAIL"
stepsCompleted: 2
currentStep: 3
nextStep: "DONE"
---

# Step 3: Implementation Readiness Gate

## Step Goal

Execute the 13-step implementation readiness checklist to determine whether the project is ready for development. Produce a structured gate report with evidence for each check.

## Execution Rules

1. Activate the **Gate Reviewer** agent persona.
2. Every checklist item must have explicit evidence — no "assumed" passes.
3. The gate result must be one of: PASS, CONCERNS, FAIL.
4. CONCERNS allows proceeding with documented risks. FAIL blocks implementation.

### Context from Previous Steps

- From Step 1: architecture.md, ADR files.
- From Step 2: Epic and story files, dependency map.
- Pre-existing: PRD.md, ux-spec.md, project-context.md.

## Instructions

1. **Activate Gate Reviewer**: Load `agents/gate-reviewer.md`. The gate reviewer is objective, thorough, and evidence-focused.

2. **Load all artifacts**: Read every artifact produced in the planning and solutioning phases. Build a mental map of coverage.

3. **Execute the 13-step checklist**: For each item, provide evidence and a PASS/FAIL determination:

   1. **PRD completeness**: All FRs have IDs and acceptance criteria
   2. **UX coverage**: Every user-facing FR has UX specification
   3. **Architecture coverage**: Every FR maps to an architectural component
   4. **Data model completeness**: All entities defined with relationships
   5. **API contract completeness**: All endpoints documented with contracts
   6. **Security design**: Authentication, authorization, and data protection addressed
   7. **NFR coverage**: Each NFR has an architectural response
   8. **Story completeness**: All stories have acceptance criteria and estimations
   9. **Dependency clarity**: No circular dependencies; critical path identified
   10. **Tech stack decisions**: All major decisions documented in ADRs
   11. **Risk identification**: Known risks documented with mitigations
   12. **Environment readiness**: Development environment setup is documented
   13. **Testing strategy**: Approach for unit, integration, and E2E testing defined

4. **Calculate gate result**:
   - **PASS**: All 13 items pass
   - **CONCERNS**: 1-3 items fail but none are critical blockers (items 1, 3, 8 are critical)
   - **FAIL**: Any critical item fails OR more than 3 items fail

5. **Write gate-report.md**: Using `implementation-readiness.md.tmpl`, produce:
   - Summary: overall result and confidence level
   - Per-item: evidence, result, and notes
   - Recommendations: what to fix for CONCERNS/FAIL items
   - Risk register: outstanding risks going into implementation

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Result is PASS                         | Implementation can begin                     |
| Result is CONCERNS                     | Document risks; user decides to proceed or fix|
| Result is FAIL                         | Identify failing phases; return for remediation|
| Evidence is ambiguous                  | Mark as FAIL — err on the side of caution    |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] All 13 checklist items have been evaluated with evidence
- [ ] Gate result is explicitly stated (PASS/CONCERNS/FAIL)
- [ ] gate-report.md exists with per-item evidence
- [ ] If CONCERNS or FAIL: recommendations are provided
- [ ] Risk register is populated

### Output Validation

| Output           | Validation Rule                                      | Pass/Fail |
|-----------------|---------------------------------------------------- |-----------|
| gate-report.md  | All 13 items evaluated with evidence                  | ____      |
| Gate result     | One of PASS/CONCERNS/FAIL explicitly stated           | ____      |

## HALT Conditions

> **HALT**: Do not proceed if any of these conditions exist:
>
> - Gate result is FAIL
> - Any checklist item lacks evidence
> - Critical items (1, 3, 8) are marked FAIL
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason, the gate report, and remediation recommendations.

## Rollback Procedure

If the gate result is FAIL:
1. Read the gate report to identify the failing checks
2. Map each failure to the phase that produced the failing artifact
3. Return to that phase's workflow to remediate
4. Re-run the gate after remediation — do not skip any checks

## Skip Conditions

- **Skip if**: A gate-report.md already exists with PASS result AND no artifacts have been modified since the gate was run
- **Do NOT skip if**: Any planning or solutioning artifact has been modified since the last gate run

## Time Box

**Maximum**: 1 hour. The gate is an evaluation, not a creation step. If evidence is difficult to find, that itself indicates a problem with artifact quality.

## Step Completion Criteria

- [ ] All 13 checklist items evaluated with specific evidence cited
- [ ] Gate result explicitly stated: PASS, CONCERNS, or FAIL
- [ ] gate-report.md written and saved
- [ ] If CONCERNS: risk acceptance documented
- [ ] If FAIL: remediation plan with specific phase/step to return to

---

**Next step**: `DONE` — Solutioning-only workflow complete. If PASS, proceed to sprint-cycle workflow.
