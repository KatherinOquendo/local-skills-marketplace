# Quick-Check Workflow

Fast evaluation path for already-high-quality content. Use when initial evaluation shows all criteria ≥ 8.

---

## When to Use This Workflow

**Conditions:**
- Initial evaluation shows all criteria ≥ 8
- OR user requests quick turnaround
- OR task confidence ≥ 0.95

**Do NOT use if:**
- Any criterion < 8
- Content is high-stakes (strategy, proposals, publications)
- User asked for "maximum quality" or "iterate until perfect"

---

## Step-by-Step

### Step 1: Initial Evaluation

```bash
python tools/rubric-evaluator.py response.md
```

**Decision point:**
- **All criteria ≥ 8?** Continue to Step 2 (quick-check applies)
- **Any criterion < 8?** Stop. Use full loop instead (`excellence-loop-full.md`)

---

### Step 2: Identify Lowest Criterion

From evaluation output:
- Find the single criterion with the lowest score
- Note its current score

Example: If scores are [9, 8, 9, 8, 9, 8, 9, 9, 9, 8], lowest is 8

---

### Step 3: One Quick Refinement Pass

**Generate suggestions for the lowest criterion:**

```bash
python tools/refinement-suggester.py response.md --criterion <name>
```

where `<name>` is the lowest-scoring criterion (e.g., `claridad`, `densidad`)

**Pick ONE suggestion** (the one with highest impact + lowest effort)

**Apply the refinement** (5-10 minutes of targeted editing)

---

### Step 4: Re-Evaluate

```bash
python tools/rubric-evaluator.py response.md
```

**Decision:**
- **All criteria ≥ 9?** Deliver (Step 5)
- **All criteria ≥ 8?** Deliver (Step 5)
- **Any criterion < 8?** Escalate to full loop (stop; use `excellence-loop-full.md`)

---

### Step 5: Deliver

**Output:** Final response to user

**Protocol:**
- No meta-commentary ("I've refined this")
- No iteration history
- Clean, polished response only

---

## Example: Quick-Check in Action

**Initial Evaluation:**
```
Fundamento:  9/10 █████████░
Veracidad:   9/10 █████████░
Calidad:     9/10 █████████░
Densidad:    8/10 ████████░░  ← Lowest
Simplicidad: 9/10 █████████░
Claridad:    9/10 █████████░
Precisión:   9/10 █████████░
Profundidad: 9/10 █████████░
Coherencia:  9/10 █████████░
Valor:       9/10 █████████░

Average: 8.9/10 ✓ QUICK-CHECK APPLIES
```

**Refinement Suggestion for Densidad:**
- "Apply 2x density constraint" (merge 3 duplicate sentences)

**Apply:** Merge 3 similar sentences into 1 concise statement

**Re-evaluate:**
```
Average: 9.1/10 ✓ All ≥ 8 → DELIVER
```

**Time:** ~8 minutes total (evaluation + refinement + re-evaluation)

---

## When to Escalate to Full Loop

**Stop quick-check and use full loop if:**

1. **Re-evaluation shows any criterion dropped below 8** after refinement
2. **Any criterion is still below 8** after refinement
3. **Original evaluation had ANY criterion below 8** (quick-check shouldn't have started)
4. **User said "make it perfect" or "iterate until done"**
5. **This is a high-stakes deliverable** (strategy, published article, major proposal)

**Action:** Start from scratch with `excellence-loop-full.md`

---

## Checklist: Before Delivering

- [ ] Initial evaluation: all criteria ≥ 8?
- [ ] Applied one targeted refinement
- [ ] Re-evaluated
- [ ] All criteria still ≥ 8?
- [ ] No meta-commentary in delivery
- [ ] User receives final response only

---

## Time Estimate

| Step | Time |
|---|---|
| Initial evaluation | 2-3 min |
| Generate suggestions | 1 min |
| Apply refinement | 5-10 min |
| Re-evaluate | 2-3 min |
| **Total** | **10-17 minutes** |

---

## When NOT to Use Quick-Check

- Content quality < 8 in any criterion → Use full loop
- High-stakes deliverables → Use full loop
- User requested "perfection" or "maximum quality" → Use full loop
- Task confidence < 0.85 → Use full loop
- Any criterion below 7 in initial eval → Use full loop

---

## Reference: Typical Quick-Check Impact

**Starting point:** 8.5-9.0 average
**Typical improvement:** +0.2 to +0.5 points (targeting lowest criterion)
**Final average:** 8.7-9.5
**Delivery threshold:** ≥ 8.0 average (all criteria ≥ 8)

Most quick-check refinements focus on:
- Densidad: 2x constraint, filler removal
- Claridad: Vague qualifier replacement
- Precisión: Add units/context to claims
- Calidad: Quick active voice pass

---

## Alternative: Skip Refinement Entirely

**If initial evaluation shows all ≥ 9:**

```bash
python tools/rubric-evaluator.py response.md
```

If ALL criteria are 9 or 10, consider **immediate delivery** (no refinement needed).

This is appropriate for:
- Very strong initial responses
- Time-sensitive queries
- Content already close to perfect
