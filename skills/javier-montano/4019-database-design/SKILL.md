---
name: database-design
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Designs database schemas, indexing strategies, and data models for relational
  and NoSQL databases with special focus on Firestore document modeling. [EXPLICIT]
  Covers normalization, denormalization trade-offs, and query optimization. [EXPLICIT]
  Trigger: "database", "schema", "Firestore", "data model", "indexing"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Database Design

> "Bad programmers worry about the code. Good programmers worry about data structures." — Linus Torvalds

## TL;DR

Designs database schemas and data models for relational (PostgreSQL, MySQL) and NoSQL (Firestore, MongoDB) databases with indexing strategies, normalization/denormalization trade-offs, and query optimization. Use this skill when modeling a new data domain, migrating databases, or optimizing query performance. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify entities, relationships, and cardinality from domain model
- Gather access patterns: what queries will the application run most frequently
- Determine consistency requirements: strong vs. eventual, ACID vs. BASE
- Assess data volume projections and growth rate

### Step 2: Analyze
- Choose database paradigm based on access patterns and consistency needs
- For relational: normalize to 3NF, then selectively denormalize for read performance
- For Firestore: model data around queries (document = view), plan subcollections vs. root collections
- Design indexes to support all identified query patterns
- Plan for data lifecycle: archival, TTL, soft deletes

### Step 3: Execute
- Create entity-relationship diagrams (ERD) or document structure diagrams
- Define schema with data types, constraints, and defaults
- Design composite indexes for multi-field queries
- Document Firestore security rules aligned to data model
- Write migration scripts or Firestore seeding patterns
- Plan backup and disaster recovery strategy

### Step 4: Validate
- Verify every identified query pattern is supported by an index
- Confirm Firestore document sizes stay well under 1MB limit
- Check that write patterns won't create hot spots or contention
- Validate referential integrity strategy (foreign keys vs. application-level)

## Quality Criteria

- [ ] All entity relationships are documented with cardinality
- [ ] Every frequent query has a supporting index
- [ ] Firestore models are designed query-first, not entity-first
- [ ] Data lifecycle (archival, deletion, retention) is planned
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Relational thinking in Firestore (over-normalizing document databases)
- Missing indexes discovered only in production under load
- God collection: single Firestore collection with deeply nested documents

## Related Skills

- `domain-driven-design` — domain model drives database entities
- `api-design` — API resources often map to database entities
- `caching-strategy` — caching compensates for database limitations

## Usage

Example invocations:

- "/database-design" — Run the full database design workflow
- "database design on this project" — Apply to current context


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
