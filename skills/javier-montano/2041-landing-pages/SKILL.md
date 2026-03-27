---
name: landing-pages
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Design and build high-converting landing pages with hero sections, CTAs,
  social proof, and A/B testing. Covers conversion optimization and analytics.
  Trigger: "landing page", "hero section", "CTA", "conversion optimization"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Landing Pages

> "Don't make me think — and definitely don't make me scroll to find the button." — Steve Krug (adapted)

## TL;DR

Guides the creation of high-converting landing pages with persuasive copy structure, compelling CTAs, social proof sections, and measurable A/B testing. Use when launching a product, campaign, or lead generation funnel that needs a focused, single-purpose page.

## Procedure

### Step 1: Discover
- Identify the primary conversion goal (sign-up, purchase, download, demo request)
- Review target audience personas and their pain points
- Analyze competitor landing pages for patterns and differentiation
- Check existing brand assets, testimonials, and social proof data

### Step 2: Analyze
- Define the value proposition hierarchy (headline → subhead → supporting points)
- Plan page sections: Hero → Problem → Solution → Features → Social Proof → CTA → FAQ
- Determine A/B test hypotheses (headline variants, CTA color, form length)
- Choose tech stack (static HTML, framework SSR, page builder)

### Step 3: Execute
- Build above-the-fold hero with clear headline, subhead, and primary CTA
- Add social proof (testimonials, logos, metrics, star ratings)
- Implement sticky CTA or repeated CTA pattern for long pages
- Set up analytics events (scroll depth, CTA clicks, form starts/completions)
- Configure A/B testing with Google Optimize, Optimizely, or custom split logic
- Optimize Core Web Vitals — fast LCP for hero image, minimal CLS

### Step 4: Validate
- Test on mobile — 60%+ traffic is mobile; CTA must be thumb-friendly
- Verify analytics events fire correctly in GA4/GTM
- Run PageSpeed Insights — target 90+ performance score
- Review copy for clarity: 8th-grade reading level, scannable structure

## Quality Criteria

- [ ] Single clear CTA — no competing navigation or distractions
- [ ] Page loads in under 2 seconds on 3G connection
- [ ] Social proof is authentic and specific (not generic)
- [ ] Mobile layout is optimized — not just responsive, but redesigned for touch
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Multiple competing CTAs that dilute conversion focus
- Hero images that push the headline below the fold on mobile
- Missing or vague value proposition ("We help businesses grow")

## Related Skills

- `google-analytics` — tracking conversions and funnel drop-off
- `image-optimization` — fast hero images are critical for LCP
