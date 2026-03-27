# BMAD Example: Brownfield Migration (Django Monolith)

## Scenario

A 4-year-old Django monolith ("ShopWave" — an e-commerce platform) needs to be
decomposed into services. The codebase has 180K lines of Python, 40+ Django apps,
and no formal architecture documentation. The team of 6 has tribal knowledge but
nothing written down.

This walkthrough shows how BMAD adapts to brownfield projects where code already
exists and the goal is migration, not greenfield construction.

---

## Step 1: Skip Phase 1 (Analysis) — You Already Have a Product

In a brownfield project, the product already exists. You don't need Mary (Analyst)
to validate the idea — the market has validated it. Instead, the analysis phase
becomes a **documentation recovery** exercise.

**What to do**:
- Run the `Document Project` script to scan the existing codebase
- Generate a `project-context.md` from the scan output
- Fill in the gaps manually: team roster, deployment URLs, conventions that
  exist as tribal knowledge

```
python scripts/init_project.py shopwave-migration --brownfield
```

This creates the project skeleton with a `project-context.md` pre-populated
from the codebase analysis (detected Django, PostgreSQL, Redis, Celery).

## Step 2: Generate project-context.md from Codebase Scan

The brownfield init script produces a starter context file. Key sections to
review and complete manually:

- **Tech Stack**: Auto-detected from `requirements.txt`, `settings.py`, and
  `docker-compose.yml`. Verify versions and add rationale for each choice.
- **Constraints**: Add budget, timeline, and regulatory constraints that the
  code scan cannot detect. For ShopWave: PCI-DSS compliance for payment
  processing, 99.95% uptime SLA, and a 6-month migration window.
- **Conventions**: Document the team's actual practices — not aspirational
  ones. If the team uses feature branches but never squash-merges, write that.

## Step 3: Start at Phase 2 — Retroactive PRD

Even though the product exists, you need a PRD to scope the **migration** work.
Activate John (PM Agent) with a modified prompt:

> "We are migrating ShopWave from a Django monolith to a service-oriented
> architecture. The PRD should define the target state, not the current state.
> Focus on which Django apps become independent services, what the boundaries
> are, and what the migration sequence looks like."

The PRD for a brownfield migration typically has:
- **Current state**: What the monolith does today (extracted from codebase scan)
- **Target state**: The desired service boundaries
- **Migration requirements**: What must continue working during migration
  (no downtime, data consistency, rollback capability)
- **Functional requirements**: Framed as "Service X must handle Y" rather than
  "Users can do Z" (the user-facing features already exist)

## Step 4: Phase 3 — Architecture with Migration Strategy

Winston (Architect Agent) produces the architecture document, but with a
critical difference from greenfield: the architecture must include a
**migration path** — not just a target state.

Key additions for brownfield architecture:
- **Strangler Fig pattern**: Which components get extracted first?
- **Data migration strategy**: How do shared database tables get split?
- **API gateway**: How do old and new services coexist during migration?
- **Feature flags**: Which migrations are behind toggles?

Example ADR for ShopWave:

> **ADR-001: Strangler Fig over Big Bang Migration**
> - Context: 180K lines of coupled Django code cannot be rewritten at once.
> - Decision: Extract services one Django app at a time, using an API gateway
>   to route traffic between monolith and new services.
> - Consequences: Longer migration timeline but zero-downtime and rollback
>   capability at each step.

## Step 5: Decompose Migration into Epics

Each service extraction becomes an epic. Bob (Scrum Master) creates epics like:

| Epic      | Title                              | Dependencies        |
|-----------|------------------------------------|--------------------|
| EPIC-001  | Extract User Service from monolith | None (foundation)  |
| EPIC-002  | Extract Product Catalog Service    | EPIC-001           |
| EPIC-003  | Extract Order Service              | EPIC-001, EPIC-002 |
| EPIC-004  | Extract Payment Service            | EPIC-003, PCI audit|
| EPIC-005  | Decommission monolith auth module  | EPIC-001 verified  |

Each epic's stories follow the pattern:
1. Set up new service skeleton
2. Implement API contract (matching existing behavior)
3. Add integration tests verifying parity with monolith
4. Route traffic via feature flag
5. Monitor and verify
6. Remove monolith code (decommission story)

## Step 6: Implementation with Safety Gates

Phase 4 operates normally, but the Implementation Readiness Gate adds
brownfield-specific checks:

- [ ] Rollback procedure documented for each service extraction
- [ ] Data migration script tested on staging copy of production data
- [ ] Feature flag configuration verified in all environments
- [ ] Monitoring dashboards updated to track new service health
- [ ] Load testing completed with traffic split between old and new

---

## Key Takeaways

1. **Skip or compress Phase 1** — the product exists, analysis becomes documentation recovery
2. **PRD defines the migration**, not the product features
3. **Architecture must include the migration path**, not just the end state
4. **Epics map to service extractions**, not feature deliveries
5. **The gate adds migration-specific safety checks** on top of standard readiness criteria

## Lessons Learned

- **What went right**: Using the `--brownfield` flag on `init_project.py` created the `project-knowledge/` directory from the start, which became the natural home for codebase scan results. Without it, the team would have created ad-hoc documentation locations.
- **What was tricky**: Writing a PRD for a migration is fundamentally different from a greenfield PRD. The "problem statement" is not a user pain point but a technical debt problem. The team had to reframe the PRD template's sections for migration context.
- **Key insight**: The Strangler Fig pattern maps perfectly to BMAD's epic structure. Each service extraction is an epic with a predictable story pattern (skeleton, API contract, integration tests, traffic routing, monitoring, decommission). This pattern can be templated.

## Decisions Made

- **Strangler Fig over Big Bang**: Despite pressure to "just rewrite it," the incremental approach was chosen for its rollback capability. Trade-off: 6-month migration window instead of 3-month rewrite attempt, but with zero-downtime guarantee.
- **User Service first**: Extracted the User Service before any other because it has the most dependencies. Trade-off: hardest service first, but once done, all subsequent extractions have a proven pattern to follow.
- **PRD focuses on migration, not features**: The team resisted the urge to add new features during migration. Trade-off: no new capabilities during the 6-month window, but the migration stays on track.

## Files You Would Produce

```
shopwave-migration/
  project-context.md        ← Generated from codebase scan + manual additions
  product-brief.md          ← Skipped or minimal (product already exists)
  prd.md                    ← Migration-focused requirements
  architecture.md           ← Target architecture + migration strategy
  epics/
    epic-001-user-service.md
    epic-002-product-catalog.md
    epic-003-order-service.md
  stories/
    story-001-user-service-skeleton.md
    story-002-user-api-contract.md
    ...
  sprint-status.yaml        ← Tracks migration progress
```
