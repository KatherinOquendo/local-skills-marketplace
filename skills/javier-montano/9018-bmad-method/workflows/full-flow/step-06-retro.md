---
stepNumber: 6
stepName: "Sprint Retrospective"
agent: "retro-facilitator"
inputs:
  - "sprint-status.yaml"
  - "Code review reports"
  - "Previous retrospective (if exists)"
outputs:
  - "retrospective.md"
  - "Updated velocity data"
  - "Archived sprint record"
stepsCompleted: 5
currentStep: 6
nextStep: "DONE"
---

# Step 6: Sprint Retrospective

## Step Goal

Reflect on the sprint execution, capture lessons learned, define actionable improvements, and update velocity data for future sprint planning. Archive the sprint for historical reference.

## Execution Rules

1. Activate the **Retrospective Facilitator** agent persona.
2. Every action item must have an owner and a target date.
3. Review previous retro action items — were they addressed?
4. Keep the retrospective concise and action-oriented.

### Context from Previous Steps

- From Step 5: `sprint-status.yaml` — story completion data, actual effort.
- From Step 5: Code review reports — quality observations.
- Previous retrospective file (if this is not the first sprint).

## Instructions

1. **Activate Retrospective Facilitator**: Load `agents/retrospective-facilitator.md` persona. Adopt a balanced, constructive tone.

2. **Review sprint metrics**: From `sprint-status.yaml`, calculate:
   - Stories planned vs. completed
   - Stories carried over or deferred
   - Velocity (story points or count completed)
   - Blockers encountered and resolution time

3. **Collect feedback in three categories**:
   - **What went well**: Practices, tools, or patterns that worked effectively.
   - **What did not go well**: Pain points, delays, quality issues, communication gaps.
   - **What to change**: Specific, actionable changes for the next sprint.

4. **Define action items**: For each "what to change" item, create a concrete action:
   - Description of the change
   - Owner (which agent or user)
   - Target: next sprint or specific date
   - How to measure success

5. **Review previous retrospective actions**: If a previous `retrospective.md` exists, check each action item. Mark as DONE, IN-PROGRESS, or NOT-STARTED. Carry forward incomplete items.

6. **Update velocity data**: Record this sprint's velocity in a trend format (append to velocity log if it exists). Note any factors that affected velocity (learning curve, scope changes, blockers).

7. **Archive the sprint**: Move completed sprint artifacts to an archive directory (`bmad-docs/sprints/sprint-N/`). Ensure sprint-status.yaml, review reports, and retrospective are preserved.

### Decision Points

| Condition                              | Action                                        |
|---------------------------------------|-----------------------------------------------|
| First sprint (no prior retro)          | Skip previous action review, establish baseline|
| All stories completed                  | Celebrate, but still identify improvements     |
| Zero stories completed                 | Root cause analysis — identify systemic issue  |
| Unclear requirement                    | HALT and request clarification                 |

## Success Metrics

- [ ] retrospective.md exists with all three feedback categories populated
- [ ] Every "what to change" item has a corresponding action item
- [ ] Action items have owners and target dates
- [ ] Previous retro actions are reviewed (if applicable)
- [ ] Velocity data is recorded
- [ ] Sprint artifacts are archived

### Output Validation

| Output              | Validation Rule                                   | Pass/Fail |
|--------------------|--------------------------------------------------|-----------|
| retrospective.md   | Three categories + action items with owners        | ____      |
| Velocity data      | This sprint's velocity is recorded                 | ____      |
| Sprint archive     | sprint-status.yaml + retro copied to archive dir   | ____      |

## HALT Conditions

> **HALT**: Do not proceed if any of these conditions exist:
>
> - sprint-status.yaml is missing or incomplete
> - Action items have no owners
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

Retrospectives do not have a rollback procedure — they are reflective artifacts. If sprint-status.yaml was lost or corrupted before the retro:
1. Reconstruct sprint data from git history and story files
2. Note data gaps explicitly in the retrospective

## Skip Conditions

- **Skip if**: The sprint had zero stories (e.g., sprint was canceled before any work began)
- **Do NOT skip if**: Stories were attempted even if none were completed — zero-completion sprints are the most important to retrospect

## Time Box

**Maximum**: 1 hour. Keep the retrospective focused on actionable improvements, not exhaustive analysis.

## Step Completion Criteria

- [ ] retrospective.md has all three feedback categories with at least 2 items each
- [ ] Every "what to change" has an action item with owner and target date
- [ ] Previous retro actions are reviewed (if applicable)
- [ ] Velocity data recorded for trend tracking
- [ ] Sprint artifacts archived

---

**Next step**: `DONE` — Full flow complete. Start a new sprint cycle from Step 5 or begin a new feature from Step 2.
