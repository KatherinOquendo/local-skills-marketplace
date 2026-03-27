# Mapping Artifact Relationships

When designing an ecosystem, understanding how artifacts relate to each other prevents orphans, conflicts, and circular dependencies.

## Relationship Types

### Rules → Skills

Rules constrain what skills can do. When a skill generates code, the rules define what that code must (or must not) look like.

```
R-no-inline-styles  ←constrains→  frontend-builder skill
R-typed-responses   ←constrains→  api-builder skill
```

**How to document**: In the skill's SKILL.md, reference the rules that apply: "Output must comply with R-no-inline-styles and R-typed-responses."

### Skills → Workflows

Workflows orchestrate skills. A workflow's steps may invoke one or more skills to accomplish their work.

```
create-endpoint workflow  →uses→  api-builder skill
                          →uses→  naming-and-slugging skill
```

**How to document**: In the workflow's Prerequisites section, list required skills.

### Workflows → Rules

Workflows can enforce rules during execution. A verification step might check rule compliance.

```
deploy-api workflow  →enforces→  R-no-debug-code rule
                     →enforces→  R-auth-required rule
```

**How to document**: In the workflow's verification step, reference which rules are checked.

## Dependency Mapping

Before creating artifacts, sketch the dependency map:

```
                    ┌─────────────┐
                    │   Rules     │
                    │ (constraints)│
                    └──────┬──────┘
                           │ constrain
                    ┌──────▼──────┐
                    │   Skills    │
                    │ (capabilities)│
                    └──────┬──────┘
                           │ used by
                    ┌──────▼──────┐
                    │  Workflows  │
                    │ (processes)  │
                    └─────────────┘
```

Dependencies flow downward. Rules are the foundation (no dependencies), skills depend on rules, and workflows depend on both.

## Common Pitfalls

**Circular dependencies**: Skill A requires Workflow B which requires Skill A. If you find this, break the cycle by extracting the shared logic into a standalone skill or reference file.

**Phantom references**: A workflow references "api-builder" but the skill is actually named "api-endpoint-builder". Always verify names match exactly.

**Over-coupling**: Every artifact references every other artifact. This makes the ecosystem rigid. Aim for loose coupling: each artifact should work independently where possible, with explicit integration points.

## Validation

After mapping relationships, verify:

1. No cycles in the dependency graph
2. Every referenced artifact exists
3. No artifact is completely isolated (referenced by nothing)
4. The dependency depth is shallow (ideally 2-3 levels max)
