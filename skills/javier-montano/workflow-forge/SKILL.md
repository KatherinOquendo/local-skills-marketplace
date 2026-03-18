---
name: workflow-forge
description: >
  Creates, validates, and optimizes step-by-step automation workflows with turbo annotations, safety gates, callgraph analysis, and sub-workflow orchestration.
  Use when the user asks to "build a workflow", "lint a workflow", "optimize workflow steps",
  "add turbo annotations", or mentions workflow forge, workflow validation, or callgraph analysis.
argument-hint: "<workflow description or path> [--mode create|lint|optimize] [--callgraph]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Workflow Forge

A workflow is a recipe: a sequence of atomic steps that turns a trigger into a verified result. Good workflows are deterministic (same input, same output), safe (destructive actions require confirmation), and short (10 steps max).

## Workflow Structure

```markdown
---
description: Creates a new React component with tests and styles
---
# create-component

## Prerequisites
- Project uses React with TypeScript
- CSS modules enabled

## Steps

### 1. Gather requirements
Ask the user: component name, props, whether it needs state.

### 2. Create component directory  // turbo
mkdir -p src/components/{name}

### 3. Generate component file  // turbo
Create src/components/{name}/{name}.tsx with boilerplate.

### 4. Verify
- [ ] Component renders without errors
- [ ] All files created in correct location
- [ ] Naming follows project conventions
```

## Creation Protocol

### Step 1: Identify the Trigger

What kicks off this workflow? A slash command, a user request, or an event. The trigger determines invocation method.

### Step 2: Break into Atomic Steps

Each step does exactly one thing. The test: can you explain it in one sentence without "and"?

| Atomic (Good) | Non-Atomic (Bad) |
|---------------|-----------------|
| "Run the linter" | "Analyze the code and fix the bugs" |
| "Create the directory" | "Set up the project and install deps" |
| "Read the config file" | "Check if config exists and create if not" |

If a step has "and" in it, split it.

### Step 3: Apply Safety Annotations

Mark steps as `// turbo` (safe to auto-execute) or leave unmarked (requires user review).

**Safe for turbo:**
- Read-only: `ls`, `cat`, `git status`, `git diff`, `npm test`
- Easily reversible: `mkdir`, creating new files
- Non-destructive: `read_file`, `list_dir`

**Never turbo:**
- Irreversible: `rm -rf`, `git push --force`, `DROP DATABASE`
- External side effects: API calls, sending emails
- Overwriting existing files
- Anything involving credentials or secrets

**Trade-off:** When in doubt, don't turbo. Better to ask once than destroy work once.

### Step 4: Add Verification

Last step always verifies the workflow produced expected results. Include a remediation path: "If X fails, do Y."

### Step 5: Validate

```bash
python tools/workflow-linter.py path/to/workflow.md
```

## Handling Complex Workflows (>10 Steps)

Do not add more steps. Instead:

1. Identify natural phase boundaries (setup, execution, verification).
2. Extract each phase into its own sub-workflow.
3. Create a parent workflow that calls sub-workflows in sequence.

```
parent-workflow.md
  → calls: setup-environment.md  (steps 1-4)
  → calls: execute-migration.md  (steps 1-5)
  → calls: verify-migration.md   (steps 1-3)
```

Each sub-workflow must be independently useful and testable.

Visualize dependencies:
```bash
python tools/workflow-callgraph.py path/to/workflows/
```

## Orchestration Patterns

### Linear Pipeline
```
step-1 → step-2 → step-3 → verify
```
Most common. Each step feeds the next.

### Fan-Out / Fan-In
```
step-1 → step-2a ─┐
       → step-2b ─┼→ step-3 (merge) → verify
       → step-2c ─┘
```
Parallel steps that converge. Use when steps are independent.

### Conditional Branch
```
step-1 → condition? → YES → step-2a → verify
                    → NO  → step-2b → verify
```
Avoid when possible. Prefer separate workflows for each branch. If unavoidable, document both paths clearly.

For multi-skill orchestration patterns, read `reference/orchestration.md`.

## Quality Checklist

- [ ] 10 steps or fewer (split into sub-workflows if more)
- [ ] Each step is atomic (one action, one sentence)
- [ ] Turbo annotations are correct (only safe, reversible actions)
- [ ] Step 1 loads context (reads required references or configs)
- [ ] Last step is verification with remediation path
- [ ] Description in frontmatter is action-oriented (what, not how)
- [ ] Prerequisites list all requirements
- [ ] No step silently fails (errors are caught or propagated)

## Assumptions & Limits

- Workflows describe procedures, not implement them. The workflow tells Claude what to do; Claude executes it.
- Turbo annotations are trust markers for the user. Marking something turbo when it's not safe erodes trust permanently.
- Sub-workflow calls assume the sub-workflow exists. Always verify references before delivery.
- Workflows are linear by design. If you need complex branching or loops, you're building a program, not a workflow. Consider a script instead.
- 10-step limit is a heuristic, not a law. But workflows that exceed it are almost always decomposable.

## Edge Cases

- **Workflow step depends on external service availability:** Add a health-check step before the dependent step. Include timeout and fallback.
- **User wants a workflow that modifies the workflow itself (meta-workflow):** Valid but fragile. Document the self-modification clearly and add extra verification.
- **Multi-skill orchestration:** Load each skill's context in Step 1. Note which skill each step depends on.
- **Workflow for a one-time task:** Still worth creating if it's complex enough to get wrong. Prefix description with "One-time:" for clarity.
- **Steps that need user input mid-workflow:** These steps cannot be turbo. Mark them clearly and specify what input is needed.
- **Platform-specific commands:** Note the platform requirement in Prerequisites (e.g., "Requires macOS" or "Requires Node 18+").

## Validation Gate

Before delivering a workflow, confirm:

- [ ] Step count is 10 or fewer (or decomposed into sub-workflows)
- [ ] Every turbo-annotated step is genuinely safe and reversible
- [ ] No destructive operation is marked turbo
- [ ] Final step includes verification with pass/fail criteria
- [ ] Frontmatter has a description
- [ ] All referenced sub-workflows or skills exist
- [ ] Prerequisites are complete (nothing assumed that isn't stated)
- [ ] Remediation paths exist for steps that can fail

## Output Location

Workflows are saved to the project's workflow directory (typically `.agent/workflows/` or `workflows/`).

## Reference Files

- `reference/output-template.md` — Complete workflow template with all sections
- `reference/self-evaluation.md` — Quality rubric for grading workflows
- `reference/orchestration.md` — Patterns for multi-skill workflow coordination

---
**Author:** Javier Montano | **Last updated:** 2026-03-12
