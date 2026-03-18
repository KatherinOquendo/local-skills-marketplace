# Optimize Workflow

Workflow for analyzing an existing workflow, identifying inefficiencies, and applying optimizations while maintaining safety and clarity.

## Frontmatter

description: Analyze a workflow for performance, safety, and clarity; optimize and re-validate

## Steps

1. **Read existing workflow file**
   - Load target workflow: `<workflow-name>.md`
   - Extract frontmatter (description, expected inputs/outputs)
   - Count steps and identify structure (linear, branching, loops)
   - Verify: frontmatter is complete, steps are numbered
   - If FAIL → Report missing frontmatter or malformed structure

2. **Run workflow-linter.py for structural validation**
   - Execute: `python workflow-linter.py <workflow-name>.md --report linter.json`
   - Capture: structural violations (unnumbered steps, vague actions, missing verification)
   - Report: "5 warnings found: 3 steps lack 'If FAIL' recovery, 1 step says 'and', 1 missing verification"
   - If FAIL → Show linter output; review with user

3. **Run workflow-callgraph.py for dependency analysis**
   - Execute: `python workflow-callgraph.py <workflow-name>.md --graph dependencies.dot`
   - Visualize: which steps depend on outputs from previous steps
   - Identify: sequential bottlenecks, independent steps that could run in parallel
   - Report: "Step 3 depends on Step 2 output; Steps 5-6 could run in parallel"
   - If FAIL → Report tool errors; check that dependencies are documented

4. **Check against self-evaluation.md rubric**
   - Run 10-item checklist: Structure (4), Safety (3), Quality (3)
   - Score current workflow (e.g., 7/10)
   - Identify failing items: multiple actions per step, >10 steps, missing verification, turbo on dangerous commands
   - If FAIL → Report score and gaps

5. **Identify optimization targets**
   - List redundancies: repeated steps, unnecessary sub-steps, redundant verification
   - List missing verifications: steps that can fail without recovery instructions
   - List unbounded loops: steps that could repeat indefinitely
   - List parallelization opportunities: independent steps marked as sequential
   - Example report: "3 redundant verifications, 2 steps with 'and', 1 missing recovery instruction"

6. **Apply optimizations**
   - Merge redundant steps: combine similar actions into single step
   - Split compound steps: separate "step and then verify" into two steps
   - Add turbo annotations: mark safe, reversible actions as // turbo
   - Add verification steps: add "If FAIL → recover" to steps that can fail
   - Reorder steps: move independent steps that can run in parallel
   - Document: before state, optimization applied, expected benefit
   - If FAIL → Ask user to review proposed changes before applying

7. **Re-lint the optimized workflow**
   - Run workflow-linter.py again on updated file
   - Expected: linter violations reduced or eliminated
   - Check: all steps are numbered, have clear actions, include verification/recovery
   - If FAIL → Review new linter output; iterate with user

8. **Re-evaluate against self-evaluation.md rubric**
   - Run 10-item checklist on optimized version
   - Expected: score ≥ 8/10 (improvement from initial score)
   - Verify: no red flags, all checks pass
   - If FAIL → Apply additional fixes; re-evaluate

9. **Deliver optimized workflow with before/after comparison** // turbo
   - Save optimized version: `cp <workflow-optimized>.md <workflow-final>.md`
   - Generate comparison report: initial score vs. final score, optimizations applied
   - Example: "Reduced from 12 steps to 9 steps | +1 turbo annotations | +2 recovery instructions | Score: 7/10 → 10/10"
   - If FAIL → Report file errors; verify permissions

10. **Final verification: workflow ready for use**
    - Confirm: all steps are atomic (no "and" actions)
    - Confirm: ≤10 steps (split into sub-workflows if needed)
    - Confirm: all commands/tools referenced actually exist
    - Confirm: final step is verification with specific checks
    - Expected: 10/10 checklist items pass
    - If FAIL → Flag remaining issues; user decides next iteration

## Verification Checklist

- [ ] workflow-linter.py reports 0 violations (or informational only)
- [ ] Workflow has ≤10 steps, all numbered, all atomic
- [ ] Self-evaluation.md score ≥ 8/10
- [ ] All dangerous commands (rm, push --force, DROP) are NOT marked turbo
- [ ] Last step is verification with specific, measurable checks
- [ ] Before/after comparison shows clear improvements
