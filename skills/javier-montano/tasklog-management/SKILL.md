---
name: tasklog-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Maintain tasklog.md for cross-session task tracking. Track status, owner, age,
  blockers. Flag stale items. Bridge to workspace/tasks/.
  Trigger: "tasklog", "track task", "open tasks", "task status", "pending items"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Tasklog Management

> "Open tasks that never close become invisible technical debt."

## TL;DR

Maintains `tasklog.md` as the cross-session task tracking system. Each item has ID, description, status, owner, opened date, and notes. Items >14 days without progress are flagged for review. Completed items retained 30 days then archived. Task bridges connect to `workspace/tasks/TL-XXX-<slug>/` for working files.

## Procedure

### Step 1: Discover
- Read existing `tasklog.md` (or create if missing)
- Identify the operation: add task, update status, close, flag stale

### Step 2: Analyze
- For new tasks: assign ID (TL-NNN), classify status, identify owner
- For updates: determine new status (open → in-progress → blocked/completed/deferred)
- For staleness review: calculate age of each open item, flag >14 days

### Step 3: Execute
- **Add task**:
  ```markdown
  | TL-015 | Implement offline cache for program catalog | open | agent | 2026-03-23 | Blocked by Principle VIII design |
  ```
- **Update status**: change status column, add notes
- **Close task**: move to `## Completed` section with completion date
- **Flag stale**: add `⚠️ STALE` prefix to items >14 days without progress
- **Create task bridge**: `workspace/tasks/TL-015-offline-cache/README.md`

### Step 4: Validate
- All open items have correct status and owner
- No items >14 days without review
- Completed items in `## Completed` section
- Task bridges exist for items needing working files
- Tasklog is readable during session protocol

## Quality Criteria

- [ ] ID format consistent (TL-NNN)
- [ ] Status is one of: open, in-progress, blocked, deferred, completed
- [ ] Items >14 days flagged
- [ ] Completed items in separate section
- [ ] Task bridges created in workspace/tasks/

## Related Skills

- `session-protocol` — Reviews tasklog during pending closure
- `changelog-management` — Complementary log for decisions
- `workspace-governance` — Task bridges live in workspace/tasks/
