# Confidence Calibration Reference

Confidence scoring is a skill, not guesswork. This reference provides the 0.0-1.0 scale with detailed descriptions, common calibration errors, and techniques to improve accuracy.

## The 0.0-1.0 Confidence Scale

### 0.95-1.0: Certain

**Meaning:** This is verifiable fact. Non-disputed. Reproducible.

**Evidence Requirements:**
- Direct measurement or observation
- Mathematical proof
- Multiple authoritative sources agree
- Public, widely-known fact
- Can be verified immediately

**Examples:**
- "Paris is the capital of France" (0.99)
- "2 + 2 = 4" (1.00)
- "Our Q3 revenue was $2.5M" (company records) (0.98)
- "The sun rose today" (observable) (0.99)

**When NOT to use this level:**
- If there's any subjective interpretation
- If you haven't personally verified
- If definition could be disputed

**Language markers:** "This is a fact that...", "Verified by...", "Confirmed by multiple sources..."

---

### 0.85-0.94: High Confidence

**Meaning:** Strong evidence and reasoning. Expert consensus. Direct data.

**Evidence Requirements:**
- Published, peer-reviewed research
- Expert testimony or established frameworks
- Company data (verified internally)
- Tested methodology
- Consistent corroboration from multiple sources

**Examples:**
- "This algorithm will improve search latency by 20-30%" (based on benchmark testing on 10K queries) (0.90)
- "Mid-market SaaS is growing 15-20% annually" (Gartner + Forrester align) (0.88)
- "This candidate has strong technical skills" (verified by technical interview + reference check) (0.89)

**When to use this level:**
- You have primary data or expert validation
- Logic is sound, assumptions are reasonable
- Minor gaps exist but don't threaten the conclusion

**When NOT to use:**
- If you haven't verified with primary sources
- If you're extrapolating beyond your domain
- If stakes are very high and you want extra margin

**Language markers:** "Based on research...", "Expert consensus indicates...", "Testing shows...", "Multiple sources confirm..."

---

### 0.70-0.84: Moderate Confidence

**Meaning:** Reasonable inference with partial evidence. Some assumptions required.

**Evidence Requirements:**
- Industry reports or secondary sources
- Analogous examples or case studies
- Expert judgment (not consensus)
- Limited data points
- Logical extrapolation

**Examples:**
- "Mid-market buyers prefer self-service onboarding" (inferred from 3 customer interviews + product usage patterns) (0.76)
- "This refactor will reduce technical debt by 40%" (estimate based on previous similar work) (0.72)
- "The market will adopt this technology within 18 months" (trend analysis + expert opinion) (0.74)

**When to use this level:**
- You have reasonable supporting evidence but gaps remain
- Logic is sound with clear assumptions
- You've considered alternatives

**When NOT to use:**
- If you have strong primary data (move to 0.85+)
- If stakes are critical and you want margin for error (consider 0.50-0.69)
- If you're guessing without structural reasoning

**Language markers:** "Based on limited data...", "Reasonable inference suggests...", "Trend indicates...", "Assuming X, then Y..."

---

### 0.50-0.69: Low Confidence

**Meaning:** Educated guess with significant assumptions. Limited support.

**Evidence Requirements:**
- Logical extrapolation (but unvalidated)
- One or two data points
- Plausible reasoning
- Hearsay or anecdotal evidence
- Market signals (not yet validated)

**Examples:**
- "This feature will reduce churn by 15-25%" (hypothesis based on customer feedback, not yet tested) (0.58)
- "React will remain the dominant front-end framework" (extrapolation from current trends) (0.62)
- "This team will ship the project 20% faster with better tooling" (assumption, no track record) (0.55)

**When to use this level:**
- Question is important but hard to answer
- You're providing hypothesis, not recommendation
- Answer influences next steps but not critical decision
- You explicitly flag the low confidence

**When NOT to use:**
- As a recommendation for major decisions without caveat
- Without explicitly marking as "hypothesis" or "assumption"
- If you haven't tried to improve confidence

**Language markers:** "Hypothetically...", "Assuming...", "Likely...", "Could...", "If current trends continue..."

---

### 0.30-0.49: Speculative

**Meaning:** Brainstorm stage. Hypothesis. Minimal evidence.

**Evidence Requirements:**
- Intuition or logical possibility
- Single mention or source
- Assumption with minimal grounding
- Thought experiment

**Examples:**
- "AI will replace 50% of programming jobs within 5 years" (speculative extrapolation) (0.35)
- "This startup will achieve unicorn status" (hope-based, not data-driven) (0.40)

**When to use this level:**
- You're thinking out loud
- Exploring possibilities, not recommending action
- User explicitly asks for speculation

**When NOT to use:**
- In recommendation or decision context
- Without clear labeling as "speculative" or "exploratory"
- When better evidence is available

**Language markers:** "Speculatively...", "It's possible that...", "One could imagine...", "This is exploratory..."

---

### Below 0.30: Unknowable

**Meaning:** Should not attempt answer. Insufficient information.

**When to declare unknowable:**
- The question requires unavailable information (future events, private intentions, etc.)
- You lack domain expertise and cannot quickly acquire it
- The answer requires primary research you cannot perform
- The problem is fundamentally ambiguous

**Examples:**
- "Will Jane accept the job offer?" (private decision, cannot predict) (unknowable)
- "What will the stock price be in 2 years?" (inherently unpredictable) (unknowable)

**Language markers:** "This cannot be answered with available information...", "This requires X, which is not accessible...", "This is unknowable because..."

---

## Common Over-Confidence Patterns

### 1. Anchoring Bias
**Definition:** First answer feels "obviously right" without exploring alternatives.

**Signal:** You rated something 0.85+ but haven't considered contradictory evidence.

**Fix:**
- Actively generate 2-3 alternative answers
- For each, ask: "What would need to be true for this to be the right answer?"
- Assign confidence to each alternative
- If top alternative isn't clearly dominant, lower your confidence

**Example:**
- Initial answer: "This hire will succeed" (0.85 confidence, anchored on impressive resume)
- Alternative 1: "Will struggle in our culture" (0.40 confidence after considering team feedback)
- Alternative 2: "Will succeed in year 1, leave in year 2" (0.45 confidence, based on pattern from similar hires)
- Revised confidence: 0.70 (weighted blend of alternatives)

---

### 2. First-Answer Bias
**Definition:** Your first instinct is correct, so you stop thinking.

**Signal:** You answered immediately with high confidence and haven't spent time on verification.

**Fix:**
- Set a minimum verification time (10 minutes for important answers)
- Ask: "What haven't I considered?"
- Red-team your first answer — what would prove it wrong?
- Sleep on it and reconsider (for non-urgent questions)

**Example:**
- Q: "Why did our conversion rate drop this month?"
- First answer: "Sales team is lazy" (0.80 confidence, gut reaction)
- After 10-minute analysis: Multiple factors (pricing change, competitor launch, traffic quality, page speed)
- Revised answer: "Primarily due to pricing change (40% impact), plus competitive pressure (30% impact). Sales effort has minimal impact." (0.75 confidence)

---

### 3. Familiarity Illusion
**Definition:** You're familiar with a topic, so you overestimate your knowledge.

**Signal:** You rate confidence 0.85+ in an area where you have domain experience, but haven't fact-checked recently.

**Fix:**
- Distinguish between "I know about this" and "I know this is true"
- Require recent data for technical/market answers
- Get a gut-check from someone outside your area
- Explicitly list your assumptions

**Example:**
- "React is the best choice for this project" (0.88 confidence, you're a React expert)
- After fact-checking: Vue and Svelte have grown; React ecosystem has fragmentation
- After getting opinions: Depends on team preference and project constraints
- Revised confidence: 0.70 (still biased toward React, but acknowledging legitimate alternatives)

---

### 4. Authority Bias
**Definition:** Accepting a framework because it's well-known or from an expert, not because it fits.

**Signal:** You cite "Gartner says..." without evaluating whether Gartner's framework applies to your situation.

**Fix:**
- Always ask: "Is this framework relevant to my specific problem?"
- Distinguish between "Gartner says X" (high confidence on Gartner's data) and "X is true for us" (potentially lower confidence)
- Seek contradictory expert views
- Test framework assumptions against your data

**Example:**
- "According to McKinsey, companies should adopt AI in 3 key areas..." (0.85 confidence)
- Question: Does McKinsey's advice apply to a 50-person company vs. Fortune 500?
- Revised: "McKinsey's framework is sound (0.88 confidence), but applicability to our company size is uncertain (0.65 confidence). Revised combined: 0.70 confidence"

---

## Common Under-Confidence Patterns

### 1. Imposter Syndrome / Self-Doubt
**Definition:** You have solid evidence but downgrade confidence because "I might be wrong."

**Signal:** You're 0.40-0.50 confident on something you could easily verify or have significant expertise in.

**Fix:**
- Build a track record: "In the past 10 questions like this, I was right X% of the time"
- Trust primary data over self-doubt
- Ask: "What's the actual error rate on this type of judgment?"
- Seek validation from peers

**Example:**
- "I think this will work, but maybe I'm overlooking something" (0.50 confidence, false humility)
- Reality: You've shipped 20 similar features; 18 worked as expected
- Revised: 0.85 confidence (based on track record)

---

### 2. Hedging Habit
**Definition:** Overuse of qualifiers ("possibly", "might", "could") that reduce stated confidence without reason.

**Signal:** Your answer is full of hedging language, and confidence is low despite strong evidence.

**Fix:**
- Rewrite without hedging language
- Re-assess confidence
- Use hedging only for actual uncertainty, not for politeness

**Example:**
- "It's possible that this might improve performance, possibly by around 10-20%..." (0.55 confidence)
- After removing hedging: "This will improve performance by 15-20%" (benchmark confirmed)
- Revised: 0.82 confidence

---

### 3. Perfectionism
**Definition:** Demanding 100% certainty before committing to any confidence level.

**Signal:** You won't go above 0.70 on anything because "there's always uncertainty."

**Fix:**
- Accept that 0.85 confidence is not certainty; it's "strong evidence with reasonable assumptions"
- Read the confidence scale again — high confidence doesn't mean perfect
- Compare to your track record: are you actually wrong 15% of the time at 0.85 confidence?
- Accept 0.80-0.90 as the normal range for good analysis

**Example:**
- "I'm not 100% sure, so I'll say 0.60" (perfectionism penalty)
- Reality: You have strong evidence but one unverifiable assumption
- Revised: 0.80 confidence (strong + assumption is reasonable)

---

### 4. Recency Bias (Inverted)
**Definition:** One past failure makes you under-confident in similar situations.

**Signal:** You had one bad outcome, so all similar questions now get 0.50-0.60 confidence despite having done them successfully 19 other times.

**Fix:**
- Base confidence on aggregate track record, not last failure
- Ask: "What was different about the failure case?"
- Adjust confidence based on specific risk factors, not general pattern

**Example:**
- Last estimate was wrong by 40%; now estimating similar task
- Old approach: 0.50 confidence (fear of repeating mistake)
- Better approach: 0.78 confidence (19/20 previous estimates were good), with specific note: "However, last attempt missed by 40%; adding 20% buffer to timeline"

---

## Calibration Techniques

### 1. Pre-Mortem
**How it works:** Imagine it's 6 months from now and your answer was completely wrong. Why?

**Technique:**
1. State your answer and confidence: "I'm 0.80 confident we'll ship on time"
2. Imagine failure: "It's now 6 months later, and we're 3 months late. What happened?"
3. Generate 5-10 failure scenarios
4. Assess which is most likely
5. Re-evaluate confidence

**Example:**
- Confidence: 0.80 we'll ship MVP in Q2
- Pre-mortem failures:
  - Scope creep (30% likelihood)
  - Unexpected technical blocker (20%)
  - Team turnover (15%)
  - Competing priorities (20%)
  - External dependencies (15%)
- Adjusted confidence: 0.68 (pre-mortem revealed 80% combined probability of delay)

---

### 2. Red Team
**How it works:** Have someone argue the opposite position aggressively.

**Technique:**
1. State your answer: "I think we should hire this candidate"
2. Red team argues against: "Here's why this hire will fail..."
3. You respond to their objections
4. After 3-4 rounds, assess whether confidence should shift

**Example:**
- You: "Hiring this person will improve team productivity" (0.75 confidence)
- Red team: "You only interviewed them once. You don't know their work style. Last external hire took 6 months to ramp."
- You: "Fair, but we did reference checks, and their technical skills are proven"
- Red team: "Technical skills aren't the issue. Cultural fit is unknown."
- You: Re-assess. Confidence → 0.65 (culture fit is a real gap)

---

### 3. Confidence Intervals
**How it works:** Instead of single-point confidence, estimate a range.

**Technique:**
1. State answer: "Performance will improve by 15%"
2. Define 90% confidence interval: "Could be anywhere from 5% to 35%"
3. Define 70% confidence interval: "Most likely 12-18%"
4. Assess: Is your point estimate within 70% interval? Is range reasonable?

**Example:**
- Answer: "We'll close 8-10 deals next quarter"
- 90% confidence interval: 5-15 deals
- 70% confidence interval: 7-12 deals
- Point estimate (0.80 confidence): 9 deals
- Sanity check: Is interval realistic? Does it align with past performance?

---

## Confidence Update Process

### After Verification

When you verify a sub-answer (VERIFY stage in DSVSR):

**Rule 1: Verification typically changes confidence.**
- If verification doesn't shift your score, verification was superficial

**Rule 2: Verification usually decreases confidence.**
- Finding gaps is more common than confirming certainty
- If verification increases confidence, document why

**Rule 3: Update with justification**
- Don't just change the number; explain what changed
- Example: "After fact-checking, confidence decreased from 0.85 to 0.75 because [specific gap found]"

**Rule 4: Confidence never decreases below 0.30 without reason**
- If you drop below 0.30, consider: Should I attempt this answer at all?

---

## Target Confidence Levels by Context

### Production Answers (User-Facing, High Stakes)
**Target: 0.95+**
- Decision-making context
- Customer-facing recommendations
- Financial or strategic implications
- "This is my final answer" context

**Tactics to reach 0.95:**
- Require verified facts for 80%+ of reasoning
- Iterate on weakest sub-problems
- Get external validation (red team, expert review)
- Accept that some questions can't reach 0.95 — deliver with caveats instead

### Exploratory Answers (Internal, Lower Stakes)
**Target: 0.85+**
- Brainstorming context
- Internal analysis
- "What should we investigate further?" context
- Working with incomplete information is acceptable

**Tactics to reach 0.85:**
- Gather reasonable evidence
- Identify gaps clearly
- Flag assumptions
- Invite feedback

### Minimum Viable Confidence (Internal, Must Deliver)
**Target: 0.70+**
- Urgent decisions
- Limited information available
- "Best guess given constraints" context
- Not appropriate for critical decisions

**Tactics to reach 0.70:**
- Document assumptions clearly
- List what would improve confidence
- Present as hypothesis, not certainty
- Plan to revisit when better data available

---

## Recalibration Checklist

Use this checklist when finalizing confidence scores:

**☐ Have I verified this answer? (If not, lower confidence by 10 points)**
☐ Have I considered 2+ alternative answers? (If not, lower by 5 points)
☐ Are my core assumptions reasonable? (If unclear, lower by 10 points)
☐ Have I checked for availability bias? (Recent/memorable examples? Lower by 10 points if yes)
☐ Have I distinguished facts from inference? (If fuzzy, lower by 10 points)
☐ Could this be wrong while still being reasonable? (If yes, cap confidence at 0.85)
☐ Am I hedging linguistically without reason? (If yes, raise confidence by 5-10 points)
☐ What's my track record on similar questions? (Let history inform your score)
☐ Would an expert in this domain agree? (If uncertain, lower by 10 points)
☐ Have I tested this answer against red team objections? (If not, lower by 10-15 points)

---

## Examples: Confidence Calibration in Practice

### Example 1: Market Size Estimate

**Question:** "How large is the mid-market CRM opportunity in Europe?"

**Initial answer:** "€3-5B market size" (0.80 confidence)

**Verification:**
- Gartner says €4.2B (published 2023)
- IDC says €3.8B (published 2024)
- Both align with our estimate ✓
- But both reports are for CRM only, not adjacent categories ⚠
- Report currency/exchange rate assumptions (€ vs. $) unclear ⚠

**Red team objections:**
- "Reports are 12+ months old; market may have shifted"
- "What if TAM was overestimated in reports?"
- "You're quoting analyst firms without questioning methodology"

**Updated confidence:** 0.82
- Sources align (good)
- Data is recent enough (good)
- But analyst reports can be wrong; caveat needed
- Final answer: "€3.8-4.2B (per Gartner, IDC), confidence 0.82. Caveat: reports are 12+ months old."

---

### Example 2: Technical Estimate

**Question:** "Can we migrate this system to cloud in 3 months?"

**Initial answer:** "Yes, 0.75 confidence"

**Verification:**
- Did we estimate all components? (No, database migration not detailed)
- Did we include testing? (Minimal allocation)
- Have we done similar migrations? (Yes, similar timeline, but different tech stack)
- Did we account for unknowns? (No, zero contingency)

**Updated confidence:** 0.60 (down from 0.75)
- Reason: Major gaps in estimation (database, testing, contingency)
- Would increase to 0.80 if:
  - We detail database migration approach
  - We allocate 20% for testing/QA
  - We include 10% contingency
  - We interview team with prior migration experience

**Final answer:** "Technically feasible but risky in 3 months (0.60 confidence). Recommend 4 months with contingency (0.82 confidence) or detailed technical spike first (1 week, then re-estimate)."

---

### Example 3: Hiring Decision

**Question:** "Will this candidate succeed in this role?"

**Initial answer:** "Yes, 0.85 confidence"

**Calibration check:**
- Am I anchored on impressive interview? (Yes — this is a risk)
- Have I verified with references? (No, only scheduled)
- Have I assessed culture fit with team? (Limited, one conversation)
- What's my track record on hiring? (60% success rate historically)

**Red team objections:**
- "You haven't talked to the team yet"
- "References haven't been verified"
- "Your base rate is only 60%; don't be overconfident"

**Adjusted confidence:** 0.70 (down from 0.85)
- Reason: Multiple verification steps pending
- Action: Complete reference checks, conduct team interviews before making offer
- If all positive: confidence 0.82
- If any concerns: confidence 0.55-0.65, need discussion

---

## Key Takeaways

1. **Confidence is learnable** — Track your predictions. Over time, your scores will become more accurate.
2. **Verification matters** — If verification doesn't change your confidence, you're not doing it right.
3. **Hedging is a tax** — Remove unnecessary qualifiers. Let real uncertainty show in the confidence number.
4. **Context determines target** — 0.95 for critical decisions, 0.85 for normal analysis, 0.70 as floor.
5. **Pre-mortems and red teams work** — Use them to catch overconfidence.
6. **Track record is king** — Your past performance is the best predictor of your future accuracy.
