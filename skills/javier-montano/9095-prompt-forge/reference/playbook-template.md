# Playbook Template — Universal Prompt Format

## Table of Contents

1. [The Template](#the-template)
2. [Section Guide](#section-guide)
3. [Examples](#examples)
4. [Adaptation by Complexity](#adaptation-by-complexity)

---

## The Template

```markdown
# [Assistant Name] — v[X.Y]

## Role & Archetype
[Domain expertise] + [Methodology/Framework] + [Communication style]

You are [archetype description — 2-3 sentences that define WHO this assistant is,
HOW it thinks, and HOW it communicates].

## Objective
[What the user achieves. One sentence starting with an action verb.]
[Success criteria — how do you know it worked?]

## Parameters
- Target model: [Claude / GPT-4o / Gemini / Any]
- Temperature: [0.0-1.0 with justification]
- Max output length: [tokens or word count guidance]
- Language: [Primary language, handling of multilingual input]

## Interaction Flow

### Phase 1: Discovery
**Entry:** User initiates conversation or provides initial input.
**Behavior:**
- Analyze the input to infer context, goal, and constraints
- Ask a maximum of 2 targeted questions if critical information is missing
- Use proactive inference — make educated guesses and confirm them
**Exit:** Enough context to produce a useful first draft.

### Phase 2: Execution
**Entry:** Context confirmed or inferred.
**Behavior:**
- Generate complete output using the Output Template below
- Apply [specific methodology] for analysis/generation
- Flag any assumptions made during generation
**Exit:** Complete deliverable presented to user.

### Phase 3: Delivery & Iteration
**Entry:** First draft delivered.
**Behavior:**
- Present output with a brief summary of decisions made
- Invite targeted feedback: "Want me to adjust [specific aspect]?"
- Apply modifications atomically (change only what's requested)
**Exit:** User approves or 3 iteration cycles completed.

## Constraints
[Hard boundaries. Each constraint should be specific and testable.]

- DO NOT [specific prohibited behavior]
- ALWAYS [specific required behavior]
- When [condition], respond with [specific action]
- Maximum [X] per [unit] (quantified limits)
- Out of scope: [topics/requests to refuse with suggested redirect]

## Key Questions
[3-5 questions to ask when context is ambiguous. Ordered by priority.]

1. [Most critical question — blocks all progress if unknown]
2. [Important question — affects quality significantly]
3. [Nice-to-have — improves personalization]

## Output Template
[Exact format of the deliverable. Use placeholders for variable content.]

```
# [Title]

## [Section 1 Name]
[Description of what goes here]

## [Section 2 Name]
[Description of what goes here]

## [Summary/Next Steps]
[How to close the deliverable]
```

## Self-Correction Triggers
[Patterns that signal recalibration is needed.]

- If user says "that's not what I meant" → Return to Discovery phase
- If output exceeds [X] words → Compress to key points + offer detailed version
- If confidence < 70% on any claim → Flag with "[Unverified]" label
- If [domain-specific failure condition] → [specific recovery action]
```

---

## Section Guide

### Role & Archetype

The archetype is the single most impactful section. A well-designed archetype:
- Constrains the AI's behavior more than explicit rules
- Sets the tone and vocabulary naturally
- Reduces the need for negative constraints

**Formula:** `[Domain Expert] who applies [Methodology] and communicates like [Style Reference]`

**Testing:** Ask: "If I described this person at a dinner party, would people immediately understand what they do and how they think?"

### Objective

One sentence. Action verb first. Measurable if possible.

- Good: "Generate conversion-optimized landing page copy that increases click-through rates."
- Bad: "Help users with their marketing needs."

### Parameters

Technical settings that affect behavior:
- **Temperature 0.0-0.3:** Factual, deterministic tasks (data analysis, code, legal)
- **Temperature 0.4-0.7:** Balanced creative-analytical tasks (marketing copy, strategy)
- **Temperature 0.8-1.0:** Highly creative tasks (brainstorming, fiction, ideation)

### Interaction Flow

The state machine of conversation. Design it so the AI always knows what phase it's in and what to do next.

**Phase transitions must be explicit.** Don't rely on the AI to figure out when to move from discovery to execution — give it clear signals.

### Constraints

The difference between a good prompt and a great one is often in the constraints. They should be:
- **Specific:** "Maximum 3 bullet points per section" not "keep it concise"
- **Testable:** You could check compliance programmatically
- **Justified:** If the "why" isn't obvious, include it

**Out-of-scope handling:** Always define what the assistant should do when asked something outside its domain. "I'm designed for X. For Y, I'd recommend [alternative]."

### Key Questions

These are fallback questions — used only when the AI can't infer the answer. Design them to be:
- Specific enough to get actionable answers
- Few enough to not annoy the user (max 5, ideally 3)
- Ordered by criticality (ask the most important first)

### Output Template

The most under-invested section in most prompts. A good output template:
- Shows the exact structure, including heading levels and order
- Uses placeholders that clarify what each section contains
- Matches what the user actually wants to receive

### Self-Correction Triggers

These are the prompt's immune system. They detect when things go wrong and route to recovery actions. Without them, errors compound silently.

---

## Examples

### Minimal Playbook (simple use case)

```markdown
# Email Subject Line Generator — v1.0

## Role & Archetype
Email marketing specialist who applies A/B testing methodology and writes
like David Ogilvy — direct, benefit-focused, every word tested.

## Objective
Generate 5 email subject lines per request that maximize open rates.

## Constraints
- Maximum 50 characters per subject line
- No clickbait or misleading claims
- Include at least one emoji variant and one plain text variant

## Output Template
| # | Subject Line | Characters | Strategy |
|---|-------------|------------|----------|
| 1 | [line] | [count] | [why it works] |
```

### Full Playbook (complex use case)

A complete example for a complex assistant would follow all sections in the template above. For brevity, refer to the scaffold generated by `tools/prompt-scaffolder.py` which produces platform-ready full Playbooks.

---

## Adaptation by Complexity

Not every prompt needs every section. Scale the Playbook to the task:

| Complexity | Sections to Include | Example Use Case |
|-----------|--------------------|--------------------|
| Simple | Role, Objective, Constraints, Output Template | Email generator, code formatter |
| Medium | All above + Interaction Flow, Key Questions | Research assistant, content strategist |
| Complex | Full Playbook | Multi-domain advisor, coaching system, enterprise assistant |

**Rule of thumb:** Start with the full template, then remove sections that add no value for this specific use case. It's easier to subtract than to realize something's missing after deployment.
