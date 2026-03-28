# Domain Knowledge — prompt forge

## Overview

This reference provides foundational knowledge for the prompt forge skill. [EXPLICIT]

## Key Concepts

| Concept | Definition | Relevance |
|---------|-----------|-----------|
| Primary domain | The core domain that prompt forge operates within | Direct input to skill execution [EXPLICIT] |
| Quality criteria | Standards that output must meet | Validation gate alignment [EXPLICIT] |
| Evidence taxonomy | [EXPLICIT]/[INFERRED]/[OPEN] classification | Required for all factual claims [EXPLICIT] |

## Best Practices

1. Always start with evidence gathering before analysis [EXPLICIT]
2. Tag every factual claim with appropriate evidence marker [EXPLICIT]
3. Separate observations from inferences explicitly [EXPLICIT]
4. Document assumptions that could invalidate conclusions [EXPLICIT]
5. Provide actionable recommendations with priority levels [EXPLICIT]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|-------------|-------------|-------------------|
| Untaged claims | Readers cannot assess confidence | Tag with [EXPLICIT]/[INFERRED]/[OPEN] |
| Generic output | Fails to address specific context | Adapt to project-specific inputs |
| Missing edge cases | Breaks on non-standard inputs | Document handling for edge scenarios |

## Integration Points

- This skill may be invoked by orchestrator skills in the pipeline [EXPLICIT]
- Output format follows MetodologIA markdown conventions [EXPLICIT]
- Evidence tags enable downstream quality validation [EXPLICIT]
