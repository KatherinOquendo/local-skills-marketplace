---
name: state-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Designs client-side state management strategies using Redux, NgRx, Zustand,
  Context API, and Firestore real-time sync. Covers state shape design,
  selector patterns, and optimistic updates. [EXPLICIT]
  Trigger: "state management", "Redux", "NgRx", "Zustand", "Context API"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# State Management

> "State is the root of all revenue... and the root of all bugs." — Unknown

## TL;DR

Designs client-side state management architectures using Redux, NgRx, Zustand, Context API, or Firestore sync, with clear patterns for state shape, selectors, and side effects. Use this skill when application state grows complex, when multiple components share data, or when choosing between state management solutions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Audit current state: what data is managed where (local, global, server, URL)
- Identify state categories: server cache, UI state, form state, navigation state
- Map component tree to identify shared state needs and prop drilling pain points
- Review existing state management patterns and libraries in the codebase

### Step 2: Analyze
- Classify state by scope: component-local, feature-scoped, app-global
- Evaluate solutions: Redux/NgRx for complex global, Zustand for simple global, Context for theme/auth, React Query/SWR for server cache
- Design normalized state shape to avoid data duplication
- Plan derived state using memoized selectors (Reselect, createSelector)

### Step 3: Execute
- Define state shape with TypeScript interfaces
- Implement action/reducer patterns (Redux/NgRx) or simpler store patterns (Zustand)
- Design selectors for derived data with memoization
- Implement optimistic updates for responsive UX
- Set up Firestore real-time listeners with proper cleanup
- Document state flow: action → middleware → reducer → selector → component

### Step 4: Validate
- Verify no unnecessary re-renders caused by state changes (React DevTools Profiler)
- Confirm Firestore listeners are detached on unmount (no memory leaks)
- Check that optimistic updates handle rollback on server error
- Validate state is serializable for debugging and persistence

## Quality Criteria

- [ ] State shape is normalized and typed with TypeScript
- [ ] Selectors are memoized for derived data
- [ ] Side effects are isolated in middleware/effects, not components
- [ ] Firestore listeners have proper cleanup lifecycle
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Putting everything in global state (server cache, form state, UI toggles)
- Denormalized state with duplicated data that gets out of sync
- Direct Firestore calls in components instead of through state management layer

## Related Skills

- `realtime-architecture` — Firestore real-time sync patterns
- `component-architecture` — state boundaries align with component boundaries
- `react-development` — React-specific state management patterns

## Usage

Example invocations:

- "/state-management" — Run the full state management workflow
- "state management on this project" — Apply to current context


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
