---
name: unit-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Write effective unit tests with Jest, Vitest, or Jasmine — including mocking,
  fixtures, snapshot testing, and test organization patterns.
  Trigger: "unit test", "Jest", "Vitest", "mock", "test case"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Unit Testing

> "A unit test should be like a good friend — honest, fast, and always there when you need them." — Unknown

## TL;DR

Guides unit test implementation with Jest, Vitest, or Jasmine — covering test structure, mocking strategies, fixture management, snapshot testing, and test organization patterns. Use when writing or improving unit tests for functions, components, or modules.

## Procedure

### Step 1: Discover
- Check existing test framework and configuration (Jest, Vitest, Jasmine)
- Review test file naming conventions and directory structure
- Identify modules with low or no test coverage
- Check mock/stub patterns currently in use

### Step 2: Analyze
- Determine what to test: pure logic, edge cases, error handling, state transitions
- Plan mocking strategy: dependency injection vs module mocking vs spy
- Evaluate test isolation requirements (each test independent, no shared state)
- Identify test data needs (fixtures, factories, builders)

### Step 3: Execute
- Write tests following AAA pattern: Arrange, Act, Assert
- Use descriptive test names: `it('should return empty array when no items match filter')`
- Mock external dependencies (API calls, database, file system) at boundaries
- Create test fixtures/factories for complex test data
- Add snapshot tests for serializable outputs (use sparingly)
- Group tests with `describe` blocks by feature or method
- Configure coverage reporting with lcov and html reporters

### Step 4: Validate
- Run full test suite — all tests pass in isolation and together
- Check coverage report for untested branches and edge cases
- Verify mocks are reset between tests (no cross-test contamination)
- Confirm tests fail for the right reasons (change code, test breaks meaningfully)

## Quality Criteria

- [ ] Tests follow AAA pattern (Arrange, Act, Assert) with clear structure
- [ ] Each test is independent — no reliance on test execution order
- [ ] Mocks scoped to test level and reset in `beforeEach`/`afterEach`
- [ ] Test names describe expected behavior, not implementation
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Testing implementation details instead of behavior (brittle tests)
- Excessive mocking that makes tests pass regardless of actual behavior
- Sharing mutable state between tests (order-dependent failures)

## Related Skills

- `test-strategy` — unit tests are the base of the test pyramid
- `linting-formatting` — ESLint plugin for test best practices
