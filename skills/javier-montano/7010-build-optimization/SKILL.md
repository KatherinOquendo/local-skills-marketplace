---
name: build-optimization
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Optimize build configuration with Vite, tree-shaking, code splitting,
  chunk strategies, and minification for smaller, faster bundles.
  Trigger: "build optimization", "Vite config", "tree-shaking", "code splitting", "bundle size"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Build Optimization

> "The best code is the code you don't ship to the browser." — Unknown

## TL;DR

Guides frontend build optimization — Vite configuration, tree-shaking for dead code elimination, route-based code splitting, manual chunk strategies, and minification settings for smaller production bundles. Use when build output is too large, page load is slow, or you need to optimize the build pipeline.

## Procedure

### Step 1: Discover
- Analyze current bundle size with `vite-plugin-visualizer` or `source-map-explorer`
- Identify the largest chunks and their composition
- Check tree-shaking effectiveness (are unused exports eliminated?)
- Review dynamic import usage for code splitting opportunities

### Step 2: Analyze
- Identify dead code and unused dependencies for removal
- Plan chunk strategy: vendor (rarely changes), shared (common code), route-level
- Evaluate library alternatives (date-fns vs moment, preact vs react for small apps)
- Assess CSS extraction and minification configuration

### Step 3: Execute
- Configure Vite `build.rollupOptions.output.manualChunks` for optimal splitting
- Implement route-level code splitting with `React.lazy()` or framework equivalent
- Enable tree-shaking by using ESM imports (named imports, not default namespace)
- Replace heavy libraries with lighter alternatives where possible
- Configure `build.target` to match `browserslist` (avoid unnecessary transpilation)
- Set up compression (gzip, brotli) via build plugin or server configuration
- Add `sideEffects: false` in `package.json` for better tree-shaking
- Configure CSS code splitting and minification

### Step 4: Validate
- Compare bundle size before and after optimization (document improvement)
- Verify tree-shaking eliminated unused code with bundle analyzer
- Confirm code splitting produces reasonable chunk sizes (50-200KB each)
- Check that lazy-loaded routes load without visible delay

## Quality Criteria

- [ ] Bundle analyzer report reviewed and largest chunks addressed
- [ ] Route-level code splitting implemented for all routes
- [ ] Tree-shaking effective — no dead code in production bundles
- [ ] Total initial JS payload under 200KB (gzipped)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Importing entire libraries when only specific functions are needed
- Creating too many chunks (HTTP/2 helps but has limits)
- Disabling minification for debugging (use source maps instead)

## Related Skills

- `performance-testing` — measuring the impact of build optimization
- `cross-browser-testing` — build targets affect browser compatibility
