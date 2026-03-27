---
name: domain-driven-design
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Applies Domain-Driven Design tactical and strategic patterns to model complex
  business domains. Identifies bounded contexts, aggregates, domain events, and
  establishes ubiquitous language shared by developers and domain experts.
  Trigger: "bounded context", "aggregate", "domain event", "ubiquitous language", "DDD"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Domain-Driven Design

> "The heart of software is its ability to solve domain-related problems for its user." — Eric Evans

## TL;DR

Models complex business domains using DDD strategic and tactical patterns — bounded contexts, aggregates, entities, value objects, domain events, and ubiquitous language. Use this skill when tackling complex business logic, designing microservice boundaries, or when the team and domain experts speak different languages.

## Procedure

### Step 1: Discover
- Conduct domain exploration through event storming or domain storytelling sessions
- Identify key business processes, actors, and domain terminology
- Search the codebase for existing domain models, entities, and naming conventions

### Step 2: Analyze
- Define bounded contexts by identifying linguistic boundaries (same word, different meaning)
- Map context relationships using a Context Map (upstream/downstream, conformist, ACL, shared kernel)
- Identify aggregates by grouping entities that share transactional consistency boundaries
- Extract domain events that represent meaningful state transitions

### Step 3: Execute
- Document the ubiquitous language glossary with precise definitions
- Design aggregate roots with invariant enforcement and consistency boundaries
- Define domain events with clear schemas and publish/subscribe contracts
- Create value objects for concepts defined by attributes rather than identity
- Map bounded context integration patterns (ACL, Published Language, Open Host)

### Step 4: Validate
- Verify aggregate boundaries enforce all business invariants
- Confirm ubiquitous language is used consistently in code, tests, and documentation
- Check that bounded contexts have clear ownership and integration contracts
- Validate domain events capture all meaningful state transitions

## Quality Criteria

- [ ] Bounded contexts have explicit boundaries and documented relationships
- [ ] Aggregates enforce consistency invariants within their boundary
- [ ] Ubiquitous language glossary exists and matches code naming
- [ ] Domain events are named in past tense and carry sufficient data
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Anemic domain model: entities with only getters/setters and no behavior
- God aggregate: single aggregate that encompasses the entire domain
- Leaking bounded context: sharing internal models across context boundaries

## Related Skills

- `event-architecture` — implements domain events technically
- `system-architecture` — bounded contexts inform service decomposition
- `flow-mapping` — visualizes the business processes DDD models
