---
name: firestore-queries
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Write efficient Firestore queries with compound filters, composite indexes,
  cursor-based pagination, aggregation queries, and real-time listeners.
  Trigger: "firestore query", "firestore index", "firestore pagination", "firestore where"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Firestore Queries

> "The right index turns an impossible query into an instant one." — Unknown

## TL;DR

Guides efficient Firestore query implementation — compound queries with multiple where clauses, composite index management, cursor-based pagination with `startAfter`/`limit`, aggregation queries (count, sum, average), and real-time listeners with proper cleanup. Use when building data-fetching logic against Firestore.

## Procedure

### Step 1: Discover
- List all queries the application needs (by screen or feature)
- Check existing `firestore.indexes.json` for defined composite indexes
- Identify queries that require sorting + filtering combinations
- Review real-time listener usage and cleanup patterns

### Step 2: Analyze
- Determine which queries need composite indexes (multi-field where + orderBy)
- Plan pagination strategy (cursor-based with `startAfter` vs offset)
- Evaluate server-side aggregation vs client-side aggregation
- Identify queries that benefit from collection group scope

### Step 3: Execute
- Build queries with `where()`, `orderBy()`, `limit()` chaining
- Create composite indexes in `firestore.indexes.json` or via Firebase console error links
- Implement cursor-based pagination: store last document, use `startAfter(lastDoc)`
- Use aggregation queries (`getCountFromServer`, `getAggregateFromServer`) for counts/sums
- Set up real-time listeners with `onSnapshot` and proper `unsubscribe()` cleanup
- Handle query errors (permission denied, missing index) with user-friendly messages

### Step 4: Validate
- Confirm all queries work without console "missing index" errors
- Test pagination with boundary cases (empty results, single page, last page)
- Verify real-time listeners unsubscribe on component unmount (no memory leaks)
- Check query performance with large collections (use Firestore emulator profiling)

## Quality Criteria

- [ ] All composite indexes defined in `firestore.indexes.json` and deployed
- [ ] Pagination uses cursor-based approach (not offset-based)
- [ ] Real-time listeners properly cleaned up on component/page teardown
- [ ] Query errors handled gracefully with fallback UI
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `offset()` for pagination (reads and charges for all skipped documents)
- Fetching all documents and filtering/sorting client-side
- Not unsubscribing from `onSnapshot` listeners (causes memory leaks and phantom reads)

## Related Skills

- `firestore-modeling` — query efficiency depends on data model design
- `firestore-security-rules` — rules must allow the queries being performed
