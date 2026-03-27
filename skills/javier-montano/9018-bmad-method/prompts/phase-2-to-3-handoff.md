# Phase 2 to Phase 3 Handoff: Planning -> Solutioning

## Pre-conditions

- `PRD.md` exists with all FRs having unique IDs and acceptance criteria
- `ux-spec.md` exists with user flows for all primary personas
- NFRs cover performance, security, and accessibility at minimum
- User has reviewed and approved both documents

## Post-conditions

- `architecture.md` exists with component diagram, data model, API design, and security sections
- At least 2 ADRs exist with context, decision, and consequences
- All stories have acceptance criteria and estimations
- Dependency map has no circular references
- Implementation readiness gate result is PASS

## Failure Signals

- Winston cannot satisfy NFRs with the chosen tech stack (return to user for constraint renegotiation)
- Bob produces stories without acceptance criteria
- Circular dependencies detected in story graph
- Gate result is FAIL on critical checks (1, 3, or 8)

## Context

Phase 2 (Planning) is complete. John (PM) has produced `PRD.md` and Sally (UX Designer) has produced `ux-spec.md`. This prompt guides the transition to Phase 3 (Solutioning) where Winston (Architect) and Bob (Scrum Master) take over.

## Pre-Transition Checklist

Before proceeding, verify Phase 2 completeness:

- [ ] `PRD.md` exists with all sections populated
- [ ] Every FR has a unique ID (FR-001+) and acceptance criteria
- [ ] NFRs cover at minimum: performance, security, accessibility
- [ ] SMART success metrics are defined
- [ ] `ux-spec.md` exists with user flows and screen inventory
- [ ] Cross-validation: every FR has UX coverage
- [ ] User has reviewed and approved both documents

If any item above is incomplete, return to Phase 2 and address it before proceeding.

## Handoff Summary

Summarize the following from Phase 2 artifacts for the solutioning agents:

1. **Requirements Overview**: Total FR count, grouped by feature area.
2. **NFR Summary**: Key performance targets, security requirements, accessibility level.
3. **UX Decisions**: Primary navigation model, key interaction patterns, responsive strategy.
4. **User Personas**: List with primary flows.
5. **Open Questions**: Any items flagged in PRD as needing resolution.
6. **Scope Constraints**: Technical constraints from project-context.md that affect architecture.
7. **Integration Points**: External systems or APIs identified in requirements.

## Agent Activation Instructions

1. **Activate Winston (Architect)**: Load `agents/winston-architect.md`. Winston will design the system architecture.

2. **Provide context to Winston**: Load all three artifacts:
   - `PRD.md` — requirements to satisfy
   - `ux-spec.md` — user experience to support
   - `project-context.md` — technical constraints and stack decisions

3. **Winston's mandate**: Create architecture.md with:
   - System component diagram
   - Data model with entities and relationships
   - API design with endpoint contracts
   - Security architecture
   - ADRs for every significant decision (minimum 2)

4. **After architecture is complete, activate Bob (Scrum Master)**: Load `agents/bob-scrum-master.md`. Bob will decompose architecture into epics and stories.

5. **Provide context to Bob**: Load `architecture.md`, `PRD.md`, and ADR files.

6. **Bob's mandate**: Create epics and stories with:
   - INVEST-compliant user stories
   - Acceptance criteria on every story
   - Estimations (S/M/L)
   - Dependency map with critical path

## Verification Before Proceeding to Phase 4

- [ ] architecture.md has all required sections
- [ ] At least 2 ADRs exist with complete sections
- [ ] All stories have acceptance criteria and estimations
- [ ] Dependency map has no circular references
- [ ] Implementation readiness gate passes (run gate-reviewer)

Only proceed to Phase 4 (Implementation) when the gate result is PASS.

---

**Next prompt**: `phase-3-to-4-handoff.md`
