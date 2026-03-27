# Phase 3 Completion Checklist

**Purpose**: Verify architecture, epics, and stories are ready for the Implementation Readiness Gate.
**Gate owner**: Architect agent or human tech lead.
**Rule**: This checklist is a pre-flight before the formal 13-step gate. Passing this checklist does not replace the gate — it increases the probability of first-pass gate success.

---

## Architecture Document

- [ ] **All required architecture sections present**: System Overview, Architecture Style, C4 Diagrams (L1-L3), Data Model, API Design, Infrastructure, Security Architecture, Key ADRs, NFR Mapping, Risks and Mitigations
- [ ] **Architecture addresses every FR** in the PRD — each FR maps to at least one architecture component
- [ ] **Architecture addresses every NFR** — each NFR has a documented architectural approach (e.g., caching for performance, horizontal scaling for throughput)
- [ ] **ADRs exist for every major decision** — technology choices, architectural style, build-vs-buy, data storage engine selections each have an ADR in `ADR-NNN` format
- [ ] **ADR statuses are current** — no ADRs left in `proposed` status that should be `accepted` or `deprecated`
- [ ] **Data model covers all entities** referenced in the PRD and API contracts — no phantom entities (used but undefined) or orphan entities (defined but unused)
- [ ] **API contracts defined** for all external-facing endpoints with request/response schemas, status codes, auth requirements, and error format
- [ ] **Security architecture documented** — authentication method, authorization model (RBAC/ABAC), input validation strategy, encryption (at rest and in transit)

## Epic Decomposition

- [ ] **Epics created** in `epics/` directory with valid YAML frontmatter per `references/schemas.md`
- [ ] **Every epic references PRD FRs** via `prd-refs` field — no epic exists without traceability to requirements
- [ ] **Epic dependencies mapped** — `blocks` / `blocked-by` / `related` relationships documented, no circular dependencies

## Story Files

- [ ] **Stories created** in `stories/` directory with valid YAML frontmatter (story-id, epic-ref, title, status, points, priority, fr-refs)
- [ ] **Every story has acceptance criteria** in Given/When/Then format with minimum 1 criterion per story
- [ ] **`acceptance-criteria-count` matches actual AC count** in the story body
- [ ] **Story points estimated** — all stories have points in {1, 2, 3, 5, 8}; any 13-point story must be split
- [ ] **Story dependencies mapped** — `blocks` / `blocked-by` relationships documented, dependency graph is a DAG (no cycles)
- [ ] **Every PRD FR covered** — at least one story traces to each FR via `fr-refs`; no orphan FRs remain
- [ ] **No orphan stories** — every story references a valid epic via `epic-ref`

## Cross-Artifact Consistency

- [ ] **Architecture `prd-ref`** points to the actual PRD file
- [ ] **Tech stack in architecture matches `project-context.md`** — no version or technology contradictions
- [ ] **Scope boundaries respected** — no stories or architecture components address items explicitly listed as out-of-scope in the PRD

## Gate Readiness

- [ ] **All artifacts committed to Git** — architecture, ADRs, epics, stories
- [ ] **Implementation Readiness Gate can be run** — all 13-step inputs are available (PRD, architecture, stories, project-context.md)

---

**Next**: Implementation Readiness Gate (`references/implementation-readiness-gate.md`)
**Reference**: `references/phase-3-solutioning.md`, `references/schemas.md`, `references/artifact-flow-chain.md`
