---
name: print-stylesheet
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Create print-optimized stylesheets with @media print, PDF-friendly layouts,
  page break control, and content visibility management for printing.
  Trigger: "print stylesheet", "print CSS", "PDF layout", "@media print"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Print Stylesheet

> "What looks good on screen doesn't always look good on paper — design for both." — Unknown

## TL;DR

Guides the creation of print-optimized stylesheets using `@media print` — hiding non-essential UI elements, controlling page breaks, adjusting typography for paper, and ensuring links and content are useful in printed/PDF form. Use when your content needs to be printable (invoices, articles, reports, resumes).

## Procedure

### Step 1: Discover
- Identify pages that users are likely to print (invoices, articles, docs, reports)
- Check existing print styles and their coverage
- Review content that only makes sense on screen (navigation, modals, interactive widgets)
- Determine target paper sizes (A4 for international, Letter for US)

### Step 2: Analyze
- Plan what to hide (nav, footer, sidebar, buttons, ads, cookie banners)
- Decide what to reveal (full URLs after links, expanded abbreviations)
- Evaluate page break placement (avoid breaking inside figures, tables, code blocks)
- Consider background colors/images (most browsers strip them by default)

### Step 3: Execute
- Add `@media print` block or separate `print.css` with `media="print"`
- Hide non-essential elements: `nav, .sidebar, .no-print { display: none; }`
- Show link URLs after anchor text: `a[href]::after { content: " (" attr(href) ")"; }`
- Control page breaks: `page-break-inside: avoid` on figures, tables, and cards
- Set appropriate margins with `@page { margin: 2cm; }`
- Force black text on white background for readability and ink economy
- Use `break-before: page` for logical content sections

### Step 4: Validate
- Print preview in Chrome, Firefox, and Safari (rendering differs)
- Verify no content is cut off at page boundaries
- Check that links show their URLs in printed output
- Confirm reasonable page count (no excessive blank pages)

## Quality Criteria

- [ ] Navigation, modals, and interactive elements hidden in print
- [ ] Page breaks avoid splitting figures, tables, and code blocks
- [ ] Text is black on white for readability and ink economy
- [ ] Link URLs visible in printed output via `::after` pseudo-element
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Forgetting print styles entirely (most web apps have none)
- Hiding too much content — the printout should still be useful
- Relying on `color-adjust: exact` for backgrounds (not universally supported)

## Related Skills

- `accessibility-testing` — print accessibility overlaps with visual a11y
- `blog-cms` — articles and documentation are the most-printed web content
