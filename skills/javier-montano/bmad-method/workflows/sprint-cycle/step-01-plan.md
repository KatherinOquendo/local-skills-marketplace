---
stepNumber: 1
stepName: "Plan the Sprint"
agent: "sm"
inputs:
  - "Story backlog (from solutioning)"
  - "Velocity data (if available)"
  - "Previous sprint retro actions (if applicable)"
outputs:
  - "sprint-status.yaml"
  - "Sprint goal statement"
stepsCompleted: 0
currentStep: 1
nextStep: "step-02-develop.md"
---

# Step 1: Plan the Sprint

## Step Goal

Define a clear sprint goal, select stories from the backlog based on priority and capacity, and create the sprint tracking file.

## Execution Rules

1. Activate **Bob (Scrum Master)** agent persona.
2. Never overcommit — capacity must be realistic based on velocity data (or conservative estimate if first sprint).
3. Selected stories must have all dependencies resolved or scheduled within the sprint.
4. The sprint goal must be a single, coherent objective.

### Context from Previous Steps

- None within this workflow — inputs come from the solutioning phase.
- If this is a subsequent sprint: previous sprint-status.yaml and retrospective.

## Instructions

1. **Activate Bob (Scrum Master)**: Load `agents/bob-scrum-master.md`.

2. **Define sprint goal**: Articulate a single clear statement of what this sprint aims to achieve. The goal should be value-oriented (what the user gets), not task-oriented (what the team does).

3. **Review the backlog**: Load all story files. Sort by priority (P0 first), then by dependency order. Identify foundation stories that unblock others.

4. **Calculate capacity**: Based on velocity data from previous sprints, determine how many story points or stories can fit. If first sprint, use a conservative estimate (60-70% of total available stories as a baseline for learning).

5. **Select stories**: Pull stories into the sprint that:
   - Align with the sprint goal
   - Have all dependencies resolved (or dependencies are also in this sprint)
   - Fit within calculated capacity
   - Are fully refined (acceptance criteria complete)

6. **Create sprint-status.yaml**: Using `sprint-status.yaml.tmpl`, populate:
   - Sprint number and goal
   - Start and target end date
   - Selected stories with status (TODO)
   - Capacity allocation
   - Known risks or blockers

7. **Verify no unresolved dependencies**: For every selected story, confirm its dependencies are either DONE (from previous sprints) or also selected in this sprint.

### Decision Points

| Condition                              | Action                                       |
|---------------------------------------|----------------------------------------------|
| Backlog has unrefined stories          | Refine first; do not select unrefined stories|
| All P0 stories exceed capacity         | Negotiate scope; split stories if possible   |
| No velocity data available             | Use conservative estimate; plan for learning |
| Dependency is on external system       | Add as risk; have a contingency plan         |
| Unclear requirement                    | HALT and request clarification               |

## Success Metrics

- [ ] Sprint goal is defined as a single coherent statement
- [ ] sprint-status.yaml exists with all selected stories
- [ ] All selected stories have complete acceptance criteria
- [ ] No unresolved dependencies among selected stories
- [ ] Capacity is explicitly stated and not exceeded

### Output Validation

| Output              | Validation Rule                                  | Pass/Fail |
|--------------------|------------------------------------------------|-----------|
| sprint-status.yaml | Goal + stories + capacity defined                | ____      |
| Sprint goal        | Single statement, value-oriented                 | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - Selected stories have unresolved dependencies
> - Stories lack acceptance criteria
> - No sprint goal defined
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If sprint planning produces an infeasible plan:
1. Reduce the committed stories to match actual capacity
2. Move deferred stories back to the backlog
3. Re-validate dependency resolution for the reduced set

## Skip Conditions

- **Skip if**: sprint-status.yaml already exists for this sprint AND user confirms it is correct
- **Do NOT skip if**: Starting a new sprint — planning is always required

## Time Box

**Maximum**: 1 hour. Sprint planning that exceeds 1 hour usually means stories need further refinement.

## Step Completion Criteria

- [ ] Sprint goal is a single value-oriented statement
- [ ] sprint-status.yaml exists with selected stories
- [ ] All selected stories have complete acceptance criteria
- [ ] No unresolved dependencies among selected stories
- [ ] Committed points do not exceed calculated capacity

---

**Next step**: `step-02-develop.md`
