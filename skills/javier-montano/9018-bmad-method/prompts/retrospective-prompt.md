# Sprint Retrospective

## Pre-conditions

- Sprint is complete (all stories are DONE, BLOCKED, or explicitly deferred)
- sprint-status.yaml has final statuses for all stories
- Code review reports are available for quality observations
- Previous retrospective is accessible (if not the first sprint)

## Post-conditions

- `retrospective.md` exists with all three feedback categories and action items
- Every action item has an owner, target date, and success measure
- Previous retro actions are reviewed with status updates
- Velocity data is recorded for trend tracking
- Sprint artifacts are archived

## Failure Signals

- Sprint-status.yaml is missing or has stories with ambiguous statuses
- Team cannot identify any "what went well" or "what did not go well" items
- Action items from the previous retro were all NOT-STARTED (systemic follow-through issue)
- Velocity is declining for 3+ consecutive sprints (escalate to user)

## Purpose

This prompt triggers a sprint retrospective after all stories have been reviewed and the sprint is complete. Use it at the end of every sprint cycle.

## Setup Instructions

1. **Activate Retrospective Facilitator**: Load `agents/retrospective-facilitator.md`.

2. **Load retrospective context**:
   - `sprint-status.yaml` — final sprint status with all story outcomes
   - Code review reports — quality observations from Quinn
   - Previous `retrospective.md` (if this is not the first sprint)
   - Velocity log (if exists)

## Retrospective Process

### Step 1: Review Sprint Metrics

Calculate and record:

| Metric | Value |
|--------|-------|
| Stories planned | [count] |
| Stories completed (DONE) | [count] |
| Stories carried over | [count] |
| Stories blocked | [count] |
| Velocity (points or count) | [value] |
| Review cycles (avg per story) | [value] |
| Blockers encountered | [count] |

Compare to previous sprint (if available). Note trends: improving, stable, or declining.

### Step 2: What Went Well

Identify practices, tools, patterns, or behaviors that contributed positively:

- What helped the team move faster?
- What produced higher quality output?
- What communication or handoff patterns worked smoothly?
- What tools or processes reduced friction?

Document at least 2 items. These are practices to continue and reinforce.

### Step 3: What Did Not Go Well

Identify pain points, delays, quality issues, or process failures:

- What caused delays or blockers?
- Where did quality escape (bugs found in review)?
- What communication gaps occurred between agents?
- What processes felt wasteful or redundant?
- What assumptions proved wrong?

Document at least 2 items. Be specific — "things were slow" is not actionable; "story estimation was consistently too optimistic by 50%" is.

### Step 4: What to Change

For each "did not go well" item, propose a concrete change:

- What specific action will address the issue?
- Who owns this action (which agent or the user)?
- When should it be implemented (next sprint, specific date)?
- How will we know it worked (success measure)?

Format each as an action item:

```
- **Action**: [description]
  **Owner**: [agent/user]
  **Target**: [next sprint / date]
  **Measure**: [how to verify success]
```

### Step 5: Review Previous Retro Actions

If a previous retrospective exists, review each action item:

| Action | Owner | Status | Notes |
|--------|-------|--------|-------|
| [description] | [owner] | DONE / IN-PROGRESS / NOT-STARTED | [notes] |

- **DONE**: Celebrate. Did it have the intended effect?
- **IN-PROGRESS**: Carry forward. Is the timeline still realistic?
- **NOT-STARTED**: Why not? Re-prioritize or remove if no longer relevant.

### Step 6: Update Velocity Trend

Append this sprint's velocity to the velocity log:

```
Sprint N: [velocity] — [factors affecting velocity]
```

Note any factors that make this sprint non-representative (learning curve, scope changes, infrastructure issues, holidays).

### Step 7: Archive Sprint

Ensure the following are preserved:
- sprint-status.yaml (final version)
- All code review reports
- retrospective.md
- Move to archive: `bmad-docs/sprints/sprint-N/`

## Output

Produce `retrospective.md` with all sections above populated. Present the summary and action items to the user for acknowledgment before closing the sprint.
