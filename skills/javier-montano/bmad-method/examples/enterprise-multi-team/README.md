# BMAD Example: Enterprise Multi-Team Platform

## Scenario

Three teams at a mid-size fintech company ("PayBridge") are building a shared
payment processing platform. Each team owns a different domain but they share
infrastructure, a common API gateway, and compliance requirements. The teams:

- **Team Payments** (6 engineers): Core payment processing, ledger, settlements
- **Team Identity** (4 engineers): KYC/AML, user verification, fraud detection
- **Team Merchant** (5 engineers): Merchant onboarding, dashboard, reporting

This walkthrough shows how BMAD scales to multi-team, enterprise contexts with
shared governance and cross-team dependencies.

---

## Shared Project Context

All three teams share a single `project-context.md` that defines the platform-
level decisions. Team-specific details live in separate context files.

```
paybridge-platform/
  project-context.md            ← Shared: tech stack, compliance, conventions
  team-payments/
    team-context.md             ← Team-specific: roster, repos, services
    prd.md
    architecture.md
    epics/
    stories/
    sprint-status.yaml
  team-identity/
    team-context.md
    prd.md
    architecture.md
    epics/
    stories/
    sprint-status.yaml
  team-merchant/
    team-context.md
    prd.md
    architecture.md
    epics/
    stories/
    sprint-status.yaml
  shared/
    api-contracts/              ← Shared API schemas (OpenAPI / protobuf)
    compliance-artifacts/       ← SOC2, PCI-DSS documentation
    gate-reviews/               ← Cross-team gate review records
```

### What Goes in the Shared project-context.md

- **Platform vision**: Unified payment processing platform
- **Tech stack mandates**: All teams use Go for services, PostgreSQL for data,
  gRPC for inter-service communication, Kubernetes for deployment
- **Compliance constraints**: PCI-DSS Level 1, SOC2 Type II, GDPR
- **Shared conventions**: Protobuf-first API design, trunk-based development,
  commit signing required, mandatory code review by 2 reviewers
- **Infrastructure**: Shared Kubernetes cluster, shared observability stack
  (Datadog), shared CI/CD pipeline (GitHub Actions)

### What Goes in Team-Specific Context

- Team roster, on-call rotation, Slack channels
- Team-owned repositories and services
- Team-specific tools (e.g., Team Identity uses a specialized fraud ML model)
- Sprint cadence (teams may run different sprint lengths)

## Cross-Team Epics with Dependencies

The most complex part of multi-team BMAD is managing cross-team dependencies.
Each team creates their own epics, but some epics have explicit dependencies
on other teams' work.

Example dependency chain for a new feature ("Instant Payouts"):

| Epic                        | Team      | Depends On                    |
|-----------------------------|-----------|-------------------------------|
| EPIC-P-007: Instant Ledger  | Payments  | None                          |
| EPIC-I-004: Payout KYC Check| Identity  | None                          |
| EPIC-P-008: Payout API      | Payments  | EPIC-P-007, EPIC-I-004        |
| EPIC-M-012: Payout Dashboard| Merchant  | EPIC-P-008 (API contract only)|

**Dependency management rules**:
1. Cross-team dependencies must be declared in the epic's `dependencies` field
2. The dependent team cannot start their epic until the dependency is "API
   contract approved" (not necessarily fully implemented)
3. API contracts are committed to `shared/api-contracts/` and reviewed by
   both teams before work begins
4. A cross-team dependency creates a mandatory sync meeting (30 min max)

## Centralized Gate Review

In enterprise BMAD, the Implementation Readiness Gate is run at two levels:

### Team-Level Gate (Standard)

Each team runs the standard 13-point gate checklist before starting Phase 4
on their own epics. This is the same gate used in single-team BMAD.

### Platform-Level Gate (Enterprise Addition)

Before a cross-team feature goes to production, a platform-level gate review
is conducted. This review is stored in `shared/gate-reviews/`:

```markdown
# Gate Review: Instant Payouts Feature
Date: 2025-04-15
Participants: Tech leads from Payments, Identity, Merchant

## Cross-Team Checklist
- [x] All API contracts finalized and committed to shared/api-contracts/
- [x] Integration tests between Payments and Identity services passing
- [x] Integration tests between Payments and Merchant services passing
- [x] Load test completed with realistic cross-service traffic patterns
- [x] Rollback procedure documented for each team's deployment
- [x] Compliance review completed (PCI-DSS impact assessment)
- [x] Observability: cross-service tracing configured and verified
- [ ] Canary deployment plan approved by platform SRE

## Decision: CONDITIONAL PASS
Proceed with canary deployment. Full rollout blocked until canary
metrics confirm < 0.1% error rate over 24 hours.
```

## Compliance Artifact Generation

Enterprise projects often need compliance documentation as a deliverable.
BMAD's artifact chain naturally produces most of what auditors need:

| Compliance Need              | BMAD Artifact                          |
|------------------------------|----------------------------------------|
| Requirements traceability    | PRD (FR-IDs) → Epics → Stories         |
| Architecture decisions       | Architecture doc + ADR index           |
| Change management records    | Git history + sprint-status.yaml       |
| Testing evidence             | Story acceptance criteria + CI reports |
| Access control documentation | project-context.md team roster + roles |
| Risk assessment              | PRD risk table + gate review records   |

For SOC2 and PCI-DSS audits, the `compliance-artifacts/` directory contains
generated reports that cross-reference BMAD artifacts:

- **Requirements Traceability Matrix**: Auto-generated from PRD FR-IDs mapped
  to epic IDs and story IDs
- **Change Log**: Aggregated from all teams' sprint-status.yaml files
- **Architecture Review Record**: Gate review documents with sign-offs

## Key Differences from Single-Team BMAD

| Aspect               | Single-Team                | Multi-Team Enterprise          |
|----------------------|----------------------------|---------------------------------|
| project-context.md   | One file                   | Shared + per-team context files |
| PRD                  | One document               | One per team, shared vision doc |
| Architecture         | One document               | Per-team + platform architecture|
| Epics                | Independent                | Cross-team dependency tracking  |
| Gate review          | Self-assessed              | Platform-level review meeting   |
| Compliance           | Not usually required       | Automated artifact generation   |
| Sprint status        | One YAML file              | Per-team YAML + aggregated view |

## Scaling Tips

1. **Assign a Platform Architect** — one person (or agent) who reviews all
   three teams' architecture docs for consistency and conflict
2. **API-first dependencies** — teams should be blocked only on API contracts,
   not on full implementations. Mock services unblock parallel work.
3. **Stagger gate reviews** — don't gate all teams simultaneously. Let each
   team pass their own gate, then do the platform gate for cross-cutting features.
4. **Shared retrospectives** — run a cross-team retro every 4 sprints to
   identify systemic issues (tooling, conventions, dependency bottlenecks)
5. **Automate compliance** — use scripts to generate traceability matrices
   from the BMAD artifact chain rather than maintaining them manually

<!-- NOTE: This example shows BMAD at its most complex scale. The key takeaway
     is that the same 4-phase structure works — but governance layers (shared
     context, platform gate, cross-team dependency protocols) are added on top.
     A reader should understand that multi-team BMAD is single-team BMAD plus
     coordination, not a fundamentally different process. -->

## Lessons Learned

- **What went right**: Committing API contracts to `shared/api-contracts/` before implementation began allowed all three teams to start work in parallel. Team Merchant built against the Payout API contract mock while Team Payments built the real implementation.
- **What was tricky**: The platform-level gate review was initially a 2-hour meeting. It was reduced to 45 minutes by requiring teams to submit their gate evidence asynchronously, using the meeting only for unresolved items and cross-team concerns.
- **Key insight**: The biggest risk in multi-team BMAD is not technical — it is the dependency handoff. The "API contract approved" milestone (not "fully implemented") as the dependency resolution criterion unlocked significant parallelism.

## Decisions Made

- **Shared project-context.md with per-team extensions**: A single source of truth for platform decisions (tech stack, compliance, conventions) prevents drift. Trade-off: teams cannot unilaterally adopt new technologies, but consistency across services is maintained.
- **Cross-team dependency protocol**: Teams are blocked only on API contracts, not implementations. Trade-off: teams may build against contracts that later change, but contract versioning and integration tests catch mismatches early.
- **Compliance artifact generation**: Automated RTM (Requirements Traceability Matrix) generation from BMAD artifacts. Trade-off: initial script development cost, but eliminates manual audit preparation that previously took 2 weeks per quarter.
