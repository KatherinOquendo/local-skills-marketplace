---
name: navigation-patterns
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implement responsive navigation patterns including mobile hamburger menus,
  mega menus, breadcrumbs, tab navigation, and sidebar layouts.
  Trigger: "navigation", "navbar", "mega menu", "breadcrumbs", "sidebar nav"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Navigation Patterns

> "If they can't find it, it doesn't exist." — Unknown

## TL;DR

Guides the implementation of responsive navigation systems — hamburger menus for mobile, mega menus for complex sites, breadcrumbs for deep hierarchies, tabs for content switching, and sidebar navigation for dashboards. Use when building or refactoring site navigation for usability and accessibility.

## Procedure

### Step 1: Discover
- Map the site's information architecture (pages, sections, depth levels)
- Identify the navigation type needed (top bar, sidebar, bottom bar, tabs)
- Check current breakpoint strategy for responsive behavior
- Review navigation requirements for accessibility (keyboard, screen reader)

### Step 2: Analyze
- Choose pattern based on content volume: simple nav (<7 items), mega menu (many categories), sidebar (dashboard)
- Plan mobile strategy: hamburger drawer, bottom navigation, or collapsible accordion
- Design active state indication and current page highlighting
- Evaluate sticky/fixed positioning impact on content area

### Step 3: Execute
- Use semantic `<nav>` element with `aria-label` for multiple nav landmarks
- Build responsive breakpoint: top nav on desktop → hamburger drawer on mobile
- Implement keyboard navigation (arrow keys for menu items, Escape to close)
- Add breadcrumbs with `<ol>` and structured data (BreadcrumbList schema)
- Style active/current states clearly with both color and non-color indicators
- Add skip navigation link as first focusable element

### Step 4: Validate
- Test keyboard navigation — all menu items reachable, submenus open/close properly
- Verify screen reader announces navigation landmarks and current page
- Check mobile menu is usable with one thumb (44px minimum touch targets)
- Confirm breadcrumbs reflect actual page hierarchy correctly

## Quality Criteria

- [ ] Navigation uses semantic `<nav>` with appropriate `aria-label`
- [ ] Skip navigation link present and functional
- [ ] Mobile navigation is accessible (not just visually hidden, but properly toggled)
- [ ] Active/current page clearly indicated in all nav components
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Hiding navigation on mobile without a clear toggle indicator
- Using only color to indicate the current/active page
- Navigation menus that require hover to access (fails on touch devices)

## Related Skills

- `modal-dialog-patterns` — mobile nav drawers often use dialog patterns
- `accessibility-testing` — navigation is a top a11y audit failure area
