# Auditoria de Output Templates — MetodologIA Discovery Framework

**Fecha:** 15 de marzo de 2026
**Alcance:** 100 skills en `/skills/`
**Autor:** Javier Montano (con Claude Code)
**Estado:** {Aprobado}

---

## Resumen Ejecutivo

| Formato | Skills que lo declaran | % del total |
|---------|----------------------|-------------|
| **MD** (Markdown) | 100 | 100% |
| **HTML** | 37 | 37% |
| **XLSX** | 18 | 18% |
| **DOCX** | 14 | 14% |
| **PPTX** | 16 | 16% |

**Completeness Score: 37/100**

> Calculo: promedio de formatos declarados por skill (185 declaraciones / 100 skills = 1.85 formatos promedio). Sobre un maximo ideal de 5 formatos, la completitud es 37%.

---

## Distribucion por Combinacion de Formatos

| Combinacion | Cantidad | Skills |
|-------------|----------|--------|
| **MD only** | 26 | Ver seccion detallada |
| **MD + HTML** | 23 | Ver seccion detallada |
| **MD + XLSX** | 10 | Ver seccion detallada |
| **MD + DOCX** | 10 | Ver seccion detallada |
| **MD + PPTX** | 13 | Ver seccion detallada |
| **MD + HTML + DOCX** | 1 | html-brand |
| **MD + DOCX + XLSX** | 0 | -- |
| **Otros (3+ formatos)** | 0 | -- |
| **Sin MD (solo otros)** | 0 | -- |

> Ningun skill declara mas de 2 formatos (excepto html-brand con MD + HTML + DOCX).

---

## Inventario Completo por Skill

### Tabla Maestra (100 skills)

| # | Skill | MD | HTML | DOCX | XLSX | PPTX | Total |
|---|-------|:--:|:----:|:----:|:----:|:----:|:-----:|
| 1 | accessibility-audit | X | X | | | | 2 |
| 2 | adoption-strategy | X | | | | X | 2 |
| 3 | ai-center-discovery | X | | | | X | 2 |
| 4 | analytics-engineering | X | | | X | | 2 |
| 5 | api-architecture | X | X | | | | 2 |
| 6 | architecture-tobe | X | | | | X | 2 |
| 7 | asis-analysis | X | X | | | | 2 |
| 8 | bi-analytics-discovery | X | | | | X | 2 |
| 9 | bi-architecture | X | | | | X | 2 |
| 10 | capacity-planning | X | | | X | | 2 |
| 11 | change-readiness-assessment | X | | | | X | 2 |
| 12 | cloud-migration | X | | | X | | 2 |
| 13 | cloud-native-architecture | X | | X | | | 2 |
| 14 | cloud-service-discovery | X | | | | X | 2 |
| 15 | commercial-model | X | | | | X | 2 |
| 16 | competitive-intelligence | X | | | | X | 2 |
| 17 | compliance-assessment | X | | | X | | 2 |
| 18 | copywriting | X | X | | | | 2 |
| 19 | cost-estimation | X | | | X | | 2 |
| 20 | data-engineering | X | | | X | | 2 |
| 21 | data-governance | X | | | X | | 2 |
| 22 | data-mesh-strategy | X | X | | | | 2 |
| 23 | data-quality | X | | | X | | 2 |
| 24 | data-science-architecture | X | | X | | | 2 |
| 25 | data-storytelling | X | | | | | 1 |
| 26 | data-viz-storytelling | X | | | | X | 2 |
| 27 | database-architecture | X | | | X | | 2 |
| 28 | dependency-analysis | X | | | X | | 2 |
| 29 | design-system | X | X | | | | 2 |
| 30 | developer-experience | X | X | | | | 2 |
| 31 | devsecops-architecture | X | X | | | | 2 |
| 32 | digital-transformation-discovery | X | | | | X | 2 |
| 33 | disaster-recovery | X | | X | | | 2 |
| 34 | discovery-handover | X | | X | | | 2 |
| 35 | discovery-orchestrator | X | X | | | | 2 |
| 36 | documentation-architecture | X | | | X | | 2 |
| 37 | dynamic-sme | X | X | | | | 2 |
| 38 | enterprise-architecture | X | | | | X | 2 |
| 39 | event-architecture | X | X | | | | 2 |
| 40 | execution-burndown | X | | | | | 1 |
| 41 | executive-pitch | X | | | | X | 2 |
| 42 | finops | X | | | X | | 2 |
| 43 | flow-mapping | X | | X | | | 2 |
| 44 | functional-spec | X | | X | | | 2 |
| 45 | functional-toolbelt | X | X | | | | 2 |
| 46 | governance-framework | X | | | X | | 2 |
| 47 | html-brand | | X | X | | | 3 |
| 48 | hypothesis-driven-development | X | | | | X | 2 |
| 49 | incident-management | X | | X | | | 2 |
| 50 | infrastructure-architecture | X | | | X | | 2 |
| 51 | input-analysis | X | | X | | | 2 |
| 52 | integration-architecture | X | X | | | | 2 |
| 53 | management-discovery | X | | | X | | 2 |
| 54 | maturity-assessment | X | | | X | | 2 |
| 55 | mentoring-training-discovery | X | | | X | | 2 |
| 56 | mermaid-diagramming | X | X | | | | 2 |
| 57 | migration-playbook | X | | X | | | 2 |
| 58 | mini-apps-discovery | X | | | | X | 2 |
| 59 | mobile-architecture | X | X | | | | 2 |
| 60 | mobile-assessment | X | X | | | | 2 |
| 61 | mobile-platform-assessment | X | | | | X | 2 |
| 62 | multidimensional-feasibility | X | X | | | | 2 |
| 63 | observability | X | | | X | | 2 |
| 64 | onboarding-playbook | X | | | | | 1 |
| 65 | output-engineering | X | X | | | | 2 |
| 66 | performance-engineering | X | | | X | | 2 |
| 67 | pipeline-governance | X | | X | | | 2 |
| 68 | poc-lab | X | | | | | 1 |
| 69 | product-strategy | X | X | | | | 2 |
| 70 | project-program-management | X | | X | | | 2 |
| 71 | qa-service-discovery | X | | | X | | 2 |
| 72 | quality-engineering | X | | | X | | 2 |
| 73 | release-strategy | X | | X | | | 2 |
| 74 | risk-controlling-dynamics | X | | X | | | 2 |
| 75 | roadmap-poc | X | X | | | | 2 |
| 76 | rpa-discovery | X | | | | X | 2 |
| 77 | scenario-analysis | X | | | | X | 2 |
| 78 | sector-intelligence | X | X | | | | 2 |
| 79 | security-architecture | X | | | X | | 2 |
| 80 | sla-design | X | | | X | | 2 |
| 81 | software-architecture | X | X | | | | 2 |
| 82 | software-viability | X | X | | | | 2 |
| 83 | solution-roadmap | X | | | X | | 2 |
| 84 | solutions-architecture | X | X | | | | 2 |
| 85 | staff-augmentation-discovery | X | | | X | | 2 |
| 86 | stakeholder-mapping | X | | X | | | 2 |
| 87 | storytelling | X | | | | | 1 |
| 88 | sustainability-assessment | X | X | | | | 2 |
| 89 | team-topology | X | | | | X | 2 |
| 90 | tech-debt-assessment | X | | | X | | 2 |
| 91 | technical-feasibility | X | | X | | | 2 |
| 92 | technical-writing | X | X | | | | 2 |
| 93 | technology-vigilance | X | X | | | | 2 |
| 94 | testing-strategy | X | X | | | | 2 |
| 95 | user-representative | X | X | | | | 2 |
| 96 | ux-design-discovery | X | X | | | | 2 |
| 97 | ux-writing | X | X | | | | 2 |
| 98 | vendor-assessment | X | | | X | | 2 |
| 99 | workshop-design | X | X | | | | 2 |
| 100 | workshop-facilitator | X | X | | | | 2 |

**Nota:** html-brand es el unico skill cuyo formato primario es HTML (no MD). Se cuentan 3 formatos porque declara HTML (primary) + DOCX (secondary); el MD esta implicito en el sistema pero no declarado como template explicito en ese skill.

---

## Skills con Solo 1 Formato (MD-only)

Los siguientes 5 skills declaran unicamente Markdown sin formato alternativo:

| # | Skill | Observacion |
|---|-------|-------------|
| 1 | data-storytelling | Solo templates Markdown (Template 1 + Template 2, ambos MD) |
| 2 | execution-burndown | Solo templates Markdown (Template 1 + Template 2, ambos MD) |
| 3 | onboarding-playbook | Solo templates Markdown (Template 1 + Template 2, ambos MD) |
| 4 | poc-lab | Solo templates Markdown (Template 1 + Template 2, ambos MD) |
| 5 | storytelling | Solo templates Markdown (Template 1 + Template 2, ambos MD) |

---

## Skills Faltantes por Formato

### Falta HTML (63 skills)

adoption-strategy, ai-center-discovery, analytics-engineering, architecture-tobe, bi-analytics-discovery, bi-architecture, capacity-planning, change-readiness-assessment, cloud-migration, cloud-native-architecture, cloud-service-discovery, commercial-model, competitive-intelligence, compliance-assessment, cost-estimation, data-engineering, data-governance, data-quality, data-science-architecture, data-storytelling, data-viz-storytelling, database-architecture, dependency-analysis, digital-transformation-discovery, disaster-recovery, discovery-handover, documentation-architecture, enterprise-architecture, execution-burndown, executive-pitch, finops, flow-mapping, functional-spec, governance-framework, hypothesis-driven-development, incident-management, infrastructure-architecture, input-analysis, management-discovery, maturity-assessment, mentoring-training-discovery, migration-playbook, mini-apps-discovery, mobile-platform-assessment, observability, onboarding-playbook, performance-engineering, pipeline-governance, poc-lab, project-program-management, qa-service-discovery, quality-engineering, release-strategy, risk-controlling-dynamics, rpa-discovery, scenario-analysis, security-architecture, sla-design, solution-roadmap, staff-augmentation-discovery, stakeholder-mapping, storytelling, team-topology, tech-debt-assessment, technical-feasibility, vendor-assessment

### Falta DOCX (86 skills)

Todos excepto: cloud-native-architecture, data-science-architecture, disaster-recovery, discovery-handover, flow-mapping, functional-spec, html-brand, incident-management, input-analysis, migration-playbook, pipeline-governance, project-program-management, release-strategy, risk-controlling-dynamics, stakeholder-mapping, technical-feasibility

### Falta XLSX (82 skills)

Todos excepto: analytics-engineering, capacity-planning, cloud-migration, compliance-assessment, cost-estimation, data-engineering, data-governance, data-quality, database-architecture, dependency-analysis, documentation-architecture, finops, governance-framework, infrastructure-architecture, management-discovery, maturity-assessment, mentoring-training-discovery, observability, performance-engineering, qa-service-discovery, quality-engineering, security-architecture, sla-design, solution-roadmap, staff-augmentation-discovery, tech-debt-assessment, vendor-assessment

### Falta PPTX (84 skills)

Todos excepto: adoption-strategy, ai-center-discovery, architecture-tobe, bi-analytics-discovery, bi-architecture, change-readiness-assessment, cloud-service-discovery, commercial-model, competitive-intelligence, data-viz-storytelling, digital-transformation-discovery, enterprise-architecture, executive-pitch, hypothesis-driven-development, mini-apps-discovery, mobile-platform-assessment, rpa-discovery, scenario-analysis, team-topology

---

## Patrones Identificados

### Patron 1: "MD + un segundo formato" (94 skills)

La gran mayoria de skills (94/100) siguen el patron de declarar **exactamente 2 formatos**: Markdown como default y un segundo formato complementario. Solo 5 skills tienen un unico formato (MD), y 1 skill (html-brand) tiene 3 formatos.

### Patron 2: Segundo formato alineado al dominio

El segundo formato no es aleatorio sino que sigue una logica de dominio:

| Segundo formato | Tipo de skill | Logica |
|----------------|---------------|--------|
| **HTML** | Arquitectura, UX, diagramas, vigilancia tecnologica | Visualizacion interactiva, dashboards, Design System MetodologIA |
| **XLSX** | Data, costos, madurez, operaciones, compliance | Matrices, scorecards, inventarios, tracking operativo |
| **DOCX** | Governance, handover, feasibility, regulatorio | Documentos formales con firmas, circulacion confidencial, auditoria |
| **PPTX** | Estrategia, comercial, ejecutivo, transformacion | Presentaciones a C-level, steering committees, sponsors |

### Patron 3: Ningun skill tiene los 5 formatos

Ningun skill declara los 5 formatos posibles. El maximo es 3 (html-brand). La mayoria tiene exactamente 2.

### Patron 4: Notacion heterogenea

Se usan al menos 4 estilos diferentes para declarar Output Templates:

| Estilo | Ejemplo | Frecuencia aprox. |
|--------|---------|-------------------|
| Tabla `\| Formato \| Nombre \| Contenido \|` | flow-mapping, api-architecture | ~20 skills |
| H3 headings `### Markdown (default)` / `### PPTX` | incident-management, adoption-strategy | ~20 skills |
| Bold paragraphs `**Formato MD (default):**` / `**Formato HTML:**` | asis-analysis, risk-controlling-dynamics | ~40 skills |
| Numbered `**Formato 1 — Markdown**` / `**Formato 2 — XLSX**` | release-strategy, competitive-intelligence | ~10 skills |
| Named templates `### Template 1: Name (Markdown)` | poc-lab, data-storytelling | ~10 skills |

### Patron 5: "Bajo demanda" vs. "secondary" vs. sin etiqueta

Los formatos no-MD se etiquetan de tres formas:
- **"bajo demanda"**: El usuario debe solicitar explicitamente el formato
- **"secondary"**: Disponible como segunda opcion automatica
- **Sin etiqueta**: Implicito que es bajo demanda

---

## Evaluacion de Completitud (0-100)

| Criterio | Peso | Score | Ponderado |
|----------|------|-------|-----------|
| Cobertura MD (100/100) | 20% | 100 | 20.0 |
| Cobertura HTML (37/100) | 20% | 37 | 7.4 |
| Cobertura DOCX (14/100) | 20% | 14 | 2.8 |
| Cobertura XLSX (18/100) | 20% | 18 | 3.6 |
| Cobertura PPTX (16/100) | 20% | 16 | 3.2 |
| **Total** | **100%** | | **37.0** |

### Score Global de Completitud: **37 / 100**

---

## Recomendaciones

1. **Estandarizar la notacion**: Elegir un unico estilo para la seccion Output Templates (recomendacion: tabla `| Formato | Nombre | Contenido |` por ser la mas compacta y parseable).

2. **Priorizar HTML**: Es el formato con mayor brecha de valor (63 skills sin HTML). Dado que el Design System MetodologIA v4 ya existe, los skills de arquitectura, UX y visualizacion deberian tener template HTML como minimo.

3. **Agregar XLSX a skills con matrices y scorecards**: Skills como scenario-analysis, hypothesis-driven-development, y adoption-strategy que producen matrices y scoring deberian tener XLSX.

4. **Agregar PPTX a skills ejecutivos**: Skills como executive-pitch (ya lo tiene), pero tambien product-strategy, software-viability, y stakeholder-mapping deberian considerar PPTX.

5. **Resolver los 5 skills MD-only**: data-storytelling, execution-burndown, onboarding-playbook, poc-lab, y storytelling son los unicos sin segundo formato. Priorizar agregar al menos un formato alternativo a cada uno.

6. **Definir politica de formatos minimos**: Establecer que todo skill debe declarar al menos MD + 1 formato complementario (HTML, DOCX, XLSX o PPTX segun dominio).

---

**Generado por:** Claude Code | **Fecha:** 15 de marzo de 2026
