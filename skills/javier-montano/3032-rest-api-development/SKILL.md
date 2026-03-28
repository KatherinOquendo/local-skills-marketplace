---
name: rest-api-development
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Build RESTful APIs on Cloud Functions with Express, including middleware,
  input validation, error handling, and API documentation. [EXPLICIT]
  Trigger: "REST API", "express API", "API endpoint", "API design"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# REST API Development

> "An API is a contract — break it, and you break trust." — Unknown

## TL;DR

Guides RESTful API development on Cloud Functions using Express — route design, middleware chains, input validation, error handling, authentication, and API documentation. Use when building backend APIs for web or mobile clients on Firebase infrastructure. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify API consumers (web app, mobile app, third-party integrations)
- Map required endpoints from frontend data needs
- Check existing API patterns or conventions in the codebase
- Review authentication and authorization requirements per endpoint

### Step 2: Analyze
- Design resource-oriented URLs: `/api/v1/users/:userId/orders`
- Plan HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE
- Define request/response schemas with consistent envelope format
- Evaluate middleware needs: auth, validation, rate limiting, CORS, logging

### Step 3: Execute
- Set up Express app wrapped in `onRequest` Cloud Function
- Implement middleware chain: CORS → auth → validation → handler
- Add input validation with Joi, Zod, or express-validator
- Build consistent error responses: `{ error: { code, message, details } }`
- Implement pagination: `{ data: [...], pagination: { total, page, limit, hasNext } }`
- Add API versioning via URL prefix (`/api/v1/`)
- Document endpoints with OpenAPI/Swagger specification

### Step 4: Validate
- Test all endpoints with valid and invalid inputs
- Verify auth middleware blocks unauthorized requests
- Confirm error responses follow consistent format
- Check API documentation matches actual behavior

## Quality Criteria

- [ ] RESTful URL design with proper HTTP method usage
- [ ] Input validation on all endpoints before business logic
- [ ] Consistent error response format across all endpoints
- [ ] Authentication enforced on protected endpoints
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using POST for everything instead of appropriate HTTP methods
- Returning 200 status code for errors (use proper 4xx/5xx codes)
- Exposing internal error details (stack traces) in production responses

## Related Skills

- `cloud-functions` — Express APIs run on Cloud Functions
- `webhook-handling` — incoming webhooks are a specialized API pattern

## Usage

Example invocations:

- "/rest-api-development" — Run the full rest api development workflow
- "rest api development on this project" — Apply to current context


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
