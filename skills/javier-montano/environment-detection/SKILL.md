---
name: environment-detection
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Detect IDE and model at session start. Adapt triad mode, skill loading,
  and capability profile. Auto-prime for optimal performance per environment.
  Trigger: "detect environment", "what IDE", "configure environment", "auto-prime"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Environment Detection

> "Know your battlefield before deploying your troops."

## TL;DR

Detects the runtime environment (IDE + model) and adapts Pristino's behavior accordingly. Determines triad mode (full/sequential/checklist/suggestion), skill loading strategy, and context budget. Runs at session start as part of the bootstrap sequence. Full protocol: `references/ontology/environment-protocol.md`.

## Procedure

### Step 1: Discover
- Check which instruction file loaded the agent (CLAUDE.md, GEMINI.md, .cursorrules, etc.)
- Check available tools (Agent tool present? → full triad mode)
- Check model context window (how much can we load?)
- Read `references/ontology/environment-protocol.md` for the full detection matrix

### Step 2: Analyze
- Map IDE to capability profile:
  - claude-code → full triad (subagents, hooks, MCP)
  - gemini/antigravity → sequential prompts (no Agent tool)
  - cursor/windsurf → checklist mode (inline rules)
  - copilot → suggestion mode (limited context)
  - codex → sequential prompts (Bash/Read/Write only)
- Map model to tier:
  - Heavy (>100K): load full Constitution + Index + history
  - Medium (32-100K): load Constitution + active skills
  - Light (<32K): load active skill only

### Step 3: Execute
- Set triad mode based on IDE detection
- Set context budget based on model tier
- Load appropriate files for the tier
- Report environment to user:
  ```
  Environment detected:
    IDE: {ide} | Model: {model} | Tier: {tier}
    Triad: {mode} | Tools: {available_tools}
    Skills: {count} | Agents: {count}
  ```

### Step 4: Validate
- Confirm detected IDE matches actual tool availability
- Confirm model tier matches actual context capacity
- If mismatch: adjust and re-report
- Log detection result for session continuity

## Quality Criteria

- [ ] IDE correctly identified from instruction file
- [ ] Model tier correctly assessed
- [ ] Triad mode matches IDE capabilities
- [ ] Context budget set appropriately
- [ ] Environment reported to user
- [ ] Evidence tags applied

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Assuming Claude Code always | May be running in Cursor/Copilot | Detect from instruction file |
| Loading full Index in Light tier | Exhausts context window | Load only active skill |
| Skipping detection | Triad mode wrong for the IDE | Always detect at session start |
| Hardcoding model name | Models change, tiers don't | Detect by capability, not name |

## Related Skills

- `session-protocol` — Environment detection is Step 0 of session init
- `context-optimization` — Context budget depends on detected tier
- `continuous-learning` — Log environment patterns for optimization
