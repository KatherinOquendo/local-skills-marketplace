# Workflow Self-Evaluation Rubric

Run through this checklist after creating a workflow. Every item should pass.

## Structure (4 items)

- [ ] **Frontmatter**: Has `description` with action-oriented summary
- [ ] **Steps numbered**: All steps are numbered sequentially
- [ ] **Step 1 is context**: First step loads/verifies required context
- [ ] **Last step is verification**: Final step confirms success with specific checks

## Safety (3 items)

- [ ] **Turbo correct**: Only safe, reversible actions have `// turbo`
- [ ] **No dangerous turbo**: Destructive commands (rm, push --force, DROP, truncate) are NOT marked turbo
- [ ] **Remediation exists**: Steps that can fail have "If FAIL →" recovery instructions

## Quality (3 items)

- [ ] **Atomic steps**: Each step does ONE thing (no "and" in the description)
- [ ] **10 steps max**: Workflow has 10 or fewer steps (split into sub-workflows if more)
- [ ] **Commands are real**: All referenced tools, commands, and paths actually exist

## Red Flags (automatic fail)

| Red Flag | Action |
|---|---|
| Step says "analyze and fix" or uses "and" | Split into two steps |
| More than 10 steps | Extract sub-workflows |
| `rm`, `push --force`, `DROP` marked as turbo | Remove turbo annotation |
| No verification step | Add one |
| Vague step like "do the task" | Rewrite with specific action and tool |

## Grading

| Score | Verdict |
|---|---|
| 10/10 | Ready to use |
| 8-9/10 | Minor fixes — address gaps |
| 6-7/10 | Structural issues — likely needs step splitting or safety review |
| Below 6 | Rethink the workflow design |
