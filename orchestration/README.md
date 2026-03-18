# Orchestration

Meta-orchestrator network — the 14 files that govern how Claude Code operates across all plugins, skills, and brands.

## File Dependency Map

```
CLAUDE.md (root)
  ├── plugin-router.md          (route commands to correct plugin by prefix)
  ├── meta-orchestrator.md      (committee composition, handoff protocols)
  ├── input-amplifier.md        (3-pass input reinterpretation on every input)
  ├── metacognition-protocol.md (reasoning, planning, self-awareness)
  ├── workflow-discipline.md    (core principles, execution discipline)
  ├── auto-calibration.md       (session priming, state detection)
  ├── rag-priming-engine.md     (RAG context loading protocols)
  ├── excellence-standards.md   (output format, branding, naming)
  ├── self-improvement.md       (lessons learned, feedback integration)
  ├── changelog.md              (network version history)
  ├── tasklog.md                (cross-session task tracking)
  ├── index-of-indexes.md       (repo map, file ontology)
  ├── preferences-log.md        (user preferences and corrections)
  └── conversation-log.md       (conversation registry)
```

## Loading Rule

Read on demand — never load all at once. Each file is loaded only when its specific concern is active (routing → plugin-router, quality → excellence-standards, etc.).
