# End-to-End Quality Pipeline

Master documentation workflow showing the complete quality chain from user input through final delivery. This orchestration workflow connects all 8 skills and demonstrates the full capability of the governed project ecosystem.

## Frontmatter

description: Orchestration workflow documenting the complete quality chain across all skills and feedback loops

## The Complete Quality Pipeline

This workflow is a **documentation and orchestration artifact** that describes how all skills work together, not a hands-on execution workflow. It shows the full architecture of the governed project system.

---

## Phase 1: Input Analysis

**Skill**: input-analyst

**Steps**:
1. User provides task, question, or request
2. input-analyst analyzes: context, ambiguity, missing information, edge cases
3. Reformulates request into clear specification with acceptance criteria
4. Output: analysis document; recommendation for which skill to execute

**Quality Checks**:
- [ ] Input analysis is concise (< 500 words)
- [ ] Edge cases identified and documented
- [ ] Acceptance criteria are measurable

---

## Phase 2: Task Decomposition and Planning

**Skill**: task-engine

**Steps**:
1. task-engine receives reformulated specification from input-analyst
2. Decompose: break task into subtasks, dependencies, confidence estimates
3. Plan: sequence subtasks by dependency; identify bottlenecks
4. Output: task plan with subtasks, sequencing, risk flags

**Quality Checks**:
- [ ] All subtasks are atomic (no "and" in descriptions)
- [ ] Dependencies clearly mapped
- [ ] Confidence scores assigned to each subtask

---

## Phase 3: Target Skill Execution

**Skills**: prompt-forge, rule-forge, workflow-forge, naming-and-slugging, ecosystem-forge, excellence-loop

**Selection Logic**:
- **prompt-forge**: when task is about prompt quality, system message design, instruction clarity
- **rule-forge**: when task is about defining governance rules, constraints, enforcement patterns
- **workflow-forge**: when task is about automating multi-step processes, orchestration
- **naming-and-slugging**: when task is about naming conventions, artifact organization, compliance
- **ecosystem-forge**: when task is about cross-skill integration, artifact verification, dependency management
- **excellence-loop**: when task quality is sub-target or iteration needed

**Execution Steps**:
1. Skill receives task plan from task-engine
2. Skill executes its core workflow (e.g., rule-forge runs create-and-validate)
3. Skill produces draft output: rule, workflow, prompt, naming audit, ecosystem analysis, etc.
4. Skill performs self-evaluation against its rubric (self-evaluation.md)
5. Output: validated artifact + self-evaluation score

**Quality Checks**:
- [ ] Self-evaluation score ≥ 8/10
- [ ] All specified acceptance criteria from Phase 1 met
- [ ] No red flags from skill's rubric

---

## Phase 4: Excellence Loop (Iterative Refinement)

**Skill**: excellence-loop

**Trigger**: When skill output scores < 8/10 on self-evaluation OR acceptance criteria not fully met

**Steps**:
1. excellence-loop receives draft output + self-evaluation results
2. Analyze gaps: which rubric items failed, what feedback does user provide
3. Generate improvement suggestions: reference docs, best practices, edge case handling
4. Apply fixes: rewrite sections, add missing elements, refine examples
5. Return to target skill for re-execution
6. Repeat until: score ≥ 8/10 AND all acceptance criteria met

**Quality Checks**:
- [ ] Improvement suggestions are specific and actionable
- [ ] Each iteration brings score closer to 10/10
- [ ] Maximum 3 iterations before escalating to user

---

## Phase 5: Final Verification and Synthesis

**Skill**: ecosystem-forge (verify-and-repair workflow)

**Steps**:
1. Run ecosystem-checker.py on all generated artifacts
2. Verify: naming compliance, cross-references valid, no conflicts, no orphans
3. Generate final health report
4. If issues found: run repair-playbook to fix
5. Output: verified artifacts + health report

**Quality Checks**:
- [ ] ecosystem-checker.py reports 0 issues
- [ ] All naming violations resolved
- [ ] No broken references
- [ ] No conflicts between new rules/workflows

---

## Phase 6: Delivery and Reflection

**Steps**:
1. Deliver final verified artifacts to user (rules, workflows, prompts, docs, etc.)
2. Generate delivery summary: what was created, quality scores, verification results
3. Provide: usage documentation, templates, reference guides
4. Optional: archive version history for audit trail
5. Reflection: what worked well, what could improve, patterns for next iteration

**Quality Checks**:
- [ ] User accepts final output
- [ ] All acceptance criteria from Phase 1 are met
- [ ] Delivery documentation is clear and actionable
- [ ] Artifacts are production-ready or marked for further iteration

---

## Architecture: How Skills Connect

```
User Input (Phase 1)
    ↓ (input-analyst analyzes)
Specification + Acceptance Criteria
    ↓ (task-engine decomposes)
Task Plan (subtasks, dependencies)
    ↓ (select target skill based on plan)
┌─────────────────────────────────────┐
│ Target Skill Execution (Phase 3)    │
│ • prompt-forge                      │
│ • rule-forge                        │
│ • workflow-forge                    │
│ • naming-and-slugging              │
│ • ecosystem-forge                  │
└─────────────────────────────────────┘
    ↓ (self-evaluate; score < 8/10?)
    └──→ excellence-loop (Phase 4) → re-execute skill
         │
         └──→ (score ≥ 8/10 ✓)
    ↓
Verified Artifacts + Health Report
    ↓ (ecosystem-checker; Phase 5)
    └──→ (issues found?) → repair-playbook → re-verify
         │
         └──→ (0 issues ✓)
    ↓
Final Delivery (Phase 6)
    ↓
User Acceptance + Reflection
```

---

## Quality Metrics Across Phases

| Phase | Metric | Target | Tool |
|---|---|---|---|
| 1 | Analysis completeness | 100% (no ambiguity) | input-analyst |
| 2 | Task decomposition | ≤ 5 main subtasks | task-engine |
| 3 | Self-evaluation score | ≥ 8/10 | skill's rubric |
| 4 | Iteration count | ≤ 3 loops | excellence-loop |
| 5 | Ecosystem health | 0 issues | ecosystem-checker |
| 6 | User acceptance | ✓ Yes | manual review |

---

## Feedback Loops Within the Pipeline

**Loop 1: Self-Evaluation Loop** (within Phase 3)
- Skill self-evaluates against rubric
- If score < 8/10: applies self-described fixes
- Re-evaluates until 8/10 ✓

**Loop 2: Excellence Loop** (Phase 4)
- If self-evaluation score < 8/10 OR acceptance criteria unmet
- excellence-loop refines output; skill re-executes
- Maximum 3 iterations before user involvement

**Loop 3: Ecosystem Verification Loop** (Phase 5)
- ecosystem-checker finds issues
- repair-playbook provides fixes
- ecosystem-checker re-verifies
- Repeat until 0 issues ✓

**Loop 4: User Feedback Loop** (Phase 6)
- User reviews delivered output
- Provides feedback or approval
- If changes needed: return to excellence-loop
- If approved: complete

---

## Example: End-to-End Quality Pipeline in Action

### User Request
"Create a rule for my Python project: no hardcoded API keys in code."

### Phase 1: Input Analysis
input-analyst → "Create a rule defining what constitutes a hardcoded API key, what file types to check, why it's dangerous"

### Phase 2: Task Decomposition
task-engine → "Subtask 1: Define scope (Python files, ENV config); Subtask 2: Create examples; Subtask 3: Validate syntax"

### Phase 3: Skill Execution
rule-forge → Creates `R-no-hardcoded-api-keys.md`
- Runs self-evaluation.md
- Scores 7/10 (glob scope too broad)

### Phase 4: Excellence Loop
excellence-loop → "Narrow glob to `src/**/*.py`; clarify examples"
rule-forge → Re-runs; scores 9/10 ✓

### Phase 5: Verification
ecosystem-forge → verify-and-repair
- Checks naming: ✓ kebab-case
- Checks cross-refs: ✓ no broken refs
- Checks conflicts: ✓ no other API-key rules

### Phase 6: Delivery
Final rule delivered: `R-no-hardcoded-api-keys.md`, score 9/10, ecosystem health 0 issues
User: "Approved ✓"

---

## How to Use This Pipeline

This workflow documents the architecture and is designed for:
1. **Understanding the system**: See how all 8 skills fit together
2. **Debugging quality issues**: Trace which phase broke down
3. **Training new team members**: Show the complete flow
4. **Designing similar systems**: Use this as a template for other governance pipelines

Each phase is independent and can be executed separately OR as part of the full pipeline. The feedback loops ensure that **output never ships below 8/10 quality**.

---

## Verification Checklist

- [ ] All 6 phases understood and documented
- [ ] Architecture diagram accurately shows skill connections
- [ ] Feedback loops are implemented and tested
- [ ] Example trace-through demonstrates the full pipeline
- [ ] Quality metrics defined for each phase
- [ ] No artifact ships below 8/10 on self-evaluation
- [ ] Final delivery includes health report and user acceptance
