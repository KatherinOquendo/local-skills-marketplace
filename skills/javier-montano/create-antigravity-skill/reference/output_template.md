# Output Template: The Skill Scaffold

When generating a new skill, deploy exactly these files with the following baseline structures. Fill out the bracketed fields `[...]` according to the user's domain request.

## 1. `SKILL.md`

```markdown
---
name: [skill-name]
description: [Short, impactful description of what this skill does]
---

# [Skill Title]

[Brief Persona/Objective definition]

## Instruction Loading Sequence

Before executing your main task, you MUST load the following context in exact order:

1. `reference/knowledge_graph.md`
2. `reference/best_practices.md`
3. `reference/output_template.md`
4. `reference/self_evaluation.md`

## Protocol

1. [Step 1 of the operation]
2. [Step 2 of the operation]
3. [Step n]
```

## 2. `reference/knowledge_graph.md`

```markdown
# Knowledge Graph

[Define the domain concepts, terms, and mental models of the specific skill. Include a mermaid chart if workflows or data pipelines are complex.]
```

## 3. `reference/best_practices.md`

```markdown
# Best Practices

[List the immutable laws, technical constraints, and negative constraints (what NOT to do) specific to this skill's domain.]
```

## 4. `reference/output_template.md`

```markdown
# Output Template

[Provide the exact text, JSON, or code scaffolding the skill must systematically produce when invoked.]
```

## 5. `reference/self_evaluation.md`

```markdown
# Self-Evaluation Rubric

[Provide a grading checklist the agent must mentally process before finalizing the user's task.]
```
