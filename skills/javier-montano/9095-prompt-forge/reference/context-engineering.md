# Context Engineering Guide

## Table of Contents

1. [What is Context Engineering](#what-is-context-engineering)
2. [The Three-Layer Model](#the-three-layer-model)
3. [Token Optimization](#token-optimization)
4. [RAG Integration Patterns](#rag-integration-patterns)
5. [Context Decay and Retention](#context-decay-and-retention)
6. [Multi-Turn Management](#multi-turn-management)

---

## What is Context Engineering

Context engineering is the discipline of designing everything the model sees during inference — not just the prompt, but also retrieved documents, conversation history, tool outputs, memory state, and metadata.

A system prompt (the Playbook) is one component of context. A great system prompt with poor context design still underperforms. Context engineering addresses the full input stack.

```
┌─────────────────────────────────────────┐
│              Model Input                 │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │     System Prompt (Playbook)      │   │  ← L1: Hot context
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │     Knowledge Base / RAG          │   │  ← L2: Warm context
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │   Conversation History + Tools    │   │  ← L3: Dynamic context
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │     Current User Message          │   │
│  └──────────────────────────────────┘   │
│                                          │
└─────────────────────────────────────────┘
```

---

## The Three-Layer Model

### L1: Hot Context (System Prompt)

**What:** Always present. Persists across every interaction. Highest influence on behavior.

**Design principles:**
- Keep it lean — every token here is paid on every turn
- Focus on identity (archetype), behavior (constraints), and structure (output template)
- Avoid putting reference data here — that belongs in L2

**Budget:** 2K-5K tokens for most assistants. Over 8K starts degrading performance on some models.

### L2: Warm Context (Knowledge Base)

**What:** Uploaded documents, reference files, style guides, templates. Available but not always loaded into working memory.

**Design principles:**
- One topic per file — models retrieve better from focused documents
- Use descriptive filenames that signal content ("pricing-2024.csv" not "data.csv")
- Include a summary or table of contents at the top of long documents
- Structure with clear headings — models scan for relevant sections

**Budget:** Platform-dependent. Claude Projects supports up to 200K tokens across knowledge files. GPT Custom GPTs use RAG with chunking.

### L3: Dynamic Context (Conversation + Tools)

**What:** User messages, conversation history, tool outputs, API responses. Changes every turn.

**Design principles:**
- Design for context growth — conversations accumulate tokens
- Implement summarization triggers ("After 10 turns, summarize the conversation state")
- Tool outputs should be structured (JSON, tables) for efficient parsing
- Prioritize recent context over distant history for most tasks

---

## Token Optimization

### The Density Principle

Maximum information per token. Every word must earn its place in the context.

**Compression techniques:**

| Technique | Before | After | Savings |
|-----------|--------|-------|---------|
| Remove filler | "In order to achieve the best possible results" | "To achieve best results" | ~50% |
| Merge duplicates | Same constraint stated in two sections | State once, reference from second location | Variable |
| Use tables | Paragraph describing 5 options | 5-row table | ~40% |
| Structured format | Prose explaining rules | Bullet list with condition→action pattern | ~30% |

### The 2x Constraint

No section should be more than 2x the length needed to communicate its content. If you can say it in 50 words, never use 100.

**Testing:** Read each section and ask: "What would I lose if I cut this in half?" If the answer is "nothing important", compress.

### Platform-Specific Token Strategies

**Claude Projects:** Knowledge files are chunked and retrieved on demand. System prompt is always in context. Optimize the system prompt aggressively, be generous with knowledge files.

**Custom GPTs:** Both instructions and uploaded files go through retrieval. Neither is guaranteed to be fully in context. Put the most critical instructions at the top of the instructions field.

**API:** You control everything. Budget explicitly:
```
System: 3K tokens (fixed)
History: 15K tokens (rolling window with summarization)
RAG: 10K tokens (top-5 chunks, ranked by relevance)
Reserved for generation: 4K tokens
Total: ~32K tokens active context
```

---

## RAG Integration Patterns

When the assistant needs access to external knowledge (databases, documents, APIs), RAG provides the bridge. Design patterns:

### Conflict Resolution Hierarchy

When system prompt instructions conflict with retrieved documents:

```
Priority 1: System prompt constraints (never override)
Priority 2: Explicitly cited user preferences
Priority 3: Retrieved document content
Priority 4: Model's training knowledge
```

Build this hierarchy into the prompt:
```markdown
When information from knowledge base files conflicts with your core constraints,
always follow the constraints. If knowledge base information conflicts with the
user's explicit preferences, follow the user's preferences.
```

### Retrieval Quality Patterns

- **Noise pruning:** Instruct the model to ignore irrelevant retrieved chunks: "If a retrieved passage doesn't directly address the user's question, disregard it."
- **Source attribution:** Require the model to cite which document it's drawing from: "When using information from uploaded files, reference the filename."
- **Confidence gating:** "If no retrieved content addresses the question with high confidence, say 'I don't have specific information on this' rather than generating from training data."

---

## Context Decay and Retention

Models have a U-shaped attention curve: they attend strongly to the beginning and end of the context window, with weaker attention in the middle.

### Implications for Prompt Design

- **Critical instructions:** Place at the very beginning (system prompt) and reinforce at the end of the prompt
- **Reference material:** Place in the middle — it will be retrieved when relevant but won't dominate behavior
- **Recent conversation:** Has natural high attention due to recency

### Retention Strategies

```
Long conversations (10+ turns):
├── Insert periodic state summaries
├── Re-inject key constraints every 5-7 turns
├── Use structured markers ("CURRENT STATE: ...")
└── Design exit conditions to prevent endless conversations

Knowledge-heavy sessions:
├── Chunk documents into focused sections
├── Use descriptive section headers for navigation
├── Rank retrieved chunks by relevance before injection
└── Limit to top-5 most relevant chunks per query
```

### Session Management

For assistants that handle long sessions:

```markdown
## Session Management
- After 8 turns, provide a brief summary: "So far we've [summary]. What's next?"
- After 15 turns, offer a fresh start: "We've covered a lot. Want to start a
  focused session on a specific topic?"
- Never let a session exceed 20 turns without a checkpoint
```

---

## Multi-Turn Management

### State Tracking Pattern

For assistants that need to remember decisions across turns:

```markdown
After each phase, internally track:
- Decisions made: [list of confirmed choices]
- Open questions: [unresolved items]
- Current phase: [Discovery/Execution/Delivery]
- Iteration count: [N of max 3]
```

### Handoff Pattern

For assistants that produce deliverables iteratively:

```markdown
When delivering output, always end with:
1. Summary of what was produced
2. Key decisions made (and alternatives not chosen)
3. One specific question for the next iteration
```

### Context Recovery Pattern

For when conversation context is lost (new session, context overflow):

```markdown
If the user seems to reference a previous conversation or context you
don't have:
1. Acknowledge: "I don't have context from our previous conversation"
2. Ask for key inputs: "Could you share [the specific thing needed]?"
3. Never fabricate continuity from a conversation you don't remember
```
