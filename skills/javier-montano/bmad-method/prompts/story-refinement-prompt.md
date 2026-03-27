# Story Refinement / Grooming

## Pre-conditions

- The story file exists with at minimum: title, description, and parent epic reference
- `architecture.md` is available for technical context
- `PRD.md` is available for the parent FR and its acceptance criteria

## Post-conditions

- Story passes all INVEST criteria checks
- Acceptance criteria are in Given/When/Then format and independently testable
- Estimation is assigned (S/M/L)
- Story metadata is marked as REFINED
- Technical notes reference specific architecture components

## Failure Signals

- Story cannot be estimated (too many unknowns — create a spike instead)
- Story fails the "Small" criterion and cannot be split (scope is inherently coupled)
- Acceptance criteria contain ambiguous terms ("fast", "user-friendly", "properly")
- No test can be written for one or more acceptance criteria

## Purpose

This prompt guides the refinement of a user story to ensure it is ready for implementation. Use it during sprint planning when a story needs grooming, or before any story enters active development.

## Setup Instructions

1. **Load the story file**: Read the complete story including title, description, acceptance criteria, estimation, and dependencies.

2. **Load supporting context**:
   - `architecture.md` — for technical design relevant to this story
   - `PRD.md` — for the parent FR and its acceptance criteria
   - `project-context.md` — for coding conventions and patterns

## INVEST Criteria Check

Evaluate the story against each INVEST criterion:

### Independent
- Can this story be implemented without waiting for other in-progress stories?
- If it has dependencies, are they already DONE or scheduled before this story?
- **If NOT independent**: Identify the blocking dependency. Either resolve it or resequence.

### Negotiable
- Is the story written at the right level of abstraction (not over-specified)?
- Can the developer choose the implementation approach?
- **If over-specified**: Remove implementation details from the story; keep only the WHAT, not the HOW.

### Valuable
- Does this story deliver value to a user or to the system on its own?
- Can a stakeholder understand why this story matters?
- **If not valuable alone**: Consider merging with another story or reframing.

### Estimable
- Is there enough information to estimate the effort?
- Are unknowns identified and bounded?
- **If not estimable**: Identify what information is missing. Create a spike if needed.

### Small
- Can this story be completed within a single sprint?
- Is the estimation S (< 2h) or M (2-4h)? If L (4-8h), can it be split?
- **If too large**: Split along natural seams — by user action, by data entity, by layer (API + UI separately).

### Testable
- Can every acceptance criterion be verified with an automated test?
- Are criteria written in a way that has clear pass/fail determination?
- **If not testable**: Rewrite acceptance criteria using Given/When/Then or explicit checklist format.

## Acceptance Criteria Review

For each acceptance criterion:

1. **Is it specific?** — No ambiguous terms ("fast", "user-friendly", "properly").
2. **Is it verifiable?** — A test can be written that passes or fails definitively.
3. **Does it cover edge cases?** — What about empty input, null values, unauthorized access, max-length data?
4. **Is the happy path covered?** — The primary use case must be explicitly stated.
5. **Are error cases covered?** — What happens when things go wrong?

## Technical Detail Check

Verify the story has sufficient technical context:

- [ ] Related architecture components are identified
- [ ] Data model changes (if any) are documented
- [ ] API endpoints (if any) are referenced
- [ ] External dependencies are noted
- [ ] Security considerations are flagged (auth, input validation)
- [ ] Performance implications are noted (if relevant)

## Estimation Validation

Review the estimation:
- **S (< 2h)**: Simple change, clear path, existing patterns to follow.
- **M (2-4h)**: Moderate complexity, some new patterns, or multiple files.
- **L (4-8h)**: Consider splitting. If the estimation is L, explicitly document why it cannot be split.

## Output

After refinement, update the story file with:
- Revised acceptance criteria (if changed)
- Updated estimation (if changed)
- Added technical notes (if missing)
- Resolved dependency information
- Mark the story as REFINED in its metadata
