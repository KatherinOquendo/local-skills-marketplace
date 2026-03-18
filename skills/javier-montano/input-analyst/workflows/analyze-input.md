# Workflow: Analyze Input

Complete input analysis workflow from raw user input to reformulated, high-quality prompt.

## Overview

This workflow orchestrates the five-pass analysis system to transform messy human input into precise, actionable prompts. Use this workflow when:

- Raw user input is unclear, typo-laden, or vague
- Intent seems ambiguous or mismatched with the stated request
- You need to verify understanding before proceeding with a task
- Input quality is critical (complex tasks, high stakes, ambiguous requirements)

**Expected time:** 5-15 minutes depending on input complexity
**Outputs:** Reformulated prompt + analysis metadata + confidence assessment

## Workflow Steps

### Step 1: Receive Raw Input

**Input:** User's unfiltered request (text only)

**What to look for:**
- Obvious typos or autocorrect artifacts ("ducking" instead of a profanity)
- Vague language ("make it better," "help me with this thing")
- Missing context (dangling pronouns, assumed knowledge)
- Emotional signals (frustration, hedging, emphasis)
- Scope ambiguity (stated request feels too small or too large)

**Output:** Raw input captured

---

### Step 2: Run Pass 1 (Surface Analysis)

**Tool:** `python tools/typo-detector.py "<input>" --json`

**What it does:**
- Detects typos, spelling errors, misspellings
- Identifies punctuation issues (missing periods, excessive punctuation, run-ons)
- Flags common autocorrect artifacts
- Detects missing vowels, doubled letters, dyslexia patterns
- Normalizes spacing and punctuation

**Review the output:**
1. Check "corrections_count" — is there significant surface noise?
2. Review "corrections" details — do the corrections preserve intent?
3. Check "surface_issues" — identify any major structural problems

**If corrections are extensive:** The user may be:
- Typing very quickly without proofreading
- Using voice-to-text with errors
- Non-native English speaker
- Experiencing dyslexia or autocorrect issues

**Output:** Corrected text + list of corrections + quality assessment

---

### Step 3: Run Pass 2 (Five Whys Analysis)

**Tool:** Use the template from `python tools/text-analyzer.py "<input>" --passes 2 --json`

**What it does:**
- Provides a guided template for Five Whys chain
- Helps dig beneath the surface request to find root need
- Asks: "Why 1, Why 2, Why 3..." until root cause is clear

**How to complete this pass:**

1. Start with the surface request (from Pass 1 corrected text or original if minimal corrections)
2. Fill in Why 1: "What prompted this request? What's the immediate trigger?"
   - Look for business context, timeline, immediate driver
   - Example: "User says 'I need a presentation.' Why? → 'Boss asked for quarterly review'"

3. Fill in Why 2: "What's the broader situation?"
   - Expand from immediate trigger to business context
   - Example: "Why a quarterly review? → 'Team missed targets this quarter'"

4. Fill in Why 3: "What decision or outcome does this lead to?"
   - Look for stakes and consequences
   - Example: "Why does missing targets matter? → 'Affects budget decisions for Q2'"

5. Stop after Why 3 if root cause is clear. Otherwise:
   - Why 4: "Why is that critical?" (if root still unclear)
   - Why 5: "What's the ultimate need?" (only if Why 4 didn't reveal root)

6. Synthesize: Write one sentence capturing the real root need

**Red flags if you're stuck:**
- Circular reasoning ("Because it's important because it's important")
- Guessing without evidence (assume only what's explicitly stated or directly inferable)
- Going too abstract ("market conditions," "human nature") — zoom back in to actionable root cause

**Output:** Root need statement + Five Whys chain (may be partial if root is clear by Why 3)

---

### Step 4: Run Pass 3 (Seven So Whats Analysis)

**Tool:** Use the template from `python tools/text-analyzer.py "<input>" --passes 3 --json`

**What it does:**
- Traces implications forward from root need to ultimate value
- Builds value chain: solution → user behavior → business impact → strategic advantage
- Helps calibrate how much quality investment this deserves

**How to complete this pass:**

1. Start with the root need from Pass 2
2. Fill in So What 1: "If we solve this, what directly happens?"
   - Functional outcome: what becomes possible
   - Example: "Users can publish content without manual support intervention"

3. Fill in So What 2: "What does that enable for users?"
   - User behavior shifts
   - Example: "Publishing becomes self-service; content goes live faster"

4. Fill in So What 3: "What happens to the business?"
   - Operational or financial impact
   - Example: "Support load drops 30%; don't need to hire more support staff"

5. Fill in So What 4: "How does this affect growth?"
   - Business metric or trajectory impact
   - Example: "Lower support costs + higher retention = better unit economics"

6. Stop after So What 4 if impact is clear. Otherwise:
   - So What 5: "Who cares at a strategic level?" (investor, executive, stakeholder perspective)
   - So What 6: "What new capability does organization gain?" (market expansion, differentiation)
   - So What 7: "What's the ultimate, long-term value?" (competitive advantage, moat)

7. **Calibration:** Use the depth of the So What chain to guide quality investment
   - Stops at So What 2-3: Standard engineering effort
   - Reaches So What 5-6: Premium effort, strategic importance
   - Reaches So What 7: Flagship effort, competitive importance

**Red flags if you're speculating:**
- "Maybe competitors will..." → Stop; can't control external forces
- "If the market..." → Stop; outside your influence
- Every So What sounds generic ("more money," "team grows," "company succeeds") → You're too abstract; back up

**Output:** Value chain (So What 1-X) + quality investment calibration

---

### Step 5: Run Pass 4 (Intent Analysis)

**Tool:** `python tools/text-analyzer.py "<input>" --passes 4 --json`

**What it does:**
- Detects gaps between what was typed and what was meant
- Identifies five gap types: vocabulary, scope, expertise, emotional, context
- Flags signals of each gap type

**How to complete this pass:**

1. Review the signals detected by the tool:
   - vocabulary_signals: User using wrong terminology?
   - scope_signals: Understating scope ("just," "quickly," "simple")?
   - expertise_signals: Over-engineering or under-engineering?
   - emotional_signals: Frustration, hedging, blame language?
   - context_signals: Missing context, dangling pronouns?

2. For each gap type detected, fill in:
   - **Explicit statements:** What did the user explicitly ask for?
   - **Implicit signals:** What can you infer from tone, word choice, context?
   - **Gap:** Where is the mismatch between explicit and implicit?
   - **Real ask:** What does the user actually need?

3. Example gap analysis:

```
TYPED: "Make our error messages better"

EXPLICIT: "Error messages," "better"
IMPLICIT: No mention of which errors, impact, or success metrics
          Suggests user is frustrated with current state
          Word choice "better" is vague

GAPS:
- Scope gap: User didn't mention the conversion drop or business impact
- Vocabulary gap: "Better" doesn't capture "reduce bounce at errors"
- Context gap: No mention of which error paths are problematic

REAL ASK: "Improve user experience at error states to reduce
          trial-to-paid conversion drop. Currently 8%; target >10%.
          Error messages are technical jargon; rewrite in plain language."
```

4. Flag any misalignment that should be addressed before proceeding

**Output:** Gap analysis + identified misalignments + "real ask" statement

---

### Step 6: Run Pass 5 (Reformulation)

**Tool:** `python tools/text-analyzer.py "<input>" --passes 5 --json`

**What it does:**
- Synthesizes Passes 1-4 into a high-quality reformulated prompt
- Follows the Playbook quality standard: clear goal + specific constraints + context + output format
- Produces machine-readable template for downstream processing

**How to complete this pass:**

1. Fill in the reformulation template using insights from Passes 2-4:

```
GOAL:
[Clear objective with action verb + measurable outcome]
[From Pass 2 root need + Pass 3 calibration]

CONTEXT:
[Why this matters, what changed, what's at stake]
[Drawn from Pass 2 Five Whys chain + Pass 3 value chain]

INTENT:
[The real ask from Pass 4 gap analysis]
[Explain what user meant vs what they typed]

CONSTRAINTS:
[What to include/exclude, format, length, audience, quality level]
[From Pass 4 gap signals + Pass 3 calibration]

EXPECTED OUTPUT:
[Deliverable type, structure, format, success criteria]
[From original request + Pass 5 reformulation template]
```

2. Example reformulation:

```
ORIGINAL: "Help me create a dashboard for our team"

REFORMULATED:
GOAL: Build a real-time team performance dashboard that shows key metrics
      (velocity, burndown, blocker count) for daily standup sync.

CONTEXT:
- Why: Team is distributed across 3 time zones; standup is async.
- Current: Team leads use 4 different tools to gather status (git, Jira, Slack)
- Problem: No single source of truth; standups take 30+ min to prepare
- Outcome: Dashboard reduces standup prep to 5 min; improves team async coordination

INTENT:
- Real need: Not a pretty dashboard, but a time-saving tool for distributed standup
- Practical success: Standup prep drops from 30 min to 5 min daily

CONSTRAINTS:
- Display: Real-time data (updates every 2-3 min)
- Access: All team members, read-only (no edit from dashboard)
- Metrics: Velocity (story points last 5 sprints), burndown (current sprint),
           blockers (priority 1-2 items stuck >1 day)
- Platform: Web-based, mobile-friendly, no authentication required on local network
- NOT in scope: Historical trends, advanced analytics, custom reporting

EXPECTED OUTPUT:
- Single-page dashboard (no scrolling)
- Auto-refresh every 2-3 minutes
- Clear visual indicators (red/yellow/green status)
- Links to drill into Jira for details
- Shareable URL for slack/wiki
- Setup documentation (how to configure data sources)

QUALITY LEVEL: Standard (team tool, operational importance)
TIMELINE: 1 week development + testing
SUCCESS: Standup prep <5 min, zero missing metrics, 100% uptime on standup day
```

3. Review reformulation for:
   - **Clarity:** Is the goal specific and measurable?
   - **Completeness:** Are constraints explicit?
   - **Calibration:** Does quality investment match importance (from Pass 3)?
   - **Preserves intent:** Does it capture what the user meant, not just what they typed?

**Output:** Reformulated prompt + analysis metadata

---

### Step 7: Output Results

**Verification Checklist:**

Before delivering reformulated prompt, verify:

- [ ] **Preserves original intent:** Did we keep what the user wanted, just made it clearer?
- [ ] **Specific and actionable:** Is there ambiguity remaining? Is the goal measurable?
- [ ] **Constraints are explicit:** Would someone else understand what to do with this prompt?
- [ ] **Success criteria defined:** Can we tell if this succeeded?
- [ ] **Confidence:** Are we confident this is what the user meant?

**Output Format:**

```json
{
  "status": "analysis_complete",
  "confidence": "high|medium|low",
  "original_input": "[user's raw input]",
  "reformulated_prompt": "[complete reformulated prompt]",
  "key_changes": [
    "Changed from 'X' to 'Y' because [reason]",
    "Added constraint 'Z' because [reason]"
  ],
  "assumptions_made": [
    "Assumed user meant 'A' (not 'B') based on context",
    "Inferred timeline 'C' from [signal]"
  ],
  "quality_assessment": {
    "original_clarity": "low/medium/high",
    "expected_downstream_clarity": "high",
    "quality_investment_required": "standard/premium/flagship"
  },
  "next_step": "Send reformulated prompt to task-engine"
}
```

---

### Step 8: Verification: Confirm Reformulation Preserves Intent

**Ask the user to verify** (if possible):

1. "I interpreted your request as: [reformulated goal]. Is that correct?"
2. "I'm assuming [key assumption]. Does that match your intent?"
3. "Success will mean: [success criteria]. Does that align with what you wanted?"

**If yes:** Proceed to task-engine with reformulated prompt
**If no:** Return to Step 5 and revise based on user feedback

---

## Scaling: When to Run Which Passes

Not every input needs all five passes. Use this guide to scale analysis depth:

| Input Quality | Passes to Run | Example |
|---------------|---------------|---------|
| Clear + specific | Pass 4 only (intent verification) | "Create a Python function that sorts a list of dicts by 'date' key" |
| Clear + vague scope | Passes 2, 4, 5 (find root, verify intent, reformulate) | "Help me with my project" |
| Messy + clear intent | Passes 1, 5 (fix surface, reformulate) | "cn u fix teh bugg in login" |
| Messy + vague | All 5 passes (full analysis) | "i need somthing for the meeting tmrw about that thing" |

---

## Tools Reference

### text-analyzer.py (Full Pipeline)

```bash
# Run all passes
python tools/text-analyzer.py "raw input text"

# Run specific passes
python tools/text-analyzer.py "input" --passes 1,4,5

# JSON output for integration
python tools/text-analyzer.py "input" --json

# Language support
python tools/text-analyzer.py "input" --language es
```

### typo-detector.py (Pass 1 Only)

```bash
# Run surface analysis only
python tools/typo-detector.py "raw text here"

# JSON output
python tools/typo-detector.py "raw text here" --json

# Language support
python tools/typo-detector.py "raw text here" --language es
```

---

## Common Issues and Fixes

### Issue: Can't find root cause in Pass 2

**Symptoms:** Why 5 is reached but root still unclear

**Fixes:**
- You may have guessed instead of inferring. Go back to explicit statements only.
- The user may not have shared necessary context. Note it as an "open question."
- The request may genuinely have no root cause (e.g., "What time is it?" → stop at Why 1)

### Issue: So What chain feels generic

**Symptoms:** Every So What sounds like "more money → team grows → success"

**Fixes:**
- You're too abstract. Step back to tangible outcomes, not strategic abstractions.
- Go deeper into specifics (not "better retention," but "x% improvement in d-day 30 retention")
- Stop once you identify how quality investment should scale

### Issue: Too many gaps detected in Pass 4

**Symptoms:** 4-5 gap types detected; reformulation feels like guessing

**Fixes:**
- Ask the user for clarification before proceeding (you may be projecting intent)
- Focus on the strongest signals only
- Note what you don't know as "open questions"
- Reformulate based on what you can infer with confidence; mark rest as assumptions

### Issue: Reformulation is much longer than original request

**Symptoms:** Pass 5 output is 10x longer than input

**Fixes:**
- You may have added too much inferred context
- Separate "context" (necessary for understanding) from "nice to have" (not essential)
- Keep reformulation concise; use GOAL + CONSTRAINTS + SUCCESS as minimum

---

## Integration with Next Steps

**After reformulation:** Send the reformulated prompt to task-engine for processing.

**Quality improvement expected:** Because the reformulated prompt is:
- Explicit about constraints and success criteria
- Grounded in real intent (not literal request)
- Calibrated for appropriate quality investment
- Free of surface-level typos and ambiguity

This upstream quality work → higher baseline quality from downstream tasks → fewer iterations needed → faster, higher-confidence results.

---

## Templates and Checklists

See reference documents for detailed templates:
- `reference/five-whys-guide.md` — Step-by-step Five Whys with examples
- `reference/seven-so-whats-guide.md` — So What chain with value calibration
- `reference/intent-detection.md` — Gap analysis framework with signal detection

See skill file `SKILL.md` for conceptual overview and integration guidance.
