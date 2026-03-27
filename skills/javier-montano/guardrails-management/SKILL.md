---
name: guardrails-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Detect, confirm, store, and enforce user-declared guidelines, constraints, and
  guardrails as JSON files. Pristino's internal RAG for working rules.
  Trigger: "guardrail", "guideline", "constraint", "from now on", "always use", "never use"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Guardrails Management

> "Rules you declare become rules the system enforces."

## TL;DR

Manages user-declared working rules stored as JSON in `references/guardrails/`. When the user expresses a preference ("always use TypeScript", "never use jQuery"), Pristino detects the intent, confirms with the user, and stores it. These rules are loaded at every session start and the Guardian checks compliance.

## Procedure

### Step 1: Discover
- Detect user intent to set a working rule (keywords: "always", "never", "from now on", "prefer", "avoid")
- Read existing guardrails: `references/guardrails/guidelines.json`, `constraints.json`, `guardrails.json`
- Check for duplicates or conflicts with existing rules

### Step 2: Analyze
- Classify the rule type:
  - **Constraint** (hard, "never"): stored in `constraints.json`
  - **Guideline** (default, "always"): stored in `guidelines.json`
  - **Guardrail** (soft, "prefer"): stored in `guardrails.json`
- Generate next ID: `GL-NNN` (guidelines), `CT-NNN` (constraints), `GR-NNN` (guardrails)

### Step 3: Execute
- **Confirm with user**: "I want to confirm: should I save this as a working [guideline/constraint/guardrail]? (yes/no)"
- If confirmed, append entry to the appropriate JSON file:
  ```json
  { "id": "GL-001", "rule": "...", "type": "guideline", "confirmed": "YYYY-MM-DD", "source": "user-explicit", "active": true }
  ```
- If listing: read all 3 files, display active rules grouped by type
- If removing: set `"active": false` on the specified rule

### Step 4: Validate
- JSON file is valid after write
- No duplicate rules across files
- Rule is actionable and verifiable by the Guardian
- Confirmation was received before storing

## Quality Criteria

- [ ] User confirmation received before storing any rule
- [ ] Rule stored in correct file (guideline/constraint/guardrail)
- [ ] ID is unique and sequential
- [ ] JSON is valid after write
- [ ] No duplicates across files
- [ ] Evidence tags applied

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Storing without confirmation | User didn't intend a permanent rule | Always double-confirm |
| Mixing types | "Never" rules in guidelines file | Classify by enforcement level |
| Storing unverifiable rules | Guardian can't check "make it nice" | Rules must be specific and testable |

## Related Skills

- `session-protocol` — Loads guardrails during bootstrap
- `continuous-learning` — Insights may generate new guardrails
- `code-review` — Guardian checks guardrail compliance
