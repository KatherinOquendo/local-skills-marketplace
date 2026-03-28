# JM Labs — Canonical Skill Registry

> **Milestone:** Centralización completa. Una fuente de verdad. Tres ecosistemas. 557 skills. Todo sincronizado.
> **Fecha:** 2026-03-27 · **Autor:** Javier Montaño

---

## El Hito

Este repositorio es ahora el **núcleo canónico** de toda la inteligencia profesional de JM Labs.

```
                    ┌─────────────────────────────────┐
                    │   JM LABS CANONICAL REGISTRY     │
                    │   557 skills · 0000–9999         │
                    │   100% MOAT certified            │
                    └────────────┬────────────────────┘
                                 │  skill-sync.sh (build-time)
               ┌─────────────────┼─────────────────┐
               ▼                 ▼                  ▼
    ┌──────────────────┐ ┌──────────────┐ ┌─────────────────────┐
    │ Sovereign        │ │ PMO-APEX     │ │ MetodologIA         │
    │ Architect (SA)   │ │  (PM)        │ │  (MAO)              │
    │ 134 skills       │ │ 113 skills   │ │ 115 skills          │
    │ 66 agents        │ │ 48 agents    │ │ 101 agents          │
    └──────────────────┘ └──────────────┘ └─────────────────────┘
```

**Antes:** Skills duplicados, inconsistentes, sin gobierno.
**Ahora:** Una edición → se propaga a todos los ecosistemas.

---

## Números del Hito

| Métrica | Valor |
|---------|-------|
| Skills canónicos | **557** |
| Autores canónicos | javier-montano (513) · metodologia (62) · joint (18) |
| Rango de numeración | 0001–9128 (espacio reservado hasta 9999) |
| Plugins consumidores | 3 (SA · PM · MAO) |
| Total skills en producción | **362** (SA: 134 · PM: 113 · MAO: 115) |
| Quality gates activos | 5 (G0–G3 + MOAT pre-commit) |
| Agentes disponibles | 215 (66 SA · 48 PM · 101 MAO) |
| Comandos disponibles | 331 (119 SA · 103 PM · 109 MAO) |
| Remotes sincronizados | 5 (origin · metodologia · jm-shared · kathe-private · personal) |

---

## Taxonomía 0000–9999

| Rango | Dominio | Skills |
|-------|---------|--------|
| 0001–0991 | Discovery, Strategy & Business Analysis | 91 |
| 1001–1060 | Architecture & System Design | 60 |
| 2001–2060 | Frontend, UI/UX & Design Systems | 60 |
| 3001–3038 | Backend, APIs & Serverless | 38 |
| 4001–4026 | Data, Databases & Analytics | 26 |
| 5001–5025 | Security, Auth & Compliance | 25 |
| 6001–6029 | Quality, Testing & CI/CD | 29 |
| 7001–7030 | DevOps, Deployment & Infrastructure | 30 |
| 8001–8020 | Performance, SEO & Growth | 20 |
| 9001–9128 | Meta-skills, AI Tooling & Orchestration | 128 |

---

## Flujo Canónico

```bash
# 1. Editar el skill canónico
vim skills/javier-montano/0043-discovery-orchestration/SKILL.md

# 2. El pre-commit valida MOAT compliance automáticamente
git commit -m "improve(skills): discovery-orchestration → MOAT"
# → Hook ejecuta moat-audit.sh
# → Bloquea si regression detectada

# 3. Sincronizar a plugins
bash scripts/skill-sync.sh --all
# → Copia a sovereign-architect/skills/
# → Copia a pm-project-framework/skills/
# → Copia a metodologia-discovery-framework/skills/
# → Actualiza skill-manifest.json en cada plugin

# 4. Push a todos los remotes
git push origin main         # JM Labs
git push metodologia main    # MetodologIA (GitHub público)
git push jm-shared main      # Compartido
```

---

## Ecosistemas Activos

### Sovereign Architect (SA) — `plugins/javier-montano/sovereign-architect/`
- **Identidad:** Principal Software Architect para development kit
- **Skills:** 134 (49 canonical + 78 plugin-only + 4 OpenClaw + 3 OpenClaw base)
- **Agentes:** 66 especializados en 3 tiers
- **Activa con:** `/sa:analyze` `/sa:run-auto` `/sa:audit-security`

### PMO-APEX (PM) — `plugins/javier-montano/pm-project-framework/`
- **Identidad:** Agentic Project Excellence Office
- **Skills:** 113 (21 canonical + 88 plugin-only + 4 OpenClaw)
- **Agentes:** 48 especializados en gestión de proyectos
- **Activa con:** `/pm:init` `/pm:run-auto` `/pm:charter`

### MetodologIA (MAO) — `plugins/metodologia/metodologia-discovery-framework/`
- **Identidad:** MAO — MetodologIA de Aprovechamiento de Oportunidades
- **Skills:** 115 (73 canonical + 38 plugin-only + 4 OpenClaw)
- **Agentes:** 101 especializados en discovery y consultoría
- **Activa con:** `/mao:run-auto` `/mao:discovery` `/mao:arch`

---

## Capstone: OpenClaw Security Kit (5022–5025)

El último hito de este milestone — 4 skills que cierran el ciclo de seguridad:

| Skill | Resuelve |
|-------|---------|
| `5022-open-claude-security` | Diseño completo de arquitectura segura para Claude Code |
| `5023-openclaw-isolation` | Aislamiento Docker con cap_drop ALL + red interna |
| `5024-openclaw-tool-auth` | Gates PreToolUse + scripts Python fail-closed |
| `5025-openclaw-personal-deploy` | Despliegue personal guiado en 5 fases |

---

## Governance

```
governance/
├── moat-dashboard.md          # Estado MOAT de todos los skills
├── moat-status.csv            # Export CSV con métricas por skill
└── moat-audit.sh              # Script de auditoría (19 checks)

scripts/
├── skill-sync.sh              # Sincronización canonical → plugins
├── moat-audit.sh              # MOAT certification runner
├── lazy-load-resolver.sh      # L1/L2/L3 loading per skill
└── secrets-scan.sh            # Gate G0 — secretos expuestos
```

### MOAT Definition of Done

Un skill es **MOAT** cuando cumple todos estos criterios:

- [ ] M1: `evals/evals.json` existe con ≥5 casos de prueba
- [ ] M2: Al menos 1 false-positive + 1 edge case en evals
- [ ] M3: Al menos 1 archivo en `references/` con ≥20 líneas
- [ ] M4: `SKILL.md` sigue Template A (frontmatter + ≥6 secciones)
- [ ] M5: ≥80% de claims con evidencia `[EXPLICIT]` `[INFERRED]` `[OPEN]`

---

## Estructura del Repositorio

```
jm-labs/
├── README.md                  # Este archivo — hub del milestone
├── CLAUDE.md                  # Instrucciones de repositorio
├── skills/
│   ├── javier-montano/        # 513 skills canónicos (0001–9128)
│   └── metodologia/           # 62 skills canónicos MetodologIA
├── plugins/
│   ├── javier-montano/
│   │   ├── sovereign-architect/     # SA plugin (134 skills)
│   │   └── pm-project-framework/    # PM plugin (113 skills)
│   └── metodologia/
│       └── metodologia-discovery-framework/  # MAO plugin (115 skills)
├── governance/
│   ├── moat-dashboard.md
│   └── moat-status.csv
└── scripts/
    ├── skill-sync.sh
    ├── moat-audit.sh
    └── lazy-load-resolver.sh
```

---

## Brand Map

| Brand | Repositorio | Licencia | Scope |
|-------|-------------|---------|-------|
| **JM Labs** | `javiermontano-sofka/jm-labs` | MIT | Canónico master |
| **MetodologIA** | `KatherinOquendo/MetodologIA` | GPL-3.0 | Discovery público |
| **JM Shared** | `KatherinOquendo/jm-labs-shared` | MIT | Skills compartidos |

---

## Links Rápidos

- [Landing interactivo](landing.html) — Navegación visual del ecosistema
- [Prompt Library](prompt-library.html) — 10 prompts + 10 meta-prompts
- [MOAT Dashboard](governance/moat-dashboard.md) — Estado de certificación
- [Sovereign Architect](plugins/javier-montano/sovereign-architect/CLAUDE.md) — SA plugin
- [PMO-APEX](plugins/javier-montano/pm-project-framework/CLAUDE.md) — PM plugin
- [MetodologIA](plugins/metodologia/metodologia-discovery-framework/CLAUDE.md) — MAO plugin

---

*JM Labs Canonical Registry v1.0 — Centralizado. Certificado. Sincronizado.*
*Una fuente de verdad para profesionales con soberanía técnica.*
*GPL-3.0 (MetodologIA) · MIT (JM Labs) · © 2026 Javier Montaño.*
