---
stepNumber: 2
stepName: "Create UX Specification"
agent: "ux-designer"
inputs:
  - "PRD.md"
  - "project-context.md (if exists)"
outputs:
  - "ux-spec.md"
stepsCompleted: 1
currentStep: 2
nextStep: "DONE"
---

# Step 2: Create UX Specification

## Step Goal

Translate the PRD into a user experience specification that maps user flows, defines screen layouts, and establishes accessibility and interaction standards.

## Execution Rules

1. Activate **Sally (UX Designer)** agent persona.
2. Every functional requirement in the PRD must have UX coverage.
3. Accessibility (WCAG) requirements are non-negotiable — always include them.
4. Use textual descriptions and mermaid diagrams; visual mockups are optional follow-ups.

### Context from Previous Steps

- From Step 1: PRD.md — functional requirements, user personas, NFRs.

## Instructions

1. **Activate Sally (UX Designer)**: Load `agents/sally-ux.md`. Sally thinks in user journeys, not features.

2. **Load the PRD**: Read PRD.md thoroughly. Identify all user personas and their primary goals.

3. **Map user flows**: For each persona, create flow diagrams (mermaid syntax) showing:
   - Entry point (how they arrive)
   - Happy path through core functionality
   - Error and edge case paths
   - Exit points

4. **Define screen/view inventory**: List every screen or view the application needs:
   - Screen name and purpose
   - Key elements and their function
   - Data displayed or collected
   - Actions available to the user

5. **Establish navigation model**: Define how users move between screens:
   - Primary navigation structure
   - Breadcrumbs or back-navigation patterns
   - Deep-link considerations

6. **Document accessibility requirements**:
   - Target WCAG conformance level (A, AA, or AAA)
   - Keyboard navigation requirements
   - Screen reader considerations
   - Color contrast and text size standards

7. **Define interaction patterns**:
   - Form validation approach (inline vs. submit-time)
   - Loading states and skeleton screens
   - Error message display patterns
   - Responsive breakpoints and behavior

8. **Cross-validate with PRD**: Verify every FR has UX coverage. Flag any gaps.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| PRD has FRs with no clear user impact  | Classify as backend-only; note in UX spec    |
| Complex flows with many branches       | Simplify; recommend progressive disclosure   |
| Accessibility target not specified      | Default to WCAG AA                           |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] ux-spec.md exists with all required sections
- [ ] User flows defined for all primary personas
- [ ] Screen inventory covers all user-facing FRs
- [ ] Accessibility requirements documented with WCAG level
- [ ] Navigation model defined
- [ ] Cross-validation: no FRs missing UX coverage

### Output Validation

| Output       | Validation Rule                                     | Pass/Fail |
|-------------|---------------------------------------------------|-----------|
| ux-spec.md  | User flows + screen inventory + accessibility exist  | ____      |

## HALT Conditions

> **HALT**: Do not proceed if any of these conditions exist:
>
> - User flows are missing for primary personas
> - Accessibility requirements are not defined
> - FRs exist without UX coverage (traceability gap)
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If the UX spec has traceability gaps:
1. Identify which FRs lack UX coverage
2. Add user flow or screen inventory entries for the missing FRs
3. Re-run cross-validation — do not proceed with gaps

## Skip Conditions

- **Skip if**: The product is backend-only (CLI tool, API service) with no user-facing UI. Document this decision explicitly.
- **Do NOT skip if**: Any FRs describe user-facing behavior

## Time Box

**Maximum**: 3 hours. Focus on flows and screens, not visual design details.

## Step Completion Criteria

- [ ] ux-spec.md exists with user flows, screen inventory, and accessibility requirements
- [ ] User flows defined for all primary personas
- [ ] Every user-facing FR has UX coverage (cross-validation complete)
- [ ] WCAG conformance level is specified
- [ ] Navigation model is defined

---

**Next step**: `DONE` — Planning-only workflow complete.
