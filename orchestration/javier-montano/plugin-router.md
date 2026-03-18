# Plugin Router — Detección de Contexto y Activación de Plugins

## Cascada de Detección (orden de prioridad)

1. **Prefijo explícito**: `/sdf:`, `/mao:`, `/pm:`, `/jm:` → Plugin correspondiente
2. **Working directory**:
   - `~/skills/plugins/sofka-*` o `discovery/` presente → Sofka (SDF)
   - `~/skills/plugins/metodologia-*` → MetodologIA (MAO)
   - `~/skills/plugins/pm-*` o `project/` presente → PMO-APEX (PM)
   - `~/personal/` o `~/jm-labs/` → JM Labs (JM)
3. **Keywords en input**:
   - "client", "discovery", "pre-sales", nombres de clientes → Sofka
   - "open source", "copyleft", "community", "MetodologIA" → MetodologIA
   - "project management", "PMO", "steering", "governance" → PM-APEX
   - "blog", "talk", "experiment", "personal project" → JM Labs
4. **Si ambiguo después de señales** → Preguntar: "¿Qué contexto? Sofka / MetodologIA / PM / JM Labs"

## Plugin Registry

| Plugin | Prefix | Directory | Conductor | Session Dir | Version |
|--------|--------|-----------|-----------|-------------|---------|
| **SDF** | `/sdf:` | `~/skills/plugins/sofka-discovery-framework/` | `discovery-conductor` | `discovery/` | v12.3 |
| **MAO** | `/mao:` | `~/skills/plugins/metodologia-discovery-framework/` | `discovery-conductor` | `discovery/` | v1.4 |
| **PM** | `/pm:` | `~/skills/plugins/pm-project-framework/` | `pm-conductor` | `project/` | v1.0 |
| **JM** | `/jm:` | TBD | TBD | TBD | TBD |

## Asset Locations

| Location | Purpose |
|----------|---------|
| `~/skills/plugins/sofka-discovery-framework/` | Sofka SAGE plugin (proprietary) |
| `~/skills/plugins/metodologia-discovery-framework/` | MetodologIA plugin (GPL-3.0) |
| `~/skills/plugins/pm-project-framework/` | PMO-APEX plugin (proprietary) |
| `~/skills/sofka-skills/` | Packaged .skill + .plugin files |
| `~/.claude/skills/` | Global skills (available everywhere) |
| `~/.claude/agents/` | Global agents |
| `~/.claude/orchestration/` | Meta-orchestration network |

## Command Cheat Sheets

### SDF (Sofka Discovery)
```
RUN       /sdf:run-guided  /sdf:run-auto  /sdf:run-express  /sdf:run-deep
GENERATE  /sdf:generate-plan  /sdf:generate-brief  /sdf:diagnose-asis
          /sdf:trace-flows  /sdf:evaluate-scenarios  /sdf:validate-feasibility
          /sdf:chart-roadmap  /sdf:write-spec  /sdf:craft-pitch  /sdf:deliver-handover
REPORT    /sdf:present-findings  /sdf:report-tech  /sdf:report-func
          /sdf:review-business  /sdf:discover-ai
ASSESS    /sdf:assess-architecture  /sdf:assess-data  /sdf:assess-cloud
          /sdf:assess-security  /sdf:assess-change
OPS       /sdf:audit-quality  /sdf:improve-deliverables  /sdf:rescue-stalled
UX        /sdf:menu  /sdf:a  /sdf:demo
```
Aliases: `asis`, `auto`, `guide`, `arch`, `tech`, `func`, `biz`, `ai`, `audit`, `improve`, `rescue`

### MAO (MetodologIA)
```
RUN       /mao:run-guided  /mao:run-auto  /mao:run-express  /mao:run-deep
GENERATE  /mao:generate-plan  /mao:generate-brief  /mao:diagnose-asis
          /mao:trace-flows  /mao:evaluate-scenarios  /mao:validate-feasibility
          /mao:chart-roadmap  /mao:write-spec  /mao:craft-pitch
BRAND     /mao:brand-publish  /mao:html-brand  /mao:design-system-brand
SERVICE   /mao:rpa-discovery  /mao:qa-discovery  /mao:ai-discovery
          /mao:cloud-discovery  /mao:ux-discovery  /mao:management-discovery
UX        /mao:menu  /mao:a  /mao:demo
```

### PM-APEX (Project Management)
```
RUN       /pm:run-guided  /pm:run-auto  /pm:run-express  /pm:run-deep
GENERATE  /pm:generate-charter  /pm:map-stakeholders  /pm:define-scope
          /pm:plan-schedule  /pm:plan-resources  /pm:assess-risks
          /pm:convene-steering  /pm:design-methodology  /pm:deliver-kickoff
REPORT    /pm:report-status  /pm:report-evm  /pm:report-lessons
          /pm:review-pmo  /pm:close-project
ASSESS    /pm:assess-agile  /pm:assess-waterfall  /pm:assess-safe
          /pm:assess-pmo  /pm:assess-governance  /pm:assess-vendor
CEREMONY  /pm:standup  /pm:retro  /pm:sprint-review  /pm:sprint-planning
TRACK     /pm:track-burndown  /pm:track-velocity  /pm:track-budget
          /pm:track-risks  /pm:track-milestones  /pm:track-team-health
OPS       /pm:init  /pm:prime-project
UX        /pm:menu  /pm:a  /pm:demo
```

## Protocolo de Activación

Al detectar contexto de plugin:

1. **Leer** plugin CLAUDE.md (hub del plugin)
2. **Verificar** `session-state.json` — ¿hay sesión activa?
3. **Ejecutar** hooks de SessionStart (si sesión nueva)
4. **Cargar** conductor del plugin + tríada permanente
5. **Handoff** — meta-orchestrator entra en modo supervisión

## Extensibilidad

Para agregar un nuevo plugin:
1. Crear directorio en `~/skills/plugins/{nombre}-framework/`
2. Agregar fila a la tabla Plugin Registry (arriba)
3. Crear CLAUDE.md del plugin con ontology propia
4. Crear hooks/hooks.json con scripts de sesión
5. El meta-orchestrator lo detectará via working directory o prefijo
