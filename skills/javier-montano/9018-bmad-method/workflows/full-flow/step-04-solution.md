---
stepNumber: 4
stepName: "Design Architecture and Decompose Stories"
agent: "architect + sm"
inputs:
  - "project-context.md"
  - "PRD.md"
  - "ux-spec.md"
outputs:
  - "architecture.md"
  - "ADR files (adr-NNN-*.md)"
  - "Epic and story files"
  - "Implementation readiness gate report"
stepsCompleted: 3
currentStep: 4
nextStep: "step-05-implement.md"
---

# Step 4: Design Architecture and Decompose Stories

## Step Goal

Decide **how** to build the system through a technical architecture document, then decompose the work into implementable epics and stories. Conclude with an implementation readiness gate check.

## Execution Rules

1. Activate **Winston (Architect)** first, then **Bob (Scrum Master)** for decomposition.
2. Every architectural decision must be documented as an ADR (Architecture Decision Record).
3. Stories must follow the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).
4. The implementation readiness gate must pass before proceeding.

### Context from Previous Steps

- From Step 1: `project-context.md` — tech stack, constraints.
- From Step 2: `product-brief.md` — vision, scope.
- From Step 3: `PRD.md` + `ux-spec.md` — requirements and UX.

## Instructions

1. **Activate Winston (Architect)**: Load `agents/winston-architect.md`. Winston designs the system architecture driven by requirements.

2. **Create architecture.md**: Using `architecture-doc.md.tmpl`, produce:
   - System overview and component diagram (mermaid)
   - Technology stack decisions with rationale
   - Data model — entities, relationships, storage strategy
   - API design — endpoints, contracts, authentication
   - Infrastructure and deployment architecture
   - Security architecture
   - Integration points and external dependencies
   - Scalability and performance design

3. **Write ADRs**: For each significant decision (framework choice, database selection, auth strategy, etc.), create an ADR file following the format: `adr-001-<slug>.md`. Each ADR must include context, decision, consequences, and status.

4. **Activate Bob (Scrum Master)**: Load `agents/bob-scrum-master.md`. Bob decomposes architecture into deliverable work units.

5. **Create epics and stories**: For each major functional area:
   - Create an epic file using `epic.md.tmpl`
   - Decompose each epic into stories using `user-story.md.tmpl`
   - Each story must have: title, description, acceptance criteria, estimation (S/M/L), dependencies
   - Sequence stories respecting dependency order

6. **Map dependencies**: Create a dependency graph showing which stories block others. Identify the critical path.

7. **Run implementation readiness gate**: Load `references/implementation-readiness-gate.md` and execute the 13-step checklist. Produce a gate report. The result must be PASS to proceed.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Tech stack conflicts with NFRs         | Revisit with user; document tradeoffs in ADR |
| Story count exceeds 50                 | Recommend phased delivery (MVP first)        |
| Gate result is CONCERNS                | Address concerns, re-run gate                |
| Gate result is FAIL                    | Return to the failing phase for remediation  |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] architecture.md exists with all required sections
- [ ] At least 2 ADRs are written
- [ ] All epics have at least one story
- [ ] Every story has acceptance criteria and estimation
- [ ] Dependency graph is documented
- [ ] Implementation readiness gate result is PASS

### Output Validation

| Output               | Validation Rule                                    | Pass/Fail |
|---------------------|--------------------------------------------------|-----------|
| architecture.md     | Component diagram + data model + API design exist  | ____      |
| ADR files           | At least 2 ADRs with complete sections             | ____      |
| Story files         | All stories have acceptance criteria               | ____      |
| Gate report         | Result is PASS                                     | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Implementation readiness gate result is FAIL
> - Architecture document is missing data model or API design
> - Stories exist without acceptance criteria
> - Circular dependencies detected in story graph
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If the gate result is FAIL:
1. Read the gate report to identify failing checks
2. Return to the phase that produced the failing artifact (Phase 2 for PRD issues, Phase 3 for architecture issues)
3. Fix the identified gaps and re-run the gate
4. Do not delete existing stories or architecture — amend them

## Skip Conditions

- **Skip if**: architecture.md, epics, and stories already exist AND the implementation readiness gate passes with PASS result
- **Do NOT skip if**: The PRD or UX spec has been modified since the architecture was written

## Time Box

**Maximum**: 6 hours (3h architecture + 2h decomposition + 1h gate). If story decomposition exceeds 50 stories, pause and recommend MVP scoping before continuing.

## Step Completion Criteria

- [ ] architecture.md has component diagram, data model, API design, and security sections
- [ ] At least 2 ADRs written with context, decision, and consequences
- [ ] All epics have at least one story with acceptance criteria
- [ ] Dependency graph documented with critical path identified
- [ ] Implementation readiness gate result is PASS

---

**Next step**: `step-05-implement.md`
