# Phase 3 to Phase 4 Handoff: Solutioning -> Implementation

## Pre-conditions

- `gate-report.md` exists with PASS or CONCERNS (with documented risk acceptance) result
- `architecture.md` is finalized with all required sections
- All stories have acceptance criteria, estimations, and dependencies mapped
- `project-context.md` is up to date with coding conventions

## Post-conditions

- Sprint 1 has been planned with sprint-status.yaml created
- At least one story has been implemented with tests and review
- sprint-status.yaml is accurate and up to date
- Retrospective has been conducted after the first sprint

## Failure Signals

- Sprint planning selects stories with unresolved dependencies
- Stories fail code review repeatedly (architecture may be insufficient)
- All stories are BLOCKED (external dependency issue)
- sprint-status.yaml diverges from actual state

## Context

Phase 3 (Solutioning) is complete. Winston (Architect) has produced the architecture, Bob (Scrum Master) has decomposed work into stories, and the Gate Reviewer has evaluated implementation readiness. This prompt guides the transition to Phase 4 (Implementation).

## Pre-Transition Checklist

Before proceeding, verify the gate result:

- [ ] `gate-report.md` exists with all 13 checklist items evaluated
- [ ] Gate result is **PASS** (or CONCERNS with documented acceptance)
- [ ] If CONCERNS: all concern items are documented with risk acceptance
- [ ] architecture.md is finalized
- [ ] All stories have acceptance criteria, estimations, and dependencies mapped
- [ ] project-context.md is up to date with coding conventions

If the gate result is FAIL, do not proceed. Return to the failing phase for remediation.

## Handoff Summary

Summarize the following for the implementation agents:

1. **Architecture Summary**: Key components, data model overview, API endpoint count.
2. **Technology Stack**: Language, framework, database, deployment target.
3. **Story Count**: Total stories, breakdown by epic, breakdown by estimation size.
4. **Critical Path**: The longest dependency chain that determines minimum timeline.
5. **Foundation Stories**: Stories with no dependencies (start here).
6. **Key ADR Decisions**: Top 3 architectural decisions that affect implementation patterns.
7. **Gate Concerns** (if any): Documented risks the team is accepting.

## Agent Activation Instructions

1. **Activate Bob (Scrum Master)** for sprint planning: Load `agents/bob-scrum-master.md`.

2. **Provide context to Bob**: Load:
   - All story files (the full backlog)
   - Dependency map
   - Velocity data (if available from previous sprints)

3. **Bob's mandate for sprint planning**:
   - Define sprint goal (value-oriented statement)
   - Select stories based on priority, dependencies, and capacity
   - Create sprint-status.yaml
   - Verify no unresolved dependencies in selected stories

4. **After sprint planning, activate Amelia (Developer)**: Load `agents/amelia-developer.md`.

5. **Provide context to Amelia**: Load:
   - sprint-status.yaml (selected stories)
   - architecture.md (system design)
   - project-context.md (coding conventions)
   - Relevant story files

6. **Amelia's mandate**: For each story in sprint order:
   - Create feature branch
   - Write tests for acceptance criteria
   - Implement following project conventions
   - Self-review before submitting for review

7. **Quinn (QA) reviews after implementation**: Load `agents/quinn-qa.md` for code review of each completed story.

## Implementation Cadence

Follow this cycle for each story:
```
Bob selects -> Amelia implements -> Quinn reviews -> Bob updates status
```

If Quinn requests changes, Amelia addresses them and resubmits. No story is DONE without Quinn's APPROVED status.

## Verification During Implementation

After each sprint:
- [ ] sprint-status.yaml is accurate
- [ ] All DONE stories have APPROVED reviews
- [ ] Tests pass for all completed stories
- [ ] Run retrospective (load `prompts/retrospective-prompt.md`)

---

**Next prompt**: `sprint-kickoff-prompt.md` (for each subsequent sprint)
