# Progressive Context Engineering for BMAD

## Table of Contents
- [Why Context Management Matters](#why-context-management-matters)
- [Token Budget Considerations](#token-budget-considerations)
- [What to Load Per Phase](#what-to-load-per-phase)
- [Lazy Loading Patterns](#lazy-loading-patterns)
- [Summarize vs Load Full](#summarize-vs-load-full)
- [Session Planning for Multi-Phase Work](#session-planning-for-multi-phase-work)
- [Context Window Optimization](#context-window-optimization)
- [The project-context.md Always-Load Principle](#the-project-contextmd-always-load-principle)
- [HALT Commands in Step Files](#halt-commands-in-step-files)
- [Avoiding Context Pollution](#avoiding-context-pollution)

---

## Why Context Management Matters

AI agents operate within fixed context windows. Every token spent on irrelevant information is a token unavailable for reasoning, generation, and verification. In BMAD, where agents move through distinct phases with different artifact needs, naive context loading (dumping everything at once) produces measurably worse outputs.

**The problem in practice**: A developer agent implementing a single story does not need the full PRD, the complete architecture document, the risk register, and all 30 stories. Loading all of that leaves less room for the actual code it needs to write and review. Worse, conflicting details across artifacts can confuse the agent into generating inconsistent code.

**BMAD's solution**: Progressive context — load only what the current phase, agent, and task require. Build context incrementally. Summarize what is not immediately needed but may be referenced.

## Token Budget Considerations

Context windows vary by model, but the principles are constant:

| Model Class | Typical Window | Usable for BMAD Work |
|-------------|---------------|---------------------|
| 128K tokens | ~96K words | ~60K after system prompt + agent persona |
| 200K tokens | ~150K words | ~120K usable |
| 1M tokens | ~750K words | ~700K usable |

**[R25]** Reserve 30% of usable context for the agent's output and reasoning. The remaining 70% is your loading budget.

### Token Budget Calculator

Use this formula to plan context loading:

```
Available budget = (Model context window) x 0.7 x 0.7
                 = Model window x 0.49

Example (128K model):
  Available = 128,000 x 0.49 = ~62,700 tokens for input artifacts

Artifact sizes (typical):
  project-context.md:  500-2,000 tokens
  PRD:                 3,000-5,000 tokens
  Architecture doc:    5,000-10,000 tokens
  Single story:        500-1,000 tokens
  API contract:        1,000-3,000 tokens
  Data model:          1,000-2,000 tokens

Phase 4 example budget (128K model, 62.7K available):
  project-context.md:    1,500 tokens
  Current story:         800 tokens
  Architecture section:  2,000 tokens
  API contract section:  1,500 tokens
  Data model section:    1,000 tokens
  ─────────────────────────────────
  Total loaded:          6,800 tokens (11% of budget — comfortable)
```

**Warning**: Larger context windows do not mean you must load more. Research consistently shows that information in the middle of long contexts receives less attention. Keep critical information near the beginning or end of the loaded context.

### Context Priority Ranking

**[R26]** When context budget is tight, load in this priority order (drop from the bottom first):

1. **project-context.md** (always load — never drop)
2. **Current task specification** (story file, rapid spec, or workflow step)
3. **Directly relevant artifact sections** (API contract for the endpoint being built, data model for the entity being created)
4. **Dependency interfaces** (acceptance criteria of blocking stories)
5. **Full upstream artifacts** (complete architecture doc, full PRD)
6. **Adjacent context** (other stories in the same epic, related ADRs)
7. **Historical context** (previous sprint retrospectives, resolved open questions)

## What to Load Per Phase

This table defines the minimum and maximum context loading per BMAD phase:

| Phase | Always Load | Load on Demand | Never Load |
|-------|-------------|----------------|------------|
| **Phase 1: Product Definition** | project-context.md, product brief | Market research, competitor analysis | Architecture docs, story files, code |
| **Phase 2: Architecture** | project-context.md, PRD, tech stack | NFR details, integration specs | Story files, test files, code |
| **Phase 3: Planning** | project-context.md, PRD summary, architecture summary, story template | Full PRD (for specific requirement), full architecture (for specific component) | Code, deployment configs |
| **Phase 4: Implementation** | project-context.md, current story, relevant architecture section, API contracts for current story | Adjacent story (for dependency), data model (for DB work), security spec (for auth work) | Full PRD, risk register, all other stories |

**Key insight**: Each phase has a "never load" column. Respecting it is as important as filling the "always load" column.

## Lazy Loading Patterns

Lazy loading means deferring artifact loading until the agent explicitly needs it. BMAD supports this through step file instructions and agent menu commands.

### Pattern 1: Reference-Then-Load

The agent starts with a summary of an artifact. When it encounters a question that the summary cannot answer, it loads the full document.

```
Step instruction: "Review the architecture summary in project-context.md.
If you need component-level detail for the auth service, load
docs/architecture.md sections 3.1-3.4."
```

### Pattern 2: Story-Scoped Loading

For Phase 4, load only artifacts relevant to the current story:

```
For story S-007 (User Authentication):
  Load: S-007.md, architecture.md#auth-service, api-contracts.md#auth-endpoints
  Do not load: S-001 through S-006, S-008 through S-014
```

### Pattern 3: Section Loading

Large documents should be loadable by section rather than in full:

```
Load architecture.md#data-layer    (just the database section)
Load prd.md#nfr                    (just non-functional requirements)
```

This requires documents to have clear heading structure, which BMAD templates enforce.

### Pattern 4: Dependency Chain Loading

When a story depends on another, load only the interface contract of the dependency, not its full implementation:

```
S-007 depends on S-001 (auth).
Load: S-001's acceptance criteria (the contract)
Do not load: S-001's implementation notes or code
```

## Summarize vs Load Full

The decision to summarize or load the full document depends on the task:

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Agent needs to verify a specific requirement | Load full section | Summaries may omit the exact detail needed |
| Agent needs general awareness of project scope | Summarize | The overview is sufficient; details would be noise |
| Agent is writing code for a specific API | Load full API contract | Every field, status code, and validation rule matters |
| Agent is reviewing cross-cutting concerns | Summarize each concern | Need breadth, not depth |
| Agent is generating a new artifact (e.g., story from PRD) | Load full source | The output quality depends on complete input |

**The summarization rule**: If the agent will make a decision based on the content, load the full relevant section. If the agent only needs to know the content exists, a summary suffices.

**How to create summaries**: BMAD's project-context.md serves as the canonical summary layer. It contains condensed versions of all key artifacts. Agents load project-context.md first and then selectively load full documents as needed.

## Session Planning for Multi-Phase Work

When work spans multiple phases (common in solo-developer BMAD), plan your sessions to minimize context switching:

### Single-Phase Sessions (Recommended)

Each session focuses on one phase. Context is loaded once and used throughout.

```
Session 1: Phase 1 — Product definition
  Load: project-context.md, product brief, market data
  Output: PRD draft

Session 2: Phase 1 — PRD refinement
  Load: project-context.md, PRD draft, stakeholder feedback
  Output: Final PRD

Session 3: Phase 2 — Architecture
  Load: project-context.md, PRD (full), tech preferences
  Output: Architecture document, tech stack
```

### Cross-Phase Sessions (When Necessary)

Sometimes you need to jump phases (e.g., a Phase 4 implementation reveals a Phase 2 architecture gap). Plan the context transition:

```
1. Complete current task and commit artifacts
2. Clear the agent's context (new session or explicit reset)
3. Load the new phase's required context
4. Address the issue in the correct phase
5. Return to the original phase with updated artifacts
```

**Never try to hold both phases in context simultaneously.** The conflicting levels of detail will degrade output quality.

## Context Window Optimization

### Technique 1: Front-Load Critical Information

Place the most important context at the beginning of the loaded content. System prompts and project-context.md go first. The current task specification goes immediately after.

### Technique 2: Use Structured References

Instead of embedding full content, use structured references that the agent can follow:

```markdown
## Current Task
Implement story S-007 (User Authentication).

## References (load if needed)
- Architecture auth section: docs/architecture.md#authentication
- API contract: docs/api-contracts.md#post-auth-login
- Data model: docs/data-model.md#user-entity
```

### Technique 3: Prune Completed Context

Once a step in a workflow is complete, its context can be released. If step 1 generates an output that step 2 consumes, step 2 does not need step 1's input — only step 1's output.

### Technique 4: Version-Pin Context

Always load artifacts from a specific Git commit, not "latest." This prevents context drift mid-session where an artifact changes after being loaded.

## The project-context.md Always-Load Principle

`project-context.md` is the single document loaded in every BMAD session regardless of phase, agent, or task. It serves as the shared memory across all agents and sessions.

**Contents of project-context.md**:
- Project name and one-line description
- Current phase and status
- Technology stack summary
- Architecture overview (component list with one-line descriptions)
- Key decisions log (numbered, with rationale)
- Current sprint/iteration scope
- Links to all major artifacts (PRD, architecture, stories)

**Why it is always loaded**:
1. It provides orientation — any agent can understand the project in 30 seconds.
2. It prevents contradictions — the decisions log is the tie-breaker for conflicts.
3. It enables context recovery — a new session can resume work from this file alone.

**Maintenance rule**: project-context.md is updated at the end of every phase transition and every significant decision. It is never more than one session behind current state.

**Size constraint**: project-context.md should stay under 2K tokens. If it exceeds this, break out detail into linked documents and keep only summaries in the main file.

## HALT Commands in Step Files

BMAD workflow step files can include HALT directives that pause the agent and prompt the user to make a decision or provide additional context before proceeding.

**Purpose**: HALT prevents an agent from proceeding with assumptions when human judgment is required.

**Syntax in step files**:
```markdown
## Step 3: Validate Requirements

Review each functional requirement for completeness.

<!-- HALT: Ask the user to confirm the priority ranking before proceeding
     to story decomposition. Do not assume priority from the PRD alone. -->
```

**When to use HALT**:
- Before irreversible decisions (architecture choices, technology selection)
- When the agent lacks information it cannot infer (business priorities, budget constraints)
- At phase boundaries before loading new context
- When a validation step finds ambiguity that requires human resolution

**When NOT to use HALT**:
- For routine transformations (PRD section to story mapping)
- When the step file provides all necessary information
- For formatting or structural decisions the agent can make independently

**Context implication**: A HALT is also a natural context checkpoint. The agent can release pre-HALT context and load post-HALT context after the user responds, keeping the window fresh.

## Avoiding Context Pollution

Context pollution occurs when irrelevant, outdated, or contradictory information enters the context window and degrades output quality.

### Source 1: Stale Artifacts

Loading a PRD from three iterations ago alongside the current architecture causes contradictions.

**Prevention**: Always load from the latest committed version. Use Git refs, not file paths, when specifying which version to load.

### Source 2: Cross-Story Bleed

When implementing story S-007, loading stories S-001 through S-014 "for reference" introduces details that the agent will try to reconcile with S-007, wasting reasoning capacity.

**Prevention**: Load only the current story and its direct dependency interfaces. If the agent asks about another story, load that specific story on demand.

### Source 3: Conversational Debris

Long chat sessions accumulate messages that are no longer relevant. The agent processes all of them on every turn.

**Prevention**: Start new sessions for new tasks. Use session boundaries aligned with workflow steps. When a session exceeds 50 turns, consider starting fresh with a context summary.

### Source 4: Template Boilerplate

Loading full templates with all their instructions when the agent only needs to fill in one section wastes context on meta-instructions.

**Prevention**: Load only the relevant template section, or load the template with completed sections stripped out.

### Source 5: Duplicate Information

The same fact stated in the PRD, the architecture doc, and the story creates redundancy that consumes tokens without adding information.

**Prevention**: Use project-context.md as the single source of truth for shared facts. Other documents reference it rather than duplicating it. When loading multiple documents, deduplicate overlapping sections.

---

## What to Do When Context Exceeds the Window

**[R27]** When total required context exceeds the available budget:

| Step | Action |
|------|--------|
| 1 | Drop items from priority level 7, then 6, then 5 (see Context Priority Ranking) |
| 2 | Replace full documents with section-level loads (e.g., `architecture.md#auth-service` instead of full doc) |
| 3 | Summarize upstream artifacts instead of loading them fully (PRD summary instead of full PRD) |
| 4 | Split the task into subtasks that each fit within context (e.g., implement API handler in one session, write tests in another) |
| 5 | If still over budget after steps 1-4, the task is too large for a single agent session — decompose into smaller stories |

**Anti-pattern**: Never truncate an artifact mid-section to fit the budget. Either load the full section or summarize it — partial sections cause hallucinations.

## Assumptions

- AI models used with BMAD support at least 128K token context windows
- project-context.md is maintained under 2K tokens as specified in the project context guide
- Artifacts use clear heading structure (H2 sections) to enable section-level loading

## Limits

- This document does NOT prescribe how to implement context loading programmatically — that depends on the AI platform
- This document does NOT cover fine-tuning or retrieval-augmented generation (RAG) approaches
- Token counts are approximate — actual tokenization varies by model

## Acceptance Criteria

- [ ] Each agent session loads only the artifacts specified in the "What to Load Per Phase" table
- [ ] project-context.md is loaded in every session (always-load principle verified)
- [ ] No session loads artifacts from the "Never Load" column for its phase
- [ ] Context budget calculation has been performed for the target model before the first sprint

See also: `references/project-context-guide.md`, `references/methodology-overview.md`, `references/phase-4-implementation.md`
