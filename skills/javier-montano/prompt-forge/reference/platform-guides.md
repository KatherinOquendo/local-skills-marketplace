# Platform Deployment Guides

## Table of Contents

1. [Claude Projects](#claude-projects)
2. [ChatGPT Custom GPTs](#chatgpt-custom-gpts)
3. [Gemini Gems](#gemini-gems)
4. [API / Programmatic](#api--programmatic)
5. [Cross-Platform Porting](#cross-platform-porting)

---

## Claude Projects

### Architecture

Claude Projects use a two-layer context system:
- **Project Instructions:** System-level prompt that persists across all conversations in the project. This is your Playbook.
- **Project Knowledge:** Files uploaded to the project that the model can reference. These are your L2 (warm) context.

### Formatting Guidelines

- Use markdown with clear heading hierarchy (H1 → H2 → H3)
- Claude responds well to XML-like tags for structured sections: `<role>`, `<constraints>`, `<output-format>`
- Use explicit section markers over implicit structure
- Newer Claude models (4.5+) take instructions literally — say exactly what you mean, no aggressive MUST/ALWAYS unless truly critical

### Knowledge Base Design

- Upload reference files as separate documents (style guides, templates, data)
- Name files descriptively — Claude uses filenames to decide relevance
- Keep individual files focused (one topic per file)
- Total knowledge base: aim for under 200K tokens for best retrieval quality

### Character Limits

- Project instructions: ~8,000 characters recommended (technically flexible but quality degrades with length)
- Knowledge files: up to 30 files, various formats (PDF, TXT, MD, CSV, code)

### Deployment Checklist

```
□ Playbook adapted to Claude's instruction format
□ Knowledge files uploaded and named descriptively
□ Tested with 3-5 representative queries
□ Verified archetype persistence after 10+ turns
□ Checked constraint compliance on edge cases
```

---

## ChatGPT Custom GPTs

### Architecture

Custom GPTs use three layers:
- **Instructions:** System prompt field (your Playbook)
- **Knowledge:** Uploaded files accessible via retrieval
- **Actions:** External API connections (optional)

### Formatting Guidelines

- GPT-4o responds well to markdown with clear delimiters
- Use `###` headers to separate sections
- Triple backticks for output templates
- Numbered steps for sequential instructions
- GPT tends to be verbose — include explicit brevity constraints

### Knowledge Base Design

- Upload files in the Knowledge section
- GPT uses RAG to pull relevant snippets from uploaded files
- Supported formats: PDF, TXT, MD, DOCX, CSV, XLSX, JSON
- Name files with clear topic labels for better retrieval
- Maximum: 20 files, 512MB each

### Character Limits

- Instructions field: ~8,000 characters
- Conversation starters: 4 maximum, keep under 100 characters each

### Deployment Checklist

```
□ Instructions pasted into GPT Builder instructions field
□ Knowledge files uploaded
□ Conversation starters defined (4 representative use cases)
□ Profile image and description set
□ Tested in Preview mode with varied queries
□ Published with appropriate sharing setting (private/link/public)
```

---

## Gemini Gems

### Architecture

Gemini Gems use:
- **System Instructions:** Your core prompt (Playbook)
- **Connected Knowledge:** Google Docs, Sheets, or Drive files
- **Extensions:** Google ecosystem integrations (optional)

### Formatting Guidelines

- Gemini works best with front-loaded formatting instructions
- Define the output structure at the top of the prompt, not the bottom
- Use clear section breaks (horizontal rules or headers)
- Gemini handles long structured responses well but can overrun length constraints without explicit limits
- Keep instructions under the character limit — Gemini truncates silently

### Knowledge Base Design

- Connect Google Docs and Sheets directly
- Gemini accesses connected docs in real-time (updates are reflected)
- Organize knowledge in Google Drive folders for clean access
- Use Google Docs headers to help Gemini navigate long documents

### Character Limits

- System instructions: ~4,000 characters (more constrained than GPT/Claude)
- This means your Playbook needs to be more compressed for Gemini
- Move detailed reference material to connected docs

### Deployment Checklist

```
□ System instructions condensed to fit character limit
□ Reference material moved to connected Google Docs
□ Tested across Gemini's available models
□ Verified behavior with and without connected docs
□ Shared with appropriate access permissions
```

---

## API / Programmatic

### Architecture

When deploying via API, you control the full context stack:
- **System message:** Your Playbook (passed as the `system` parameter)
- **RAG pipeline:** Dynamic document retrieval
- **Function calling / Tools:** External capabilities
- **Conversation history:** You manage turn history and summarization

### Formatting Guidelines

- All platforms support markdown in system messages
- For structured output, specify JSON schema explicitly
- Use `<xml-tags>` for complex section boundaries (especially with Claude)
- Include explicit response format instructions for each API call

### Token Management

```
Total Context = System Prompt + Conversation History + RAG Results + Tool Outputs
```

**Budget allocation (for 128K context models):**
- System prompt: 2K-5K tokens (keep lean)
- Conversation history: 10K-30K tokens (with rolling summarization)
- RAG results: 5K-20K tokens (ranked, top-k)
- Tool outputs: variable
- Generation: 4K-8K tokens reserved

### Deployment Checklist

```
□ System prompt optimized for token density
□ RAG pipeline tested with representative queries
□ Function calling schemas defined and tested
□ Conversation history management strategy implemented
□ Error handling for API failures defined
□ Cost monitoring configured
□ Rate limiting and retry logic in place
```

---

## Cross-Platform Porting

When moving a prompt between platforms, these dimensions need adaptation:

### Adaptation Matrix

| Dimension | Claude | GPT-4o | Gemini |
|-----------|--------|--------|--------|
| Instruction compliance | Very literal, precise | Responsive, can be verbose | Strong but needs front-loading |
| XML tags | Excellent support | Works but less standard | Limited support |
| Markdown | Full support | Full support | Full support |
| System prompt size | Flexible (~8K chars) | ~8K chars | ~4K chars |
| Knowledge retrieval | Project knowledge | RAG from uploaded files | Connected Google Docs |
| Tone default | Balanced, follows directions | Eager, can over-help | Concise, structured |

### Porting Checklist

```
1. □ Verify target platform character limits
2. □ Compress if moving to a more constrained platform
3. □ Replace platform-specific formatting (e.g., XML tags → markdown)
4. □ Adapt knowledge base format (PDF → Google Docs for Gemini, etc.)
5. □ Test archetype persistence on target platform
6. □ Adjust verbosity constraints (GPT needs more "be brief" directives)
7. □ Verify output template compliance on target model
```

### Platform-Specific Adjustments

**Claude → GPT:**
- Remove XML tags or convert to markdown headers
- Add explicit anti-verbosity constraints
- GPT may need stronger output format enforcement

**Claude → Gemini:**
- Compress instructions significantly (4K char limit)
- Move reference content to connected Google Docs
- Front-load format definitions (put output template before instructions)

**GPT → Claude:**
- Claude is more literal — remove "helpful" padding
- Claude excels with XML structured sections
- Reduce MUST/ALWAYS language — explain why instead

**Any → API:**
- Optimize for token density (every token costs money at scale)
- Add explicit JSON/structured output schemas
- Design for stateless interaction (manage history externally)
