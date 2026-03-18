# Diminishing Returns: When to Stop Iterating

This document helps you recognize when further refinement yields minimal improvement and when to deliver the current best version.

---

## The Cost of Iteration

Each iteration has costs:

| Cost Factor | Impact |
|---|---|
| **Token consumption** | 10-30% of original response per iteration |
| **Time cost** | 30-60 seconds per iteration |
| **Quality ceiling** | Some defects are structural; no amount of patching fixes them |

Expected return from iteration:

- **Iteration 1:** Score improvement +2-4 points average (highest ROI)
- **Iteration 2:** Score improvement +1-2 points average (good ROI)
- **Iteration 3:** Score improvement +0-1 point average (low ROI)
- **Iteration 4+:** Score improvement <0.5 points (negative ROI)

---

## Signal Detection Table

### Signal 1: Delta < 0.5

**What it means:** The average score barely improved between iterations.

**Threshold:** If average score increased by less than 0.5 between iteration N and N+1, continue to iteration N+2, then deliver.

| Scenario | Action |
|---|---|
| Iteration 1: 7.8 → Iteration 2: 8.2 (delta +0.4) | Continue to iteration 3, then deliver |
| Iteration 2: 8.2 → Iteration 3: 8.7 (delta +0.5) | Acceptable; can continue if other signals allow |
| Iteration 3: 8.7 → Iteration 4: 8.9 (delta +0.2) | Stop. Diminishing returns. Deliver iteration 3. |

---

### Signal 2: Same Criterion Stuck

**What it means:** You've tried to fix a criterion twice, and it refuses to improve.

**Threshold:** If the same criterion fails after 2 refinement attempts, stop trying.

| Scenario | Action |
|---|---|
| Iteration 1: Profundidad = 5 | Try refinement |
| Iteration 2: Profundidad = 6 (improved 1 point) | Try again |
| Iteration 3: Profundidad = 6 (no change) | Stop. Architectural issue. Deliver iteration 2. |
| Iteration 1: Valor = 4, Iteration 2: Valor = 4 | Structural problem. Can't patch. Deliver iteration 1. |

**Why:** A criterion that refuses to improve despite two refinement cycles indicates a structural problem, not a superficial issue. More patches won't help.

---

### Signal 3: Iteration Count

**What it means:** You've done the maximum safe number of iterations.

**Hard limit:** 3 iterations maximum.

- **Why 3?** Beyond 3 iterations, token ROI becomes negative. Better to deliver good (not perfect) than to exhaust context for marginal gains.

| Iteration | Expected | Hard Stop? |
|---|---|---|
| 1 | Yes. Mandatory | No |
| 2 | Yes. Often delivers good enough | No |
| 3 | Optional. Only if iteration 2 shows promise | Yes — after 3, deliver |
| 4+ | Never. Stop at 3. | ALWAYS |

---

## Decision Tree: Continue, Deliver, or Restructure?

```
START: Have I evaluated this content?
│
├─ No → Evaluate. Go to STEP 1
│
└─ Yes → Continue to STEP 1

STEP 1: Are all 10 criteria ≥ 10?
│
├─ Yes → DELIVER IMMEDIATELY ✓
│
└─ No → Continue to STEP 2

STEP 2: Are all criteria ≥ 8 AND is this iteration ≥ 2?
│
├─ Yes → DELIVER (good enough) ✓
│
└─ No → Continue to STEP 3

STEP 3: Have I done 3 iterations?
│
├─ Yes → DELIVER (max iterations reached) ✓
│
└─ No → Continue to STEP 4

STEP 4: Did the average score improve by ≥ 0.5 in the last iteration?
│
├─ Yes → Continue to STEP 5
│
└─ No → DELIVER (diminishing returns) ✓

STEP 5: Is any criterion below 4 AND has it stayed below 4 after 2 refinements?
│
├─ Yes → RESTRUCTURE (not patching) → Redesign and restart loop
│
└─ No → Continue to STEP 6

STEP 6: Is any criterion at exactly the same score as the previous iteration?
│
├─ Yes → Check if this is the same criterion stuck twice
│        ├─ Yes → DELIVER (diminishing returns) ✓
│        └─ No → Continue to STEP 7
│
└─ No → Continue to STEP 7

STEP 7: Are there 3+ criteria below 8?
│
├─ Yes → REFINE (targetable issues remain)
│        └─ Identify 3 lowest. Apply refinement tactics. Re-evaluate. Go back to STEP 1.
│
└─ No → DELIVER (most criteria above 8) ✓
```

---

## Cost-Benefit Analysis

### The Math

**Cost of one iteration:**
- Evaluation: ~5 seconds + tokens
- Refinement: ~20 seconds + tokens
- Re-evaluation: ~5 seconds + tokens
- **Total:** ~30 seconds + 50-100K tokens

**Benefit of one iteration:**
- +1 to +4 points on average (iteration 1-2)
- +0 to +1 point on average (iteration 3)
- <0.5 points on average (iteration 4+)

**ROI Calculation:**

| Iteration | Avg Improvement | Cost | ROI | Decision |
|---|---|---|---|---|
| 1 | +3 | High | Excellent | Always do |
| 2 | +1.5 | High | Good | Usually do |
| 3 | +0.5 | High | Fair | Only if iteration 2 showed promise |
| 4 | +0.2 | High | Poor | Never do |

---

## When Low Scores Indicate Structural Redesign (Not Patching)

### Red Flags for Structural Issues

**Fundamento ≤ 4:** Content is fundamentally incomplete. Missing major sections or illogical ordering.
- Patching: Adding a paragraph here/there
- Restructuring: Rewrite with proper architecture (problem → solution → validation → conclusion)

**Valor ≤ 4:** Generic content with no domain expertise. Can't patch generic into expert-level.
- Patching: Add a few expert tips
- Restructuring: Rewrite from domain perspective, include methodology, reasoning patterns, shortcuts

**Profundidad ≤ 4:** Only happy path covered; ignores edge cases entirely.
- Patching: Add a few edge cases
- Restructuring: Rebuild with failure modes as first-class concern (every component needs error handling)

### Decision Rule

If any criterion is ≤ 4 after 2 refinement attempts:
- **Don't patch.** Patching fixes symptoms, not root causes.
- **Restructure:** Identify why the criterion is so low. Is it:
  - Missing entire sections? → Rebuild architecture
  - Lacking expert perspective? → Rewrite from domain expertise
  - Ignoring edge cases? → Design in failure modes from start
- **Restart the loop** with the restructured version.

---

## The 80/20 Rule Applied to Iteration

**Principle:** 80% of quality improvement comes from the first 2 iterations. The remaining 20% takes 4+ iterations.

### Phase 1: Rapid Improvement (Iterations 1-2)
- **What improves:** Calidad, Claridad, Precisión, Densidad (mechanical improvements)
- **Typical score jump:** 6-7 → 8-9
- **ROI:** Excellent. Always iterate.

### Phase 2: Diminishing Returns (Iterations 3+)
- **What improves:** Valor, Fundamento, Profundidad (require deeper work)
- **Typical score jump:** 8-9 → 8.5-9.5 (small increments)
- **ROI:** Fair to poor. Iterate only if iteration 2 showed strong improvement.

### Optimization Strategy

For most contexts:
1. **Always:** Do iteration 1. Score typically jumps 1-2 full points.
2. **Usually:** Do iteration 2. Score typically jumps 0.5-1 point. Often enough for "good".
3. **Rarely:** Do iteration 3. Only if iteration 2 showed strong improvement (delta >1) and scores are close to 10.
4. **Never:** Do iteration 4+. Negative ROI.

---

## Special Cases: When to Stop Early

### Case 1: Time-Sensitive Content

**Scenario:** User needs answer quickly; perfect isn't required.

**Decision:**
- If all criteria ≥ 8 after iteration 1, deliver immediately
- Don't pursue iteration 2
- Trade: 20-30% quality for 100% speed

### Case 2: Incremental Content (Part of Larger Work)

**Scenario:** This is chapter 5 of a 10-chapter document. Later chapters will refine earlier ones.

**Decision:**
- If all criteria ≥ 7 after iteration 1, deliver
- Plan to revisit in final pass
- Trade: Perfect now for coherence across entire work

### Case 3: User Has Low Tolerance for Latency

**Scenario:** User explicitly said "fast response is more important than perfection".

**Decision:**
- If all criteria ≥ 7.5 after iteration 1, deliver
- Skip iteration 2 and 3
- Trade: Quality for responsiveness

### Case 4: Content is Naturally Complex (Low Ceiling)

**Scenario:** Topic is inherently difficult; expertise injection hits diminishing returns.

**Decision:**
- Cap iterations at 2
- Deliver when average ≥ 8.5
- Accept that some criteria may stay at 7-8 due to topic complexity

---

## Delivery Decision Flowchart (Simplified)

```
Initial Eval Score (iteration 1):
│
├─ ALL criteria 10 → DELIVER NOW ✓
├─ ALL criteria 9-10 → 1 quick pass, then DELIVER
├─ ALL criteria 8-10 → Iteration 2. If all ≥8 after, DELIVER
├─ 3+ criteria < 8 → Full loop. Max 3 iterations
└─ Any criteria < 4 → Restructure, not patch. Restart loop.
```

---

## Iteration History Tracking

To know when to stop, track this for each iteration:

```
Iteration N:
- Average score: [X]/10
- Lowest criterion: [Y] (score)
- Delta from iteration N-1: [+Z points]
- Changes made: [list]
- Time spent: [seconds]
- Tokens used: [approximate]
```

**Decision trigger:** When delta < 0.5 for 2 consecutive iterations, stop.

---

## Example: Three-Iteration Progression

**Iteration 1 (Initial):**
- Scores: 7, 6, 8, 5, 7, 6, 7, 8, 7, 6
- Average: 6.7/10
- Lowest: Densidad (5)
- Delta: N/A (first)
- Action: Refine densidad, calidad, claridad

**Iteration 2 (After first refinement):**
- Scores: 8, 7, 9, 8, 8, 8, 8, 9, 8, 7
- Average: 8.0/10
- Lowest: Valor (7)
- Delta: +1.3 (good improvement)
- Action: Refine valor. Check if all ≥8 yet... no. Continue.

**Iteration 3 (After second refinement):**
- Scores: 9, 8, 10, 9, 9, 9, 9, 9, 9, 8
- Average: 8.9/10
- Lowest: Veracidad (8) and Valor (8)
- Delta: +0.9 (good improvement)
- Decision: Try iteration 4?

**Iteration 4 (Optional attempt):**
- Scores: 9, 8, 10, 9, 9, 9, 9, 9, 9, 8
- Average: 8.9/10
- Delta: +0 (no improvement)
- Decision: STOP. Deliver iteration 3. (Delta < 0.5 and stuck criteria = stop signal)

---

## Final Checklist: Am I Done?

- [ ] All criteria ≥ 10?
- [ ] All criteria ≥ 8 AND iteration ≥ 2?
- [ ] Total iterations = 3 already?
- [ ] Delta < 0.5 for last iteration?
- [ ] Any criterion ≤ 4 for 2 iterations? (If yes, need restructure, not iteration 4)

**If ANY of the above is true → DELIVER. Do not continue iterating.**
