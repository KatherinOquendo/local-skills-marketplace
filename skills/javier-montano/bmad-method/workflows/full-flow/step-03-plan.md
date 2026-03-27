---
stepNumber: 3
stepName: "Plan Requirements and UX"
agent: "pm + ux-designer"
inputs:
  - "project-context.md"
  - "product-brief.md"
outputs:
  - "PRD.md"
  - "ux-spec.md"
stepsCompleted: 2
currentStep: 3
nextStep: "step-04-solution.md"
---

# Step 3: Plan Requirements and UX

## Step Goal

Define **what** to build through a comprehensive Product Requirements Document and a UX specification that maps user experience. Both artifacts must be complete enough to drive architectural decisions.

## Execution Rules

1. Activate **John (PM)** first for PRD, then **Sally (UX Designer)** for UX spec.
2. All requirements must be traceable back to the product brief.
3. Metrics must follow the SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound).
4. Do not include implementation details — that belongs in Phase 3.

### Context from Previous Steps

- From Step 1: `project-context.md` — tech constraints, project type.
- From Step 2: `product-brief.md` — vision, users, problem, success criteria.

## Instructions

1. **Activate John (PM)**: Load `agents/john-pm.md` persona. John transforms the product brief into structured, actionable requirements.

2. **Create PRD.md**: Using the `prd.md.tmpl` template, produce a PRD covering:
   - Executive summary linking back to the product brief
   - Functional requirements (FRs) with unique IDs (FR-001, FR-002, ...)
   - Non-functional requirements (NFRs) — performance, security, scalability, accessibility
   - User stories overview (high-level, detailed stories come in Phase 3)
   - Acceptance criteria for each FR
   - SMART metrics tied to success criteria from the brief
   - Assumptions and dependencies

3. **Validate PRD completeness**: Ensure every product brief goal maps to at least one FR. Ensure every FR has acceptance criteria. Ensure NFRs cover performance, security, and accessibility at minimum.

4. **Activate Sally (UX Designer)**: Load `agents/sally-ux.md` persona. Sally translates requirements into user-facing experience.

5. **Create ux-spec.md**: Produce a UX specification covering:
   - User flow diagrams (described textually or as mermaid charts)
   - Screen/view inventory with purpose descriptions
   - Navigation model
   - Accessibility requirements (WCAG level target)
   - Responsive design considerations
   - Error state handling patterns
   - Key interaction patterns

6. **Cross-validate**: Verify that every FR in the PRD has a corresponding UX representation. Flag any gaps.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Product brief lacks user personas      | Return to Step 2 to complete personas         |
| Scope is very large                    | Recommend phased delivery with MVP definition |
| UX requires visual mockups             | Note as follow-up; textual spec is sufficient |
| Unclear requirement                    | HALT and request clarification                |

## Success Metrics

- [ ] PRD.md exists with all required sections populated
- [ ] Every FR has a unique ID and acceptance criteria
- [ ] NFRs cover at minimum: performance, security, accessibility
- [ ] ux-spec.md exists with user flows and screen inventory
- [ ] Every FR maps to a UX element (traceability verified)
- [ ] At least one SMART metric is defined

### Output Validation

| Output       | Validation Rule                                        | Pass/Fail |
|-------------|------------------------------------------------------|-----------|
| PRD.md      | All FRs have IDs + acceptance criteria                 | ____      |
| ux-spec.md  | User flows exist for all primary personas              | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - PRD has FRs without acceptance criteria
> - No NFRs are defined
> - UX spec has no user flows
> - Traceability gap: FRs exist with no UX coverage
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If the PRD or UX spec fails review:
1. Identify the specific failing sections (missing ACs, incomplete NFRs, etc.)
2. Reload the relevant agent (John for PRD, Sally for UX)
3. Fix only the failing sections — do not rewrite from scratch
4. Re-validate with the cross-validation checklist

## Skip Conditions

- **Skip if**: PRD.md and ux-spec.md already exist AND have been approved by the user AND pass the `validate_prd.py` checks
- **Do NOT skip if**: The product brief has changed since the PRD was written

## Time Box

**Maximum**: 4 hours (2h for PRD + 2h for UX spec). If requirements gathering stalls, HALT and return to Step 2 for additional analysis.

## Step Completion Criteria

- [ ] PRD.md has all FRs with unique IDs and acceptance criteria
- [ ] NFRs cover performance, security, and accessibility at minimum
- [ ] ux-spec.md has user flows for every primary persona
- [ ] Cross-validation: every FR has UX coverage
- [ ] User has reviewed and approved both documents

---

**Next step**: `step-04-solution.md`
