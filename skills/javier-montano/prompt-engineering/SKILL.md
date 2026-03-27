---
name: prompt-engineering
author: JM Labs (Javier Montaño)
version: 2.0.0
description: >
  Design, evaluate, and optimize prompts for LLMs. Covers system prompts,
  few-shot patterns, chain-of-thought, structured output, guardrails,
  meta-prompting, and prompt evaluation. Produces Zettelkasten-ready
  knowledge artifacts and branded deliverables.
  Trigger: "prompt engineering", "system prompt", "few-shot", "chain of thought", "prompt design"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
sub-agents:
  - agents/lead.md
  - agents/support.md
  - agents/guardian.md
  - agents/specialist.md
knowledge:
  - knowledge/knowledge-graph.md
  - knowledge/body-of-knowledge.md
templates:
  - templates/output.html
  - templates/output.docx.md
  - templates/output.xlsx.md
---

# Prompt Engineering

> "A prompt is not a question — it is an architecture for reasoning."

## TL;DR

Design, evaluate, and optimize prompts for any LLM. This skill covers
the full lifecycle: understanding the task → selecting the right pattern
(few-shot, CoT, system prompt, meta-prompt) → writing the prompt →
evaluating output quality → iterating. Produces Zettelkasten-ready
knowledge artifacts and branded deliverables (HTML, DOCX, XLSX).

## Sub-Agents

| Agent | Role in Triad | File |
|-------|--------------|------|
| `prompt-lead` | Designs and writes the prompt | `agents/lead.md` |
| `prompt-support` | Reviews for bias, edge cases, injection risk | `agents/support.md` |
| `prompt-guardian` | Evaluates output quality, validates evidence | `agents/guardian.md` |
| `prompt-specialist` | Deep expertise in advanced patterns (meta, constitutional) | `agents/specialist.md` |

## Procedure

### Step 1: Discover
- Identify the task the prompt must accomplish
- Determine the target LLM (Claude, Gemini, GPT, Llama — affects syntax)
- Gather examples of desired input/output pairs
- Read `knowledge/body-of-knowledge.md` for pattern catalog
- Check `knowledge/knowledge-graph.md` for related concepts

### Step 2: Analyze
- Select the prompt pattern:
  - **Zero-shot**: task is well-defined, model has sufficient training data
  - **Few-shot**: task needs examples to calibrate output format/style
  - **Chain-of-thought (CoT)**: task requires multi-step reasoning
  - **System prompt**: task needs persistent behavioral constraints
  - **Meta-prompt**: task is to generate other prompts
  - **Constitutional**: task needs value-aligned, self-correcting output
- Evaluate trade-offs: precision vs cost, latency vs quality, generality vs specificity
- Identify guardrails needed (output format, length, safety)

### Step 3: Execute
- Write the prompt following the selected pattern
- Structure: role → context → task → constraints → output format → examples
- Add guardrails: output schema, safety filters, refusal patterns
- Test with 3+ diverse inputs to verify robustness
- Document the prompt with evidence tags

### Step 4: Validate
- Run evaluation suite: accuracy, consistency, edge case handling
- Check for prompt injection vulnerability
- Verify output format compliance
- Score confidence (>= 0.95 per Constitution)
- Generate deliverable using appropriate template

## Quality Criteria

- [ ] Pattern selection justified with evidence
- [ ] Prompt tested with 3+ diverse inputs
- [ ] Edge cases identified and handled
- [ ] Injection resistance verified
- [ ] Output format consistent across runs
- [ ] Guardrails prevent harmful/off-topic output
- [ ] Evidence tags on all claims
- [ ] Knowledge graph updated with new patterns discovered

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| "Just ask nicely" | No structure = inconsistent results | Use role-context-task-format pattern |
| Massive single prompt | Exceeds attention, dilutes focus | Decompose into chain of focused prompts |
| No examples | Model guesses output format | Add 2-3 few-shot examples |
| Ignoring the model | Claude ≠ GPT ≠ Llama | Adapt syntax to target model |
| No evaluation | "It looks right" isn't evidence | Test with diverse inputs, score metrics |

## Related Skills

- `ai-safety` — Guardrails and output validation
- `structured-output` — JSON mode, schema-constrained generation
- `context-window-management` — Token budgeting for long prompts
- `rag-patterns` — Prompts that integrate retrieved context
- `llm-evaluation` — Systematic prompt evaluation methods

## Knowledge

- `knowledge/knowledge-graph.md` — Zettelkasten concept map
- `knowledge/body-of-knowledge.md` — Pattern catalog and references

## Templates

- `templates/output.html` — Branded HTML prompt documentation
- `templates/output.docx.md` — Word document spec for prompt library
- `templates/output.xlsx.md` — Evaluation matrix spreadsheet
