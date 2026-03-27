# Enterprise Governance — Multi-Team BMAD at Scale

## Table of Contents
- [Purpose](#purpose)
- [Shared project-context.md Across Teams](#shared-project-contextmd-across-teams)
- [Cross-Team Dependency Management](#cross-team-dependency-management)
- [Compliance Artifacts and Audit Trails](#compliance-artifacts-and-audit-trails)
- [Git-Based Accountability](#git-based-accountability)
- [Role-Based Access to BMAD Artifacts](#role-based-access-to-bmad-artifacts)
- [Scaling Agents Across Teams](#scaling-agents-across-teams)
- [Reporting Hierarchies](#reporting-hierarchies)
- [Integration with External Tools](#integration-with-external-tools)
- [SOC2 and HIPAA Considerations](#soc2-and-hipaa-considerations)
- [Change Management for BMAD Adoption](#change-management-for-bmad-adoption)

---

## Purpose

When BMAD is used by a single developer or a small team, governance is lightweight — a single Git repository, one project-context.md, and informal coordination. At enterprise scale (multiple teams, compliance requirements, external stakeholders), governance must become explicit without becoming bureaucratic.

This guide addresses the structures needed to run BMAD across 3 or more teams while maintaining its core benefits: documentation-first development, agent-assisted quality, and Git-based accountability.

### RACI Matrix for BMAD Roles

**[R33]** Use this RACI matrix to clarify responsibilities across BMAD activities:

| Activity | Product Manager | Architect | Developer | QA | Compliance Officer | Team Lead |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| Write PRD | **R/A** | C | I | I | C (regulated) | I |
| Architecture design | C | **R/A** | C | I | I | I |
| Story creation | **R** | C | C | C | I | **A** |
| Gate evaluation | I | **R/A** | I | C | C (regulated) | I |
| Implementation | I | C | **R/A** | I | I | I |
| Code review | I | C | **R** | C | I | **A** |
| Sprint planning | **R** | C | C | C | I | **A** |
| Compliance audit prep | I | C | I | I | **R/A** | C |
| Gate override | I | **R** | I | I | C | **A** |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

### Escalation Hierarchy

```
Level 1: Team Lead — resolves within-team blockers, sprint conflicts
Level 2: Program Lead — resolves cross-team dependency conflicts, timeline issues
Level 3: Engineering Director — resolves resource conflicts, budget decisions, process exceptions
Level 4: CTO / VP Engineering — resolves technology strategy conflicts, compliance escalations
```

**[R34]** Escalation SLAs:
- Level 1: Respond within 4 hours
- Level 2: Respond within 1 business day
- Level 3: Respond within 2 business days
- Level 4: Respond within 1 week

## Shared project-context.md Across Teams

In multi-team environments, project-context.md evolves into a hierarchical structure:

### Structure

```
organization-context.md          (org-wide: shared tech standards, common services)
  └─ program-context.md          (program-level: cross-team goals, shared dependencies)
       ├─ team-a/project-context.md  (team-level: team A's domain)
       ├─ team-b/project-context.md  (team-level: team B's domain)
       └─ team-c/project-context.md  (team-level: team C's domain)
```

### Organization Context

Contains information shared across all teams:
- Company technology standards and approved stack
- Shared service catalog (auth service, notification service, etc.)
- Cross-cutting NFRs (security baselines, accessibility requirements)
- Naming conventions and coding standards

### Program Context

Contains information shared within a program (a group of teams working toward a common product):
- Program-level PRD summary
- Cross-team architecture overview
- Shared API contracts between teams
- Program-level risk register
- Sprint/release calendar

### Team Context

Standard project-context.md scoped to one team's domain. References the program and organization contexts for shared decisions.

### Merge and Conflict Rules

When team context conflicts with program context, program context wins. When program context conflicts with organization context, organization context wins. Exceptions require documented architectural decision records (ADRs) with approval from the relevant authority.

## Cross-Team Dependency Management

### Identifying Cross-Team Dependencies

Dependencies surface at several points in the BMAD flow:

1. **Phase 2 (Architecture)**: Team A's architecture relies on Team B's API.
2. **Phase 3 (Stories)**: Team A's story S-007 is blocked by Team B's S-003.
3. **Phase 4 (Implementation)**: Team A needs Team B's service deployed to staging.

### The Dependency Contract

For each cross-team dependency, create a dependency contract:

```markdown
## Dependency Contract: DC-001

### Provider
- Team: Team B
- Service: Authentication Service
- API: POST /api/v1/auth/validate-token

### Consumer
- Team: Team A
- Story: S-007 (Order creation requires auth validation)

### Contract
- Request: { token: string }
- Response 200: { valid: boolean, userId: string, roles: string[] }
- Response 401: { error: { code: "TOKEN_INVALID" } }
- SLA: p95 < 50ms, availability 99.9%

### Timeline
- Contract agreed: 2025-01-15
- Provider delivery: 2025-01-22 (staging), 2025-01-29 (production)
- Consumer integration: starts after staging delivery

### Escalation
- If delivery slips by > 3 days, escalate to Program Lead.
- Consumer must have a mock/stub available from contract agreement date.
```

### Dependency Board

Maintain a cross-team dependency board (can be a markdown file, a Jira board, or a GitHub Project):

| DC ID | Provider | Consumer | Status | Risk |
|-------|----------|----------|--------|------|
| DC-001 | Team B (Auth) | Team A (Orders) | On track | Low |
| DC-002 | Team C (Payments) | Team A (Checkout) | Delayed 2d | Medium |

Review this board in a weekly cross-team sync (15-30 minutes).

## Compliance Artifacts and Audit Trails

BMAD's documentation-first approach naturally produces artifacts that satisfy compliance requirements. The key is organizing them for auditors.

### Artifact Mapping to Compliance

| BMAD Artifact | SOC2 Control | HIPAA Safeguard | ISO 27001 |
|--------------|-------------|-----------------|-----------|
| PRD with security section | CC6.1 (Logical access) | 164.312(a)(1) Access control | A.9 Access control |
| Architecture doc | CC6.6 (System boundaries) | 164.312(e)(1) Transmission security | A.13 Communications security |
| Gate report | CC8.1 (Change management) | 164.312(c)(1) Integrity | A.14 System acquisition |
| Story acceptance criteria | CC8.1 (Testing) | 164.312(c)(2) Mechanism to authenticate ePHI | A.14.2 Security in development |
| Git commit history | CC7.2 (Monitoring) | 164.312(b) Audit controls | A.12.4 Logging |
| Rollback plan | CC7.4 (Incident response) | 164.308(a)(6) Contingency plan | A.17 Business continuity |

### Compliance Directory Structure

```
compliance/
  audit-trail/
    gate-reports/         (all gate reports, dated)
    change-records/       (PRD change log, architecture decisions)
    access-reviews/       (who has access to what artifacts)
  policies/
    security-baseline.md  (maps to organization-context.md security section)
    data-handling.md      (data classification, retention, encryption)
    incident-response.md  (references rollback plans)
```

### Audit-Ready Gate Reports

Enhance the standard gate report for compliance environments:

```markdown
## Gate Report — [Feature Name]
Date: [YYYY-MM-DD]
Reviewer: [Name/Agent ID]
Approved by: [Name] (human approval required for regulated features)

### Results
[Standard 13-step results]

### Compliance Notes
- Data classification: [Public/Internal/Confidential/Restricted]
- PHI/PII involved: [Yes/No]
- Third-party data sharing: [Yes/No, with data processing agreement reference]
- Regulatory review required: [Yes/No]

### Signatures
- Technical reviewer: [Name, Date]
- Security reviewer: [Name, Date] (if security-relevant)
- Compliance officer: [Name, Date] (if regulated)
```

## Git-Based Accountability

BMAD's Git-first approach provides accountability out of the box. Enterprise environments need additional structure.

### Commit Message Standards

```
<type>(scope): <description>

Types: feat, fix, docs, gate, story, arch, prd, security
Scope: component or artifact name
```

Examples:
```
docs(prd): add payment processing requirements for Q2
gate(checkout): pass implementation readiness gate (13/13 PASS)
story(S-007): create order creation story with 8 acceptance criteria
arch(auth): switch from session-based to JWT auth (ADR-005)
```

### Branch Strategy for BMAD Artifacts

```
main                        (production-ready artifacts)
  └─ docs/prd-v2            (PRD revisions — PR required)
  └─ docs/arch-auth-update  (Architecture changes — PR required)
  └─ stories/sprint-12      (New stories for sprint 12)
  └─ feature/S-007          (Implementation of story S-007)
```

All BMAD artifact changes go through pull requests with at least one reviewer.

### Blame and History

Git blame on BMAD artifacts answers compliance questions:
- Who wrote this requirement? `git blame docs/prd.md`
- When was this architecture decision made? `git log --follow docs/architecture.md`
- Who approved this gate report? `git log --all -- compliance/gate-reports/`

## Role-Based Access to BMAD Artifacts

### Access Matrix

| Role | PRD | Architecture | Stories | Gate Reports | Code | Compliance |
|------|-----|-------------|---------|-------------|------|------------|
| Product Manager | Read/Write | Read | Read/Write | Read | — | Read |
| Architect | Read | Read/Write | Read | Read/Write | Read | Read |
| Developer | Read | Read | Read | Read | Read/Write | — |
| QA Engineer | Read | Read | Read/Write | Read | Read | Read |
| Compliance Officer | Read | Read | Read | Read/Write | — | Read/Write |
| Team Lead | Read | Read | Read/Write | Read/Write | Read | Read |
| External Auditor | Read | Read | Read | Read | — | Read |

### Implementation

Use Git repository permissions (GitHub Teams, GitLab Groups) to enforce access:
- `docs/` directory: accessible to all team roles
- `compliance/` directory: restricted to compliance officers and team leads
- `src/` directory: accessible to developers, read-only for others
- Branch protection: `main` requires PR approval from designated reviewers

## Scaling Agents Across Teams

### Shared Agent Definitions

In multi-team setups, agent definitions are shared at the organization level:

```
org-bmad/
  agents/
    pm.agent.yaml          (shared PM agent definition)
    architect.agent.yaml   (shared Architect agent definition)
    developer.agent.yaml   (shared Developer agent definition)
  templates/
    prd-template.md
    story-template.md
    architecture-template.md
```

Teams consume these shared definitions and can extend them with team-specific customizations (see `customization-guide.md`).

### Agent Consistency

When multiple teams use the same agent definitions:
- PRDs from different teams follow the same structure.
- Architecture documents are cross-readable.
- Stories have consistent acceptance criteria format.
- Gate reports are comparable across teams.

This consistency enables program-level reporting and cross-team reviews.

### Team-Specific Agent Extensions

Teams can add agent menu items for domain-specific workflows:

```yaml
# Team B's extension to the shared Architect agent
extends: org-bmad/agents/architect.agent.yaml
additional_menu:
  - trigger: HC
    description: HIPAA Compliance Check
    workflow: team-b/workflows/hipaa-check.md
```

## Reporting Hierarchies

### Team-Level Reports

Each team produces weekly:
- Stories completed vs planned
- Gate pass rate (first attempt vs re-evaluation)
- Technical debt items created vs resolved
- Artifact currency (how up-to-date are docs)

### Program-Level Reports

Program leads aggregate weekly:
- Cross-team dependency status
- Feature completion across teams
- Risk register changes
- Gate failure patterns (which steps fail most across teams)

### Executive Reports

Monthly or quarterly:
- Features delivered through BMAD vs ad-hoc
- Quality metrics (defect rates for BMAD-managed vs unmanaged features)
- Compliance posture (artifact completeness for regulated features)
- BMAD adoption metrics (percentage of work following the process)

### Report Generation

BMAD artifacts in Git enable automated reporting:
- Count stories by status from story file metadata
- Calculate gate pass rates from gate report files
- Track artifact freshness from Git commit dates
- Generate dependency status from contract files

## Integration with External Tools

### Jira / Linear / GitHub Projects

BMAD artifacts are the source of truth. External tools provide workflow management.

**Sync pattern**:
```
BMAD Story File (Git) ──creates──> Jira Ticket
                      ──updates──> Jira Ticket status
Jira Ticket           ──links to──> BMAD Story File (via URL in description)
```

**What lives where**:
- Requirements, acceptance criteria, architecture: Git (BMAD artifacts)
- Status, assignments, sprint boards, time tracking: Jira/Linear
- Discussion, decisions: PR comments (linked from Jira)

### Slack / Teams Integration

- Gate pass/fail notifications to team channels
- Dependency contract status changes to program channel
- New story creation notifications to relevant team channels
- Compliance artifact review reminders

### CI/CD Integration

- Pre-merge: validate BMAD artifact schemas (story files have required fields)
- Pre-deploy: verify gate report exists and passes for all stories in the release
- Post-deploy: update project-context.md deployment status automatically

## SOC2 and HIPAA Considerations

### SOC2 Type II

BMAD naturally supports SOC2 through:

**Change Management (CC8.1)**:
- Every change starts as a BMAD story with acceptance criteria.
- Stories pass through the implementation readiness gate.
- Code changes are traceable to stories via commit messages.
- Gate reports document what was reviewed before implementation.

**Monitoring (CC7.2)**:
- Git history provides a complete audit trail.
- Gate reports document periodic review of system changes.
- Artifact freshness reports show documentation currency.

**Risk Management (CC3.2)**:
- Risk registers are maintained as BMAD artifacts.
- Risks are reviewed at each gate evaluation.
- Mitigation strategies are documented and tracked.

### HIPAA

For projects handling Protected Health Information (PHI):

**Access Controls (164.312(a)(1))**:
- PRD security section documents access control requirements.
- Architecture doc defines authentication and authorization boundaries.
- Gate Step 10 (Security Review) verifies access controls before implementation.

**Audit Controls (164.312(b))**:
- Git history provides artifact-level audit trail.
- Audit logging stories ensure application-level audit trails.
- Gate reports document review of audit requirements.

**Integrity (164.312(c)(1))**:
- Acceptance criteria include data integrity checks.
- Data model review (Gate Step 9) verifies integrity constraints.
- Test coverage tied to acceptance criteria provides ongoing integrity verification.

**Additional HIPAA requirements for BMAD artifacts**:
- PHI must never appear in BMAD artifacts (use references, not actual data).
- Story acceptance criteria must include de-identification requirements where applicable.
- Gate reports for PHI-handling features require compliance officer sign-off.

## Change Management for BMAD Adoption

### The Adoption Curve

Enterprise BMAD adoption follows a predictable curve:

**Phase A — Champion (Weeks 1-4)**:
- 1-2 teams pilot BMAD on non-critical projects.
- Champions receive training and support.
- Success metrics defined (quality, velocity, documentation coverage).

**Phase B — Early Adoption (Weeks 5-12)**:
- Pilot results shared with other teams.
- 3-5 teams adopt BMAD for new features.
- Shared agent definitions and templates established.
- First cross-team dependency contracts created.

**Phase C — Majority Adoption (Months 3-6)**:
- BMAD becomes the default process for new features.
- Compliance team integrates BMAD artifacts into audit preparation.
- Reporting hierarchies established.
- Legacy projects begin brownfield adoption (see `brownfield-patterns.md`).

**Phase D — Maturity (Months 6+)**:
- All new work follows BMAD.
- Process improvements fed back into shared definitions.
- BMAD metrics integrated into engineering KPIs.
- External tool integrations fully automated.

### Resistance Patterns and Responses

| Resistance | Root Cause | Response |
|------------|-----------|----------|
| "Too much process" | Team has been successful with ad-hoc | Show BMAD quick flow. Demonstrate time saved from reduced rework. |
| "My team is different" | Team has domain-specific needs | Customize templates for their domain. Show customization-guide.md. |
| "We already have a process" | Existing process works adequately | Show coexistence path — BMAD layers on, does not replace. |
| "AI agents cannot understand our code" | Skepticism about AI quality | Pilot with a real project. Let results speak. Focus on documentation value even without AI. |
| "Management wants metrics we cannot produce" | Reporting anxiety | Show automated reporting from Git-based artifacts. |

### Success Metrics for Adoption

Track these metrics to demonstrate BMAD value:

- **Defect rate**: Compare defect rates for BMAD-managed vs non-BMAD features.
- **Rework rate**: Measure how often stories need re-implementation after initial completion.
- **Documentation currency**: Percentage of artifacts updated within the last sprint.
- **Gate first-pass rate**: Percentage of gate evaluations that pass on the first attempt (target: >70%).
- **Onboarding time**: How quickly new team members become productive (measured by time to first merged PR).
- **Audit preparation time**: Hours spent preparing for compliance audits (must decrease over time).

### Audit Checklist for Compliance

**[R35]** Run this checklist before any compliance audit:

- [ ] All gate reports for the audit period are committed to `compliance/audit-trail/gate-reports/`
- [ ] Every deployed feature has a traceable path: Story -> FR -> PRD -> Brief
- [ ] All ADRs are current (no deprecated ADRs referencing active technology)
- [ ] Access review has been conducted within the last 90 days
- [ ] All overridden gate steps have documented remediation (resolved or in-progress with deadline)
- [ ] project-context.md for each team is current (staleness check passes)
- [ ] Compliance-relevant stories (security, PHI, PII) have compliance officer sign-off on gate reports
- [ ] Git history shows who authored and who approved each artifact change

---

## Assumptions

- The organization has 3+ teams that will adopt or have adopted BMAD
- A compliance framework (SOC2, HIPAA, ISO 27001, or equivalent) applies to at least some projects
- Teams use a shared Git platform (GitHub, GitLab, Bitbucket) with branch protection capabilities

## Limits

- This guide does NOT cover specific regulatory certification processes — consult your compliance team
- This guide does NOT prescribe organizational structure — it provides governance patterns that adapt to existing structures
- This guide does NOT cover financial governance or budget management

## Edge Cases

- **Team uses a different VCS than the organization standard**: BMAD requires Git-based accountability. If a team uses a different VCS, they must mirror BMAD artifacts to a Git repository for compliance purposes.
- **External contractor team needs BMAD access**: Use read-only access to shared artifacts. Contractor-produced artifacts go through the same PR review process but require additional sign-off from the owning team lead.
- **Acquisition introduces a team with incompatible processes**: Treat as a brownfield adoption. See `references/brownfield-patterns.md`. Do not force immediate BMAD compliance — use the phased migration plan.

## Acceptance Criteria

- [ ] RACI matrix is documented and communicated to all teams
- [ ] Escalation hierarchy is defined with SLAs per level
- [ ] Shared agent definitions exist in a central repository
- [ ] Cross-team dependency contracts exist for all known dependencies
- [ ] Audit checklist passes before every compliance audit

See also: `references/methodology-overview.md`, `references/customization-guide.md`, `references/brownfield-patterns.md`, `references/implementation-readiness-gate.md`
