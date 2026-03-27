---
name: changelog-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Maintain changelog.md with semantic entries for decisions, completions, amendments,
  insights, blockers, and discoveries. Cross-session continuity log.
  Trigger: "changelog", "log decision", "record change", "what happened", "session log"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Changelog Management

> "If it's not logged, it didn't happen."

## TL;DR

Maintains `changelog.md` as the cross-session continuity log. Records significant decisions, completions, amendments, insights, blockers, and discoveries with date, type, description, rationale, and constitutional principle references. Read during session protocol (Step 2: State Recovery) to understand what happened in recent sessions.

## Procedure

### Step 1: Discover
- Read existing `changelog.md` (or create if missing)
- Identify the event to log (decision, completion, amendment, etc.)
- Determine which constitutional principles are involved

### Step 2: Analyze
- Classify event type: `decision`, `completion`, `amendment`, `insight`, `blocker`, `discovery`
- Draft description (concise, actionable)
- Identify rationale (why this matters)
- Map to constitutional principles

### Step 3: Execute
- Append entry to `changelog.md` under today's date:
  ```markdown
  ## 2026-03-23
  - **[decision]**: Selected strip-over-escape for input sanitization — simpler, covers primary vector (copy-paste) [Principle VII, XIV]
  - **[completion]**: Firebase Auth integration complete — email + Google social login [Principle I, VII]
  - **[insight]**: Audit log paths must be fully qualified for recovery — captured in insights/security.md [Principle VII]
  ```
- If no section for today exists, create it
- Keep entries chronological (newest date at top)

### Step 4: Validate
- Entry includes date, type, description, rationale, principles
- No duplicate entries for the same event
- Changelog is readable by someone with zero context (self-sufficient entries)
- Recent entries (last 5) are loadable during session protocol

## Quality Criteria

- [ ] Entry has correct type tag
- [ ] Description is concise and self-sufficient
- [ ] Constitutional principles referenced
- [ ] Date is correct
- [ ] No duplicates
- [ ] Evidence tags applied

## Related Skills

- `session-protocol` — Reads changelog during state recovery
- `tasklog-management` — Complementary log for task tracking
- `continuous-learning` — Insights logged here and in insights/
