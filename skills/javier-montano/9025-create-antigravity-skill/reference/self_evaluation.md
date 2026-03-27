# Self-Evaluation Rubric: The Excellence Loop

Before you deliver the **newly created skill** to the user, you MUST pause and pass this quality gate. Ask yourself critically:

## 1. Architectural Integrity

- [ ] Did I create the orchestrator entrypoint `SKILL.md`?
- [ ] Does `SKILL.md` have valid YAML frontmatter?
- [ ] Did I create the `/reference/` directory with all 4 required files (`knowledge_graph.md`, `best_practices.md`, `output_template.md`, `self_evaluation.md`)?
- [ ] Does `SKILL.md` explicitly enforce an `Instruction Loading Sequence` pointing to the reference files?

## 2. Markdown Structural Strictness (Phase G)

- [ ] Are ALL my headings (`##`) separated from text by a blank line above and below?
- [ ] Are ALL my lists (`- item`) separated from surrounding text/headings by a blank line above and below?
- [ ] Are ALL my code fences (` ``` `) surrounded by blank lines on the outside?

## 3. Density and Specificity

- [ ] Is the skill generic ("Write good code") or high-density ("Enforce purely functional components without side effects")?
- [ ] Did I remove conversational filler (e.g., "Here is the code you requested") from the templates?

**[CRITICAL INSTRUCTION]**: If any answer is NO, you MUST fix the generated files internally before notifying the user of completion. Do not compromise on the sub-repo pattern.
