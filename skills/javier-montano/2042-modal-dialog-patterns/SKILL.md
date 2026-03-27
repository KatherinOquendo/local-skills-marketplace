---
name: modal-dialog-patterns
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implement accessible modal and dialog patterns using the HTML dialog element,
  focus trapping, keyboard navigation, and ARIA attributes.
  Trigger: "modal", "dialog", "popup", "focus trap", "overlay"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Modal & Dialog Patterns

> "A modal should earn its interruption — not every message deserves to stop the world." — Unknown

## TL;DR

Guides the implementation of accessible modal dialogs using the native `<dialog>` element with proper focus management, keyboard interaction, scroll locking, and ARIA semantics. Use when building confirmation dialogs, forms in overlays, lightboxes, or any content that requires user attention before proceeding.

## Procedure

### Step 1: Discover
- Identify dialog use cases (confirmation, form, info, alert, image lightbox)
- Check if native `<dialog>` element is viable or if a polyfill is needed
- Review existing modal implementations for accessibility gaps
- Determine if dialogs are modal (blocks background) or non-modal (coexists)

### Step 2: Analyze
- Choose between modal (`showModal()`) and non-modal (`show()`) dialog behavior
- Plan focus management: where focus goes on open, where it returns on close
- Design keyboard interaction (Escape to close, Tab trapped inside, no focus outside)
- Evaluate scroll lock strategy (`overflow: hidden` on body vs `overscroll-behavior`)

### Step 3: Execute
- Use native `<dialog>` element with `showModal()` for modal behavior
- Implement focus trap: auto-focus first interactive element, cycle Tab within dialog
- Add `aria-labelledby` (dialog title) and `aria-describedby` (dialog description)
- Style `::backdrop` pseudo-element for overlay dimming
- Lock background scroll when modal is open
- Close on Escape key (built into `<dialog>`) and optional backdrop click
- Return focus to the trigger element on close

### Step 4: Validate
- Test keyboard-only operation (open, interact, close, focus returns correctly)
- Verify screen reader announces dialog role, title, and content
- Confirm background content is inert (not focusable or clickable)
- Check that stacked/nested dialogs work correctly if needed

## Quality Criteria

- [ ] Focus moves to dialog on open and returns to trigger on close
- [ ] Tab key is trapped within the dialog (no focus escape to background)
- [ ] Dialog has `aria-labelledby` pointing to its heading
- [ ] Escape key closes the dialog
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Building modals from `<div>` elements without `role="dialog"` and focus management
- Forgetting to return focus to the trigger element on close
- Using `z-index` wars instead of the native `<dialog>` top layer

## Related Skills

- `accessibility-testing` — modal dialogs are common a11y failure points
- `navigation-patterns` — mobile navigation often uses dialog/drawer patterns
