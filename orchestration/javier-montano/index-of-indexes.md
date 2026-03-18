# Index of Indexes — Mapa Maestro de Repos, Archivos y Ontologías

## Repositorios y Directorios Raíz

| Path | Descripción | Plugin | Tipo |
|------|-------------|--------|------|
| `~/skills/plugins/` | Repo principal de plugins | — | Git repo (monorepo) |
| `~/skills/plugins/sofka-discovery-framework/` | Sofka SAGE v12.3 | SDF | Plugin framework |
| `~/skills/plugins/metodologia-discovery-framework/` | MetodologIA MAO v1.4 | MAO | Plugin framework |
| `~/skills/plugins/pm-project-framework/` | PMO-APEX v1.0 | PM | Plugin framework |
| `~/skills/sofka-skills/` | Packaged .skill + .plugin files | — | Distribution |
| `~/.claude/` | Configuración global Claude Code | — | Config |
| `~/.claude/orchestration/` | Red de meta-orquestación | — | Orchestration |
| `~/.claude/skills/` | Skills globales (350+) | — | Global skills |
| `~/.claude/agents/` | Agentes globales | — | Global agents |
| `~/.claude/projects/` | Memory por proyecto | — | Persistence |

## Índices de Orquestación Global

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `~/.claude/CLAUDE.md` | 46 | Hub: identity, plugins, detection, network index, hard rules |
| `orchestration/meta-orchestrator.md` | 93 | Composición Tier 0/1/2, spawning, handoff, conflictos |
| `orchestration/input-amplifier.md` | 62 | 3-pass reasoning silencioso, escalación |
| `orchestration/metacognition-protocol.md` | 112 | Structured Reasoning, Plan Mode, Demand Elegance |
| `orchestration/auto-calibration.md` | 80 | Estado COLD→DEEP, lazy-load, cross-session |
| `orchestration/rag-priming-engine.md` | 92 | Auto-conversión inputs → priming-rag-*.md |
| `orchestration/workflow-discipline.md` | 115 | 8 patrones workflow + Core Principles |
| `orchestration/plugin-router.md` | 102 | Detección, registry, cheat sheets, activación |
| `orchestration/excellence-standards.md` | 82 | Formato, branding, naming, token efficiency |
| `orchestration/self-improvement.md` | 66 | Correcciones, anti-patrones, propagación cross-plugin |
| `orchestration/changelog.md` | — | Registro versionado de cambios a la red |
| `orchestration/tasklog.md` | — | Tareas, progreso, backlog cross-sesión |
| `orchestration/index-of-indexes.md` | — | Este archivo — mapa maestro |
| `orchestration/preferences-log.md` | — | Preferencias del usuario (workflow, output, design) |
| `orchestration/conversation-log.md` | — | Registro ejecutivo de conversaciones |
| `orchestration/self-improvement.md` | 66 | Correcciones, anti-patrones, propagación |
| `orchestration/changelog.md` | — | Registro de cambios de la red |
| `orchestration/tasklog.md` | — | Tareas y progreso cross-sesión |
| `orchestration/index-of-indexes.md` | — | Este archivo |

## Índices por Plugin

### SDF (Sofka SAGE v12.3)

| Archivo | Descripción |
|---------|-------------|
| `sofka-discovery-framework/CLAUDE.md` | Hub del plugin: ontology index, hard rules, quick start |
| `sofka-discovery-framework/references/ontology/protocol-zero-hallucination.md` | 6 evidence tags, >30% rule, severity flags |
| `sofka-discovery-framework/references/ontology/pipeline-orchestration.md` | 10 fases, 4 gates, 16 entregables, 4 modos |
| `sofka-discovery-framework/references/ontology/agent-committee.md` | 48 agentes: tríada + core + 36 especialistas + 7 Sabios |
| `sofka-discovery-framework/references/ontology/skills-catalog.md` | 107 skills por dominio + metadata |
| `sofka-discovery-framework/references/ontology/commands-reference.md` | 104 comandos por categoría |
| `sofka-discovery-framework/references/ontology/rag-priming-policy.md` | Política de adjuntos, 5-step processing |
| `sofka-discovery-framework/references/ontology/output-standards.md` | Markdown-Excellence, branding Sofka, HTML tokens |
| `sofka-discovery-framework/references/ontology/service-routing.md` | 10 tipos de servicio, auto-detección, routing |
| `sofka-discovery-framework/references/ontology/session-automation.md` | Hooks, discovery/, calibración, ghost menu |
| `sofka-discovery-framework/references/ontology/lessons-learned.md` | Correcciones y patrones (living doc) |
| `sofka-discovery-framework/references/ontology/quality-gates.md` | G0-G3 criterios y aprobación |
| `sofka-discovery-framework/references/ontology/brand-orchestration.md` | Multi-marca, isolation, output templates |
| `sofka-discovery-framework/references/ontology/canonical-tokens.md` | CSS design tokens Sofka |

### MAO (MetodologIA v1.4)

| Archivo | Descripción |
|---------|-------------|
| `metodologia-discovery-framework/CLAUDE.md` | Hub del plugin: P.I.V.O.T.E, 4 fases, maturity levels |
| `metodologia-discovery-framework/references/ontology/` | 13 sub-archivos (misma estructura que SDF, branding MetodologIA) |

### PM-APEX (v1.0)

| Archivo | Descripción |
|---------|-------------|
| `pm-project-framework/CLAUDE.md` | Hub del plugin: PM lifecycle, steering committee |
| `pm-project-framework/references/ontology/` | 13 sub-archivos (adaptados a gestión de proyectos) |

## Scripts de Automatización (por plugin)

| Script | Descripción | Fase |
|--------|-------------|------|
| `scripts/secrets-scan.sh` | G0 security gate — detecta credenciales | SessionStart |
| `scripts/scan-deliverables.sh` | Inventario de entregables existentes | SessionStart |
| `scripts/session-context-gen.sh` | Genera SESSION-README.md + SESSION-CLAUDE.md | SessionStart |
| `scripts/auto-prime-check.sh` | Detecta estado de RAG priming | SessionStart |
| `scripts/ghost-menu-inject.sh` | Inyecta navegación contextual | SessionStart + PostToolUse |
| `scripts/session-changelog.sh` | Inicializa/actualiza changelog de sesión | SessionStart + PostToolUse |
| `scripts/index-repo.sh` | Genera repo-index.json | SessionStart |
| `scripts/lazy-load-resolver.sh` | Carga progresiva L1/L2/L3 por fase y tipo | On demand |
| `scripts/inject-metacognition.sh` | Inyecta protocolos FULL/LIGHT en agentes | On demand |
| `scripts/context-prune.sh` | Comprime changelog >150 líneas | PostToolUse |
| `scripts/post-prime-calibrate.sh` | Recalibra después de priming | PostToolUse |
| `scripts/sdf-init.sh` | Wizard de inicialización SDF | Manual |
| `scripts/export-pdf.sh` | Markdown → PDF con branding | Manual |
| `scripts/convert-skills.sh` | Exporta skills a Cursor/Codex/Gemini | Manual |
| `scripts/render-mermaid.sh` | Renderiza diagramas Mermaid | Manual |
| `scripts/discovery-retro.sh` | Retrospectiva cuantitativa | Manual |
| `scripts/skill-dependency-graph.sh` | Mapa de dependencias de skills | Manual |
| `scripts/secrets-mask.sh` | Enmascara datos sensibles | Manual |

## Hooks

| Archivo | Eventos |
|---------|---------|
| `{plugin}/hooks/hooks.json` | SessionStart (5 hooks), PostToolUse (3 hooks, matcher: Write\|Edit) |
| `~/skills/plugins/hooks/hooks.json` | Shared hooks (misma estructura) |

## Artifacts de Sesión (discovery/ o project/)

| Archivo | Descripción | Generado por |
|---------|-------------|--------------|
| `session-state.json` | Estado serializado del pipeline | session-changelog.sh |
| `SESSION-README.md` | Contexto auto-detectado del proyecto | session-context-gen.sh |
| `SESSION-CLAUDE.md` | Instrucciones de sesión para este repo | session-context-gen.sh |
| `calibration-digest.md` | Estado de priming + cobertura | auto-prime-check.sh |
| `ghost-menu.md` | Navegación contextual actualizada | ghost-menu-inject.sh |
| `session-changelog.md` | Log de acciones (auto-pruned >150) | session-changelog.sh |
| `repo-index.json` | Inventario de archivos del repo | index-repo.sh |
| `.sage-secrets-audit.log` | Resultado del scan G0 | secrets-scan.sh |
| `needs-priming` | Marker si priming requerido | auto-prime-check.sh |
| `rag-priming/*.md` | Priming files de sesión | rag-priming-engine |

## Memory (Persistencia Cross-Sesión)

| Path | Descripción |
|------|-------------|
| `~/.claude/projects/-Users-deonto-skills-plugins/memory/MEMORY.md` | Índice de memorias del proyecto plugins |
| `~/.claude/projects/-Users-deonto-skills-plugins/memory/user_javier_identity.md` | Identidad 3-brand |
| `~/.claude/projects/-Users-deonto-skills-plugins/memory/feedback_file_naming_tags.md` | {WIP}/{Aprobado} tags |
