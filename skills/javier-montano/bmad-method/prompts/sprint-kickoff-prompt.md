# Sprint Planning Kickoff

## Pre-conditions

- Implementation readiness gate has passed (PASS or accepted CONCERNS)
- Story backlog exists with estimated and refined stories
- If not the first sprint: previous sprint-status.yaml is closed and retrospective is complete

## Post-conditions

- `sprint-status.yaml` exists with sprint goal, selected stories, and capacity
- All selected stories have complete acceptance criteria
- No unresolved dependencies among selected stories
- User has approved the sprint plan

## Failure Signals

- No stories are ready for selection (all lack acceptance criteria or have unresolved dependencies)
- Committed points exceed calculated capacity by more than 10%
- Sprint goal cannot be stated as a single value-oriented sentence
- Multiple P0 stories are deferred due to capacity constraints

## Purpose

This prompt initiates sprint planning at the beginning of each sprint cycle. Use it when starting the first sprint after the gate passes, or when beginning any subsequent sprint.

## Setup Instructions

1. **Activate Bob (Scrum Master)**: Load `agents/bob-scrum-master.md`.

2. **Load required context**:
   - All story files (the product backlog)
   - Dependency map
   - Previous `sprint-status.yaml` (if this is not the first sprint)
   - Previous `retrospective.md` (if exists — check for action items)
   - Velocity data from past sprints (if available)

## Sprint Planning Steps

### 1. Define the Sprint Goal

Write a single statement that describes what value this sprint delivers. The goal should answer: "At the end of this sprint, users (or the system) will be able to ____."

Format: A value-oriented statement, not a task list.
- Good: "Users will be able to register and log in to their accounts."
- Bad: "Implement auth endpoints, create user table, build login form."

### 2. Review the Backlog

Sort available stories by:
1. Priority (P0 > P1 > P2)
2. Dependency order (foundation stories first)
3. Sprint goal alignment

Identify which stories directly contribute to the sprint goal. These are primary candidates.

### 3. Calculate Capacity

- **If velocity data exists**: Use average velocity from last 3 sprints. Apply 80% factor for buffer.
- **If first sprint**: Use a conservative estimate — select 60-70% of what seems possible. The first sprint establishes the baseline.
- **Factor in**: Retro action items that consume capacity, known holidays or interruptions.

### 4. Select Stories

Pull stories into the sprint that:
- [ ] Align with the sprint goal
- [ ] Have all dependencies resolved (done in previous sprints) or also selected in this sprint
- [ ] Fit within calculated capacity
- [ ] Are fully refined (acceptance criteria exist)
- [ ] Have estimations (S/M/L)

Do NOT select:
- Stories with unresolved external dependencies
- Stories missing acceptance criteria
- Stories that exceed remaining capacity

### 5. Create sprint-status.yaml

Use the `sprint-status.yaml.tmpl` template. Populate:
- Sprint number (sequential)
- Sprint goal
- Start date and target end date
- Selected stories with initial status: TODO
- Capacity allocation
- Known risks or blockers

### 6. Verify No Unresolved Dependencies

For every selected story, trace its dependencies:
- Dependency is DONE from a previous sprint: OK
- Dependency is also selected in this sprint and sequenced before: OK
- Dependency is NOT done and NOT selected: REJECT the story or add the dependency

### 7. Communicate the Plan

Present the sprint plan to the user:
- Sprint goal
- Story count and estimated effort
- Any risks or dependencies to watch
- Get explicit approval before beginning development

## Post-Planning

Once approved, proceed to development:
- Load `prompts/story-refinement-prompt.md` if any story needs last-minute grooming
- Begin implementation with the first story in dependency order
