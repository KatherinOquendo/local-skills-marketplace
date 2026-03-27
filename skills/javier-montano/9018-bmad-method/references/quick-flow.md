# Quick Flow — Barry Agent Guide

## Table of Contents
- [What is Quick Flow](#what-is-quick-flow)
- [Triage Criteria](#triage-criteria)
- [Quick Flow vs Full BMAD Decision Matrix](#quick-flow-vs-full-bmad-decision-matrix)
- [Rapid Spec Format](#rapid-spec-format)
- [Abbreviated Implementation Workflow](#abbreviated-implementation-workflow)
- [Self-Review Checklist](#self-review-checklist)
- [When to Escalate to Full Flow](#when-to-escalate-to-full-flow)
- [Examples](#examples)

---

## What is Quick Flow

Quick Flow is the fast lane for small, well-understood changes that do not justify the full 4-phase BMAD process. It is managed by the Barry agent — a generalist who handles triage, rapid spec writing, implementation, and self-review in a single pass.

**Key principle**: Quick Flow is not a shortcut that skips quality. It compresses the 4 phases into a single streamlined workflow where each phase is performed but at reduced depth.

**When properly used, Quick Flow**:
- Delivers fixes and small features in minutes instead of hours
- Maintains traceability (every change still links to a rationale)
- Avoids bureaucratic overhead for trivial changes
- Preserves the option to escalate at any point

---

## Triage Criteria

Barry performs a scope check on every incoming request before deciding the flow path. The triage evaluates five dimensions:

### Scope Check Matrix

| Dimension | Quick Flow Threshold | Full BMAD Threshold |
|-----------|---------------------|---------------------|
| **Estimated size** | 1-3 story points | 5+ story points |
| **Files affected** | 1-3 files | 4+ files |
| **New domain concepts** | None | Introduces new entities or patterns |
| **Architecture impact** | None — works within existing patterns | Changes system boundaries or introduces new components |
| **Risk level** | Low — easily reversible | Medium/High — affects data, security, or external systems |

### Quick Decision Tree

```
Is the request a bug fix or minor enhancement?
├── YES → Does it touch more than 3 files?
│         ├── YES → Full BMAD (start Phase 2 or 3)
│         └── NO → Does it introduce new domain concepts?
│                   ├── YES → Full BMAD (start Phase 1)
│                   └── NO → QUICK FLOW
└── NO → Is it a new feature?
          ├── YES → Full BMAD (start Phase 1)
          └── Is it a refactor or chore?
                ├── Isolated refactor (1-3 files) → QUICK FLOW
                └── Cross-cutting refactor → Full BMAD (start Phase 3)
```

---

## Quick Flow vs Full BMAD Decision Matrix

| Scenario | Flow | Rationale |
|----------|------|-----------|
| Fix typo in error message | Quick Flow | 1 file, zero risk, 1 point |
| Add input validation to existing form | Quick Flow | 1-2 files, follows existing patterns, 2 points |
| Add new API endpoint for existing resource | Quick Flow | 2-3 files (route, controller, test), clear pattern, 3 points |
| Add user authentication system | Full BMAD | Multiple files, new domain concept, security implications |
| Build search functionality | Full BMAD | New feature requiring architecture decisions |
| Update dependency version | Quick Flow | 1 file (package.json), low risk if tests pass |
| Migrate database schema | Full BMAD | Data integrity risk, may require ADR |
| Fix CSS layout bug | Quick Flow | 1 file, visual-only change, easily verified |
| Add payment processing | Full BMAD | High risk, regulatory implications, new external integration |
| Rename a variable across codebase | Quick Flow | Mechanical change, tooling-assisted, easily reversible |
| Add real-time notifications | Full BMAD | New infrastructure (WebSockets), architecture decision needed |

---

## Rapid Spec Format

Quick Flow does not produce a full PRD. Instead, Barry writes a rapid spec — a compressed artifact that captures the essential information in a single block.

### Rapid Spec Template

```markdown
# Rapid Spec: [Short Title]

**Request**: [One sentence describing what needs to happen]
**Rationale**: [Why this change is needed]
**Scope**: [Files/components affected]
**Approach**: [How it will be implemented — 2-3 sentences max]
**Acceptance**: [How to verify it works — 1-3 criteria]
**Risk**: Low | Medium (if medium, consider escalation)
**Traceability**: [FR-ID if applicable, or "ad-hoc fix"]
```

### Rapid Spec Example

```markdown
# Rapid Spec: Fix email validation regex

**Request**: The registration form accepts emails without a TLD (e.g., "user@domain").
**Rationale**: Users are registering with invalid emails, causing bounce-backs.
**Scope**: `src/auth/validators.ts`, `src/auth/validators.test.ts`
**Approach**: Update the email regex to require at least one dot after the @ symbol.
  Add test cases for edge cases (subdomains, plus addressing, unicode domains).
**Acceptance**:
  - "user@domain" is rejected
  - "user@domain.com" is accepted
  - "user+tag@sub.domain.co.uk" is accepted
**Risk**: Low — isolated change with comprehensive test coverage.
**Traceability**: FR-AUTH-002
```

---

## Abbreviated Implementation Workflow

Quick Flow compresses the 4 phases into 6 steps:

### Step 1 — Triage (Phase 1 compressed)
- Read the request
- Run the scope check matrix
- Decide: Quick Flow or escalate

### Step 2 — Rapid Spec (Phase 2 compressed)
- Write the rapid spec (see template above)
- Confirm acceptance criteria are clear

### Step 3 — Plan (Phase 3 compressed)
- Identify the files to change
- Determine the approach (no architecture doc needed)
- Check for obvious dependencies

### Step 4 — Implement (Phase 4)
- Create a feature branch
- Write or update tests first (TDD applies even in Quick Flow)
- Make the code change
- Run the test suite

### Step 5 — Self-Review
- Run the self-review checklist (see below)
- Fix any issues found

### Step 6 — Complete
- Commit with a message referencing the rapid spec
- Update story status if applicable
- Merge (or open PR for human review)

---

## Self-Review Checklist

Since Quick Flow often bypasses peer review, Barry performs a structured self-review before marking the work as complete.

### Checklist

```markdown
## Quick Flow Self-Review

### Correctness
- [ ] All acceptance criteria from the rapid spec are met
- [ ] Edge cases are handled (null, empty, boundary values)
- [ ] Error messages are clear and actionable

### Tests
- [ ] New or modified tests exist for every changed behavior
- [ ] Tests pass locally
- [ ] No existing tests broken by the change

### Conventions
- [ ] Code follows project-context.md conventions
- [ ] No linting errors or warnings
- [ ] File naming follows project patterns

### Safety
- [ ] No hardcoded secrets or credentials
- [ ] No new dependencies added (or if added, they are justified)
- [ ] No security regressions (input validation, auth checks intact)

### Scope
- [ ] Change is contained to the files listed in the rapid spec
- [ ] No unrelated changes included ("while I'm here" changes)
- [ ] If scope expanded during implementation, reassess Quick Flow eligibility
```

### Failing the Self-Review

If any checkbox cannot be checked:
- Fix the issue if it is straightforward
- If the fix would expand scope beyond Quick Flow thresholds, escalate to Full BMAD
- Never skip a checkbox — document why it does not apply if genuinely irrelevant

---

## When to Escalate to Full Flow

Quick Flow can be abandoned at any point. Escalation signals:

### During Triage
- The request is vague and cannot be scoped without research
- Multiple stakeholders have different expectations
- The request involves a domain you do not understand

### During Rapid Spec
- You cannot write clear acceptance criteria
- The approach requires decisions that should be ADRs
- The risk assessment lands at "Medium" or higher

### During Implementation
- More than 3 files need changes
- You discover the change requires a database migration
- Existing tests reveal the change has unexpected side effects
- The implementation takes longer than 2 hours (sign of underestimated complexity)

### Escalation Decision Tree

```
Is the issue blocking Quick Flow completion?
├── NO → Continue Quick Flow, document the concern for future work
└── YES → What type of blocker?
          ├── Scope expanded (>3 files or >3 points) → Escalate to Phase 3
          ├── New domain concept discovered → Escalate to Phase 1
          ├── Architecture decision needed → Escalate to Phase 3
          ├── Security concern identified → Escalate to Phase 3 (gate step 10)
          └── Ambiguous requirements → Escalate to Phase 2
```

### Escalation Protocol

1. Stop Quick Flow work (do not discard it)
2. Document what was discovered during the attempt
3. Convert the rapid spec into a starting point for the appropriate BMAD phase
4. Hand off to the relevant agent (PM for Phase 2, Architect for Phase 3)

The rapid spec is not wasted — it becomes input to the full process.

### Maximum Quick Flow Chain Rule

**[R10]** Do not execute more than 3 consecutive Quick Flows without consolidating. When the 4th Quick Flow request arrives for the same feature area:

1. Stop and review the last 3 Quick Flow changes together
2. Assess whether these changes constitute a feature that deserves a proper story
3. If yes: write a retroactive story consolidating the 3 Quick Flows and proceed with any remaining work as a Phase 3-4 flow
4. If no (truly independent fixes): proceed, but flag the pattern in the next retrospective

**Why**: Sequential Quick Flows in the same area indicate emerging complexity that Quick Flow was not designed to handle. Consolidation prevents architectural drift and maintains traceability.

---

## Examples

### Example 1: Quick Flow — Fix broken link

```
Request: "The 'Documentation' link in the footer goes to a 404 page."

Triage: 1 file (footer component), no domain concepts, zero risk → Quick Flow

Rapid Spec:
  Request: Fix broken documentation link in footer
  Scope: src/components/Footer.tsx
  Approach: Update href from "/docs" to "/documentation" (URL changed in last deploy)
  Acceptance: Footer link navigates to the documentation page
  Risk: Low

Implementation: 1-line change, 1 test update, self-review passes.
Total time: 5 minutes.
```

### Example 2: Quick Flow — Add loading spinner

```
Request: "The dashboard takes 3 seconds to load but shows no feedback."

Triage: 2 files (dashboard component + CSS), existing pattern (spinner used elsewhere),
  2 points → Quick Flow

Rapid Spec:
  Request: Add loading spinner to dashboard while data fetches
  Scope: src/pages/Dashboard.tsx, src/styles/dashboard.css
  Approach: Use existing Spinner component, show during fetch, hide on completion
  Acceptance: Spinner shows immediately on page load, disappears when data renders
  Risk: Low

Implementation: Import spinner, add conditional render, add CSS, update test.
Total time: 15 minutes.
```

### Example 3: Escalation — Add export feature

```
Request: "Users should be able to export their data as CSV."

Triage: New feature, multiple files (UI button, export logic, API endpoint, tests),
  introduces file generation concept, 5+ points → Full BMAD

Decision: Escalate to Phase 2. PM writes requirements for export feature
  (what data, what format, access controls, file size limits).
```

### Example 4: Escalation mid-implementation

```
Request: "Fix the search results sorting — it should sort by relevance, not alphabetical."

Triage: Sounds like 1 file change, 2 points → Quick Flow

During implementation: Discovered that "relevance" requires a scoring algorithm
  that does not exist. The current search is a simple LIKE query.
  Adding relevance scoring requires database changes (full-text search index),
  a new scoring service, and updates to the API response format.

Decision: Escalate to Phase 3. Architect designs the search architecture.
  The rapid spec becomes input for the architecture discussion.
```

---

## Assumptions

- The developer (or Barry agent) has access to the existing codebase and can assess scope accurately
- project-context.md exists and is current (conventions, exclusion zones are known)
- The change fits within existing architectural patterns — no new components or services needed

## Limits

- Quick Flow does NOT produce PRDs, architecture documents, or formal gate reports
- Quick Flow must NOT be used for security-sensitive changes (authentication, authorization, encryption)
- Quick Flow does NOT apply to database schema migrations — those always require a story

## Edge Cases

- **Quick Flow fix introduces a regression**: Revert immediately. Write a proper story with comprehensive acceptance criteria including the regression scenario. Do not attempt a second Quick Flow for the same area.
- **Quick Flow request is ambiguous**: If you cannot write clear acceptance criteria in 2 minutes, it is not a Quick Flow candidate. Escalate.
- **Quick Flow touches a file in an exclusion zone**: Abort Quick Flow. Exclusion zones override Quick Flow eligibility regardless of scope.

## Trade-offs

| Option | Pro | Con | Winner |
|--------|-----|-----|--------|
| Always use Quick Flow for <3 files | Faster delivery | Risk of accumulated drift | Conditional: use only when 3 consecutive chain limit is not reached |
| Always use Full BMAD | Better traceability | Overhead for trivial changes | For changes >3 story points or >3 files |

## Acceptance Criteria

- [ ] Rapid spec exists before implementation begins (even for Quick Flow)
- [ ] Self-review checklist passes with all boxes checked
- [ ] Change is contained to files listed in the rapid spec
- [ ] No more than 3 consecutive Quick Flows in the same feature area without consolidation

See also: `references/methodology-overview.md`, `references/phase-4-implementation.md`, `references/brownfield-patterns.md`
