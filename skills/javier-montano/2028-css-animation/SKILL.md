---
name: css-animation
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements web animations using CSS keyframes, transitions, GSAP library,
  and the View Transitions API. Covers performance-optimized animations,
  reduced motion support, and scroll-driven animations. [EXPLICIT]
  Trigger: "animation", "keyframes", "transitions", "GSAP", "View Transitions", "scroll animation"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# CSS Animation

> "Animation is not the art of drawings that move but the art of movements that are drawn." — Norman McLaren

## TL;DR

Implements web animations using CSS keyframes, transitions, GSAP, and the View Transitions API with performance optimization and accessibility considerations (prefers-reduced-motion). Use this skill when adding micro-interactions, page transitions, scroll-driven animations, or complex choreographed sequences. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify animation requirements: micro-interactions, page transitions, scroll effects, loading states
- Review existing animations for performance issues (layout thrashing, jank)
- Check browser support for target animation features (View Transitions, scroll-timeline)
- Assess reduced motion preferences: does the current implementation respect prefers-reduced-motion?

### Step 2: Analyze
- Choose the right tool for each animation:
  - **CSS Transitions**: simple state changes (hover, focus, active)
  - **CSS Keyframes**: multi-step, looping, or complex single-element animations
  - **GSAP**: complex timelines, scroll-triggered, physics-based animations
  - **View Transitions API**: page/route transitions with morphing elements
  - **Scroll-driven animations**: progress-based animations tied to scroll position
- Optimize for performance: prefer transform and opacity (compositor-only properties)
- Design animation curves: ease-in for exits, ease-out for entries, ease-in-out for transitions

### Step 3: Execute
- Implement CSS transitions for interactive state changes with appropriate duration (150-300ms)
- Build keyframe animations for loading states, attention-grabbers, and decorative effects
- Set up GSAP timelines for complex choreographed sequences
- Implement View Transitions for route changes with fallback for unsupported browsers
- Add `@media (prefers-reduced-motion: reduce)` to disable or simplify all animations
- Use will-change sparingly to hint compositor optimization

### Step 4: Validate
- Verify animations run at 60fps using Chrome DevTools Performance panel
- Confirm prefers-reduced-motion eliminates or simplifies all motion
- Check animations don't cause layout shifts (CLS impact)
- Test animation feel: duration, easing, and staging feel natural

## Quality Criteria

- [ ] Animations use compositor-only properties (transform, opacity) where possible
- [ ] prefers-reduced-motion is respected for all animations
- [ ] Animation durations are appropriate (150-300ms for UI, longer for storytelling)
- [ ] No layout shifts caused by animations (CLS = 0)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Animating width/height/top/left causing layout recalculation on every frame
- Ignoring prefers-reduced-motion for users with vestibular disorders
- will-change on everything: causes excessive memory consumption

## Related Skills

- `css-architecture` — animation classes within the CSS methodology
- `performance-architecture` — animations impact Core Web Vitals (CLS)
- `responsive-design` — animations may need adjustment per viewport

## Usage

Example invocations:

- "/css-animation" — Run the full css animation workflow
- "css animation on this project" — Apply to current context


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
