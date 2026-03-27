# Phase 2 Completion Checklist

**Purpose**: Verify PRD, personas, and UX spec are ready for handoff to Phase 3 (Solutioning).
**Gate owner**: PM agent or human product manager.
**Rule**: Every FAIL-marked item blocks handoff. WARN items must have documented remediation plans.

---

## PRD Completeness

- [ ] **All required PRD sections present**: Introduction, Personas, Functional Requirements, Non-Functional Requirements, User Stories (summary), UX Requirements, Success Metrics, Scope (In/Out)
- [ ] **YAML frontmatter valid** with title, version, status, author, date, product-brief-ref, stakeholders, and success-metrics fields
- [ ] **Every FR has a unique ID** in `FR-AREA-NNN` format (e.g., FR-AUTH-001) — no duplicates, no gaps that suggest deletions without explanation
- [ ] **Every FR has a priority** using MoSCoW (Must / Should / Could / Won't) or equivalent
- [ ] **NFRs have quantitative targets** — no aspirational language ("fast", "scalable") without a number attached (e.g., "p95 < 200ms", "10K concurrent users")
- [ ] **NFR measurement method documented** — each target states how it will be verified
- [ ] **Success metrics are SMART** (Specific, Measurable, Achievable, Relevant, Time-bound) with baselines where known
- [ ] **Scope boundaries explicit** — IN scope and OUT of scope sections both populated with minimum 3 out-of-scope items, each with disposition (future phase / never / deferred)

## Personas

- [ ] **At least one persona defined** with goals, frustrations, and behavioral context (not just demographics)
- [ ] **Each persona mapped to FRs** — every persona has at least one FR that serves their primary goal
- [ ] **Error states and edge-case personas considered** — admin, first-time user, power user, or equivalent role coverage

## UX Specification

- [ ] **UX spec covers all personas** — navigation model and key flows address each persona's primary journey
- [ ] **Error states included** — what the user sees on validation failure, network error, empty state, permission denied
- [ ] **Responsive behavior documented** if applicable (breakpoints, layout shifts, mobile-specific interactions)
- [ ] **Accessibility requirements stated** — WCAG level target, keyboard navigation, screen reader considerations

## Traceability and Consistency

- [ ] **Product brief reference valid** — `product-brief-ref` in PRD frontmatter points to an existing file
- [ ] **No orphan FRs** — every FR is addressable by at least one user story (summary level is sufficient at this phase)
- [ ] **No contradictions** between PRD, personas, and UX spec (e.g., PRD says "mobile-first" but UX spec only describes desktop)
- [ ] **Open questions section exists** — remaining unknowns listed with owner and target resolution date, none blocking Phase 3

## Artifact Hygiene

- [ ] **PRD committed to Git** at `planning_artifacts/PRD.md`
- [ ] **UX spec committed** at `planning_artifacts/ux-spec.md`

---

**Next**: Phase 3 — Solutioning (`workflows/full-flow/step-04-solution.md`)
**Reference**: `references/phase-2-planning.md`, `references/schemas.md`
