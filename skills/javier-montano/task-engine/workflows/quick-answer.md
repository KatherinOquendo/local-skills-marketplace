# Workflow: Quick Answer

## Overview

This workflow handles simple, low-complexity questions that don't require the full DSVSR protocol. It delivers fast answers with appropriate confidence levels.

## Trigger Conditions

Activate this workflow when:
- Complexity score is 0-2 points (see complexity-heuristics.md)
- Question is factual, single-domain, unambiguous
- Consequences of being wrong are low
- User isn't explicitly asking for deep analysis or high confidence

## Workflow Steps

### Step 1: Receive Question

**Input:** Question from user

**Actions:**
1. Read and understand the question
2. Quickly scan for:
   - Explicit confidence request? ("high confidence needed")
   - Format preference? ("Keep it brief", "Detailed")
   - Time constraint? ("Quick answer", "In 5 minutes")

**Output:** Question + context

---

### Step 2: Detect Complexity

**Actions:**
1. Run complexity-heuristics quick check
2. Assess:
   - Is this a single, clear question?
   - Is there only one reasonable interpretation?
   - Are there multiple interconnected factors?

**Decision:**
- Complexity score 0-2 → Continue with quick answer (Step 3)
- Complexity score 3-5 → Escalate to hybrid path
- Complexity score 6+ → Escalate to full DSVSR

**Output:** Complexity assessment + routing decision

---

### Step 3: Answer Directly

**Actions:**
1. Provide clear, concise answer
2. Include brief reasoning (1-2 sentences)
3. Add inline confidence level
4. Include caveats if relevant (e.g., "Assumes X")

**Output Format:**

```
ANSWER:
[Direct, clear answer to the question]

REASONING:
[1-2 sentences explaining why you're confident]

CONFIDENCE: [0.XX]

[Optional caveat: "Note: This assumes X"]
```

---

### Step 4: Append Minimal Metadata

**Actions:**
1. Inline confidence (already in Step 3)
2. No separate metadata block (keep it minimal)
3. If caveats exist, state them clearly

**Output:**
- Answer with inline confidence
- Caveats (if any)
- Skip comprehensive metadata

---

### Step 5: Output

**Actions:**
1. Send answer directly to user
2. Skip excellence-loop for trivial questions (optional)

**Output:** User-ready response

---

## Workflow Diagram

```
START
  ↓
[1. Receive Question]
  ↓
[2. Detect Complexity]
  ├─ Low (0-2)? → Continue
  ├─ Medium (3-5)? → Escalate to hybrid
  └─ High (6+)? → Escalate to DSVSR
  ↓
[3. Answer Directly]
  ↓
[4. Append Minimal Metadata]
  ↓
[5. Output to User]
  ↓
END
```

---

## Examples

### Example 1: Factual Question (Simple)

**Question:** "What year was Python released?"

**Complexity:** 0 points
- Single question
- Single answer
- No ambiguity
- No stakes

**Workflow:**
1. Receive: "What year was Python released?"
2. Detect: Complexity 0 → Quick answer
3. Answer: "Python was first released in 1991 by Guido van Rossum."
4. Confidence: 0.99 (historical fact, widely documented)
5. Output: "Python was released in 1991. Confidence: 0.99"

---

### Example 2: Simple Advice (Quick)

**Question:** "Should we use React or Vue for this project?"

**Complexity:** First check...
- Single question (yes)
- But TWO frameworks to compare (trade-off)
- Multiple valid answers (depends on context)
- **Re-assess: Complexity is actually 4-5 points (trade-off, comparison)**

**Action:** Escalate to hybrid path (not quick answer)

---

### Example 3: Definitional Question (Simple)

**Question:** "What's the difference between SQL and NoSQL databases?"

**Complexity:** 2 points
- Single question
- Comparison but not decision-oriented
- Textbook answer
- No stakes (informational)

**Workflow:**
1. Receive: Definition question
2. Detect: Complexity 2 → Quick answer
3. Answer: "SQL databases use structured tables with predefined schemas (e.g., PostgreSQL). NoSQL databases use flexible data models (e.g., MongoDB, Redis) suitable for unstructured data."
4. Confidence: 0.95 (standard definitions)
5. Output: Direct answer with confidence

---

### Example 4: Technical Verification (Quick)

**Question:** "Is this Python syntax valid? `my_list = [1, 2, 3]; print(my_list[0])`"

**Complexity:** 1 point
- Single question
- Verifiable
- No ambiguity
- Low stakes

**Workflow:**
1. Receive: Code verification
2. Detect: Complexity 1 → Quick answer
3. Answer: "Yes, this is valid Python syntax. It creates a list and prints the first element (1)."
4. Confidence: 1.0 (syntactic correctness is verifiable)
5. Output: "Yes, valid Python. Output: 1. Confidence: 1.0"

---

## Escalation Rules

### When to Escalate from Quick Answer to Hybrid

**Trigger 1:** Confidence uncertainty
- You start answering, realize you're not sure
- Example: "I think X, but I'm not confident"
- Action: Pause, switch to hybrid (light decomposition)

**Trigger 2:** Hidden complexity discovered
- Question seems simple, but has multiple dimensions
- Example: "Is React better?" → depends on team, project, timeline
- Action: Escalate to hybrid, identify factors

**Trigger 3:** User requests clarification
- User says: "But what about Y factor?"
- Indicates you missed something
- Action: Escalate to hybrid or full DSVSR

### When to Escalate from Quick Answer to Full DSVSR

**Trigger:** User requests high confidence
- User says: "I need to be confident in this"
- Original question was simple, but stakes just increased
- Action: Start full DSVSR from beginning

---

## Time Budget

| Step | Time |
|------|------|
| Receive + Detect | 30 sec |
| Answer + Confidence | 1-2 min |
| Metadata + Output | 30 sec |
| **Total** | **2-3 minutes** |

---

## Quality Checklist

Before sending quick answer, verify:

- ☐ Question understood correctly (re-read once)
- ☐ Answer is direct and clear (not hedging)
- ☐ Confidence is honest (not inflated or deflated)
- ☐ Caveats stated if relevant
- ☐ No important nuance missed (re-scan question)
- ☐ Answer is actionable (if decision-oriented)

---

## Common Mistakes to Avoid

### Mistake 1: Over-Explaining Simple Answers

**Wrong:** "Well, Python was actually released in 1991, though there were earlier drafts in 1989, and the first major version was in 1994, and..."

**Right:** "Python was released in 1991."

**Fix:** Keep simple answers simple. Add nuance only if user asks.

### Mistake 2: Under-Confident on Well-Known Facts

**Wrong:** "I think Python was released around 1991, but I'm not sure. Confidence: 0.60"

**Right:** "Python was released in 1991. Confidence: 0.99"

**Fix:** Historical facts and well-documented information deserve high confidence.

### Mistake 3: Answering a Question That Needs Escalation

**Wrong:** "Should we pivot to enterprise?" [Quick answer without decomposing the decision]

**Right:** "This needs deeper analysis. Let me decompose this into sub-factors: market fit, team readiness, financial impact, customer risk..."

**Fix:** Use complexity heuristics honestly. Don't force complex questions into quick answers.

### Mistake 4: Skipping Inline Confidence

**Wrong:** "React and Vue are both good. Vue might be faster to develop with in your case."

**Right:** "React and Vue are both solid. Vue might be slightly faster to develop with. Confidence: 0.75, as this depends on team experience."

**Fix:** Always include confidence, even in quick answers.

---

## Key Principles

1. **Speed is the point** — Quick answers should feel effortless
2. **Accuracy still matters** — Don't sacrifice correctness for speed
3. **Confidence is honest** — Mark your uncertainty clearly
4. **Escalate generously** — If you doubt, escalate
5. **User-focused** — Answer what they asked, not more
