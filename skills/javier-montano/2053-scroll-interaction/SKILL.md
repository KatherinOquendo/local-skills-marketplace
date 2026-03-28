---
name: scroll-interaction
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implement scroll-driven interactions using Intersection Observer, CSS
  scroll-driven animations, parallax effects, and scroll progress indicators. [EXPLICIT]
  Trigger: "scroll animation", "intersection observer", "parallax", "scroll-driven"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Scroll Interaction

> "Scrolling is the new clicking — make the journey worth taking." — Unknown

## TL;DR

Guides the implementation of scroll-driven interactions — fade-in animations triggered by Intersection Observer, CSS scroll-driven animations, parallax effects, scroll progress indicators, and snap scrolling. Use when you want to create engaging scroll experiences without sacrificing performance. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify elements that should animate on scroll (sections, cards, images, counters)
- Check for existing scroll libraries (GSAP ScrollTrigger, AOS, Lenis)
- Review performance budget — scroll handlers can easily cause jank
- Determine `prefers-reduced-motion` requirements

### Step 2: Analyze
- Choose approach: CSS scroll-driven animations (modern) vs Intersection Observer (wider support)
- Plan animation triggers (enter viewport, exit, scroll progress percentage)
- Evaluate parallax feasibility (avoid on mobile — performance and UX concerns)
- Design fallback for `prefers-reduced-motion: reduce` (instant state, no animation)

### Step 3: Execute
- Set up Intersection Observer with appropriate `rootMargin` and `threshold` values
- Add CSS classes on intersection for enter/exit animations
- Implement scroll-driven animations with `animation-timeline: scroll()` where supported
- Build scroll progress indicator using `animation-timeline: scroll(root)` or JS fallback
- Add `scroll-snap-type` for section-based scrolling experiences
- Respect `prefers-reduced-motion` — disable or simplify all animations

### Step 4: Validate
- Profile with DevTools Performance tab — no jank at 60fps during scrolling
- Test on low-end mobile devices (scroll performance is most critical there)
- Verify `prefers-reduced-motion` disables animations completely
- Confirm no layout shifts caused by animated elements changing size

## Quality Criteria

- [ ] All scroll animations run at 60fps (no main thread bottlenecks)
- [ ] Intersection Observer used instead of scroll event listeners
- [ ] `prefers-reduced-motion` respected — animations disabled for users who prefer it
- [ ] Animations enhance content comprehension, not just decoration
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `scroll` event listeners instead of Intersection Observer (causes jank)
- Parallax effects on mobile devices (poor performance, disorienting UX)
- Animations that block content visibility until scroll (users may never see it)

## Related Skills

- `portfolio-sites` — scroll animations are common in portfolios
- `performance-testing` — measuring scroll performance impact

## Usage

Example invocations:

- "/scroll-interaction" — Run the full scroll interaction workflow
- "scroll interaction on this project" — Apply to current context


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
