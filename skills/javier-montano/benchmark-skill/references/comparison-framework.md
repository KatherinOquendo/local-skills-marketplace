# Comparison Framework

Reference for benchmark-skill. Protocols for consistent scoring, delta classification, and trade-off analysis.

## Scoring Consistency Protocol

The biggest risk in benchmarking is inconsistent scoring — giving different scores to the same content quality because of context effects (the second state looks better because you just saw the first). These protocols prevent drift.

### Anchoring Rule

Score State A first, completely. Write down every score with evidence. Then score State B. When scoring State B, for any unchanged section, use State A's score exactly — don't re-evaluate unchanged content.

### Evidence Anchoring

Each score needs a specific finding:

| Weak Evidence | Strong Evidence |
|--------------|----------------|
| "Clarity seems good" | "Clarity: 8 — all terms defined in Glossary (15 terms), 0 ambiguous pronouns (grep verified), 1 vague qualifier ('appropriate') in line 142" |
| "Depth improved" | "Depth: 5→8 — edge cases went from 2 (intentional informal, multi-question) to 6 (added: contradictory signals, repeated requests, non-text input, sarcasm)" |

### Handling Subjective Dimensions

Dimensions 4 (density), 5 (simplicity), and 10 (value) are inherently subjective. To minimize drift:

| Dimension | Objective Proxy |
|-----------|----------------|
| Density | Count sentences that could be deleted without information loss. Fewer = higher density. |
| Simplicity | Count concepts explained multiple ways. Fewer = simpler. Word count per concept. |
| Value | Count sections where deletion wouldn't change skill output. Fewer zero-value sections = higher value. |

## Delta Classification Rules

### IMPROVED

All of these must be true:
- Average score increased by >= 0.5
- Zero gate regressions (no checkpoint that passed now fails)
- Zero rubric regressions of 2+ points on any dimension
- At least 2 dimensions improved by 1+ points

A 1-point improvement on 7 dimensions with a 1-point regression on 1 dimension is IMPROVED — the regression is noted but doesn't block the classification.

### LATERAL

- Average changed by < 0.5 (either direction)
- Trade-offs approximately balance: gains in some dimensions offset by losses in others
- No net gate change

**LATERAL is not a failure.** A skill that trades density for depth (more edge cases, slightly less compressed) made a valid trade-off. The benchmark reports the trade-off transparently.

### REGRESSED

Any of these is true:
- Average decreased by >= 0.5
- 1+ gate checkpoint regressed (passed → failed)
- 2+ dimensions regressed by 2+ points

**REGRESSED demands root cause analysis.** Every regression must trace to a specific change. The benchmark report must answer: "What change caused this regression, and was it intentional?"

### TRANSFORMED

- Fundamental structural change (single-file → multi-file, complete rewrite, different skill architecture)
- Direct dimension comparison is misleading because the skills operate differently
- Score both independently. Present as parallel scorecards rather than deltas.

**TRANSFORMED is neither good nor bad.** A complete rewrite may be necessary. The benchmark acknowledges that pre/post comparison is apples-to-oranges and presents both evaluations separately.

## Trade-Off Analysis Framework

Not every regression is a problem. Some are deliberate trade-offs. The benchmark must distinguish intentional trade-offs from accidental regressions.

### Trade-Off Detection

A change is a trade-off (not a regression) when:
1. The same change that caused dimension X to drop also caused dimension Y to rise
2. The improvement in Y is larger than or equal to the loss in X
3. The change was deliberate (traceable to a specific intervention in the changelog)

| Trade-Off | Typical Cause | Assessment |
|-----------|--------------|------------|
| Depth ↑, Density ↓ | Added edge cases, failure modes, trade-offs | Acceptable — more content adds value even if less compressed |
| Clarity ↑, Simplicity ↓ | Added glossary, data contracts, explicit definitions | Acceptable — clarity for the reader > brevity for its own sake |
| Precision ↑, Foundation ↓ | Added numeric thresholds without explaining reasoning | Needs fix — precision without foundation is arbitrary numbers |
| Depth ↑, Value ↓ | Added sections that don't affect behavior | Needs fix — depth is only valuable if it changes output |

### Trade-Off Reporting

For each detected trade-off:
```
Trade-off: Density 9→8, Depth 5→8
Cause: Added 5 edge cases + failure modes table (surgeon-skill intervention B4)
Assessment: Acceptable — the added depth addresses real failure scenarios.
            The density loss is 1 point on sentences that could be tighter,
            not on filler. Net value positive.
```

## Against-Standard Comparison

When comparing against the gold standard (theoretical 10/10), the benchmark behaves differently:

| Aspect | Version Comparison | Standard Comparison |
|--------|-------------------|-------------------|
| State B | Real skill at a different point in time | Theoretical perfect skill |
| Regressions | Possible and critical to detect | Not possible (can't regress below yourself) |
| Net Assessment | IMPROVED / LATERAL / REGRESSED / TRANSFORMED | GAP-TO-STANDARD: how far from 10/10 |
| Primary value | "Did changes help?" | "How much room for improvement?" |
| Delta interpretation | Positive = improvement, negative = regression | All deltas show the gap (always positive or zero) |

### Standard Comparison Output

```markdown
## Gap to Gold Standard
| Dimension | Current | Standard | Gap | Highest-Impact Fix |
|-----------|---------|----------|-----|-------------------|
| Foundation | 7 | 10 | -3 | Add "because" reasoning to 8 ungrounded rules |
| Depth | 5 | 10 | -5 | Add 3+ edge cases, failure mode table, trade-offs |
| ... | | | | |
| Average | 7.2 | 10 | -2.8 | |

## Prioritized Gaps (by impact on certification)
1. Depth (gap: 5) — highest gap, lowest absolute score
2. Foundation (gap: 3) — affects every instruction's credibility
3. Precision (gap: 2) — vague criteria produce vague compliance
```

## Cross-Session Comparison Caveat

Scores from different sessions may vary by 1 point on subjective dimensions. When comparing:
- An x-ray-skill report from last week vs a certify-skill report from today
- Acknowledge the variance in the report header
- Focus on changes of 2+ points as reliable signals
- Changes of 1 point may be scoring variance, not actual improvement

The most reliable comparisons are same-session (benchmark-skill scores both states) because the same context and calibration apply to both.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
