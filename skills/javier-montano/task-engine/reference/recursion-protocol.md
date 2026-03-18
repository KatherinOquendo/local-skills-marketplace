# Recursion Protocol: Thread and Attachment Scanning

This document defines the protocol for scanning thread context and attachments before producing any answer. Recursion ensures you leverage all available information and maintain explicit awareness of information sources.

## The Recursion Principle

Before producing ANY answer, scan your information environment:

1. **Thread context** — All previous messages in the conversation (what has the user told me?)
2. **Attachments** — All files, documents, data provided (what artifacts do I have?)
3. **Stated preferences** — Format, depth, style, confidence requirements (what does the user want?)
4. **Implicit context** — Time constraints, audience, stakes (what's the environment?)

This scan happens BEFORE decomposition, not after. The output of recursion scans informs which sub-problems matter most.

---

## Priority Order: Information Sources

When the same information appears in multiple sources (thread, attachments, general knowledge), use this priority:

**Tier 1: Explicit instructions in current turn**
- User says "Please use this framework" → use it
- User says "Ignore that previous request" → ignore it
- These are binding overrides

**Tier 2: Stated preferences from prior turns**
- User said earlier "I prefer detailed analysis" → deliver detailed
- User said "High confidence required" → target 0.95
- User said "Markdown format" → markdown format

**Tier 3: Information from attachments**
- User provided a document, spreadsheet, video, image → that's primary data
- Trust attachment data over general knowledge (unless contradicted by verification)
- Cite attachment data: "According to your [document name]..."

**Tier 4: Thread context (prior messages)**
- Previous messages in conversation provide context
- Use to disambiguate the current question
- Example: "Earlier you mentioned your team is distributed" → assume distributed team in analysis

**Tier 5: Implicit context (environment clues)**
- Time of day, conversation flow, apparent urgency
- Use for tone/depth calibration
- Don't rely on for factual information

**Tier 6: General knowledge**
- Only use when above tiers don't apply
- Mark as "from my training data" if user might want to verify

---

## Thread Scanning Protocol

### Step 1: Read ALL prior messages in thread

**What to extract:**
- Facts stated by the user (treat as ground truth)
- User's stated preferences (format, depth, style)
- Constraints mentioned (time, budget, team size)
- Context clues (what problem are they solving?)
- Prior analysis or decisions

**Technique:**
- Skim recent messages first (last 5-10)
- For questions that reference earlier context, scroll back and read the full history
- Note any contradictions or evolution in the user's thinking

**Example:**
```
User (Turn 1): "We're considering hiring a VP of Sales. She's a strong candidate."
User (Turn 3): "Actually, one concern is that she's never worked with our specific product category before."

Action: Incorporate both statements. Not a contradiction; an evolution.
Updated context: "Strong candidate overall, but product category is a gap."
```

### Step 2: Identify stated preferences

**What to look for:**
- Format: "Can you structure this as...", "Use a table", "Explain simply"
- Depth: "Keep it brief", "Deep dive", "High-level overview"
- Confidence: "I need to be confident in this", "This is exploratory"
- Tone: "Professional", "Casual", "For a board presentation"
- Audience: "For engineers", "Non-technical stakeholder", "My boss"

**Technique:**
- Search recent messages for "please", "I need", "can you", "I want"
- These often indicate preferences
- If no stated preference, infer from context (board presentation → formal, detailed)

**Example:**
```
User: "Can you give me a high-level breakdown? I have 10 minutes."

Stated preferences:
- Format: Breakdown (structured list or outline)
- Depth: High-level (summary, not exhaustive)
- Time: 10 minutes (implication: be concise, skip deep dives)

Action: Use bullet points, limit to 5-7 key items, skip nuance
```

### Step 3: Identify constraints and context

**What to look for:**
- Time constraints: "Need this by Friday", "This is urgent"
- Resource constraints: "Limited budget", "Small team"
- Domain context: "We're a startup", "We're in healthcare", "Non-technical buyer"
- Risk context: "This is a critical system", "Customer is unhappy"
- Historical context: "We tried this before and it failed", "This is our 3rd iteration"

**Technique:**
- Scan for constraint language: "only", "limited", "must", "can't"
- Build a constraint list for reference during analysis

**Example:**
```
User: "We need to scale to 100K concurrent users, but we're a startup with 3 engineers. We've tried cloud infrastructure before and regretted the complexity. What approach should we take?"

Constraints extracted:
- Scale: 100K concurrent users
- Team: 3 engineers (small, limited bandwidth)
- Historical: Cloud infrastructure was negatively received
- Inference: Prefer simplicity and maintainability over cost optimization

Action: Avoid recommending complex distributed systems. Suggest simple, local solutions first.
```

### Step 4: Assess information completeness

**Ask yourself:**
- What information do I have? (Facts, constraints, preferences)
- What information am I missing? (Data I'd need to answer better)
- How does missing information affect my confidence?

**Document the gaps:**
- Create a list of missing information
- For each gap, estimate its impact on confidence
- Decide: retrieve, or deliver with caveat?

**Example:**
```
Question: "Should we hire this candidate?"

Information I have:
✓ Resume and interview feedback
✓ Role requirements
✓ Team composition
✓ Stated preferences (need high confidence, will do reference checks)

Information missing:
✗ Reference checks (user said will do, but not yet done)
✗ Technical test results
✗ Culture fit assessment with team
✗ Compensation expectations

Impact: Missing information limits confidence to 0.75 (will increase to 0.85-0.90 after references)
Action: Deliver preliminary assessment, recommend next steps for full verification
```

---

## Attachment Scanning Protocol

### Step 1: List all attachments

Before starting, identify what the user has provided:
- Documents (PDF, DOCX, TXT)
- Spreadsheets (CSV, XLSX)
- Code files (source code, config files)
- Images (diagrams, screenshots, photos)
- Data (JSON, API responses, database exports)
- Other (videos, audio, archives)

**Action:** Read the filename and file type. These often indicate the purpose.

### Step 2: Scan attachment content

**For documents:**
- Read headings to understand structure
- Skim for key numbers, decisions, constraints
- Look for dates (how fresh is this information?)
- Note what the user highlighted or annotated

**For data/spreadsheets:**
- What are the columns? (What's being measured?)
- What are the row counts? (How much data?)
- Are there trends or anomalies? (What stands out?)
- What's the date range? (How recent?)

**For code:**
- What's the purpose of this code? (What does it do?)
- What's the current state? (Working? Broken? In progress?)
- What's the question? (What does the user want to know about it?)

**For images/diagrams:**
- What does this visualize? (Architecture? User flow? Data model?)
- What's your first impression? (Well-designed? Complex? Unclear?)
- How does this relate to the question?

### Step 3: Integration priority

**Priority rules:**

- **Quantitative data (spreadsheets, metrics) beats qualitative opinion** — Use numbers as ground truth
- **Provided documents beat general knowledge** — User gave you this for a reason
- **Recent data beats old data** — Verify freshness
- **Direct quotes from user beat your paraphrase** — When citing, use their words

**Example:**
```
User: "I think our conversion rate is declining because of the price increase."
Attachment: Spreadsheet showing conversion rates over time

The spreadsheet shows:
- Before price increase: 5.2% conversion
- After price increase: 4.8% conversion (8% drop)

Action: "Price increase coincides with 8% conversion drop (per your data), but other factors may contribute.
Recommend analyzing [specific metrics] to isolate the cause."

Key: Used their data, not speculation. Acknowledged their hypothesis, asked for deeper analysis.
```

### Step 4: Cite attachment sources

When using information from attachments, be explicit:

**Good citations:**
- "According to your Q3 revenue report..."
- "As shown in the architecture diagram you provided..."
- "Your customer feedback spreadsheet shows..."
- "The performance benchmark you attached indicates..."

**Avoid:**
- "Market data shows..." (what market data? theirs? general?)
- "Reports indicate..." (which reports?)
- "The data suggests..." (your data? mine? unclear)

---

## Preference Integration

### Format Preferences

| User Preference | Action |
|---|---|
| "Keep it brief" | Use bullet points, max 3-5 items, executive summary |
| "Detailed analysis" | Full decomposition, all nuances, examples |
| "Markdown format" | Use markdown headers, lists, code blocks |
| "Spreadsheet/table" | Organize as table for easy comparison |
| "Walkthrough format" | Step-by-step, numbered, actionable |

### Depth Preferences

| User Preference | Action |
|---|---|
| "High-level overview" | Summary only, skip implementation details |
| "Deep dive" | All nuances, caveats, advanced considerations |
| "Exploratory" | Open-ended, multiple options, no single recommendation |
| "Executive summary" | 1 page, key findings, recommendation |

### Confidence Preferences

| User Preference | Action |
|---|---|
| "High confidence needed" | Target 0.95, full DSVSR, iterate until verified |
| "Exploratory" | Target 0.85, identify gaps, offer caveats |
| "Rough estimate" | Target 0.70, flag assumptions |

---

## Completeness Statement Template

Always include a completeness statement to show your information scan:

### Format 1: Detailed

```
SOURCES REVIEWED:
• [Number] messages in thread (from [date] to present)
• [Number] attachments: [names]
• Stated preferences: [list, e.g., "high confidence required", "non-technical audience"]
• Constraints identified: [list, e.g., "3-person team", "budget limited", "urgent"]

INFORMATION GAPS:
• [Gap 1]: Would increase confidence to [0.XX] if available
• [Gap 2]: Required for full recommendation (currently unknown)
• [Gap 3]: Non-critical, but would clarify [aspect]

IMPACT ON CONFIDENCE:
• Missing information limits confidence to [0.XX]
• Recommend retrieving [specific gap] to reach [target confidence]
```

### Format 2: Concise

```
RECURSION SCAN:
✓ [N] prior messages reviewed
✓ [N] attachments processed: [names]
✓ Stated preferences: [summary]
✓ Key constraints: [summary]

Information gaps: [brief list]
Confidence impact: [how gaps affect confidence]
```

### Format 3: Minimal (for simple questions)

```
Based on your recent messages and the [document name] you provided.
```

---

## Information Contradiction Protocol

### When sources contradict

**Situation:** User said "X is true" in Turn 1, but their attached spreadsheet shows "X is false"

**Protocol:**
1. Identify the contradiction explicitly
2. Cite both sources
3. Ask for clarification OR make a judgment call based on priority order (facts beat opinions)

**Example:**
```
You mentioned earlier that "our sales team closes deals in 30 days."
However, your CRM data (attached) shows average deal cycle is 45 days.

Two possibilities:
A) The 30 days refers to a specific segment (large deals? enterprise?)
B) The data is more current than your earlier estimate

Recommendation: I'll use the 45-day figure from your CRM data (most recent), but please clarify if the 30-day figure applies to a specific segment.
```

---

## Recursion in Practice

### Example 1: Hiring Decision with Attachments

**Turn 1 User message:** "Should we hire Sarah? She's a strong candidate."

**Turn 2 Attachment:** Resume, interview feedback, market comp data

**Turn 3 User message:** "Oh, also, our team is distributed across 5 time zones and very async-first. She's been in co-located companies mostly."

**Recursion scan output:**
```
SOURCES:
• 3 prior messages (evolution of criteria)
• Attachments: Resume, interview feedback, market comp data
• Stated preferences: Decision-focused (should we hire?)
• Constraints: Distributed, async-first team (culture fit important)

PRIORITY CONTEXT:
From Turn 3: Team is distributed/async-first
This is recent, so prioritizes culture fit as a major factor
Resume shows co-located background (potential gap)

INFORMATION GAPS:
• Cultural fit assessment vs. distributed team (critical)
• References not yet checked
• Communication style compatibility unknown

CONFIDENCE IMPACT:
Starting confidence: 0.70 (without culture fit assessment)
Required for recommendation: 0.85 (high stakes decision)
Gap: 0.15 points (mostly from culture fit + references)

RECOMMENDED NEXT STEPS:
1. Assess communication preference (sync vs. async)
2. Check references, especially previous remote work experience
3. If culture fit checks pass, confidence → 0.88
```

### Example 2: Technical Decision with Code Attachment

**User:** "Can we migrate to this new framework?"

**Attachment:** Sample migration code, current codebase metrics

**Recursion scan:**
```
SOURCES:
• Question is direct (migration decision)
• Attachment: Sample code, current metrics
• No stated preferences (infer: technical audience)
• Implicit stakes: High (framework lock-in)

DATA FROM ATTACHMENTS:
• Current codebase: [N] lines of code, [tech stack]
• Sample migration: [approach, effort estimate]

INFORMATION GAPS:
• Team familiarity with new framework (critical)
• Roadmap impact (what gets delayed?)
• Migration risk assessment (what breaks?)

ACTION:
Will require FULL DSVSR (complexity: 6+ points)
Sub-problems:
  - SP-1: Feature parity assessment (use attachment as baseline)
  - SP-2: Migration effort (use sample code to estimate)
  - SP-3: Team learning curve (requires team input)
  - SP-4: Business impact
```

---

## Special Case: Implicit Information

Sometimes the user doesn't explicitly state something, but context makes it clear.

**Implicit signals to watch for:**
- Time of day sent → urgency level
- Message frequency (many messages in short time) → pressure
- Repeated keywords → importance
- Question escalation (moved from question to urgent demand) → stakes increased

**Example:**
```
Turn 1 (calm): "Curious about cloud migration options"
Turn 2 (more urgent): "Client is asking about timeline"
Turn 3 (pressure): "Client might leave unless we have a plan by Friday"

Implicit escalation: Stakes and urgency have increased
Action: Increase target confidence from 0.85 to 0.90 (higher stakes)
Action: Time-box analysis to 3 hours max (deliver Friday)
```

---

## Meta-Protocol: When Recursion Reveals Gaps

If your recursion scan reveals that you're missing critical information:

**Decision tree:**
```
Is the missing information retrievable from the thread/attachments?
├── YES → Retrieve it before starting DSVSR
└── NO → Continue to next question

Is the missing information retrievable with user input (1-2 minutes)?
├── YES → Ask the user (pause analysis, get info, continue)
└── NO → Continue to next question

Will proceeding without this information limit confidence below 0.75?
├── YES → Deliver with explicit caveat (document the gap, its impact, and recommended next step)
└── NO → Proceed normally
```

---

## Key Takeaways

1. **Recursion is the first step** — Scan context before decomposing
2. **Priority order matters** — Recent explicit info beats old general knowledge
3. **Cite your sources** — Show the user that you used their data
4. **Gaps are normal** — Document them and their confidence impact
5. **Preferences shape analysis** — Honor stated preferences in format and depth
6. **Contradictions require clarification** — Don't hide conflicts; surface them
