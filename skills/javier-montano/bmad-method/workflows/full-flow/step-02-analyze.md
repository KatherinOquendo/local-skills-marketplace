---
stepNumber: 2
stepName: "Analyze Problem Space"
agent: "analyst"
inputs:
  - "project-context.md"
  - "User's problem statement or idea"
outputs:
  - "product-brief.md"
  - "Research notes (if applicable)"
stepsCompleted: 1
currentStep: 2
nextStep: "step-03-plan.md"
---

# Step 2: Analyze Problem Space

## Step Goal

Explore the problem space thoroughly and produce a validated `product-brief.md` that captures the vision, target users, core value proposition, and key risks. This artifact becomes the foundation for all planning decisions.

## Execution Rules

1. Activate the **Mary (Analyst)** agent persona before beginning analysis.
2. Every claim in the product brief must carry an evidence tag: `[RESEARCH]`, `[USER-INPUT]`, `[INFERENCIA]`, or `[SUPUESTO]`.
3. Do not prescribe solutions — this phase is about the problem, not the implementation.

### Context from Previous Steps

- From Step 1: `project-context.md` — project name, type, tech stack, constraints.

## Instructions

1. **Activate Mary (Analyst)**: Load `agents/mary-analyst.md` persona. Adopt the analyst mindset — curious, evidence-driven, assumption-challenging.

2. **Conduct brainstorming (if greenfield)**: If the user has only a rough idea, facilitate a structured brainstorming session. Ask the 5 essential questions: Who is the user? What problem do they face? Why now? What alternatives exist? What would success look like?

3. **Perform research**: If the domain is unfamiliar, use WebSearch and WebFetch to gather market context, competitor analysis, and domain knowledge. Document sources with URLs and dates.

4. **Synthesize the product brief**: Create `product-brief.md` covering:
   - Vision statement (1-2 sentences)
   - Target audience and user personas
   - Problem statement with evidence
   - Proposed value proposition
   - Key assumptions and risks
   - Success criteria (measurable)
   - Scope boundaries (what is explicitly OUT)

5. **Validate with evidence tags**: Review every statement in the brief. Tag each with its evidence source. Flag any `[SUPUESTO]` (assumption) items as requiring future validation.

6. **Present to user for review**: Summarize the brief's key points and ask the user to confirm or correct before proceeding to planning.

### Decision Points

| Condition                              | Action                                      |
|---------------------------------------|---------------------------------------------|
| User provides detailed requirements    | Skip brainstorming, go to synthesis          |
| Domain is highly specialized           | Recommend domain expert review before moving |
| More than 5 unvalidated assumptions    | Flag risk — consider additional research     |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] `product-brief.md` exists with all required sections
- [ ] Every claim has an evidence tag
- [ ] At least one measurable success criterion is defined
- [ ] User has reviewed and approved the brief
- [ ] Scope boundaries are explicitly stated

### Output Validation

| Output              | Validation Rule                                  | Pass/Fail |
|--------------------|------------------------------------------------|-----------|
| product-brief.md   | All sections present AND evidence tags on claims | ____      |
| Research notes     | Sources cited with URLs (if research performed)  | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - The product brief has no measurable success criteria
> - The user has not reviewed the brief
> - The problem statement is vague or contradictory
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If this step produces an unsatisfactory product brief:
1. Archive the current `product-brief.md` as `product-brief.v1.md`
2. Re-run the analysis with revised user input or additional research
3. Do not delete research notes — they remain valuable context

## Skip Conditions

- **Skip if**: A validated `product-brief.md` already exists from a previous session AND the user confirms no scope changes since it was written
- **Do NOT skip if**: The project scope has changed since the existing brief was written

## Time Box

**Maximum**: 2 hours. If brainstorming and research have not converged into a clear problem statement within 2 hours, HALT and escalate to the user for direction.

## Step Completion Criteria

- [ ] `product-brief.md` exists with vision, problem, personas, and success metrics
- [ ] Every claim has an evidence tag (`[RESEARCH]`, `[USER-INPUT]`, `[SUPUESTO]`)
- [ ] At least 1 measurable success criterion defined
- [ ] User has explicitly approved the brief

---

**Next step**: `step-03-plan.md`
