# Workflow: Port Prompt

Adapt a prompt from one platform to another while preserving behavior.

## Trigger

User wants to move a prompt between platforms (e.g., GPT → Claude Project, Claude → Gemini Gem).

## Steps

### Step 1: Analyze Source

Read the source prompt and identify:
- Current platform (format, structure, length)
- Core behavior (archetype, constraints, output format)
- Platform-specific features used (Actions, MCP, Extensions)
- Knowledge base / external files dependency

### Step 2: Map Platform Differences

Consult `reference/platform-guides.md` § Cross-Platform Porting.

Key deltas to check:

| Dimension | Check |
|-----------|-------|
| Character limit | Source fits in target? Compression needed? |
| Formatting | XML tags → markdown? Different heading conventions? |
| Knowledge base | PDF → Google Docs? Project files → GPT uploads? |
| Tools/Actions | MCP → Actions? Extensions → Function calling? |
| Model behavior | More/less literal? Verbosity differences? |

### Step 3: Adapt

Apply platform-specific transformations:

**Compressing (e.g., Claude → Gemini):**
- Merge sections that can be combined
- Move reference content to external docs
- Keep only essential constraints inline
- Front-load output format definition

**Expanding (e.g., Gemini → Claude):**
- Add sections that the more detailed platform supports
- Use XML tags for structured sections
- Add more specific constraints
- Include full output template inline

**Behavioral adjustments:**
- Claude → GPT: Add anti-verbosity constraints, strengthen format enforcement
- GPT → Claude: Reduce MUST/ALWAYS language, explain reasoning instead
- Any → Gemini: Front-load format, compress aggressively

### Step 4: Evaluate on Target

Run the evaluator on the adapted prompt:

```bash
python tools/prompt-evaluator.py [adapted-file] --verbose
```

Verify scores are comparable to the source prompt.

### Step 5: Test

Provide 3 test queries that should produce equivalent behavior on both platforms. The user can verify behavioral parity.

### Step 6: Deliver

Present:
- Adapted prompt, ready for target platform
- Deployment guide for the target platform
- Summary of adaptations made
- Test queries for behavioral verification

## Exit Criteria

- Prompt formatted for target platform
- Character limits respected
- Core behavior preserved
- Deployment instructions included
