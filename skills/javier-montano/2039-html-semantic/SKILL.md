---
name: html-semantic
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements semantic HTML5 with proper document structure, landmark elements,
  forms, tables, multimedia, and SEO-friendly markup. Ensures content is
  meaningful, accessible, and machine-readable. [EXPLICIT]
  Trigger: "semantic HTML", "HTML5", "forms", "tables", "landmarks", "markup"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# HTML Semantic

> "HTML is the skeleton. CSS is the skin. JavaScript is the muscle." — Unknown

## TL;DR

Implements semantic HTML5 using proper document structure, landmark elements, accessible forms and tables, and multimedia markup that is meaningful to browsers, assistive technologies, and search engines. Use this skill when building new pages, auditing markup quality, or when div-soup needs to be replaced with meaningful structure. [EXPLICIT]

## Procedure

### Step 1: Discover
- Audit existing HTML for semantic quality: are divs used where landmarks should be?
- Review content hierarchy: is the heading structure logical (h1 → h2 → h3)?
- Check form markup: labels, fieldsets, input types, validation attributes
- Identify multimedia content needing proper elements (video, audio, figure)

### Step 2: Analyze
- Map content to semantic elements: header, nav, main, aside, footer, article, section
- Design heading hierarchy reflecting content outline
- Plan form structure with proper grouping (fieldset/legend) and input types
- Identify table data vs. layout misuse
- Assess microdata/structured data opportunities

### Step 3: Execute
- Replace div-based layouts with semantic landmarks (header, nav, main, footer)
- Structure headings in proper hierarchy (one h1, logical nesting)
- Build forms with: label associations, fieldset grouping, native validation attributes
- Implement responsive images: picture, source, srcset, sizes
- Use proper list markup: ul/ol for lists, dl for key-value pairs
- Add meta elements: charset, viewport, description, Open Graph

### Step 4: Validate
- Run HTML validation (W3C validator) — zero errors
- Verify heading outline is logical using a heading structure checker
- Check all form inputs have associated labels (htmlFor or wrapping)
- Validate landmark structure with accessibility audit tools

## Quality Criteria

- [ ] Document uses semantic landmarks (header, nav, main, aside, footer)
- [ ] Heading hierarchy is logical without skipping levels
- [ ] Forms use proper labels, fieldsets, and native validation
- [ ] Images have appropriate alt text (meaningful or empty for decorative)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Div soup: using divs for everything instead of semantic elements
- Heading abuse: using headings for visual sizing instead of structure
- Placeholder-as-label: using placeholder attribute instead of proper label elements

## Related Skills

- `accessibility-design` — semantic HTML is the foundation of accessibility
- `seo-architecture` — semantic markup improves search engine understanding
- `form-engineering` — detailed form implementation patterns

## Usage

Example invocations:

- "/html-semantic" — Run the full html semantic workflow
- "html semantic on this project" — Apply to current context


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
