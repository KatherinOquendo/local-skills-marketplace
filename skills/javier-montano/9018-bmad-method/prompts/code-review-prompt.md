# Code Review

## Pre-conditions

- Story status is IN-REVIEW in sprint-status.yaml
- All tests pass (developer has confirmed via self-review)
- The code diff is available (feature branch vs. main)
- The story file with acceptance criteria is accessible

## Post-conditions

- Review report exists with APPROVED, CHANGES-REQUESTED, or BLOCKED result
- Every acceptance criterion is individually verified with evidence
- sprint-status.yaml is updated (DONE if APPROVED, remains IN-REVIEW if CHANGES-REQUESTED)
- No CRITICAL findings remain unresolved

## Failure Signals

- Tests are failing when Quinn starts the review (developer skipped self-review)
- Acceptance criteria cannot be traced to specific tests
- Multiple CRITICAL findings indicate architectural issues (escalate to Winston)
- Story repeatedly fails review (> 2 cycles indicates story needs re-scoping)

## Purpose

This prompt triggers a structured code review for a completed story. Use it after a developer marks a story as ready for review (IN-REVIEW status).

## Setup Instructions

1. **Activate Quinn (QA)**: Load `agents/quinn-qa.md`.

2. **Load review context**:
   - The story file — for acceptance criteria
   - The code diff — all changes made for this story
   - `project-context.md` — for coding conventions and quality standards
   - `architecture.md` — for architectural patterns and design decisions

## Review Process

### Step 1: Acceptance Criteria Verification

For each acceptance criterion in the story:

| # | Criterion | Test Covering It | Verified? | Notes |
|---|-----------|-----------------|-----------|-------|
| 1 | [criterion text] | [test name/file] | YES/NO | [notes] |

- Every criterion must have at least one test.
- The test must actually validate the criterion (not just share a similar name).
- Check edge cases: does the test cover boundary conditions, empty input, error paths?

### Step 2: Code Quality Check

Against `project-context.md` conventions:

- [ ] **Naming**: Variables, functions, classes follow project naming conventions
- [ ] **Structure**: Code is organized consistently with existing patterns
- [ ] **Error handling**: Errors are caught, logged, and handled gracefully (not swallowed)
- [ ] **Logging**: Appropriate log statements at correct levels (debug, info, error)
- [ ] **Comments**: Complex logic has explanatory comments; no redundant comments
- [ ] **Dead code**: No commented-out code blocks or unused imports
- [ ] **DRY**: No unnecessary duplication; shared logic is extracted
- [ ] **Single responsibility**: Functions and classes have focused purposes

### Step 3: Test Quality Review

- [ ] **Test names are descriptive**: Each test name explains what it verifies
- [ ] **Tests are independent**: No shared mutable state between tests
- [ ] **Positive cases covered**: Happy path is tested
- [ ] **Negative cases covered**: Invalid input, unauthorized access, missing data
- [ ] **Edge cases covered**: Boundary values, empty collections, null/undefined
- [ ] **Test data is realistic**: Not just "test" or "foo" values

### Step 4: Security Review

- [ ] **No hardcoded secrets**: No API keys, passwords, or tokens in code
- [ ] **Input validation**: User input is validated before processing
- [ ] **SQL injection protection**: Parameterized queries used (if applicable)
- [ ] **XSS protection**: Output is sanitized (if applicable)
- [ ] **Auth enforcement**: Protected routes check authentication and authorization
- [ ] **Sensitive data handling**: PII is not logged; encryption used where needed

### Step 5: Performance Review

- [ ] **No N+1 queries**: Database queries inside loops are flagged
- [ ] **Pagination**: Large data sets use pagination, not full loads
- [ ] **Async operations**: Long-running tasks are not blocking the main thread
- [ ] **Caching**: Frequently accessed, rarely changing data uses caching (if applicable)
- [ ] **Resource cleanup**: Connections, file handles, streams are properly closed

## Review Report Format

```
# Code Review: [Story ID] — [Story Title]

## Result: [APPROVED / CHANGES-REQUESTED / BLOCKED]

## Acceptance Criteria Verification
[Table from Step 1]

## Findings

### Critical (must fix)
- [finding with file:line reference]

### Major (should fix)
- [finding with file:line reference]

### Minor (consider fixing)
- [finding with file:line reference]

### Suggestions (optional improvements)
- [suggestion]

## Summary
[1-2 sentence overall assessment]
```

## Post-Review Actions

- **APPROVED**: Update sprint-status.yaml to DONE. No further action needed.
- **CHANGES-REQUESTED**: Return to developer with specific findings. After fixes, re-review only the changed items.
- **BLOCKED**: Escalate to user. Typically for architectural issues or security concerns that require design changes.
