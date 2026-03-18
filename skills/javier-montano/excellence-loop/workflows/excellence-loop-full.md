# Full Excellence Loop Workflow

Complete evaluation-refinement cycle for maximizing response quality.

---

## Overview

**Input:** Response draft (from task-engine or user prompt)

**Output:** Final polished response at 10/10 on all criteria (or best achievable version)

**Duration:** 2-5 minutes per response

**Invisible to user:** Process is completely hidden; only final version is delivered

---

## Step-by-Step Workflow

### Step 1: Receive Response Draft

**Input source:**
- Task-engine output, OR
- Direct response to user query

**Data to capture:**
- Full response text
- Task metadata (deadline, importance, confidence score from task-engine)
- User context (domain, audience, use case)

---

### Step 2: Run Initial Evaluation

**Command:**
```bash
python tools/rubric-evaluator.py response.md --verbose
```

**Output:** Scorecard showing all 10 criteria

**Decision point:**
- **If all 10 criteria are 10/10:** Go to Step 10 (DELIVER)
- **If all criteria ≥ 8:** Go to Step 3 (Fast path)
- **If any criterion < 8:** Go to Step 4 (Full loop)

---

### Step 3: Fast Path (All ≥ 8)

**Condition:** All criteria score 8 or higher

**Action:** One quick refinement pass
1. Identify the lowest-scoring criterion (even if it's 8)
2. Run refinement suggester:
   ```bash
   python tools/refinement-suggester.py response.md --top 1
   ```
3. Apply the top suggestion (quick fix)
4. Re-evaluate:
   ```bash
   python tools/rubric-evaluator.py response.md
   ```

**Decision:**
- **If all ≥ 9:** Proceed to Step 10 (DELIVER)
- **Otherwise:** Follow full loop (Step 4)

---

### Step 4: Identify Lowest-Scoring Criteria

**Process:**
1. From evaluation output, identify the 3 criteria with lowest scores
2. Record these (example: Densidad 5, Valor 6, Claridad 7)
3. Note any criterion below 4 (indicates structural problem)

---

### Step 5: Generate Refinement Suggestions

**Command:**
```bash
python tools/refinement-suggester.py response.md --top 3
```

**Output:** Specific, actionable suggestions for each low-scoring criterion

**Review suggestions:**
- For each criterion, pick 1-2 suggestions with highest impact
- Focus on "low effort, high impact" first
- Note expected improvements

---

### Step 6: Apply Targeted Refinements

**Process:**
1. Take the response draft
2. Apply top suggestions in order of impact:
   - Start with highest-impact, lowest-effort (usually Densidad, Claridad, Precisión)
   - Progress to medium-effort (Calidad, Simplicidad)
   - Save high-effort for iteration 2+ (Profundidad, Valor, Fundamento)
3. Preserve all structure and content; focus on surgical improvements

**Example refinements:**
- Remove duplicate sentences (Densidad)
- Replace vague qualifiers (Claridad)
- Convert prose lists to tables (Densidad)
- Add edge case handling (Profundidad)
- Inject domain expertise (Valor)

**Output:** Refined response (still response.md, updated)

---

### Step 7: Re-Evaluate

**Command:**
```bash
python tools/rubric-evaluator.py response.md
```

**Record results:** Note new scores for all 10 criteria

**Calculate improvement:**
- Compare to previous iteration
- Calculate average delta
- Identify any criteria that improved significantly vs. stayed stuck

---

### Step 8: Check Termination Conditions

**Evaluate against these signals:**

| Signal | Condition | Action |
|--------|-----------|--------|
| All ≥ 10 | All criteria are 10/10 | STOP → Go to Step 10 (DELIVER) |
| All ≥ 8, iteration ≥ 2 | Good enough threshold reached | STOP → Go to Step 10 (DELIVER) |
| Delta < 0.5 | Diminishing returns | STOP → Go to Step 10 (DELIVER) |
| Same criterion stuck | Failed to improve after 2 attempts | Architecture problem. STOP → Step 10 (DELIVER best) |
| Iteration = 3 | Hard iteration limit reached | STOP → Go to Step 10 (DELIVER best) |
| Any criterion ≤ 4 (2nd attempt) | Structural failure | Restructure needed. Consider redesign or STOP |

---

### Step 9: Continue or Deliver?

**Decision logic:**

```
IF all criteria ≥ 10:
  → DELIVER (Step 10)

IF all criteria ≥ 8 AND iteration ≥ 2:
  → DELIVER (Step 10)

IF delta < 0.5 (score barely improved):
  → DELIVER (Step 10)

IF iteration = 3 (hard limit):
  → DELIVER (Step 10)

IF any criterion ≤ 4 after 2 refinement attempts:
  → Consider restructuring OR DELIVER best version

ELSE (there's room to improve):
  → Go back to Step 4 (next iteration)
```

---

### Step 10: Archive (Optional) and Deliver

**Archive version history (if requested or high-stakes):**
```bash
python tools/version-archiver.py --show-history response.md
```

**Delivery protocol:**
- User receives ONLY the final response
- NO meta-commentary about the refinement process
- NO iteration counts, score progression, or process traces
- NO "I've refined this through 3 iterations"

**Exception:** If user explicitly asked "show me the iterations" or "how did you arrive at this?", deliver version history as a separate artifact

**Delivery format:**
```
[Final response text, clean and polished]

---

### Version History [OPTIONAL - ONLY IF REQUESTED]

[Iteration progression, if user requested it]
```

---

## Example: Three-Iteration Loop

### Initial Evaluation
- Average: 6.7/10
- Lowest: Densidad (5), Claridad (6), Valor (6)

### Iteration 1 Refinements
- Merged duplicate sentences (Densidad)
- Replaced vague qualifiers (Claridad)
- Added 2-3 domain expertise examples
- Re-evaluate: 8.0/10 (delta +1.3) ✓ Strong improvement

### Iteration 2 Refinements
- Added edge cases and error handling (Profundidad)
- Expanded methodology section (Valor)
- Re-evaluate: 9.1/10 (delta +1.1) ✓ Continued improvement

### Iteration 3 Decision
- Check conditions: all ≥ 9, iteration = 2
- Deliver (meets "good enough" threshold)

---

## Time Budgets by Confidence

**Task-engine provides confidence score (0.0 - 1.0)**

| Confidence | Max Iterations | Fast Path? | Note |
|---|---|---|---|
| ≥ 0.95 | 1 | Yes (skip if ≥8) | High confidence: quick pass only |
| 0.85-0.94 | 2 | Yes (skip if ≥8) | Good confidence: 1-2 iterations |
| < 0.85 | 3 | No (full loop) | Low confidence: aggressive refinement |

---

## Decision Tree (Quick Reference)

```
START: Evaluate response
│
├─ All ≥ 10? → DELIVER ✓
├─ All ≥ 8? → Fast path (1 quick refinement) → Deliver
├─ Any ≤ 4? → Structural problem? → Restructure or deliver best
│
└─ Full loop:
    1. Run full evaluation
    2. Identify lowest 3 criteria
    3. Generate suggestions
    4. Apply refinements (Densidad → Claridad → Precisión first)
    5. Re-evaluate
    6. Check termination conditions
    7. If not done → Loop back to step 2
    8. Deliver final version
```

---

## Common Pitfalls

### Pitfall 1: Over-iterating
**Problem:** Continuing past diminishing returns (delta < 0.5)
**Solution:** Stop at iteration 3, or when delta shows no improvement

### Pitfall 2: Structural Patch
**Problem:** A criterion stays below 4 despite refinement attempts
**Solution:** This indicates architectural failure. Accept the score or redesign.

### Pitfall 3: Invisible Process (broken)
**Problem:** Delivering version history or process notes to user
**Solution:** ONLY deliver the final response. Archive history separately.

### Pitfall 4: Missing High-Stakes Signal
**Problem:** Not recognizing when response is important enough to iterate 3x
**Solution:** Check task metadata. High-stakes (strategy, proposals, publications) → full loop always

---

## Automation Integration

### With task-engine
```
task-engine response → excellence-loop → user sees final only
```

**Handoff:**
1. task-engine outputs response + confidence score
2. excellence-loop uses confidence to calibrate iteration depth
3. task-engine receives final polished response

### Calibration
- Confidence ≥ 0.95: Fast path (max 1 iteration)
- Confidence 0.85-0.94: Standard loop (max 2 iterations)
- Confidence < 0.85: Full loop (max 3 iterations, aggressive)

---

## Manual Invocation

**When user says:**
- "Make this perfect"
- "Iterate until done"
- "Highest quality possible"
- "Excellence loop"
- "Auto-improve this"

**Action:** Run the full workflow (all steps) regardless of initial quality

---

## Checklist: Before Delivering

- [ ] All 10 criteria evaluated
- [ ] Latest scores recorded
- [ ] No iteration > 3
- [ ] No criterion stuck below 4 (after 2 attempts)
- [ ] Delta ≥ 0.5 between this and previous iteration (or iteration 1)
- [ ] User sees ONLY final response (no process traces)
- [ ] Version history archived separately if needed
- [ ] No meta-commentary ("I've refined this through...")

---

## Refinement Impact Reference

| Criterion | Typical Improvement | Effort | Tools |
|-----------|---|---|---|
| Densidad | +2-3 points | Low | Apply 2x constraint, table conversion |
| Claridad | +2-3 points | Low | Vague qualifier replacement |
| Precisión | +1-2 points | Low | Aspirational→testable conversion |
| Calidad | +1-2 points | Medium | Active voice, filler removal |
| Simplicidad | +1-2 points | Medium | Hierarchy flattening, jargon explanation |
| Profundidad | +1-2 points | Medium | Edge case discovery, error handling |
| Coherencia | +1 point | Medium | Cross-references, terminology audit |
| Veracidad | +1-2 points | High | Source verification, citation addition |
| Fundamento | +1-2 points | High | Restructuring, section addition |
| Valor | +1-2 points | High | Expertise injection, methodology |
