#!/usr/bin/env python3
"""
Rubric Evaluator: Score content against 10-criterion excellence rubric.

Usage:
    python rubric-evaluator.py <file_path> [--strict] [--json] [--verbose]

Criteria:
    1. Fundamento: Structural completeness
    2. Veracidad: Factual accuracy
    3. Calidad: Writing quality
    4. Densidad: Information density
    5. Simplicidad: Accessibility
    6. Claridad: Unambiguity
    7. Precisión: Specificity
    8. Profundidad: Edge case coverage
    9. Coherencia: Internal consistency
    10. Valor: User impact

Output:
    - Formatted scorecard (default)
    - JSON format (--json)
    - Detailed issues (--verbose)
    - Strict mode threshold: 10/10 (--strict, default: 8/10)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class RubricEvaluator:
    """Evaluates content against 10-criterion excellence rubric."""

    CRITERIA = [
        'fundamento',
        'veracidad',
        'calidad',
        'densidad',
        'simplicidad',
        'claridad',
        'precision',
        'profundidad',
        'coherencia',
        'valor',
    ]

    CRITERION_NAMES = {
        'fundamento': 'Fundamento (Foundation)',
        'veracidad': 'Veracidad (Truthfulness)',
        'calidad': 'Calidad (Quality)',
        'densidad': 'Densidad (Density)',
        'simplicidad': 'Simplicidad (Simplicity)',
        'claridad': 'Claridad (Clarity)',
        'precision': 'Precisión (Precision)',
        'profundidad': 'Profundidad (Depth)',
        'coherencia': 'Coherencia (Coherence)',
        'valor': 'Valor (Value)',
    }

    def __init__(self, filepath: str):
        """Initialize evaluator with content file."""
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()

        self.scores: Dict[str, int] = {}
        self.issues: Dict[str, List[str]] = {c: [] for c in self.CRITERIA}

    def evaluate(self) -> Dict[str, int]:
        """Run all criterion checks and return scores."""
        self.check_fundamento()
        self.check_veracidad()
        self.check_calidad()
        self.check_densidad()
        self.check_simplicidad()
        self.check_claridad()
        self.check_precision()
        self.check_profundidad()
        self.check_coherencia()
        self.check_valor()
        return self.scores

    def _score(self, criterion: str, points: int, issue: str = ""):
        """Record a score and optional issue."""
        self.scores[criterion] = points
        if issue:
            self.issues[criterion].append(issue)

    def _get_lines(self) -> List[str]:
        """Split content into lines."""
        return self.content.split('\n')

    def _get_sentences(self) -> List[str]:
        """Split content into sentences."""
        # Simple sentence splitter: split on . ! ? followed by space
        sentences = re.split(r'(?<=[.!?])\s+', self.content)
        return [s.strip() for s in sentences if s.strip()]

    def _get_words(self) -> List[str]:
        """Split content into words."""
        return re.findall(r'\b\w+\b', self.content.lower())

    def _has_heading_hierarchy(self) -> Tuple[int, int]:
        """Return (max_depth, section_count)."""
        lines = self._get_lines()
        max_depth = 0
        section_count = 0
        for line in lines:
            match = re.match(r'^(#+)', line)
            if match:
                depth = len(match.group(1))
                max_depth = max(max_depth, depth)
                section_count += 1
        return max_depth, section_count

    # ========================
    # CRITERION 1: Fundamento
    # ========================

    def check_fundamento(self):
        """Check structural completeness."""
        max_depth, section_count = self._has_heading_hierarchy()

        # Check for core structure
        score = 10
        lines = self._get_lines()
        has_intro = any('intro' in line.lower() or 'overview' in line.lower()
                       for line in lines[:5] if line.strip())
        has_conclusion = any('conclud' in line.lower() or 'summary' in line.lower()
                            for line in lines[-5:] if line.strip())

        if not has_intro:
            score -= 2
            self.issues['fundamento'].append("No clear introduction/overview")

        if not has_conclusion:
            score -= 2
            self.issues['fundamento'].append("No clear conclusion/summary")

        if section_count < 3:
            score -= 2
            self.issues['fundamento'].append("Too few sections; structure unclear")

        if max_depth > 5:
            score -= 1
            self.issues['fundamento'].append(f"Deep heading hierarchy ({max_depth} levels)")

        self._score('fundamento', max(2, score))

    # ========================
    # CRITERION 2: Veracidad
    # ========================

    def check_veracidad(self):
        """Check factual accuracy and weasel word usage."""
        score = 10
        words = self._get_words()

        # Weasel word patterns
        weasel_words = [
            'somehow', 'mysteriously', 'apparently', 'allegedly',
            'arguably', 'supposedly', 'purportedly', 'reputedly',
            'it is said', 'it is believed', 'it is thought',
            'seems to', 'appears to', 'rather', 'quite', 'somewhat'
        ]

        weasel_count = 0
        for weasel in weasel_words:
            pattern = r'\b' + weasel.replace(' ', r'\s') + r'\b'
            weasel_count += len(re.findall(pattern, self.content.lower()))

        if weasel_count >= 6:
            score -= 4
            self.issues['veracidad'].append(f"Heavy weasel word usage ({weasel_count} instances)")
        elif weasel_count >= 3:
            score -= 2
            self.issues['veracidad'].append(f"Several weasel words ({weasel_count} instances)")
        elif weasel_count >= 1:
            score -= 1
            self.issues['veracidad'].append(f"Some weasel words ({weasel_count} instances)")

        # Check for unsupported numeric claims
        numbers = re.findall(r'\d+(?:\.\d+)?', self.content)
        has_sources = bool(re.search(r'(source|cite|according|research|study)', self.content.lower()))

        if len(numbers) > 5 and not has_sources:
            score -= 2
            self.issues['veracidad'].append("Numeric claims without citations")

        self._score('veracidad', max(2, score))

    # ========================
    # CRITERION 3: Calidad
    # ========================

    def check_calidad(self):
        """Check writing quality: passive voice, filler words, consistency."""
        score = 10
        sentences = self._get_sentences()

        # Passive voice check: "is/was + past participle" or "to be + verb"
        passive_count = 0
        for sent in sentences:
            if re.search(r'\b(is|are|was|were|be|been)\s+\w+ed\b', sent.lower()):
                passive_count += 1

        passive_ratio = passive_count / len(sentences) if sentences else 0
        if passive_ratio > 0.7:
            score -= 3
            self.issues['calidad'].append(f"Excessive passive voice ({passive_ratio:.0%} of sentences)")
        elif passive_ratio > 0.5:
            score -= 2
            self.issues['calidad'].append(f"Much passive voice ({passive_ratio:.0%} of sentences)")
        elif passive_ratio > 0.3:
            score -= 1
            self.issues['calidad'].append(f"Some passive voice ({passive_ratio:.0%} of sentences)")

        # Filler word check
        filler_words = [
            'very', 'really', 'quite', 'rather', 'just', 'basically',
            'essentially', 'fairly', 'pretty', 'somewhat'
        ]
        filler_count = 0
        for filler in filler_words:
            filler_count += len(re.findall(r'\b' + filler + r'\b', self.content.lower()))

        if filler_count >= 10:
            score -= 2
            self.issues['calidad'].append(f"High filler word count ({filler_count})")
        elif filler_count >= 5:
            score -= 1
            self.issues['calidad'].append(f"Some filler words ({filler_count})")

        # Grammar/typo estimation (basic check)
        # Check for common patterns
        if re.search(r'\s{2,}', self.content):
            score -= 1
            self.issues['calidad'].append("Multiple consecutive spaces (formatting issue)")

        self._score('calidad', max(2, score))

    # ========================
    # CRITERION 4: Densidad
    # ========================

    def check_densidad(self):
        """Check information density: word count vs section count, duplicates."""
        score = 10
        lines = self._get_lines()
        _, section_count = self._has_heading_hierarchy()
        words = self._get_words()
        sentences = self._get_sentences()

        # Word-to-section ratio
        if section_count > 0:
            words_per_section = len(words) / section_count
            if words_per_section < 30:
                score -= 2
                self.issues['densidad'].append("Very low word density per section")
            elif words_per_section > 400:
                score -= 1
                self.issues['densidad'].append("Very long sections; could be split")

        # Duplicate/redundant sentence check
        sentence_starts = [s.split()[:3] if s.split() else [] for s in sentences]
        duplicate_count = 0
        for i in range(len(sentence_starts) - 1):
            if sentence_starts[i] == sentence_starts[i + 1]:
                duplicate_count += 1

        if duplicate_count >= 3:
            score -= 2
            self.issues['densidad'].append(f"Significant duplication ({duplicate_count} similar sentences)")
        elif duplicate_count >= 1:
            score -= 1
            self.issues['densidad'].append(f"Some duplication ({duplicate_count} similar sentences)")

        self._score('densidad', max(2, score))

    # ========================
    # CRITERION 5: Simplicidad
    # ========================

    def check_simplicidad(self):
        """Check accessibility: heading depth, jargon, domain knowledge required."""
        score = 10
        max_depth, _ = self._has_heading_hierarchy()

        # Heading depth
        if max_depth > 5:
            score -= 3
            self.issues['simplicidad'].append(f"Very deep hierarchy ({max_depth} levels)")
        elif max_depth > 4:
            score -= 2
            self.issues['simplicidad'].append(f"Deep hierarchy ({max_depth} levels)")
        elif max_depth > 3:
            score -= 1
            self.issues['simplicidad'].append(f"Hierarchy depth is {max_depth} levels")

        # Jargon density (rough estimate: CamelCase, SCREAMING_SNAKE, or technical terms)
        jargon_patterns = [
            r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',  # CamelCase
            r'\b[A-Z_]{3,}\b',  # SCREAMING_CASE
        ]
        jargon_count = 0
        for pattern in jargon_patterns:
            jargon_count += len(re.findall(pattern, self.content))

        words = self._get_words()
        total_words = len(words)
        if total_words > 0 and jargon_count / total_words > 0.1:
            score -= 2
            self.issues['simplicidad'].append("High jargon/technical term density")

        self._score('simplicidad', max(2, score))

    # ========================
    # CRITERION 6: Claridad
    # ========================

    def check_claridad(self):
        """Check clarity: vague qualifiers, ambiguous pronouns."""
        score = 10

        # Vague qualifier check
        vague_qualifiers = [
            'appropriate', 'reasonable', 'significant', 'sometimes', 'often',
            'usually', 'typically', 'roughly', 'somewhat', 'perhaps',
            'probably', 'maybe', 'possibly', 'fairly', 'relatively'
        ]
        vague_count = 0
        for qualifier in vague_qualifiers:
            pattern = r'\b' + qualifier + r'\b'
            vague_count += len(re.findall(pattern, self.content.lower()))

        if vague_count >= 15:
            score -= 3
            self.issues['claridad'].append(f"Many vague qualifiers ({vague_count})")
        elif vague_count >= 8:
            score -= 2
            self.issues['claridad'].append(f"Several vague qualifiers ({vague_count})")
        elif vague_count >= 4:
            score -= 1
            self.issues['claridad'].append(f"Some vague qualifiers ({vague_count})")

        # Ambiguous pronoun check (rough estimate)
        pronouns = re.findall(r'\b(it|they|them|this|that|which)\b', self.content.lower())
        if len(pronouns) > len(self._get_sentences()) * 0.5:
            score -= 1
            self.issues['claridad'].append("High pronoun usage; possible ambiguity")

        self._score('claridad', max(2, score))

    # ========================
    # CRITERION 7: Precisión
    # ========================

    def check_precision(self):
        """Check precision: aspirational vs testable claims, units, specificity."""
        score = 10

        # Aspirational language patterns
        aspirational = [
            r'\b(be\s+\w+|make\s+\w+|improve\s+\w+|optimize|enhance)\b',
            r'\b(good|better|best|excellent|great|nice|clean|simple)\b',
            r'\b(be\s+concise|write\s+clearly|perform\s+well)\b'
        ]

        aspirational_count = 0
        for pattern in aspirational:
            aspirational_count += len(re.findall(pattern, self.content.lower()))

        if aspirational_count >= 10:
            score -= 3
            self.issues['precision'].append(f"High aspirational language ({aspirational_count} instances)")
        elif aspirational_count >= 5:
            score -= 2
            self.issues['precision'].append(f"Several aspirational statements ({aspirational_count})")
        elif aspirational_count >= 2:
            score -= 1
            self.issues['precision'].append(f"Some aspirational language ({aspirational_count})")

        # Check for units in numeric claims
        numbers = re.findall(r'\d+(?:\.\d+)?', self.content)
        has_units = bool(re.search(r'\d+\s*(?:seconds?|ms|bytes?|words?|%|items?|times?)', self.content.lower()))

        if len(numbers) > 3 and not has_units:
            score -= 1
            self.issues['precision'].append("Numeric claims lack units/context")

        self._score('precision', max(2, score))

    # ========================
    # CRITERION 8: Profundidad
    # ========================

    def check_profundidad(self):
        """Check depth: edge cases, error handling, failure modes."""
        score = 10

        # Check for edge case/error handling language
        edge_case_keywords = [
            'edge case', 'corner case', 'error', 'fail', 'exception',
            'unexpected', 'missing', 'conflict', 'contradict',
            'fallback', 'recovery', 'timeout', 'overflow'
        ]

        edge_case_count = 0
        for keyword in edge_case_keywords:
            pattern = r'\b' + keyword + r'\b'
            edge_case_count += len(re.findall(pattern, self.content.lower()))

        if edge_case_count == 0:
            score -= 3
            self.issues['profundidad'].append("No edge case or error handling mentioned")
        elif edge_case_count < 3:
            score -= 2
            self.issues['profundidad'].append("Limited edge case coverage")
        elif edge_case_count < 5:
            score -= 1
            self.issues['profundidad'].append("Moderate edge case coverage")

        # Check for "what if" / conditional language
        has_conditionals = bool(re.search(r'\b(if|when|unless|except|while|given|assuming)\b', self.content.lower()))
        if not has_conditionals and score > 5:
            score -= 1
            self.issues['profundidad'].append("Limited conditional/scenario planning")

        self._score('profundidad', max(2, score))

    # ========================
    # CRITERION 9: Coherencia
    # ========================

    def check_coherencia(self):
        """Check coherence: cross-references, contradictions, terminology consistency."""
        score = 10

        # Check for cross-references
        has_references = bool(re.search(r'(section|chapter|see|refer|above|below)', self.content.lower()))
        if not has_references:
            score -= 1
            self.issues['coherencia'].append("No cross-references between sections")

        # Check for contradictory language patterns
        contradictions = [
            (r'\balways\b', r'\bnever\b'),
            (r'\brequired\b', r'\boptional\b'),
            (r'\bmust\b', r'\bshould not\b'),
        ]

        for pattern1, pattern2 in contradictions:
            has_p1 = bool(re.search(pattern1, self.content.lower()))
            has_p2 = bool(re.search(pattern2, self.content.lower()))
            if has_p1 and has_p2:
                score -= 1
                self.issues['coherencia'].append("Potentially contradictory claims found")
                break

        # Terminology consistency check (rough)
        sentences = self._get_sentences()
        if len(sentences) > 5:
            # Sample: check if key terms repeat consistently
            words = self._get_words()
            if len(set(words)) / len(words) > 0.9:
                score -= 1
                self.issues['coherencia'].append("High unique word ratio; terminology may be inconsistent")

        self._score('coherencia', max(2, score))

    # ========================
    # CRITERION 10: Valor
    # ========================

    def check_valor(self):
        """Check value: domain expertise, methodology, actionability."""
        score = 10

        # Check for methodology/reasoning language
        methodology_keywords = [
            'methodology', 'approach', 'framework', 'principle', 'strategy',
            'reason', 'because', 'thus', 'therefore', 'conclude',
            'insight', 'expert', 'best practice', 'pattern'
        ]

        methodology_count = 0
        for keyword in methodology_keywords:
            pattern = r'\b' + keyword + r'\b'
            methodology_count += len(re.findall(pattern, self.content.lower()))

        if methodology_count == 0:
            score -= 3
            self.issues['valor'].append("No methodology or reasoning provided")
        elif methodology_count < 3:
            score -= 2
            self.issues['valor'].append("Limited methodology/reasoning")
        elif methodology_count < 6:
            score -= 1
            self.issues['valor'].append("Moderate methodology content")

        # Check for actionability
        action_keywords = ['action', 'step', 'implement', 'execute', 'do', 'apply', 'next']
        action_count = sum(
            len(re.findall(r'\b' + kw + r'\b', self.content.lower()))
            for kw in action_keywords
        )

        if action_count == 0:
            score -= 1
            self.issues['valor'].append("Not actionable; lacks clear next steps")

        self._score('valor', max(2, score))

    # ========================
    # OUTPUT FORMATTING
    # ========================

    def get_average_score(self) -> float:
        """Calculate average score across all criteria."""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

    def format_scorecard(self) -> str:
        """Format scores as a visual scorecard with bars."""
        if not self.scores:
            return "No scores to display."

        lines = [
            "\n" + "=" * 60,
            f"RUBRIC EVALUATION: {self.filepath.name}",
            "=" * 60 + "\n",
        ]

        for criterion in self.CRITERIA:
            score = self.scores.get(criterion, 0)
            name = self.CRITERION_NAMES[criterion]

            # Create bar visualization
            filled = "█" * score
            empty = "░" * (10 - score)
            bar = f"{filled}{empty}"

            lines.append(f"{criterion:12s} {name:25s} {score:2d}/10 {bar}")

        avg = self.get_average_score()
        lines.extend([
            "",
            "-" * 60,
            f"AVERAGE: {avg:.1f}/10",
            "-" * 60,
        ])

        # Show threshold
        threshold = 10  # --strict mode threshold (set in main)
        if avg >= threshold:
            lines.append(f"✓ PASSED (>= {threshold}/10)")
        else:
            lines.append(f"✗ NEEDS WORK (< {threshold}/10)")

        return "\n".join(lines)

    def format_json(self) -> str:
        """Format scores as JSON."""
        data = {
            'filename': str(self.filepath),
            'scores': self.scores,
            'average': round(self.get_average_score(), 2),
            'issues': self.issues,
        }
        return json.dumps(data, indent=2)

    def format_verbose(self) -> str:
        """Format scores with detailed issues."""
        lines = [self.format_scorecard(), "\nDETAILED ISSUES:\n"]

        for criterion in self.CRITERIA:
            issues = self.issues.get(criterion, [])
            if issues:
                name = self.CRITERION_NAMES[criterion]
                lines.append(f"\n{name}:")
                for issue in issues:
                    lines.append(f"  - {issue}")

        return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Evaluate content against 10-criterion excellence rubric.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('filepath', help='Path to content file')
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict threshold: 10/10 required (default: 8/10)',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format',
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed issues per criterion',
    )

    args = parser.parse_args()

    try:
        evaluator = RubricEvaluator(args.filepath)
        evaluator.evaluate()

        if args.json:
            print(evaluator.format_json())
        elif args.verbose:
            print(evaluator.format_verbose())
        else:
            print(evaluator.format_scorecard())

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
