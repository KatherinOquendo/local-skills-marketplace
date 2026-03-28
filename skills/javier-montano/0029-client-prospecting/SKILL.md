---
name: client-prospecting
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  AI-driven client prospecting by geography and sector. Research targets, score by fit, generate outreach strategy. Output: branded HTML report. [EXPLICIT]
  Trigger: "prospect clients", "find leads", "outreach", "target geography", "Miami", "Orlando"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Client Prospecting

> "Method over hacks. Evidence over assumption."

## TL;DR

AI-driven client prospecting by geography and sector. Research targets, score by fit, generate outreach strategy. Output: branded HTML report. All HTML outputs use the MetodologIA brand design system (references/brand/design-tokens.json + html-template.html). [EXPLICIT]

## Procedure

### Step 1: Discover
- Gather requirements from user input
- Read existing context and reference materials
- Load brand design tokens from references/brand/design-tokens.json

### Step 2: Analyze
- Structure the content sections
- Identify data sources (web search, provided docs, codebase)
- Plan the output format (HTML using brand template)

### Step 3: Execute
- Research and gather content
- Structure into the brand HTML template (references/brand/html-template.html)
- Apply design tokens: navy background, gold accents, Poppins/Montserrat, glassmorphism
- Replace template variables: {{TITLE}}, {{SUBTITLE}}, {{CONTENT}}, {{DATE}}

### Step 4: Validate
- HTML renders correctly with brand aesthetic
- Content is accurate and evidence-tagged
- No raw hex colors (all via CSS variables)
- Print-friendly layout works
- Evidence tags applied to all claims

## Quality Criteria

- [ ] Uses MetodologIA brand template (navy + gold + glassmorphism)
- [ ] All content evidence-tagged
- [ ] Print-friendly
- [ ] No raw hex colors — uses CSS variables
- [ ] Poppins headings, Montserrat body, JetBrains Mono code

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Raw hex colors in HTML | Breaks brand consistency | Use CSS variables from design-tokens.json |
| Generic white background | Not MetodologIA aesthetic | Navy (#0A122A) background always |
| Missing evidence tags | Claims without basis | Tag every claim |

## Related Skills

- branded-html-output — Base skill for all HTML generation
- guardrails-management — Check user guardrails before generating

## Usage

Example invocations:

- "/client-prospecting" — Run the full client prospecting workflow
- "client prospecting on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
