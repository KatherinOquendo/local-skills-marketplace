# 04 — Critical Path Improvement Plan

> Ruta crítica priorizada para robustecer el Metodología-Discovery-Framework (MAO v1.4)
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)

---

## Principio de Priorización

1. **Primero lo que desbloquea más**: Skills palanca antes que skills hoja.
2. **Primero lo sistémico**: Un cambio que arregla 101 archivos > un cambio que arregla 1.
3. **Primero lo reversible**: Quick wins antes que rediseños.
4. **Primero la marca**: Corregir tokens legacy antes que agregar features.

---

## Ruta Crítica

```
Fase 0: Token Cleanup (sistémico, 101+ archivos)
  ↓
Fase 1: Frontmatter Standardization (sistémico, 111 archivos)
  ↓
Fase 2: Skills Palanca Upgrade (5 skills críticas)
  ↓
Fase 3: Ontología Sync (catálogo, pipeline diagram)
  ↓
Fase 4: Batch Skill Elevation (67 skills batch → gold-standard)
  ↓
Fase 5: Evals & Quality Gates internos
```

---

## Fase 0: Token Cleanup (QUICK WIN — Mayor ROI)

**Qué**: Reemplazar tokens legacy (#6366F1 → #122562, #0F172A → #1F2833, Montserrat → Poppins) en 101 SKILL.md + ~100 HTML samples + references + agents.

**Por qué**: 91% de skills generan entregables con marca incorrecta. Es la deuda más visible y más fácil de pagar.

**Desbloquea**: Todos los entregables generados desde skills afectadas salen con marca correcta.

**Esfuerzo**: S (script de find-and-replace batch)

**Impacto**: Crítico — corrige output visual de TODOS los entregables.

**Dependencias**: Ninguna.

**Riesgo**: Bajo — cambio mecánico, verificable con grep.

### Mapeo de reemplazos
| Token Legacy | Token Correcto | Contexto |
|-------------|---------------|---------|
| `#6366F1` | `#122562` | Navy (hero bg, headers, table headers) |
| `#0F172A` | `#1F2833` | Dark (body text) |
| `#1A1A2E` | `#1F2833` | Dark alt (body text) |
| `#22D3EE` | `#FFD700` | Accent (success, highlights) |
| `#0A122A` | `#1F2833` | Deep dark (body text) |
| `Montserrat` | `Poppins` | Heading font |
| `Clash Grotesk` | `Poppins` | Heading font alt |
| `Inter` | `Trebuchet MS` | Body font |

---

## Fase 1: Frontmatter Standardization

**Qué**: Estandarizar frontmatter de todas las skills al patrón gold-standard:
```yaml
---
name: metodologia-{skill-name}
description: >
  Trigger description...
argument-hint: "..."
author: Javier Montano · Comunidad MetodologIA
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---
```

**Por qué**: Frontmatter con `model: opus` y `context: fork` ejecuta la skill en subagente con modelo Opus. Sin estos campos, la skill corre en el modelo por defecto y en contexto compartido.

**Desbloquea**: Ejecución consistente de todas las skills.

**Esfuerzo**: M (script + revisión manual de descriptions)

**Impacto**: Alto — cada skill se ejecuta con el modelo y contexto correctos.

**Dependencias**: Fase 0 (tokens limpios primero para no mezclar cambios).

---

## Fase 2: Skills Palanca Upgrade

**Qué**: Elevar las 5 skills palanca a Referente (90+):

| Skill | Score Actual | Target | Cambio Principal |
|-------|:---:|:---:|-----|
| discovery-orchestrator | 95 | 98 | Reconciliar catálogo (dice 59 skills, hay 111). Agregar evals/. |
| output-engineering | 85 | 92 | Agregar Grounding Guideline (tiene "Guiding Principle"). Verificar format routing completo. |
| design-system-brand | 88 | 93 | Agregar evals/. Verificar token consistency con brand-config-neoswiss.json. |
| input-analysis | 86 | 92 | Agregar author field. Agregar evals/. |
| html-brand | 91 | 95 | Agregar evals/. Verificar WCAG AA en sample output. |

**Por qué**: Estas skills son invocadas por o afectan a todas las demás. Mejorarlas mejora el output de todo el framework.

**Desbloquea**: Referente como modelo para el upgrade batch de Fase 4.

**Esfuerzo**: M (5 skills, mejoras quirúrgicas)

**Impacto**: Alto — cascade effect sobre todas las skills dependientes.

**Dependencias**: Fase 0 + Fase 1 completadas.

---

## Fase 3: Ontología Sync

**Qué**:
1. Actualizar skills-catalog.md: 108 → 111 skills
2. Actualizar pipeline-orchestration.md: corregir tokens Mermaid (#22D3EE → #FFD700)
3. Actualizar discovery-orchestrator SKILL.md: catálogo interno dice 59 skills
4. Reconciliar CLAUDE.md: confirmar "111 skills MOAT" consistente

**Por qué**: La ontología es la fuente de verdad. Si dice 108 cuando hay 111, el orquestador no conoce 3 skills.

**Esfuerzo**: S

**Impacto**: Medio — consistencia de la fuente de verdad.

**Dependencias**: Fase 0 (para incluir token fix del Mermaid).

---

## Fase 4: Batch Skill Elevation

**Qué**: Upgrade de ~67 skills batch-generated a estructura gold-standard:

Para cada skill batch:
1. Agregar **Grounding Guideline** (2-3 líneas filosóficas contextual al dominio)
2. Agregar **When NOT to Use** section
3. Agregar **Inputs** section con parámetros MODO/FORMATO/VARIANTE
4. Agregar **Conditional Logic** (al menos un IF/THEN por contexto detectado)
5. Agregar **Assumptions & Limits**
6. Agregar **Delivery Structure** (secciones numeradas del output)
7. Estandarizar **naming**: "Grounding Guideline" (no "Guiding Principle")

**Por qué**: Eleva el piso de calidad del framework de ~66 a ~80.

**Esfuerzo**: L (67 skills × ~30 min = ~33 horas estimadas)

**Impacto**: Transformativo — uniformiza el framework.

**Dependencias**: Fase 2 (skills palanca como modelo) + Fase 0 + Fase 1.

**Estrategia de ejecución**: Usar `assembly-skill` (x-ray → surgeon → certify) del IDE en batches de 5-10 skills por dominio.

---

## Fase 5: Evals & Quality Gates Internos

**Qué**: Crear evals/ para al menos las 5 skills palanca y un template reutilizable.

**Por qué**: Sin evals no hay verificación automatizada de calidad. Cualquier mejora puede degradarse sin detección.

**Esfuerzo**: L

**Impacto**: Medio-Alto a largo plazo.

**Dependencias**: Todas las fases anteriores.

---

## Top 10 Mejoras de Mayor ROI

| # | Mejora | Esfuerzo | Impacto | ROI |
|---|--------|:---:|:---:|:---:|
| 1 | **Batch token replacement** en 101 SKILL.md | S | Crítico | **Máximo** |
| 2 | **Batch token replacement** en ~100 HTML samples | S | Alto | **Muy alto** |
| 3 | **Estandarizar frontmatter** (agregar model/context) en ~67 skills | M | Alto | **Alto** |
| 4 | **Actualizar skills-catalog.md** (108 → 111) | S | Medio | **Alto** |
| 5 | **Corregir tokens Mermaid** en pipeline-orchestration.md | S | Bajo | **Alto** |
| 6 | **Agregar Grounding Guideline** a ~67 skills batch | L | Alto | **Medio** |
| 7 | **Crear evals/** para 5 skills palanca | M | Alto | **Medio** |
| 8 | **Agregar conditional logic** a ~67 skills batch | L | Alto | **Medio** |
| 9 | **Upgrade discovery-orchestrator** catálogo interno (59 → 111) | S | Medio | **Medio** |
| 10 | **Regenerar HTML samples** con tokens correctos | M | Medio | **Medio** |

---

## Skills que Deben Convertirse en Palancas de Mejora de Otras Skills

### Del framework MAO (internas)

| Skill | Rol como palanca |
|-------|-----------------|
| **discovery-orchestrator** | Define el flujo de todas las demás skills. Si lista 59, solo orquesta 59. |
| **output-engineering** | Controla el formato de output. Si mejora, todos los outputs mejoran. |
| **design-system-brand** | Provee tokens de marca. Si se corrige, corrige la marca de todo. |
| **input-analysis** | Pre-procesa inputs. Mejora la calidad de entrada de todo el pipeline. |
| **html-brand** | Template para HTML. Mejora impacta todos los entregables HTML. |

### Del entorno Claude Code (externas)

| Skill IDE | Uso como palanca |
|-----------|-----------------|
| **assembly-skill** | Pipeline x-ray → surgeon → certify para batch upgrade de 67 skills |
| **surgeon-skill** | Mejoras automatizadas por skill (agregar Grounding Guideline, conditional logic) |
| **certify-skill** | Verificación post-mejora |
| **x-ray-skill** | Diagnóstico pre-mejora |

### Estrategia de Orquestación

```
Para cada batch de 5-10 skills:
1. x-ray-skill → diagnóstico individual
2. surgeon-skill → aplicar mejoras (tokens, frontmatter, Grounding Guideline)
3. certify-skill → verificar que alcanza CERTIFIED
4. Si no certifica → iterar surgeon-skill con hallazgos específicos
```

---

## REC-GO / REC-NO-GO

### REC-GO (proceder)
- **Fase 0** (token cleanup): Proceder inmediatamente. Riesgo cero, impacto máximo.
- **Fase 1** (frontmatter): Proceder después de Fase 0. Riesgo bajo.
- **Fase 3** (ontología sync): Proceder en paralelo con Fase 1.
- **Skills palanca** (Fase 2): Proceder después de Fase 0+1.

### REC-NO-GO (no proceder todavía)
- **Fase 4** (batch elevation de 67 skills): NO proceder sin primero completar Fases 0-2 y tener evals mínimos. Riesgo de degradar skills sin forma de detectarlo.
- **Modificar hooks.json**: NO tocar sin testing. Los hooks son funcionales y un cambio erróneo rompe la automatización de sesión.
- **Eliminar archivos placeholder vacíos** (changelog.md, index.md): NO eliminar sin confirmar que no son parte de una convención del repo padre.
- **Modificar plan.md v9.0**: NO modificar. Es un plan activo del autor. Coordinar, no sobreescribir.

---

*Entregable 04 de 07 — Auditoría MAO v1.4*
