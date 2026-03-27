# Analysis Patterns: Dyslexia, Typos & Autocorrect

This reference documents common patterns that signal surface-level errors, dyslexia-related reversals, and autocorrect artifacts. Use these patterns to detect and correct surface issues in Pass 1.

## Common Letter Reversals

These are high-confidence dyslexia signals. The user knows the correct word but their brain/fingers produce the reversed letter pair.

### Visual Reversals (Mirror Confusion)

| Correct | Common Error | Signal | Context |
|---------|-------------|--------|---------|
| b | d | Vertical line position confusion | "I nee to buld a deck" |
| d | b | Same pattern reversed | "The dat was corrupted" |
| p | q | Lower loop position | "I qon't know the aswer" |
| q | p | Same pattern reversed | "I have a question (epstion)" |

### Sequential Reversals (Adjacent Letter Swap)

| Correct | Common Error | Pattern | Example |
|---------|-------------|---------|---------|
| was | saw | Consonant cluster swap | "I saw it was wrong" vs "It saw obvious" |
| from | form | Vowel swap at word end | "Results form the test" |
| there | theer | Double-letter adjacency | "I've been theer before" |
| receive | recieve | i/e reversal (common across many words) | "Did you recieve the memo?" |
| quite | queit | Common in -eit endings | "That's a queit problem" |

### Double-Letter Reversals

| Pattern | Example | Detection Rule |
|---------|---------|-----------------|
| ll → ll (correct) | "I will tell you" | Single occurrence is normal |
| ll doubled → llll | "I willll tell you" | Three+ same letter in sequence |
| Single instead of double | "I wil tell you" | Known double-letter words missing one |

## Phonetic Substitutions

The user hears the word correctly but spells it by sound, producing homophones or near-homophones.

### Homophone Errors (Same Sound, Different Spelling)

| Correct | Common Error | Signal | Example |
|----------|-------------|--------|---------|
| there | their, they're | Context determines correct form | "Their going there with they're friends" |
| to | too, two | Homophone substitution | "I need to go to the store" vs "I want too" (meaning "also") |
| would | wood | Pronunciation confusion | "I wood like to" |
| through | threw | Past tense confusion | "I threw the door" |
| wear | where, ware | Homophone mixing | "Where is my shoes?" |
| its | it's | Possessive vs contraction | "The cat licked it's paw" |
| your | you're | Possessive vs contraction | "Your going to love this" |

### Near-Phonetic Substitutions

| Correct | Common Error | Signal | Example |
|----------|-------------|--------|---------|
| because | becuz, becuase | Phonetic respelling | "Becuz of the weather..." |
| friend | frend | Missing vowel sound | "My frend told me" |
| said | sed | Pronounced differently from spelling | "She sed it was fine" |
| people | poeple, pepol | Vowel order confusion | "Some poeple think..." |

## Missing Vowels Pattern

Common in fast typing or dyslexic patterns: vowels are omitted, creating consonant clusters that are hard to parse.

| Correct | Error Pattern | Signal | Example |
|---------|---------------|--------|---------|
| about | abt | Missing vowel in middle | "That's abt what I meant" |
| because | bcs, bcz | Multiple vowels missing | "bcs of the issue" |
| could | cld | Vowel cluster missing | "I cld be wrong" |
| would | wld | Same pattern | "Tht wld be nice" |
| should | shld | Same pattern | "You shld know this" |
| different | dffrnt, dffrent | Vowels removed entirely | "That's dffrnt from before" |
| important | imprtnt | Repeated vowel-removal | "This is imprtnt" |

### Detection Heuristic

**Rule:** If word has 2+ consecutive consonants with no vowels between them, check if inserting a vowel creates a known English word. Common insertion points: after first consonant cluster, in the middle, before final consonant.

**Regex Pattern:**
```
([bcdfghjklmnpqrstvwxyz]{2,})[bcdfghjklmnpqrstvwxyz]*
```

When matched, test vowel insertion at positions between consonants.

## Common Autocorrect Artifacts

Autocorrect systems introduce predictable errors. These appear when:
- User typed quickly and a wrong word was substituted
- Phone keyboard predicted wrong word (swipe typing errors)
- OS/browser autocorrect activated unexpectedly

### High-Confidence Autocorrect Signals

| Artifact | Common Source | Detection | Example |
|----------|---------------|-----------|---------|
| "ducking" | Profanity filter autocorrect | Swear word nearby in context, unusual word choice | "This is fucking annoying" → "This is ducking annoying" |
| "bitch" → "batch" | iOS/Android autocorrect | Unusual formality shift mid-sentence | Original context has casual tone |
| "teh" → "the" | Typo, not autocorrect | Two letters swapped, very common | "teh quick brown fox" |
| Letter substitution | Adjacent key on keyboard | Specific typo pattern (qwerty neighbors) | "wirking" instead of "working" (d/f neighbors) |
| Random capitalization | Voice-to-text | Name words capitalized mid-sentence | "I talked to Sarah... no I mean My Friend Sarah" |

### QWERTY Neighbor Errors

Detect by checking if substitution character is adjacent on keyboard:

```
Standard QWERTY mapping:
q w e r t y u i o p
 a s d f g h j k l
  z x c v b n m

Common neighbor pairs:
- e/r, r/t, t/y (top row horizontal)
- a/s, s/d, d/f (middle row horizontal)
- z/x, x/c, c/v (bottom row horizontal)
- r/f, t/g, y/h, u/j (vertical pairs)
```

## Punctuation Error Patterns

Missing, incorrect, or excessive punctuation that changes meaning.

### Missing Punctuation (No Caps, Run-ons, Fragments)

| Pattern | Signal | Example | Fix |
|---------|--------|---------|-----|
| No sentence breaks | All lowercase, no periods | "i need to build a function that sorts lists and validates input and returns errors if something breaks" | Add periods at logical boundaries |
| Missing comma in list | Run-on with "and" | "I need to add users groups projects and teams" | Separate with commas |
| Missing opening quote | Quote mark appears mid-sentence | `He said "I'm here and never closed the quote` | Add closing quote |
| Double punctuation | !! ?? ... | "What!!!??? This is terrible!!" | Normalize to single punctuation |

### Incorrect Punctuation

| Error Type | Pattern | Example | Fix |
|-----------|---------|---------|-----|
| Period instead of comma | "I need help. Can you assist?" | "I need help, can you assist?" (if dependent) | Context-aware replacement |
| Apostrophe for plural | "The dog's are running" | "The dogs are running" | Remove possessive from plural |
| Missing apostrophe | "Its a problem" | "It's a problem" | Add apostrophe to contraction |

### Excessive Punctuation

| Pattern | Signal | Example |
|---------|--------|---------|
| Multiple periods | "I don't know...." | Replace with single period |
| Multiple exclamation | "This is amazing!!!" | Normalize to single |
| Mixed punctuation | "What?!?!?!" | Simplify to "What?" or "What?!" |

## Mixed Language Detection Signals

When code, technical syntax, or another language appears in casual text.

### Code Embedded in Text

| Signal | Example | Detection |
|--------|---------|-----------|
| Function calls | "I need to parseInt(myVar) and then" | Detect patterns: `word(` with lowercase start |
| Variable assignment | "set x = y and then do something" | Keywords: "set", "var", "let", "const" followed by identifier |
| Pseudocode | "if user is logged then show page" | Keywords: "if", "then", "else", "for", "while" in English sentence |
| URL/path | "Navigate to https://example.com/path" | Detect URL patterns and file paths |

### Code-Like Syntax Artifacts

| Pattern | Example | Fix |
|---------|---------|-----|
| Markdown headers | "## My Section Title" appearing mid-paragraph | Extract and structure properly |
| JSON keys | "The field 'firstName' contains..." | Detect quoted keywords |
| SQL-like | "Select all users Where age > 18" | Detect capitalized SQL keywords |

### Language Mixing

| Signal | Example | Context |
|--------|---------|---------|
| Spanish-English switch | "Necesito hacer un feature para mañana" | Note language; may need monolingual processing |
| French-English | "Je veux créer a new document" | Same as above |

## Detection Heuristics as Regex-Friendly Patterns

### Pattern Library for Automated Detection

```
# LETTER REVERSALS
- Pattern: \b(recieve|thier|teh|hte|kown|cant\b|dont\b|woudl|siad)\b
  Confidence: HIGH (these are almost always errors)

# PHONETIC SUBSTITUTIONS
- Pattern: \b(becuz|becuse|becuz|becuase)\b
  Confidence: HIGH (phonetic spelling of "because")

- Pattern: \bthere\s+(is|are|be).*\bthere\b|\bthere\b.*\btheir\b|\bthere\b.*\bthey're\b
  Confidence: MEDIUM (needs context analysis)

# MISSING VOWELS
- Pattern: ([bcdfghjklmnpqrstvwxyz]){3,}
  Confidence: MEDIUM (check if vowel insertion creates word)

# AUTOCORRECT ARTIFACTS
- Pattern: \b(ducking|freaking|fudging)\b (in non-literal context)
  Confidence: HIGH (almost always autocorrect)

- Pattern: \b(teh|teh|hte)\b
  Confidence: VERY HIGH (classic transposition error)

# QWERTY NEIGHBOR ERRORS
- Pattern: wirking|wirk (instead of working/work)
  Confidence: MEDIUM (context-dependent)

# MISSING PUNCTUATION
- Pattern: ^\s*[a-z] | [a-z]\s+[a-z]{2,}\s+and | [^.!?]\s*$
  Confidence: MEDIUM (lowercase start, run-on with "and", no ending punctuation)

# DOUBLE LETTERS
- Pattern: ([a-z])\1{3,}
  Confidence: HIGH (4+ same letter is almost always error)

# CONTRACTED FORMS MISTAKES
- Pattern: \b(im|youre|hes|shes|theyre|its)\b
  Confidence: MEDIUM (could be intentional, check context)
```

## Integration with Pass 1 (Surface Analysis)

Use these patterns to build the correction dictionary for `typo-detector.py`:

1. **Load high-confidence patterns first** (recieve, teh, becuz, ducking)
2. **Check context for medium-confidence patterns** (there/their/they're, its/it's)
3. **Apply vowel insertion heuristic** for missing vowel patterns
4. **Detect keyboard neighbors** for adjacent-key typos
5. **Normalize punctuation** and add missing periods/commas
6. **Flag mixed language** for user awareness (don't auto-correct)

Each correction should preserve original intent while fixing surface issues only. When in doubt, flag for human review rather than auto-correct.
