# BMAD Method — Methodology Overview

## Table of Contents
- [What is BMAD](#what-is-bmad)
- [Core Principles](#core-principles)
- [The 4-Phase Model](#the-4-phase-model)
- [Documentation-First Architecture](#documentation-first-architecture)
- [Agent-as-Code Paradigm](#agent-as-code-paradigm)
- [Progressive Context Engineering](#progressive-context-engineering)
- [Comparison to Other Methodologies](#comparison-to-other-methodologies)
- [Anti-Patterns](#anti-patterns)
- [Glossary](#glossary)

---

## What is BMAD

BMAD (Breakthrough Method for Agile AI-Driven Development) is an open-source framework that transforms AI-assisted development from ad-hoc prompting into a structured, auditable, multi-agent process. Created by BMad Code, it overlays agile methodology principles with AI agent orchestration and Git-based artifact versioning.

**Key insight**: Software is a logical construction requiring human judgment for correctness. BMAD positions AI agents as disciplined collaborators operating within versioned constraints — not black-box code generators.

**Version**: v6-alpha (current) with 34+ workflows, 8 specialized agents, and progressive context-engineering.

## Core Principles

### 1. Documentation-First
Source code is a downstream derivative. The source of truth is the artifact chain: Product Brief → PRD → Architecture → Stories → Code. When AI has a spec to follow, hallucinations decrease dramatically.

### 2. Agent Specialization
Each agent embodies a specific role with defined expertise, communication style, and constraints. No single agent does everything. This creates multi-perspective review that prevents isolated decision-making.

### 3. Progressive Context
AI agents receive only the context relevant to their current phase and task. Context is built incrementally across phases, not dumped all at once. This reduces noise and improves output quality.

### 4. Gate-Based Advancement
Phases are separated by mandatory gates. The Implementation Readiness gate (13 checks) prevents premature coding. You cannot proceed to Phase 4 without passing the gate.

### 5. Git-Based Accountability
Every artifact — human or AI-generated — is version-controlled. This creates an auditable trail for compliance, debugging, and knowledge transfer.

### 6. Constrained Generation
Before AI generates code, developers establish explicit constraints via project-context.md and story files: designated libraries, performance requirements, code exclusion zones. AI operates within guardrails, not in open-ended space.

## The 4-Phase Model

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Phase 1       │    │   Phase 2       │    │   Phase 3       │    │   Phase 4       │
│   ANALYSIS      │───→│   PLANNING      │───→│   SOLUTIONING   │───→│ IMPLEMENTATION  │
│                 │    │                 │    │                 │    │                 │
│ Agent: Mary     │    │ Agents: John,   │    │ Agents: Winston,│    │ Agents: Amelia, │
│ (Analyst)       │    │ Sally (PM, UX)  │    │ Bob (Arch, SM)  │    │ Quinn (Dev, QA) │
│                 │    │                 │    │                 │    │                 │
│ Output:         │    │ Output:         │    │ Output:         │    │ Output:         │
│ product-brief   │    │ PRD, ux-spec    │    │ architecture,   │    │ Code, tests,    │
│                 │    │                 │    │ epics, stories  │    │ sprint-status   │
└─────────────────┘    └─────────────────┘    └────────┬────────┘    └─────────────────┘
                                                       │
                                               ┌───────┴───────┐
                                               │  READINESS    │
                                               │  GATE (13     │
                                               │  checks)      │
                                               │  PASS/FAIL    │
                                               └───────────────┘
```

### Phase 1: Analysis (Optional)
- **Purpose**: Explore and validate before committing resources
- **Activities**: Brainstorming, domain research, market analysis, competitive intelligence
- **Key artifact**: `product-brief.md`
- **Skip when**: Problem is well-understood, internal tool, or quick flow

### Phase 2: Planning
- **Purpose**: Define what to build, for whom, and why
- **Activities**: PRD creation, UX design, persona mapping, success metrics
- **Key artifacts**: `PRD.md`, `ux-spec.md`
- **Critical**: Requirements must be measurable and SMART

### Phase 3: Solutioning
- **Purpose**: Decide how to build it and verify readiness
- **Activities**: Architecture design, ADRs, epic decomposition, story writing, gate review
- **Key artifacts**: `architecture.md`, `epics/*.md`, `stories/*.md`
- **Gate**: Implementation Readiness (13-step) must pass before Phase 4

### Phase 4: Implementation
- **Purpose**: Build incrementally with continuous validation
- **Activities**: Sprint planning, story development, code review, testing, retrospective
- **Key artifacts**: Working code, `sprint-status.yaml`, test results
- **Cycle**: Plan → Develop → Review → Retro (repeats per sprint)

## Documentation-First Architecture

Traditional flow: Prompt → Code → (maybe) Documentation
BMAD flow: Brief → PRD → Architecture → Stories → Code → (auto) Documentation

**Why this matters**:
1. **Reduced hallucinations**: AI generates within constraints, not imagination
2. **Traceability**: Every line of code traces back to a requirement
3. **Reviewability**: Stakeholders review specs before code exists
4. **Replayability**: If AI generates bad code, regenerate from the same spec
5. **Compliance**: Versioned artifacts create audit trail automatically

## Agent-as-Code Paradigm

Agents are not chat personas — they are versioned, structured YAML definitions:

```yaml
metadata:
  id: analyst
  name: Mary
  icon: 🔬
persona:
  role: Business Analyst & Research Specialist
  identity: Methodical researcher who validates assumptions with data
  communication_style: Analytical, evidence-based, asks probing questions
  principles:
    - Always validate assumptions with data
    - Question what seems obvious
    - Present findings with confidence levels
menu:
  - trigger: "BR"
    description: Brainstorm
    workflow: workflows/1-analysis/brainstorm/
  - trigger: "PB"
    description: Create Product Brief
    workflow: workflows/1-analysis/create-product-brief/
```

**Benefits**:
- Agents are version-controlled like code
- Personas are consistent across sessions
- New agents can be created by copying/modifying existing ones
- Agent behavior is auditable and reviewable

## Progressive Context Engineering

BMAD manages AI context windows carefully:

| Phase | Context loaded | Why |
|-------|---------------|-----|
| 1 | project-context.md only | Minimal context for open exploration |
| 2 | + product-brief.md | Brief constrains PRD scope |
| 3 | + PRD.md, ux-spec.md | Requirements constrain architecture |
| 4 | + architecture.md, story file | Full context for focused implementation |

**Rules**:
- Load only what the current phase needs
- Each phase's output becomes permanent context for downstream phases
- project-context.md is always loaded (it's the constitution)
- Story files provide focused, complete context per implementation unit

## Comparison to Other Methodologies

| Dimension | Scrum | SAFe | Waterfall | BMAD |
|-----------|-------|------|-----------|------|
| AI-native | No | No | No | **Yes** |
| Agent specialization | No | No | No | **8 agents** |
| Documentation-first | Sometimes | Yes | Yes | **Mandatory** |
| Phase gates | Sprint review | PI planning | Phase gates | **13-step gate** |
| Context engineering | N/A | N/A | N/A | **Progressive** |
| Artifact versioning | Optional | Recommended | Required | **Git-native** |
| Adaptability | High | Medium | Low | **High** |
| Quick flow bypass | N/A | N/A | N/A | **Barry agent** |

**BMAD is not a replacement for Scrum/SAFe** — it is a layer that makes AI agents work within agile principles. You can run BMAD sprints inside SAFe PIs or Scrum ceremonies.

### Decision Tree: Should I Use BMAD?

```
Is AI involved in your development workflow?
├── NO → BMAD adds overhead without core benefit. Use standard agile.
└── YES → Are you building more than a throwaway prototype?
          ├── NO → Use Quick Flow only (see references/quick-flow.md)
          └── YES → Do you have compliance or audit requirements?
                    ├── YES → Full BMAD with enterprise governance (see references/enterprise-governance.md)
                    └── NO → Is team size > 1?
                              ├── YES → Full BMAD (4-phase)
                              └── NO → BMAD Lite: Phase 3-4 + Quick Flow for small changes
```

### Comparison Metrics

| Metric | Without BMAD (ad-hoc AI) | With BMAD | Measurement Method |
|--------|--------------------------|-----------|-------------------|
| Requirement-to-code traceability | ~10-20% | >95% | Traceability matrix audit |
| AI hallucination rate in generated code | 30-50% of outputs need correction | <10% with constrained generation | Code review rejection rate |
| Onboarding time for new team member | Days to weeks | Hours (read project-context.md) | Time to first merged PR |
| Post-implementation rework | 25-40% of stories | <10% after gate adoption | Stories requiring re-implementation |
| Audit preparation time | Days of manual collection | Minutes (artifacts already in Git) | Hours spent per audit cycle |

### Version Compatibility

| BMAD Version | Status | Key Changes | Migration Notes |
|-------------|--------|-------------|-----------------|
| v6-alpha | **Current** | 34+ workflows, 8 agents, progressive context | Active development |
| v5 | Deprecated | Earlier agent definitions, fewer workflows | Migrate agent YAML to v6 schema |

**[R1]** BMAD v6-alpha is the only supported version. All references in this document target v6-alpha.

## Anti-Patterns

| Anti-Pattern | Problem | BMAD Solution |
|-------------|---------|---------------|
| Prompt-and-pray | No spec, AI hallucinates | Documentation-first chain |
| God agent | One agent does everything | 8 specialized agents |
| Context dumping | Load everything into prompt | Progressive context loading |
| Skip to code | No architecture, stories diverge | Mandatory readiness gate |
| Orphan stories | Stories don't trace to requirements | Artifact flow validation |
| Stale context | project-context.md outdated | Living document pattern |
| Gate theater | Gate exists but never fails | 13-step automated validation |

## Glossary

| Term | Definition |
|------|-----------|
| **ADR** | Architecture Decision Record — documents a significant technical decision |
| **Agent-as-Code** | Defining AI agent personas as versioned YAML files |
| **Artifact flow** | The chain of documents where each phase's output feeds the next |
| **Barry (Quick Flow)** | Agent that bypasses phases 1-3 for small changes |
| **Brownfield** | Applying BMAD to an existing codebase |
| **Control manifest** | Developer-defined constraints before AI code generation |
| **FR** | Functional Requirement |
| **Gate** | Mandatory checkpoint between phases (especially Phase 3→4) |
| **Greenfield** | Starting a new project from scratch with BMAD |
| **HALT** | Command in step files preventing AI read-ahead |
| **IR** | Implementation Readiness — the 13-step gate |
| **NFR** | Non-Functional Requirement |
| **PRD** | Product Requirements Document |
| **Progressive context** | Loading only phase-relevant context into AI prompts |
| **project-context.md** | The project's constitution — rules, conventions, stack |
| **Sharded steps** | Workflows broken into individual step files for sequential execution |
| **Sprint-status.yaml** | YAML file tracking story progress within a sprint |
| **Story** | Implementable unit of work with acceptance criteria (Given/When/Then) |

---

## Assumptions

- [R2] AI models used with BMAD support at least 128K token context windows
- [R3] The team uses Git (or compatible VCS) for all artifact storage
- [R4] At least one team member understands agile fundamentals (sprints, stories, acceptance criteria)
- [R5] AI agents are used as collaborators, not autonomous decision-makers — human review is mandatory at gates

## Limits

- This document does NOT cover AI model selection, prompt engineering techniques, or LLM fine-tuning
- This document does NOT prescribe specific programming languages, frameworks, or cloud providers
- This document does NOT replace domain-specific compliance frameworks (SOC2, HIPAA) — see `references/enterprise-governance.md`
- Cost estimation and pricing are explicitly out of scope for all BMAD documentation

## Acceptance Criteria

- [ ] Reader can explain BMAD's 4-phase model and name each phase's primary agent
- [ ] Reader can articulate why documentation-first reduces AI hallucinations
- [ ] Reader can decide whether BMAD applies to their project using the decision tree
- [ ] Reader can distinguish BMAD from Scrum/SAFe (layer vs replacement)

See also: `references/phase-1-analysis.md`, `references/phase-2-planning.md`, `references/phase-3-solutioning.md`, `references/phase-4-implementation.md`, `references/quick-flow.md`
