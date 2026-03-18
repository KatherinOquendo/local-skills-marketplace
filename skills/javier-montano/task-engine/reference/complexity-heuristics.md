# Complexity Heuristics Reference

This document provides decision frameworks for determining when to use the full DSVSR protocol versus the fast path for simple questions.

## Decision Matrix: DSVSR vs. Fast Path

### The Complexity Score

For each question, evaluate these signals and assign points:

| Signal | Simple (0 pts) | Moderate (1 pt) | Complex (2 pts) |
|--------|---|---|---|
| **Word Count** | < 20 words | 20-50 words | > 50 words |
| **Question Type** | Factual, single-domain | Multi-domain, some strategy | Multi-domain, strategic, open-ended |
| **Ambiguity** | Low (one valid interpretation) | Moderate (2-3 interpretations) | High (many interpretations) |
| **Stakes** | Low (informational, no impact) | Medium (operational, some impact) | High (strategic, decision-driving) |
| **Dependencies** | None (standalone) | 1-2 dependencies | Multiple interconnected factors |
| **Time Sensitivity** | Non-urgent | Some time pressure | Urgent AND complex |
| **Domain Expertise Required** | General knowledge | Specialized knowledge | Multiple specialties |
| **Prior Context in Thread** | None (fresh question) | Some relevant context | Extensive relevant context |

### Activation Rules

**Low Complexity (Score 0-2 points):** Use FAST PATH
- Answer directly with inline confidence
- Minimal metadata
- Skip decomposition and verification
- Suitable for factual lookups, simple advice

**Moderate Complexity (Score 3-5 points):** Use HYBRID PATH
- Light decomposition (2-3 sub-problems)
- Standard verification
- Include metadata
- Still relatively quick

**High Complexity (Score 6+ points):** Use FULL DSVSR
- Complete decomposition (3+ sub-problems)
- Full verification (logic, facts, completeness, bias)
- Synthesis with confidence weighting
- Reflection and iteration if needed
- Comprehensive metadata

---

## Quick Complexity Detector

Before answering, scan for red flags:

**Red flags for complexity:**
- Multiple "and"s, "or"s, "versus"s in the question
- Keywords: "how should we", "what's the best", "trade-off", "strategy", "architecture"
- Embedded questions ("By the way, what about X?")
- Contradictions or tensions in the premise
- User asking for "high confidence" or "thorough analysis"
- Decisions with irreversible consequences
- Multi-disciplinary question (technical + business + people)
- Future prediction or causality ("will this cause...?")

**Green flags for simplicity:**
- Single, clear question
- Factual lookup ("What year did X happen?")
- Unambiguous answer ("Is this syntax valid?")
- Informational purpose ("Explain this concept")
- No dependencies or prerequisites
- Quick verification possible

---

## Decision Trees

### Decision Tree 1: Complexity Assessment

```
START: Received a question

Q1: Is this a straightforward factual lookup?
├── YES → FAST PATH (no DSVSR needed)
└── NO → Continue to Q2

Q2: Does the question contain 2+ decision factors or trade-offs?
├── NO → FAST PATH (still simple)
└── YES → Continue to Q3

Q3: Does answering require knowledge from multiple domains?
├── NO → HYBRID PATH (light decomposition)
└── YES → Continue to Q4

Q4: Are the consequences of being wrong significant?
├── NO → HYBRID PATH
└── YES → Continue to Q5

Q5: Does the question explicitly ask for high confidence or thorough analysis?
├── YES → FULL DSVSR
└── NO → Continue to Q6

Q6: Does the answer depend on information not yet available?
├── NO → HYBRID PATH
└── YES → FULL DSVSR (retrieve missing info)

END: Use selected path
```

### Decision Tree 2: Mid-Analysis Escalation

```
SITUATION: You started with FAST or HYBRID, then encountered low confidence

Q1: Is confidence currently below 0.70?
├── NO → Continue with current path
└── YES → Continue to Q2

Q2: Would increasing confidence require sub-problem decomposition?
├── NO → Continue with current path (document the gap)
└── YES → Continue to Q3

Q3: Is there time to escalate to FULL DSVSR?
├── NO → Deliver with confidence caveat
└── YES → Escalate to FULL DSVSR

Q4: After escalation, does confidence reach 0.85+?
├── YES → Deliver with updated metadata
└── NO → Deliver with explicit limitations

END: Output answer with appropriate confidence level
```

---

## Signal Details: Understanding Complexity

### Signal 1: Word Count

**Simple (< 20 words):** "What year was Python released?"
**Moderate (20-50 words):** "How should we refactor our authentication system to support OAuth and still maintain backward compatibility?"
**Complex (> 50 words):** "We're considering pivoting our product to focus on enterprise customers. The market looks large, but we'd need to build new features, hire sales staff, and change our entire go-to-market. We're also worried about losing current customers. Should we do this?"

**Why word count matters:**
- More words = more concepts
- More concepts = more dependencies
- More dependencies = higher complexity

---

### Signal 2: Question Type

**Factual:** "What is the capital of France?"
- Single answer
- Verifiable
- No judgment required

**Conceptual:** "Explain the difference between SQL and NoSQL databases"
- Comparison/explanation
- Some judgment on framing
- Moderate complexity

**Advisory:** "What database should we use for this project?"
- Requires trade-off analysis
- Multiple valid answers
- Judgment on context fit

**Strategic:** "How should we evolve our product roadmap to stay competitive in a changing market?"
- Multiple domains (technical, business, market)
- Long-term implications
- Irreversible decision
- High complexity

---

### Signal 3: Ambiguity

**Low:** "Is Python a compiled or interpreted language?"
- Single interpretation
- Possible pedantic nuance, but basically unambiguous

**Moderate:** "Should we hire more engineers?"
- What does "hire more" mean? (absolute number? percentage increase?)
- What role? (engineers in what discipline?)
- For what duration? (short-term? long-term?)
- 2-3 reasonable interpretations

**High:** "How do we build a better product?"
- "Better" for whom? (customers? business? team?)
- "Better" in what dimension? (features? performance? reliability? UX?)
- What's the baseline? (better than today? than competitors?)
- Dozens of interpretations

**Technique:** List 3+ interpretations of the question. If you get more than 2, it's high ambiguity.

---

### Signal 4: Stakes

**Low:** "What's the syntax for list comprehension in Python?"
- Wrong answer: You'll Google it again
- No business impact

**Medium:** "What's the best Python testing framework?"
- Wrong answer: Team adopts less-than-optimal tool
- Project impact, reversible

**High:** "Should we use Python or Go for our new microservices?"
- Wrong answer: Year of poor performance, maintenance burden, team frustration
- Business impact, partially irreversible (rewrite is expensive)
- Affects hiring, tech culture, roadmap

**High-Stakes Examples:**
- Hiring decisions
- Strategic pivots
- Architecture choices
- Customer contracts
- Security/compliance decisions

---

### Signal 5: Dependencies

**None (Standalone):**
- "What is the capital of France?"
- Answer is independent of other knowledge

**1-2 Dependencies:**
- "Should we use PostgreSQL?" depends on (1) scale expectations, (2) team expertise
- Can be addressed sequentially

**Multiple Interconnected:**
- "Should we pivot to enterprise?" depends on:
  - Market size (competitive positioning)
  - Product fit (technical readiness)
  - Team capability (hiring constraints)
  - Financial runway (which depends on churn, which depends on product strategy)
  - Customer reaction (segments us: keep SMB? both? strategic choice)
- Dependencies form a web, not a chain

**Technique:** Draw dependency graph (see DECOMPOSE stage). If graph has cycles or >5 nodes, high complexity.

---

### Signal 6: Time Sensitivity

**Non-Urgent:**
- "What's the history of containerization?"
- Can research thoroughly

**Some Time Pressure:**
- "What database should we use for our new project?"
- Needed soon, but not today
- Can invest 2-3 hours

**Urgent AND Simple:**
- "Is server X down? (quick check)"
- Immediate answer needed, simple verification
- FAST PATH despite urgency

**Urgent AND Complex:**
- "Client is leaving unless we do X. Should we do it?"
- Immediate answer needed, complex decision
- FULL DSVSR with time-boxed iterations (30-60 min)

---

### Signal 7: Domain Expertise

**General Knowledge:**
- "What's the capital of France?"
- "Explain how photosynthesis works"
- No specialized training needed

**Specialized Knowledge:**
- "How do we optimize our PostgreSQL queries?"
- "What's the best OAuth flow for our use case?"
- Requires domain expertise, but one domain

**Multiple Specialties:**
- "Should we hire this VP of Sales?" (recruiting, compensation, culture, team dynamics)
- "How should we restructure our organization?" (org design, culture, business strategy, people management)
- Requires multiple experts or deep cross-functional knowledge

---

### Signal 8: Prior Context

**No Context:**
- Question is self-contained, no thread history matters
- Example: "What's the syntax for async/await?"

**Some Context:**
- Question references prior conversation, but answer can stand alone
- Example: Previous discussion about authentication, now asking "Which OAuth library should we use?"

**Extensive Context:**
- Understanding requires reading multiple thread messages
- Answer builds on prior discussion
- Implicit assumptions from context

**Why it matters:**
- More context = more information to process
- More information = more potential for misalignment
- Requires information recursion (see recursion-protocol.md)

---

## Worked Examples: Complexity Scoring

### Example 1: Simple Question

**Question:** "What year was React released?"

**Scoring:**
- Word count: 8 words (0 pts)
- Question type: Factual (0 pts)
- Ambiguity: None (0 pts)
- Stakes: Low (0 pts)
- Dependencies: None (0 pts)
- Time sensitivity: Non-urgent (0 pts)
- Domain expertise: General (0 pts)
- Prior context: None (0 pts)

**Total: 0 points → FAST PATH**

**Response:**
"React was released by Facebook in 2013. Confidence: 0.98."

---

### Example 2: Moderate Question

**Question:** "We're considering switching from React to Vue. Our team has React experience. Vue might be faster to develop with. What should we do?"

**Scoring:**
- Word count: 29 words (1 pt)
- Question type: Advisory (1 pt)
- Ambiguity: What's "faster"? Performance or dev velocity? (1 pt)
- Stakes: Medium (project impact, reversible) (1 pt)
- Dependencies: Team skills, project timeline, business goals (1 pt)
- Time sensitivity: Some (1 pt)
- Domain expertise: Specialized (frontend architecture) (1 pt)
- Prior context: Depends on thread (0-1 pts)

**Total: 6-7 points → FULL DSVSR**

**Decomposition:**
- SP-1: What are Vue vs. React trade-offs for our specific project?
- SP-2: What's the switching cost (learning curve, ecosystem, migration)?
- SP-3: Does the performance gain justify the switching cost?
- SP-4: What's the team's preference, and how important is that?

---

### Example 3: Edge Case: Looks Simple, Is Complex

**Question:** "Should we hire this person?"

**Initial Intuition:** Simple (single yes/no)

**Actual Scoring:**
- Word count: 5 words (0 pts) — but question is deceptively deep
- Question type: Strategic (hiring decisions are high-impact) (2 pts)
- Ambiguity: "Suitable for what role?" "Success defined how?" "Timeline?" (2 pts)
- Stakes: HIGH (wrong hire damages team, culture, productivity) (2 pts)
- Dependencies: Role clarity, candidate skills, team fit, compensation, market (2 pts)
- Time sensitivity: Can vary (non-urgent → urgent) (1-2 pts)
- Domain expertise: Multiple (recruiting, management, culture, domain expertise) (2 pts)
- Prior context: Usually substantial (candidate history, team needs) (1 pt)

**Total: 10-12 points → FULL DSVSR (despite brief question)**

**Lesson:** Word count is not destiny. Short questions can hide deep complexity. Look at stakes, domain expertise, and dependencies.

---

### Example 4: Edge Case: Looks Complex, Is Simple

**Question:** "You mentioned earlier that our conversion rate dropped. I assume it's because of the price increase you implemented last month. Was that the cause?"

**Initial Intuition:** Complex (multi-factor analysis)

**Actual Scoring:**
- Word count: 38 words (1 pt)
- Question type: Analytical (1 pt)
- Ambiguity: Clear assumption being tested (0 pts)
- Stakes: Medium (understanding root cause) (1 pt)
- Dependencies: None really (causal claim is simple to test) (0 pts)
- Time sensitivity: Informational (0 pts)
- Domain expertise: General analytics (0 pts)
- Prior context: Yes, but question is scoped (1 pt)

**Total: 3-4 points → HYBRID PATH**

**Response:**
"Likely a factor, but not the only one. Confidence breakdown:
- Price increase: 40-60% of drop (0.78 confidence)
- Competitive factors: 20-30% (0.65 confidence)
- Traffic quality shift: 15-25% (0.62 confidence)

I'd recommend analyzing [specific metrics] to isolate the actual driver. Would take 30 min of analysis to reach 0.85+ confidence on breakdown."

**Lesson:** Apparent complexity can be simple if the question is well-scoped. The user already identified a hypothesis; you're just validating it.

---

## Auto-Escalation Protocol

### When to Escalate from Fast Path to Hybrid

**Trigger 1: Low inline confidence**
- You started answering, confidence is clearly below 0.70
- Action: Pause. Restructure as HYBRID with decomposition

**Trigger 2: Hidden complexity discovered**
- You realized the question has more dimensions than initially apparent
- Action: Re-decompose and restart analysis

**Trigger 3: User pushback**
- User says "But what about [factor you didn't consider]?"
- Action: Escalate to HYBRID or FULL DSVSR

---

### When to Escalate from Hybrid to Full DSVSR

**Trigger 1: Global confidence below 0.80 after hybrid verification**
- Hybrid iteration didn't improve enough
- Action: Full DSVSR with explicit reflection

**Trigger 2: Conflicting sub-answers**
- Two factors point in opposite directions
- Action: Full DSVSR to resolve conflicts

**Trigger 3: Stakeholder requests high confidence**
- User asks for 0.90+ confidence
- User needs justification for decision
- Action: Full DSVSR with metadata

---

### Escalation Output Template

When escalating, communicate clearly to the user:

```
Initial assessment: [FAST/HYBRID path]
Complexity discovered: [What made you escalate?]
Revised path: [FULL DSVSR]

Reason: [Brief explanation of why higher rigor needed]

This will require [estimated time] of analysis. Shall I proceed?
```

---

## Context-Specific Heuristics

### Hiring Decisions
- **Always complexity ≥ 6 points** (even if question is brief)
- **Always use FULL DSVSR**
- Rationale: Wrong hire has compounding consequences

### Technical Architecture Decisions
- **Usually complexity ≥ 6 points**
- Exceptions: Adding a known library in familiar stack (HYBRID)
- Rationale: Architecture decisions have long-term lock-in

### Factual Questions
- **Usually complexity ≤ 2 points (FAST PATH)**
- Exceptions: When factual answer is ambiguous or context-dependent
- Example: "Does Vue or React have better performance?" is complex (context-dependent) vs. "Is React a library or framework?" is simple (factual)

### Debugging / Troubleshooting
- **Evaluate based on problem scope**
- Single isolated bug: FAST/HYBRID
- System-wide issue: FULL DSVSR

### Strategic Business Questions
- **Always complexity ≥ 6 points (FULL DSVSR)**
- Rationale: Strategy affects entire company direction

---

## Key Takeaways

1. **Complexity is multi-dimensional** — Word count alone doesn't determine path. Use the full scoring matrix.
2. **Low confidence forces escalation** — If you hit 0.65 confidence in FAST path, escalate to HYBRID or FULL.
3. **Stakes matter most** — High-stakes decisions always warrant full DSVSR, even if they seem simple.
4. **Watch for hidden complexity** — Short questions can hide deep dependencies (hiring, architecture).
5. **Time-box escalations** — If escalating to FULL DSVSR, set a time limit to avoid analysis paralysis.
6. **Re-score as you learn** — Initial complexity assessment may change as you gather information.
