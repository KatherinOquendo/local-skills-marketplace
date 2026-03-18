# Five Whys Guide: Root Cause Analysis

## Table of Contents

1. [Origin & Principle](#origin--principle)
2. [The Chain: Layer by Layer](#the-chain-layer-by-layer)
3. [When to Stop](#when-to-stop)
4. [The Protocol](#the-protocol)
5. [Examples Across Domains](#examples-across-domains)
6. [Pitfalls & Countermeasures](#pitfalls--countermeasures)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Integration with Pipeline](#integration-with-pipeline)

## Origin & Principle

From Toyota's lean manufacturing (1970s): ask "why" iteratively to move from symptoms to root causes. In knowledge work, users describe the problem they feel (symptom) rather than the need they have (root cause). Each "why" peels back one layer of causation.

**Key adaptation for input analysis:** Unlike manufacturing where root causes are physical, user requests have root causes that are intentional — there's a decision, emotion, or constraint driving the request. The goal is to find that driver.

## The Chain: Layer by Layer

| Layer | Question | What You Learn | Signal You're There |
|-------|----------|---------------|-------------------|
| Why 1 | What prompted this request? | Immediate trigger | Business context visible |
| Why 2 | What's the broader situation? | Organizational context | Stakes becoming clear |
| Why 3 | What decision depends on this? | Consequence or decision point | Risk/value exposed |
| Why 4 | What's at risk if this goes wrong? | Strategic exposure | Organizational consequences |
| Why 5 | What's the ultimate need? | Root strategic purpose | True motivation revealed |

**Critical distinction:** Each Why should produce a different type of answer. If Why 3 sounds like Why 1 reworded, you've stalled — reframe the question as "what changes because of this?" or "who else is affected?"

### Inference Rules

Each Why answer must be grounded in one of these evidence types:

| Evidence Type | Example | Reliability |
|---------------|---------|-------------|
| Explicit statement | "My boss asked me to present" | HIGH — use directly |
| Direct inference | Timeline mention implies deadline | HIGH — minimal assumption |
| Contextual inference | Industry norms suggest X | MEDIUM — note as inference |
| Open question | Cannot determine without asking | Flag and stop |

If you reach an open question, do not fabricate an answer. State the question explicitly and note what the answer would change about the analysis.

## When to Stop

Stop the chain when any of these conditions is met:

1. **Root cause is clear and actionable.** If Why 2-3 reveals an unambiguous need that changes how you respond, adding more Whys adds noise, not insight.

2. **Circular reasoning appears.** "Because it's required → because it's a requirement → because it's required." You've hit bedrock.

3. **Open question blocks progress.** Answering the next Why requires information you cannot infer. Stop and note the question.

4. **Scope becomes external.** If the Why points to "market conditions," "competitor actions," or "industry trends" — you've exited the user's actionable sphere. Back up one level.

5. **User explicitly stated the root.** Sometimes Why 1 is the root: "I need this because the client asked for it by Friday." No deeper analysis needed.

**Decision heuristic:** If the root need statement from your current depth would produce the same reformulated prompt as going one level deeper, stop. Additional depth isn't adding value.

## The Protocol

### Step 1: Capture Surface Request

Write down exactly what the user said they need. No interpretation yet.
- "I need help writing a job description"

### Step 2: Why 1 — Immediate Driver

What prompted this request right now?
- "We're hiring for a new role and need to post by Friday"
- Note: if this is obvious, state it briefly. If unclear, flag as open question.

### Step 3: Why 2 — Context Expansion

What's the broader situation?
- "Lost a team member + expanding for Q2. Need someone who can ship from week 1."
- Signal: urgency + quality bar are now visible.

### Step 4: Why 3 — Consequence

What decision or outcome depends on this?
- "Right hire affects Q2 velocity. Bad hire = 3 months rework + missed client deadline."
- Signal: risk and cost of failure are quantifiable.

### Step 5: Why 4-5 — Strategic Level (only if root unclear)

What's the deeper organizational impact?
- "Major client delivery in Q3; hire's code quality affects reputation. Client is 30% of revenue."
- Only continue if the root need is still ambiguous after Why 3.

### Step 6: Synthesize Root Need

One sentence that captures the true need:
- "A job description that attracts senior engineers capable of shipping production code independently, for a role that directly affects a Q3 client delivery worth 30% of revenue."

**Test your synthesis:** If a skilled recruiter read only this sentence, would they write a fundamentally different JD than if they read only the surface request? If yes, the 5 Whys added value. If the JD would be the same, the surface request was already sufficient.

## Examples Across Domains

### Example 1: Business (Marketing/Sales)

**Surface:** "I need a pricing page for our SaaS product."

| Why | Answer | Evidence |
|-----|--------|----------|
| 1 | Customers leave because they can't find pricing. Competitors show price upfront. | Explicit: sales team feedback |
| 2 | Transparency expected; customers don't want demo forms just to know budget fit. | Inference: market norms |
| 3 | Losing 2-3 deals/week at early stage. Targeting 30% growth this year. | Explicit: metrics cited |
| 4 | Growth targets justify Series A fundraising next quarter. | Inference: startup context |

**Root need:** "A trust-building pricing page that removes friction for budget-conscious prospects, supports growth metrics for Series A positioning."

**Calibration impact:** This isn't "make a pricing page" — it's a revenue-critical conversion asset. Include competitive positioning, trust signals, and analytics.

### Example 2: Technical (Engineering)

**Surface:** "Our API is too slow. Help me optimize it."

| Why | Answer | Evidence |
|-----|--------|----------|
| 1 | Users complain pages load 5-10 seconds. Satisfaction dropping. | Explicit: user complaints |
| 2 | User base doubled in Q1. Concurrent requests: 100→250/sec. DB is fine. | Explicit: metrics |
| 3 | New users abandoning before load. Retention down 5% MoM. | Explicit: churn data |
| 4 | Acquisition contingent on 80% annual retention. Missing = deal killed. | Explicit: deal terms |

**Root need:** "Reduce API response latency to <500ms at 250+ req/sec to meet acquisition retention targets. Bottleneck is API layer, not database."

**What this changes:** Don't do generic optimization. Profile top 5 endpoints, add Redis caching, measure against retention (not just latency).

### Example 3: Creative (Content/Design)

**Surface:** "Help make our website more engaging."

| Why | Answer | Evidence |
|-----|--------|----------|
| 1 | 60% bounce rate. People land and leave without interacting. | Explicit: analytics |
| 2 | Redesigned for Gen Z audience but content still sounds corporate. | Explicit: stated mismatch |
| 3 | Conversion drops 30%. CAC increasing unsustainably. | Inference: growth math |
| 4 | Pre-Series A. Metrics define valuation. High CAC = red flag. | Inference: startup context |

**Root need:** "Redesign voice and visual experience for Gen Z expectations, targeting <40% bounce and demonstrating product-market fit for fundraising."

**Note on example bias:** All three examples involve startups heading toward fundraising. This reflects a common pattern where stakes escalate through business metrics, but the technique applies equally to non-startup contexts (internal tooling, government projects, personal requests). In those cases, the Why chain bottoms out at operational impact or personal constraint rather than investor metrics.

### When Five Whys Fails

The technique has structural limitations:

| Limitation | Example | Mitigation |
|-----------|---------|------------|
| User has no deeper need | "What time is it?" → no layers to peel | Recognize literal requests via Pass 4; skip Whys entirely |
| Multiple independent root causes | Request stems from 3 unrelated problems converging | Run separate Why chains per problem; merge in reformulation |
| Root cause is emotional, not logical | Frustration drives the request, not a business need | Hand off to Pass 4 (emotional gap detection) instead of forcing deeper Whys |
| Insufficient context for any inference | Cold-start with a single vague sentence | Stop at Why 1; flag the rest as open questions |

## Pitfalls & Countermeasures

| Pitfall | Detection Signal | Countermeasure |
|---------|-----------------|----------------|
| **Blaming people** | "Because Marcus didn't..." | Ask why again — there's always a system issue beneath personal failure |
| **Too abstract** | "Market conditions", "human nature" | Back up to last concrete, actionable answer |
| **Circular reasoning** | Answer repeats the problem | Reframe: "what specifically changes if we solve this?" |
| **Guessing** | "Probably...", "I think...", "generally..." | Ground in explicit statements or flag as open question |
| **Stopping at symptom** | Delivering a "form" when they need a "feedback system" | Always ask at least Why 1 + Why 2 before designing |
| **Missing the constraint** | "For decision-making" (true but incomplete) | Ask "why this format / why now / why this approach?" |
| **Forcing depth** | Why 4 adds nothing new, but you push to Why 5 | Apply the decision heuristic: would one more Why change the reformulation? If no, stop. |

## Acceptance Criteria

A complete Five Whys analysis must include:

- [ ] Surface request captured verbatim (no interpretation)
- [ ] Each Why answer cites its evidence type (explicit/inference/open question)
- [ ] Chain stops at the first level where root need is actionable
- [ ] No Why answer is a rewording of a previous answer
- [ ] Root need statement is a single sentence that would change how a skilled professional responds
- [ ] Open questions (if any) are listed with what their answers would affect

## Pipeline Connections

This pass feeds into Passes 3, 4, and 5. For the full data flow, backtrack protocol, and inter-pass contracts, see the **Data Contracts** and **Pipeline Integration** sections in `SKILL.md`.

**Key handoffs from this pass:**
- **root need** → Pass 3 uses it as starting point for forward-tracing
- **root need** → Pass 5 uses it as the GOAL in the reformulated prompt
- **open questions** → Pass 4 treats these as context gaps
- **Why chain constraints** (timeline, budget, stakeholders discovered during Whys) → Pass 5 CONSTRAINTS

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
