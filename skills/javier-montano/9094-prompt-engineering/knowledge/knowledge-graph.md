# Prompt Engineering — Knowledge Graph

<!-- Zettelkasten-ready: use [[wikilinks]] for Obsidian compatibility -->

## Core Concepts

- [[prompt-pattern]] — A reusable structure for prompting LLMs
- [[zero-shot]] — No examples, relies on model's training
- [[few-shot]] — 2-5 examples calibrate output format and style
- [[chain-of-thought]] — "Think step by step" decomposition
- [[system-prompt]] — Persistent behavioral constraints
- [[meta-prompt]] — Prompt that generates prompts
- [[constitutional-ai]] — Self-correcting with value alignment

## Relationships

```
prompt-pattern
├── zero-shot (simplest, when task is well-defined)
├── few-shot (adds examples for calibration)
│   └── depends-on: example-quality
├── chain-of-thought (multi-step reasoning)
│   ├── variant: zero-shot-cot ("think step by step")
│   └── variant: few-shot-cot (examples with reasoning)
├── system-prompt (persistent constraints)
│   ├── composes-with: few-shot
│   └── composes-with: chain-of-thought
├── meta-prompt (generates prompts)
│   └── requires: prompt-evaluation
└── constitutional-ai (self-correction)
    └── requires: value-criteria
```

## Tags

#prompt-engineering #llm #ai #patterns #zettelkasten

## Cross-References

- [[rag-patterns]] — Prompts that integrate retrieved context
- [[structured-output]] — Schema-constrained prompt output
- [[ai-safety]] — Guardrails and injection prevention
- [[context-window-management]] — Token budgeting for prompts
- [[llm-evaluation]] — Measuring prompt effectiveness

## Decision Heuristics

| If... | Then use... | Because... |
|-------|------------|-----------|
| Task is well-defined, model knows the domain | Zero-shot | Simplest, lowest cost |
| Output format matters but task is clear | Few-shot (2-3 examples) | Examples calibrate format |
| Task requires reasoning or math | Chain-of-thought | Decomposition improves accuracy |
| Agent needs persistent behavior | System prompt | Constraints survive across turns |
| Need to generate prompts at scale | Meta-prompt | One prompt generates many |
| Output must align with values | Constitutional | Self-correction loop |
