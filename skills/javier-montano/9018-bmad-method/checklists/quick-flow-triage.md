# Quick Flow Triage Checklist

**Purpose**: Verify a change qualifies for Quick Flow before bypassing the full BMAD process.
**Gate owner**: Barry agent (Quick Flow) or human developer.
**Rule**: If any item fails, the change must go through Full BMAD starting at the indicated phase. Quick Flow is a privilege, not a default.

---

## Eligibility

- [ ] **Scope is 3 story points or fewer** — if you cannot confidently estimate it at 3 or below, it is not a Quick Flow candidate
- [ ] **No architectural changes** — the change works entirely within existing component boundaries, communication patterns, and infrastructure; no new services, no new inter-service calls
- [ ] **No new external dependencies** — no new third-party libraries, APIs, or services are introduced (updating an existing dependency version is acceptable if tests pass)
- [ ] **No data model changes** — no new database tables, columns, indexes, or migrations; no changes to entity relationships
- [ ] **Existing test coverage exists** for the affected area — you are modifying code that already has tests, not writing tests for a previously untested module
- [ ] **`project-context.md` exists and is current** — conventions, tech stack, and constraints are documented; Quick Flow relies on this context being accurate
- [ ] **Not the 4th consecutive Quick Flow** in the same feature area — if 3 Quick Flows have already landed in this area without consolidation, stop and assess per [R10] in `references/quick-flow.md`
- [ ] **No security-sensitive changes** — the change does not touch authentication, authorization, encryption, or input validation for external-facing endpoints

---

## If Any Item Fails

| Failed Item | Escalation Target |
|-------------|-------------------|
| Scope > 3 points | Phase 3 (story decomposition) |
| Architectural change | Phase 3 (architecture review) |
| New dependency | Phase 3 (ADR required) |
| Data model change | Phase 3 (data model review) |
| No test coverage | Phase 4 (write tests first as a separate story) |
| No project-context.md | Phase 1 or `scripts/init_project.py` |
| 4th consecutive Quick Flow | Consolidation review, then Phase 3 if warranted |
| Security-sensitive | Phase 3 (security review, gate step 10) |

---

**Reference**: `references/quick-flow.md`, `workflows/quick-flow/step-01-triage.md`
