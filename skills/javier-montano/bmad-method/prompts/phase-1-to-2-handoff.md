# Phase 1 to Phase 2 Handoff: Analysis -> Planning

## Pre-conditions

- `product-brief.md` exists and has been approved by the user
- `project-context.md` exists with tech stack and constraints filled in
- Mary (Analyst) agent has completed her analysis work

## Post-conditions

- `PRD.md` exists with all FRs having unique IDs and acceptance criteria
- `ux-spec.md` exists with user flows for all primary personas
- Cross-validation confirms every FR has UX coverage
- User has reviewed and approved both documents

## Failure Signals

- PRD has FRs without acceptance criteria after John completes
- ux-spec.md has no user flows after Sally completes
- Cross-validation reveals FRs with no UX coverage
- User rejects PRD or UX spec during review

## Context

Phase 1 (Analysis) is complete. Mary (Analyst) has produced the `product-brief.md`. This prompt guides the transition to Phase 2 (Planning) where John (PM) and Sally (UX Designer) take over.

## Pre-Transition Checklist

Before proceeding, verify Phase 1 completeness:

- [ ] `product-brief.md` exists and is finalized
- [ ] Vision statement is clear (1-2 sentences)
- [ ] Target audience is defined with personas
- [ ] Problem statement has evidence tags
- [ ] Success criteria are measurable
- [ ] Scope boundaries are explicit (what is IN and OUT)
- [ ] Assumptions are listed and tagged `[SUPUESTO]`

If any item above is incomplete, return to Phase 1 and address it before proceeding.

## Handoff Summary

Summarize the following from the product brief for the planning agents:

1. **Vision**: State the one-line vision from the brief.
2. **Target Users**: List each persona with their primary goal.
3. **Core Problem**: The validated problem statement.
4. **Value Proposition**: What differentiates this solution.
5. **Success Metrics**: The measurable criteria from the brief.
6. **Scope Boundaries**: What is explicitly out of scope.
7. **Key Risks**: Top 3 risks or unvalidated assumptions.

## Agent Activation Instructions

1. **Activate John (PM)**: Load `agents/john-pm.md`. John will transform the product brief into a structured PRD.

2. **Provide context to John**: Load `product-brief.md` as primary context. Also load `project-context.md` for technical constraints.

3. **John's mandate**: Create PRD.md with:
   - Functional requirements (FR-001+) with acceptance criteria
   - Non-functional requirements (performance, security, accessibility)
   - SMART success metrics
   - Traceability back to product brief sections

4. **After PRD is complete, activate Sally (UX Designer)**: Load `agents/sally-ux.md`. Sally will translate the PRD into user experience specification.

5. **Provide context to Sally**: Load `PRD.md` and `product-brief.md` (for persona details).

6. **Sally's mandate**: Create ux-spec.md with:
   - User flows per persona
   - Screen inventory
   - Navigation model
   - Accessibility requirements

## Verification Before Proceeding to Phase 3

- [ ] PRD.md has all FRs with IDs and acceptance criteria
- [ ] ux-spec.md has user flows for all primary personas
- [ ] Every FR has UX coverage (cross-validation complete)
- [ ] NFRs are defined
- [ ] User has reviewed both artifacts

Only proceed to Phase 3 (Solutioning) when all items above are verified.

---

**Next prompt**: `phase-2-to-3-handoff.md`
