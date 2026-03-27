# Agent-as-Code Specification

## Table of Contents
- [Overview](#overview)
- [Agent YAML Format](#agent-yaml-format)
- [Persona Design Principles](#persona-design-principles)
- [Communication Style Guidelines](#communication-style-guidelines)
- [Menu and Workflow Binding](#menu-and-workflow-binding)
- [Agent Compilation](#agent-compilation)
- [Creating Custom Agents](#creating-custom-agents)
- [Agent Composition Patterns](#agent-composition-patterns)
- [Versioning Agents with Git](#versioning-agents-with-git)
- [Best Practices](#best-practices)

---

## Overview

Agent-as-Code is the BMAD paradigm where AI agent definitions are stored as version-controlled YAML files rather than ephemeral prompt configurations. This makes agents:

- **Reproducible**: Same YAML produces the same agent behavior across sessions
- **Auditable**: Changes to agent behavior are tracked in Git history
- **Composable**: Agents can share traits, workflows, and menu items
- **Testable**: Agent definitions can be validated against schemas before deployment

The canonical format is `.agent.yaml`, which compiles to `.agent.md` for consumption by AI systems that prefer markdown prompts.

---

## Agent YAML Format

### Complete Field Reference

```yaml
# ═══════════════════════════════════════
# METADATA — Required
# ═══════════════════════════════════════
metadata:
  id: string              # Unique kebab-case identifier (e.g., "product-manager")
  name: string            # Human-readable display name (e.g., "Product Manager")
  icon: string            # Single emoji representing the agent (e.g., "📋")
  module: string          # Module this agent belongs to (e.g., "bmm")
  version: string         # Semantic version (e.g., "1.0.0") — optional but recommended
  description: string     # One-line purpose statement — optional

# ═══════════════════════════════════════
# PERSONA — Required
# ═══════════════════════════════════════
persona:
  role: string            # Professional title (e.g., "Senior Product Manager")
  identity: string        # Multi-sentence background narrative describing expertise,
                          # personality traits, and working philosophy.
  communication_style: string
                          # How the agent communicates: tone, verbosity, format preferences.
  principles:             # Core beliefs that guide decision-making (1-5 items)
    - string              # (e.g., "Requirements must be testable and traceable")
    - string

# ═══════════════════════════════════════
# MENU — Required (at least 1 entry)
# ═══════════════════════════════════════
menu:
  - trigger: string       # 2-letter uppercase shorthand (e.g., "WP" for "Write PRD")
    description: string   # Display name shown in the menu (e.g., "Write PRD")
    workflow: string      # Relative path to workflow file
                          # (e.g., "workflows/write-prd/step-01-gather.md")

# ═══════════════════════════════════════
# PROMPTS — Optional
# ═══════════════════════════════════════
prompts:
  system: string          # System prompt injected when the agent is activated.
                          # Used for global instructions that apply to all workflows.
  greeting: string        # Initial message when the agent is first invoked — optional.

# ═══════════════════════════════════════
# CONTEXT — Optional
# ═══════════════════════════════════════
context:
  required_files:         # Files the agent needs loaded into context
    - string              # (e.g., "project-context.md", "prd.md")
  optional_files:         # Files that enhance agent performance if available
    - string

# ═══════════════════════════════════════
# CONSTRAINTS — Optional
# ═══════════════════════════════════════
constraints:
  allowed_tools:          # Tools this agent is permitted to use
    - string              # (e.g., "read", "write", "search", "bash")
  forbidden_actions:      # Explicit prohibitions
    - string              # (e.g., "Do not modify architecture.md")
  output_format: string   # Default output format (e.g., "markdown", "yaml", "json")
```

### Minimal Valid Agent

```yaml
metadata:
  id: quick-fixer
  name: Quick Fixer
  icon: "🔧"
  module: bmm

persona:
  role: Bug Fix Specialist
  identity: A focused developer who fixes bugs quickly and cleanly.
  communication_style: Terse, code-focused, no unnecessary explanation.
  principles:
    - Fix the bug, not the symptom
    - Every fix includes a test

menu:
  - trigger: FX
    description: Fix Bug
    workflow: workflows/fix-bug/step-01-reproduce.md
```

---

## Persona Design Principles

### 1. Specificity Over Generality

Bad: "An experienced developer who knows many languages."
Good: "A backend specialist with 10 years of Python and PostgreSQL experience who obsesses over query performance and considers N+1 queries a personal affront."

Specific personas produce more consistent, predictable outputs.

### 2. Complementary Tensions

Design agents with deliberate tensions to create healthy conflict:
- The **Architect** values long-term maintainability; the **Developer** values shipping speed
- The **PM** advocates for user needs; the **Architect** advocates for technical constraints
- The **Analyst** explores broadly; the **PM** scopes narrowly

These tensions prevent groupthink in multi-agent workflows.

### 3. Bounded Expertise

Every agent should have explicit knowledge boundaries:
- What they are expert in (their domain)
- What they defer to other agents on
- What they refuse to do (constraints)

An agent that claims expertise in everything produces shallow outputs across the board.

### 4. Behavioral Consistency

The persona should produce predictable behavior patterns:
- Same input should produce structurally similar output across sessions
- Communication style should be recognizable without seeing the agent name
- Decision-making should follow stated principles

### 5. Personality Without Gimmicks

Personality makes agents distinctive and memorable. Gimmicks make them annoying.

Good personality: "Methodical, asks clarifying questions before acting, presents options as numbered lists."
Gimmick: "Always responds in rhyming couplets" or "Talks like a pirate."

---

## Communication Style Guidelines

### Style Dimensions

| Dimension | Spectrum | Example |
|-----------|----------|---------|
| **Verbosity** | Terse ↔ Detailed | "LGTM" vs "The approach is sound because..." |
| **Formality** | Casual ↔ Formal | "Let's do it" vs "I recommend proceeding with option A" |
| **Structure** | Freeform ↔ Structured | Prose paragraphs vs numbered lists and tables |
| **Confidence** | Hedging ↔ Assertive | "This might work" vs "This is the correct approach" |
| **Focus** | Broad ↔ Narrow | Considers context and alternatives vs laser-focused on the task |

### Agent Style Examples

**Analyst (Ana)**:
```
communication_style: >
  Exploratory and thorough. Presents findings as structured research reports.
  Uses evidence tags on every claim. Asks probing questions. Comfortable
  saying "I don't know yet" when research is incomplete. Prefers bullet
  points and tables over prose.
```

**Architect (Arch)**:
```
communication_style: >
  Precise and opinionated. Presents decisions with clear justification.
  Uses diagrams and code examples. Challenges assumptions directly but
  respectfully. Prefers structured formats: ADRs, numbered lists,
  comparison tables.
```

**Developer (Dev)**:
```
communication_style: >
  Code-forward and concise. Shows rather than tells. Provides working
  examples before lengthy explanations. Uses inline comments to explain
  non-obvious decisions. Prefers short paragraphs and code blocks.
```

---

## Menu and Workflow Binding

### Menu Design

The menu is the agent's command interface. Each menu entry binds a trigger to a workflow.

```yaml
menu:
  - trigger: WP
    description: Write PRD
    workflow: workflows/write-prd/step-01-gather.md
  - trigger: RP
    description: Review PRD
    workflow: workflows/review-prd/step-01-checklist.md
  - trigger: UP
    description: Update PRD
    workflow: workflows/update-prd/step-01-identify-changes.md
```

### Trigger Conventions

- Always 2 uppercase letters
- Mnemonic: first letters of the action (WP = Write PRD, RP = Review PRD)
- Unique within an agent (no duplicates)
- Try to be unique across agents in the same module (avoid collision)

### Workflow Files

Workflows are multi-step markdown files that guide the agent through a process:

```markdown
---
stepNumber: 1
stepName: Gather Requirements
agent: product-manager
inputs:
  - product-brief.md
outputs:
  - prd-draft.md
nextStep: step-02-structure.md
---

# Step 1: Gather Requirements

## Instructions
1. Read the product brief thoroughly
2. Extract all explicit requirements
3. Identify implicit requirements from the problem statement
4. List open questions that need resolution

## Output Format
Create a requirements list with FR-IDs in the standard format.

## Completion Criteria
- All brief sections have been reviewed
- At least 10 functional requirements identified
- Open questions documented
```

---

## Agent Compilation

### YAML to Markdown Compilation

The `.agent.yaml` file compiles to `.agent.md` for AI consumption. The compilation process:

1. **Header**: Agent name, icon, role from metadata
2. **System prompt**: From `prompts.system` (if present)
3. **Persona block**: Identity, communication style, principles formatted as prose
4. **Context requirements**: Listed files from `context` block
5. **Constraints**: Allowed tools and forbidden actions
6. **Menu**: Formatted as a command table
7. **Greeting**: From `prompts.greeting` (if present)

### Compiled Output Example

```markdown
# 📋 Product Manager

## System Prompt
You are the Product Manager agent in the BMAD framework...

## Persona
**Role**: Senior Product Manager

You are a detail-oriented product manager with 8 years of experience
translating business needs into precise technical requirements...

**Communication Style**: Structured and thorough. Uses numbered lists...

**Principles**:
1. Requirements must be testable and traceable
2. Scope boundaries prevent scope creep
3. User needs drive priorities, not technical preferences

## Context
**Required**: project-context.md, product-brief.md
**Optional**: personas/, ux-spec.md

## Constraints
**Allowed tools**: read, write, search
**Forbidden**: Do not modify architecture.md or story files

## Commands
| Trigger | Action |
|---------|--------|
| WP | Write PRD |
| RP | Review PRD |
| UP | Update PRD |
```

---

## Creating Custom Agents

### Step-by-Step Process

1. **Define the role**: What gap does this agent fill? What does no existing agent do well?
2. **Write the persona**: Start with role, then identity, then communication style, then principles
3. **Design the menu**: What are the 3-5 core actions this agent performs?
4. **Create workflows**: Write step files for each menu action
5. **Set constraints**: What should this agent explicitly not do?
6. **Test**: Run the agent through its workflows and verify output quality
7. **Iterate**: Refine persona and constraints based on output quality

### Custom Agent Checklist

- [ ] `metadata.id` is unique across all agents in the module
- [ ] `persona.identity` is at least 2 sentences
- [ ] `persona.principles` has 2-5 items
- [ ] Every menu trigger has a corresponding workflow file that exists
- [ ] Constraints are specific enough to prevent scope creep
- [ ] The agent has been tested on at least 2 representative tasks

---

## Agent Composition Patterns

### Pattern 1: Sequential Handoff

Agents work in sequence, each producing output consumed by the next.

```
Analyst → PM → Architect → Developer
  Brief → PRD → Architecture → Code
```

Each agent reads the upstream artifact and produces the downstream artifact.

### Pattern 2: Parallel Review

Multiple agents review the same artifact simultaneously, each from their expertise.

```
         ┌→ Architect (technical feasibility)
PRD ────→├→ Developer (implementability)
         └→ Analyst (requirement completeness)
```

Feedback is merged, and the PM resolves conflicts.

### Pattern 3: Specialized Delegation

A coordinator agent delegates subtasks to specialists.

```
PM (coordinator)
  ├→ Analyst: research competitive landscape
  ├→ Architect: assess technical feasibility
  └→ UX Designer: create wireframes
PM consolidates into PRD
```

### Pattern 4: Iterative Refinement

An agent's output is reviewed by another agent, and the cycle repeats until quality criteria are met.

```
Developer writes code → Reviewer reviews → Developer revises → Reviewer approves
```

---

## Versioning Agents with Git

### Version Strategy

- Agent YAML files live in the project repository alongside code
- Use semantic versioning in `metadata.version`
- Track changes to agent definitions in commit messages

### What to Version Control

| File | Version Control | Reason |
|------|----------------|--------|
| `.agent.yaml` | Yes | Source of truth for agent definition |
| `.agent.md` | Optional | Compiled output; can be regenerated |
| `workflows/*.md` | Yes | Agent behavior depends on workflow content |
| Test transcripts | Recommended | Evidence that agent produces correct output |

### Commit Message Convention

```
agent(product-manager): update persona to emphasize scope management

The PM agent was allowing scope creep during PRD writing.
Added a principle about scope boundaries and updated the
communication style to be more assertive about out-of-scope items.
```

---

## Best Practices

### 1. Keep Personas Focused
Each agent does one job well. If an agent's menu has more than 7 entries, consider splitting into two agents.

### 2. Write Constraints Explicitly
"Do not modify architecture files" is better than hoping the agent figures it out. Negative constraints prevent the most costly mistakes.

### 3. Test With Edge Cases
Run each agent through ambiguous inputs, incomplete information, and contradictory requirements. A robust persona handles these gracefully.

### 4. Document Interactions
When two agents interact, document the handoff protocol: what artifact is passed, what the receiving agent expects, and what happens if the artifact is incomplete.

### 5. Evolve, Do Not Rewrite
When an agent underperforms, adjust the persona or add a constraint. Avoid complete rewrites — incremental changes are easier to test and revert.

### 6. Use Evidence Tags in Agent Output
Agents should tag their claims just like humans: `[DATA]`, `[INFERENCE]`, `[ASSUMPTION]`. This is enforced through persona principles, not through tooling.

### 7. Separate Configuration From Behavior
The YAML defines WHAT the agent is. The workflow files define WHAT the agent does. Keep them separate — a persona change should not require workflow changes, and vice versa.

### 8. Review Agent Changes Like Code Changes
Agent definition changes must go through the same PR review process as code changes. A persona tweak can have outsized impact on downstream artifact quality.

---

## Agent Testing Strategy

### Test Levels

| Level | What to Test | Method | Frequency |
|-------|-------------|--------|-----------|
| Schema validation | YAML structure matches agent schema | Automated lint (CI) | Every commit |
| Persona consistency | Same input produces structurally similar output | Run 3 representative prompts, compare output structure | Every persona change |
| Workflow binding | Every menu trigger resolves to an existing workflow file | Automated file existence check | Every commit |
| Integration | Agent produces correct artifacts in a multi-agent handoff | End-to-end test on a sample project | Per release |

### Test Protocol for Persona Changes

1. Select 3 representative inputs that exercise the agent's core workflows
2. Run each input with the OLD persona and save outputs
3. Run each input with the NEW persona and save outputs
4. Compare: structural similarity must be >80%. If communication style changed intentionally, document the delta.
5. If output quality degrades on any input, revert the persona change

## Agent Versioning — Semver Rules

**[R11]** Agent definitions follow semantic versioning in `metadata.version`:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Fix typo in persona, update communication style nuance | PATCH (1.0.x) | 1.0.0 -> 1.0.1 |
| Add new menu item, add workflow, change principles | MINOR (1.x.0) | 1.0.1 -> 1.1.0 |
| Change agent role, rename agent, restructure persona fundamentally | MAJOR (x.0.0) | 1.1.0 -> 2.0.0 |

**[R12]** MAJOR version bumps require re-running the integration test suite. MINOR bumps require the persona consistency test. PATCH bumps require schema validation only.

## Agent Deprecation Process

When an agent is no longer needed:

1. Set `metadata.status: deprecated` in the agent YAML
2. Add `metadata.deprecated-date` and `metadata.successor` (if a replacement agent exists)
3. Keep the deprecated agent available for 2 sprints (grace period)
4. After the grace period, move the agent YAML to an `agents/archived/` directory
5. Update all workflow references that pointed to the deprecated agent

**[R13]** Never delete an agent definition — archive it. Git history alone is not sufficient because workflow files may reference agents by ID.

---

## Assumptions

- AI systems consuming compiled `.agent.md` files support markdown-based system prompts
- The team uses Git for version control of agent definitions alongside code
- At least one team member can review agent persona changes for quality impact

## Limits

- This specification does NOT cover multi-model agent routing (running different agents on different LLMs)
- This specification does NOT cover agent runtime infrastructure (how agents are invoked by the user)
- Agent-as-Code is a definition format, not an execution framework

## Edge Cases

- **Two agents need the same trigger code**: Triggers must be unique within a module. If collision occurs, the second agent must change its trigger. Document the conflict in the agent's YAML as a comment.
- **Agent persona produces inconsistent output across LLM providers**: Pin the LLM provider in `metadata.llm-hint` (advisory, not enforced). Adjust persona specificity — more specific personas produce more consistent output across providers.
- **Agent needs to call another agent**: Use the Sequential Handoff or Specialized Delegation patterns. An agent must NOT embed another agent's persona — it must reference the other agent by ID.

## Acceptance Criteria

- [ ] Agent YAML passes schema validation
- [ ] Every menu trigger maps to an existing workflow file
- [ ] `metadata.version` follows semver and is incremented on every change
- [ ] Persona consistency test passes for any persona modification
- [ ] Deprecated agents are archived, not deleted

See also: `references/methodology-overview.md`, `references/customization-guide.md`, `references/schemas.md`
