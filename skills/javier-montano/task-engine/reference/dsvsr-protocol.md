# DSVSR Protocol: Detailed Reference

The DSVSR (Decompose-Solve-Verify-Synthesize-Reflect) protocol is the engine of complex problem solving. This reference document provides detailed methodology, decision trees, and worked examples for each stage.

## Stage 1: DECOMPOSE

Breaking a problem into atomic sub-problems is the most critical step. A poor decomposition cascades into weak answers.

### Methodology

**Step 1.1: Identify the core question**
- Strip away context, narrative, and emotional framing
- Ask: "What specifically needs to be answered?"
- Example: "Should we hire this candidate?" → core question = "Will this person contribute positively to the team?"

**Step 1.2: List all components requiring answers**
- Read the question line-by-line
- Mark every "and", "vs", "or" as a potential split
- Extract embedded questions ("By the way, what about X?")
- Identify assumptions that need verification

**Step 1.3: Map dependencies**
Look for keywords:
- "If...then" → dependency exists
- "Because" → causal dependency
- "Before/after" → sequencing dependency
- "Assuming X is true" → conditional dependency

**Step 1.4: Determine solve order**
- Foundation problems first (no dependencies)
- Middle-layer problems depend on foundations
- Synthesis problems depend on lower layers
- Order by urgency and blocking risk

**Step 1.5: Tag domains**
- Technical: Code, systems, algorithms, architecture
- Business: Strategy, market, ROI, risk, competition
- Creative: Design, user experience, messaging, positioning
- Factual: Verifiable, historical, empirical
- Analytical: Logic, reasoning, inference
- Human: Psychology, motivation, culture, team dynamics

### Output Format

```
DECOMPOSITION ANALYSIS:
Problem: [Original question]
Core: [Stripped-down essential question]

Sub-problems identified: [N]

├── SP-1: [Atomic question 1]
│   Domain: [technical | business | creative | factual | analytical | human]
│   Dependencies: none
│   Priority: [1-3, with 1=foundational]
│
├── SP-2: [Atomic question 2]
│   Domain: [X]
│   Dependencies: SP-1
│   Priority: [X]
│
└── SP-3: [Atomic question 3]
    Domain: [X]
    Dependencies: SP-1, SP-2
    Priority: [X]

Solve order: SP-1 → SP-2 → SP-3
```

### Worked Example: Business Strategy Problem

**Original Problem:**
"We're considering pivoting our SaaS product to focus on the mid-market segment. The market opportunity looks big, but I'm concerned about execution risk, current customer churn, and whether we have the right team. Should we do this?"

**Decomposition:**

```
Core question: Can we successfully execute a market pivot to mid-market with acceptable risk?

Sub-problems identified: 6

├── SP-1: Market Size & Opportunity
│   Domain: business, factual
│   Dependencies: none
│   Priority: 1
│   Detail: How large is the mid-market opportunity, and how much TAM are we addressing?
│
├── SP-2: Current Competitive Position
│   Domain: business, factual
│   Dependencies: SP-1
│   Priority: 1
│   Detail: Who competes in mid-market? What are our competitive advantages/disadvantages?
│
├── SP-3: Product Fit & Technical Readiness
│   Domain: technical, business
│   Dependencies: SP-2
│   Priority: 1
│   Detail: Does our current product architecture support mid-market needs? What pivots required?
│
├── SP-4: Customer Churn Risk
│   Domain: business, analytical
│   Dependencies: SP-3
│   Priority: 2
│   Detail: If we pivot, how many current customers will we lose, and what's the revenue impact?
│
├── SP-5: Team Capability Assessment
│   Domain: human, business
│   Dependencies: SP-3
│   Priority: 2
│   Detail: Does our team have the skills/bandwidth to execute this pivot?
│
└── SP-6: Financial Runway & Risk
    Domain: business, analytical
    Dependencies: SP-4, SP-5
    Priority: 2
    Detail: Given churn and execution costs, do we have sufficient runway? What's break-even timeline?
```

---

## Stage 2: SOLVE

Answer each sub-problem with rigorous confidence calibration.

### Methodology

**For each sub-problem:**

1. **Gather relevant evidence** — What data, research, expertise, or reasoning applies?
2. **Construct the answer** — Build reasoning chain from evidence to conclusion
3. **Assess confidence** — Use the scale below with explicit justification
4. **Identify gaps** — What information would increase confidence?
5. **Flag constraints** — Time pressure, unavailable data, expertise gaps

### Confidence Scale (Detailed)

| Score | Label | Meaning | Evidence Required |
|-------|-------|---------|-------------------|
| 0.95-1.0 | Certain | Verifiable, non-disputed, reproducible | Direct measurement, mathematical proof, multiple sources agree, public facts |
| 0.85-0.94 | High | Strong reasoning, expert consensus, direct evidence | Published research, expert interview, company data, tested methodology |
| 0.70-0.84 | Moderate | Reasonable inference, partial evidence, some assumptions | Industry reports, analogous examples, expert judgment, limited data |
| 0.50-0.69 | Low | Educated guess, significant assumptions, limited support | Logical extrapolation, market research, one source, hearsay |
| 0.30-0.49 | Speculative | Hypothesis stage, minimal evidence, high uncertainty | Brainstorm, assumption, single mention, intuition |
| Below 0.30 | Unknowable | Should not attempt answer, declare the gap | Insufficient information to reason |

### Output Format

```
SP-[N]: [Sub-problem]

ANSWER:
[Concise, specific answer to the sub-problem]

CONFIDENCE: [0.XX]

JUSTIFICATION:
[Explicit reasoning for the confidence score]
[Which pieces of evidence support this level?]

WOULD INCREASE TO [0.XX] IF:
[Specific information that would strengthen confidence]

CONSTRAINTS:
[Time pressure? Unknown data? Expertise gaps?]
```

### Worked Example: Continuing the Business Strategy

**SP-1: Market Size & Opportunity**

```
ANSWER:
The mid-market SaaS space (100-500 employees) represents approximately $45-65B globally, growing at 18-22% CAGR. We're looking at a $8-12B serviceable opportunity in our vertical (project management), with current penetration at ~15%, suggesting $1.2-1.8B available market for new entrants.

CONFIDENCE: 0.82

JUSTIFICATION:
- Gartner and Forrester reports consistently show mid-market as fastest-growing segment (✓ published data)
- Multiple analyst firms overlap on TAM estimates within ±15% (✓ triangulation)
- Our vertical sizing matches industry analyst estimates (✓ alignment)
- However, our "serviceable opportunity" assumes we can capture mid-market customers, which may be overstated without distribution proof (⚠ assumption)
- Market reports are 12-18 months old; growth rates may have shifted (⚠ timeliness)

WOULD INCREASE TO 0.90+ IF:
- We conducted bottom-up analysis (count mid-market competitors, survey deployment)
- We interviewed 10+ mid-market prospects about their buying patterns
- We analyzed Gartner/Forrester 2024+ reports (not 2023 data)

CONSTRAINTS:
- Market sizing is inherently probabilistic; ±20% uncertainty is normal
- Vertical-specific data is less reliable than horizontal market data
```

**SP-2: Current Competitive Position**

```
ANSWER:
We face 4-6 direct competitors in mid-market (Monday, Asana, Jira, Wrike, Smartsheet). We have advantages in: ease-of-use (3+ NPS higher), custom integrations, and price flexibility. We have disadvantages in: brand recognition, sales infrastructure, and enterprise customer reference base. Relative market share: we're #6-7 in mid-market, ~8-12% of revenue from mid-market today.

CONFIDENCE: 0.78

JUSTIFICATION:
- Direct knowledge of product capabilities vs. competitors (✓ internal data)
- NPS data from our own customers comparing us to alternatives (✓ primary source)
- Publicly available competitor financials and customer lists (✓ public data)
- However, mid-market sales infrastructure assessment is subjective (⚠ bias risk)
- Competitor sales team size is private; estimate based on job postings (⚠ incomplete data)
- Market share estimate assumes mid-market deployment patterns; actual may vary (⚠ assumption)

WOULD INCREASE TO 0.88+ IF:
- We conducted win/loss analysis on last 20 mid-market deals
- We interviewed 5+ customers who evaluated multiple competitors
- We surveyed mid-market buyers on brand awareness and preference

CONSTRAINTS:
- Competitive advantage assessment is inherently subjective
- Mid-market buyer priorities may differ from our current SMB customer base
```

**SP-3: Product Fit & Technical Readiness**

```
ANSWER:
Our product is 60-70% aligned with mid-market needs. Required pivots: (1) advanced permissions/governance (2-3 sprints), (2) compliance certifications (SOC2 Type II: 3-4 months), (3) API-first integration architecture (4-6 sprints). Timeline to market-ready: 5-7 months. Major blocker: governance module scope creep risk — mid-market needs are diverse.

CONFIDENCE: 0.81

JUSTIFICATION:
- We analyzed 12 mid-market RFPs and mapped to our product backlog (✓ primary analysis)
- Engineering team sized each feature based on architecture review (✓ internal expertise)
- SOC2 timeline based on previous compliance projects in our portfolio (✓ empirical data)
- However, mid-market feature requests are still fuzzy; detailed requirements not yet gathered (⚠ assumption)
- Timeline estimates assume no competing priorities; actual may slip (⚠ risk factor)
- We haven't validated that these features solve top pain points in mid-market (⚠ incomplete validation)

WOULD INCREASE TO 0.90+ IF:
- We conducted detailed requirements gathering with 10+ mid-market prospects
- We built a working prototype of governance module and tested with real customers
- We finalized SOC2 audit schedule with external firm (vs. estimate)

CONSTRAINTS:
- Feature scope is still being refined; estimates may shift 30-50%
- Mid-market customization requests typically exceed estimates by 20-30%
```

---

## Stage 3: VERIFY

Cross-check every sub-answer against four dimensions.

### Verification Checklist

For each sub-answer, address:

**☐ LOGIC**
- Is the reasoning internally consistent?
- Do premises support the conclusion?
- Are there logical fallacies (false cause, hasty generalization, false dilemma)?
- Would a peer economist/engineer/strategist accept the logic chain?

*Technique: Red-team your own logic. Assume you're wrong. Where would the failure be?*

**☐ FACTS**
- Are all factual claims verifiable or qualified with confidence?
- Have I conflated opinion ("users prefer X") with fact?
- Are citations current and authoritative?
- Did I misinterpret data (correlation vs. causation)?

*Technique: For each factual claim, ask "How would I prove this to a skeptic?" If you can't easily answer, lower confidence or mark as assumption.*

**☐ COMPLETENESS**
- Have I considered all relevant perspectives (technical, business, user, competitive)?
- What major aspect am I NOT addressing?
- Who would disagree with this answer, and why?
- Is there a simpler explanation I'm overlooking?

*Technique: Steel-man the opposite view. What's the strongest objection to your answer?*

**☐ BIAS**
- Anchoring: Is my first intuition driving the answer, without exploring alternatives?
- Confirmation: Am I only finding evidence that supports my initial hypothesis?
- Availability: Am I overweighting recent or memorable examples?
- Authority: Am I accepting a framework because it's well-known, not because it fits this problem?

*Technique: Reverse your initial position. Try to argue the opposite. How strong is that case?*

### Verification Update Process

After verification, update confidence scores:
- If verification reveals flaws → confidence decreases
- If verification confirms reasoning → confidence increases by 5-10 points
- If verification reveals gaps → confidence stays same but rationale clarifies
- **If verification changes nothing → verification was superficial; retry**

### Worked Example: Verification of SP-4

**Original Answer (SP-4: Customer Churn Risk)**

"If we pivot to mid-market, current SMB customers will decline rapidly. I estimate 40-60% churn in Year 1, impacting $2-3M ARR. Older customers are more at risk than recent ones."

**Original Confidence: 0.65**

---

**VERIFICATION:**

**☐ LOGIC CHECK**
- Premise: "Product pivot creates misalignment" → true, product features shift
- Premise: "SMB customers can't use mid-market product" → WEAK. Mid-market features typically include SMB features
- Premise: "Older customers leave first" → Assumption, no evidence
- **Finding:** Logic chain is weak. Pivot doesn't necessarily drive churn; pricing/support changes are bigger factors.
- **Verdict:** Reasoning is incomplete. Need to separate product factors from go-to-market factors.

**☐ FACTS CHECK**
- "40-60% churn" — where does this come from? No data cited.
- "Older customers leave first" — contradicts SaaS data (retention typically improves with tenure)
- "$2-3M ARR impact" — based on what total ARR? Need specifics.
- **Finding:** Most claims are unsubstantiated. This is speculation, not analysis.
- **Verdict:** Significantly lower confidence warranted. Need actual churn models.

**☐ COMPLETENESS CHECK**
- I'm addressing product misalignment but NOT:
  - Pricing strategy (will we increase prices? that drives churn, not product)
  - Support model (will we reduce SMB support? that drives churn)
  - Parallel product strategy (could we run SMB and mid-market products? reduces churn)
  - Customer segmentation (not all SMB customers are at risk; high-growth SMBs stay)
- **Finding:** My answer is narrow. It conflates multiple factors.
- **Verdict:** Incomplete analysis. Should break into sub-factors: product, pricing, support, strategy.

**☐ BIAS CHECK**
- Anchoring: I assumed churn from product pivot without exploring alternatives
- Confirmation: I only looked for reasons churn would increase (mid-market-focused product), not decrease (easier to use, better integrated)
- Availability: Last company I know of did a pivot and lost customers → overweighting one example
- **Finding:** My initial intuition (pivot = churn) is driving the answer, not evidence.
- **Verdict:** Reverse position: Why might SMB customers stay? (Feature expansion, better support, pricing flexibility) This is equally plausible.

---

**VERIFICATION OUTCOME:**

```
REVISED ANSWER:
Churn impact depends on three factors:
1. Product misalignment: Estimated 15-25% churn from features misaligned with SMB needs
2. Pricing strategy: Unknown. If prices increase, 30-50% additional churn. If prices stay flat, minimal impact.
3. Go-to-market: If we reduce SMB support, 25-35% churn. If we maintain dual support, <10% churn.

Total churn range: 15-95%, depending on parallel product strategy.

Without clarity on pricing and support strategy, precise estimate is impossible.

REVISED CONFIDENCE: 0.52 (down from 0.65)

RATIONALE:
- My original answer masked uncertainty behind false precision
- Verification revealed three independent factors, not yet decided
- I can estimate factor ranges, but global estimate requires strategy decisions
- Recommend: Model churn under 3-4 scenarios (pivot + price increase, pivot + parallel product, etc.)

REVISED WOULD INCREASE TO 0.75+ IF:
- Leadership confirms pricing strategy (same, increase, or tiered)
- Leadership confirms support model (parallel vs. migrated)
- We analyze historical churn during prior feature shifts
```

---

## Stage 4: SYNTHESIZE

Combine verified sub-answers into a coherent, confidence-weighted response.

### Methodology

**Step 4.1: Order sub-answers by confidence**
- List all sub-answers with confidence scores
- High-confidence answers form the foundation
- Build analysis from strongest to weakest

**Step 4.2: Layer in caveats**
- Moderate-confidence answers included WITH explicit caveats
- Low-confidence answers included AS HYPOTHESES
- Never present low-confidence as certainty

**Step 4.3: Identify conflicts**
- Where do sub-answers contradict?
- Is conflict real (one answer is wrong) or apparent (both are true in different contexts)?
- Use conflict resolution hierarchy to adjudicate

**Step 4.4: Compute global confidence**
- Weight each sub-answer by importance
- Global confidence = Σ(sub_confidence × importance_weight) / Σ importance_weights
- Global confidence is NEVER higher than lowest critical sub-answer

**Step 4.5: Mark certainty vs. hypothesis**
- **Certainty:** Supported by multiple high-confidence sub-answers
- **Hypothesis:** Supported by lower-confidence sub-answers or inference
- Make distinction explicit in final answer

### Conflict Resolution Hierarchy

When sub-answers contradict:

1. **Verified facts** — Highest priority. If two facts conflict, one is wrong; investigate.
2. **Logical deductions from verified facts** — Next priority. Sound logic from good data beats intuition.
3. **Expert consensus** — Established frameworks from domain experts. Use unless contradicted by data.
4. **Reasonable inference** — Well-reasoned extrapolation from partial evidence. Flag uncertainty.
5. **Educated speculation** — Hypothesis stage. Always mark as such. Lowest priority.

**Example conflict resolution:**
- Sub-answer A (0.88 confidence): "Market is growing 18-22% CAGR"
- Sub-answer B (0.62 confidence): "Market is mature, growth slowing to 5-8%"

Sub-answer A is higher confidence AND based on published analyst data (higher hierarchy). Sub-answer B should be reframed: "Analyst consensus shows 18-22% growth, though some sources suggest slower mid-market segment growth (5-8%) — requires investigation."

### Global Confidence Computation

```
Global_Confidence = Σ (confidence_i × importance_i) / Σ importance_i

Example:
SP-1 Market Size: 0.82 confidence, importance 1.0 (foundational)
SP-2 Competition: 0.78 confidence, importance 0.9 (important)
SP-3 Product Fit: 0.81 confidence, importance 1.0 (foundational)
SP-4 Churn Risk: 0.52 confidence, importance 0.8 (important but revised down)
SP-5 Team: 0.70 confidence, importance 0.7 (matters but secondary)
SP-6 Financial: 0.68 confidence, importance 1.0 (critical, but derives from others)

Global = (0.82×1.0 + 0.78×0.9 + 0.81×1.0 + 0.52×0.8 + 0.70×0.7 + 0.68×1.0) / (1.0+0.9+1.0+0.8+0.7+1.0)
       = (0.82 + 0.702 + 0.81 + 0.416 + 0.49 + 0.68) / 5.4
       = 3.918 / 5.4
       = 0.726
```

**Global Confidence: 0.73 (moderate)**

This is BELOW target (0.95), triggering REFLECT stage.

---

## Stage 5: REFLECT

If global confidence < target, diagnose and iterate.

### Reflection Protocol

```
IF global_confidence < target (default 0.95):
  1. DIAGNOSE:
     - Which sub-problem has the lowest confidence?
     - Why is it low? (data gap, logic gap, expertise gap, complexity gap)

  2. ASSESS:
     - Is this sub-problem critical to the final answer?
     - Would increasing its confidence materially change the recommendation?

  3. DECIDE:
     a) If retrievable → gather information and retry (max 3 iterations)
     b) If not retrievable → deliver with caveats (flag specific uncertainties)
     c) If unknowable → state clearly ("This cannot be answered with available information")

  4. OUTPUT:
     - Final answer (reflecting decision in step 3)
     - Explicit confidence score with breakdown
     - Caveats and assumptions
```

### Reflection Questions

Ask yourself:

1. **What is the single biggest weakness in my reasoning?**
   - Which assumption, if false, breaks the answer?
   - Which data point, if wrong, changes the recommendation?

2. **If I'm wrong, what's the most likely cause?**
   - Underestimated complexity?
   - Misunderstood the problem?
   - Missing critical data?
   - Expertise gap in a specific domain?

3. **What would someone who disagrees say?**
   - What's their strongest objection?
   - How would they frame the problem differently?
   - Are they right about something I'm missing?

4. **Is there a simpler explanation I'm overlooking?**
   - Am I over-complicating the problem?
   - Is the answer obvious, and I'm adding layers of complexity?

### Worked Example: Reflection on the Strategy Decision

**Global Confidence: 0.73** (below target 0.95)

**DIAGNOSE:**
- Lowest confidence sub-problems: SP-4 (Churn, 0.52) and SP-6 (Financial, 0.68)
- Why? SP-4 lacks a committed go-to-market strategy (pricing, support model undefined). SP-6 depends on SP-4.
- These are not "unknowable" — they require business decision first, then analysis

**ASSESS:**
- Is SP-4 critical? YES. Churn directly impacts financial viability. If we miscalculate here, the entire pivot breaks.
- Would increasing its confidence change recommendation? YES.
  - If churn is 15% (parallel strategy): pivot is attractive
  - If churn is 80% (aggressive pivot): pivot is risky

**DECIDE:**
- Option A (Retrieve): Ask leadership to decide on pricing/support strategy. Then re-solve SP-4 and SP-6.
- Option B (Deliver with caveats): Recommend pivot, but flag that success depends entirely on parallel product strategy.
- Option C (Unknowable): Declare that recommendation cannot be made until strategy is set.

**CHOSEN: Option A (Retrieve)**

*Action: Pause recommendation. Gather leadership input on three questions:*
1. *Will SMB customers pay mid-market prices, or will we maintain tiered pricing?*
2. *Will we run SMB and mid-market as separate product lines, or migrate all to one product?*
3. *What support/success model will we maintain for SMB customers?*

*Once answered, re-solve SP-4 and SP-6 (estimated 2 hours). Target: 0.90+ global confidence.*

---

## Complete End-to-End Example

**Problem:** "Should we hire this VP of Sales candidate (Sarah)?"

### DECOMPOSE

```
Core Question: Will Sarah succeed as VP of Sales and drive growth?

Sub-problems:
├── SP-1: Does Sarah have relevant sales experience and track record?
│   Domain: factual, analytical | Dependencies: none | Priority: 1
│
├── SP-2: Does Sarah's management style fit our culture?
│   Domain: human | Dependencies: none | Priority: 1
│
├── SP-3: Can Sarah execute our specific sales motion (complex B2B SaaS)?
│   Domain: technical, business | Dependencies: SP-1 | Priority: 2
│
├── SP-4: Will the team accept Sarah's leadership?
│   Domain: human | Dependencies: SP-2 | Priority: 2
│
└── SP-5: Is the compensation package appropriate for market?
    Domain: business, factual | Dependencies: none | Priority: 1
```

### SOLVE

```
SP-1: Sarah's Sales Track Record
Confidence: 0.90
Answer: Sarah closed 8 enterprise deals at competitor (average contract $500K), grew team from 4 to 12 in 2 years, achieved quota 120%+ three years running. Similar product category (project management SaaS). Clear execution record.
Would increase to 0.95 if: We interviewed her references (not yet done)

SP-2: Culture Fit
Confidence: 0.68
Answer: Interview impression is positive (collaborative, data-driven), but limited interaction with broader team. One round of interviews is insufficient data.
Would increase to 0.85 if: She meets with 5-6 team members, we conduct culture-fit panel

SP-3: Can Execute Our Motion
Confidence: 0.75
Answer: Sarah has enterprise sales background. Our motion includes strong mid-market component which she's less experienced with. She can likely learn, but ramp time may be 4-6 months vs. ideal 2-3.
Would increase to 0.88 if: We conduct detailed sales process deep-dive with her; model deal pipeline together

SP-4: Team Acceptance
Confidence: 0.62
Answer: Current team has mixed reactions. Longer-tenured sales reps may perceive her as external hire (threat). Newer reps may welcome strong leadership. Unknown without direct conversation.
Would increase to 0.80 if: We conduct anonymous team survey on leadership preferences

SP-5: Compensation
Confidence: 0.92
Answer: Market comp for VP Sales in this region/stage is $200-250K + 20-30% equity. We're offering $220K + 1.5% equity. On-market for cash, slightly light on equity. Could be negotiated.
Would increase to 0.95 if: We confirm with recruiter and market comps
```

### VERIFY

```
SP-1 LOGIC: ✓ Strong. Experience → execution capability is reasonable inference.
SP-1 FACTS: ⚠ References not yet checked. Verify past achievements with references.
SP-1 COMPLETENESS: ✓ Product category relevant. Team scaling proven.
SP-1 BIAS: ✓ Interview was positive; confirm with cold reference calls.
→ Revised confidence: 0.90 (confirmed)

SP-2 LOGIC: ✓ Culture fit is observable. Interview is limited data but relevant.
SP-2 FACTS: ⚠ One interview is insufficient. Need broader team input.
SP-2 COMPLETENESS: ✗ Haven't tested how Sarah handles conflict, pressure, ambiguity. Limited data.
SP-2 BIAS: ⚠ First impression anchoring. Interviewer was impressed; may be biased positive.
→ Revised confidence: 0.65 (down from 0.68) — revealed gaps

SP-3 LOGIC: ✓ Experience transfer is reasonable (enterprise → mid-market is doable).
SP-3 FACTS: ✓ Her background is mid-market-lite; she has enterprise expertise clearly.
SP-3 COMPLETENESS: ✓ Ramp time concern is valid and addressed.
SP-3 BIAS: ⚠ Assuming mid-market is easy once you know enterprise. May be wrong.
→ Revised confidence: 0.73 (down from 0.75)

SP-4 LOGIC: ✓ Team reaction is critical and observable.
SP-4 FACTS: ✓ Team has mixed reactions (we know this).
SP-4 COMPLETENESS: ✗ We haven't directly asked team what they want in a leader. Assuming based on gossip.
SP-4 BIAS: ⚠ We like Sarah; may be filtering team concerns through positive lens.
→ Revised confidence: 0.58 (down from 0.62)

SP-5 LOGIC: ✓ Market research is solid.
SP-5 FACTS: ✓ Compensation data is current.
SP-5 COMPLETENESS: ✓ Both cash and equity covered.
SP-5 BIAS: ✓ No apparent bias.
→ Revised confidence: 0.92 (confirmed)
```

### SYNTHESIZE

```
Confidence breakdown:
- SP-1 (Track record): 0.90 (high, foundational)
- SP-2 (Culture fit): 0.65 (low, important)
- SP-3 (Can execute): 0.73 (moderate, important)
- SP-4 (Team acceptance): 0.58 (low, important for success)
- SP-5 (Compensation): 0.92 (high, not critical to decision)

Importance weights:
- Track record: 1.0 (foundational)
- Culture fit: 0.9 (critical, but assessable after hiring)
- Can execute: 1.0 (critical)
- Team acceptance: 0.7 (matters for retention/effectiveness)
- Compensation: 0.5 (table stakes)

Global Confidence = (0.90×1.0 + 0.65×0.9 + 0.73×1.0 + 0.58×0.7 + 0.92×0.5) / (1.0+0.9+1.0+0.7+0.5)
                  = (0.90 + 0.585 + 0.73 + 0.406 + 0.46) / 4.1
                  = 3.081 / 4.1
                  = 0.752

GLOBAL CONFIDENCE: 0.75 (moderate)
```

### REFLECT

```
Global confidence 0.75 < target 0.95.

Weakest sub-problems: SP-4 (0.58), SP-2 (0.65).
Both are "people" factors — culture fit and team acceptance.

Can we increase confidence?
- SP-2: Yes. Expand interviews to 5+ team members + culture fit panel. 4 hours work. Can increase to 0.82+
- SP-4: Yes. Anonymous team survey + one-on-one conversations. 6 hours work. Can increase to 0.75+

Are these factors critical?
- YES. Culture misalignment leads to failure rates of 30-40% in early hiring.
- YES. Team rejection creates dysfunction even if candidate is capable.

DECISION: Retrieve information (Option A).

ACTION PLAN:
1. Schedule panel interview with 5 team members (2 hours)
2. Conduct culture-fit assessment (1 hour)
3. Deploy anonymous team survey (1 hour analysis)
4. One-on-one with sales team leader on concerns (1 hour)
5. Re-solve SP-2 and SP-4 based on findings

Estimated time: 6 hours. Target revised global confidence: 0.85+

IF revised confidence reaches 0.85+ → make offer
IF revised confidence stays 0.70-0.84 → make offer with 90-day probation
IF revised confidence drops below 0.70 → pass and reopen search
```

---

## Key Takeaways

1. **Decompose thoroughly** — Poor decomposition cascades. Spend time on sub-problem definition.
2. **Confidence is hard** — Default to underestimating. Justification matters more than the number.
3. **Verification changes things** — If verification doesn't shift confidence or reveal gaps, you're not doing it right.
4. **Synthesis is integration** — Combine sub-answers into coherent narrative, weighted by confidence.
5. **Reflect honestly** — If global confidence is low, diagnose and retrieve. Don't deliver with false precision.
6. **Worked examples are your friend** — Return to these examples when unclear on any stage.
