# BMAD Artifact Schemas

All YAML/JSON schemas for BMAD artifacts. Used by validation scripts and as reference for template creation.

**[R38]** Every field marked `# Required` must be present for the artifact to pass schema validation. Fields marked `# Optional` may be omitted. Fields with `enum` constraints must use one of the listed values exactly.

---

## 1. Agent Definition Schema (`.agent.yaml`)

```yaml
# Required fields
metadata:
  id: string          # Required. kebab-case unique identifier. Regex: ^[a-z][a-z0-9-]*$
  name: string        # Required. Display name. Max 50 characters.
  icon: string        # Required. Single emoji character.
  module: string      # Required. Module identifier (e.g., "bmm"). Regex: ^[a-z]{2,10}$
  version: string     # Optional but recommended. Semver format: ^\\d+\\.\\d+\\.\\d+$
  description: string # Optional. One-line purpose. Max 120 characters.
  status: string      # Optional. Enum: active | deprecated. Default: active.

# Required persona block
persona:
  role: string                  # Required. Professional title. Max 100 characters.
  identity: string              # Required. Min 2 sentences. Background, personality, expertise narrative.
  communication_style: string   # Required. How the agent communicates.
  principles:                   # Required. Core beliefs (min 1, max 5 items).
    - string

# Required menu block (at least 1 entry, max 7 entries)
menu:
  - trigger: string             # Required. Exactly 2 uppercase letters. Regex: ^[A-Z]{2}$
    description: string         # Required. Workflow display name. Max 50 characters.
    workflow: string            # Required. Relative path to workflow file. Must resolve to existing file.

# Optional prompts
prompts:
  system: string                # Optional. System prompt for agent activation.
  greeting: string              # Optional. Initial message when agent is invoked.
```

### Validation Rules
- `metadata.id` must be unique across all agents in the same module
- `menu.trigger` must be unique within the agent
- `persona.principles` array must have 1-5 entries
- `menu` array must have 1-7 entries
- Every `workflow` path must resolve to an existing file at build time

## 2. Workflow Step File Schema (`step-NN-name.md`)

```yaml
---
# Frontmatter (YAML)
stepNumber: integer             # Sequential step number (1-based)
stepName: string                # Human-readable step name
agent: string                   # Agent ID responsible for this step
inputs:                         # Files/artifacts required as input
  - string                      # Relative path to artifact
outputs:                        # Files/artifacts produced
  - string                      # Relative path to output
stepsCompleted: [string]        # Array of completed step IDs (state tracking)
currentStep: string             # Current step ID
nextStep: string                # Next step ID (null if last)
---

## Step Goal
<Clear objective for this step>

## Execution Rules
<Constraints and guardrails for the agent>

## Instructions
1. <Numbered action items>
2. ...

## Success Metrics
<How to validate this step completed correctly>

<!-- HALT: Do not proceed to next step until this step is validated -->
```

## 3. PRD Frontmatter Schema

```yaml
---
title: string                   # Product/feature name
version: string                 # PRD version (semver)
status: enum                    # draft | review | approved | superseded
author: string                  # PRD author
date: string                    # ISO 8601 date
product-brief-ref: string       # Path to source product brief
stakeholders:
  - name: string
    role: string
success-metrics:
  - metric: string
    target: string
    measurement: string
---
```

## 4. Architecture Document Frontmatter

```yaml
---
title: string                   # Architecture title
version: string                 # Document version
status: enum                    # draft | review | approved
prd-ref: string                 # Path to source PRD
architect: string               # Author
date: string                    # ISO 8601
tech-stack:
  frontend: [string]
  backend: [string]
  database: [string]
  infrastructure: [string]
adrs:                           # Architecture Decision Records
  - id: string                  # ADR-001 format
    title: string
    status: enum                # proposed | accepted | deprecated | superseded
    date: string
---
```

## 5. Epic Schema

```yaml
---
epic-id: string                 # EPIC-001 format
title: string
status: enum                    # draft | ready | in-progress | done
priority: enum                  # critical | high | medium | low
prd-refs:                       # PRD functional requirements covered
  - string                      # FR-001 format
story-count: integer
estimated-points: integer
dependencies:
  - epic-id: string
    type: enum                  # blocks | blocked-by | related
---
```

## 6. User Story Schema

```yaml
---
story-id: string                # Required. Regex: ^STORY-[A-Z]+-\\d{3}$ (e.g., STORY-AUTH-001)
epic-ref: string                # Required. Parent epic ID. Must match an existing epic.
title: string                   # Required. Max 100 characters.
status: enum                    # Required. Enum: draft | ready | in-progress | review | done | blocked
points: integer                 # Required. Allowed values: 1, 2, 3, 5, 8. (13 is forbidden — split the story)
priority: enum                  # Required. Enum: critical | high | medium | low
assigned-to: string             # Optional. Agent ID or team member name. Null if unassigned.
sprint: integer                 # Optional. Sprint number. Null if unassigned. Range: 1-999.
dependencies:
  - story-id: string            # Optional array. Each entry references an existing story.
    type: enum                  # Required if dependency exists. Enum: blocks | blocked-by
acceptance-criteria-count: integer # Required. Min 1. Must match actual AC count in story body.
fr-refs:                        # Required. At least one FR reference for traceability.
  - string                      # FR-AREA-NNN format
---
```

### Validation Rules
- `points` must be a Fibonacci number in {1, 2, 3, 5, 8}. Value 13 is a validation error.
- `acceptance-criteria-count` must be >= 1 and must match the number of Given/When/Then blocks in the story body
- `fr-refs` must contain at least one entry that matches an FR in the PRD
- Circular dependencies (A blocks B, B blocks A) are a validation error

## 7. Sprint Status Schema (`sprint-status.yaml`)

```yaml
sprint:
  number: integer               # Sprint number
  start-date: string            # ISO 8601
  end-date: string              # ISO 8601
  goal: string                  # Sprint goal statement
  status: enum                  # planning | active | review | closed

stories:
  - id: string                  # Story ID
    title: string
    status: enum                # Todo | in-progress | review | done | blocked
    points: integer
    assigned-to: string
    branch: string              # Git branch name
    notes: string               # Optional status notes

metrics:
  total-points: integer
  completed-points: integer
  velocity: float               # Points/sprint (rolling average)
  burndown:                     # Daily burndown data
    - date: string
      remaining: integer

blockers:
  - id: string
    description: string
    severity: enum              # critical | high | medium
    owner: string
    resolution: string          # null if unresolved
```

## 8. Project Context Schema (`project-context.md`)

```yaml
---
project-name: string
version: string
team-size: integer
created: string                 # ISO 8601
last-updated: string            # ISO 8601
---
```

Required sections (H2 headings):
- `## Vision` — What the project achieves and why
- `## Tech Stack` — Languages, frameworks, databases, infrastructure
- `## Constraints` — Budget, timeline, regulatory, technical limitations
- `## Conventions` — Code style, naming, branching, commit messages
- `## Team` — Roles, responsibilities, communication channels
- `## Links` — Repos, docs, dashboards, external resources

## 9. Gate Result Schema

```json
{
  "gate": "implementation-readiness",
  "date": "ISO 8601",
  "result": "PASS | CONCERNS | FAIL",
  "checks": [
    {
      "step": 1,
      "name": "PRD completeness",
      "status": "pass | warn | fail",
      "evidence": "Description of what was found",
      "severity": "critical | warning | info"
    }
  ],
  "summary": {
    "total": 13,
    "passed": 11,
    "warnings": 1,
    "failed": 1
  },
  "recommendation": "Free text recommendation"
}
```

## 10. Config Schema (`.bmad/config.yaml`)

```yaml
bmad:
  version: string               # BMAD version
  module: string                # Module name (default: "bmm")

project:
  name: string
  type: enum                    # greenfield | brownfield
  communication-language: string # en | es | pt | etc.

paths:
  planning-artifacts: string    # Default: planning_artifacts/
  architecture: string          # Default: architecture/
  epics: string                 # Default: epics/
  stories: string               # Default: stories/
  sprints: string               # Default: sprints/
  project-knowledge: string     # Default: project-knowledge/

user:
  name: string
  role: string
```

---

## Schema Migration Guide

**[R39]** When a schema changes, follow this migration protocol:

| Change Type | Migration Action | Backwards Compatible? |
|-------------|-----------------|----------------------|
| New optional field added | No migration needed. Existing artifacts remain valid. | Yes |
| New required field added | Add field with default value to all existing artifacts. | No — requires migration script |
| Field renamed | Update all artifacts. Keep old field as alias for 1 sprint. | No — requires migration |
| Field removed | Remove from schema. Existing artifacts with the field remain valid (ignored). | Yes |
| Enum value added | No migration needed. Existing values remain valid. | Yes |
| Enum value removed | Update all artifacts using the removed value. | No — requires migration |
| Validation rule tightened | Audit all artifacts against new rule. Fix violations. | No — requires audit |

### Backwards Compatibility Rules

**[R40]** Schema changes must follow these rules:
1. PATCH version changes (1.0.x) must be backwards compatible (no migrations required)
2. MINOR version changes (1.x.0) may add required fields with defaults. Migration script must be provided.
3. MAJOR version changes (x.0.0) may break backwards compatibility. Full migration guide must be provided.
4. All schema changes must be documented in a changelog with before/after examples.

### Schema Validation Automation

Recommended CI integration:
```
Pre-commit hook:
  1. Parse all .agent.yaml files → validate against Agent Definition Schema
  2. Parse all story frontmatter → validate against User Story Schema
  3. Parse sprint-status.yaml → validate against Sprint Status Schema
  4. Report violations as errors (block commit)
```

---

## Assumptions

- YAML is the primary schema format for BMAD artifacts (JSON is accepted for gate results only)
- Validation tooling can parse YAML frontmatter from markdown files
- Schema versions are tracked alongside BMAD methodology versions

## Limits

- These schemas define structure, not content quality — a valid schema does not guarantee a good PRD
- Schemas do NOT enforce cross-artifact consistency (e.g., FR references in stories matching actual PRD FRs) — that requires the traceability matrix
- Custom fields added by teams (per `references/customization-guide.md`) are not covered by these schemas

## Edge Cases

- **Artifact predates the current schema version**: Run the migration script for each version gap. If no migration script exists, manually add required fields with reasonable defaults and document the migration.
- **Team uses JSON instead of YAML**: Convert to YAML for BMAD artifact storage. JSON is acceptable only for gate result files and CI integration outputs.
- **Schema validation blocks a commit but the artifact is intentionally non-standard**: Document the deviation in `.bmad/customizations.yaml` per `references/customization-guide.md`. Add a schema validation exception for the specific field/file.

## Acceptance Criteria

- [ ] All artifact schemas in this document have explicit required/optional annotations on every field
- [ ] Validation rules are specific enough to implement in a CI script (regex, ranges, enum values)
- [ ] Migration guide exists for every backwards-incompatible schema change
- [ ] Schema version is tracked and incremented on every change

See also: `references/agent-as-code.md`, `references/artifact-flow-chain.md`, `references/customization-guide.md`
