# Naming Patterns Reference

Detailed naming conventions per entity type, edge cases, and the canonical slug algorithm.

## Entity Patterns

### Skills

Skills live in their own directory. The directory name IS the skill identifier.

```
Pattern:   kebab-case-name/
Examples:  naming-and-slugging/
           rule-forge/
           ecosystem-forge/
```

Internal structure follows fixed conventions:

| File/Dir | Name | Note |
|---|---|---|
| Main file | `SKILL.md` | Uppercase exception — recognized by tooling |
| References | `reference/*.md` | Kebab-case filenames |
| Scripts | `tools/*.py` | Kebab-case with `.py` extension |

### Rules

Rules define binary Pass/Fail constraints. The `R-` prefix makes them instantly identifiable in listings and grep results.

```
Pattern:   R-kebab-case.md
Examples:  R-no-console-log.md
           R-lowercase-filenames.md
           R-max-function-length.md
```

The body after `R-` describes what the rule governs. Prefer "no-X" for prohibition rules and "require-X" for obligation rules.

### Workflows

Workflows describe step-by-step automation. Starting with a verb makes the action immediately clear.

```
Pattern:   verb-noun.md  or  verb-noun-context.md
Examples:  create-component.md
           deploy-staging.md
           review-pull-request.md
```

The verb is the action, the noun is the target. Optional context narrows scope.

### Documents

General documentation follows plain kebab-case.

```
Pattern:   topic-description.md
Examples:  architecture-overview.md
           onboarding-guide.md
           api-reference.md
```

## Edge Cases

### Acronyms and Initialisms

Treat as a single lowercase word. Never capitalize or separate individual letters.

```
Good:  api-client.ts     oauth2-handler.ts     css-module.ts
Bad:   API-client.ts     o-auth-2-handler.ts   CSS-Module.ts
```

### Numbers

Allowed when semantically meaningful. Not allowed as arbitrary sequence identifiers.

```
Good:  oauth2-handler.ts   (2 is part of the protocol name)
       http2-server.ts     (2 is part of the technology name)
Bad:   file-2.md           (2 is a sequence number — use descriptive name)
       step-3-deploy.md    (3 is ordering — use verb-noun pattern instead)
```

### Compound Extensions

Extensions like `.test.ts`, `.module.css`, and `.spec.tsx` are semantic — they encode what the file *is* (a test, a module, a spec). These are NOT naming violations; they are expected patterns.

```
Valid compound extensions:
  .test.ts    .test.tsx    .test.js
  .spec.ts    .spec.tsx    .spec.js
  .module.css .module.scss
  .stories.tsx .stories.ts
  .config.ts  .config.js
  .d.ts
```

The base name before the compound extension must still follow kebab-case: `user-auth.test.ts`, not `UserAuth.test.ts`.

### Uppercase Convention Files

Some files are recognized by tooling in UPPERCASE. These are the only exceptions to kebab-case:

```
SKILL.md     README.md      LICENSE        LICENSE.txt
REFERENCE.md CHANGELOG.md   CONTRIBUTING.md
Makefile     Dockerfile
```

No other files should use uppercase.

### Extensions

Always lowercase: `.md`, `.ts`, `.tsx`, `.py`, `.json`, `.yaml`. Never `.MD`, `.Py`, or `.JSON`.

## Slug Transformation Algorithm

The canonical algorithm implemented by `slugger.py`:

```
Step  Input                    Output
───────────────────────────────────────────────
1.    "Héllo Wörld!"          "Hello World!"      (NFKD → ASCII)
2.    "Hello World!"          "hello world!"      (lowercase)
3.    "hello world!"          "hello-world!"      (spaces/underscores → hyphens)
4.    "hello-world!"          "hello-world"       (remove non [a-z0-9-])
5.    "hello-world"           "hello-world"       (collapse consecutive hyphens)
6.    "hello-world"           "hello-world"       (trim leading/trailing hyphens)
```

The clean mode adds two additional steps after step 6:

```
7.    "new-api-client-v2"     "api-client"        (strip version markers)
8.    "api-client-final"      "api-client"        (strip status/noise suffixes)
```
