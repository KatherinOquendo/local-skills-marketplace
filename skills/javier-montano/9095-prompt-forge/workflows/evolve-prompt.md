# Workflow: Evolve Prompt

Take a working prompt and systematically improve it through the Excellence Loop.

## Trigger

User wants to optimize, improve, or upgrade an existing prompt that already works but could be better.

## Steps

### Step 1: Baseline

Evaluate the current prompt to establish a baseline:

```bash
python tools/prompt-evaluator.py [prompt-file] --verbose --strict
```

Record the baseline scores. This is the benchmark to beat.

### Step 2: Identify Weak Dimensions

From the scorecard, select the **3 lowest-scoring criteria**. These are the improvement targets.

**Rule:** Fix no more than 3 dimensions per iteration. More causes regressions.

### Step 3: Apply Targeted Improvements

For each weak dimension, consult `reference/evaluation-rubric.md` for the repair protocol:

| Criterion | Typical Fix |
|-----------|-------------|
| Foundation | Upgrade archetype to hybrid, add missing sections |
| Accuracy | Verify all named frameworks, remove unverifiable claims |
| Quality | Remove filler, convert passive to active voice |
| Density | Apply 2x constraint, merge duplicates, use tables |
| Simplicity | Flatten hierarchy, replace jargon with plain language |
| Clarity | Replace vague qualifiers with specific conditions |
| Precision | Convert aspirational constraints to testable rules |
| Depth | Add edge case handling, self-correction triggers |
| Coherence | Map cross-section dependencies, resolve contradictions |
| Value | Add domain methodology, reasoning directives, expertise |

### Step 4: Re-Evaluate

Run the evaluator again on the improved version:

```bash
python tools/prompt-evaluator.py [improved-file] --verbose --strict
```

**Verify:**
- Targeted dimensions improved
- No regressions on other dimensions
- Overall average increased

### Step 5: Iterate or Deliver

**If all criteria ≥ 8:** Deliver the improved prompt with a changelog.

**If not:** Return to Step 2 with the new scorecard. Maximum 3 iterations.

**If stuck after 2 attempts on same dimension:** The architecture may need restructuring rather than patching. Consider rebuilding that section from scratch using the Create workflow.

### Step 6: Version and Deliver

Update the version number:
- Minor improvement → v1.X+1
- Structural change → v2.0

Deliver with:
- Before/after scorecard comparison
- Changelog of what changed and why
- Updated deployment instructions if platform-relevant changes were made

## Exit Criteria

- All 10 criteria ≥ 8/10
- No regressions from baseline
- Changelog documenting all changes
- Version number updated
