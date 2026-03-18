# Version History Template and Archive Format

This document describes how to capture, format, and display iteration history for archival or user delivery.

---

## Archive Format

Version history is stored in JSON alongside the content file.

**Filename:** `{content-name}.history.json`

**Location:** Same directory as the content file

**Structure:**

```json
{
  "content_name": "my-document.md",
  "created_at": "2026-03-01T14:30:00Z",
  "iterations": [
    {
      "iteration": 1,
      "timestamp": "2026-03-01T14:30:00Z",
      "version_label": "initial-draft",
      "scores": {
        "fundamento": 7,
        "veracidad": 6,
        "calidad": 8,
        "densidad": 5,
        "simplicidad": 7,
        "claridad": 6,
        "precision": 7,
        "profundidad": 8,
        "coherencia": 7,
        "valor": 6
      },
      "average_score": 6.7,
      "weaknesses": ["Densidad", "Claridad", "Valor"],
      "changes_made": "N/A (initial draft)",
      "notes": "Initial evaluation baseline"
    },
    {
      "iteration": 2,
      "timestamp": "2026-03-01T14:45:00Z",
      "version_label": "densidad-pass",
      "scores": {
        "fundamento": 8,
        "veracidad": 7,
        "calidad": 9,
        "densidad": 8,
        "simplicidad": 8,
        "claridad": 8,
        "precision": 8,
        "profundidad": 9,
        "coherencia": 8,
        "valor": 7
      },
      "average_score": 8.0,
      "delta_from_previous": 1.3,
      "weaknesses": ["Veracidad", "Valor"],
      "changes_made": [
        "Merged 5 duplicate sentences in §2",
        "Converted prose list to table in §4",
        "Replaced 'somewhat' with specific metrics",
        "Removed 12 filler phrases"
      ],
      "notes": "Strong improvement. Two criteria remain below 8."
    },
    {
      "iteration": 3,
      "timestamp": "2026-03-01T15:00:00Z",
      "version_label": "final",
      "scores": {
        "fundamento": 10,
        "veracidad": 10,
        "calidad": 10,
        "densidad": 10,
        "simplicidad": 10,
        "claridad": 10,
        "precision": 10,
        "profundidad": 10,
        "coherencia": 10,
        "valor": 10
      },
      "average_score": 10.0,
      "delta_from_previous": 2.0,
      "weaknesses": [],
      "changes_made": [
        "Added domain expertise section explaining why this approach works",
        "Explicitly handled 5 edge cases in implementation section",
        "Added success criteria and measurement framework",
        "Cross-linked all sections for coherence"
      ],
      "status": "DELIVERED",
      "notes": "Achieved 10/10. Ready for publication."
    }
  ],
  "delivery_info": {
    "final_iteration": 3,
    "final_score": 10.0,
    "total_refinements": 2,
    "time_spent_seconds": 900,
    "tokens_used_estimate": 15000,
    "delivered_at": "2026-03-01T15:05:00Z"
  }
}
```

---

## Markdown Display Format

When delivering version history to the user, format as Markdown:

```markdown
## Version History — [Document Title]

### Overview
- **Final Score:** 10.0/10
- **Iterations:** 3
- **Total Time:** 15 minutes
- **Status:** Delivered

---

### Iteration 1: Initial Draft
**Date:** 2026-03-01 14:30 UTC

**Scores:**
- Fundamento: 7
- Veracidad: 6
- Calidad: 8
- Densidad: 5 ⚠️
- Simplicidad: 7
- Claridad: 6 ⚠️
- Precisión: 7
- Profundidad: 8
- Coherencia: 7
- Valor: 6 ⚠️

**Average:** 6.7/10

**Weaknesses:** Densidad (5), Claridad (6), Valor (6)

**Notes:** Initial evaluation shows strong structure but weak density and clarity. Value proposition needs domain expertise injection.

---

### Iteration 2: Densidad & Claridad Pass
**Date:** 2026-03-01 14:45 UTC

**Changes Made:**
- Merged 5 duplicate sentences in section 2
- Converted prose list to comparison table
- Replaced vague qualifiers with specific thresholds
- Removed 12 filler phrases
- Clarified 3 ambiguous conditions

**Scores:**
- Fundamento: 8 ✓
- Veracidad: 7
- Calidad: 9 ✓
- Densidad: 8 ✓ (improved +3)
- Simplicidad: 8 ✓
- Claridad: 8 ✓ (improved +2)
- Precisión: 8 ✓
- Profundidad: 9 ✓
- Coherencia: 8 ✓
- Valor: 7

**Average:** 8.0/10 (+1.3 from iteration 1)

**Weaknesses:** Veracidad (7), Valor (7)

**Notes:** Significant improvement in clarity and density. All major criteria now ≥8. Next pass will focus on domain expertise and edge case coverage.

---

### Iteration 3: Valor & Profundidad Pass (FINAL)
**Date:** 2026-03-01 15:00 UTC

**Changes Made:**
- Added domain expertise framework explaining methodology
- Documented 5 common failure modes and recovery strategies
- Defined explicit success criteria and measurement approach
- Cross-linked all sections to improve coherence
- Added specific examples from similar projects

**Scores:**
- Fundamento: 10 ✓
- Veracidad: 10 ✓ (improved +3)
- Calidad: 10 ✓
- Densidad: 10 ✓
- Simplicidad: 10 ✓
- Claridad: 10 ✓
- Precisión: 10 ✓
- Profundidad: 10 ✓
- Coherencia: 10 ✓
- Valor: 10 ✓ (improved +3)

**Average:** 10.0/10 (+2.0 from iteration 2)

**Status:** ✓ DELIVERED

**Notes:** All criteria at 10/10. Ready for publication.

---

## Summary

| Iteration | Average Score | Delta | Status |
|-----------|---|---|---|
| 1 | 6.7/10 | — | Initial |
| 2 | 8.0/10 | +1.3 | In Progress |
| 3 | 10.0/10 | +2.0 | ✓ Delivered |
```

---

## How to Generate the Archive

### Step 1: Store Initial Scores
After first evaluation (before any refinement):
```bash
python tools/version-archiver.py \
  --input my-document.md \
  --iteration 1 \
  --scores "7,6,8,5,7,6,7,8,7,6" \
  --changes "Initial draft"
```

### Step 2: After Each Refinement, Record New Scores
```bash
python tools/version-archiver.py \
  --input my-document.md \
  --iteration 2 \
  --scores "8,7,9,8,8,8,8,9,8,7" \
  --changes "Merged duplicate sentences, converted prose to table, replaced vague qualifiers"
```

### Step 3: View Complete History
```bash
python tools/version-archiver.py --show-history my-document.md
```

Output:
```
Version History: my-document.md

Iteration 1 (2026-03-01 14:30):
  Average: 6.7/10
  Scores: F:7 V:6 C:8 D:5 S:7 Cl:6 P:7 Pr:8 Co:7 Va:6

Iteration 2 (2026-03-01 14:45):
  Average: 8.0/10
  Delta: +1.3
  Scores: F:8 V:7 C:9 D:8 S:8 Cl:8 P:8 Pr:9 Co:8 Va:7
  Changes: Merged duplicates, converted table, replaced vague qualifiers

Iteration 3 (2026-03-01 15:00):
  Average: 10.0/10
  Delta: +2.0
  Scores: F:10 V:10 C:10 D:10 S:10 Cl:10 P:10 Pr:10 Co:10 Va:10
  Status: DELIVERED
```

---

## When to Include Version History

### Always Include
- User explicitly requested: "Show me the iterations" or "What was the process?"
- High-stakes deliverables: strategy documents, major proposals, published articles
- Learning purposes: teaching, documentation, case studies
- Audit trail required: compliance, regulated industries

### Optionally Include
- Multi-day projects: helps show methodology to stakeholders
- Complex refinements: demonstrates rigor in difficult domains
- Quality transparency: builds trust in the final output

### Never Include (Omit Version History)
- Simple responses to straightforward questions
- User said "just give me the answer"
- Casual communication (chat, quick advice)
- Internal drafts not for external consumption

---

## Version History Metadata

**Required Fields:**

```json
{
  "content_name": "string",
  "created_at": "ISO 8601 timestamp",
  "iterations": [
    {
      "iteration": "integer (1, 2, 3, ...)",
      "timestamp": "ISO 8601",
      "scores": {
        "fundamento": "0-10",
        "veracidad": "0-10",
        "calidad": "0-10",
        "densidad": "0-10",
        "simplicidad": "0-10",
        "claridad": "0-10",
        "precision": "0-10",
        "profundidad": "0-10",
        "coherencia": "0-10",
        "valor": "0-10"
      },
      "average_score": "float 0-10",
      "changes_made": "string or array of strings"
    }
  ]
}
```

**Optional Fields:**

```json
{
  "delta_from_previous": "float",
  "weaknesses": "array of criterion names",
  "notes": "string with any additional context",
  "status": "INITIAL | IN_PROGRESS | DELIVERED",
  "version_label": "semantic label (e.g., 'densidad-pass')"
}
```

---

## Example: Short Project (2 iterations)

```markdown
## Version History — API Documentation

### Iteration 1: Initial
- Average: 7.2/10
- Weaknesses: Profundidad (4), Valor (5)

### Iteration 2: Final (DELIVERED)
- Average: 9.1/10
- Changes: Added 5 edge cases, included methodology section
```

---

## Example: Long Project (4 iterations, truncated)

```markdown
## Version History — Architecture Design Document

### Iteration 1: Initial
- Average: 6.8/10

### Iteration 2: Claridad Pass
- Average: 7.9/10 (+1.1)

### Iteration 3: Profundidad Pass
- Average: 8.7/10 (+0.8)

### Iteration 4: Final (DELIVERED)
- Average: 9.4/10 (+0.7)
- Note: Diminishing returns after iteration 3; continued for comprehensive edge case coverage
```

---

## Delivery Notes

**What to include in version history:**
- Timestamps (shows work over time)
- Score progression (demonstrates improvement path)
- Changes made (shows specific actions taken)
- Criterion names, not abbreviations (clarity for non-technical users)

**What NOT to include:**
- Internal tool output (JSON, detailed logs)
- Token counts (not meaningful to users)
- Time elapsed per iteration (too granular)
- Alternative solutions considered but rejected (clutter)
