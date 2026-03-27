# Prompt Engineering — Body of Knowledge

## Canon

### Foundational Patterns

1. **Role-Context-Task-Format (RCTF)**: The universal prompt structure.
   - Role: "You are a senior data analyst"
   - Context: "Given this dataset of Q4 sales..."
   - Task: "Identify the top 3 trends"
   - Format: "Output as a numbered list with evidence"

2. **Few-Shot Learning**: Provide 2-5 input/output examples.
   - Quality > quantity: 2 perfect examples beat 10 mediocre ones
   - Include edge cases in examples
   - Match the exact output format you want

3. **Chain-of-Thought (CoT)**: "Let's think step by step"
   - Zero-shot CoT: Just add "Think step by step" (Wei et al., 2022)
   - Few-shot CoT: Examples include reasoning traces
   - Best for: math, logic, multi-step analysis

4. **System Prompts**: Persistent behavioral constraints.
   - Place at the beginning of the conversation
   - Include: identity, capabilities, limitations, output format
   - Claude: uses system parameter; GPT: first message role=system

5. **Meta-Prompting**: Prompts that generate prompts.
   - Input: task description + constraints
   - Output: optimized prompt for the task
   - Evaluation: test generated prompt against metrics

### Advanced Patterns

6. **Constitutional AI**: Self-correcting prompts.
   - Step 1: Generate initial response
   - Step 2: Critique against principles
   - Step 3: Revise based on critique
   - Principles map to Constitution values

7. **Prompt Chaining**: Sequential prompts where output N feeds input N+1.
   - Decompose complex tasks into atomic steps
   - Each step has its own prompt optimized for that sub-task
   - Error handling between chain links

8. **Retrieval-Augmented Prompts**: Integrate RAG context.
   - Place retrieved context before the question
   - Use delimiters: "### Context:\n{retrieved}\n### Question:\n{query}"
   - Instruction: "Answer based ONLY on the provided context"

## Standards & References

- Wei et al. (2022) — Chain-of-Thought Prompting
- Brown et al. (2020) — Few-Shot Learners (GPT-3)
- Anthropic — Constitutional AI approach
- OpenAI — Prompt Engineering Guide
- Google — Gemini Prompt Design Guidelines

## Quality Metrics

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Accuracy | Correct outputs / total runs | >= 90% |
| Consistency | Same output for same input across runs | >= 85% |
| Format compliance | Outputs match specified schema | 100% |
| Injection resistance | Adversarial inputs handled safely | 100% |
| Token efficiency | Prompt tokens / useful output tokens | < 3:1 ratio |
