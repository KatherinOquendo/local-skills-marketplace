# Implementation Readiness Gate Evaluation

## Pre-conditions

- Phase 2 artifacts exist: `PRD.md`, `ux-spec.md`
- Phase 3 artifacts exist: `architecture.md`, at least 2 ADRs, epic files, story files
- `project-context.md` is current
- All artifacts are in their final (not draft) state

## Post-conditions

- `gate-report.md` exists with all 13 items evaluated with evidence
- Gate result is one of PASS, CONCERNS, or FAIL
- If CONCERNS: documented risk acceptance or remediation plan
- If FAIL: specific phases/artifacts identified for remediation

## Failure Signals

- Multiple checklist items have no evidence (artifacts are incomplete)
- Critical items (1, 3, 8) fail (PRD, architecture coverage, story completeness)
- Evidence is ambiguous or self-referential ("assumed complete")

## Purpose

This prompt triggers a formal gate evaluation to determine whether the project is ready for implementation. Load this prompt when transitioning from solutioning to implementation, or when validating completeness at any checkpoint.

## Setup Instructions

1. **Activate Gate Reviewer**: Load `agents/gate-reviewer.md`. The gate reviewer must be objective and evidence-driven.

2. **Load all artifacts**: Read every artifact from the planning and solutioning phases:
   - `project-context.md`
   - `product-brief.md` (if exists)
   - `PRD.md`
   - `ux-spec.md`
   - `architecture.md`
   - All ADR files (`adr-*.md`)
   - All epic files
   - All story files
   - Dependency map

3. **Build the artifact map**: Before running checks, catalog what exists and what is missing. Any missing artifact is an automatic FAIL for its related checklist item.

## The 13-Step Checklist

Evaluate each item. For every item, provide:
- **Evidence**: Cite the specific artifact and section that addresses this item
- **Result**: PASS or FAIL
- **Notes**: Any concerns, even if the item passes

### Checklist Items

1. **PRD Completeness** — All FRs have unique IDs and acceptance criteria. No placeholder text.
2. **UX Coverage** — Every user-facing FR has a corresponding element in ux-spec.md.
3. **Architecture Coverage** — Every FR maps to an architectural component or service.
4. **Data Model Completeness** — All entities are defined with fields, types, and relationships.
5. **API Contract Completeness** — All endpoints are documented with methods, paths, request/response schemas, and auth requirements.
6. **Security Design** — Authentication mechanism, authorization model, data encryption, and input validation are specified.
7. **NFR Coverage** — Each non-functional requirement has an architectural element that addresses it.
8. **Story Completeness** — Every story has acceptance criteria, estimation, and dependency information.
9. **Dependency Clarity** — No circular dependencies exist. Critical path is identified and reasonable.
10. **Tech Stack Decisions** — All major technology choices are documented in ADRs with rationale.
11. **Risk Identification** — Known risks are documented with severity and mitigation strategy.
12. **Environment Readiness** — Development environment setup is documented or scripted.
13. **Testing Strategy** — Approach for unit, integration, and E2E testing is defined with tool choices.

## Scoring

- **PASS**: All 13 items pass.
- **CONCERNS**: 1-3 non-critical items fail. Critical items (1, 3, 8) must all pass.
- **FAIL**: Any critical item fails, OR more than 3 items fail.

## Gate Report Format

Produce `gate-report.md` with the following structure:

```
# Implementation Readiness Gate Report

## Summary
- **Result**: [PASS / CONCERNS / FAIL]
- **Date**: [date]
- **Items Passed**: [count] / 13
- **Confidence Level**: [HIGH / MEDIUM / LOW]

## Detailed Results
| # | Check | Result | Evidence | Notes |
|---|-------|--------|----------|-------|
| 1 | PRD Completeness | PASS/FAIL | [artifact:section] | [notes] |
... (all 13 rows)

## Recommendations
- [List specific actions to address any FAIL or CONCERNS items]

## Risk Register
- [Outstanding risks going into implementation]
```

## Post-Gate Actions

- **If PASS**: Proceed to implementation. Load `prompts/phase-3-to-4-handoff.md`.
- **If CONCERNS**: Present concerns to user. If user accepts risks, proceed. Document acceptance.
- **If FAIL**: Identify which phase produced the failing artifacts. Return to that phase for remediation. Do not proceed.
