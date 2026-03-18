# Workflow: Review Prompt

Evaluate an existing prompt against the 10-criterion rubric and deliver a scorecard with prioritized fixes.

## Trigger

User provides a prompt and asks for review, feedback, quality check, or evaluation.

## Steps

### Step 1: Ingest

Read the full prompt. Identify:
- Target platform (infer from format if not stated)
- Current version (if versioned)
- The user's specific concerns (if stated)

### Step 2: Automated Evaluation

Run the evaluator:

```bash
python tools/prompt-evaluator.py [prompt-file] --verbose --strict
```

Capture the scorecard output.

### Step 3: Deep Analysis

Beyond the automated checks, manually evaluate:

1. **Archetype quality** — Is it a true hybrid or single-dimensional?
2. **Flow completeness** — Are phase transitions explicit?
3. **Constraint testability** — Could you write assertions for each constraint?
4. **Token efficiency** — Can any section be compressed without losing meaning?
5. **Platform fit** — Is it optimized for its target platform?

### Step 4: Deliver Scorecard

Present results in this format:

```markdown
## Prompt Review Scorecard

| Criterion | Score | Status |
|-----------|-------|--------|
| Foundation | X/10 | ✓/✗ |
| ... | ... | ... |

**Overall: X.X/10**

### Priority Fixes (ordered by impact)

1. **[Criterion]:** [specific issue] → [specific fix]
2. **[Criterion]:** [specific issue] → [specific fix]
3. **[Criterion]:** [specific issue] → [specific fix]

### Strengths

- [What's working well]
- [What to preserve]
```

### Step 5: Offer Next Steps

Based on the review:
- If score ≥ 8 average → "Ready for production. Minor tweaks suggested."
- If score 6-7 average → "Solid foundation. Apply the priority fixes and re-evaluate."
- If score < 6 → "Recommend running the Evolve workflow for a structured improvement cycle."

## Exit Criteria

- Scorecard delivered with per-criterion scores
- Priority fixes listed and specific
- Clear recommendation for next steps
