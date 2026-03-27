# BMAD Anti-Patterns Catalog

## Table of Contents
- [How to Use This Catalog](#how-to-use-this-catalog)
- [Process Anti-Patterns](#process-anti-patterns)
- [Artifact Anti-Patterns](#artifact-anti-patterns)
- [Agent Anti-Patterns](#agent-anti-patterns)
- [Context Anti-Patterns](#context-anti-patterns)
- [Sprint Anti-Patterns](#sprint-anti-patterns)
- [Quick Reference Matrix](#quick-reference-matrix)

---

## How to Use This Catalog

Each anti-pattern entry contains: **Name**, **Severity** (Critical/High/Medium), **Phase(s)** affected, **Symptom** (what you observe), **Root Cause** (why it happens), **Fix** (what to do), **Prevention** (how to stop it recurring), and **Reference** (where to find details).

Severity levels:
- **Critical**: Blocks progress or produces incorrect outputs. Must fix immediately.
- **High**: Degrades quality significantly. Fix within the current sprint.
- **Medium**: Causes inefficiency or minor quality loss. Fix within 2 sprints.

---

## Process Anti-Patterns

### AP-01: Prompt-and-Pray
**Severity**: Critical
**Phase(s)**: All (bypasses BMAD entirely)
**Symptom**: Developer prompts the AI with a vague request ("build me a login system") and accepts whatever comes out.
**Root Cause**: No documentation-first discipline. No story, no acceptance criteria, no constraints.
**Fix**: Stop. Write a story with acceptance criteria. Load project-context.md. Prompt the AI with specific constraints from the story file.
**Prevention**: The Orchestrator must verify that a story file exists before routing to the Developer agent. No story = no coding.
**Reference**: `references/methodology-overview.md#anti-patterns`

### AP-02: Phase Skipping
**Severity**: Critical
**Phase(s)**: Phase 2→3 or Phase 3→4
**Symptom**: Implementation begins without a PRD, without architecture, or without passing the gate.
**Root Cause**: Urgency override — "we don't have time for planning." False economy: skipping planning multiplies implementation time by 2-5x.
**Fix**: The Orchestrator checks artifact existence before routing. If the gate-result file is missing or shows FAIL, Phase 4 is blocked. No exceptions without the override procedure [R21].
**Prevention**: Make the gate a CI check (see `references/integration-patterns.md#gate-as-ci-stage`). Automate the enforcement.
**Reference**: `references/implementation-readiness-gate.md` [R20]

### AP-03: Gate Theater
**Severity**: High
**Phase(s)**: Phase 3→4 transition
**Symptom**: The gate runs but never fails. Every evaluation is PASS regardless of artifact quality.
**Root Cause**: Gate evaluator is rubber-stamping instead of critically evaluating. Common when the same person writes artifacts and evaluates the gate.
**Fix**: Separate the gate evaluator from the artifact producer. The Gate Reviewer agent must not be the same agent that created the architecture or stories. Track gate metrics: if first-pass rate is 100% across 5+ evaluations, the gate is not functioning.
**Prevention**: Monitor gate override frequency and first-pass rate per `references/metrics-framework.md#pm-2-gate-pass-rate`.
**Reference**: `references/implementation-readiness-gate.md#gate-metrics-history`

### AP-04: Waterfall Disguise
**Severity**: High
**Phase(s)**: Phase 1→2→3
**Symptom**: Team refuses to start Phase 3 until every Phase 2 artifact is "perfect." Months pass in planning without any implementation.
**Root Cause**: Misunderstanding BMAD phases as waterfall gates. BMAD phases are iterative — artifacts can be refined after the gate passes, through the change propagation protocol.
**Fix**: Set time-boxes for each phase (see `references/metrics-framework.md#pm-1-cycle-time-per-phase`). Artifacts must be "good enough for gate" not "perfect." Ship PRD v1.0.0, not v∞.
**Prevention**: Track phase cycle time. If Phase 2 exceeds 7 working days for a medium project, force a review.
**Reference**: `references/brownfield-patterns.md#pitfall-5`

### AP-05: Ceremony Without Substance
**Severity**: Medium
**Phase(s)**: Phase 4
**Symptom**: Sprint planning takes 5 minutes. Retrospectives produce no action items. Ceremonies exist as checkboxes, not tools.
**Root Cause**: Team treats ceremonies as overhead rather than diagnostic instruments.
**Fix**: Every retrospective must produce at least 1 concrete, assigned action item with a deadline. Sprint planning must include velocity review, dependency validation, and risk identification — not just story assignment.
**Prevention**: Use the retrospective template from `references/phase-4-implementation.md#sprint-retrospective`. Verify action items from the previous retro before starting the new one.
**Reference**: `references/phase-4-implementation.md#sprint-retrospective`

### AP-06: Scope Creep Through Quick Flow
**Severity**: High
**Phase(s)**: Quick Flow → Phase 4
**Symptom**: Sequential Quick Flows in the same area accumulate into an undocumented feature. No PRD, no architecture review, no gate — but the codebase has grown significantly.
**Root Cause**: Quick Flow's 3-consecutive-limit [R10] is not enforced. Each individual change is small, but the aggregate is a feature.
**Fix**: Review the last 3-4 Quick Flows. Write a retroactive story consolidating them. Assess whether architecture review is needed.
**Prevention**: Track Quick Flow count per feature area per sprint. Alert at 3 consecutive Quick Flows.
**Reference**: `references/quick-flow.md` [R10]

### AP-07: Process Cargo Cult
**Severity**: Medium
**Phase(s)**: All
**Symptom**: Team follows every BMAD step mechanically without understanding why. Artifacts are filled in but contain no insight. Stories have acceptance criteria that are reworded requirements, not testable behaviors.
**Root Cause**: Adoption focused on form, not function. Team was told WHAT to do, not WHY.
**Fix**: For each BMAD artifact, the producer must be able to answer: "What decision does this artifact enable?" If they cannot answer, they do not understand the artifact's purpose.
**Prevention**: Onboarding must include the "why" for each phase and artifact. Use `references/methodology-overview.md` as the conceptual foundation.
**Reference**: `references/methodology-overview.md#core-principles`

---

## Artifact Anti-Patterns

### AP-08: Orphan Story
**Severity**: High
**Phase(s)**: Phase 3, Phase 4
**Symptom**: A story exists in the backlog but traces to no FR in the PRD, or traces to an FR that was removed.
**Root Cause**: PRD was updated without running the backward scan on stories.
**Fix**: Archive the orphan story (do not delete). Run `check_artifact_flow.py --orphans`. Update the traceability matrix.
**Prevention**: Run orphan detection at every sprint boundary. Add it as a CI check.
**Reference**: `references/artifact-flow-chain.md#orphan-detection`

### AP-09: Zombie Artifact
**Severity**: Medium
**Phase(s)**: Phase 3, Phase 4
**Symptom**: An artifact (ADR, story, architecture section) exists but is outdated and contradicts current reality. Nobody has updated it, but nobody has removed it either.
**Root Cause**: No artifact freshness tracking. No update trigger when related artifacts change.
**Fix**: Review every artifact referenced by the current sprint's stories. Mark outdated artifacts as deprecated or update them. Use `git log` to find artifacts unchanged for >2 sprints.
**Prevention**: Track artifact freshness (see `references/metrics-framework.md#pm-5-artifact-freshness`). Include artifact review in sprint planning.
**Reference**: `references/artifact-flow-chain.md#versioning-rules-for-artifacts`

### AP-10: PRD as Novel
**Severity**: Medium
**Phase(s)**: Phase 2
**Symptom**: PRD is 30+ pages of prose. Nobody reads it completely. AI agents consume most of the context window loading it.
**Root Cause**: PM confused thoroughness with verbosity. Requirements are buried in narrative instead of structured in tables and lists.
**Fix**: Restructure PRD using the schema from `references/schemas.md`. FRs must be in tabular format with IDs, descriptions, and MoSCoW priorities. Eliminate prose sections that do not contain requirements.
**Prevention**: PRD template must enforce structured format. Limit PRD to sections defined in the schema. Supplementary research goes in separate documents, not the PRD.
**Reference**: `references/schemas.md#3-prd-frontmatter-schema`

### AP-11: Missing Traceability
**Severity**: Critical
**Phase(s)**: Phase 3→4
**Symptom**: Stories exist but have no `fr-refs` field. Code exists but commit messages have no story IDs. Nobody can answer "which requirement does this code implement?"
**Root Cause**: Traceability was treated as optional instead of mandatory. Schema validation was not enforced.
**Fix**: Retroactively add `fr-refs` to all stories. Add story ID enforcement via commit-msg hook (see `references/integration-patterns.md#commit-message-story-id-enforcement`). Build the traceability matrix.
**Prevention**: Pre-commit hook validates `fr-refs` exists on every story file. Commit-msg hook validates story ID in every commit.
**Reference**: `references/artifact-flow-chain.md#traceability-matrix`

### AP-12: Copy-Paste Architecture
**Severity**: High
**Phase(s)**: Phase 3
**Symptom**: Architecture document is a generic template with project-specific names filled in. It describes "a standard microservices architecture" without any project-specific decisions.
**Root Cause**: Architect used a template without adapting it. No ADRs exist because no actual decisions were documented.
**Fix**: For every component in the architecture, answer: "Why this component and not an alternative?" If you cannot answer, write an ADR. If the architecture has no ADRs, it has no decisions — it is a template, not an architecture.
**Prevention**: Gate step 2 (Architecture Alignment) must verify ADRs exist. Architecture without ADRs is a FAIL.
**Reference**: `references/implementation-readiness-gate.md#step-2-architecture-alignment`

### AP-13: Acceptance Criteria as Wishes
**Severity**: High
**Phase(s)**: Phase 3
**Symptom**: Acceptance criteria use subjective language: "the page should load quickly," "the UI should look professional," "the system should handle errors gracefully."
**Root Cause**: Story writer did not apply the testability criterion: can you write an automated test from this AC?
**Fix**: Every AC must follow Given/When/Then with specific values. Replace "quickly" with "< 200ms p95." Replace "handle errors" with "return HTTP 400 with error code INVALID_INPUT."
**Prevention**: Gate step 4 (Acceptance Criteria Quality) catches this. Apply during story writing, not just at the gate.
**Reference**: `references/implementation-readiness-gate.md#step-4-acceptance-criteria-quality`

---

## Agent Anti-Patterns

### AP-14: God Agent
**Severity**: Critical
**Phase(s)**: All
**Symptom**: One agent handles analysis, planning, architecture, story writing, and implementation. Outputs lack the multi-perspective review that agent specialization provides.
**Root Cause**: Solo developer uses a single "do everything" prompt instead of cycling through specialized agents.
**Fix**: Even solo developers must activate different agent personas per phase. The persona constrains the agent's perspective — an Analyst asks different questions than an Architect.
**Prevention**: Orchestrator enforces agent routing. Each phase has designated agents per `references/methodology-overview.md#the-4-phase-model`.
**Reference**: `references/methodology-overview.md#core-principles`

### AP-15: Agent Scope Creep
**Severity**: High
**Phase(s)**: Any
**Symptom**: Developer agent modifies the PRD. PM agent writes code. Architect agent changes story point estimates.
**Root Cause**: Agent YAML has no `forbidden_actions` constraints, or constraints are not specific enough.
**Fix**: Add explicit `constraints.forbidden_actions` to every agent. Developer: "Do not modify PRD, architecture, or epic files." PM: "Do not write code or modify test files."
**Prevention**: Agent schema validation checks that `forbidden_actions` is populated. See `references/agent-as-code.md`.
**Reference**: `references/agent-as-code.md#agent-yaml-format`, `references/conflict-resolution-protocol.md#ownership-matrix`

### AP-16: Persona Amnesia
**Severity**: Medium
**Phase(s)**: Any
**Symptom**: Agent outputs are generic and indistinguishable from raw LLM output. Communication style does not match the persona definition. The "Architect" writes like the "Developer."
**Root Cause**: Persona identity is too vague (e.g., "An experienced engineer"). The persona does not constrain behavior enough.
**Fix**: Rewrite `persona.identity` to be at least 3 specific sentences. Include: expertise area, working philosophy, and a distinctive behavioral trait. Run the persona consistency test (3 inputs, compare outputs).
**Prevention**: Agent testing strategy per `references/agent-as-code.md#agent-testing-strategy`. MINOR version bumps require the persona consistency test.
**Reference**: `references/agent-as-code.md#persona-design-principles`

### AP-17: Agent Echo Chamber
**Severity**: Medium
**Phase(s)**: Phase 2→3
**Symptom**: All agents agree with each other. No trade-offs are surfaced. PRD is approved without critique. Architecture is accepted without challenge.
**Root Cause**: Agent personas lack deliberate tensions. All agents are designed to be agreeable.
**Fix**: Ensure complementary tensions exist: PM advocates for user needs vs. Architect advocates for technical constraints. Analyst explores broadly vs. PM scopes narrowly. If agents never disagree, the multi-agent model is not adding value.
**Prevention**: Design agent personas with the "complementary tensions" principle from `references/agent-as-code.md#persona-design-principles`.
**Reference**: `references/agent-as-code.md#persona-design-principles`

---

## Context Anti-Patterns

### AP-18: Context Dumping
**Severity**: High
**Phase(s)**: Any
**Symptom**: Every session loads the full PRD, full architecture doc, all stories, and project-context.md — regardless of the current task. Agent outputs are unfocused and sometimes contradictory.
**Root Cause**: No progressive context discipline. Loading everything "just in case" wastes context window capacity and introduces noise.
**Fix**: Follow the "What to Load Per Phase" table strictly. Each phase has an "Always Load," "Load on Demand," and "Never Load" column. Respect all three.
**Prevention**: Validate context loading against the phase table at session start. If an artifact is in the "Never Load" column for the current phase, do not load it.
**Reference**: `references/progressive-context.md#what-to-load-per-phase`

### AP-19: Stale Context
**Severity**: High
**Phase(s)**: Phase 4
**Symptom**: Agent references an outdated version of an artifact. Architecture doc from 3 iterations ago is loaded. Code is generated against a superseded API contract.
**Root Cause**: Context loaded from a stale file or cached version instead of the latest commit.
**Fix**: Always load from the latest committed version. Use Git refs when specifying which version to load. Verify artifact version in frontmatter matches expected version.
**Prevention**: Version-pin context to a specific Git commit per session. Add a version check at session start: "Is this artifact's version the latest?"
**Reference**: `references/progressive-context.md#avoiding-context-pollution`

### AP-20: Context Pollution via Conversation
**Severity**: Medium
**Phase(s)**: Any (long sessions)
**Symptom**: Session has 50+ turns. Agent outputs degrade. Agent starts contradicting its earlier statements or mixing up details from different stories.
**Root Cause**: Conversational debris accumulates. The agent processes all prior messages on every turn, including irrelevant exploration and dead-end discussions.
**Fix**: Start a new session. Summarize current state into project-context.md. Load fresh context in the new session.
**Prevention**: Align session boundaries with workflow steps. One step per session when possible. Never exceed 50 turns without a session reset.
**Reference**: `references/progressive-context.md#avoiding-context-pollution`

### AP-21: Mid-Section Truncation
**Severity**: Critical
**Phase(s)**: Any
**Symptom**: Agent hallucinates details about an artifact section that was partially loaded. Generated code references API fields that do not exist.
**Root Cause**: An artifact was truncated mid-section to fit the context window. The agent filled in the missing parts from its training data.
**Fix**: Never truncate an artifact mid-section. Either load the full section or summarize it. Partial sections cause hallucinations.
**Prevention**: Follow [R27]: drop items by priority level, replace full docs with section loads, summarize instead of truncating.
**Reference**: `references/progressive-context.md` [R27]

---

## Sprint Anti-Patterns

### AP-22: Perpetual Carry-Over
**Severity**: High
**Phase(s)**: Phase 4
**Symptom**: The same stories carry over sprint after sprint. Stories that were "almost done" in Sprint 2 are still "almost done" in Sprint 4.
**Root Cause**: Stories are too large, estimates are systematically too low, or hidden dependencies keep surfacing.
**Fix**: If a story has been carried over twice, split it unconditionally. Re-estimate using actuals from similar completed stories, not gut feel.
**Prevention**: Track carry-over rate per `references/metrics-framework.md#pm-4-carry-over-rate`. No story may exceed 5 points. The 8-point maximum in the schema [schemas.md] is for exceptional cases only.
**Reference**: `references/phase-4-implementation.md#carry-over-policy`

### AP-23: Sprint Stuffing
**Severity**: High
**Phase(s)**: Phase 4
**Symptom**: Sprint is planned with 50 points when velocity average is 30. Team commits to optimistic plan and consistently under-delivers.
**Root Cause**: Planning ignores velocity data. "This sprint will be different" mindset.
**Fix**: Sprint capacity = 3-sprint velocity average minus 10-20% buffer. No exceptions. If stakeholders want more stories, either extend the timeline or remove lower-priority stories.
**Prevention**: Automated velocity check in sprint planning. Sprint capacity cannot exceed 110% of 3-sprint average without documented justification.
**Reference**: `references/phase-4-implementation.md#story-selection-and-capacity`

### AP-24: Testing After Implementation
**Severity**: High
**Phase(s)**: Phase 4
**Symptom**: Developer writes all code first, then writes tests to match the implementation. Tests pass trivially because they test what was built, not what was specified.
**Root Cause**: TDD discipline not followed. Tests derived from implementation rather than from acceptance criteria.
**Fix**: Delete tests that were reverse-engineered from code. Re-read the story's Given/When/Then. Write failing tests from the AC text. Then modify code (or regenerate) to pass those tests.
**Prevention**: Code review checklist item: "Were tests written before implementation?" Definition of Done requires TDD evidence.
**Reference**: `references/phase-4-implementation.md#test-driven-story-development`

### AP-25: Invisible Blockers
**Severity**: High
**Phase(s)**: Phase 4
**Symptom**: A developer is stuck for 2 days but sprint-status.yaml still shows "in-progress." The blocker is discovered at the sprint end, too late to recover.
**Root Cause**: No blocker escalation protocol. Developer tries to solve everything independently.
**Fix**: Mandate: if progress halts for more than 4 hours, document the blocker in sprint-status.yaml and escalate per the blocker protocol.
**Prevention**: Daily sprint-status.yaml updates. If a story's status has not changed in 2 days and is not "done," the Scrum Master must investigate.
**Reference**: `references/phase-4-implementation.md#handling-blockers`

### AP-26: Retrospective Amnesia
**Severity**: Medium
**Phase(s)**: Phase 4
**Symptom**: The same problems appear sprint after sprint. Retro action items are created but never tracked. Nobody checks if last sprint's actions were implemented.
**Root Cause**: Retro action items are not tracked as stories or tasks. They exist only in the retro document.
**Fix**: Every retro action item must have an owner and a deadline. Action items that require implementation must become stories in the next sprint backlog.
**Prevention**: Start every retro by reviewing the previous retro's action items. If an action was not completed, it must either be completed this sprint or explicitly deprioritized with justification.
**Reference**: `references/phase-4-implementation.md#sprint-retrospective`

### AP-27: Rogue Code
**Severity**: Critical
**Phase(s)**: Phase 4
**Symptom**: Code exists on a feature branch that does not correspond to any story. "While I'm here" changes are bundled with story implementations.
**Root Cause**: No scope discipline during implementation. Developer sees an opportunity to fix or improve something unrelated and includes it.
**Fix**: Revert the unrelated changes. If the improvement is worthwhile, create a Quick Flow rapid spec for it. Each branch must implement exactly one story.
**Prevention**: Code review checklist: "Does every change in this PR trace to the referenced story?" Self-review checklist item: "No unrelated changes included."
**Reference**: `references/quick-flow.md#self-review-checklist`

---

## Quick Reference Matrix

| ID | Name | Severity | Phase(s) | Fix Reference |
|----|------|----------|----------|---------------|
| AP-01 | Prompt-and-Pray | Critical | All | `methodology-overview.md` |
| AP-02 | Phase Skipping | Critical | 2→3, 3→4 | `implementation-readiness-gate.md` |
| AP-03 | Gate Theater | High | 3→4 | `implementation-readiness-gate.md` |
| AP-04 | Waterfall Disguise | High | 1→2→3 | `brownfield-patterns.md` |
| AP-05 | Ceremony Without Substance | Medium | 4 | `phase-4-implementation.md` |
| AP-06 | Scope Creep Through Quick Flow | High | QF→4 | `quick-flow.md` |
| AP-07 | Process Cargo Cult | Medium | All | `methodology-overview.md` |
| AP-08 | Orphan Story | High | 3, 4 | `artifact-flow-chain.md` |
| AP-09 | Zombie Artifact | Medium | 3, 4 | `artifact-flow-chain.md` |
| AP-10 | PRD as Novel | Medium | 2 | `schemas.md` |
| AP-11 | Missing Traceability | Critical | 3→4 | `artifact-flow-chain.md` |
| AP-12 | Copy-Paste Architecture | High | 3 | `implementation-readiness-gate.md` |
| AP-13 | Acceptance Criteria as Wishes | High | 3 | `implementation-readiness-gate.md` |
| AP-14 | God Agent | Critical | All | `methodology-overview.md` |
| AP-15 | Agent Scope Creep | High | Any | `agent-as-code.md` |
| AP-16 | Persona Amnesia | Medium | Any | `agent-as-code.md` |
| AP-17 | Agent Echo Chamber | Medium | 2→3 | `agent-as-code.md` |
| AP-18 | Context Dumping | High | Any | `progressive-context.md` |
| AP-19 | Stale Context | High | 4 | `progressive-context.md` |
| AP-20 | Context Pollution via Conversation | Medium | Any | `progressive-context.md` |
| AP-21 | Mid-Section Truncation | Critical | Any | `progressive-context.md` |
| AP-22 | Perpetual Carry-Over | High | 4 | `phase-4-implementation.md` |
| AP-23 | Sprint Stuffing | High | 4 | `phase-4-implementation.md` |
| AP-24 | Testing After Implementation | High | 4 | `phase-4-implementation.md` |
| AP-25 | Invisible Blockers | High | 4 | `phase-4-implementation.md` |
| AP-26 | Retrospective Amnesia | Medium | 4 | `phase-4-implementation.md` |
| AP-27 | Rogue Code | Critical | 4 | `quick-flow.md` |

---

## Assumptions

- The team has access to the full BMAD reference documentation for cross-referenced fixes
- Validation scripts (`validate_project.py`, `check_artifact_flow.py`) are available for automated detection
- Anti-pattern detection is a team responsibility — no single role is accountable for catching all patterns

## Limits

- This catalog covers BMAD-specific anti-patterns — it does NOT cover general software anti-patterns (God Object, Spaghetti Code, etc.)
- Detection is primarily manual or semi-automated — fully automated detection of all 27 patterns is not feasible
- Severity ratings are calibrated for AI-assisted development — traditional teams may experience different impact levels

## Acceptance Criteria

- [ ] Catalog contains 25+ anti-patterns covering all 5 categories
- [ ] Every anti-pattern has a concrete, actionable fix (not "be more careful")
- [ ] Every fix cross-references the appropriate BMAD reference document
- [ ] Quick reference matrix enables lookup by ID, severity, or phase
- [ ] No anti-pattern duplicates content already in another reference doc — each entry adds unique diagnostic value

See also: `references/methodology-overview.md`, `references/troubleshooting.md`, `references/metrics-framework.md`, `references/implementation-readiness-gate.md`, `references/progressive-context.md`
