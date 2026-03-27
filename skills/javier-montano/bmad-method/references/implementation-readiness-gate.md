# Implementation Readiness Gate — Full 13-Step Specification

## Table of Contents
- [Purpose](#purpose)
- [Gate Overview](#gate-overview)
- [Scoring Rules](#scoring-rules)
- [The 13 Steps](#the-13-steps)
  - [Step 1: PRD Completeness](#step-1-prd-completeness)
  - [Step 2: Architecture Alignment](#step-2-architecture-alignment)
  - [Step 3: Story Decomposition](#step-3-story-decomposition)
  - [Step 4: Acceptance Criteria Quality](#step-4-acceptance-criteria-quality)
  - [Step 5: Dependency Mapping](#step-5-dependency-mapping)
  - [Step 6: Risk Register](#step-6-risk-register)
  - [Step 7: NFR Coverage](#step-7-nfr-coverage)
  - [Step 8: API Contracts](#step-8-api-contracts)
  - [Step 9: Data Model](#step-9-data-model)
  - [Step 10: Security Review](#step-10-security-review)
  - [Step 11: Performance Targets](#step-11-performance-targets)
  - [Step 12: Deployment Strategy](#step-12-deployment-strategy)
  - [Step 13: Rollback Plan](#step-13-rollback-plan)
- [Remediation Guidance](#remediation-guidance)
- [Re-Evaluation Process](#re-evaluation-process)

---

## Purpose

The Implementation Readiness Gate is the mandatory checkpoint between Phase 3 (Solutioning) and Phase 4 (Implementation). It prevents premature coding by verifying that all upstream artifacts are complete, consistent, and actionable. **[R20]** No story enters development without passing this gate.

The gate exists because AI-assisted code generation amplifies both good and bad inputs. A missing constraint in the PRD becomes hundreds of lines of wrong code within minutes. The gate catches these gaps before that amplification occurs.

### Gate Override Procedure

**[R21]** Overrides are exceptional and must follow this protocol:

| Step | Action | Required |
|------|--------|----------|
| 1 | Document which step(s) are being overridden and why | Written justification per step |
| 2 | Identify the override authority | Human architect or tech lead (agents cannot override gates) |
| 3 | Set a remediation deadline | Must not exceed 1 sprint from override date |
| 4 | Log the override in the gate report | Include: who, when, why, deadline |
| 5 | Create a remediation story | Story must be in the current or next sprint backlog |

**Override audit trail format**:
```markdown
## Override Record
- Step overridden: [Step number and name]
- Override authority: [Name and role]
- Date: [ISO 8601]
- Justification: [Why this cannot wait]
- Remediation deadline: [Date]
- Remediation story: [STORY-ID]
- Resolved: [Yes/No — date if yes]
```

**[R22]** No more than 2 steps may be overridden simultaneously. If 3+ steps require override, the gate has fundamentally failed and must not be overridden — return to Phase 3.

### Partial Gate for MVPs

For MVP/prototype projects, the gate can run in partial mode with reduced scope:

| MVP Gate (6 steps) | Full Gate Equivalent |
|--------------------|---------------------|
| Step 1: PRD Completeness | Same (required) |
| Step 2: Architecture Alignment | Same (required) |
| Step 3: Story Decomposition | Same |
| Step 4: Acceptance Criteria Quality | Same |
| Step 8: API Contracts | Same (required) |
| Step 10: Security Review | Same (required) |

**[R23]** MVP partial gate still requires zero FAILs on included steps. Steps 5-7, 9, 11-13 are documented as "Deferred — MVP" in the gate report.

## Gate Overview

**When**: After story creation, before any implementation begins.
**Who runs it**: The Architect agent or a human reviewer with architecture knowledge.
**Inputs**: PRD, architecture document, tech stack, story files, project-context.md.
**Output**: Gate report with per-step PASS/WARN/FAIL and an overall verdict.

**Overall verdict rules**:
- **PASS** — All 13 steps are PASS or WARN (no more than 3 WARNs). Proceed to implementation.
- **CONDITIONAL PASS** — 4-6 WARNs with zero FAILs. Proceed with documented remediation plan.
- **FAIL** — Any step is FAIL. Return to the relevant phase for correction.

## Scoring Rules

Each step produces one of three ratings:

| Rating | Meaning | Allows Proceeding? |
|--------|---------|-------------------|
| PASS | Fully meets criteria with evidence | Yes |
| WARN | Partially meets criteria; gap is minor and documented | Yes (with limit) |
| FAIL | Missing, inconsistent, or critically incomplete | No |

**Weighted scoring**: Steps 1, 2, 8, and 10 are critical — a WARN on any critical step counts as two WARNs toward the overall threshold. A FAIL on any step is an immediate overall FAIL regardless of other scores.

---

## The 13 Steps

### Step 1: PRD Completeness

**What is checked**: The Product Requirements Document contains all required sections with sufficient detail for downstream agents to operate without guessing.

**How to check it**:
- Verify against the PRD schema (see `schemas.md`): problem statement, goals, user personas, functional requirements, non-functional requirements, success metrics, scope boundaries.
- Confirm every functional requirement has at least one associated user story.
- Check that scope boundaries explicitly list what is OUT of scope.

**PASS criteria**: All required sections present. Every functional requirement is traceable to at least one story. Success metrics are quantifiable.

**WARN criteria**: All sections present but one or two functional requirements lack story traceability, or success metrics exist but are qualitative rather than quantitative.

**FAIL criteria**: Missing sections (especially problem statement or functional requirements). More than 30% of functional requirements have no story traceability. No success metrics defined.

**Example evidence**: "PRD contains 12 functional requirements. 12/12 traced to stories (FR-001 -> S-001, FR-002 -> S-003, ...). Success metric: 'Reduce checkout time from 4.2s to under 2s.' Out-of-scope section explicitly excludes payment provider migration."

**Common failures**: Vague problem statements ("improve the user experience"), missing out-of-scope section leading to scope creep, success metrics that cannot be measured ("users should feel satisfied").

---

### Step 2: Architecture Alignment

**What is checked**: The architecture document is consistent with the PRD and the chosen tech stack. Component boundaries match the functional requirements. There are no orphan components (described but unused) or phantom dependencies (used but undescribed).

**How to check it**:
- Cross-reference each PRD functional requirement to at least one architecture component.
- Verify the tech stack document matches what the architecture describes.
- Check that all inter-component communication paths are documented.

**PASS criteria**: Every PRD requirement maps to an architecture component. Tech stack versions match. All communication paths documented.

**WARN criteria**: One or two requirements map ambiguously to components, or a minor version discrepancy exists in the tech stack.

**FAIL criteria**: Architecture contradicts the PRD (e.g., PRD says real-time but architecture shows batch-only). Orphan components found. Major tech stack inconsistency.

**Example evidence**: "Architecture defines 5 services. FR-001 through FR-012 each map to at least one service. Communication: API Gateway -> Auth Service (REST), Auth Service -> User DB (TCP/5432). Tech stack: Node 20.x matches both architecture and package.json."

**Common failures**: Architecture written for a different version of the PRD. Tech stack says PostgreSQL but architecture diagrams show MongoDB. Microservices defined but no service mesh or API gateway described.

---

### Step 3: Story Decomposition

**What is checked**: Stories are properly sized, follow the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable), and collectively cover all PRD requirements.

**How to check it**:
- Review each story for INVEST compliance.
- Check that no single story spans more than one sprint (or is expected to exceed 3 days of AI-assisted work).
- Verify story dependencies form a DAG (directed acyclic graph) with no circular dependencies.

**PASS criteria**: All stories meet INVEST. No story exceeds estimated 3-day scope. Dependency graph is acyclic. Coverage is complete — every PRD requirement has at least one story.

**WARN criteria**: 1-2 stories are slightly oversized but have clear sub-task breakdowns. One dependency is ambiguous but resolvable.

**FAIL criteria**: Stories are epics in disguise (multi-week scope). Circular dependencies exist. PRD requirements are missing from the story set.

**Example evidence**: "14 stories created. Largest is S-007 (estimated 2.5 days). Dependency graph: S-001 -> S-003 -> S-007 (no cycles). Coverage: all 12 FRs mapped."

**Common failures**: "Implement the backend" as a single story. Stories that depend on each other circularly. Stories that duplicate effort across different agents.

---

### Step 4: Acceptance Criteria Quality

**What is checked**: Every story has acceptance criteria written in Given/When/Then or equivalent testable format. Criteria are specific enough that a test can be written directly from them.

**How to check it**:
- Read each acceptance criterion. Can you write a test from it without asking clarifying questions?
- Check for edge cases: are error states, empty states, and boundary conditions covered?
- Verify criteria do not duplicate across stories without reason.

**PASS criteria**: All stories have testable acceptance criteria. Edge cases documented. No ambiguous language ("should work well", "fast enough").

**WARN criteria**: Most criteria are testable but 1-2 stories use slightly ambiguous language that can be reasonably interpreted.

**FAIL criteria**: Stories lack acceptance criteria entirely. Criteria use subjective language without thresholds. No edge cases considered.

**Example evidence**: "S-003 AC: Given a user with valid JWT, When they request GET /api/orders, Then they receive a 200 response with an array of their orders (max 50 per page). Given an expired JWT, When they request GET /api/orders, Then they receive 401 with error code AUTH_EXPIRED."

**Common failures**: "The page loads quickly" (no threshold). Missing error-state criteria. Acceptance criteria that test implementation details rather than behavior.

---

### Step 5: Dependency Mapping

**What is checked**: All external dependencies (third-party services, APIs, libraries, infrastructure) and internal dependencies (between stories, between components) are identified, versioned, and have fallback plans.

**How to check it**:
- List all `import` / dependency declarations from the tech stack and architecture.
- For each external service, verify: is it available? Is there a sandbox/staging environment? What happens if it is down?
- For internal dependencies, confirm the execution order is achievable.

**PASS criteria**: All dependencies listed with versions. External services have sandbox access confirmed. Fallback behavior documented for critical external dependencies.

**WARN criteria**: Dependencies listed but one or two lack confirmed sandbox access. Fallback behavior described at high level but not in acceptance criteria.

**FAIL criteria**: Dependencies not cataloged. External service availability unknown. No fallback consideration for critical paths.

**Example evidence**: "External: Stripe API v2023-10-16 (sandbox key confirmed), SendGrid v3 (test mode verified). Internal: S-001 (auth) must complete before S-003 (orders). Fallback: if Stripe is down, queue payment and retry with exponential backoff."

**Common failures**: Assuming third-party APIs are always available. Not pinning dependency versions. Discovering a needed API requires an enterprise contract mid-sprint.

---

### Step 6: Risk Register

**What is checked**: A risk register exists that identifies at least the top 5 project risks with likelihood, impact, and mitigation strategies.

**How to check it**:
- Verify the register uses a standard format: Risk ID, Description, Likelihood (H/M/L), Impact (H/M/L), Mitigation, Owner.
- Check that technical risks (scalability, third-party outage), process risks (scope creep, key person dependency), and timeline risks are all represented.
- Confirm mitigations are actionable, not aspirational.

**PASS criteria**: 5+ risks identified across technical, process, and timeline categories. Each has an actionable mitigation. Owners assigned.

**WARN criteria**: Risks identified but mitigations are vague ("we will monitor") for 1-2 entries. Fewer than 5 risks but major categories covered.

**FAIL criteria**: No risk register. Risks identified but zero mitigations. Only one category of risk considered.

**Example evidence**: "R-001: Stripe API rate limits may throttle during peak checkout. Likelihood: M. Impact: H. Mitigation: implement request queuing with circuit breaker. Owner: Backend Lead."

**Common failures**: Listing only positive risks ("might launch early"). Mitigations that are just restated risks ("we will handle it"). No owner assigned.

---

### Step 7: NFR Coverage

**What is checked**: Non-functional requirements (performance, scalability, accessibility, i18n, observability) are explicitly stated with measurable targets.

**How to check it**:
- Review the PRD NFR section and architecture constraints.
- For each NFR, verify a numeric or verifiable target exists.
- Confirm NFRs are reflected in at least one story's acceptance criteria or a dedicated NFR story.

**PASS criteria**: NFRs exist for performance, scalability, and at least two other categories. All have measurable targets. Reflected in stories.

**WARN criteria**: NFRs exist but one category lacks a measurable target. NFRs documented but not yet reflected in story acceptance criteria.

**FAIL criteria**: No NFR section. NFRs are aspirational ("should be fast") with no thresholds.

**Example evidence**: "Performance: API p95 latency < 200ms. Scalability: support 10K concurrent users. Accessibility: WCAG 2.1 AA. Observability: all services emit structured logs to centralized collector."

**Common failures**: Conflating NFRs with functional requirements. Setting unrealistic targets without benchmarking. Forgetting observability and operability NFRs.

---

### Step 8: API Contracts

**What is checked**: All API endpoints are defined with request/response schemas, status codes, authentication requirements, and versioning strategy.

**How to check it**:
- Review the API contract document or OpenAPI spec.
- Verify every endpoint referenced in stories has a contract.
- Check that error responses are standardized (consistent error object shape).

**PASS criteria**: All endpoints documented with schemas. Error format standardized. Auth requirements per endpoint. Versioning strategy stated.

**WARN criteria**: Core endpoints documented but 1-2 secondary endpoints lack full schema. Error format mostly consistent.

**FAIL criteria**: No API contracts exist. Stories reference endpoints that are not defined. No error standardization.

**Example evidence**: "POST /api/auth/login — Request: {email: string, password: string}. Response 200: {token: string, expiresIn: number}. Response 401: {error: {code: 'INVALID_CREDENTIALS', message: string}}. Auth: none (public). Version: /api/v1/."

**Common failures**: Defining only happy-path responses. Inconsistent naming conventions across endpoints. No pagination contract for list endpoints.

---

### Step 9: Data Model

**What is checked**: The data model (ERD or equivalent) is defined, normalized appropriately, and consistent with the API contracts and PRD.

**How to check it**:
- Review the data model document against the PRD entities.
- Verify every API response field traces to a data model field.
- Check for indexing strategy on frequently-queried fields.
- Confirm relationships (1:1, 1:N, M:N) are explicit.

**PASS criteria**: All PRD entities modeled. Relationships explicit. Index strategy documented. API fields trace to model fields.

**WARN criteria**: Model complete but index strategy is "to be determined during implementation." One or two API fields lack clear model mapping.

**FAIL criteria**: No data model. Model contradicts API contracts (e.g., API returns `userName` but model has no such field). Relationships ambiguous.

**Example evidence**: "Entities: User, Order, Product, OrderItem. User 1:N Order. Order 1:N OrderItem. OrderItem N:1 Product. Indexes: User.email (unique), Order.userId, Order.createdAt (descending)."

**Common failures**: No consideration of soft deletes vs hard deletes. Missing audit fields (createdAt, updatedAt). Data model designed for one database but tech stack specifies another.

---

### Step 10: Security Review

**What is checked**: Authentication, authorization, input validation, and data protection strategies are defined and consistent across all artifacts.

**How to check it**:
- Verify auth strategy (JWT, session, OAuth) is documented with token lifecycle.
- Check authorization model (RBAC, ABAC) with role definitions.
- Confirm input validation rules exist for all user-facing endpoints.
- Review data-at-rest and data-in-transit encryption strategy.

**PASS criteria**: Auth and authz documented. Input validation rules defined. Encryption strategy stated. OWASP top 10 addressed.

**WARN criteria**: Core auth documented but one area (e.g., CSRF protection) is mentioned without implementation detail.

**FAIL criteria**: No security section. Auth strategy undefined. No input validation mentioned.

**Example evidence**: "Auth: JWT with RS256, 15-min access token, 7-day refresh token. Authz: RBAC with roles [admin, member, viewer]. Input: zod schemas on all request bodies. Encryption: TLS 1.3 in transit, AES-256 at rest. CSRF: double-submit cookie pattern."

**Common failures**: Storing JWTs in localStorage without XSS mitigation. No rate limiting on auth endpoints. Assuming the framework handles everything.

---

### Step 11: Performance Targets

**What is checked**: Specific, measurable performance targets exist and are tied to testing strategy.

**How to check it**:
- Review performance targets from NFRs and verify they have specific numbers.
- Check that a load testing approach is defined (tool, scenarios, thresholds).
- Verify targets are realistic given the architecture and infrastructure.

**PASS criteria**: Latency, throughput, and resource targets defined. Load test approach documented. Targets validated against architecture constraints.

**WARN criteria**: Targets exist but load testing approach is high-level ("will use k6"). Targets not yet validated against infrastructure limits.

**FAIL criteria**: No performance targets. Targets are aspirational without infrastructure backing. No testing strategy.

**Example evidence**: "p50 < 100ms, p95 < 200ms, p99 < 500ms for all API endpoints. Throughput: 1000 req/s sustained. Load testing: k6 scripts targeting staging, run in CI on every release candidate. Target infra: 2x t3.medium, validated to handle 1200 req/s in spike test."

**Common failures**: Setting targets without knowing current baseline. No distinction between p50 and p99. Testing only happy paths under load.

---

### Step 12: Deployment Strategy

**What is checked**: A deployment strategy is defined covering environments, CI/CD pipeline, feature flags, and release process.

**How to check it**:
- Verify environment definitions (dev, staging, production) with their purposes.
- Check CI/CD pipeline stages are documented.
- Confirm feature flag strategy if incremental rollout is planned.
- Review database migration strategy.

**PASS criteria**: Environments defined. CI/CD pipeline documented. Migration strategy for schema changes. Release process documented.

**WARN criteria**: Environments and CI/CD defined but feature flag strategy is "optional." Migration approach mentioned but no tooling selected.

**FAIL criteria**: No deployment strategy. CI/CD not considered. No migration plan for data model changes.

**Example evidence**: "Environments: dev (auto-deploy on push), staging (deploy on PR merge to main), production (manual promotion from staging). CI: lint -> test -> build -> deploy. Migrations: Prisma migrate with review step before production. Feature flags: LaunchDarkly for gradual rollout of new checkout flow."

**Common failures**: No staging environment. Database migrations applied directly to production. No distinction between deploy and release.

---

### Step 13: Rollback Plan

**What is checked**: A rollback strategy exists for both application code and data migrations, with clear triggers and procedures.

**How to check it**:
- Verify rollback triggers are defined (error rate threshold, latency spike, manual decision).
- Check that application rollback procedure is documented (revert to previous container image, feature flag toggle).
- Confirm data migration rollback is addressed (backward-compatible migrations, or explicit down-migration scripts).
- Verify rollback has been tested or is testable.

**PASS criteria**: Triggers defined. Application rollback procedure documented. Data rollback addressed. Communication plan for stakeholders during rollback.

**WARN criteria**: Application rollback documented but data migration rollback is "case-by-case." No formal communication plan.

**FAIL criteria**: No rollback plan. Destructive migrations with no reversal path. No triggers defined.

**Example evidence**: "Trigger: error rate > 5% for 2 minutes OR p95 latency > 1s for 5 minutes. Application rollback: revert ECS task definition to previous revision (< 2 min). Data rollback: all migrations are backward-compatible; down migrations tested in staging. Communication: PagerDuty alert -> Slack #incidents -> status page update."

**Common failures**: Assuming rollback means "just redeploy the old version" without considering database changes. No rollback testing. No defined authority for initiating rollback.

---

## Remediation Guidance

When a step receives WARN or FAIL:

1. **Identify the gap** — The gate report specifies exactly what is missing.
2. **Route to the correct phase** — PRD issues go back to Phase 1 (PM agent). Architecture issues go to Phase 2 (Architect agent). Story issues go to Phase 3 (PM agent).
3. **Fix and re-submit** — The responsible agent or human fixes the artifact and updates it in Git.
4. **Partial re-evaluation** — Only the failed/warned steps need re-evaluation, not the full 13-step gate.

**Remediation SLA**: WARN items should be resolved within the same sprint. FAIL items block all implementation until resolved.

## Re-Evaluation Process

1. The fixer commits the corrected artifact to Git with a message referencing the gate step (e.g., "fix(gate): add rollback triggers for step 13").
2. The Architect agent re-runs only the affected steps.
3. If all steps now PASS or meet the WARN threshold, the gate opens.
4. The gate report is updated in-place with a re-evaluation timestamp and the new scores.
5. All gate reports are retained in version control for audit purposes.

**Maximum re-evaluations**: 3 per gate cycle. If the gate fails 3 times, escalate to a human architecture review session before further attempts.

### Gate Metrics History

**[R24]** Track these metrics across gate evaluations to identify systemic issues:

| Metric | What It Reveals | Action Threshold |
|--------|----------------|-----------------|
| First-pass rate | Quality of Phase 3 output | <70% first-pass rate over 5 gates -> review Phase 3 workflows |
| Most-failed step | Systemic gap in the team's process | Same step fails 3+ times -> create a team training story |
| Average remediation time | How quickly gaps are fixed | >3 days average -> review remediation routing |
| Override frequency | Whether gates are being circumvented | >20% of gates include overrides -> review gate criteria relevance |

---

## Assumptions

- All upstream artifacts (PRD, architecture, stories, project-context.md) are committed to Git before the gate runs
- The gate evaluator (architect agent or human) has read access to all project artifacts
- Gate evaluation is time-boxed to 2 hours for the full 13-step gate, 1 hour for the MVP partial gate

## Limits

- The gate validates artifact completeness and consistency — it does NOT validate technical correctness of the architecture
- The gate does NOT guarantee that implementation will succeed — it guarantees that implementation has the information it needs to begin
- The gate does NOT replace code review, testing, or security audits during Phase 4

## Edge Cases

- **Gate step does not apply to the project**: Replace the step with a domain-equivalent (e.g., Step 8 API Contracts -> CLI Interface Contract for CLI tools). Document the substitution in the gate report. See `references/customization-guide.md`.
- **Gate passes but a critical issue is discovered in Phase 4**: Do not retroactively fail the gate. Instead, document the gap, create a remediation story, and add the check to the gate for future evaluations.
- **Brownfield project where historical artifacts do not exist**: Run the gate against whatever artifacts exist. Mark missing artifacts as WARN (not FAIL) if the team has compensating knowledge. Create stories to backfill the gaps.

## Acceptance Criteria

- [ ] Gate report exists with per-step PASS/WARN/FAIL ratings
- [ ] Overall verdict is documented (PASS, CONDITIONAL PASS, or FAIL)
- [ ] Any overrides follow the override procedure with audit trail
- [ ] Gate metrics history is updated after each evaluation
- [ ] All FAIL items are remediated before Phase 4 begins

See also: `references/phase-3-solutioning.md`, `references/phase-4-implementation.md`, `references/artifact-flow-chain.md`, `references/customization-guide.md`
