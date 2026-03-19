# 05 — Skill-by-Skill Upgrade Specifications

> Especificaciones de mejora por skill para el Metodología-Discovery-Framework (MAO v1.4)
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)

---

## Organización

Las specs se agrupan por tier y prioridad, no por orden alfabético. Se detallan las 5 skills palanca y las 5 skills batch evaluadas en profundidad. Para las ~67 batch restantes se provee una spec genérica reutilizable.

---

## Grupo A: Skills Palanca (5 skills — Prioridad Máxima)

### A1. discovery-orchestrator

**Ruta**: `skills/discovery-orchestrator/SKILL.md`
**Score actual**: 95 | **Target**: 98

**Diagnóstico**: Skill referente del framework. Estructura impecable. Dos problemas: (1) catálogo interno lista 59 skills cuando hay 111, (2) tokens legacy en output templates, (3) sin evals/.

**Problemas detectados**:
1. Línea 56: "Skill Catalog (59 skills across 9 domains)" — debería decir 111 skills across 11 domains
2. Tokens legacy en output templates (secciones profundas del archivo)
3. Sin directorio evals/

**Cambios concretos**:
- [ ] Actualizar catálogo interno: 59 → 111 skills, 9 → 11 dominios
- [ ] Reemplazar tokens legacy en output templates
- [ ] Crear `evals/eval-orchestrator.md` con criterios de validación
- [ ] Verificar consistencia con skills-catalog.md actualizado

**Criterio de aceptación**: Score ≥ 98. Catálogo interno = skills-catalog.md = 111. Zero tokens legacy. Evals presente.

---

### A2. output-engineering

**Ruta**: `skills/output-engineering/SKILL.md`
**Score actual**: 85 | **Target**: 92

**Diagnóstico**: Buen orquestador de formatos con Auto-Brand Protocol y format routing. Usa "Guiding Principle" en vez de "Grounding Guideline". Tokens legacy en output templates.

**Problemas detectados**:
1. "Guiding Principle" → debería ser "Grounding Guideline"
2. Tokens legacy en secciones de output templates
3. Sin evals/

**Cambios concretos**:
- [ ] Renombrar "Guiding Principle" → "Grounding Guideline"
- [ ] Reemplazar tokens legacy
- [ ] Agregar evals/eval-output-engineering.md
- [ ] Verificar que format routing cubre los 6 formatos (HTML, DOCX, PPTX, XLSX, PDF, MD)

**Criterio de aceptación**: Score ≥ 92. "Grounding Guideline" presente. Zero tokens legacy.

---

### A3. design-system-brand

**Ruta**: `skills/design-system-brand/SKILL.md`
**Score actual**: 88 | **Target**: 93

**Diagnóstico**: Skill de design system con paleta Neo-Swiss correcta en el cuerpo principal, pero tokens legacy en secciones de output templates (la sección de generación de outputs para otros formatos).

**Problemas detectados**:
1. Tokens legacy en output template sections
2. Sin evals/
3. Podría incluir validación explícita contra brand-config-neoswiss.json

**Cambios concretos**:
- [ ] Limpiar tokens legacy en output templates
- [ ] Agregar sección "Validation Protocol" que verifica contra brand-config-neoswiss.json
- [ ] Crear evals/eval-design-system.md
- [ ] Agregar "When NOT to Use" section

**Criterio de aceptación**: Score ≥ 93. Zero tokens legacy. Validation protocol presente.

---

### A4. input-analysis

**Ruta**: `skills/input-analysis/SKILL.md`
**Score actual**: 86 | **Target**: 92

**Diagnóstico**: Skill sofisticada con 5-pass methodology. Sin tokens legacy (una de las 10 limpias). Falta author field en frontmatter.

**Problemas detectados**:
1. Sin `author:` en frontmatter
2. Sin `model:` y `context:` en frontmatter
3. Sin evals/
4. Sin "Grounding Guideline" explícito (tiene "Assumptions & Limits" pero no filosofía)

**Cambios concretos**:
- [ ] Agregar `author: Javier Montano · Comunidad MetodologIA`
- [ ] Agregar `model: opus` y `context: fork`
- [ ] Agregar "Grounding Guideline" section
- [ ] Crear evals/eval-input-analysis.md

**Criterio de aceptación**: Score ≥ 92. Frontmatter completo. Grounding Guideline presente.

---

### A5. html-brand

**Ruta**: `skills/html-brand/SKILL.md`
**Score actual**: 91 | **Target**: 95

**Diagnóstico**: Skill referente para HTML con Neo-Swiss v6. Tokens legacy en output templates (paradójicamente, la skill que define la marca correcta tiene tokens incorrectos en su propia config de outputs).

**Problemas detectados**:
1. Tokens legacy en secciones de output template
2. Sin evals/
3. Sample output HTML podría verificar WCAG AA automáticamente

**Cambios concretos**:
- [ ] Limpiar tokens legacy
- [ ] Crear evals/eval-html-brand.md con checklist WCAG AA
- [ ] Verificar que sample-output.html usa tokens correctos

**Criterio de aceptación**: Score ≥ 95. Zero tokens legacy. Evals presente. Sample HTML correcto.

---

## Grupo B: Skills Batch Evaluadas en Profundidad (5 skills)

### B1. secrets-sanitization

**Ruta**: `skills/secrets-sanitization/SKILL.md`
**Score actual**: 70 | **Target**: 82

**Diagnóstico**: Skill funcional con patrón batch-generated. Sin Grounding Guideline. Output templates con tokens legacy. Frontmatter batch (version, license, category, tags).

**Cambios concretos**:
- [ ] Reemplazar tokens legacy en output templates
- [ ] Migrar frontmatter a gold-standard (agregar model, context, argument-hint; quitar version, license, category, tags)
- [ ] Agregar "Grounding Guideline" (ej: "Un secreto expuesto no es un bug — es una brecha de confianza")
- [ ] Agregar "When NOT to Use" section
- [ ] Agregar "Inputs" section con parámetros MODO/FORMATO
- [ ] Agregar "Assumptions & Limits"

**Criterio de aceptación**: Score ≥ 82. Estructura gold-standard. Zero tokens legacy.

---

### B2. context-optimization

**Ruta**: `skills/context-optimization/SKILL.md`
**Score actual**: 67 | **Target**: 80

**Cambios concretos**: Mismo patrón que B1:
- [ ] Tokens legacy → correctos
- [ ] Frontmatter → gold-standard
- [ ] Agregar Grounding Guideline
- [ ] Agregar When NOT to Use
- [ ] Agregar Inputs con MODO/FORMATO
- [ ] Agregar Assumptions & Limits

---

### B3. poc-lab

**Ruta**: `skills/poc-lab/SKILL.md`
**Score actual**: 67 | **Target**: 80

**Cambios específicos adicionales**:
- [ ] Reemplazar TL;DR con Grounding Guideline (ej: "Una PoC sin hipótesis es una demo disfrazada de validación")
- [ ] Agregar conditional logic para scope de PoC (1 sprint vs multi-sprint)

---

### B4. rendering-engine

**Ruta**: `skills/rendering-engine/SKILL.md`
**Score actual**: 66 | **Target**: 80

**Cambios específicos adicionales**:
- [ ] CRÍTICO: Output templates tienen tokens legacy prominentes (línea 29: #6366F1, #0F172A, Montserrat)
- [ ] Agregar "Branding Rules" section completa con tokens Neo-Swiss v6
- [ ] Considerar si esta skill es redundante con output-engineering

---

### B5. cross-platform-convert

**Ruta**: `skills/cross-platform-convert/SKILL.md`
**Score actual**: 64 | **Target**: 78

**Cambios específicos adicionales**:
- [ ] No tiene tokens legacy (una de las 10 limpias)
- [ ] Agregar Grounding Guideline
- [ ] Agregar validation que conversión preserva semántica

---

## Grupo C: Spec Genérica para ~67 Skills Batch Restantes

### Template de Upgrade Batch → Gold-Standard

Para cada skill batch-generated, aplicar estos cambios en orden:

#### Paso 1: Token Cleanup
```
Reemplazar en SKILL.md:
  #6366F1 → #122562
  #0F172A → #1F2833
  #1A1A2E → #1F2833
  #22D3EE → #FFD700
  Montserrat → Poppins
  Clash Grotesk → Poppins
  Inter → Trebuchet MS
```

#### Paso 2: Frontmatter Migration
```yaml
# QUITAR estos campos:
version: X.X.X
license: MIT
category: ...
tags: [...]

# AGREGAR estos campos:
argument-hint: "..."
model: opus
context: fork

# VERIFICAR que existan:
name: metodologia-{skill-name}
description: > (multi-line trigger description)
author: Javier Montano · Comunidad MetodologIA
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
```

#### Paso 3: Estructura Gold-Standard
Agregar o mejorar estas secciones en orden:

1. **Grounding Guideline** (3 líneas, contextual al dominio)
2. **Inputs** section con `$ARGUMENTS` parsing + `{MODO}` + `{FORMATO}` + `{VARIANTE}`
3. **When NOT to Use** (3-5 bullets)
4. **Assumptions & Limits** (edge cases + workarounds)
5. **Delivery Structure** (secciones numeradas S1-SN)
6. **Conditional Logic** (al menos 1 IF/THEN contextual)
7. **Cross-References** a skills relacionadas

#### Paso 4: Verificación
- grep -c '#6366F1\|#0F172A\|Montserrat' → debe ser 0
- Frontmatter tiene model + context + argument-hint
- "Grounding Guideline" o equivalent presente
- Al menos 1 conditional logic block

---

### Skills Batch por Dominio (para ejecución ordenada)

| Dominio | Skills Batch | Cantidad |
|---------|-------------|----------|
| Arquitectura | database-architecture, devsecops-architecture, documentation-architecture, event-architecture, infrastructure-architecture, integration-architecture, security-architecture | 7 |
| Data & Analytics | data-mesh-strategy, data-quality, data-science-architecture, data-storytelling, data-viz-storytelling | 5 |
| Análisis & Discovery | dependency-analysis, maturity-assessment | 2 |
| Cloud & Platform | capacity-planning, disaster-recovery, finops, sustainability-assessment | 4 |
| Calidad & Ops | compliance-assessment, incident-management, onboarding-playbook, performance-engineering, pipeline-governance, quality-engineering, release-strategy, sla-design, vendor-assessment | 9 |
| Gestión & Estrategia | competitive-intelligence, execution-burndown, governance-framework, product-strategy, project-program-management, risk-controlling-dynamics, sector-intelligence | 7 |
| Editorial & Comunicación | copywriting, functional-toolbelt, technical-writing, ux-writing | 4 |
| Cambio & Adopción | mentoring-training-discovery, workshop-facilitator | 2 |
| Innovación | hypothesis-driven-development, migration-playbook, poc-lab, roadmap-poc, technology-vigilance | 5 |
| Herramientas & DX | cli-init, context-optimization, developer-experience, mini-apps-discovery, rendering-engine, team-topology | 6 |
| Service Discovery | cloud-service-discovery, digital-transformation-discovery, management-discovery, mobile-assessment, mobile-platform-assessment, qa-service-discovery, staff-augmentation-discovery, user-representative, ux-design-discovery | 9 |
| **Total** | | **~60** |

*Nota: ~7 skills batch tienen estructura mixta (batch base + algunas secciones gold). Evaluar individualmente.*

---

*Entregable 05 de 07 — Auditoría MAO v1.4*
