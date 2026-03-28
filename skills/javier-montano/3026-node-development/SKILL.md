---
name: node-development
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Node.js development patterns including streams, ESM modules, error handling,
  process management, and production-ready server configuration. [EXPLICIT]
  Trigger: "node.js", "node patterns", "streams", "ESM modules"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Node.js Development

> "Node isn't about threads — it's about not waiting." — Ryan Dahl (paraphrased)

## TL;DR

Guides Node.js development best practices — ESM module patterns, stream processing for large data, robust error handling, environment configuration, and production-ready patterns. Use when building Node.js server-side applications, CLIs, or Cloud Functions backends. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check Node.js version and `package.json` engine requirements
- Review module system in use (CommonJS `require` vs ESM `import`)
- Identify error handling patterns and unhandled rejection behavior
- Check environment variable management strategy

### Step 2: Analyze
- Evaluate migration path to ESM if still on CommonJS
- Plan error handling hierarchy (operational vs programmer errors)
- Design logging strategy (structured JSON logs for Cloud environments)
- Assess dependency management and security audit practices

### Step 3: Execute
- Configure `"type": "module"` in `package.json` for ESM
- Implement structured error classes extending `Error` with status codes
- Use streams for file/data processing to avoid memory issues
- Set up environment variables with dotenv and validation (Joi/Zod)
- Configure graceful shutdown handling (`SIGTERM`, `SIGINT`)
- Implement structured logging (pino, winston) with request correlation IDs
- Set up `npm audit` in CI pipeline for dependency vulnerability scanning

### Step 4: Validate
- Verify no unhandled promise rejections (`process.on('unhandledRejection')`)
- Test with large payloads to confirm stream processing works
- Check memory usage under load (no memory leaks in long-running processes)
- Confirm graceful shutdown completes in-flight requests before exiting

## Quality Criteria

- [ ] ESM modules used with proper `"type": "module"` configuration
- [ ] All async errors caught and handled appropriately
- [ ] Structured logging with correlation IDs for request tracing
- [ ] Environment variables validated at startup (fail fast on misconfiguration)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `try/catch` without proper error propagation (swallowing errors)
- Loading entire files into memory instead of using streams
- Mixing CommonJS and ESM without proper interop configuration

## Related Skills

- `cloud-functions` — Cloud Functions run Node.js runtime
- `serverless-patterns` — Node.js patterns specific to serverless

## Usage

Example invocations:

- "/node-development" — Run the full node development workflow
- "node development on this project" — Apply to current context


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
