# Seven So Whats Guide: Value Chain Analysis

## Table of Contents

1. [Purpose](#purpose)
2. [The Chain: Forward Tracing](#the-chain-forward-tracing)
3. [When to Stop](#when-to-stop)
4. [The Protocol](#the-protocol)
5. [Examples Across Domains](#examples-across-domains)
6. [Calibration Framework](#calibration-framework)
7. [Pitfalls & Countermeasures](#pitfalls--countermeasures)
8. [Acceptance Criteria](#acceptance-criteria)
9. [Integration with Pipeline](#integration-with-pipeline)

## Purpose

While 5 Whys drills **down** to root cause, 7 So Whats traces **forward** to ultimate impact. This reveals:

| Question | Answer |
|----------|--------|
| How important is this really? | What would change if we solved it perfectly? |
| Where should quality investment go? | High-impact chains deserve more care than low-impact ones. |
| What does success look like at each level? | Helps calibrate response depth and metrics. |
| Who else is affected? | Hidden stakeholders and downstream constraints. |

**The relationship:** 5 Whys answers "What's the real problem?" — 7 So Whats answers "Why should I care about solving it?"

## The Chain: Forward Tracing

Each "So What" builds on the previous answer, tracing a causal chain of implications. Every answer should start with a **concrete outcome**, not abstract value.

| Level | Question | What You Learn | Signal |
|-------|----------|---------------|--------|
| So What 1 | If we solve this, what directly happens? | Functional outcome | Feature works; users benefit |
| So What 2 | What does that enable for users? | Behavior change | Workflow is materially different |
| So What 3 | What changes about how the team/business operates? | Operational impact | Cost structure or capacity changes |
| So What 4 | How does that affect business metrics? | Financial impact | Revenue, retention, or CAC moves |
| So What 5 | Who else cares, and why? | Stakeholder expansion | Investors, board, partners affected |
| So What 6 | What new capability does the org gain? | Strategic capability | Market opportunity expands |
| So What 7 | How does this affect competitive position? | Competitive advantage | Long-term defensibility |

**Critical distinction from 5 Whys:** Each So What should produce a **different audience or scope** of impact. If So What 3 affects the same people as So What 2, you're elaborating rather than tracing forward. Ask: "who NEW cares about this?"

### Evidence Rules

Each So What uses the unified evidence taxonomy from `SKILL.md` (explicit / inferred / open), with a specificity qualifier:

| Evidence | Specificity | Example | Use in Calibration |
|----------|------------|---------|-------------------|
| explicit | quantified | "Support load drops 30%" | Direct metric for success criteria |
| explicit | qualified | "Support team can refocus" | Useful, but add a metric to make it measurable |
| inferred | qualified | "Investors see sustainable growth" | Note as inference; validate if chain reaches Flagship |
| inferred | speculative | "Maybe competitors will..." | Stop here — speculation threshold crossed |

## When to Stop

1. **Implications become speculative.** "If we improve retention, maybe VCs will fund us, and maybe we'll hire..." — stop at the last concrete link.

2. **Outside the org's control.** "Competitors will be forced to match us" — you can't know or control that.

3. **Chain becomes generic.** "More money → team grows → company succeeds" could describe any project. Back up to the last specific outcome.

4. **You've answered the calibration question.** If you know whether this deserves Standard, Premium, or Flagship effort, additional So Whats don't change the decision.

**Decision heuristic:** If the next So What wouldn't change the quality level assignment, stop. The chain's purpose is calibration, not exhaustive forecasting.

## The Protocol

### Step 1: State Root Need (from 5 Whys)

"Enable customers to publish content without manual backend intervention."

### Step 2: So What 1 — Immediate Outcome

What can users directly do?
- "Users publish from the UI without contacting support. Content goes live immediately."

### Step 3: So What 2 — Behavior Change

How does user behavior shift?
- "Publishing becomes self-service. Support tickets for 'can you publish X?' disappear."

### Step 4: So What 3 — Operational Impact

What changes about team operations?
- "Support load drops 30%. Team refocuses on harder problems. Don't need to hire as we scale."

### Step 5: So What 4 — Business Impact

How do metrics move?
- "Lower support costs + longer customer tenure = higher net retention. Unit economics improve."

### Step 6: So What 5-7 — Strategic (only if needed for calibration)

Continue only if calibration is still unclear:
- So What 5: "Investors see scalable growth without proportional support costs."
- So What 6: "With funding, expand to non-technical customers and new segments."
- So What 7: "Self-service platform becomes competitive moat. Differentiate on ease-of-use."

### Step 7: Calibrate

Based on chain depth, assign quality level (see Calibration Framework below).

## Examples Across Domains

### Example 1: Business (Product)

**Root Need:** "Build self-service reporting dashboard for customer usage metrics."

| Level | So What | Evidence Type |
|-------|---------|---------------|
| 1 | Customers see usage in real-time without emailing support | Quantified: removes ticket category |
| 2 | Self-debugging → fewer tickets, longer tenure | Quantified: -20% support tickets |
| 3 | Support team focuses on strategic issues. No hiring needed at 2x scale | Quantified: cost avoidance |
| 4 | Lower support costs + higher retention = profitable growth path | Quantified: unit economics |
| 5 | Predictable profitability = stronger Series A positioning | Qualified: investor narrative |
| 6 | With funding, build analytics features → intelligence platform, not just tool | Qualified: product strategy |
| 7 | Competitors still generate reports manually. We own the decision workflow. | Speculative threshold |

**Calibration:** So What 6-7 chain → **Flagship effort.** Invest in design, reliability, scale planning, analytics tracking.

### Example 2: Technical (Engineering)

**Root Need:** "Migrate database to distributed system for multi-region scaling."

| Level | So What | Evidence Type |
|-------|---------|---------------|
| 1 | Multi-region workloads. Region-1 failure doesn't affect region-2 | Quantified: HA architecture |
| 2 | Asia/Europe users get lower latency. SLA compliance improves | Quantified: latency targets |
| 3 | "Slow performance" tickets drop 40%. Can onboard without proportional support | Quantified: ticket reduction |
| 4 | Higher SLA + lower latency → enterprise market entry. Premium pricing | Qualified: market expansion |
| 5 | Enterprise market attracts VC. $100M+ revenue pathway visible | Speculative threshold |

**Calibration:** So What 4-5 chain → **Premium effort.** Extensive testing, gradual rollout, monitoring, documentation, team training.

### Example 3: Creative (Marketing)

**Root Need:** "Produce weekly video content for TikTok/YouTube audience building."

| Level | So What | Evidence Type |
|-------|---------|---------------|
| 1 | Consistent, platform-native content. Audience sees us regularly | Qualified: content strategy |
| 2 | Followers + views grow. Some audience visits website | Quantified: traffic source |
| 3 | Organic traffic +50%. Lead gen cost drops (viral content = free traffic) | Quantified: CAC reduction |
| 4 | Better unit economics. Can be selective in customers (better fit) | Qualified: business model |
| 5 | Brand moat visible to investors. Not just product; trusted voice | Speculative threshold |

**Calibration:** So What 4-5 chain → **Premium effort.** Invest in production quality, analytics, consistency, experimentation.

**Note on example bias:** All three examples involve startups progressing toward fundraising. This reflects a common pattern, but the technique applies equally to enterprise contexts (where So What chains bottom out at regulatory compliance, operational efficiency, or employee retention) and personal projects (where chains bottom out at learning outcomes or personal satisfaction). Adjust the chain questions to match the user's organizational context.

## Calibration Framework

The core output of Seven So Whats is a quality level assignment that guides all downstream investment.

| Chain Depth | Quality Level | What It Means in Practice |
|-------------|---------------|--------------------------|
| So What 1-2 | **Standard** | Regular effort. Focus on correctness and user experience. Ship when ready. |
| So What 3-4 | **Premium** | Increased rigor. Code review, testing, documentation, analytics. Cross-team coordination if needed. |
| So What 5-7 | **Flagship** | Maximum investment. Design, scalability, edge cases, monitoring, team communication plan, post-launch review. |

### Calibration Decision Table

| Signal | Level | Reasoning |
|--------|-------|-----------|
| Affects only the requesting user | Standard | Blast radius is small |
| Affects a team or department | Premium | Multiple stakeholders |
| Affects company metrics, funding, or market position | Flagship | Strategic importance demands rigor |
| User explicitly said "quick" or "good enough" | Standard (respect stated preference) | Don't over-invest against user wishes |
| Chain reveals higher stakes than user stated | Upgrade by 1 level | User may not realize the downstream impact |

**Trade-off:** Over-calibrating wastes time (flagship effort on a standard task). Under-calibrating risks rework (standard effort on a flagship need). When uncertain, the cost of under-calibration is higher — invest the extra rigor.

### Worked Example: Calibration in Action

**Request:** "Make our error messages better"

**5 Whys root:** Error messages losing 15% of trial signups at conversion point.

**So What chain:**
1. Users understand errors and can retry → fewer bounces
2. Trial-to-paid conversion: 8% → 11% (3% lift for free)
3. 3% more customers/month with same CAC. Unit economics improve.
4. Better metrics → stronger Series A positioning
5. Series A → hire product designer → rethink entire onboarding (10x impact)

**Calibration:** Reaches So What 5 → **Premium effort.** Not just rewriting text — audit all 50+ error states, add actionable next steps, track conversion metrics pre/post, coordinate with product team.

## Pitfalls & Countermeasures

| Pitfall | Signal | Fix |
|---------|--------|-----|
| **Generic chain** | Every So What applies to any project | Back up to last specific outcome with a named metric or stakeholder |
| **Speculation** | "Maybe competitors will...", "If the market..." | Stop. You can't control external forces. |
| **Scope creep via So What** | Chain reveals 10 things worth doing | Calibrate for the current request only. Note strategic insights for future work. |
| **Skipping operational level** | Jumps from user behavior (2) to investor impact (5) | Fill in: what changes for the team? What metric moves? |
| **Same audience every level** | "Users benefit" repeated 3 ways | Each level should introduce a new stakeholder or scope |

## Acceptance Criteria

A complete Seven So Whats analysis must include:

- [ ] Root need statement from 5 Whys as starting point (not surface request)
- [ ] Each So What cites evidence type (explicit/inferred) with specificity (quantified/qualified) per the unified taxonomy in `SKILL.md`
- [ ] Chain stops at or before speculation threshold
- [ ] Each level introduces a new scope of impact or stakeholder
- [ ] Quality level assigned: Standard, Premium, or Flagship with reasoning
- [ ] Calibration decision explicitly stated and justified
- [ ] No So What is a rewording of a previous one

## Pipeline Connections

This pass receives from Pass 2 and feeds into Pass 5. For the full data flow and inter-pass contracts, see `SKILL.md`.

**Key handoffs from this pass:**
- **quality level** (Standard/Premium/Flagship) → Pass 5 includes it as an explicit field in the reformulated prompt
- **value chain** → Pass 5 uses it as the "why this matters" CONTEXT section
- **quantified So What answers** → Pass 5 uses them as success metrics (e.g., "retention: 45% → 60%")
- **stakeholders discovered at So What 5+** → Pass 5 adds them as CONSTRAINTS ("this affects investor narrative")

**Key dependency:** If Pass 2 produced open questions, do not build the So What chain on unverified assumptions. Acknowledge the gaps and note how the calibration would change if the open questions were answered differently.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
