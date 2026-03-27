# Customization Guide — Adapting BMAD to Your Needs

## Table of Contents
- [Customization Philosophy](#customization-philosophy)
- [Adding Custom Phases](#adding-custom-phases)
- [Removing Phases for Lightweight Projects](#removing-phases-for-lightweight-projects)
- [Creating Domain-Specific Agents](#creating-domain-specific-agents)
- [Modifying Gate Criteria](#modifying-gate-criteria)
- [Workflow Variants](#workflow-variants)
- [Integrating with Existing Ceremonies](#integrating-with-existing-ceremonies)
- [Custom Templates](#custom-templates)
- [Extending the Agent Roster](#extending-the-agent-roster)
- [BMAD for Solo Developers vs Teams](#bmad-for-solo-developers-vs-teams)
- [Customization Without Breaking the Framework](#customization-without-breaking-the-framework)

---

## Customization Philosophy

BMAD is a framework, not a regulation. Every team, domain, and project has unique needs. The methodology is designed to be adapted — but adapted thoughtfully, not arbitrarily.

**The customization rule**: Understand why a component exists before removing or modifying it. Every BMAD element solves a specific problem. If your project does not have that problem, remove the element. If your project has a different variant of the problem, modify the element. If you are not sure, keep it for one project and evaluate afterward.

**What is safe to customize**:
- Templates (fields, sections, formatting)
- Agent personas and communication styles
- Gate criteria thresholds and weights
- Phase boundaries and naming
- Workflow step order within a phase
- Tool integrations

**What should NOT be customized**:
- The principle that documentation precedes implementation
- The requirement for testable acceptance criteria
- Git-based version control of artifacts
- The concept of gate-based phase transitions (though gate contents can change)

## Adding Custom Phases

BMAD's standard 4-phase model can be extended for projects with additional needs.

### Example: Adding a Phase 0 — Discovery

For projects with high uncertainty, add a discovery phase before product definition:

```
Phase 0: Discovery
  Purpose: Validate that the problem is worth solving.
  Artifacts: User research summary, competitive analysis, feasibility study.
  Gate: Discovery gate — Is there evidence of a real problem?
        Is a solution technically feasible?

Phase 1: Product Definition (standard)
Phase 2: Architecture (standard)
Phase 3: Planning (standard)
Phase 4: Implementation (standard)
```

### Example: Adding a Phase 5 — Launch

For products with significant launch coordination:

```
Phase 4: Implementation (standard)

Phase 5: Launch
  Purpose: Coordinate release, documentation, and go-to-market.
  Artifacts: Launch checklist, user documentation, monitoring dashboards,
             support runbook.
  Gate: Launch readiness gate — Are all launch criteria met?
```

### How to Add a Phase

1. **Define the purpose** — What problem does this phase solve?
2. **Define the artifacts** — What outputs does this phase produce?
3. **Define the gate** — What must be true to exit this phase?
4. **Create agent workflows** — Which agent handles this phase's work?
5. **Update project-context.md template** — Add the phase to the status tracking.
6. **Document in your team's BMAD customization log**.

## Removing Phases for Lightweight Projects

Not every project needs all 4 phases. Here are common reductions:

### Two-Phase BMAD (Planning + Implementation)

For small features added to an existing, well-documented system:

- **Skip Phase 1**: The PRD already exists at the product level. The feature is a line item.
- **Skip Phase 2**: The architecture is established. The feature fits within existing patterns.
- **Keep Phase 3**: Write stories with acceptance criteria.
- **Keep Phase 4**: Implement the stories.

This works when the existing PRD and architecture are current and cover the new feature's domain.

### Single-Phase BMAD (Implementation Only)

For bug fixes and minor changes:

- Write a minimal story (description + acceptance criteria + bug reproduction steps).
- Implement and verify against acceptance criteria.
- No PRD update, no architecture review, no gate.

This is the absolute minimum BMAD — a structured story with testable criteria. It is still better than ad-hoc because the acceptance criteria provide a verification target.

### When Reduction is Dangerous

Do NOT reduce phases when:
- The feature involves new architectural components
- The feature touches security, authentication, or data models
- Multiple teams are affected
- The feature has compliance implications
- Scope is ambiguous (if you are not sure what "done" looks like, you need Phase 1)

## Creating Domain-Specific Agents

BMAD agents can be specialized for your domain while inheriting the base agent capabilities.

### Example: E-Commerce PM Agent

```yaml
metadata:
  id: ecommerce-pm
  name: E-Commerce Product Manager
  icon: "🛒"
  module: bmm

persona:
  role: E-Commerce Product Manager
  identity: >
    You are a product manager specializing in e-commerce platforms.
    You understand conversion funnels, cart abandonment, payment flows,
    and marketplace dynamics. You prioritize requirements based on
    revenue impact and customer lifetime value.
  communication_style: >
    Data-driven and customer-focused. Always reference conversion metrics
    when prioritizing. Pushback on features that do not connect to a
    measurable business outcome.
  principles:
    - Every feature must connect to a conversion metric or retention metric
    - Cart and checkout flows are always P0 — revenue depends on them
    - Payment integration stories require security review before implementation
    - Mobile experience is equal priority to desktop, never an afterthought

menu:
  - trigger: PB
    description: Create Product Brief (E-Commerce)
    workflow: workflows/ecommerce-product-brief.md
  - trigger: PR
    description: Create PRD (E-Commerce)
    workflow: workflows/ecommerce-prd.md
  - trigger: CF
    description: Conversion Funnel Analysis
    workflow: workflows/conversion-analysis.md
```

### Domain-Specific Agent Design Steps

1. **Start from a base BMAD agent** (PM, Architect, Developer).
2. **Add domain expertise** to the persona identity.
3. **Add domain principles** that guide decision-making.
4. **Create domain-specific workflows** for common tasks in your domain.
5. **Add domain-specific menu items** that trigger those workflows.
6. **Test the agent** on a real project in your domain before rolling out.

### Domains That Benefit from Custom Agents

- **Healthcare**: Agents that understand HIPAA, HL7/FHIR, clinical workflows
- **Finance**: Agents that understand PCI-DSS, transaction integrity, reconciliation
- **Gaming**: Agents that understand game loops, matchmaking, real-time state sync
- **IoT**: Agents that understand device constraints, edge computing, OTA updates
- **Data platforms**: Agents that understand ETL, data quality, schema evolution

## Modifying Gate Criteria

The 13-step implementation readiness gate can be modified to match your project's needs.

### Adding Gate Steps

If your domain has additional concerns, add steps:

```markdown
Step 14: Accessibility Audit
  What is checked: WCAG 2.1 AA compliance plan exists for all user-facing stories.
  PASS: All user-facing stories include accessibility acceptance criteria.
  WARN: Most stories have accessibility criteria but 1-2 are missing.
  FAIL: No accessibility consideration in any story.
```

### Removing Gate Steps

If a step does not apply to your project, remove it with documentation:

```markdown
## Gate Customization Log
- Step 8 (API Contracts): REMOVED. This project has no API — it is a CLI tool.
  Replacement: Step 8a (CLI Interface Contract) — all commands, flags, and
  output formats documented.
- Step 12 (Deployment Strategy): SIMPLIFIED. Single binary distribution,
  no multi-environment deployment needed.
```

### Adjusting Weights

Change which steps are critical based on your domain:

| Domain | Critical Steps (WARN counts as 2) |
|--------|----------------------------------|
| Default BMAD | 1 (PRD), 2 (Architecture), 8 (API), 10 (Security) |
| Healthcare | 1, 2, 9 (Data Model), 10 (Security) |
| Real-time systems | 2, 7 (NFR), 8 (API), 11 (Performance) |
| Internal tools | 1, 3 (Stories), 4 (Acceptance Criteria), 12 (Deployment) |

### Adjusting Thresholds

Relax or tighten the overall pass threshold:

```markdown
# Startup / MVP threshold
PASS: No FAILs. Up to 5 WARNs allowed.
CONDITIONAL PASS: No FAILs. 6-8 WARNs.
FAIL: Any FAIL.

# Regulated environment threshold
PASS: All 13 steps PASS. Zero WARNs.
CONDITIONAL PASS: All PASS with up to 2 WARNs (none on critical steps).
FAIL: Any FAIL or any WARN on a critical step.
```

## Workflow Variants

### Agile (Scrum) Alignment

Map BMAD phases to Scrum ceremonies:

| BMAD Activity | Scrum Ceremony | Timing |
|--------------|---------------|--------|
| PRD creation/update | Product Backlog Refinement | Ongoing |
| Architecture review | Sprint Planning (technical discussion) | Sprint start |
| Story creation | Sprint Planning (commitment) | Sprint start |
| Gate evaluation | Sprint Planning (readiness check) | Before first story starts |
| Implementation | Sprint execution | During sprint |
| Acceptance verification | Sprint Review / Demo | Sprint end |
| Process retrospective | Sprint Retrospective | Sprint end |

### Kanban Alignment

BMAD with continuous flow instead of sprints:

- Stories enter a "Ready for Gate" column when written.
- Gate evaluation happens on demand (not sprint-bound).
- Stories that pass the gate move to "Ready for Implementation."
- WIP limits apply to each column including "In Gate Review."
- No sprint boundaries — work flows continuously through the BMAD pipeline.

### Hybrid (Scrumban)

Sprint-bounded planning with continuous flow execution:
- PRD and architecture reviews happen in sprint planning.
- Stories are created and gate-reviewed at sprint start.
- Implementation flows continuously within the sprint.
- Stories that pass acceptance move to "Done" without waiting for sprint end.

## Integrating with Existing Ceremonies

### Standups

Add a 30-second BMAD check to existing standups:
- "My story S-007 acceptance criteria 3 of 5 passing."
- "Blocked on gate step 8 — API contract for payment endpoint not finalized."

Do NOT replace standups with BMAD-specific meetings. Layer the information into what already exists.

### Sprint Planning

Integrate BMAD into existing sprint planning:
1. Review new stories (BMAD artifacts, not Jira tickets).
2. Run the gate for stories entering the sprint (can be pre-done and reviewed).
3. Commit to stories with acceptance criteria as the definition of done.

### Sprint Demos

Use BMAD acceptance criteria as the demo script:
- Walk through each story's acceptance criteria.
- Demonstrate PASS for each criterion.
- Any failing criteria are visible to stakeholders immediately.

### Retrospectives

Add BMAD-specific retrospective questions:
- Did any story need re-implementation because of incomplete acceptance criteria?
- Did the gate catch anything that would have caused problems in implementation?
- Were any BMAD artifacts unhelpful or redundant?
- What template changes would improve our next sprint?

## Custom Templates

### Modifying Existing Templates

BMAD templates have required and optional sections. Customize by:

1. **Adding sections**: Add domain-specific sections to templates.
   ```markdown
   ## Regulatory Impact (added for healthcare team)
   - PHI fields involved: [list]
   - HIPAA safeguards required: [list]
   - Compliance review needed: [Yes/No]
   ```

2. **Removing optional sections**: Remove sections tagged as optional that your team never fills in.

3. **Changing field labels**: Rename fields to match your team's vocabulary.
   ```
   "User Personas" -> "Customer Segments" (for B2B teams)
   "Stories" -> "Work Items" (for teams using that terminology)
   ```

### Creating New Templates

For domain-specific artifacts that BMAD does not cover:

```markdown
# Template: [Artifact Name]

## Purpose
[Why this artifact exists and when to create it]

## Required Sections
- [Section 1]: [description of what goes here]
- [Section 2]: [description]

## Optional Sections
- [Section 3]: [when to include this]

## Example
[Filled-in example of this template]

## Validation Criteria
[How to check if this artifact is complete]
```

Register custom templates in your team's project-context.md so agents know they exist.

## Extending the Agent Roster

### When to Create a New Agent

Create a new agent when:
- A recurring task requires specialized expertise not covered by existing agents.
- The task has a distinct persona (different communication style, different principles).
- The task produces unique artifacts not handled by existing workflows.

Do NOT create a new agent when:
- An existing agent can handle the task with a new workflow.
- The "agent" is really just a template or checklist.
- The specialization is a one-time need.

### New Agent Template

```yaml
metadata:
  id: [kebab-case-id]
  name: [Display Name]
  icon: "[emoji]"
  module: bmm

persona:
  role: [Professional title]
  identity: [Background, expertise, personality — 2-3 sentences]
  communication_style: [How this agent communicates — 1-2 sentences]
  principles:
    - [Core belief 1]
    - [Core belief 2]
    - [Core belief 3]

menu:
  - trigger: [XX]
    description: [Workflow display name]
    workflow: [path/to/workflow.md]
```

### Agent Interaction Patterns

When adding agents, define how they interact with existing agents:

```
New Agent: Security Reviewer
  Receives input from: Architect agent (architecture doc), PM agent (PRD security section)
  Produces output for: Gate evaluation (Step 10 evidence)
  Escalates to: Human security lead (for critical findings)
  Never interacts with: Developer agent directly (findings go through gate)
```

## BMAD for Solo Developers vs Teams

### Solo Developer Adaptations

| BMAD Element | Team Version | Solo Version |
|-------------|-------------|-------------|
| Agent personas | Specialized agents for each role | One person wears all hats; use agents as thinking tools |
| PR reviews | Peer review required | Self-review using agent as reviewer; or skip for low-risk changes |
| Gate evaluation | Architect agent runs gate | Solo dev runs gate; use it as a checklist rather than a ceremony |
| Ceremonies | Standups, demos, retros | Personal journal: what I did, what I learned, what I would change |
| project-context.md | Maintained for team consumption | Maintained for future-self consumption and session continuity |

### Solo Developer Quick Setup

1. Use BMAD quick flow for small projects (see `greenfield-patterns.md`).
2. Use full BMAD for projects you expect to maintain for more than 3 months.
3. Treat agents as rubber ducks with expertise — talk through decisions with them.
4. Commit artifacts to Git even though nobody else is reading them. Future-you will thank present-you.

### Scaling from Solo to Team

When a solo project grows to need a team:

1. Your BMAD artifacts become the onboarding material.
2. New team members read project-context.md to understand the project in 5 minutes.
3. The PRD and architecture doc answer "why was it built this way?" questions.
4. Story history shows the evolution of the project.
5. Gate reports show what was validated before each phase of implementation.

This is one of BMAD's strongest value propositions for solo developers — it makes your project transferable.

## Customization Without Breaking the Framework

### The Invariants

These properties must hold regardless of customization:

1. **Traceability**: Every piece of code traces back to a story. Every story traces back to a requirement.
2. **Testability**: Every story has acceptance criteria that can be verified.
3. **Versioning**: All artifacts are in version control.
4. **Progression**: Work moves through defined phases with explicit transitions (even if the phases are customized).

### The Compatibility Test Suite

**[R36]** Before adopting any customization, run ALL four tests. A customization that fails any test must not be adopted.

| # | Test | Question | Pass Criteria |
|---|------|----------|---------------|
| 1 | Onboarding | Can a new team member understand the project from its artifacts? | New member can set up environment and understand project scope within 1 hour of reading artifacts |
| 2 | Traceability | Can an auditor trace a code change back to a business requirement? | Every commit references a story ID, every story references an FR, every FR references a brief section |
| 3 | Testability | Can a developer know when a story is done? | Every story has acceptance criteria in Given/When/Then or equivalent testable format |
| 4 | Continuity | Can the project be resumed after a 3-month pause? | project-context.md + latest artifacts provide enough context to resume without oral history |

### Customization Registry Format

**[R37]** Maintain a machine-parseable customization registry alongside the customization log:

```yaml
# .bmad/customizations.yaml
customizations:
  - id: CUST-001
    date: "2025-02-15"
    type: gate-modification   # gate-modification | phase-change | agent-extension | template-change
    description: "Replaced Gate Step 8 (API Contracts) with CLI Interface Contract"
    reason: "Project is a CLI tool with no HTTP API"
    affects:
      - implementation-readiness-gate.md
      - gate-report-template.md
    reversible: true
    compatibility-test: pass  # pass | fail | partial
    review-date: "2025-04-15"
    status: active            # active | reverted | superseded
```

**What must remain for BMAD to work** (the invariants, regardless of customization):
1. Documentation precedes implementation (at minimum: a story before code)
2. Acceptance criteria exist for every work unit
3. All artifacts are version-controlled in Git
4. Phase transitions have explicit criteria (even if the phases are customized)

### Customization Log

Maintain a customization log in your project or team repository:

```markdown
# BMAD Customization Log

## [Date] — [Customization]
Reason: [Why this was changed]
Impact: [What BMAD elements are affected]
Reversible: [Yes/No]
Review date: [When to evaluate if this customization is working]

## 2025-02-15 — Removed Gate Step 8 (API Contracts)
Reason: Project is a CLI tool with no HTTP API.
Impact: Gate now has 12 steps. Step 8 replaced with CLI Interface Contract check.
Reversible: Yes — restore if project adds an API layer.
Review date: 2025-04-15
```

### Progressive Customization

The recommended customization approach:

1. **Sprint 1-2**: Use BMAD exactly as-is. No customizations.
2. **Sprint 3**: Retrospective identifies friction points. Make 1-2 small customizations.
3. **Sprint 4-6**: Evaluate customizations. Keep what works, revert what does not.
4. **Ongoing**: One customization per sprint maximum. Always with documented rationale.

This prevents the common failure mode of customizing everything at once and losing the framework's coherence.

---

## Assumptions

- The team has completed at least 1-2 sprints using unmodified BMAD before customizing
- Customization is motivated by specific friction points identified in retrospectives, not theoretical preferences
- A customization registry is maintained in the project repository

## Limits

- This guide does NOT cover customizing the AI models or prompting strategies — only BMAD framework components
- This guide does NOT prescribe customizations — it provides the process for making safe customizations
- Customizations must not violate the 4 invariants (traceability, testability, versioning, progression)

## Edge Cases

- **Team wants to remove the gate entirely**: This violates invariant #4 (phase transitions have explicit criteria). Instead, reduce the gate to the MVP partial gate (6 steps). If that is still too much, reduce to a 3-step mini-gate: PRD completeness, story decomposition, security review.
- **Two teams customize BMAD differently and must collaborate**: Establish a shared compatibility baseline (the 4 invariants + shared ID formats). Document team-specific deviations in each team's customization registry.
- **Customization breaks the compatibility test after initial pass**: Revert immediately. Run a retrospective to understand why it passed initially but failed in practice. Do not re-adopt without a modified approach.

## Acceptance Criteria

- [ ] Customization registry exists in `.bmad/customizations.yaml`
- [ ] Every customization passes all 4 compatibility tests before adoption
- [ ] No more than 1 customization is introduced per sprint
- [ ] The 4 BMAD invariants are preserved regardless of customization
- [ ] Review dates are set and honored for every active customization

See also: `references/methodology-overview.md`, `references/implementation-readiness-gate.md`, `references/enterprise-governance.md`, `references/agent-as-code.md`
