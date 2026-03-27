---
name: vanilla-javascript
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements solutions using vanilla JavaScript: DOM manipulation, event
  handling, Fetch API, ES modules, Web APIs, and modern ECMAScript features
  without framework dependencies.
  Trigger: "vanilla JS", "DOM manipulation", "Fetch API", "ES modules", "plain JavaScript"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Vanilla JavaScript

> "Any application that can be written in JavaScript, will eventually be written in JavaScript." — Jeff Atwood (Atwood's Law)

## TL;DR

Implements robust solutions using vanilla JavaScript with modern DOM APIs, event delegation, Fetch API, ES modules, and Web APIs without relying on framework abstractions. Use this skill when building lightweight widgets, enhancing server-rendered pages, learning fundamentals, or when a framework is overkill.

## Procedure

### Step 1: Discover
- Identify the feature requirements and browser support targets
- Check if a framework is already in use (vanilla JS may not be the right choice then)
- Review existing vanilla JS patterns in the codebase for consistency
- Inventory Web APIs available for the target browsers

### Step 2: Analyze
- Plan DOM interaction strategy: querySelector, event delegation, MutationObserver
- Design module structure using ES modules (import/export)
- Choose data fetching approach: Fetch API with async/await, AbortController for cancellation
- Evaluate Web API opportunities: Intersection Observer, ResizeObserver, Web Storage
- Plan error handling and graceful degradation strategy

### Step 3: Execute
- Implement with modern ECMAScript: destructuring, spread, optional chaining, nullish coalescing
- Use event delegation on parent elements instead of per-element listeners
- Implement Fetch API calls with proper error handling, timeout, and retry
- Organize code as ES modules with clear import/export boundaries
- Use template literals for dynamic HTML generation (sanitize user input!)
- Implement custom events for component communication without coupling

### Step 4: Validate
- Verify no memory leaks: event listeners removed, observers disconnected
- Confirm XSS prevention: user input is sanitized before DOM insertion
- Test error handling for network failures and API errors
- Check module loading works with the target build system or native ESM

## Quality Criteria

- [ ] Event delegation used instead of per-element listeners where appropriate
- [ ] Fetch calls handle errors, timeouts, and cancellation
- [ ] User input is sanitized before DOM insertion (XSS prevention)
- [ ] Code is organized as ES modules with clear boundaries
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- innerHTML with unsanitized user input (XSS vulnerability)
- Adding event listeners in loops without delegation
- Synchronous XMLHttpRequest blocking the main thread

## Related Skills

- `typescript-patterns` — type-safe JavaScript with TypeScript
- `html-semantic` — proper HTML structure for DOM manipulation targets
- `css-animation` — JavaScript-triggered CSS animations
