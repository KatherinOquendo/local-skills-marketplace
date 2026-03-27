# Analysis Patterns: Surface Error Detection

Pattern library for Pass 1. Organized by error type, each with detection confidence, regex patterns, and correction strategy. Use this to extend or calibrate `scripts/typo-detector.py`.

## Table of Contents

1. [Letter Reversals](#letter-reversals) — dyslexia-related visual and sequential swaps
2. [Phonetic Substitutions](#phonetic-substitutions) — homophones and near-homophones
3. [Missing Vowels](#missing-vowels) — fast-typing consonant clusters
4. [Autocorrect Artifacts](#autocorrect-artifacts) — OS/keyboard prediction errors
5. [QWERTY Neighbor Errors](#qwerty-neighbor-errors) — adjacent-key misstrikes
6. [Punctuation Errors](#punctuation-errors) — missing, incorrect, excessive
7. [Mixed Language & Code Signals](#mixed-language--code-signals) — language switching, embedded syntax
8. [Confidence Framework](#confidence-framework) — when to auto-correct vs flag
9. [Regex Pattern Library](#regex-pattern-library) — copy-paste detection patterns

## Letter Reversals

### Visual Reversals (Mirror Confusion)

High-confidence dyslexia signal. The user knows the correct word; their brain produces the mirrored letter.

| Pair | Direction | Example in Context | Confidence |
|------|-----------|-------------------|------------|
| b ↔ d | Vertical line confusion | "I nee**d** to **b**uild" → "I nee**b** to **d**uild" | HIGH |
| p ↔ q | Lower loop confusion | "I **q**on't know" → "I **p**on't know" | HIGH |
| m ↔ w | Rotational confusion | "**w**ake" ↔ "**m**ake" (context-dependent) | MEDIUM — requires context |

### Sequential Reversals (Adjacent Letter Swap)

| Correct | Error | Pattern | Detection Rule |
|---------|-------|---------|----------------|
| was | saw | Full word reversal | Check if reversed word is also valid English — requires context |
| from | form | Interior swap | Known word pair; common in fast typing |
| receive | recieve | i/e swap | Applies to all -eive/-ieve words: believe, perceive, achieve |
| there | theer | Doubled adjacency | 3+ character window with repeated vowels |

**Key insight:** Sequential reversals produce valid English words ("form" for "from", "saw" for "was"), making them harder to detect without sentence context. Flag as MEDIUM confidence and check surrounding syntax.

### Double-Letter Errors

| Pattern | Example | Detection |
|---------|---------|-----------|
| Missing double | "wil" for "will", "tel" for "tell" | Known double-letter words + edit distance 1 |
| Extra repetition | "willll", "helllo" | 3+ consecutive identical chars → `([a-z])\1{2,}` |
| Wrong letter doubled | "comming" for "coming" | Dictionary lookup + common patterns |

## Phonetic Substitutions

The user hears correctly but spells by sound.

### High-Impact Homophones

These are the most frequently observed phonetic errors in English user input:

| Correct | Errors | Detection Strategy |
|---------|--------|-------------------|
| there / their / they're | Context: location vs possessive vs contraction | Parse sentence role: subject → "they're", possessive → "their", location → "there" |
| your / you're | Possessive vs contraction | If followed by verb/adjective → likely "you're"; if followed by noun → "your" |
| its / it's | Possessive vs contraction | Same rule as your/you're; "its" before noun, "it's" before verb/adj |
| to / too / two | Preposition vs adverb vs number | "too" = "also" or "excessively"; "two" = number; "to" = everything else |
| affect / effect | Verb vs noun (usually) | "affect" as verb, "effect" as noun — but exceptions exist; flag MEDIUM |

### Near-Phonetic Substitutions

| Correct | Common Errors | Confidence |
|---------|--------------|------------|
| because | becuz, becuase, becuse, cuz | HIGH — unambiguous misspellings |
| friend | frend, freind | HIGH |
| said | sed | MEDIUM — could be intentional abbreviation |
| people | poeple, pepol | HIGH |
| definitely | definately, definatly, defiantly | HIGH — "defiantly" is almost always a misspelling of "definitely" |
| separate | seperate | HIGH — one of the most common misspellings in English |

## Missing Vowels

Fast typing or intentional abbreviation removes vowels, creating consonant clusters.

| Correct | Pattern | Context Signal |
|---------|---------|----------------|
| about | abt | Informal/chat context → intentional. Formal context → error |
| because | bcs, bcz | Almost always intentional abbreviation |
| could / would / should | cld, wld, shld | Chat abbreviation |
| different | dffrnt | Error — too compressed to be intentional |
| important | imprtnt | Error — same pattern |

**Detection heuristic:** If a word has 3+ consecutive consonants with no vowels, test vowel insertion at each inter-consonant position. If exactly one insertion produces a known English word, correct with HIGH confidence. If multiple insertions produce valid words, flag MEDIUM.

**Decision: intentional vs error.** Abbreviations like "abt", "bcs", "pls" are widely accepted in casual contexts. Correct only in formal contexts or when the rest of the message uses full words (inconsistency signals error, not style).

## Autocorrect Artifacts

OS/keyboard autocorrect introduces a distinct error class: the wrong word is spelled correctly.

### High-Confidence Autocorrect Signals

| Artifact | Source | Detection |
|----------|--------|-----------|
| "ducking" in non-duck context | Profanity filter | Surrounding casual/frustrated tone |
| Random capitalization mid-sentence | Voice-to-text | Proper nouns where common nouns expected |
| Wrong but similar word | Swipe typing | "wirking" → "working", "tge" → "the" |
| Grammatically correct but semantically wrong | Predictive text | Sentence parses fine but meaning is off |

**Key insight:** Autocorrect errors are harder to detect than typos because the resulting word is valid. Detection requires semantic analysis, not just spelling checks. When an otherwise fluent sentence contains one semantically jarring word, suspect autocorrect.

## QWERTY Neighbor Errors

Adjacent-key misstrikes follow the keyboard layout:

```
q w e r t y u i o p
 a s d f g h j k l
  z x c v b n m
```

**Common neighbor pairs** (horizontal + vertical):
- Top row: e↔r, r↔t, t↔y, u↔i, i↔o
- Middle row: a↔s, s↔d, d↔f, f↔g, h↔j, j↔k, k↔l
- Bottom row: z↔x, x↔c, c↔v, v↔b, b↔n, n↔m
- Vertical: q↔a, w↔s, e↔d, r↔f, t↔g, y↔h, u↔j, i↔k, o↔l

**Detection:** For each unrecognized word, substitute each character with its QWERTY neighbors. If exactly one substitution produces a known word, correct with HIGH confidence.

**Limitations:**
- Does not work for non-QWERTY layouts (AZERTY, Dvorak). If error patterns don't match QWERTY neighbors, the user may have a different keyboard layout.
- Mobile keyboards have different adjacency maps (larger touch targets, predictive text). Mobile errors tend toward autocorrect artifacts and swipe-typing mismatches rather than QWERTY neighbor errors. Treat mobile input as a blend of this section and the Autocorrect Artifacts section.

## Punctuation Errors

### Missing Punctuation

| Pattern | Signal | Correction Strategy |
|---------|--------|-------------------|
| No sentence breaks (all lowercase, no periods) | Fast typing, mobile input | Insert periods at natural clause boundaries |
| Missing list commas | "users groups projects teams" | Insert commas; check for serial comma style |
| Unclosed quotes/parentheses | Structural error | Flag but don't auto-close — position is ambiguous |

### Incorrect Punctuation

| Error | Example | Rule |
|-------|---------|------|
| Apostrophe for plural | "the dog's are running" | Remove apostrophe unless possessive |
| Missing contraction apostrophe | "dont", "cant", "wont" | Add apostrophe: "don't", "can't", "won't" |
| Period instead of comma | "I need help. can you assist" | Lowercase after period signals run-on → replace with comma |

### Excessive Punctuation

Normalize: `!!!` → `!`, `???` → `?`, `....` → `.`, `?!?!` → `?!`

**Exception:** Preserve double punctuation when it signals emphasis intentionally (e.g., "Really??" in casual context). Normalize only when excessive (3+).

## Mixed Language & Code Signals

### Code Embedded in Text

| Signal | Example | Detection |
|--------|---------|-----------|
| Function calls | "I need to parseInt(myVar)" | Pattern: `\w+\(` with camelCase identifier |
| Variable names | "set x = y and then do" | Keywords: let, const, var, set before identifier |
| Pseudocode | "if user is logged then show page" | Control flow keywords in natural language sentence |
| Paths/URLs | "/api/users/123" | Pattern: starts with `/` or `http` |

**Decision:** Don't "correct" code syntax embedded in text. Preserve it exactly and note the mixed context.

### Language Switching

| Pattern | Example | Action |
|---------|---------|--------|
| Spanish-English | "Necesito hacer un feature para el dashboard" | Note primary language; preserve technical terms in their original language |
| Spanglish patterns | "deployear", "commitear", "pushear" | Recognize as hybrid verbs; don't correct to either language |
| Code-switch mid-sentence | "el API returns un error" | Preserve; flag as mixed-language for downstream awareness |

**Limitation:** This skill handles major language pairs (Spanish-English, French-English) but not all combinations. For unsupported pairs, flag the mixed content and proceed with best-effort analysis.

## Confidence Framework

Every correction must carry a confidence level that determines the action:

| Level | Criteria | Action |
|-------|----------|--------|
| VERY HIGH | Classic transposition ("teh" → "the"), repeated letters ("helllo") | Auto-correct silently |
| HIGH | Known misspelling with single valid correction ("recieve" → "receive") | Auto-correct, include in corrections list |
| MEDIUM | Context-dependent homophone, abbreviation in formal context | Flag as suggestion; present both options |
| LOW | Semantic autocorrect, ambiguous abbreviation, word valid in both forms | Flag only; do not auto-correct |

**Core principle:** It's better to leave a typo intact than to introduce a wrong correction. When confidence is below HIGH, present options rather than deciding.

## Regex Pattern Library

Copy-paste patterns for automated detection:

```python
# VERY HIGH confidence — auto-correct
TRANSPOSITIONS = r'\b(teh|hte|taht|waht|adn|nad|ahve|hvae)\b'
REPEATED_CHARS = r'([a-z])\1{2,}'  # 3+ same letter
COMMON_MISSPELLINGS = r'\b(recieve|occured|seperate|definately|accomodate|occassion)\b'

# HIGH confidence — correct + log
PHONETIC = r'\b(becuz|becuse|becuase|frend|freind|sed|poeple|pepol)\b'
MISSING_APOSTROPHE = r'\b(dont|cant|wont|shouldnt|wouldnt|couldnt|didnt|isnt|arent|wasnt|werent|hasnt|havent|hadnt)\b'
AUTOCORRECT_PROFANITY = r'\b(ducking|freaking|fudging)\b'  # in non-literal context

# MEDIUM confidence — flag as suggestion
HOMOPHONES = r'\b(there|their|they\'re|your|you\'re|its|it\'s|to|too|two|affect|effect)\b'
MISSING_VOWELS = r'\b[bcdfghjklmnpqrstvwxyz]{3,}\b'  # 3+ consonants, no vowels
CONTRACTED_FORMS = r'\b(im|youre|hes|shes|theyre|whos|whats)\b'

# LOW confidence — flag only
NO_END_PUNCTUATION = r'[^.!?\n]\s*$'
LOWERCASE_START = r'^\s*[a-z]'
EXCESSIVE_PUNCTUATION = r'[!?]{3,}|\.{4,}'
```

## Integration with Pass 1

Processing order matters — apply detections in this sequence:

1. **VERY HIGH confidence corrections first** — transpositions, repeated chars, classic misspellings
2. **HIGH confidence corrections** — phonetic errors, missing apostrophes, autocorrect artifacts
3. **Punctuation normalization** — missing periods, excessive punctuation, unclosed quotes
4. **MEDIUM confidence flags** — homophones, missing vowels (present as suggestions, not corrections)
5. **Language/code detection** — mixed language flags, embedded syntax (preserve, don't correct)

Each correction records: original text, corrected text, confidence level, and pattern that triggered it. This audit trail enables Pass 5 to verify that no meaning was altered.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
