# Intent Detection: Gap Analysis Framework

## Table of Contents

1. [Core Problem](#core-problem)
2. [The Five Gap Types](#the-five-gap-types)
3. [Detection Protocol](#detection-protocol)
4. [Gap Priority & Conflict Resolution](#gap-priority--conflict-resolution)
5. [Signal Detection Quick Reference](#signal-detection-quick-reference)
6. [Reformulation Strategies](#reformulation-strategies)
7. [Edge Cases](#edge-cases)
8. [Acceptance Criteria](#acceptance-criteria)
9. [Integration with Pipeline](#integration-with-pipeline)

## Core Problem

Users rarely say exactly what they mean. The gap between typed request and actual need falls into 5 distinct categories, each with different detection signals and different reformulation strategies.

**Key insight:** Most inputs have 1-2 gap types, not all 5. If you detect 4-5 gaps, you're likely over-analyzing — focus on the strongest signals and ask for clarification on the rest.

## The Five Gap Types

### 1. Vocabulary Gap

**Definition:** User knows the concept but uses the wrong word for it.

**Why it happens:** Domain mismatch (non-technical user using technical terms), jargon confusion, translation barriers, or trend-chasing ("use AI" when they mean "automate this").

**Detection signals:**

| Signal | Example | Inference |
|--------|---------|-----------|
| Wrong term used consistently | "I need an algorithm for sorting" | Means: workflow or process, not computational algorithm |
| Over-technical for context | "JSON serialization in the database" | Means: store structured data |
| Describes outcome, not mechanism | "Make it use AI" | Means: automate this repetitive task |
| Vague placeholder words | "the strategy", "the solution" | Vocabulary + scope gap combined |
| Mixes domain terminology | "ML to predict churn" (no ML infrastructure mentioned) | Borrowed term from adjacent field |

**Reformulation:** Map to correct terminology. Explain the difference briefly. If the mapping is uncertain, present both interpretations and ask.

**Worked example:**
```
TYPED: "We need machine learning to predict churn"
SIGNALS: No mention of training data, model infra, or data science team.
         Context: 2-person startup, 2 years of customer data.
GAP: "ML" → "data analysis + simple scoring rules"
REFORMULATION: "Analyze 2 years of customer data to identify patterns
preceding churn. Create a scoring system to flag at-risk customers.
Not ML (too early, <500 users, no infra) — simple rules first."
```

### 2. Scope Gap

**Definition:** User understates the actual scope needed.

**Why it happens:** Underestimates scale, doesn't see dependencies, too modest, or describes a symptom rather than the problem.

**Detection signals:**

| Signal | Example | Inference |
|--------|---------|-----------|
| Minimizing language | "Just", "quickly", "simple change" | Actual scope is likely larger |
| Symptom language | "Fix the bug", "make it faster" | Root need is architectural, not tactical |
| Missing dependencies | "Update the login flow" | Doesn't mention: DB schema, API changes, mobile app |
| Vague deliverable | "Make a dashboard" | What features? What data? Who uses it? |
| "While you're at it" | "Fix X. Also, maybe Y?" | Multiple needs bundled as afterthought |

**Reformulation:** Use 5 Whys to find root need. Identify all affected systems. Expand scope to address root cause. Phase if large.

**Worked example:**
```
TYPED: "Fix the slow API"
SIGNALS: No endpoints specified, no traffic numbers, no latency targets.
         5 Whys revealed: 3 endpoints handle 60% traffic, unoptimized.
         New user retention dropping because of page loads.
REFORMULATION: "Reduce latency on login/dashboard/publish endpoints
from p99 2.5s to <500ms at 250 req/sec. Not: full API redesign,
not database migration. Success: retention improves within 2 weeks."
```

### 3. Expertise Gap

**Definition:** User asks for X but means Y because they don't know the right approach.

**Why it happens:** Jumping to solution before understanding problem, cargo-culting ("microservices because it's modern"), or confusing tool with outcome.

**Detection signals:**

| Signal | Example | Inference |
|--------|---------|-----------|
| Over-engineering | "Set up Kafka for event streaming" | Actual need: store and replay a few events |
| "Best practice" reasoning | "We should use microservices" | Doesn't match actual requirements |
| Tool instead of outcome | "Install Docker" | Actual need: deploy the application |
| Mixing abstraction levels | "Use ML and also manually script it" | Doesn't understand the concepts |
| Tech request from non-tech user | Junior asks for advanced technique | Learning stage; simpler approach likely works |

**Reformulation:** Ignore proposed solution. Focus on the problem. Offer simplest solution that works. Explain why simpler is better (when it is).

**Worked example:**
```
TYPED: "We need ML to predict which users upgrade"
SIGNALS: 2-person startup, <500 users, no data science team.
GAP: "predict" ≠ "needs ML". Actual need: identify upgrade signals.
REFORMULATION: "Analyze which free users upgraded. Identify common
traits. Create simple rules: if [signal], likely to upgrade.
Why not ML: <500 users = not enough data. Simple rules are
interpretable and actionable now. Revisit ML at 50k+ users."
```

### 4. Emotional Gap

**Definition:** Emotional state drives the request, but user frames it technically.

**Why it happens:** Work culture expects professional framing. Embarrassment about emotional needs. Venting disguised as a request.

**Detection signals:**

| Signal | Example | Inference |
|--------|---------|-----------|
| Hedging / uncertainty | "This probably doesn't matter, but..." | Emotional anxiety, not technical confidence |
| Negative framing | "This is terrible", "Nothing works" | Frustration, not objective assessment |
| Blame language | "Previous dev was incompetent" | Emotional frustration at people/decisions |
| Superlatives | "The WORST code I've ever seen" | Emotional reaction, not measured assessment |
| Self-deprecating | "I'm probably stupid for not understanding" | Insecurity driving the request |
| Fear of action | "I'm worried I'll break something" | Anxiety needs addressing alongside technical fix |

**Reformulation:** Validate emotion (don't dismiss). Separate emotional context from technical problem. Address both. Offer safety mechanisms (tests, backups, phased approach).

**Worked example:**
```
TYPED: "This code is a DISASTER. Previous dev was INCOMPETENT.
        I'm worried I'll break something."
SIGNALS: Caps emphasis, blame language, fear of action.
GAP: Technical request + emotional need for safety/confidence.
REFORMULATION: "Refactor [system] module for readability + add tests.
Phase 1: Write tests for current behavior (safety net).
Phase 2: Refactor one function at a time (controlled change).
Phase 3: Document as you go (builds confidence).
Context: Inherited code anxiety is normal. Tests first = safe."
```

### 5. Context Gap

**Definition:** User assumes shared context that isn't explicitly stated.

**Why it happens:** Obvious to them (months of work context). Dangling pronouns. Different mental models. Inside references.

**Detection signals:**

| Signal | Example | Inference |
|--------|---------|-----------|
| Dangling references | "It's not working", "Fix this" | No clear antecedent |
| Assumed knowledge | "You know the issue with X" | No prior mention of X |
| Pronouns without context | "They're asking for this" | Who is "they"? What is "this"? |
| Implicit dependencies | "The database change" | What changed? When? By whom? |
| Inside references | "Handle the widget thing" | Context only in their head |

**Reformulation:** Ask clarifying questions. Replace pronouns with proper nouns. Add necessary background. Make all references explicit.

**Worked example:**
```
TYPED: "Can you review the changes and make sure it's working?"
SIGNALS: "The changes" (which?), "it's working" (for whom? How?).
GAPS: No system identified, no test criteria, no timeline, no audience.
REFORMULATION: "Review the auth refactor (User model + middleware
changes) for correctness before Friday merge. Test: login flows
(email, OAuth), session expiry, concurrent sessions, password reset.
Success: all tests pass, no login regression, support doesn't report
new session issues post-deploy."
```

## Detection Protocol

### Step 1: Transcribe Explicit Statements

What did the user literally say?
- Direct statements (what they asked for)
- Constraints mentioned (format, timeline, budget)
- Success criteria defined (or notably absent)

### Step 2: Identify Implicit Signals

What can you infer from word choice, tone, and absences?

| Signal Category | Keywords | Inference |
|----------------|----------|-----------|
| Hedging | "Maybe", "if possible", "not sure" | Uncertainty; may underestimate scope |
| Urgency | "ASAP", "by Friday", "emergency" | Timeline tight; may sacrifice quality |
| Minimizing | "Just", "quick fix", "small" | Scope likely understated |
| Emotional | "Frustrated", "worried", "disappointed" | Emotional factor in play |
| Missing info | Doesn't mention what you'd expect | Obvious to them, or unknown to them |

### Step 3: Map Gaps

For each detected signal, classify the gap type and map:

```
Explicit → Implicit → Gap → Real Ask
```

### Step 4: Synthesize the Real Ask

**Formula:**
```
The user really needs: [synthesized from all passes]
Not: [what they literally typed]
Because: [specific gap that revealed the mismatch]
Evidence: [the signals that support this interpretation]
```

## Gap Priority & Conflict Resolution

When multiple gaps are detected, they may conflict. Resolution order:

| Priority | Gap Type | Reasoning |
|----------|----------|-----------|
| 1 | Emotional | Unaddressed emotion derails everything downstream. Address first. |
| 2 | Context | Without context, all other gap analyses build on sand. Clarify before proceeding. |
| 3 | Scope | Scope determines what work is actually needed. |
| 4 | Expertise | Once scope is clear, evaluate whether proposed approach fits. |
| 5 | Vocabulary | Terminology fixes are easy once intent is clear. |

**Conflict examples:**

| Conflict | Resolution |
|----------|------------|
| Scope says "big project" but user said "just a quick fix" | Trust concrete details over framing language. Note the contradiction. |
| Emotional signals present but user denies frustration | Address the emotion implicitly (offer safety mechanisms) without labeling it. |
| Vocabulary suggests X but expertise gap suggests Y | Focus on the outcome they want, not the term they used or the approach they proposed. |
| Multiple context gaps (can't proceed without answers) | Ask the 2 most critical clarifying questions. Don't dump 10 questions at once. |

**Decision rule:** When gaps conflict, the one that would change the reformulation the most takes priority. A vocabulary fix changes word choice. A scope revelation changes the entire deliverable. Prioritize by magnitude of impact on the reformulated prompt.

## Signal Detection Quick Reference

| Gap | Keywords to Watch | Question to Ask |
|-----|------------------|-----------------|
| Vocabulary | AI, ML, algorithm, blockchain, "make it smart" | "What specifically will you do with the output?" |
| Scope | "Just", "quickly", "simple", "maybe", "also" | "What's the root need? Why now?" |
| Expertise | Over-technical or under-technical for context | "What are you trying to achieve?" (not how) |
| Emotional | "Frustrated", "worried", "terrible", "impossible" | "What's the underlying concern here?" |
| Context | Pronouns, no background, assumed knowledge | "Can you give me more context on X?" |

## Reformulation Strategies

### Per Gap Type

| Gap | Strategy | Key Principle |
|-----|----------|---------------|
| Vocabulary | Map to correct term; explain difference | Don't just correct — educate |
| Scope | Expand via 5 Whys; phase if large; define success | Address root cause, not symptom |
| Expertise | Ignore proposed solution; focus on outcome; simplest first | The user wants the result, not the technique |
| Emotional | Validate; separate emotion from tech; offer safety | Both problems are real |
| Context | Ask questions; replace pronouns; add background | Make the implicit explicit |

### Universal Reformulation Template

```
GOAL: [Action verb + measurable outcome]
CONTEXT: [Why this matters — from 5 Whys + gap analysis]
INTENT: [What they really need vs what they typed + gap evidence]
CONSTRAINTS: [Explicit + inferred boundaries]
NOT IN SCOPE: [What this is NOT, to prevent scope creep]
EXPECTED OUTPUT: [Deliverable type, format, success criteria]
QUALITY LEVEL: [From 7 So Whats calibration]
OPEN QUESTIONS: [What couldn't be resolved — with suggested answers]
```

## Edge Cases

### No Gap Detected

Sometimes the literal request IS the real ask. Detection: explicit and implicit align, no uncertainty signals, request is specific and measurable, user has relevant expertise.

When this happens: confirm intent (Pass 4 output = "no significant gap detected") and pass through with minimal reformulation. This is a success, not a failure.

### Too Many Gaps (4-5 types)

If you detect signals in nearly every category, you're likely projecting. Recovery:
1. Focus on the strongest 1-2 signals (highest confidence)
2. Flag the rest as "possible gaps — need clarification"
3. Ask the user 2 targeted questions (not 5)
4. Re-analyze after clarification

### Gap Appears Mid-Analysis

Sometimes a gap only becomes visible during Pass 2 or Pass 3 (e.g., 5 Whys reveals the user said "optimize" but means "save the acquisition deal"). This is normal — update the gap analysis retroactively and let it inform Pass 5.

### User Rejects Your Interpretation

If the user says "no, I literally mean X" — respect that. Operationally:
1. Set the reformulated prompt to match their stated intent exactly.
2. Preserve your gap analysis as a "context" annotation (not as the primary directive).
3. Do not re-argue the gap. If they reject it, the gap analysis was wrong for this user.
4. If the downstream result fails, revisit the gap analysis — the user may then be more receptive.

The gap analysis is a hypothesis, not a diagnosis. Confidence in the hypothesis does not override stated user intent.

## Acceptance Criteria

A complete intent analysis must include:

- [ ] Explicit statements transcribed verbatim from user input
- [ ] At least 2 implicit signal categories checked (even if no signals found)
- [ ] Each detected gap classified by type with cited evidence
- [ ] "Real ask" synthesized as a single statement with gap justification
- [ ] Gaps that conflict are resolved using the priority framework
- [ ] Open questions listed (what you can't determine without more info)
- [ ] Confidence level assigned: high (strong signals), medium (some inference), low (mostly open questions)

## Pipeline Connections

This pass receives from Passes 2 and 3, and feeds into Pass 5. For the full data flow, backtrack protocol, and inter-pass contracts, see `SKILL.md`.

**Key handoffs from this pass:**
- **real ask** → Pass 5 uses it as the INTENT section of the reformulated prompt
- **gap analysis** → Pass 5 addresses each detected gap explicitly
- **open questions** → Pass 5 lists them with suggested answers
- **confidence** → contributes to overall confidence aggregation (see `SKILL.md`)

**Key dependencies:**
- **From Pass 2:** Root cause often reveals scope/vocabulary gaps invisible in the surface request. If Pass 2 changed the understanding significantly, incorporate it before running gap detection.
- **From Pass 3:** If calibration reveals higher stakes than the user stated ("quick fix" but Flagship calibration), note this as a scope gap.

**Traceability rule for Pass 5:** Each section of the reformulated prompt traces to a specific pass. GOAL ← Pass 2. CONTEXT ← Pass 2 + Pass 3. INTENT ← Pass 4. CONSTRAINTS ← all passes. QUALITY LEVEL ← Pass 3.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
