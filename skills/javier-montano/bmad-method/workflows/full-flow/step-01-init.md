---
stepNumber: 1
stepName: "Initialize Project"
agent: "orchestrator"
inputs:
  - "User request or project name"
  - "Project type indicator (greenfield/brownfield)"
outputs:
  - "project-context.md"
  - "Initialized project directory structure"
stepsCompleted: 0
currentStep: 1
nextStep: "step-02-analyze.md"
---

# Step 1: Initialize Project

## Step Goal

Initialize the BMAD project workspace and assess readiness for the full development lifecycle. Produce a populated `project-context.md` that anchors all subsequent phases.

## Execution Rules

1. Never skip the project-type assessment — greenfield and brownfield follow different paths.
2. All outputs must be written to disk before proceeding; no in-memory-only state.
3. If any required tool (Bash, Write) is unavailable, HALT immediately.

### Context from Previous Steps

- None — this is the first step.

## Instructions

1. **Check for existing project**: Run `ls` on the target directory. If a `project-context.md` already exists, load it and confirm with the user whether to reset or resume.

2. **Run the init script**: Execute `python ${CLAUDE_SKILL_DIR}/scripts/init_project.py <project-name>` with the appropriate flag (`--greenfield` or `--brownfield`). Capture stdout for the scaffold report.

3. **Create project-context.md**: Using the `project-context.md.tmpl` template, populate all required fields:
   - Project name, description, and goal statement
   - Technology stack (language, framework, database, infrastructure)
   - Coding conventions and naming patterns
   - Repository structure overview
   - Known constraints and assumptions

4. **Identify project type**: Determine whether the project is greenfield (no existing code) or brownfield (existing codebase). For brownfield, run a preliminary code scan to document existing patterns, dependencies, and tech debt indicators.

5. **Validate initialization**: Confirm that the directory structure was created, `project-context.md` exists and is non-empty, and the project type is explicitly recorded.

6. **Summarize readiness**: Produce a short readiness statement listing what is confirmed and what remains unknown. Flag any items that require user input before Phase 1 can begin.

### Decision Points

| Condition                              | Action                                    |
|---------------------------------------|-------------------------------------------|
| Project directory already exists       | Ask user: reset or resume                 |
| User has not specified tech stack      | Prompt for minimum viable tech decisions  |
| Brownfield with no readable codebase   | HALT — cannot proceed without code access |
| Unclear requirement                    | HALT and request clarification            |

## Success Metrics

- [ ] `project-context.md` exists on disk with all required sections populated
- [ ] Project type (greenfield/brownfield) is explicitly recorded
- [ ] Directory scaffold matches BMAD standard structure
- [ ] No placeholder values remain in project-context.md (all `{{ }}` resolved)

### Output Validation

| Output                        | Validation Rule                                | Pass/Fail |
|------------------------------|-----------------------------------------------|-----------|
| project-context.md           | File exists AND all required sections present  | ____      |
| Directory structure          | Contains bmad-docs/ with expected subdirs      | ____      |

## HALT Conditions

> **HALT**: Do not proceed to the next step if any of these conditions exist:
>
> - The init script failed or produced errors
> - project-context.md is missing or has unresolved placeholders
> - The user has not confirmed the project type
> - Any success metric above is marked FAIL

**On HALT**: Notify the user with the halt reason and all context gathered so far.

## Rollback Procedure

If this step fails after partial execution:
1. Delete the partially created project directory (`rm -rf <project-name>/`)
2. Fix the issue (invalid name, missing tool, disk space)
3. Re-run from the beginning — this step is idempotent when starting clean

## Skip Conditions

- **Skip if**: A valid `project-context.md` already exists and the user wants to resume an existing project (confirm with user first)
- **Do NOT skip if**: The project directory exists but `project-context.md` is missing or contains only placeholders

## Time Box

**Maximum**: 30 minutes. If the user cannot provide minimum project context (name, type, basic tech stack) within 30 minutes, HALT and schedule a follow-up session.

## Step Completion Criteria

- [ ] `project-context.md` exists with all required sections filled
- [ ] Project type is recorded in both `project-context.md` and `config.yaml`
- [ ] Directory scaffold passes `validate_project.py` directory checks
- [ ] User has confirmed the project context is accurate

---

**Next step**: `step-02-analyze.md`
