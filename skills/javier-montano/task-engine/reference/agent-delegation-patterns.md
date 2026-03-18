# Agent Delegation Patterns Reference

This document defines when, how, and why to delegate sub-problems to specialized subagents, along with confidence aggregation and fallback protocols.

## Delegation Decision Framework

### When to Delegate

Delegate a sub-problem to a specialized subagent when:

**✓ Delegate if:**
1. Sub-problem requires domain expertise outside your general knowledge
2. Subagent would provide significantly higher confidence than inline solving
3. Domain has specialized tools or methodologies available
4. Parallel processing saves time (multiple sub-problems can run simultaneously)
5. Risk of error is high, so specialization is worth the latency cost

**✗ Don't delegate if:**
1. Sub-problem is simple enough to solve inline with confidence > 0.75
2. Subagent unavailable (would delay response more than inline solve)
3. Sub-problem is already well-understood from prior analysis
4. User wants single-source response (don't fragment authority)

---

## Domain-to-Specialist Routing Matrix

| Sub-Problem Domain | Primary Specialist | Signals for Delegation |
|---|---|---|
| **Mathematical/Statistical** | Math-reasoning subagent | Probability, statistics, optimization, proofs |
| **Code Analysis/Debugging** | Code-analysis subagent | Bug diagnosis, performance analysis, code review |
| **Legal/Compliance** | Legal-reasoning subagent | Contract interpretation, regulatory compliance, liability |
| **Data Analysis** | Data-analysis subagent | Large dataset queries, statistical modeling, trend analysis |
| **Domain-Specific Technical** | Domain expert subagent | Molecular biology, physics, medicine, finance domains |
| **Research/Literature** | Research subagent | Survey of academic literature, state-of-the-art review |
| **Creative/Design** | Creative subagent | UI/UX design, copywriting, brand positioning |
| **General Knowledge** | Handle inline | Facts, explanations, common advice |

### Decision Tree: Delegate or Handle Inline?

```
Sub-problem identified: [description]

Q1: Is this general knowledge or common domain?
├── YES → Handle inline (confidence likely sufficient)
└── NO → Continue to Q2

Q2: Is a specialist subagent available?
├── NO → Handle inline with lower confidence caveat
└── YES → Continue to Q3

Q3: Would specialization materially improve confidence?
├── NO (would increase only 0-5 points) → Handle inline
└── YES (would increase 10+ points) → Continue to Q4

Q4: Is time available for delegation (subagent latency)?
├── NO (urgent response needed) → Handle inline, plan for follow-up
└── YES → Delegate

ACTION: Delegate to specialist
```

---

## Subagent Contract

### What You Send to Subagent

When delegating, provide a clear, scoped request:

```
SUBAGENT REQUEST:
Domain: [math | code | legal | data | research | creative]
Sub-problem: [Specific question, 1-2 sentences]

Context: [Relevant background, constraints]

Required Output:
- Answer: [Concise answer to the sub-problem]
- Confidence: [0.XX, with justification]
- Evidence: [Key evidence supporting the answer]
- Limitations: [What could weaken this answer?]
- Time-boxed: [Deliver in X minutes]
```

### Example Delegation Request

```
SUBAGENT REQUEST:
Domain: Code-analysis
Sub-problem: Why is our Django ORM query slow for the customer list endpoint?

Context:
- Database has 50K customers
- Query retrieves customer.name, customer.email, related_orders.count
- Currently takes 2-3 seconds
- Using Django ORM with select_related

Required Output:
- Root cause of slowness
- Confidence: target 0.88+
- Specific fix recommendation (code change)
- Performance improvement estimate
- Time-boxed: 10 minutes
```

### What Subagent Returns

Expect this structure:

```
SUBAGENT RESPONSE:
Domain: [As provided]
Sub-problem: [As provided]

ANSWER:
[Concise answer]

CONFIDENCE: [0.XX]

JUSTIFICATION:
[Why this confidence level, what evidence supports it]

EVIDENCE:
- Point 1: [Specific data or reasoning]
- Point 2: [Specific data or reasoning]

LIMITATIONS:
- Could change if [condition]
- Haven't verified [aspect]
- Assumes [assumption]

FOLLOW-UP (if needed):
[If confidence is low, what would improve it?]
```

---

## Confidence Aggregation from Subagents

### Basic Aggregation (Single Sub-Problem)

When one subagent solves one sub-problem:

**Rule:** Global confidence on that sub-problem = subagent confidence × (1 - delegation_uncertainty)

Where delegation_uncertainty accounts for:
- Misalignment between request and actual problem (0.05-0.15)
- Subagent misunderstanding context (0.05-0.10)
- Translation error (0.05-0.10)

**Calculation:**
```
Subagent returned confidence: 0.88
Delegation uncertainty: 0.10 (small risk of misalignment)
Effective confidence: 0.88 × (1 - 0.10) = 0.88 × 0.90 = 0.79

Use 0.79 confidence for this sub-problem in global aggregation
```

### Complex Aggregation (Multiple Subagents)

When multiple subagents solve different sub-problems:

**Rule:** Aggregate using same logic as sub-problems

```
Global = Σ(subagent_confidence × importance) / Σ importance

Example:
SP-1 (Math subagent): 0.90 confidence, importance 1.0
  → Effective: 0.90 × 0.90 (delegation) = 0.81
SP-2 (Code subagent): 0.85 confidence, importance 0.8
  → Effective: 0.85 × 0.90 (delegation) = 0.765
SP-3 (Inline): 0.75 confidence, importance 0.7
  → Effective: 0.75 × 1.0 (no delegation) = 0.75

Global = (0.81×1.0 + 0.765×0.8 + 0.75×0.7) / (1.0 + 0.8 + 0.7)
       = (0.81 + 0.612 + 0.525) / 2.5
       = 1.947 / 2.5
       = 0.779
```

### Handling Subagent Conflicts

When two subagents give conflicting answers:

**Resolution hierarchy:**
1. **Verify both answers** — Which one did you misunderstand?
2. **Check subagent confidence** — Did they flag the conflict?
3. **Assess relevance** — Are they answering slightly different questions?
4. **Use conflict resolution hierarchy** (from SYNTHESIZE stage):
   - Verified facts > Logical deductions > Expert consensus > Inference > Speculation

**Example:**
```
Math subagent: "Probability of success is 12%" (0.88 confidence)
Data subagent: "Historical data shows 18% success rate" (0.82 confidence)

Resolution:
- Math subagent likely performed theoretical calculation
- Data subagent used empirical data
- Which is more relevant? (Depends on whether historical conditions match current)
- Recommendation: "Theoretical expectation is 12%, but historical empirical rate is 18%.
  Confidence: Use 18% as baseline (0.82), acknowledge 12% theoretical lower bound."
```

---

## Fallback Protocol: When Subagent Unavailable

If a specialized subagent is unavailable (too slow, not accessible, insufficient capacity):

**Fallback decision tree:**
```
Subagent unavailable

Q1: Can I solve this inline with reasonable confidence?
├── YES (confidence 0.70+) → Solve inline, mark as "without specialist review"
└── NO (confidence < 0.70) → Continue to Q2

Q2: Is this sub-problem critical to the global answer?
├── NO (low importance) → Skip this sub-problem, note as gap
└── YES (high importance) → Continue to Q3

Q3: Can I get specialist input through alternative means?
├── YES (ask user, reference library, document review) → Do it
└── NO → Proceed with inline solve, cap confidence at 0.65

OUTPUT: Always note the fallback in metadata
```

---

## Sequential Delegation (Dependent Sub-Problems)

### Pattern: A → B → C (Chain)

When sub-problems depend on each other:

```
SP-1 (Delegate to Math): "What's the optimal pricing formula?"
    ↓ (sends result to SP-2)
SP-2 (Delegate to Data): "Given that pricing formula, what's revenue projection?"
    ↓ (sends result to SP-3)
SP-3 (Inline): "Synthesize both results into recommendation"
```

**Execution:**
1. Delegate SP-1, wait for result
2. Provide result to SP-2 delegation request
3. Delegate SP-2, wait for result
4. Synthesize with SP-3 inline

**Confidence calculation:**
- Errors compound in chains
- Global confidence = min(all sub-confidences) for critical chains
- If SP-1 is 0.85 and SP-2 is 0.78, global ≤ 0.78 (chain is only as strong as weakest link)

### Pattern: Parallel Delegation (Independent Sub-Problems)

When sub-problems are independent:

```
SP-1 (Math): "Optimization calculation" [parallel]
SP-2 (Code): "Performance analysis" [parallel]
SP-3 (Data): "Trend analysis" [parallel]
SP-4 (Inline): "Synthesize all three"
```

**Execution:**
1. Delegate all three simultaneously (if resources allow)
2. Wait for all to complete
3. Synthesize results

**Confidence calculation:**
- No compounding errors
- Global confidence = weighted average of all sub-confidences
- Parallelization saves time without confidence penalty

---

## Subagent Selection Guidelines

### Math-Reasoning Subagent

**Delegate when:**
- Sub-problem requires: probability, statistics, optimization, proof, mathematical modeling
- Examples:
  - "What's the probability of success given these parameters?"
  - "How should we optimize this allocation problem?"
  - "Prove that this algorithm converges"
  - "What's the statistical confidence interval for this estimate?"

**Expect confidence:** 0.88-0.98 (math is precise)

**Limitations:**
- Assumptions matter (garbage in → garbage out)
- Real-world data may not fit mathematical assumptions
- Oversimplification risk

---

### Code-Analysis Subagent

**Delegate when:**
- Sub-problem requires: debugging, performance analysis, code review, architecture evaluation
- Examples:
  - "Why is this query slow?"
  - "What's the security vulnerability in this code?"
  - "Can this algorithm handle 100K users?"
  - "Which framework is better for our use case?"

**Expect confidence:** 0.80-0.90 (depends on code clarity and availability)

**Limitations:**
- Needs access to actual code (not pseudocode)
- Performance analysis is context-dependent
- Framework choice depends on team expertise (code-analysis subagent can't know your team)

---

### Legal-Reasoning Subagent

**Delegate when:**
- Sub-problem requires: contract interpretation, regulatory compliance, liability assessment, licensing
- Examples:
  - "Are we compliant with GDPR for our data retention?"
  - "What are the liability implications of this ToS?"
  - "Can we use this open-source library given our commercial use?"

**Expect confidence:** 0.78-0.88 (legal has nuance, jurisdiction matters)

**Limitations:**
- Not a lawyer (disclaimer always needed)
- Jurisdiction-specific (may not apply to your situation)
- Regulatory changes happen (advice may age)

---

### Data-Analysis Subagent

**Delegate when:**
- Sub-problem requires: dataset querying, statistical modeling, trend analysis, anomaly detection
- Examples:
  - "What caused the spike in support tickets last week?"
  - "Is our churn trend improving?"
  - "What are the top factors driving customer acquisition?"
  - "Forecast next quarter revenue"

**Expect confidence:** 0.75-0.90 (depends on data quality and dataset size)

**Limitations:**
- Garbage data → garbage analysis
- Confounding variables may not be obvious
- Sample size matters (small datasets = low confidence)

---

### Research Subagent

**Delegate when:**
- Sub-problem requires: academic literature review, state-of-the-art survey, published research
- Examples:
  - "What's the current best practice for distributed transactions?"
  - "What does research say about remote work productivity?"
  - "Survey recent papers on LLM alignment"

**Expect confidence:** 0.80-0.95 (published research is vetted)

**Limitations:**
- Limited to published research (may miss industry practice)
- Publication lag (best practice moves faster than papers)
- Research may not apply to your specific context

---

### Creative Subagent

**Delegate when:**
- Sub-problem requires: design, copywriting, positioning, UX decisions
- Examples:
  - "What should our brand voice be?"
  - "How should we position feature X?"
  - "Design a user onboarding flow"

**Expect confidence:** 0.65-0.80 (creative is subjective)

**Limitations:**
- Subjective (depends on taste, audience, brand)
- Need to validate with real users
- Not a substitute for design thinking process

---

## Metadata for Delegated Answers

When you delegate and aggregate, your metadata should reflect it:

```
---
📊 REASONING METADATA:
• Global confidence: [0.XX]
• Sub-problem breakdown:
  - SP-1 (delegated to [specialist]): [0.XX]
  - SP-2 (delegated to [specialist]): [0.XX]
  - SP-3 (inline): [0.XX]
• Delegation notes:
  - [Specialist 1]: [What they solved, any limitations]
  - [Specialist 2]: [What they solved, any limitations]
• Aggregation method: [Weighted average | Min of chain | Other]
• Fallbacks used: [None | [Description of any fallbacks]]
• Sources: [Subagent 1, Subagent 2, internal data, thread context]
• Weaknesses: [Specify any gaps from delegation]
• Verification: [All delegated results checked | Conflicts identified]
---
```

---

## Real-World Example: Hiring Decision with Delegation

**Problem:** "Should we hire this VP of Sales candidate?"

**Initial decomposition:**
- SP-1: Does she have strong sales track record? (Code/data analysis?)
- SP-2: Can she execute our sales motion? (Sales expertise?)
- SP-3: Does she fit our culture? (Human judgment? Not delegable)
- SP-4: Is compensation fair? (Legal/Data?)

**Delegation plan:**
```
SP-1: Reference-check analysis
  Delegate to: Data-analysis subagent
  Request: "Analyze her past job performance (tenure, ramp time, quota achievement)"
  Expected confidence: 0.85

SP-2: Sales motion execution
  Delegate to: Domain expert (VP of Sales network)
  Request: "Assess if her experience maps to our B2B SaaS motion"
  Expected confidence: 0.80

SP-3: Culture fit
  Handle inline: Internal assessment, team interviews needed
  Confidence: Start at 0.60, improve after team input

SP-4: Compensation fairness
  Delegate to: Market-data research
  Request: "What's market rate for VP Sales in our region/stage?"
  Expected confidence: 0.90
```

**Execution:**
1. Delegate SP-1, SP-2, SP-4 in parallel (10-15 min turnaround)
2. Handle SP-3 inline (request team input)
3. Aggregate results

**Aggregation:**
```
SP-1: 0.85 × 0.90 (delegation) = 0.765
SP-2: 0.80 × 0.90 (delegation) = 0.72
SP-3: 0.65 × 1.0 (inline) = 0.65
SP-4: 0.90 × 0.90 (delegation) = 0.81

Importance weights:
  SP-1: 1.0 (foundational)
  SP-2: 1.0 (foundational)
  SP-3: 0.9 (culture fit critical)
  SP-4: 0.5 (nice to have)

Global = (0.765×1.0 + 0.72×1.0 + 0.65×0.9 + 0.81×0.5) / (1.0+1.0+0.9+0.5)
       = (0.765 + 0.72 + 0.585 + 0.405) / 3.4
       = 2.475 / 3.4
       = 0.728

Global confidence: 0.73 (below 0.85 target)

Gap: Mostly from culture fit (SP-3, 0.65) which is critical
Recommendation: Complete team interviews before making offer. If team feedback is positive, confidence → 0.83
```

---

## Key Takeaways

1. **Delegate for specialization** — Use subagents to reach higher confidence faster
2. **Document the contract** — Be clear about what you're asking and what you expect
3. **Apply delegation uncertainty** — Reduce subagent confidence by 10% for aggregation
4. **Parallel when possible** — Independent sub-problems can run simultaneously
5. **Verify conflicts** — When subagents disagree, diagnose the source
6. **Mark in metadata** — Always note which sub-problems were delegated
7. **Have fallbacks** — Know what to do if subagent is unavailable
