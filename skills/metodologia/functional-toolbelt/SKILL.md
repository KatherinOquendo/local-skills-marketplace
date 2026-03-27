---
name: metodologia-functional-toolbelt
author: Javier Montano · Comunidad MetodologIA
argument-hint: "[tool-name-or-number] [context]"
description: >
  Functional analysis toolkit with 6 tools for requirements engineering.
  Use when the user asks to "run event storming", "create a story map", "extract business rules",
  "write acceptance criteria", "build traceability matrix", "detect anti-patterns",
  or mentions "Given/When/Then", "functional toolbelt", "requirements quality".
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Functional Toolbelt

Mental models, techniques, and validation tools for producing better functional analysis. NOT a deliverable skill — a **toolbelt** that enhances output quality of any requirements or specification work.

## Grounding Guideline

**Tools do not produce quality — discipline in their use does.** The functional toolbelt is not a deliverable — it is a techniques kit that elevates the quality of any functional analysis work. Event storming without discipline is chaotic brainstorming. Acceptance criteria without structure is ambiguous prose.

### Toolbelt Philosophy

1. **Right technique for the context.** Event storming to discover domains, story mapping to plan releases, acceptance criteria to validate. Do not use a hammer for everything.
2. **Proportional formalism.** Critical business rules in pseudo-code. Simple rules in natural language. The level of formalism depends on severity.
3. **End-to-end traceability.** Every requirement has an origin (stakeholder, rule, flow) and a destination (test, acceptance criteria). Without traceability, requirements are loose declarations.

## $ARGUMENTS

```
$ARGUMENTS format: [tool-name-or-number] [context]
Examples:
  "event-storming loan-origination"     → Tool 1, domain=loan-origination
  "acceptance-criteria user-registration" → Tool 4, story=user-registration
  "anti-patterns scan requirements.md"   → Tool 6, input=requirements.md
  "3 business rules from interviews"     → Tool 3, source=interview notes
```

- If no tool specified → show 6-tool menu with one-line descriptions
- If tool specified without context → ask for the input artifact

### Pipeline Parameters

| Parameter | Values | Default | Effect |
|-----------|---------|---------|--------|
| `MODO` | `piloto-auto`, `desatendido`, `supervisado`, `paso-a-paso` | `piloto-auto` | Level of human intervention during tool execution |
| `FORMATO` | `markdown`, `html`, `dual` | `markdown` | Generated artifact output format |
| `VARIANTE` | `ejecutiva`, `tecnica` | `tecnica` | Executive (~40% content, visual summary) vs technical (full detail + matrices) |

- `MODO=paso-a-paso` → pauses after each tool output for review
- `FORMATO=html` → applies design-system tokens to output
- `VARIANTE=ejecutiva` → findings summary only, no detailed matrices

## Output Format Protocol

| FORMATO | Structure | Primary Use |
|---------|-----------|---------------|
| `markdown` | MD tables, code blocks for GWT, matrices in text | Wikis, repos, internal documentation |
| `html` | Styled with design-system tokens, responsive tables, callouts | Stakeholder presentations, formal deliverables |
| `dual` | Both generated; MD as source, HTML as render | When the team needs to edit (MD) and present (HTML) |

- Markdown always includes front-matter with metadata (tool used, domain, date)
- HTML applies brand-config.json if available

## Tool 1: Event Storming (Lightweight — 90 min)

**Inputs:** Domain actors, key processes
**Process:** Identify domain events (temporal markers) > Group by aggregate > Identify commands + actors > Surface policies/rules > Mark hot spots (unknowns)
**Output:** Event timeline > domain events > aggregates > bounded contexts

**Edge Cases:**
- Circular events (Order Placed > Payment > Order Placed): surface business rule preventing cycle
- God-aggregate (5+ events): signals context boundary issue — recommend splitting
- Missing actors (events without source): mark as hot spot requiring stakeholder clarification

**Trade-offs:** Speed (90 min) vs completeness (full domain modeling) — prioritize critical paths. Visual (sticky board) vs structured (spreadsheet) — visual aids creativity, spreadsheet aids traceability.

**Conditional Logic:**
- IF events unclear → trace 1 user journey end-to-end first
- IF no process flows exist → generate basic flow from stakeholder interviews
- IF aggregate boundaries disputed → document multiple hypotheses, defer to architecture team

---

## Tool 2: Story Mapping

**Process:** Extract user activities from flows > Decompose to tasks > Write user stories > Assign acceptance criteria > Plot backbone (activities, horizontal) vs detail (stories, vertical) > Slice into releases (MVP, phases 2-3)
**Output:** Backbone > Walking Skeleton (MVP) > Release Plan with story counts

**Edge Cases:**
- Epic masquerading as story (too large): split into 2-3 stories per variant
- Technical story without user value: reframe as infrastructure epic or reject
- Missing happy path: prioritize nominal flow in early release, edge cases later

**Trade-offs:** Granularity (tiny stories, many) vs manageability (fewer, less traceable) — target 8-13 stories per release. Detail (full AC now) vs speed (AC during sprint) — write basic AC now, refine during sprint planning.

**Conditional Logic:**
- IF multiple actors → separate story maps per actor, merge at integration points
- IF story > 13 points → decompose into 2 stories
- IF no metrics for priority → use business risk (revenue loss if not delivered) as proxy

---

## Tool 3: Business Rule Extraction

**Techniques:** Decision Table (conditions > actions > rows = rules), Decision Tree (condition > branches > leaf = outcome), Rule Catalog (name, classification, condition, action, exception, data, owner)

**Classification:** Constraint (what cannot happen), Derivation (what is calculated), Inference (what is deduced), Action-Enabling (what triggers a process)

**Validation:** Completeness (all condition combinations covered?), Consistency (no contradicting rules?), Necessity (traces to business objective?)

**Edge Cases:**
- Ambiguous conditions ("customer is qualified"): decompose into measurable sub-conditions
- Untestable actions ("notify relevant stakeholders"): specify exactly who, when, how
- Hidden exceptions: surface via stakeholder questioning

**Trade-offs:** Formality (decision tables) vs readability (narrative) — use both. Completeness (all rules) vs speed (80% important rules) — prioritize rules tied to business risk.

**Conditional Logic:**
- IF rule involves time → document temporal constraints
- IF rule has >5 conditions → decompose into sub-rules or decision tree
- IF rules conflict → document conflict, escalate to business stakeholder

---

## Tool 4: Acceptance Criteria (Given/When/Then)

**Pattern:** Given [precondition], When [action], Then [expected result]
**Variations:** Basic (single behavior), Extended (+And), Negative (Then = failure), Boundary (edge values)

**Quality Rules (Non-Negotiable):**
1. One behavior per scenario
2. Measurable outcomes (no "works correctly")
3. No implementation details (no "onClick handler fires")
4. Testable preconditions (specific values)
5. Use specific values ("income $75K" not "income")

**Anti-Patterns:** Vague Then ("handle appropriately"), Missing Given, Implementation leakage ("API endpoint called"), Untestable conditions ("under load" without metric), Conjunctive action (3 outcomes = 3 scenarios)

**Edge Cases:**
- Conditional actions (different Then per data): separate scenarios per condition
- Async outcomes: specify max acceptable delay in Then
- Third-party deps ("email delivered"): define acceptable failure mode

**Conditional Logic:**
- IF AC mentions external system → add "system unavailable" scenario
- IF scenarios > 8 per story → split across multiple stories
- IF AC references business rule → link back to rule catalog

---

## Tool 5: Traceability Matrix

**Structure:** Requirement ID | Requirement | Linked Use Cases | Linked Flows | Test Cases | AC Covered

**Validation Rules:**
1. Every requirement has >= 1 use case (else orphaned)
2. Every use case has >= 1 flow (else abstract)
3. Every flow has >= 1 test case (else untested)
4. Every test case traces to >= 1 AC (else invalid)

**Coverage Metrics:** % traced requirements, % untested flows, % AC without tests

**Gap Detection:** Requirements without UCs (disconnected), Flows without UCs (orphaned), Orphan test cases (no AC), AC without tests (unvalidated)

**Edge Cases:**
- Many-to-many (one flow covers multiple requirements): signals decomposition issue
- Matrix > 50 requirements: filter by domain or split
- Regulatory requirements: trace with 100% coverage rigor

**Conditional Logic:**
- IF regulatory → require 100% traceability coverage
- IF critical path flow → ensure >= 2 test cases (happy + error)
- IF gap found → assign to owner (requirements > product, flows > design, tests > QA)

---

## Tool 6: Anti-Pattern Detector

**Categories:**
1. **Ambiguity:** "handle appropriately" (no measurable outcome) → specify exact behavior
2. **Untestability:** "system should be user-friendly" (no metric) → provide measurable criteria
3. **Over-Specification:** "use MySQL 8.0.32" (how not what) → state requirement, let design choose
4. **Missing Exceptions:** "user logs in" (no failure path) → add negative scenarios
5. **Scope Creep:** Requirements not tracing to business objectives → defer or reject
6. **Gold Plating:** Features nobody asked for → require explicit business driver

**Detection Process:** Scan requirements (missing measurements) > Scan AC (implementation details, missing negatives) > Scan rules (untestable conditions) > Scan flows (missing error paths) > Cross-check traceability

**Edge Cases:**
- Intentional underspecification (innovation/exploration phase): mark as exploration story, exempt
- Phase-dependent strictness: lenient in early phases, strict at phase gates
- Regulatory over-specification ("must use FIPS 140-2"): document as compliance constraint, not anti-pattern

**Conditional Logic:**
- IF ambiguity in executive summary → escalate (high visibility)
- IF multiple anti-patterns in same requirement → likely incomplete understanding, request clarification
- IF severity = blocker (missing negative scenario on critical path) → must fix before phase exit

---

## Assumptions & Limits

- Toolbelt is reference, not prescriptive — projects adapt or skip tools based on context
- Tools 1-3 need domain expert input; async facilitation possible but slower
- Output quality depends on input quality — ensure upstream artifacts are solid
- Not a replacement for domain knowledge — surfaces structure, business logic expertise still required
- Event storming assumes access to at least one domain expert; pure documentation-based analysis is weaker
- Traceability matrix scales to ~200 requirements before tooling (Jira, Azure DevOps) becomes necessary
- GWT acceptance criteria assume BDD-aware team; teams unfamiliar with BDD need coaching first

## Edge Cases

| Scenario | Adaptation |
|----------|-----------|
| No domain expert available | Use existing documentation + anti-pattern detector to surface gaps; flag as risk |
| Legacy system with no documentation | Start with reverse event storming (trace from outputs back to events) |
| Regulatory domain (healthcare, finance) | Use full 6-tool suite; traceability matrix mandatory with 100% coverage |
| Agile team resisting formal AC | Start with Tool 4 only (GWT); demonstrate value before introducing full suite |
| Microservices with shared bounded contexts | Event storming per service, then cross-reference at integration points |
| Multi-language stakeholders | Standardize domain glossary first (Tool 3 extraction includes terminology) |

## Macro Trade-offs

| Dimension | Full Suite (6 tools) | Core Set (3-4 tools) | Decision Rule |
|-----------|---------------------|---------------------|---------------|
| Coverage | Robust requirements | Acceptable for low-risk | Use full suite for regulated/complex; core for standard |
| Depth vs breadth | Deep on 2 tools | Surface all 6 | Deep dive for complex domains; surface for known domains |
| Facilitation | In-person (high quality) | Async/tool-driven (scalable) | Hybrid recommended |
| Formalism | Decision tables + pseudo-code | Natural language rules | Pseudo-code for critical/financial rules; NL for UI/UX rules |

## Validation Gate

Before delivering toolbelt output, verify:
- [ ] Tool selection justified for project context
- [ ] Inputs identified and available (or gaps flagged)
- [ ] Edge cases for the selected tool explicitly addressed
- [ ] Output format matches downstream consumer needs
- [ ] Anti-patterns checked on own output (recursive quality)
- [ ] MODO/FORMATO/VARIANTE params respected in output
- [ ] Traceability links present (requirement origin → test destination)
- [ ] Domain glossary terms used consistently across all outputs

## Edge Cases

| Case | Handling Strategy |
|------|---------------------|
| No domain expert available for event storming or story mapping | Use existing documentation + anti-pattern detector to surface gaps; mark output as developer assumptions, not domain knowledge; flag as risk |
| Legacy system without any documentation | Start with reverse event storming (trace from outputs back to events); combine with Tool 6 anti-pattern detector to identify structural gaps |
| Regulated domain (healthcare, finance) requires 100% traceability | Use full 6-tool suite; traceability matrix mandatory with 100% coverage; every requirement traced from origin to test case |
| Agile team resists formalization of acceptance criteria | Start with Tool 4 (GWT) only; demonstrate value with concrete examples before introducing full suite; do not force simultaneous adoption |

## Decisions & Trade-offs

| Decision | Discarded Alternative | Justification |
|----------|----------------------|---------------|
| Design as toolbelt of 6 independent tools (not a sequential flow) | Mandatory sequential pipeline of all 6 tools | Projects adapt or skip tools based on context; forcing all 6 in sequence wastes effort on simple projects |
| Proportional formalism (pseudo-code for critical rules, natural language for simple rules) | Same level of formalism for all rules | Excessive formalism on simple rules generates overhead; insufficient formalism on critical rules generates ambiguity |
| GWT acceptance criteria with one-behavior-per-scenario rule | Allow multiple behaviors per GWT scenario | Multiple behaviors in one scenario make tests fragile and results ambiguous; one behavior = one scenario = one test |

## Knowledge Graph

```mermaid
graph TD
    subgraph Core["Functional Toolbelt Core"]
        A[metodologia-functional-toolbelt]
        T1[Tool 1: Event Storming]
        T2[Tool 2: Story Mapping]
        T3[Tool 3: Business Rule Extraction]
        T4[Tool 4: Acceptance Criteria GWT]
        T5[Tool 5: Traceability Matrix]
        T6[Tool 6: Anti-Pattern Detector]
    end
    subgraph Inputs["Inputs"]
        I1[Domain Actors & Processes]
        I2[User Flows & Journeys]
        I3[Stakeholder Interviews]
        I4[Existing Requirements]
    end
    subgraph Outputs["Outputs"]
        O1[Event Timeline & Bounded Contexts]
        O2[Story Map & Release Plan]
        O3[Business Rule Catalog]
        O4[Acceptance Criteria Suite]
        O5[Traceability Matrix]
        O6[Anti-Pattern Report]
    end
    subgraph Related["Related Skills"]
        R1[metodologia-workshop-design]
        R2[metodologia-technical-feasibility]
        R3[metodologia-ux-design-discovery]
        R4[metodologia-quality-engineering]
    end
    I1 --> T1
    I2 --> T2
    I3 --> T3
    I4 --> T6
    T1 --> T2 --> T3 --> T4 --> T5
    T6 --> T4
    T6 --> T5
    A --> O1
    A --> O2
    A --> O3
    A --> O4
    A --> O5
    A --> O6
    R1 --> A
    A --> R2
    A --- R3
    A --> R4
```

## Output Templates

**MD format (default):**

```
# Functional Toolbelt — {project} — Tool {N}: {name}
## Summary
> Tool applied: {name}. Domain: {context}. Findings: X items generated, Y gaps identified.
## Tool Output
[Specific content of the selected tool: event timeline, story map, rule catalog, GWT, matrix, or anti-pattern report]
## Identified Gaps
| Gap | Severity | Suggested Owner | Action |
## Cross-Reference
[Traceability to upstream/downstream tools]
```

**HTML format (for stakeholder presentation):**

```
Header: Logo + project + selected tool
Section 1: Tool Output (interactive visualization per tool)
  - Event Storming: visual timeline with colored stickies
  - Story Map: horizontal backbone + vertical stories
  - Rule Catalog: expandable table with decision trees
  - GWT: formatted scenarios with syntax highlighting
  - Traceability: interactive matrix with filters
  - Anti-Patterns: report with severity traffic-light
Section 2: Gaps & Action Items
Section 3: Cross-References to Related Tools
Footer: MetodologIA attribution + date
```
- Filename: `D-01_Functional_Toolbelt_{project}_{WIP}.html`
- Branded (Design System MetodologIA v5). Light-First Technical page with interactive tool output adapted to the selected tool (event timeline, story map, traceability matrix, etc.), gaps with traffic-light indicators, and navigable cross-references. WCAG AA, responsive, print-ready.

**DOCX format (on demand):**
- Filename: `D-01_Functional_Toolbelt_{project}_{WIP}.docx`
- Generated with python-docx under MetodologIA Design System v5: cover page, auto-generated TOC, branded headers/footers, zebra tables, Poppins typography (navy headings), Trebuchet MS (body), gold accents

**XLSX format (on demand):**
- Filename: `D-01_Functional_Toolbelt_{project}_{WIP}.xlsx`
- Generated with openpyxl under MetodologIA Design System v5. Headers with navy background and white Poppins typography, conditional formatting, auto-filters enabled, values without formulas. Sheets: Event Storming, Story Map, Business Rules, Acceptance Criteria, Traceability Matrix, Anti-Patterns.

**PPTX format (on demand):**
- Filename: `{phase}_{deliverable}_{client}_{WIP}.pptx`
- Generated with python-pptx under MetodologIA Design System v5. Slide master with navy gradient, Poppins titles, Trebuchet MS body, gold accents. Max 20 slides executive variant / 30 technical variant. Speaker notes with evidence references ([CODE], [DOC], [INFERENCE], [ASSUMPTION]).

## Evaluation

| Dimension | Weight | Criterion | Minimum Threshold |
|-----------|------|----------|---------------|
| Trigger Accuracy | 10% | Skill activates on prompts for event storming, story map, business rules, GWT, traceability, anti-patterns | 7/10 |
| Completeness | 25% | Selected tool executed completely; tool edge cases addressed; output includes identified gaps and cross-references | 7/10 |
| Clarity | 20% | Output is consumable by downstream role (dev, QA, product); GWT follows the 5 quality rules; event timeline is chronological | 7/10 |
| Robustness | 20% | Edge cases covered (no domain expert, legacy without docs, regulated, team resists formalization); conditional logic applied | 7/10 |
| Efficiency | 10% | Correct tool selected for context; full suite not executed when a single tool is sufficient | 7/10 |
| Value Density | 15% | End-to-end traceability present; anti-patterns detected with concrete fix; domain glossary consistent across outputs | 7/10 |

**Global minimum threshold: 7/10.** If any dimension falls below, the deliverable requires revision before delivery.

## Cross-References

- `functional-spec` — consumes toolbelt outputs to build formal specification document
- `quality-engineering` — testing strategy informed by traceability matrix (Tool 5)
- `flow-mapping` — process flows feed into event storming (Tool 1) and story mapping (Tool 2)
- `design-system` — when FORMATO=html, applies brand tokens to toolbelt outputs

## Output Artifact

**Primary:** `D-01_Functional_Toolbelt_{project}.md` (or `.html` if `{FORMATO}=html|dual`) — Functional patterns catalog, composition strategies, implementation guidelines.

**Included diagrams:**
- Pattern composition diagram
- Function pipeline flowchart
- Type hierarchy visualization

---
**Author:** Javier Montano | **Last updated:** March 12, 2026
