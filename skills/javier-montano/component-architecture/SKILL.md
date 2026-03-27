---
name: component-architecture
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Designs frontend module boundaries, interface contracts, and composition
  patterns for scalable component hierarchies. Covers smart/dumb patterns,
  compound components, and dependency injection.
  Trigger: "component architecture", "module boundary", "composition pattern", "interface contract"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Component Architecture

> "Composition over inheritance." — Gang of Four

## TL;DR

Designs scalable frontend component hierarchies with clear module boundaries, interface contracts, and composition patterns that promote reusability and testability. Use this skill when building component libraries, structuring large frontend applications, or when component coupling is causing maintenance issues.

## Procedure

### Step 1: Discover
- Audit existing component structure and identify coupling issues
- Map component categories: layout, navigation, data display, forms, feedback
- Identify shared components vs. feature-specific components
- Review existing design system tokens and patterns

### Step 2: Analyze
- Apply smart/dumb (container/presentational) separation
- Identify compound component opportunities (components that work together as a unit)
- Design interface contracts: required props, optional props, render props, slots
- Plan component composition strategy: HOCs, render props, hooks, or slots

### Step 3: Execute
- Define module boundaries with clear public APIs (barrel exports)
- Create component interface contracts with TypeScript props interfaces
- Implement compound component patterns for complex interactive elements
- Design a folder structure that reflects component hierarchy and ownership
- Document component usage examples with props variations
- Establish naming conventions: PascalCase, prefix conventions, file organization

### Step 4: Validate
- Verify components have single responsibility (one reason to change)
- Confirm interface contracts are minimal — no unnecessary props
- Check that smart components don't contain presentational logic
- Validate components are testable in isolation without heavy mocking

## Quality Criteria

- [ ] Components follow single responsibility principle
- [ ] Interface contracts are typed and documented with examples
- [ ] Smart/dumb separation is consistently applied
- [ ] Module boundaries have explicit public APIs via barrel exports
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- God component: one component handling display, state, and business logic
- Prop drilling through 5+ levels instead of using context or state management
- Tightly coupled components that cannot be tested or used independently

## Related Skills

- `design-system` — design tokens consumed by components
- `state-management` — state boundaries align with component architecture
- `responsive-design` — components adapt to viewport using architecture patterns
