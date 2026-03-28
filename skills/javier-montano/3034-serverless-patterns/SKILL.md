---
name: serverless-patterns
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Apply serverless architecture patterns — cold start mitigation, connection
  pooling, idempotency, fan-out/fan-in, and cost optimization. [EXPLICIT]
  Trigger: "serverless", "cold start", "idempotency", "connection pooling"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Serverless Patterns

> "Serverless is not about no servers — it's about no server management." — Unknown

## TL;DR

Guides serverless architecture patterns for Cloud Functions and similar platforms — cold start optimization, database connection management, idempotent function design, fan-out/fan-in patterns, and cost optimization strategies. Use when designing or optimizing serverless architectures. [EXPLICIT]

## Procedure

### Step 1: Discover
- Profile current function cold start times and invocation frequency
- Check database connection patterns (new connection per invocation?)
- Review function memory allocation and timeout configurations
- Identify functions with concurrency or ordering requirements

### Step 2: Analyze
- Categorize functions by latency sensitivity (user-facing vs background)
- Evaluate connection pooling strategies for databases and external APIs
- Design idempotency patterns for event-driven functions
- Plan cost optimization (right-sizing memory, minimum instances)

### Step 3: Execute
- Initialize global-scope resources (DB connections, SDK clients) outside handler
- Set minimum instances for latency-critical functions to avoid cold starts
- Implement idempotency tokens/checks for all event-driven functions
- Use fan-out pattern: one trigger spawns multiple parallel functions via PubSub
- Apply the single-responsibility principle: one function per concern
- Configure concurrency settings (Cloud Functions v2 supports multiple concurrent requests)
- Implement circuit breaker pattern for external service calls

### Step 4: Validate
- Measure cold start times with and without minimum instances
- Verify idempotent functions produce same result on duplicate invocations
- Load test concurrent invocations to confirm scaling behavior
- Review billing to ensure cost optimization measures are effective

## Quality Criteria

- [ ] Global-scope initialization for shared resources (no per-request SDK init)
- [ ] Idempotent design for all event-driven functions
- [ ] Minimum instances configured for user-facing latency-critical functions
- [ ] Memory allocation right-sized based on actual usage profiling
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Creating new database connections on every function invocation
- Assuming functions execute in order (event-driven functions may run out of order)
- Over-provisioning minimum instances (increased cost with no benefit)

## Related Skills

- `cloud-functions` — Cloud Functions are the primary serverless platform
- `scheduled-functions` — scheduled serverless execution patterns

## Usage

Example invocations:

- "/serverless-patterns" — Run the full serverless patterns workflow
- "serverless patterns on this project" — Apply to current context


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
