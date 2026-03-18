# Workflow: Create Prompt

Create a new system prompt from scratch using the full forge cycle.

## Trigger

User requests a new system prompt, custom assistant, or AI configuration for any platform.

## Steps

### Step 1: Capture Context

Gather the minimum viable context to produce a strong first draft.

**Required inputs:**
- Domain / topic of the assistant
- Target platform (Claude Project, Custom GPT, Gemini Gem, API)
- Primary deliverable (what the user gets from the assistant)

**Optional inputs (infer if not provided):**
- Target audience
- Language preference
- Tone/style reference
- Specific frameworks or methodologies to embed

**Rule:** Ask max 2 questions. Infer the rest. Generate first, confirm after.

### Step 2: Scaffold

Run the scaffolder to generate a starting structure:

```bash
python tools/prompt-scaffolder.py --domain "[domain]" --platform [platform] --language [lang]
```

Or write directly using the Playbook template from `reference/playbook-template.md`.

### Step 3: Draft

Fill in every section of the Playbook:

1. Define the hybrid archetype (domain + methodology + communication style)
2. Write a measurable objective
3. Design the interaction flow (discovery → execution → delivery)
4. Specify constraints (specific, testable, justified)
5. Define the output template with placeholders
6. Add self-correction triggers

**Quality gate:** Every section must have content. No placeholders left unfilled.

### Step 4: Evaluate

Run the evaluator:

```bash
python tools/prompt-evaluator.py output.md --verbose --strict
```

**Pass criteria:** All 10 criteria ≥ 8/10.

If any criterion fails:
- Read the repair protocol in `reference/evaluation-rubric.md`
- Apply the fix
- Re-evaluate

### Step 5: Platform Adapt

Format the output for the target platform using `reference/platform-guides.md`:

- Claude Project → Check character limits, optimize for literal instruction following
- Custom GPT → Add conversation starters, check Instructions field limit
- Gemini Gem → Compress to ~4K chars, move reference to connected docs
- API → Optimize for token density, add JSON schema if needed

### Step 6: Deliver

Present the final prompt with:
- The complete prompt text, ready to paste
- Platform-specific deployment instructions
- Recommended knowledge base files (if applicable)
- 3 test queries to verify behavior

## Exit Criteria

- Prompt scores ≥ 8 on all 10 criteria
- Formatted for target platform
- Deployment instructions included
