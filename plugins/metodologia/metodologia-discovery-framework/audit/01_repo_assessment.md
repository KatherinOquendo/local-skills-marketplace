# 01 — Repository Assessment

> Auditoría estructural del repositorio Metodología-Discovery-Framework (MAO v1.4)
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)

---

## TL;DR

El framework MAO es un sistema de discovery con 111 skills, 101 agentes, 109 comandos y 19 scripts, orquestado por un pipeline de 10 fases con 4 quality gates. La arquitectura es ambiciosa y bien diseñada en su núcleo, pero presenta un problema sistémico crítico: **101 de 111 SKILL.md contienen tokens de marca prohibidos** (#6366F1, #0F172A, Montserrat) que contradicen las propias reglas del framework. La infraestructura (hooks, scripts, ontología) es sólida. El gap principal está entre la calidad del núcleo (gold-standard) y la calidad de la periferia (batch-generated con contaminación legacy).

---

## 1. Estructura del Repositorio

```
plugins/metodologia/metodologia-discovery-framework/
├── .claude-plugin/plugin.json          # Metadata del plugin (v1.4.0, MIT)
├── CLAUDE.md                           # Hub de instrucciones (217 líneas)
├── README.md                           # Documentación pública (294 líneas)
├── CHANGELOG.md                        # Historial de cambios
├── plan.md                             # Plan de mejora v9.0 (9 workstreams)
├── settings.json                       # Config (agent: discovery-conductor)
├── landing.html                        # Landing interactivo
├── prompt-library.html                 # Catálogo searchable de prompts
├── agents/                             # 101 agentes especializados (.md)
├── commands/                           # 109 comandos (.md)
├── skills/                             # 111 directorios de skills
│   └── {skill-name}/
│       ├── SKILL.md                    # Definición canónica
│       ├── references/                 # Material de soporte
│       ├── examples/                   # Samples (README.md + sample-output.html)
│       ├── prompts/                    # Prompts específicos
│       └── agents/                     # Agentes asignados (opcional)
├── references/
│   ├── ontology/                       # 13 archivos de ontología viva
│   ├── priming-rag/                    # ~32 documentos de conocimiento RAG
│   ├── engagement-templates/           # Templates de engagement
│   ├── assets/                         # Logos SVG, brand materials
│   ├── brand-config-neoswiss.json      # Single Source of Truth de tokens
│   ├── neo-swiss-template.css          # CSS canónico (488 líneas)
│   ├── master-index.md                 # Índice de navegación (78KB)
│   ├── service-type-matrix.md          # Routing por tipo de servicio
│   └── design-system-*.md             # Versiones del design system
├── hooks/hooks.json                    # 6 hooks SessionStart + 3 PostToolUse
├── scripts/                            # 19 shell scripts
├── prompts/versions/                   # v0 (legacy) + v1 (actual, 5 archivos)
└── .discovery/                         # Templates y samples de marca
```

---

## 2. Modelo Operativo

### Filosofía
- **MAO** = MetodologIA de Aprovechamiento de Oportunidades
- **"Método + TecnologIA = Soberanía"**
- **P.I.V.O.T.E.**: Personas, Interacciones, Valor → Organización, Tecnología, Evolución
- 4 meta-fases: FUNDAMENTAR → ACELERAR → CATALIZAR → AMPLIFICAR
- 4 niveles de madurez: Orgánica (1x) → Convencional (1.2x) → Aumentada (2-5x) → Apalancada (10-100x)

### Pipeline de Discovery (10 fases)
| Fase | Entregable | Skill principal |
|------|-----------|----------------|
| 00 | Discovery Plan | discovery-orchestrator |
| 01 | Stakeholder Map | stakeholder-mapping |
| 02 | Brief Técnico | input-analysis |
| 03 | Análisis AS-IS | asis-analysis |
| 04 | Mapeo de Flujos | flow-mapping |
| **G1** | **Gate Post-Escenarios** | |
| 05 | Escenarios ToT | scenario-analysis |
| 05b | Feasibility Think Tank | multidimensional-feasibility |
| **G1.5** | **Gate Post-Feasibility** | |
| 06 | Solution Roadmap | solution-roadmap |
| **G2** | **Gate Post-Roadmap** | |
| 07 | Spec Funcional | functional-spec |
| 08 | Pitch Ejecutivo | executive-pitch |
| 09 | Handover Operativo | discovery-handover |
| **G3** | **Gate Final** | |
| 10-14 | Reportes | Varios |

### 10 Tipos de Servicio
SDA (default), QA, Management, RPA, Data-AI, Cloud, SAS, UX-Design, Digital-Transformation, Multi-Service

### Quality Gates
- **G1**: Scoring 6D completo, <40% supuestos
- **G1.5**: ≥5/7 votos Go del Think Tank
- **G2**: FTE-meses validados, Monte Carlo ejecutado
- **G3**: Consistencia cruzada, Excellence loop ≥8/10

### Protocolo Zero-Hallucination
Etiquetas obligatorias: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` `[STAKEHOLDER]`
Si >30% `[SUPUESTO]` → banner de advertencia obligatorio.

---

## 3. Convenciones Declaradas vs Observadas

| Convención declarada | Observada | Estado |
|---------------------|-----------|--------|
| Design System Neo-Swiss v6 (#122562, #FFD700) | 101/111 SKILL.md usan tokens legacy (#6366F1) | **VIOLADA** |
| Tokens prohibidos: #6366F1, Montserrat, etc. | Presentes en 101 SKILL.md + samples HTML + references | **VIOLADA** |
| Skills en inglés (internals) | Mezclado: gold-standard en inglés, batch-generated en español | **PARCIAL** |
| Output en español (latam business) | Consistente en outputs | **OK** |
| SKILL.md + references/ + scripts/ + evals/ | evals/ no existe en ninguna skill | **INCOMPLETA** |
| Evidence tags en toda afirmación | Solo en prompts y ontología, no en skills | **PARCIAL** |
| Ghost menu en cada artefacto importante | Referenciado pero no verificable sin ejecución | **NO VERIFICABLE** |
| Changelog automático | hooks.json lo implementa correctamente | **OK** |
| RAG priming al inicio de sesión | hooks.json lo implementa correctamente | **OK** |
| 108 skills MOAT (skills-catalog.md) | 111 directorios en skills/ | **INCONSISTENTE** |

---

## 4. Inconsistencias Estructurales Detectadas

### 4.1 Contaminación de tokens legacy (CRÍTICO)
- **101 de 111** SKILL.md contienen `#6366F1`, `#0F172A`, o `Montserrat` en sus output templates
- Esto contradice CLAUDE.md líneas 158-161 que los lista como "Tokens PROHIBIDOS (Legacy)"
- Solo 10 skills están limpias: adoption-strategy, ai-center-discovery, architecture-tobe, bi-analytics-discovery, bi-architecture, change-readiness-assessment, client-browser-audit, cross-platform-convert, discovery-retrospective, input-analysis
- La contaminación también afecta 335 archivos totales (HTML samples, references, agents)

### 4.2 Discrepancia en conteo de skills
- CLAUDE.md línea 6: "111 skills MOAT"
- skills-catalog.md título: "Catálogo de 108 Skills"
- skills-catalog.md tabla resumen: Total = 108
- Directorio skills/: 111 carpetas
- **3 skills no documentadas en catálogo**: necesita reconciliación

### 4.3 Archivos vacíos en raíz del repositorio
- `changelog.md`, `index.md`, `log.md`, `tasklog.md` — todos vacíos
- Patrón repetido en subdirectorios del repo

### 4.4 Ausencia de evals/
- CLAUDE.md raíz del repo dice "Skills follow Anthropic gold standard: SKILL.md + references/ + scripts/ + evals/"
- Ninguna skill tiene directorio evals/
- Ninguna skill tiene scripts/ propios (los scripts están centralizados)

### 4.5 Pipeline-orchestration.md usa tokens legacy
- El diagrama Mermaid en `references/ontology/pipeline-orchestration.md` (línea 38-41) usa `#22D3EE` y `#1A1A2E` — ambos prohibidos

### 4.6 Frontmatter inconsistente
- Skills gold-standard usan: name, description, author, argument-hint, model, context, allowed-tools
- Skills batch-generated usan: name, description, author, version, license, category, tags, allowed-tools
- No hay estándar único de frontmatter

### 4.7 Grounding Guideline vs Guiding Principle
- Skills gold-standard alternan entre "Grounding Guideline" (español) y "Guiding Principle" (inglés)
- No hay convención declarada sobre cuál usar

---

## 5. Fortalezas del Framework

1. **Ontología viva bien diseñada**: 13 archivos especializados con separación clara de responsabilidades
2. **Quality gates formalizados**: 4 gates con criterios explícitos, umbrales y acciones de remediación
3. **Pipeline secuencial robusto**: 10 fases con dependencias claras y skill assignments
4. **Hooks funcionales**: 6 SessionStart + 3 PostToolUse con guard de plugin activo
5. **Progressive MOAT loading**: L1/L2/L3 para optimización de contexto (lazy-load-resolver.sh bien implementado)
6. **Multi-servicio**: 10 tipos de servicio con routing automático
7. **Comité dinámico**: 101 agentes en 5 niveles de activación con spawning formalizado
8. **Plan de mejora activo**: plan.md v9.0 con 9 workstreams y estado de avance
9. **Brand system completo**: brand-config-neoswiss.json como SSoT + CSS canónico
10. **Cobertura de dominios amplia**: 11 dominios funcionales cubiertos

---

## 6. Debilidades del Framework

1. **Contaminación legacy masiva**: 91% de skills violando las propias reglas de marca
2. **Brecha gold-standard vs batch**: ~20 skills son gold-standard, ~91 son batch-generated con menor profundidad
3. **Sin evals/**: No hay evaluaciones de calidad por skill
4. **Sin scripts/ por skill**: Centralización total en scripts/
5. **Catálogo desactualizado**: skills-catalog.md no refleja las 111 skills reales
6. **Frontmatter sin estándar**: Dos patrones incompatibles coexisten
7. **Idioma mixto**: "Grounding Guideline" vs "Guiding Principle" sin convención
8. **Archivos placeholder vacíos**: changelog.md, index.md en múltiples niveles

---

## 7. Estado de Completitud

| Componente | Cantidad | Completitud | Calidad |
|-----------|----------|-------------|---------|
| Skills | 111 | 100% (111/111 tienen SKILL.md) | Variable (20 gold, 91 batch) |
| Agentes | 101 | 100% | Uniforme |
| Comandos | 109 | 100% | No auditados en detalle |
| Scripts | 19 | 100% | Bien estructurados |
| Ontología | 13 | 100% | Alta calidad |
| Hooks | 9 | 100% | Funcionales |
| RAG priming | ~32 | 100% | No auditados en detalle |
| Prompts v1 | 5 | 100% | No auditados en detalle |
| Design system | 3 archivos | 100% (JSON+CSS+MD) | Bien definido |
| evals/ | 0 | 0% | **NO EXISTE** |

---

*Entregable 01 de 07 — Auditoría MAO v1.4*
