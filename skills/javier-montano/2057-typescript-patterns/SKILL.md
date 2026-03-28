---
name: typescript-patterns
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements advanced TypeScript patterns: branded types, generics, utility
  types, discriminated unions, strict mode, module augmentation, and type-safe
  API contracts for robust frontend and backend code. [EXPLICIT]
  Trigger: "TypeScript", "branded types", "generics", "utility types", "strict mode"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# TypeScript Patterns

> "TypeScript is JavaScript that scales." — TypeScript Team

## TL;DR

Implements advanced TypeScript patterns including branded types for domain safety, generics for reusable code, discriminated unions for exhaustive handling, and strict mode enforcement for maximum type safety. Use this skill when designing type-safe APIs, improving codebase type coverage, or when TypeScript types are too loose to catch bugs. [EXPLICIT]

## Procedure

### Step 1: Discover
- Review tsconfig.json: strict mode settings, target, module resolution
- Audit type coverage: any usage, type assertions, missing return types
- Identify pain points: runtime errors that types should have caught
- Check existing type patterns: utility types, generics, branded types in use

### Step 2: Analyze
- Enable strict mode flags: strictNullChecks, noImplicitAny, strictFunctionTypes
- Identify domain concepts that benefit from branded types (UserId vs. string)
- Find opportunities for generics: repeated patterns with different types
- Design discriminated unions for state machines and variant types
- Plan Zod/io-ts integration for runtime validation matching TypeScript types

### Step 3: Execute
- Implement branded types for domain primitives: `type UserId = string & { __brand: 'UserId' }`
- Build generic utilities: `Result<T, E>`, `AsyncState<T>`, `DeepPartial<T>`
- Use discriminated unions with exhaustive switch for state handling
- Create type-safe event emitters and pub/sub with generic event maps
- Implement const assertions and template literal types for API routes
- Set up path aliases in tsconfig for clean imports
- Configure eslint-plugin-typescript for type-aware linting rules

### Step 4: Validate
- Verify strict mode is fully enabled with no escape hatches
- Confirm zero `any` usage (or documented exceptions with eslint-disable)
- Check that generic constraints are tight enough to prevent misuse
- Test that branded types prevent cross-domain value mixing at compile time

## Quality Criteria

- [ ] Strict mode is fully enabled in tsconfig.json
- [ ] Domain primitives use branded types preventing value confusion
- [ ] Discriminated unions have exhaustive handling (never type check)
- [ ] Generic constraints are documented and appropriately tight
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `any` to bypass type errors instead of fixing the types
- Type assertions (`as Type`) to silence the compiler without validation
- Over-engineering types: complex conditional types that nobody can read

## Related Skills

- `angular-development` — TypeScript is the foundation of Angular
- `react-development` — type-safe React components and hooks
- `api-design` — type-safe API contracts with OpenAPI codegen

## Usage

Example invocations:

- "/typescript-patterns" — Run the full typescript patterns workflow
- "typescript patterns on this project" — Apply to current context


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
