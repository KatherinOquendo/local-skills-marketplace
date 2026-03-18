# Rule Output Template

Use this template when creating new governance rules. Copy the structure below and fill in each section.

```markdown
---
description: [One-line summary: what this rule prevents]
globs: "[file/path/patterns, comma-separated]"
---
# R-[kebab-case-name]

## The Constraint

[One sentence: the immutable constraint. Be specific and binary.]

## Why This Matters

[2-3 sentences: what failure does this prevent? What bad outcome does it block?
Don't say "best practice" — explain the actual consequence of violation.]

## Scope

- **Files affected:** [glob patterns, e.g., `src/**/*.ts`]
- **Trigger:** [When is this checked? On create, on edit, on commit?]

## Examples

### Bad (Violation)

​```[language]
// Show the exact violation, annotated with why it's bad
​```

### Good (Compliance)

​```[language]
// Show the corrected version, as close to the Bad example as possible
// Only the violation should differ
​```

## Exceptions

[Optional: Are there cases where this rule doesn't apply?
e.g., "Test files (`**/*.test.ts`) are exempt because console.log
aids debugging during test development."]
```

## Complete Example

Here's a finished rule following this template:

```markdown
---
description: Prevents inline styles in React components
globs: "src/components/**/*.tsx"
---
# R-no-inline-styles

## The Constraint

No `style={{}}` attributes on JSX elements in component files.

## Why This Matters

Inline styles bypass the design system, making visual consistency impossible
to maintain. They can't be overridden by themes, don't benefit from CSS
caching, and make responsive design harder. All styling should go through
the design token system or CSS modules.

## Scope

- **Files affected:** `src/components/**/*.tsx`
- **Trigger:** On file save or pre-commit

## Examples

### Bad (Violation)

​```tsx
function Card({ title }) {
  return (
    <div style={{ padding: '16px', backgroundColor: '#f5f5f5' }}>
      <h2 style={{ color: '#333' }}>{title}</h2>
    </div>
  );
}
​```

### Good (Compliance)

​```tsx
import styles from './card.module.css';

function Card({ title }) {
  return (
    <div className={styles.card}>
      <h2 className={styles.title}>{title}</h2>
    </div>
  );
}
​```

## Exceptions

Dynamically computed values (e.g., `style={{ width: `${percentage}%` }}`)
are acceptable when the value depends on runtime data that can't be
expressed as a CSS class.
```
