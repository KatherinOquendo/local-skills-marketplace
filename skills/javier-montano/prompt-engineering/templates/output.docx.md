# DOCX Output Template — Prompt Engineering

## Document Structure (for python-docx generation)

```
Title: "Prompt Library: {{project_name}}"
Subtitle: "Designed with MetodologIA Prompt Engineering"

Section 1: Executive Summary
  - Task description
  - Pattern selected (with justification)
  - Key metrics (accuracy, consistency, token efficiency)

Section 2: Prompt Catalog
  For each prompt:
  - Name, version, pattern type
  - Full prompt text (in code block)
  - Test results (3+ inputs with outputs)
  - Confidence score

Section 3: Evaluation Matrix
  Table: prompt × metric × score

Section 4: Recommendations
  - Improvement opportunities
  - Model-specific adaptations
  - Guardrail enhancements

Footer: "MetodologIA — {{date}}"
```

## Formatting Rules
- Heading 1: Poppins Bold 18pt, Navy #0A122A
- Heading 2: Poppins SemiBold 14pt, Gold #FFD700
- Body: Montserrat Regular 11pt
- Code: JetBrains Mono 10pt, gray background
- Tables: Gold header row, alternating light/dark rows
