# Workflow: Solve Complex Task

## Overview

This workflow executes the full DSVSR protocol (Decompose-Solve-Verify-Synthesize-Reflect) for complex problems requiring high confidence (0.95+).

## Trigger Conditions

Activate this workflow when:
- Complexity score is 6+ points (see complexity-heuristics.md)
- User explicitly asks for high confidence or thorough analysis
- Problem has multiple domains or dependencies
- Consequences of being wrong are significant
- Prior fast-path attempt yielded confidence < 0.75

## Workflow Steps

### Step 1: Receive Problem

**Input:** Problem statement from user or from input-analyst

**Actions:**
1. Read and understand the problem
2. Note any explicit preferences (format, depth, confidence target)
3. Identify time constraints
4. Scan thread context and attachments (see recursion-protocol.md)

**Output:** Problem statement + context summary

---

### Step 2: Detect Complexity

**Actions:**
1. Run complexity-heuristics check
2. Assess word count, question type, ambiguity, stakes, dependencies
3. Assign complexity score (0-15 points)

**Decision:**
- If complexity < 3 points → Redirect to quick-answer workflow (return to start)
- If complexity 3-5 points → Use hybrid path (light decomposition)
- If complexity 6+ points → Continue to full DSVSR (next step)

**Output:** Complexity assessment + routing decision

---

### Step 3: Decompose Into Sub-Problems

**Actions:**
1. Identify core question (strip context)
2. List all components requiring separate answers
3. Map dependencies (if/then, before/after, because relationships)
4. Identify domains (technical, business, creative, factual, analytical, human)
5. Order by dependency chain (foundations first)

**Tools:** Use task-decomposer.py for structural analysis

**Output:**
```
Sub-problems identified: [N]
├── SP-1: [description] (domain: [X], depends on: none, priority: 1)
├── SP-2: [description] (domain: [X], depends on: SP-1, priority: 2)
└── SP-N: [description] (domain: [X], depends on: [...], priority: [X])

Solve order: SP-1 → SP-2 → ... → SP-N
```

---

### Step 4: Solve Each Sub-Problem

**For each sub-problem (in order):**

1. Gather relevant evidence (data, research, reasoning)
2. Construct answer with explicit reasoning
3. Assess confidence (0.0-1.0 scale, see confidence-calibration.md)
4. Identify gaps (what would increase confidence?)
5. Mark critical issues if confidence < 0.70

**Output per sub-problem:**
```
SP-[N]: [Sub-problem]

ANSWER:
[Concise answer to the sub-problem]

CONFIDENCE: [0.XX]

JUSTIFICATION:
[Explicit reasoning for the confidence score]

WOULD INCREASE TO [0.XX] IF:
[Specific information that would strengthen confidence]
```

**Decision Point:** If any critical sub-problem has confidence < 0.70:
- Flag for potential escalation to REFLECT stage
- Continue solving remaining sub-problems

---

### Step 5: Verify All Answers

**For each sub-answer:**

1. **Logic check:** Is the reasoning internally consistent? Do premises support conclusion?
2. **Facts check:** Are factual claims verifiable? Have I confused opinion with fact?
3. **Completeness check:** Have I considered all relevant aspects? What am I NOT addressing?
4. **Bias check:** Am I anchored on first solution? Confirming only what I believe? Overweighting familiar examples?

**Actions:**
- Red-team your own answers (assume you're wrong, where would you fail?)
- Identify contradictions with other sub-answers
- Revise confidence scores based on verification findings
- Document any issues discovered

**Output:**
```
VERIFICATION RESULTS:
☐ LOGIC: [Pass | Issues: ...]
☐ FACTS: [Pass | Issues: ...]
☐ COMPLETENESS: [Pass | Issues: ...]
☐ BIAS: [Pass | Issues: ...]

Revised confidence: [Updated scores based on findings]
```

---

### Step 6: Synthesize Into Coherent Response

**Actions:**
1. Start with highest-confidence sub-answers (foundation)
2. Layer in moderate-confidence answers with caveats
3. Handle conflicts (use conflict resolution hierarchy)
4. Mark clearly: what is **certainty** vs what is **hypothesis**
5. Compute global confidence (weighted average by sub-problem importance)

**Conflict Resolution Hierarchy** (if sub-answers contradict):
- Priority 1: Verified facts
- Priority 2: Logical deductions from verified facts
- Priority 3: Expert consensus / established frameworks
- Priority 4: Reasonable inference from partial evidence
- Priority 5: Educated speculation (always flagged)

**Output:**
- Coherent response integrating all sub-answers
- Global confidence score (0.XX)
- Clear marking of certainties vs hypotheses

---

### Step 7: Reflect on Confidence

**Decision Tree:**
```
IF global_confidence < target (default 0.95):

    1. DIAGNOSE:
       - Which sub-problem has the lowest confidence?
       - Why is it low? (data gap, logic gap, expertise gap)

    2. ASSESS:
       - Is this sub-problem critical to the final answer?
       - Would increasing its confidence change the recommendation?

    3. DECIDE:
       a) If retrievable → gather information and retry (max 3 iterations)
       b) If not retrievable → deliver with caveats (flag specific uncertainties)
       c) If fundamentally unknowable → state this clearly

ELSE (global_confidence >= target):
    → Proceed to Step 8 (generate metadata)
```

**Reflection Questions:**
- What is the single biggest weakness in my reasoning?
- If I'm wrong, what's the most likely cause?
- What would someone who disagrees with me say?
- Is there a simpler explanation I'm overlooking?

---

### Step 8: Iterate on Weak Sub-Problems (If Needed)

**Trigger:** If any critical sub-problem confidence < target AND retrievable information exists

**Actions (max 3 iterations):**
1. Identify specific information gap
2. Gather additional data/research
3. Re-solve the weak sub-problem
4. Re-verify the updated answer
5. Recompute global confidence
6. Check if target reached

**Example Iteration:**
```
Iteration 1:
- Weak sub-problem: "Market size"
- Gap: Using analyst reports only, no primary research
- Action: Analyze bottom-up (count competitors, survey customers)
- Result: Confidence 0.82 → 0.88

Iteration 2:
- Weak sub-problem: "Product-market fit"
- Gap: Limited customer validation
- Action: Run structured interviews with 5-7 target customers
- Result: Confidence 0.70 → 0.82

Global confidence: 0.78 → 0.85 (approaching target)
```

**Decision Point:** After max 3 iterations:
- If confidence >= 0.85 → Deliver with confidence metadata
- If confidence 0.70-0.84 → Deliver with caveats and next steps
- If confidence < 0.70 → Deliver with explicit limitations

---

### Step 9: Generate Metadata

**Actions:**
1. Compute final global confidence
2. Collect sub-problem confidence scores
3. List sources consulted (thread, attachments, knowledge)
4. Identify weaknesses and gaps
5. Determine rigidity level (executive, analytical, exploratory)
6. Generate metadata using metadata-generator.py

**Output:**
```
---
📊 REASONING METADATA:
• Global confidence: [0.XX]
• Sub-problem confidence: [SP-1: 0.XX, SP-2: 0.XX, ...]
• Sources consulted: [thread messages, attachments, knowledge]
• Weaknesses identified: [if any]
• Rigidity level: [exploratory | analytical | executive]
• Verification status: [all checks passed | [N] flags raised]
---
```

---

### Step 10: Output to Excellence-Loop

**Actions:**
1. Format final response with:
   - Coherent answer (from synthesize step)
   - Reasoning explanation (how you arrived at it)
   - Confidence metadata (global + sub-problem breakdown)
   - Caveats and limitations (if any)

2. Hand off to excellence-loop for quality refinement

**Excellence-loop will:**
- Review reasoning for clarity
- Check citations and sources
- Validate conclusions against metadata
- Refine formatting and presentation
- Add examples or elaboration if needed

---

## Workflow Diagram

```
START
  ↓
[1. Receive Problem]
  ↓
[2. Detect Complexity]
  ├─ Low? → Redirect to quick-answer
  ├─ Hybrid? → Light decomposition path
  └─ High? → Continue to full DSVSR
  ↓
[3. Decompose] → Generate sub-problems
  ↓
[4. Solve] → Answer each with confidence
  ↓
[5. Verify] → Check logic, facts, completeness, bias
  ↓
[6. Synthesize] → Combine with weighted integration
  ↓
[7. Reflect] → Assess global confidence
  ↓
  Is confidence >= target?
  ├─ YES → [9. Generate Metadata]
  └─ NO → [8. Iterate] → (max 3 cycles) → Back to Reflect
  ↓
[9. Generate Metadata]
  ↓
[10. Output to Excellence-Loop]
  ↓
END
```

---

## Time Budget

Typical time allocation for complex problems:

| Step | Time | Notes |
|------|------|-------|
| Receive + Detect | 2-3 min | Quick assessment |
| Decompose | 5-10 min | Detailed structural analysis |
| Solve | 15-30 min | Per sub-problem: 3-5 min |
| Verify | 10-15 min | Per sub-problem: 2-3 min |
| Synthesize | 5-10 min | Integration and conflict resolution |
| Reflect | 3-5 min | Diagnostic assessment |
| Iterate | 10-20 min | If needed (per iteration) |
| Generate Metadata | 2-3 min | Automated |
| **Total** | **45-100 min** | Depends on complexity and iteration count |

---

## Exit Conditions

### Success Path
- Global confidence >= target (0.95)
- All sub-problems verified
- Output ready for excellence-loop

### Acceptable Path
- Global confidence 0.85-0.94
- Caveats clearly marked
- Deliverable with next-steps recommended

### Degraded Path
- Global confidence 0.70-0.84
- Significant gaps documented
- Exploratory-level delivery, not executive

### Abort Path
- Global confidence < 0.70 after 3 iterations
- Fundamentally unanswerable with available information
- Declare unknowable, recommend research approach

---

## Troubleshooting

### Problem: Confidence won't increase above 0.75

**Diagnosis:**
- Missing critical information
- Multiple valid perspectives (not converging)
- Domain expertise gap

**Solutions:**
1. Ask user for missing information
2. Acknowledge multiple valid paths (present as options)
3. Escalate to domain specialist (if available)

### Problem: Verification discovers major flaws

**Diagnosis:**
- Initial assumptions were wrong
- Missed important dimension
- Logic error in reasoning

**Solutions:**
1. Revise affected sub-problems
2. Recompute global confidence
3. Document what changed and why

### Problem: Sub-problems are too dependent (can't solve in order)

**Diagnosis:**
- Decomposition needs refactoring
- Circular dependencies exist

**Solutions:**
1. Revisit decomposition (go back to Step 3)
2. Reorder sub-problems or reframe dependencies
3. Restart solve cycle

---

## Key Principles

1. **Rigor matters** — Don't rush verification and reflection
2. **Iteration is normal** — Low confidence often requires retrieval and re-solving
3. **Transparency is key** — Document gaps, assumptions, caveats
4. **Confidence is earned** — 0.95 is a high bar; 0.85 is solid
5. **Excellence-loop comes next** — Don't over-refine here; let that stage polish
