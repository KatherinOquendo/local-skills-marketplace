---
stepNumber: 1
stepName: "Design System Architecture"
agent: "architect"
inputs:
  - "PRD.md"
  - "ux-spec.md"
  - "project-context.md"
outputs:
  - "architecture.md"
  - "ADR files (adr-NNN-*.md)"
stepsCompleted: 0
currentStep: 1
nextStep: "step-02-stories.md"
---

# Step 1: Design System Architecture

## Step Goal

Design the complete system architecture driven by the PRD and UX spec. Document every significant technical decision as an Architecture Decision Record.

## Execution Rules

1. Activate **Winston (Architect)** agent persona.
2. Architecture must satisfy all NFRs from the PRD.
3. Every significant decision requires an ADR — minimum 2 ADRs.
4. Prefer proven patterns over novel approaches unless innovation is a stated goal.

### Context from Previous Steps

- None within this workflow — inputs are pre-existing artifacts from planning.

## Instructions

1. **Activate Winston (Architect)**: Load `agents/winston-architect.md`. Winston is principled, evidence-based, and thinks in systems.

2. **Load planning artifacts**: Read PRD.md, ux-spec.md, and project-context.md. Identify all constraints: tech stack, NFRs, infrastructure requirements, team capabilities.

3. **Create architecture.md**: Using `architecture-doc.md.tmpl`, produce:
   - **System overview**: High-level component diagram (mermaid) showing major subsystems
   - **Technology decisions**: Language, framework, database, messaging, caching — each with rationale
   - **Data model**: Entity-relationship diagram (mermaid), field definitions, relationships, indexes
   - **API design**: Endpoints, methods, request/response contracts, authentication mechanism
   - **Security architecture**: Auth flow, data encryption, input validation, OWASP considerations
   - **Infrastructure**: Deployment topology, CI/CD approach, environment strategy
   - **Integration points**: External services, third-party APIs, webhooks
   - **Scalability design**: Horizontal/vertical scaling strategy, caching layers, async processing

4. **Write ADRs**: For each major decision, create `adr-NNN-<slug>.md`:
   - **Context**: What problem or question prompted this decision
   - **Decision**: What was decided and why
   - **Alternatives considered**: What other options were evaluated
   - **Consequences**: Positive and negative implications
   - **Status**: ACCEPTED, PROPOSED, or SUPERSEDED

5. **Validate against NFRs**: Map each NFR to the architectural element that addresses it. Flag any unaddressed NFRs.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Tech stack not yet decided             | Propose options with tradeoff analysis in ADR|
| NFR conflicts with tech constraint     | Document tradeoff; escalate to user          |
| Architecture is complex (>10 services) | Recommend phased rollout; start simpler      |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] architecture.md exists with all required sections
- [ ] Component diagram is present and readable
- [ ] Data model is defined with entities and relationships
- [ ] API design covers all user-facing FRs
- [ ] At least 2 ADRs written with complete sections
- [ ] Every NFR maps to an architectural element

### Output Validation

| Output            | Validation Rule                                     | Pass/Fail |
|------------------|---------------------------------------------------|-----------|
| architecture.md  | Component diagram + data model + API design present  | ____      |
| ADR files        | Minimum 2, each with context + decision + consequences| ____    |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Architecture document is missing data model or API design
> - No ADRs written
> - NFRs are unaddressed
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If the architecture fails NFR validation:
1. Identify the unaddressed NFRs
2. Research alternative architectural patterns that address the gap
3. Write a new ADR documenting the revised decision
4. Update the architecture document — do not start a new one

## Skip Conditions

- **Skip if**: architecture.md already exists, passes NFR validation, and has at least 2 ADRs
- **Do NOT skip if**: The PRD or UX spec has been updated since the architecture was written

## Time Box

**Maximum**: 4 hours. If tech stack decisions require evaluation beyond 4 hours, create a spike story and timebox the evaluation separately.

## Step Completion Criteria

- [ ] architecture.md has all required sections (overview, components, data model, API, security)
- [ ] Component diagram is present and readable
- [ ] At least 2 ADRs with context, decision, alternatives, and consequences
- [ ] Every NFR maps to an architectural element

---

**Next step**: `step-02-stories.md`
