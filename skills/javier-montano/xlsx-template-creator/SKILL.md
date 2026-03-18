---
name: xlsx-template-creator
description: >
  Generates XLSX template specifications with columns, formulas, conditional formatting, and dashboard layouts for tracking and metrics.
  Use when the user asks to "create a spreadsheet template", "build a tracking matrix", "design a metrics dashboard",
  "generate an XLSX spec", or mentions xlsx template, spreadsheet layout, or KPI dashboard.
argument-hint: <tracking-matrix|metrics-dashboard> <title>
allowed-tools: Read, Write, Edit, Glob
---

# XLSX Template Creator

Generate XLSX template specifications — YAML definitions that describe spreadsheet structure, formulas, validation rules, and conditional formatting for a rendering skill to produce .xlsx files.

## Assumptions & Limits

- **Assumes**: A rendering skill/tool converts the YAML spec to actual .xlsx (this skill defines structure)
- **Limit**: Complex chart types (waterfall, Gantt) require post-render configuration
- **Limit**: Sparklines depend on renderer support — degrade to text trends if unavailable
- **Trade-off**: YAML spec = version-controllable, auditable; direct .xlsx = exact formatting but binary

### When to use each type

| Signal | Tracking Matrix | Metrics Dashboard |
|---|---|---|
| Individual task/item tracking | Yes | No |
| KPI monitoring over time | No | Yes |
| Compliance checklist | Yes | No |
| Executive summary | No | Yes |
| Both | Create one of each, cross-reference |

## Usage

```
/xlsx-template-creator tracking-matrix "Workflow Execution Tracker"
/xlsx-template-creator metrics-dashboard "Agent Performance Dashboard"
```

Parse `$1` as type, `$2` as title. If missing, interview.

## Before Generating

1. **Read column spec**: `Read references/xlsx-columns-spec.md` if available
2. **Read source KPIs**: If linked to a skill/workflow, read its metrics
3. **Check existing**: `Glob **/templates/*.xlsx.md` for consistency

## Tracking Matrix Spec

3 sheets: **Tracker** (data), **Summary** (aggregation), **Config** (dropdowns)

```yaml
templateType: tracking-matrix
title: "{{title}}"

sheets:
  - name: Tracker
    frozenRows: 1
    frozenCols: 2
    autoFilter: true
    columns:
      - header: "ID"
        width: 8
        type: auto-increment
        description: "Unique row identifier"
      - header: "Item"
        width: 40
        type: text
        description: "Task or item being tracked"
      - header: "Owner"
        width: 20
        type: dropdown
        source: "Config!A2:A50"
        description: "Responsible person/agent"
      - header: "Status"
        width: 15
        type: dropdown
        source: "Config!B2:B10"
        conditionalFormat:
          "Completado": { bg: "#c6efce", font: "#006100" }
          "En Progreso": { bg: "#ffeb9c", font: "#9c5700" }
          "Bloqueado": { bg: "#ffc7ce", font: "#9c0006" }
          "Pendiente": { bg: "#f2f2f2", font: "#666666" }
      - header: "Priority"
        width: 12
        type: dropdown
        source: "Config!C2:C5"
        conditionalFormat:
          "Critica": { bg: "#ffc7ce", font: "#9c0006" }
          "Alta": { bg: "#ffeb9c", font: "#9c5700" }
      - header: "Start Date"
        width: 12
        type: date
        format: "YYYY-MM-DD"
      - header: "Due Date"
        width: 12
        type: date
        format: "YYYY-MM-DD"
        conditionalFormat:
          overdue: { bg: "#ffc7ce" }  # Due date < today AND status != Completado
      - header: "% Complete"
        width: 10
        type: percentage
        conditionalFormat:
          dataBar: { color: "#4472c4", min: 0, max: 1 }
      - header: "Notes"
        width: 50
        type: text
        wrapText: true

  - name: Summary
    purpose: "Auto-calculated dashboard from Tracker data"
    layout:
      - cell: "A1"
        value: "Dashboard"
        style: { font: "16pt bold" }
      - cell: "A3"
        label: "Total Items"
        formula: "=COUNTA(Tracker!A:A)-1"
      - cell: "A4"
        label: "Completed"
        formula: "=COUNTIF(Tracker!D:D,\"Completado\")"
      - cell: "A5"
        label: "In Progress"
        formula: "=COUNTIF(Tracker!D:D,\"En Progreso\")"
      - cell: "A6"
        label: "Blocked"
        formula: "=COUNTIF(Tracker!D:D,\"Bloqueado\")"
      - cell: "A8"
        label: "Completion Rate"
        formula: "=IF(B3>0,B4/B3,0)"
        format: "0.0%"
      - cell: "A9"
        label: "Overdue Items"
        formula: "=COUNTIFS(Tracker!G:G,\"<\"&TODAY(),Tracker!D:D,\"<>Completado\")"

  - name: Config
    purpose: "Dropdown values — edit here to update all dropdowns"
    columns:
      - header: "Owners (A)"
        values: ["{{owner1}}", "{{owner2}}", "{{owner3}}"]
      - header: "Status (B)"
        values: ["Pendiente", "En Progreso", "En Revision", "Completado", "Bloqueado", "Cancelado"]
      - header: "Priority (C)"
        values: ["Critica", "Alta", "Media", "Baja"]
```

## Metrics Dashboard Spec

4 sheets: **KPIs** (current vs target), **Trends** (historical), **Alerts** (out-of-range), **Config** (thresholds)

```yaml
templateType: metrics-dashboard
title: "{{title}}"

sheets:
  - name: KPIs
    frozenRows: 1
    columns:
      - header: "KPI"
        width: 30
      - header: "Current"
        width: 12
        type: number
      - header: "Target"
        width: 12
        type: number
        source: "Config!B:B"
      - header: "% of Target"
        width: 12
        formula: "=IF(C{row}>0,B{row}/C{row},0)"
        format: "0.0%"
        conditionalFormat:
          ">= 1.0": { bg: "#c6efce", font: "#006100" }
          ">= 0.7": { bg: "#ffeb9c", font: "#9c5700" }
          "< 0.7": { bg: "#ffc7ce", font: "#9c0006" }
      - header: "Trend (12mo)"
        width: 15
        sparkline: "Trends!B{row}:M{row}"
      - header: "Status"
        width: 10
        formula: "=IF(D{row}>=1,\"OK\",IF(D{row}>=0.7,\"WARNING\",\"CRITICAL\"))"

  - name: Trends
    purpose: "12-month historical data for sparklines"
    columns:
      - header: "KPI"
        width: 30
      - headers: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        width: 8
        type: number

  - name: Alerts
    purpose: "Auto-filtered: KPIs outside acceptable range"
    autoFilter: true
    conditionalFormat:
      row:
        "Critical": { bg: "#ffc7ce" }
        "Warning": { bg: "#ffeb9c" }
    columns:
      - header: "KPI"
        width: 30
      - header: "Severity"
        width: 12
        formula: "=IF(KPIs!D{row}<Config!D{row},\"Critical\",IF(KPIs!D{row}<Config!C{row},\"Warning\",\"OK\"))"
      - header: "Current"
        width: 12
      - header: "Threshold"
        width: 12
      - header: "Gap"
        width: 12
        formula: "=C{row}-D{row}"
      - header: "Action Required"
        width: 50
        type: text

  - name: Config
    purpose: "Thresholds and targets — edit here"
    columns:
      - header: "KPI"
      - header: "Target"
        type: number
      - header: "Warning Threshold"
        type: number
        description: "% of target that triggers warning (e.g., 0.7)"
      - header: "Critical Threshold"
        type: number
        description: "% of target that triggers critical (e.g., 0.5)"
      - header: "Unit"
        type: text
```

## Formatting Standards

| Element | Standard | Rationale |
|---|---|---|
| Header row | Bold, frozen, #f2f2f2 background | Always visible while scrolling |
| Data validation | Dropdowns reference Config sheet | Single source of truth for allowed values |
| Conditional formatting | Semantic: green=good, yellow=warning, red=critical | Universal understanding |
| Data bars | For percentage columns | Visual progress indicator |
| Named ranges | All Config columns | Clean formula references |
| Print area | Set per sheet | Predictable print output |
| No merged cells | Data areas only (header merges OK) | Prevents sort/filter issues |
| Column widths | Explicit per column | No auto-width surprises |

## Edge Cases

- **More than 10 dropdown values**: Config sheet handles unlimited rows — formula ranges should use full column (e.g., `Config!A:A`)
- **Cross-sheet references break on rename**: Use named ranges instead of sheet!cell references
- **Percentage column with 0 denominator**: All formulas use `IF(denominator>0, calc, 0)` guard
- **Dashboard with >20 KPIs**: Split into category sub-tables with subtotals

## Validation Gate

- [ ] All required sheets present for chosen type
- [ ] Every column has header, width, and type
- [ ] Dropdown columns reference Config sheet
- [ ] Conditional formatting uses semantic colors (green/yellow/red)
- [ ] Formulas guard against division by zero
- [ ] Summary/dashboard formulas reference correct sheet ranges
- [ ] No merged cells in data areas
- [ ] Named ranges defined for cross-sheet references
- [ ] Print area set per sheet
- [ ] Config sheet is clearly labeled as "edit here"

---
**Author:** Javier Montano | **Last updated:** 2026-03-12
