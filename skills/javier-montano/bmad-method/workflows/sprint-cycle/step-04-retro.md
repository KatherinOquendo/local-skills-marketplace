---
stepNumber: 4
stepName: "Sprint Retrospective"
agent: "retro-facilitator"
inputs:
  - "sprint-status.yaml"
  - "Code review reports"
  - "Previous retrospective (if exists)"
outputs:
  - "retrospective.md"
  - "Updated velocity data"
stepsCompleted: 3
currentStep: 4
nextStep: "DONE"
---

# Step 4: Sprint Retrospective

## Step Goal

Reflect on the sprint, capture what worked and what did not, define actionable improvements, and update velocity data for future planning.

## Execution Rules

1. Activate the **Retrospective Facilitator** agent persona.
2. Every action item must have an owner and a target.
3. Review previous retro actions before defining new ones.
4. Be honest about failures — they are learning opportunities.

### Context from Previous Steps

- From Step 1: Sprint goal and capacity plan.
- From Step 3: sprint-status.yaml (final), code review reports.
- Previous retrospective (if this is not the first sprint).

## Instructions

1. **Activate Retrospective Facilitator**: Load `agents/retrospective-facilitator.md`.

2. **Review sprint metrics**:
   - Stories planned vs. completed vs. carried over
   - Velocity (completed story points or count)
   - Blocker count and average resolution time
   - Review cycle count (how many stories needed re-review)

3. **Gather feedback**:
   - **What went well**: Effective practices, good tool usage, smooth handoffs, quality wins.
   - **What did not go well**: Delays, blockers, quality escapes, unclear requirements, process friction.
   - **What to change**: Concrete proposals for the next sprint.

4. **Define action items**: For each "what to change" proposal:
   - Clear description of the change
   - Owner (agent persona or user)
   - Target: next sprint or specific milestone
   - Success measure: how will we know it worked?

5. **Review previous retro actions** (if applicable): Load the previous retrospective. For each action item, determine:
   - DONE: completed and effective
   - IN-PROGRESS: started but not finished
   - NOT-STARTED: was not addressed
   - Carry forward any IN-PROGRESS or NOT-STARTED items

6. **Update velocity data**: Record this sprint's velocity. If a velocity log exists, append to it. Note factors that affected velocity (new team member ramp-up, infrastructure issues, scope changes).

7. **Present retrospective**: Share findings with user. Confirm action items are understood and accepted.

### Decision Points

| Condition                              | Action                                        |
|---------------------------------------|-----------------------------------------------|
| First sprint (no prior retro)          | Skip step 5; establish baseline velocity      |
| Sprint had zero completions            | Focus on root cause analysis                  |
| Too many action items (> 5)            | Prioritize top 3; defer the rest              |
| Unclear requirement                    | HALT and request clarification                |

## Success Metrics

- [ ] retrospective.md exists with all three feedback categories
- [ ] Every "what to change" has a corresponding action item
- [ ] Action items have owners and targets
- [ ] Previous retro actions reviewed (if applicable)
- [ ] Velocity data recorded

### Output Validation

| Output              | Validation Rule                                   | Pass/Fail |
|--------------------|--------------------------------------------------|-----------|
| retrospective.md   | Three categories populated + action items defined  | ____      |
| Velocity data      | Sprint velocity recorded with trend context        | ____      |

## HALT Conditions

> **HALT**: Do not proceed if any of these conditions exist:
>
> - sprint-status.yaml is missing or incomplete
> - Action items lack owners
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

Retrospectives are reflective and have no rollback. If sprint data is incomplete:
1. Reconstruct from git log and story file statuses
2. Note any data gaps explicitly in the retrospective

## Skip Conditions

- **Skip if**: Sprint was canceled with zero stories attempted
- **Do NOT skip if**: Even one story was worked on — partial sprints need retrospection

## Time Box

**Maximum**: 45 minutes. Retrospectives that run long lose focus. Prioritize the top 3 action items.

## Step Completion Criteria

- [ ] retrospective.md has all three feedback categories populated
- [ ] Every "what to change" has an action item with owner and deadline
- [ ] Previous retro actions reviewed (if applicable)
- [ ] Velocity data recorded
- [ ] User has acknowledged the action items

---

**Next step**: `DONE` — Sprint cycle complete. Begin next sprint from step-01-plan.md.
