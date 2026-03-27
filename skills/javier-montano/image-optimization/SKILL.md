---
name: image-optimization
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Optimize images for web performance using modern formats (WebP, AVIF),
  responsive srcset, lazy loading, and CDN delivery strategies.
  Trigger: "image optimization", "WebP", "AVIF", "lazy loading", "srcset"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Image Optimization

> "The fastest image is the one you don't load." — Addy Osmani

## TL;DR

Guides comprehensive image optimization for web performance — converting to modern formats (WebP, AVIF), implementing responsive images with srcset and sizes, adding lazy loading, and configuring CDN delivery with caching. Use when images are the bottleneck in your page load performance (they usually are).

## Procedure

### Step 1: Discover
- Audit current image assets (count, sizes, formats, dimensions)
- Measure image impact on page weight and LCP with Lighthouse
- Check existing image pipeline (build-time optimization, CMS upload)
- Identify hero/above-the-fold images vs below-the-fold content images

### Step 2: Analyze
- Determine optimal formats per use case (AVIF for photos, SVG for icons, WebP as fallback)
- Calculate responsive breakpoints based on actual layout widths (not arbitrary)
- Evaluate CDN options (Firebase Hosting, Cloudflare, imgix, Cloudinary)
- Decide build-time vs runtime image processing strategy

### Step 3: Execute
- Convert images to WebP/AVIF with quality optimization (80% quality typical sweet spot)
- Implement `<picture>` element with format fallback chain (AVIF → WebP → JPEG)
- Add `srcset` and `sizes` attributes matching actual rendered widths
- Apply `loading="lazy"` to below-the-fold images, `fetchpriority="high"` to LCP image
- Set up build pipeline (sharp, imagemin, or framework plugin) for automatic optimization
- Configure CDN caching headers (`Cache-Control: public, max-age=31536000, immutable`)

### Step 4: Validate
- Run Lighthouse — target zero "properly size images" warnings
- Verify LCP image loads within 2.5 seconds on simulated 3G
- Confirm lazy loading works (images don't load until scrolled into view)
- Check that AVIF/WebP is served to supporting browsers, JPEG to others

## Quality Criteria

- [ ] All raster images served in at least WebP format with JPEG fallback
- [ ] Responsive images use srcset with at least 3 size variants
- [ ] LCP image is preloaded or has `fetchpriority="high"`
- [ ] Total image weight per page is under 500KB for typical content pages
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Serving 2000px images in 300px containers (no srcset)
- Lazy loading the LCP hero image (delays largest contentful paint)
- Using CSS background-image for content images (no srcset, no alt text, no lazy loading)

## Related Skills

- `performance-testing` — measuring the impact of image optimization
- `build-optimization` — integrating image processing into the build pipeline
