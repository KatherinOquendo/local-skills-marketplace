# Intent Detection: Gap Analysis Framework

## The Core Problem

Users often don't say what they mean. They might:
- Use wrong vocabulary for the right concept
- Understate scope ("fix this thing" meaning "redesign the system")
- Avoid explaining expertise gaps (ask for "algorithm" when they mean "process")
- Hide emotional frustration behind technical requests
- Leave context unstated because it's obvious to them

Intent Detection is the process of finding the **gap between typed request and actual need**, then reformulating the request to close that gap.

## The Five Gap Types

Each gap type has specific detection signals and reformulation strategies.

### Gap Type 1: Vocabulary Gap

**What it is:** User knows the concept but uses wrong word for it.

**Why it happens:**
- Domain mismatch (user from non-technical background using programming words)
- Jargon confusion (similar-sounding terms)
- Translation or language barrier

**Detection Signals:**

| Signal | Example | What it suggests |
|--------|---------|------------------|
| Uses wrong term consistently | "I need an algorithm for sorting" (means: a workflow or process) | May not know correct terminology |
| Mixes domains | "Use machine learning to predict which customers will churn" (means: identify patterns in historical data, not build ML model) | Borrowed terminology from adjacent field |
| Over-technical for context | "I need JSON serialization in the database" (means: store structured data) | Terminology exceeds actual need |
| Describes outcome, not mechanism | "Make it use AI" (means: automate this repetitive task) | Don't know the word for what they want |
| Vague placeholder words | "Do the thing," "use the strategy," "implement the solution" | Vocabulary gap + scope gap |

**Reformulation Strategy:**

1. Identify what they actually need (the concept)
2. Use correct terminology for that concept
3. Add explanation of what it actually is (for clarity)
4. Ask clarifying questions if mapping is uncertain

**Example:**

```
TYPED: "We need machine learning to predict churn"

SIGNALS:
- "Machine learning" is trendy but often used incorrectly
- Context is: we have 2 years of customer data, we notice some customers cancel
- No mention of training models, data science team, or deployment infrastructure

GAP: User means "analyze historical data to identify patterns that predict
churn," not "build and deploy a machine learning system"

REFORMULATION:
Objective: Analyze 2 years of customer data to identify patterns
that precede churn. Create a simple scoring system to flag at-risk customers.

What this IS NOT:
- Not a machine learning model (we don't need to build/train/deploy)
- Not a predictive system (we're not building automation)

What this IS:
- Data analysis + pattern identification (which customers share common traits?)
- Actionable output (a list of at-risk customers + why, for manual intervention)

Better term: "Churn risk analysis" or "Customer segmentation for retention"
```

### Gap Type 2: Scope Gap

**What it is:** User understates the actual scope needed.

**Why it happens:**
- Doesn't realize scale of the problem
- Underestimates dependencies
- Too modest about asking for investment
- Describes a symptom, not the underlying problem

**Detection Signals:**

| Signal | Example | What it suggests |
|--------|---------|------------------|
| Minimizing language | "Just" fix this, "quickly" add that, "simple" change | Actual scope is larger than stated |
| Symptom language | "Fix the bug," "make it faster," "improve this" | Real need is architectural, not tactical |
| Missing dependencies | "Update the login flow" (without mentioning: database schema changes, API changes, mobile app changes) | Scope is much larger than realized |
| Vague deliverable | "Make a dashboard," "create a report," "build a tool" | What exactly is it? How many features? |
| "While you're at it" clauses | "Fix X. Also, maybe we should Y?" | Multiple needs, bundled as one |

**Reformulation Strategy:**

1. Ask "why" to understand root need (use Pass 2: 5 Whys)
2. Identify all affected systems/stakeholders
3. Expand scope to address root cause, not just symptom
4. Break into phases if scope is large

**Example:**

```
TYPED: "Fix the slow API"

SIGNALS:
- No mention of which endpoints, which traffic levels, what latency
- Doesn't mention if database is bottleneck or query optimization is needed
- No context on impact (how is slowness affecting users?)

REAL SCOPE (from 5 Whys):
- Why slow? → 3 endpoints handling 60% of traffic are unoptimized
- Why now? → New user growth = doubled concurrent requests
- Why impact? → Retention dropping because of page load times
- Why matters? → Affects acquisition deal closure (3 months out)

REFORMULATION:
Scope: Reduce latency on 3 critical endpoints (login, dashboard, publish)
       from current p99 2.5s to <500ms at peak traffic (250 req/sec).

Not in scope (yet):
- Redesign entire API
- Migrate to new database
- Rebuild frontend (that's separate)

Success metric:
- p99 latency <500ms at target load
- Retention improves within 2 weeks of deployment
- Deal closure metrics improved for acquisition discussions

Timeline: 2 weeks analysis + optimization, 1 week testing
```

### Gap Type 3: Expertise Gap

**What it is:** User asks for X but means Y because they don't know the right vocabulary for their actual need.

**Why it happens:**
- User is junior/new to domain
- Jumping to solution before understanding problem
- Asking what they think they should ask, not what they actually need
- Terminology confusion (thinks X means what Y means)

**Detection Signals:**

| Signal | Example | What it suggests |
|--------|---------|------------------|
| Technical request with non-technical context | "Use a hash table" (from someone who just learned data structures) | Learning stage; probably doesn't need advanced technique |
| Over-engineering | "Set up Kafka for event streaming" (actual need: store and replay a few events) | Overkill; doesn't understand actual requirements |
| Mixing levels of abstraction | "Use machine learning and also manually script it" | Doesn't understand the concepts |
| "Best practice" language | "We should use microservices because it's modern" (without understanding tradeoffs) | Cargo-cult programming; doesn't match actual need |
| Asking for tool instead of outcome | "Install Docker" (actual need: deploy the application) | Confusing tool with the problem it solves |

**Reformulation Strategy:**

1. Ignore the proposed solution; focus on the problem
2. Ask what they're trying to achieve (not how to achieve it)
3. Offer the simplest solution that solves the actual problem
4. Explain why simpler approach is better (if that's true)

**Example:**

```
TYPED: "We need to use machine learning to predict user behavior"

SIGNALS:
- No mention of features, training data, model evaluation
- Context: early-stage startup, 2 people
- Actual use case: "We want to know if a user will upgrade to paid"

EXPERTISE GAP: User equates "predict" with "machine learning"
Actual need: Identify signals that correlate with upgrade likelihood

REFORMULATION:
Goal: Identify patterns that predict which users will upgrade from free to paid.

Approach (NOT machine learning):
1. Analyze data: which free users upgraded? What do they have in common?
2. Identify signals: Did they use Feature X more? Have higher engagement? etc.
3. Create simple rules: If [signal], then likely to upgrade
4. Test: Show this to sales team, see if it's useful
5. Iterate: Refine rules based on feedback

Why not ML?
- Too early (we have <500 users; ML needs 10k+ with clean labels)
- Too complex (team would spend 2 months on it, get mediocre results)
- Simpler approach works better (interpretable rules > black-box model at this stage)

Timeline: 1 week analysis + reporting
Success: Actionable signals to inform sales/retention outreach

Later: If this is successful and we have 50k+ users, revisit ML.
```

### Gap Type 4: Emotional Gap

**What it is:** User's emotional state or frustration is driving the request, but they're asking for a technical solution.

**Why it happens:**
- Embarrassment about asking for emotional support
- Work culture expects technical/professional framing
- User is venting, not actually asking for that solution
- Frustration is the real issue, not the stated problem

**Detection Signals:**

| Signal | Example | What it suggests |
|--------|---------|------------------|
| Hedging / vague language | "This probably doesn't matter, but..." "Maybe I'm overthinking..." | Emotional anxiety, not technical confidence |
| Negative framing | "This is terrible," "Nothing works," "Why does this exist?" | Frustration, not objective problem statement |
| Blame language | "The previous developer was incompetent," "Management doesn't understand" | Emotional frustration at people/decisions |
| Superlatives | "The WORST code I've ever seen," "IMPOSSIBLE to use" | Emotional reaction, not measured assessment |
| Self-deprecating | "I'm probably stupid for not understanding this," "I guess I should just learn to code" | Insecurity driving the request |
| Mixed emotions + tech | "This makes me so frustrated because X doesn't work, and I'm worried about Y" | Emotional layer present; not just technical problem |

**Reformulation Strategy:**

1. Acknowledge the emotion (validate it; don't dismiss)
2. Separate emotion from technical problem
3. Address the technical problem clearly
4. Offer emotional support/context if relevant

**Example:**

```
TYPED: "This code is a DISASTER. The previous developer was incompetent.
        Can you help me fix it? I'm worried I'll break something."

SIGNALS:
- All-caps "DISASTER" = emotional intensity
- Blame language (incompetent developer) = frustration
- "I'm worried" = anxiety about making changes

EMOTIONAL GAP: User is frustrated with inherited code and anxious about
making changes. Technical request = plea for help managing that anxiety.

REFORMULATION:
Goal: Refactor the [system] module to improve readability and add tests.
      This will reduce risk of breaking changes and give you confidence
      for future maintenance.

Emotional support:
- It's normal to feel overwhelmed with unfamiliar code. Don't blame the
  previous developer; code complexity grows over time.
- Tests will give you safety net. Start with one module, not everything.
- Break into phases: tests first (low risk), then refactoring (safer).

Technical approach:
Phase 1: Add tests for current behavior (without changing code)
         This gives you confidence that your changes don't break anything
Phase 2: Refactor systematically (one function at a time)
Phase 3: Document as you go (helps you understand + future maintainer)

Success: Improved readability + test coverage + your confidence
Timeline: 2 weeks for phase 1, 1 week per phase after
```

### Gap Type 5: Context Gap

**What it is:** User assumes shared context that isn't explicitly stated.

**Why it happens:**
- It's obvious to them (they've been working on this for months)
- Dangling pronouns ("fix this" referring to something not mentioned)
- Missing background information
- Different mental models of "the problem"

**Detection Signals:**

| Signal | Example | What it suggests |
|--------|---------|------------------|
| Dangling references | "It's not working," "This needs to be fixed," "Make it better" | No clear antecedent; context missing |
| Assumed shared knowledge | "You know the issue with X" (no prior mention of X) | User's context ≠ reader's context |
| Pronouns without context | "They're asking for this," "It's causing problems" | Who/what is "they"/"it"? |
| Implicit dependencies | Mentions "the database change" without explaining what changed | Assumes you know the system |
| Inside jokes or references | "Handle the widget thing like we talked about" | Context exists only in their head |

**Reformulation Strategy:**

1. Ask clarifying questions to fill gaps
2. Make all references explicit
3. Add necessary background
4. Avoid pronouns; use names/proper nouns

**Example:**

```
TYPED: "Can you review the changes and make sure it's working?"

SIGNALS:
- "The changes" = what changes? To what system?
- "It's working" = working for whom? In what context?
- No mention of what was modified, why, or what success looks like

CONTEXT GAPS:
- No mention of which system (API? Database? Frontend?)
- No mention of what you're testing (happy path? Error cases? Performance?)
- No mention of who will use this
- No mention of when it's needed

REFORMULATION:
Goal: Review the authentication refactor (changes to User model and
      auth middleware) to ensure it works correctly before merging to main.

Context:
- Why: Session handling was causing login failures for some users
- What changed: User model split into User + Session tables
- Who uses it: All 500+ daily active users will be affected
- Timeline: Need to merge by Friday (Friday deploy window)

What to test:
1. Login with email + password (happy path)
2. Login with OAuth (Google, GitHub)
3. Session expiration (30 min timeout)
4. Concurrent logins (user with 2+ open sessions)
5. Password reset flow
6. Edge cases: very long sessions, rapid login/logout

Success criteria:
- All test cases pass
- No regressions in metrics (login success rate)
- Support doesn't report new session issues post-deploy

Expected timeline: 2-3 hours review + testing
```

Notice how the reformulation is now clear because context is explicit.

## The Protocol: From Typed to Real Ask

### Step 1: Transcribe Explicit Statements

Write down exactly what the user said. Look for:
- Direct statements (what they asked for)
- Constraints they mentioned (format, timeline, budget)
- Success criteria they defined (or didn't)

Example: "I need a Python script to analyze user data"

Explicit statements:
- Language: Python
- Deliverable: Script
- Purpose: Analyze user data
- Scope: Unspecified

### Step 2: Identify Implicit Signals

What can you infer from word choice, tone, context?

| Signal Type | Example | Inference |
|-------------|---------|-----------|
| Hedging language | "Maybe we could..." "If it's not too much..." | User is uncertain; may underestimate scope |
| Urgency words | "ASAP," "by Friday," "emergency" | Timeline is tight; may sacrifice quality |
| Minimizing words | "Just add," "quick fix," "small change" | Scope likely understated |
| Emotional words | "Frustrated," "worried," "disappointed" | Emotional factor in play |
| Domain mixing | Uses technical + business terms | Cross-functional context |
| Missing info | Doesn't mention X (which you'd normally ask) | Either obvious to them, or they don't know |

Example additions:
- Hedging: "Maybe we could..." → User uncertain about whether this is the right approach
- No mention of format → Probably doesn't know what format they need

### Step 3: Identify Gaps Between Explicit and Implicit

What's the mismatch?

| Explicit | Implicit | Gap | Type |
|----------|----------|-----|------|
| "Analyze user data" | No mention of output, use case, scale | What analysis? What will you do with it? | Scope gap |
| "Python script" | But mentions "real-time," "thousands of users" | Python script won't scale to real-time + thousands | Expertise gap |
| "Make it faster" | No mention of current speed, target speed, or impact | What does "faster" mean? How fast do you need? | Vocabulary gap |

### Step 4: Form the "Real Ask"

Synthesize explicit + implicit + gap analysis into the real ask.

**Real Ask Formula:**
```
The user really needs: [synthesized from 5 Whys + context]
Not: [what they typed]
Because: [gap that revealed the mismatch]
```

Example:
```
TYPED: "I need a Python script to analyze user data"

REAL ASK: "Build an automated daily report that identifies churn signals
in our customer base, so the retention team can reach out to at-risk
customers before they cancel."

NOT: A one-time Python analysis script
BECAUSE: User mentioned "daily," "at-risk," and "retention team actions"
         This suggests ongoing use and business decision support,
         not one-time exploratory analysis

Gap analysis revealed:
- Scope: Daily + at-risk identification = ongoing system, not script
- Timeline: Implicit urgency (retention team needs it now)
- Output: Not just analysis, but actionable recommendations
- Expertise: User may not know this requires database integration +
            automation, not just Python scripting
```

## Signal Detection Table: Quick Reference

Use this table during pass 4 to quickly identify gaps:

| Gap Type | Common Words | What to Look For | Question to Ask |
|----------|--------------|-----------------|-----------------|
| Vocabulary | Algorithm, AI, machine learning, blockchain, database | Technical term used with non-technical context | What specifically will you do with this? |
| Scope | "Just," "quickly," "simple," "maybe," "also," "while you're at it" | Minimizing language, bundled requests | What's the root need here? Why now? |
| Expertise | Over-technical ("JSON serialization") or under-technical ("make it smart") | Mismatch between tool complexity and actual need | What are you trying to achieve? (Not how) |
| Emotional | "Frustrated," "worried," "terrible," "impossible," "again" | Emotional intensity, blame language, repetition | What's the underlying concern here? |
| Context | Dangling pronouns, no background, assumed knowledge | Missing information that would be obvious to writer but not to reader | Can you give me more context on X? |

## Reformulation Strategies Per Gap Type

### For Vocabulary Gaps
- Use correct terminology
- Explain what the correct term means
- Clarify what they asked vs what they need

### For Scope Gaps
- Use 5 Whys to uncover root need
- Identify all affected systems
- Break into phases if scope is large
- Define success metrics specifically

### For Expertise Gaps
- Ignore proposed solution; focus on problem
- Ask about constraints (team size, timeline, resources)
- Recommend simplest solution first
- Explain why simpler approach is better

### For Emotional Gaps
- Validate the emotion
- Separate emotional context from technical problem
- Address both the technical issue and emotional concern
- Offer reassurance/support where appropriate

### For Context Gaps
- Ask clarifying questions
- Replace pronouns with proper nouns
- Add necessary background
- Confirm understanding

## Edge Case: When the Literal Request IS the Real Ask

**Sometimes there's no gap.** The user said exactly what they meant.

**Detection:**
- Explicit and implicit align
- No signals of uncertainty, frustration, or hidden context
- Request is specific and measurable
- User has relevant expertise

**Example:**
```
TYPED: "Create a Python function that sorts a list of dictionaries by 'date' key"

CHECK FOR GAPS:
- Explicit: Python function, sort, list of dicts, by 'date' key
- Implicit: Clear scope, specific requirement, direct request
- Vocabulary: Correct terminology, no mismatch
- Scope: Well-defined, no minimization
- Expertise: Language + operation + data structure all mentioned appropriately
- Context: All necessary info present
- Emotional: None

VERDICT: No gap. This is what they mean.

REFORMULATION: Direct response
Goal: Create a Python function that accepts a list of dictionaries and
      returns them sorted by the 'date' key in ascending order.

Function signature:
def sort_by_date(records: list[dict]) -> list[dict]:
    return sorted(records, key=lambda x: x['date'])

That's it. No additional analysis needed.
```

In this case, Pass 4 confirms intent but doesn't require reformulation. The user asked for what they needed.

## Integration with Reformulation (Pass 5)

The reformulated prompt from Pass 5 should directly address all gaps identified in Pass 4:

```
ORIGINAL REQUEST: "Make error messages better"

PASS 4 ANALYSIS:
Gap type: Scope gap (symptom described, not root cause)
Gap type: Context gap (no info on which error messages, impact, or success metrics)
Gap type: Vocabulary gap (user may mean "user experience" not just "messages")

REFORMULATION (Pass 5):
Goal: Improve user experience at error states to reduce trial-to-paid
      conversion drop from 8% to >10%.

Current situation:
- Error messages are technical jargon (e.g., "Socket timeout")
- Users bounce when they hit errors (don't retry)
- 15% of trial signups fail at first error

What to change:
- Rewrite errors in plain language (explain what went wrong in user terms)
- Add actionable next steps (what should the user do now?)
- Add context (why did this happen? Not the user's fault?)

What NOT to change (yet):
- Don't redesign entire onboarding (that's phase 2)
- Don't change system architecture (errors are symptom, not cause)

Success metrics:
- Error message clarity: 80%+ users understand error + next step
- Bounce rate at errors: <8% (down from 15%)
- Conversion rate: >10% (up from 8%)

Timeline: 1 week messaging + testing

Why this matters:
- Conversion improvement = better unit economics
- Better metrics = stronger Series A positioning
- This phase informs future onboarding redesign
```

This reformulation directly addresses all gaps because they were explicitly identified in Pass 4.
