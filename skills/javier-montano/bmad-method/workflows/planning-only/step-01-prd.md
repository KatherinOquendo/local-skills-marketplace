---
stepNumber: 1
stepName: "Create Product Requirements Document"
agent: "pm"
inputs:
  - "project-context.md (if exists)"
  - "Product brief or user requirements"
outputs:
  - "PRD.md"
stepsCompleted: 0
currentStep: 1
nextStep: "step-02-ux.md"
---

# Step 1: Create Product Requirements Document

## Step Goal

Produce a comprehensive Product Requirements Document that fully defines what needs to be built, for whom, and how success will be measured.

## Execution Rules

1. Activate **John (PM)** agent persona.
2. If no product brief exists, gather requirements directly from the user before writing.
3. Every functional requirement must have a unique ID and acceptance criteria.
4. Do not include implementation details — focus on the WHAT, not the HOW.

### Context from Previous Steps

- None — this is the first step. Load project-context.md if available.

## Instructions

1. **Activate John (PM)**: Load `agents/john-pm.md`. Adopt the product manager mindset — user-focused, metrics-driven, scope-aware.

2. **Load context**: Read `project-context.md` if it exists. If not, gather minimum context from the user: project name, target users, high-level goal.

3. **Gather requirements**: If a product brief exists, use it as input. Otherwise, conduct a requirements gathering session:
   - Who are the target users?
   - What problems are we solving?
   - What does success look like (metrics)?
   - What is out of scope?

4. **Create PRD.md**: Using `prd.md.tmpl`, populate:
   - Executive summary
   - Target audience and personas
   - Functional requirements (FR-001, FR-002, ...) each with acceptance criteria
   - Non-functional requirements (performance, security, accessibility, reliability)
   - Success metrics (SMART format)
   - Assumptions and dependencies
   - Out-of-scope items
   - Open questions (to be resolved before solutioning)

5. **Validate completeness**: Run through the checklist:
   - Every user persona has at least one FR
   - Every FR has acceptance criteria
   - NFRs cover performance, security, and accessibility
   - At least one SMART metric exists
   - Open questions are explicitly listed

6. **Present for review**: Share the PRD summary with the user and get approval.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| No product brief and user is vague     | Run structured Q&A before writing PRD        |
| Requirements are conflicting           | Document conflicts, ask user to prioritize   |
| Scope is extremely large               | Recommend MVP scoping with phased roadmap    |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] PRD.md exists with all required sections
- [ ] Every FR has a unique ID and acceptance criteria
- [ ] NFRs cover performance, security, accessibility
- [ ] At least one SMART success metric defined
- [ ] User has reviewed and approved

### Output Validation

| Output   | Validation Rule                                    | Pass/Fail |
|---------|--------------------------------------------------|-----------|
| PRD.md  | All FRs have IDs + acceptance criteria + NFRs exist | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - FRs lack acceptance criteria
> - No NFRs defined
> - User has not reviewed the PRD
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If the PRD is rejected during review:
1. Capture the specific feedback from the reviewer
2. Archive the current version as `PRD.v1.md`
3. Address feedback and produce a new version
4. Re-submit for review — do not skip the review step

## Skip Conditions

- **Skip if**: A validated PRD.md already exists and passes `validate_prd.py` checks AND user confirms no scope changes
- **Do NOT skip if**: The product brief was updated since the PRD was written

## Time Box

**Maximum**: 3 hours. If requirements gathering exceeds 3 hours, schedule a separate requirements workshop.

## Step Completion Criteria

- [ ] PRD.md exists with all required sections populated
- [ ] Every FR has a unique ID (FR-NNN) and acceptance criteria
- [ ] NFRs cover performance, security, and accessibility
- [ ] At least one SMART success metric defined
- [ ] User has reviewed and approved the PRD

---

**Next step**: `step-02-ux.md`
