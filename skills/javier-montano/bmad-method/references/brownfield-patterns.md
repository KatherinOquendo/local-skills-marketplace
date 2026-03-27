# Brownfield Patterns — Applying BMAD to Existing Codebases

## Table of Contents
- [When to Use This Guide](#when-to-use-this-guide)
- [Initial Assessment](#initial-assessment)
- [Generating project-context.md from Existing Code](#generating-project-contextmd-from-existing-code)
- [Incremental Adoption Strategy](#incremental-adoption-strategy)
- [Coexistence with Existing Processes](#coexistence-with-existing-processes)
- [Legacy Inventory](#legacy-inventory)
- [Dealing with Undocumented Architecture](#dealing-with-undocumented-architecture)
- [Creating Retroactive PRDs](#creating-retroactive-prds)
- [Migration from Ad-Hoc to BMAD](#migration-from-ad-hoc-to-bmad)
- [Common Pitfalls](#common-pitfalls)

---

## When to Use This Guide

Use this guide when you are introducing BMAD into a project that already has:
- An existing codebase (any size, any language)
- Established development workflows (even informal ones)
- Production users relying on current functionality
- Technical debt that makes changes risky
- Team members who have been working without BMAD

You do NOT need to stop development to adopt BMAD. The brownfield approach is specifically designed for live projects where disruption must be minimized.

### Risk Scoring for Legacy Adoption

**[R28]** Before committing to BMAD adoption, score the project's readiness:

| Factor | Score 0 (High Risk) | Score 1 (Medium) | Score 2 (Low Risk) |
|--------|-------------------|------------------|-------------------|
| Test coverage | <20% | 20-60% | >60% |
| Documentation exists | None | README + sparse comments | API docs + architecture notes |
| CI/CD pipeline | None | Basic (lint + test) | Full pipeline with staging |
| Team openness to process change | Resistant | Neutral | Enthusiastic |
| Codebase age | >5 years, no refactoring | 2-5 years | <2 years or recently modernized |
| Dependency freshness | >50% outdated | 20-50% outdated | <20% outdated |

**Total score interpretation**:
- **0-4**: High risk. Start with Level 1 only (stories). Do not attempt full BMAD adoption.
- **5-8**: Medium risk. Start with Level 1-2. Plan Level 3 after 2 successful sprints.
- **9-12**: Low risk. Can attempt Level 2-3 immediately.

### Minimum Documentation Threshold Before Starting BMAD

**[R29]** Before beginning ANY BMAD work on a brownfield project, these must exist:

- [ ] project-context.md (generated or manual — even a draft is sufficient)
- [ ] A list of exclusion zones (files/directories AI must not touch)
- [ ] At least a Level 1 architecture inventory (component names and one-line descriptions)

Without these three items, AI agents operating on the codebase risk violating unknown constraints or modifying protected files.

## Initial Assessment

Before adopting BMAD for an existing project, run the "Document Existing Project" assessment to understand what you have.

### Step 1: Code Inventory

Run a structural audit of the codebase:

```
Questions to answer:
- What languages and frameworks are in use?
- What is the directory structure pattern? (monorepo, polyrepo, monolith)
- How many distinct services/modules exist?
- What is the test coverage percentage?
- What CI/CD exists?
- How are dependencies managed?
```

### Step 2: Documentation Audit

Catalog what documentation exists:

| Document Type | Exists? | Current? | Location |
|--------------|---------|----------|----------|
| README | | | |
| API docs (OpenAPI/Swagger) | | | |
| Architecture diagrams | | | |
| Database schema docs | | | |
| Deployment runbooks | | | |
| Onboarding guide | | | |
| Decision log / ADRs | | | |

Mark each as "Yes/Current", "Yes/Stale", or "No". This inventory determines how much retroactive documentation work is needed.

### Step 3: Process Audit

Document the current development workflow:

```
Questions to answer:
- How does work get planned? (Jira tickets, GitHub issues, verbal)
- How does code get reviewed? (PR reviews, pair programming, none)
- How does code get deployed? (CI/CD, manual, scripts)
- How are decisions made? (meetings, Slack, one person decides)
- What ceremonies exist? (standups, demos, retros)
```

### Step 4: Risk Assessment

Identify the highest-risk areas for introducing process change:

- What parts of the codebase are most fragile?
- Where would a regression have the most impact?
- Who on the team is most/least open to process change?
- What is the current pain point that motivates BMAD adoption?

## Generating project-context.md from Existing Code

For brownfield projects, project-context.md is generated retrospectively rather than built incrementally.

### Approach: AI-Assisted Reverse Documentation

Use the BMAD Document Existing Project workflow to generate a draft:

1. **Feed the AI the codebase structure** — directory tree, package.json/Cargo.toml/go.mod, Docker files.
2. **Feed sample source files** — entry points, route definitions, database models.
3. **Feed existing docs** — READMEs, API specs, any architecture notes.
4. **Ask the AI to generate** a project-context.md following the BMAD template.

### Template for Brownfield project-context.md

```markdown
# Project Context — [Project Name]

## Overview
[One paragraph: what the project does, who uses it, how long it has existed]

## Current State
- **Phase**: Brownfield adoption — existing production system
- **Codebase age**: [X years/months]
- **Team size**: [N developers]
- **Tech stack**: [language, framework, database, infrastructure]

## Architecture Summary
[Component list with one-line descriptions, derived from code audit]
- **Component A**: [description]
- **Component B**: [description]

## Key Decisions (Historical)
[Decisions inferred from code and any existing ADRs]
1. [Decision] — [Rationale if known, "rationale unknown" if not]

## Technical Debt Register
[Top 5 known debt items with severity]
1. [Debt item] — Severity: [H/M/L]

## BMAD Adoption Scope
[What is being brought under BMAD management — start small]
- Feature X (new development) — Full BMAD flow
- Module Y (maintenance) — BMAD stories only (Phase 3-4)

## Artifact Links
- PRD: [link or "to be created"]
- Architecture: [link or "derived from code audit"]
- Stories: [link or "to be created"]
```

### Validation

After generating, validate against the actual codebase:
- Does every listed component actually exist in code?
- Are the tech stack versions accurate (check lock files)?
- Are there components in code that are NOT listed?

## Incremental Adoption Strategy

The core principle of brownfield BMAD adoption: **start with Phase 3-4 for new features, then retroactively build Phase 1-2 artifacts as needed.**

### Level 1: Stories Only (Minimum Viable BMAD)

Adopt BMAD stories for new feature work:
- Write stories with acceptance criteria before coding
- Use the BMAD story template
- Run acceptance criteria verification after implementation
- Keep stories in Git alongside code

This requires zero retroactive documentation. It immediately improves new development quality.

**Time investment**: 15-30 minutes per feature for story writing.

### Level 2: Stories + Architecture Sections

When stories touch shared components, document those components:
- Write architecture sections for components involved in current work
- Keep a running architecture document that grows organically
- Each new story adds documentation for the components it touches

**Time investment**: 30-60 minutes per feature, declining as architecture doc fills in.

### Level 3: Retroactive PRD + Full Flow for Major Features

For significant new features (multi-sprint), run the full BMAD flow:
- Write a PRD (scoped to the feature, not the entire product)
- Validate against existing architecture
- Run the implementation readiness gate
- Implement through BMAD Phase 4

**Time investment**: 2-4 hours upfront, saves 10-20 hours in reduced rework.

### Level 4: Full BMAD Coverage

Once the team is comfortable, retroactively create:
- A product-level PRD covering existing functionality
- A complete architecture document
- A decision log extracted from Git history and team memory

This is a project in itself and should be treated as such — with its own stories and timeline.

## Coexistence with Existing Processes

BMAD does not require abandoning existing tools or ceremonies. It layers on top.

### With Jira/Linear/GitHub Issues

- BMAD stories are the source of truth; Jira tickets reference them.
- Story IDs map to ticket IDs (e.g., S-007 corresponds to PROJ-142).
- Acceptance criteria live in the BMAD story file. The Jira ticket links to it.
- Status tracking stays in Jira. BMAD artifacts stay in Git.

### With Existing PR Reviews

- PR descriptions reference the BMAD story being implemented.
- Reviewers check code against story acceptance criteria.
- The story file can be updated in the same PR if implementation reveals needed changes.

### With Standups and Ceremonies

- Standups reference stories by ID.
- Sprint planning pulls from the BMAD story backlog.
- Demos verify acceptance criteria in front of stakeholders.
- Retrospectives can evaluate BMAD process effectiveness alongside delivery metrics.

### With Existing CI/CD

- BMAD does not modify CI/CD pipelines.
- Optionally, add a BMAD artifact validation step (schema checks on story files, architecture lint).
- Deployment strategy documentation can be generated from existing pipeline configs.

## Legacy Inventory

Before BMAD can manage a brownfield project, you need a legacy inventory — a catalog of what exists and its health.

### Inventory Template

For each module or service:

```markdown
## Module: [Name]

### Vital Signs
- Lines of code: [N]
- Test coverage: [N%]
- Last meaningful change: [date]
- Dependencies: [count, with N outdated]
- Known bugs: [count]

### Documentation Status
- README: [current/stale/missing]
- API docs: [current/stale/missing]
- Inline comments: [adequate/sparse/none]

### BMAD Readiness
- Can be described in a PRD section: [yes/no]
- Architecture is inferable from code: [yes/no]
- Has clear boundaries (inputs/outputs): [yes/no]
- Priority for BMAD adoption: [high/medium/low/skip]
```

### Prioritization

Adopt BMAD for modules in this order:
1. **Active development** — modules receiving new features now
2. **High-risk** — modules where bugs have the most impact
3. **Integration points** — modules that many other modules depend on
4. **Stable** — modules that rarely change (lowest priority, may never need full BMAD coverage)

## Dealing with Undocumented Architecture

Most brownfield projects have architecture that exists only in the code and the team's collective memory.

### Extraction Techniques

**From code structure**:
- Directory layout reveals component boundaries.
- Import/dependency graphs reveal relationships.
- Entry points (main files, route registrations) reveal the public surface.
- Configuration files reveal infrastructure assumptions.

**From Git history**:
- Files that change together likely belong to the same component.
- Commit messages reveal intent (especially well-written ones).
- Merge patterns reveal team boundaries and component ownership.

**From team interviews**:
- Ask: "Draw the system on a whiteboard." Photograph and transcribe.
- Ask: "What breaks when X goes down?" This reveals dependencies.
- Ask: "What would you rewrite first?" This reveals known architectural problems.

### Documentation Strategy

Document discovered architecture at the level appropriate for current needs:

1. **Level 1 — Component list**: Name and one-line description of each component. (30 minutes)
2. **Level 2 — Interaction diagram**: Arrows showing which components communicate. (1-2 hours)
3. **Level 3 — Full architecture doc**: Component details, data flows, infrastructure, security boundaries. (1-2 days)

Start at Level 1. Move to deeper levels only when BMAD work requires the detail.

## Creating Retroactive PRDs

Sometimes you need a PRD for a feature that already exists — to enable BMAD-managed enhancements or to establish a baseline for future work.

### The Reverse-Engineering Approach

1. **Start from the UI** — Screenshot every screen. Catalog every user action.
2. **Map to backend** — For each user action, trace the code path. Document the API call, business logic, and data access.
3. **Extract requirements** — Convert observed behavior into requirement statements: "The system SHALL allow users to filter orders by date range."
4. **Identify gaps** — Where does the current behavior differ from what users actually need? These gaps become new requirements.

### Retroactive PRD Template

```markdown
# PRD: [Feature Name] (Retroactive)

## Current State
[Description of what exists today]

## Problem Statement
[Why this feature was built — if known. "Historical rationale undocumented" if not.]

## Functional Requirements (As-Built)
[Requirements derived from current behavior]
- FR-001: The system allows [behavior observed in code/UI]
- FR-002: ...

## Gaps and Enhancements
[Where the current implementation falls short]
- GAP-001: [missing behavior] — Priority: [H/M/L]

## Non-Functional Requirements (As-Built)
[Performance, security, etc. derived from current system characteristics]

## Success Metrics
[Metrics for planned enhancements, not the existing feature]
```

### When NOT to Create a Retroactive PRD

- For modules that are stable and not planned for changes
- For modules scheduled for replacement
- For infrastructure that is better documented as architecture than as product requirements

## Migration from Ad-Hoc to BMAD

A phased migration plan for teams moving from ad-hoc development to BMAD:

### Week 1-2: Awareness

- Introduce BMAD concepts to the team.
- Generate project-context.md for the existing codebase.
- No process changes yet.

### Week 3-4: Pilot

- Select one upcoming feature as a BMAD pilot.
- Write a PRD and stories for it using BMAD templates.
- Implement using BMAD Phase 4 practices.
- Hold a retrospective on the pilot.

### Week 5-8: Expansion

- Apply BMAD to all new features.
- Begin Level 2 adoption (stories + architecture sections).
- Update project-context.md after each feature.
- Refine templates based on team feedback.

### Week 9-12: Stabilization

- Full BMAD flow for major features.
- Begin retroactive documentation for high-priority modules.
- Establish the implementation readiness gate for significant features.
- Review and customize BMAD templates for team needs.

### Ongoing: Maturity

- All new work follows BMAD.
- Architecture document grows organically.
- Gate is standard for all multi-story features.
- Team contributes improvements back to BMAD templates.

## Common Pitfalls

### Pitfall 1: Big Bang Adoption

**Symptom**: Trying to document the entire existing system before writing any new code.
**Consequence**: Weeks of documentation work with no visible development progress. Team loses enthusiasm.
**Fix**: Start with Level 1 (stories only) for new features. Build documentation incrementally.

### Pitfall 2: Ignoring Existing Conventions

**Symptom**: BMAD artifacts use different naming conventions, directory structures, or terminology than the existing codebase.
**Consequence**: Cognitive overhead switching between BMAD artifacts and code. Team treats BMAD as "that extra process."
**Fix**: Adapt BMAD templates to match existing project conventions. If the team calls them "tickets" not "stories," use "tickets" in your BMAD artifacts.

### Pitfall 3: Retroactive Documentation Drift

**Symptom**: Creating a retroactive architecture document, then never updating it as the code evolves.
**Consequence**: The document becomes stale within weeks and developers stop trusting it.
**Fix**: Include an architecture doc update step in every PR template. Treat documentation updates as part of the story definition of done.

### Pitfall 4: Over-Documenting Stable Code

**Symptom**: Creating detailed PRDs and architecture docs for modules that have not changed in a year and have no planned changes.
**Consequence**: Wasted effort on artifacts nobody will read.
**Fix**: Apply BMAD documentation effort proportionally to change frequency. Stable modules get Level 1 inventory only.

### Pitfall 5: Treating BMAD as Waterfall

**Symptom**: Refusing to start implementation until every Phase 1 and Phase 2 artifact is perfect.
**Consequence**: Analysis paralysis. The existing codebase continues to evolve without BMAD guidance.
**Fix**: In brownfield projects, phases can overlap. You can implement stories for Module A while still documenting Module B. The key constraint is that each individual story passes its relevant gate checks, not that the entire system is fully documented.

### Pitfall 6: Ignoring Technical Debt

**Symptom**: Creating clean BMAD artifacts that describe the ideal state while ignoring the reality of legacy code.
**Consequence**: Stories are blocked by undocumented dependencies, unexpected behaviors, and hidden coupling.
**Fix**: Include a "Current Reality" section in every story that touches legacy code. Acknowledge technical debt explicitly and either address it in the story or document it as a risk.

---

## Assumptions

- The existing project has a functioning build and test pipeline (even minimal)
- At least one team member has deep knowledge of the existing codebase
- The team is willing to invest 15-30 minutes per feature in story writing (Level 1 minimum)

## Limits

- This guide does NOT cover data migration from legacy systems — that requires its own project plan
- This guide does NOT prescribe how to resolve existing technical debt — it only documents it
- Brownfield BMAD adoption does NOT require retroactive PRDs for existing features unless those features are being modified

## Edge Cases

- **No team member understands the codebase**: Before BMAD adoption, run a code archeology sprint. Use AI to generate a project-context.md and architecture inventory. Human-validate before proceeding.
- **Project has no tests at all**: Add a "write tests for touched code" requirement to every BMAD story. Do not attempt to write tests for the entire codebase retroactively.
- **Multiple teams own the same codebase**: Establish shared exclusion zones and a single project-context.md before any team begins BMAD adoption. See `references/enterprise-governance.md`.

## Acceptance Criteria

- [ ] Risk score has been calculated and adoption level selected accordingly
- [ ] Minimum documentation threshold is met (project-context.md, exclusion zones, Level 1 inventory)
- [ ] First BMAD story has been written and implemented successfully (pilot validation)
- [ ] Retroactive documentation drift prevention is in place (PR template includes doc update step)

See also: `references/methodology-overview.md`, `references/project-context-guide.md`, `references/greenfield-patterns.md`, `references/customization-guide.md`
