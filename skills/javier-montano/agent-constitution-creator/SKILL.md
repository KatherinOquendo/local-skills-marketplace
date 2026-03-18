---
name: agent-constitution-creator
description: Generate constitutional agent.md documents with 22 mandatory fields for agentic ecosystems.
argument-hint: <agent-id> [role-description]
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Agent Constitution Creator

Generate constitutional `agent.md` documents — the persistent system prompt and operational identity for agents in any multi-agent ecosystem. Each constitution defines 22 fields covering identity, scope, security, delegation, meta-cognition, and completion criteria.

> **Scope**: This creates comprehensive agent constitutions for agentic frameworks (multi-agent systems, tool-calling architectures). For lightweight Claude Code subagent definitions, use `/agent-creator`.

## Assumptions & Limits

- **Assumes** a multi-agent ecosystem exists or is being designed (single-agent systems don't need constitutions)
- **Assumes** the ecosystem has shared concepts: tool registry, security checkpoints, delegation patterns
- **Limit**: Constitutions are static documents — they don't enforce behavior at runtime (enforcement is the orchestrator's job)
- **Trade-off**: More specific constitutions = less agent autonomy but more predictable behavior. More general = flexible but prone to scope creep.

## Usage

```
/agent-constitution-creator data-analyst "Transforms raw data into structured insights"
/agent-constitution-creator onboarding-agent   # interview mode
```

Parse `$1` as agent ID (kebab-case), `$2` as role. If `$2` absent, ask:
1. What is this agent's primary responsibility?
2. What other agents exist in the ecosystem? (for delegation/escalation context)
3. What tools should it have access to?

## Before Generating

1. **Read ecosystem context**: `Glob agents/*/agent.md` — understand existing agents, their roles, and boundaries
2. **Check for overlap**: If another agent's scope overlaps >30%, consider merging or adding explicit boundary delineation
3. **Read tool registry**: Identify available tools for the Allowed Tools section
4. **Read security spec**: If the ecosystem has security checkpoints, load them

## The 21 Fields

Organized in 4 categories for coherence:

### Identity (3 fields)
| # | Field | Purpose | Quality Bar |
|---|---|---|---|
| 1 | Mission | Reason for existing | Specific to THIS agent; 1-2 sentences; includes measurable outcome |
| 2 | Mandate | What it MUST do | Concrete, verifiable actions (not aspirational) |
| 3 | Scope | Operational boundaries | Clear in/out list; no grey areas |

### Authority (6 fields)
| # | Field | Purpose | Quality Bar |
|---|---|---|---|
| 4 | Non-Goals | Explicit exclusions | ≥3 items users might wrongly expect |
| 5 | Inputs | Data it receives | Typed: `{name}: {type} — {description}` |
| 6 | Outputs | What it produces | Format specified: JSON, Markdown, file path |
| 7 | Decision Rights | Autonomous decisions | Clear boundary: "can X without approval; must escalate Y" |
| 8 | Allowed Tools | Authorized tools | Specific names from registry; no wildcards |
| 9 | Forbidden Tools | Prohibited tools | Explicit denials prevent scope creep |

### Governance (6 fields)
| # | Field | Purpose | Quality Bar |
|---|---|---|---|
| 10 | Memory Policy | Read/write rules | Keys, formats, retention periods, size limits |
| 11 | Security Policy | Security controls | References specific checkpoints (CP1/input, CP2/prompt, CP3/output) |
| 12 | Orchestration Policy | Multi-agent participation | Role in delegation chains: initiator, delegate, observer |
| 13 | Delegation Rules | When/how to delegate | Criteria for single-agent, panel (terna), committee modes |
| 14 | Escalation Rules | When to escalate | Triggers, target agent/human, context to include |
| 15 | Tone / Output Style | Communication style | Language, formality, formatting conventions |

### Quality (7 fields)
| # | Field | Purpose | Quality Bar |
|---|---|---|---|
| 16 | Validation Discipline | Output verification | Method: self-check, peer review, automated test |
| 17 | Meta-Cognition Protocol | Reasoning discipline | FULL (triad: 3 patterns + confidence + bias scan) or LIGHT (decompose + evidence-check + bias scan) |
| 18 | Failure Handling | Error recovery | Per-failure-mode: detection → response → fallback |
| 19 | Completion Criteria | Done definition | Verifiable assertions, not "task is done" |
| 20 | KPIs | Performance metrics | ≥3 metrics with targets and units |
| 21 | Dependencies | Required services | Other agents, APIs, data sources needed |
| 22 | Version | Document version | Semver; change log in commit or footer |

## Output Template

Write to `agents/{id}/agent.md`:

```markdown
---
id: "{id}"
name: "{name}"
role: "{role}"
version: "1.0.0"
---

# Mission
{1-2 sentences with measurable outcome}

# Mandate
- {Concrete action 1}
- {Concrete action 2}

# Scope
**In scope:**
- {boundary 1}

**Out of scope:**
- {boundary 1} → {responsible agent}

# Non-Goals
- {Exclusion 1} (→ {who handles it instead})
- {Exclusion 2}
- {Exclusion 3}

# Inputs
- `{inputName}`: {type} — {description}

# Outputs
- `{outputName}`: {format} — {description}

# Decision Rights
**Autonomous:** {decisions this agent makes alone}
**Requires approval:** {decisions needing human or lead-agent sign-off}

# Allowed Tools
- `{tool_name}` — {why this agent needs it}

# Forbidden Tools
- `{tool_name}` — {why it's forbidden}

# Memory Policy
- **Reads:** `{key}` — {purpose}
- **Writes:** `{key}` — {what, when, retention}
- **Size limit:** {max per entry}

# Security Policy
- **CP1 (Input):** {sanitization rules}
- **CP2 (Prompt):** {hardening rules}
- **CP3 (Output):** {validation rules}

# Orchestration Policy
{Role in delegation: initiator | delegate | both. How it participates in chains.}

# Delegation Rules
- **Single:** {when to delegate to one agent}
- **Panel:** {when to use 3-agent panel}
- **Committee:** {when to convene full committee}

# Escalation Rules
- **Trigger:** {condition}
- **Target:** {agent-id or human role}
- **Context:** {what to include in escalation}

# Tone / Output Style
{Language, formality, format preferences}

# Validation Discipline
{Method and criteria for self-validation before delivery}

# Meta-Cognition Protocol
{FULL for triad/orchestrator agents, LIGHT for all others}

**LIGHT (default):**
1. Decompose — max 5 sub-problems before solving
2. Evidence-check — tag claims with confidence [CONFIANZA: alta|media|baja]
3. Bias scan — check anchoring, confirmation, availability
4. Structure-first — bullet skeleton before prose
5. Escalate — when confidence is baja, flag and present alternatives

**FULL (triad only):** adds Structured Reasoning, Skeleton-of-Thought, Chain-of-Code patterns + 0.0–1.0 confidence scoring

# Failure Handling
| Failure Mode | Detection | Response | Fallback |
|---|---|---|---|
| {mode 1} | {signal} | {action} | {alternative} |

# Completion Criteria
- [ ] {Verifiable assertion 1}
- [ ] {Verifiable assertion 2}

# KPIs
| Metric | Target | Unit |
|---|---|---|
| {metric 1} | {value} | {unit} |

# Dependencies
- `{agent-id}` — {what for}
- `{service}` — {what for}
```

## Example: Good vs Bad

**Bad Mission:** "This agent helps with data tasks."
**Good Mission:** "Transform raw CSV/JSON datasets into validated, typed schemas with anomaly detection, producing structured analysis within 60 seconds per 10K rows."

**Bad Non-Goals:** "Doesn't do other things."
**Good Non-Goals:**
- Does NOT handle real-time streaming data (→ `stream-processor` agent)
- Does NOT perform ML model training (→ `ml-trainer` agent)
- Does NOT make business decisions from data (→ escalate to human analyst)

**Bad Failure Handling:** "Handle errors appropriately."
**Good Failure Handling:**

| Mode | Detection | Response | Fallback |
|---|---|---|---|
| Malformed input | Schema validation fails | Log error, return structured error message | Ask user to provide sample row |
| Tool unavailable | Tool call timeout > 30s | Retry once, then escalate | Use alternative tool or manual approach |
| Conflicting data | >5% rows with contradictory values | Flag conflicts, proceed with majority value | Escalate to human with conflict report |

## Validation Gate

- [ ] All 22 fields present and non-empty
- [ ] Mission is specific to THIS agent (not reusable for any agent)
- [ ] Mission includes a measurable outcome
- [ ] Non-Goals has ≥3 items with responsible alternative agent/human named
- [ ] Allowed Tools lists specific names (no wildcards)
- [ ] Security Policy references specific checkpoints with rules
- [ ] Delegation Rules specify criteria for each mode
- [ ] Failure Handling has ≥3 failure modes with detection→response→fallback
- [ ] Completion Criteria are verifiable assertions (testable, not subjective)
- [ ] KPIs include ≥3 metrics with units
- [ ] No two agents in the ecosystem have overlapping Scope

---
**Autor:** Javier Montaño | **Última actualización:** 12 de marzo de 2026
