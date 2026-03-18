# Best Practices for Writing Rules

## One Rule Per File

Don't bundle "no console.log AND no debugger AND no alert" into one rule. Each constraint gets its own file because:
- Rules become individually toggleable (disable one without affecting others)
- Testing is isolated (a failure points to exactly one constraint)
- Evolution is clean (change one rule without touching unrelated constraints)

If you later want to allow `debugger` in dev mode, you'd have to rewrite a combined rule. Three separate rules let you exempt one.

## The Power of No

Negative constraints are more effective than positive mandates. "No `console.log`" is clearer than "use the logging service" because:
- Negative: blocks one bad thing, allows many good alternatives
- Positive: mandates one approach, may not fit all contexts

Use whichever framing is clearest. Some rules are naturally positive ("all functions must have JSDoc"). But when both framings work, prefer the negative — it's more permissive.

## Scope Precision

The glob is the enforcement boundary. Getting it wrong means either false positives (blocking legitimate code) or false negatives (missing violations).

**Decision framework:**

| Start here | Widen only if... |
|---|---|
| `src/api/routes/*.ts` | Violations appear in adjacent directories |
| `src/api/**/*.ts` | The constraint applies to all API code, not just routes |
| `**/*.ts` | The constraint is truly universal to all TypeScript |

Never start at `**/*.ts` and narrow down. Start surgical and widen based on evidence.

## Writing the "Why" Section

The reasoning section prevents two failure modes:

1. **Resentment**: Developers bypass rules they don't understand. A clear "why" converts compliance from obligation to agreement.
2. **Misapplication**: Without context, future maintainers may apply the rule too broadly or too narrowly.

**Template**: "[Specific bad outcome] because [causal mechanism], leading to [downstream impact]."

Example: "Untyped API responses silently propagate incorrect data structures (causal) because TypeScript can't validate runtime shapes (mechanism), causing runtime errors that are hard to trace to the API layer (downstream)."

## Exceptions Design

Most rules need exceptions. Document them explicitly to prevent two anti-patterns:

1. **Total bypass**: A team finds one legitimate exception and disables the entire rule
2. **Invisible exceptions**: Some files are silently excluded but nobody knows which ones

Good exception format:
```
## Exceptions
- Test files (`**/*.test.ts`): console.log aids debugging during test development
- Build scripts (`scripts/`): Direct console output is the expected interface
```

Each exception names the scope (glob) and the justification.

## Naming Patterns

Rule names should be scannable — someone listing a `rules/` directory should understand each rule without opening it.

| Pattern | When to use | Example |
|---|---|---|
| `R-no-{thing}` | Prohibition | `R-no-console-log` |
| `R-require-{thing}` | Obligation | `R-require-jsdoc` |
| `R-max-{thing}` | Threshold | `R-max-function-length` |
| `R-{domain}-{constraint}` | Domain-scoped | `R-api-typed-responses` |
