#!/usr/bin/env python3
"""
prompt-evaluator.py — Scores a prompt against the 10-criterion rubric.

Usage:
    python prompt-evaluator.py <path-to-prompt.md>
    python prompt-evaluator.py <path-to-prompt.md> --json
    python prompt-evaluator.py <path-to-prompt.md> --verbose
    python prompt-evaluator.py <path-to-prompt.md> --strict

Reads a markdown prompt file and evaluates it against structural
and content quality criteria. Outputs a scorecard with per-criterion
scores, identified issues, and fix suggestions.

Note: This tool performs heuristic/structural analysis. For deep
semantic evaluation, combine with LLM-as-a-judge review.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# --- Criterion Checkers ---

def check_foundation(content: str, sections: dict) -> dict:
    """Criterion 1: Structural completeness."""
    score = 10
    issues = []

    essential = ["role", "objective", "constraint", "output"]
    found = {k: False for k in essential}

    for key in essential:
        for section_name in sections:
            if key in section_name.lower():
                found[key] = True
                break

    # Also check content patterns
    if not found["role"]:
        if re.search(r"(you are|archetype|persona|role)", content, re.I):
            found["role"] = True

    if not found["objective"]:
        if re.search(r"(objective|goal|purpose|mission)", content, re.I):
            found["objective"] = True

    missing = [k for k, v in found.items() if not v]
    if missing:
        score -= len(missing) * 2
        issues.append(f"Missing sections: {', '.join(missing)}")

    # Check for hybrid archetype
    role_patterns = re.findall(r"(expert|specialist|consultant|advisor|strategist|engineer|analyst)", content, re.I)
    if len(set(role_patterns)) < 2:
        score -= 1
        issues.append("Role may be single-dimensional (consider hybrid archetype: domain + methodology + style)")

    return {"score": max(1, score), "issues": issues}


def check_accuracy(content: str, sections: dict) -> dict:
    """Criterion 2: Factual correctness heuristics."""
    score = 10
    issues = []

    # Check for potentially made-up framework names
    suspicious_patterns = [
        r"\b[A-Z]{5,}\b",  # Very long acronyms that might be invented
    ]
    for pattern in suspicious_patterns:
        matches = re.findall(pattern, content)
        known_acronyms = {"ALWAYS", "NEVER", "IMPORTANT", "CRITICAL", "WARNING", "PHASE", "STATE", "TABLE"}
        unknown = [m for m in matches if m not in known_acronyms]
        if len(unknown) > 5:
            score -= 1
            issues.append(f"Multiple unfamiliar acronyms detected ({len(unknown)}). Verify they reference real frameworks.")

    return {"score": max(1, score), "issues": issues}


def check_quality(content: str, sections: dict) -> dict:
    """Criterion 3: Writing quality."""
    score = 10
    issues = []

    # Filler words
    filler_patterns = [
        r"\bbasically\b", r"\bessentially\b", r"\bin order to\b",
        r"\bactually\b", r"\bjust\b", r"\breally\b",
        r"\bvery\b", r"\bquite\b", r"\bsimply\b"
    ]
    filler_count = sum(len(re.findall(p, content, re.I)) for p in filler_patterns)
    word_count = len(content.split())
    filler_ratio = filler_count / max(word_count, 1)

    if filler_ratio > 0.02:
        score -= 2
        issues.append(f"High filler word ratio ({filler_count} filler words in {word_count} words)")
    elif filler_ratio > 0.01:
        score -= 1
        issues.append(f"Moderate filler word usage ({filler_count} instances)")

    # Passive voice (rough heuristic)
    passive_patterns = re.findall(r"\b(is|are|was|were|been|be)\s+\w+ed\b", content, re.I)
    if len(passive_patterns) > 10:
        score -= 1
        issues.append(f"Frequent passive voice ({len(passive_patterns)} instances). Consider active voice.")

    return {"score": max(1, score), "issues": issues}


def check_density(content: str, sections: dict) -> dict:
    """Criterion 4: Information-to-token ratio."""
    score = 10
    issues = []

    word_count = len(content.split())
    section_count = len(sections)

    if section_count > 0:
        avg_section_length = word_count / section_count
        if avg_section_length > 500:
            score -= 2
            issues.append(f"Average section length is {avg_section_length:.0f} words. Consider compression.")
        elif avg_section_length > 300:
            score -= 1
            issues.append(f"Some sections may be verbose (avg {avg_section_length:.0f} words/section)")

    # Check for duplicate sentences (rough)
    sentences = re.split(r'[.!?]\s', content)
    sentences_clean = [s.strip().lower() for s in sentences if len(s.strip()) > 20]
    seen = set()
    duplicates = 0
    for s in sentences_clean:
        if s in seen:
            duplicates += 1
        seen.add(s)

    if duplicates > 3:
        score -= 2
        issues.append(f"Found {duplicates} duplicate or near-duplicate sentences")
    elif duplicates > 0:
        score -= 1
        issues.append(f"Found {duplicates} duplicate sentence(s)")

    # Total length check
    if word_count > 5000:
        score -= 1
        issues.append(f"Total length ({word_count} words) is high for a system prompt. Consider moving reference material to knowledge base files.")

    return {"score": max(1, score), "issues": issues}


def check_simplicity(content: str, sections: dict) -> dict:
    """Criterion 5: Structural accessibility."""
    score = 10
    issues = []

    # Check nesting depth
    max_heading_level = 0
    for line in content.split("\n"):
        match = re.match(r"^(#{1,6})\s", line)
        if match:
            level = len(match.group(1))
            max_heading_level = max(max_heading_level, level)

    if max_heading_level > 4:
        score -= 2
        issues.append(f"Heading nesting depth of {max_heading_level} is excessive. Flatten to max H3.")
    elif max_heading_level > 3:
        score -= 1
        issues.append("Consider flattening heading hierarchy (currently uses H4+)")

    # Check for jargon density
    jargon = [
        r"\btoken\b", r"\bRAG\b", r"\bembedding", r"\bvector",
        r"\blatency\b", r"\bthroughput\b", r"\binference\b",
        r"\bfine-tun", r"\bhallucina"
    ]
    jargon_count = sum(len(re.findall(p, content, re.I)) for p in jargon)
    if jargon_count > 20:
        score -= 1
        issues.append(f"High technical jargon density ({jargon_count} instances). May be inaccessible to non-technical users.")

    return {"score": max(1, score), "issues": issues}


def check_clarity(content: str, sections: dict) -> dict:
    """Criterion 6: Unambiguity."""
    score = 10
    issues = []

    # Vague qualifiers
    vague_patterns = [
        (r"\bappropriate\b", "appropriate"),
        (r"\bas needed\b", "as needed"),
        (r"\bwhen necessary\b", "when necessary"),
        (r"\bsometimes\b", "sometimes"),
        (r"\bgenerally\b", "generally"),
        (r"\btypically\b", "typically"),
    ]

    for pattern, word in vague_patterns:
        count = len(re.findall(pattern, content, re.I))
        if count > 3:
            score -= 1
            issues.append(f"Vague qualifier '{word}' used {count} times. Replace with specific conditions.")

    return {"score": max(1, score), "issues": issues}


def check_precision(content: str, sections: dict) -> dict:
    """Criterion 7: Constraint specificity."""
    score = 10
    issues = []

    # Aspirational constraints
    aspirational = [
        r"\bbe professional\b",
        r"\bkeep it concise\b",
        r"\bbe helpful\b",
        r"\bbe accurate\b",
        r"\buse good judgment\b",
    ]

    for pattern in aspirational:
        if re.search(pattern, content, re.I):
            score -= 1
            issues.append(f"Aspirational constraint detected: '{pattern.strip(chr(92)).strip('b')}'. Convert to specific, testable rule.")

    # Check for quantified constraints
    has_quantified = bool(re.search(r"\b(maximum|minimum|at least|at most|no more than|exactly)\s+\d+", content, re.I))
    if not has_quantified:
        score -= 1
        issues.append("No quantified constraints found. Consider adding specific limits (word counts, max items, etc.)")

    return {"score": max(1, score), "issues": issues}


def check_depth(content: str, sections: dict) -> dict:
    """Criterion 8: Edge case handling."""
    score = 10
    issues = []

    # Check for error/edge case handling
    edge_patterns = [
        r"(edge case|corner case)",
        r"(error|fail|fallback)",
        r"(if .* missing|if .* unclear|if .* ambiguous)",
        r"(out of scope|not supported|cannot)",
    ]

    found_edge = sum(1 for p in edge_patterns if re.search(p, content, re.I))
    if found_edge == 0:
        score -= 3
        issues.append("No edge case or error handling found. Add fallback behavior for ambiguous/missing/invalid inputs.")
    elif found_edge < 2:
        score -= 1
        issues.append("Minimal edge case handling. Consider adding more fallback behaviors.")

    # Check for self-correction
    if not re.search(r"(self.correct|trigger|recalibrat|recover)", content, re.I):
        score -= 1
        issues.append("No self-correction triggers found. Add recovery behaviors for common failure modes.")

    return {"score": max(1, score), "issues": issues}


def check_coherence(content: str, sections: dict) -> dict:
    """Criterion 9: Internal consistency."""
    score = 10
    issues = []

    # Check for contradicting patterns (basic heuristic)
    has_always = set(re.findall(r"always\s+(\w+)", content, re.I))
    has_never = set(re.findall(r"never\s+(\w+)", content, re.I))
    contradictions = has_always & has_never

    if contradictions:
        score -= 2
        issues.append(f"Potential contradictions: words used with both ALWAYS and NEVER: {contradictions}")

    # Check that output template exists if deliverable is mentioned
    mentions_deliverable = bool(re.search(r"(deliverable|output|produce|generate)", content, re.I))
    has_template = bool(re.search(r"(template|format|structure)", content, re.I))
    if mentions_deliverable and not has_template:
        score -= 1
        issues.append("Mentions deliverables but no output template/format found. Add a concrete output structure.")

    return {"score": max(1, score), "issues": issues}


def check_value(content: str, sections: dict) -> dict:
    """Criterion 10: Delta over base model."""
    score = 10
    issues = []

    # Check for domain-specific content
    has_methodology = bool(re.search(r"(framework|methodology|approach|technique|strategy|principle)", content, re.I))
    has_constraints = bool(re.search(r"(constraint|rule|boundary|limit|must not|do not)", content, re.I))
    has_output_format = bool(re.search(r"(template|format|structure|schema)", content, re.I))
    has_reasoning = bool(re.search(r"(analyze|reason|think|evaluate|consider)", content, re.I))

    components = [has_methodology, has_constraints, has_output_format, has_reasoning]
    present = sum(components)

    if present <= 1:
        score -= 3
        issues.append("Low value-add: prompt mainly provides formatting, not expertise. Add domain methodology, constraints, and reasoning directives.")
    elif present == 2:
        score -= 1
        issues.append("Moderate value-add. Consider strengthening with additional domain-specific methodology or reasoning patterns.")

    return {"score": max(1, score), "issues": issues}


# --- Main Logic ---

CRITERIA = [
    ("Foundation", check_foundation),
    ("Accuracy", check_accuracy),
    ("Quality", check_quality),
    ("Density", check_density),
    ("Simplicity", check_simplicity),
    ("Clarity", check_clarity),
    ("Precision", check_precision),
    ("Depth", check_depth),
    ("Coherence", check_coherence),
    ("Value", check_value),
]


def parse_sections(content: str) -> dict:
    """Extract markdown sections by heading."""
    sections = {}
    current_heading = "preamble"
    current_content = []

    for line in content.split("\n"):
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            sections[current_heading] = "\n".join(current_content)
            current_heading = match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    sections[current_heading] = "\n".join(current_content)
    return sections


def evaluate(filepath: str, verbose: bool = False, strict: bool = False) -> dict:
    """Run full evaluation on a prompt file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")

    # Strip YAML frontmatter if present
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].strip()

    sections = parse_sections(content)

    word_count = len(content.split())
    results = []
    total_score = 0

    for name, checker in CRITERIA:
        result = checker(content, sections)
        result["criterion"] = name
        results.append(result)
        total_score += result["score"]

    avg_score = total_score / len(CRITERIA)
    threshold = 8 if strict else 6

    failures = [r for r in results if r["score"] < threshold]

    return {
        "file": str(path),
        "word_count": word_count,
        "section_count": len(sections),
        "criteria": results,
        "average_score": round(avg_score, 1),
        "total_score": total_score,
        "max_possible": len(CRITERIA) * 10,
        "pass": len(failures) == 0,
        "failures": [r["criterion"] for r in failures],
        "threshold": threshold,
    }


def print_scorecard(result: dict, verbose: bool = False):
    """Print a formatted scorecard."""
    print(f"\n{'='*60}")
    print(f"  PROMPT EVALUATION SCORECARD")
    print(f"{'='*60}")
    print(f"  File: {result['file']}")
    print(f"  Words: {result['word_count']}  |  Sections: {result['section_count']}")
    print(f"  Threshold: {result['threshold']}/10 per criterion")
    print(f"{'='*60}\n")

    for r in result["criteria"]:
        bar = "█" * r["score"] + "░" * (10 - r["score"])
        status = "✓" if r["score"] >= result["threshold"] else "✗"
        print(f"  {status} {r['criterion']:<14} [{bar}] {r['score']}/10")

        if verbose and r["issues"]:
            for issue in r["issues"]:
                print(f"    → {issue}")

    print(f"\n{'─'*60}")
    print(f"  Average: {result['average_score']}/10  |  Total: {result['total_score']}/{result['max_possible']}")

    if result["pass"]:
        print(f"  Status: ✓ PASS")
    else:
        print(f"  Status: ✗ FAIL — Fix: {', '.join(result['failures'])}")

    print(f"{'─'*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a prompt against the 10-criterion rubric"
    )
    parser.add_argument("file", help="Path to the prompt markdown file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed issues")
    parser.add_argument("--strict", action="store_true", help="Use strict threshold (8 instead of 6)")

    args = parser.parse_args()

    result = evaluate(args.file, verbose=args.verbose, strict=args.strict)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_scorecard(result, verbose=args.verbose or True)

    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
