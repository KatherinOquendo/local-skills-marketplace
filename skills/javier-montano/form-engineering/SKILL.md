---
name: form-engineering
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements robust web forms with client and server validation, multi-step
  wizards, file upload handling, accessible error messaging, and optimistic
  submission patterns.
  Trigger: "form validation", "multi-step form", "file upload", "form engineering", "wizard"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Form Engineering

> "Forms are the gatekeepers of the web. Make them inviting, not intimidating." — Luke Wroblewski

## TL;DR

Implements robust web forms with layered validation (HTML5, client-side, server-side), multi-step wizards, file upload handling, and accessible error messaging for friction-free data capture. Use this skill when building complex forms, improving form conversion rates, or when form validation is inconsistent across the application.

## Procedure

### Step 1: Discover
- Identify form requirements: fields, validation rules, submission endpoint
- Review existing form patterns in the codebase for consistency
- Gather UX requirements: inline validation timing, error message placement
- Check accessibility: labels, error associations, keyboard navigation

### Step 2: Analyze
- Design validation layers:
  1. **HTML5 native**: required, type, pattern, min/max attributes
  2. **Client-side**: real-time validation with debounced feedback
  3. **Server-side**: authoritative validation (never trust client only)
- Plan multi-step form flow: step sequence, data persistence, back/forward navigation
- Design file upload: accepted types, size limits, progress feedback, preview
- Plan error handling: field-level errors, form-level errors, server errors

### Step 3: Execute
- Build forms with proper HTML: label, fieldset/legend, input types, autocomplete attributes
- Implement real-time validation with meaningful error messages (not just "invalid")
- Create multi-step wizard with progress indicator and state preservation
- Implement file upload with drag-and-drop, preview, progress bar, and retry
- Set up optimistic submission: disable button, show loading, handle success/error
- Associate errors with inputs using aria-describedby and aria-invalid
- Implement autosave for long forms to prevent data loss

### Step 4: Validate
- Verify all inputs have associated labels and error message connections
- Confirm server-side validation catches everything client-side does (and more)
- Test keyboard-only form completion (Tab, Enter, Escape)
- Check that error messages are specific and actionable ("Email must include @")

## Quality Criteria

- [ ] Every input has a visible label and accessible error association
- [ ] Validation runs on both client and server with consistent rules
- [ ] Error messages are specific, actionable, and politely worded
- [ ] Multi-step forms preserve state on back navigation
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Client-only validation without server-side verification
- Generic error messages ("Invalid input") that don't help users fix the issue
- Clearing the entire form on submission error, losing user input

## Related Skills

- `accessibility-design` — accessible form patterns and error handling
- `html-semantic` — proper form markup and native validation
- `angular-development` — Angular reactive forms implementation
