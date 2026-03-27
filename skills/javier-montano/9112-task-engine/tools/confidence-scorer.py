#!/usr/bin/env python3
"""
Confidence Scorer: Analyze and calibrate confidence levels across sub-answers.

Usage:
  python confidence-scorer.py --answers answers.json
  python confidence-scorer.py --answers answers.json --target 0.95
  python confidence-scorer.py --answers answers.json --json
"""

import argparse
import json
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ConfidenceAnalysis:
    """Analysis of confidence for a single answer."""
    sub_problem_id: str
    answer_text: str
    stated_confidence: float
    evidence_density: float
    hedging_count: int
    specificity_score: float
    recommended_confidence: float
    reasoning: str
    flags: List[str]


class ConfidenceScorer:
    """Analyzes and scores confidence levels."""

    # Hedging phrases that indicate uncertainty
    HEDGING_PHRASES = [
        "might", "may", "could", "possibly", "probably", "likely",
        "seems", "appears", "suggests", "seems to", "perhaps",
        "somewhat", "fairly", "relatively", "comparatively",
        "in some cases", "sort of", "kind of", "a bit",
        "not entirely", "arguably", "potentially"
    ]

    # Strong evidence indicators
    EVIDENCE_KEYWORDS = [
        "verified", "confirmed", "proven", "tested", "data shows",
        "research indicates", "study found", "experiment proved",
        "evidence supports", "demonstrated", "established",
        "measured", "calculated", "documented", "published",
        "benchmark", "track record", "empirical", "statistical"
    ]

    # Assumption indicators
    ASSUMPTION_KEYWORDS = [
        "assume", "assuming", "if", "suppose", "assuming that",
        "depends on", "contingent on", "provided that"
    ]

    def __init__(self, target_confidence: float = 0.95):
        self.target_confidence = target_confidence
        self.analyses: List[ConfidenceAnalysis] = []

    def analyze_answer(self, sub_problem_id: str, answer_text: str, stated_confidence: float) -> ConfidenceAnalysis:
        """Analyze a single answer for confidence calibration."""
        evidence_density = self._score_evidence_density(answer_text)
        hedging_count = self._count_hedging_phrases(answer_text)
        specificity = self._score_specificity(answer_text)

        # Compute recommended confidence
        recommended = self._compute_recommended_confidence(
            evidence_density, hedging_count, specificity, stated_confidence
        )

        # Identify flags
        flags = self._identify_flags(
            stated_confidence, recommended, hedging_count, evidence_density
        )

        reasoning = self._generate_reasoning(
            stated_confidence, recommended, evidence_density, hedging_count, specificity
        )

        analysis = ConfidenceAnalysis(
            sub_problem_id=sub_problem_id,
            answer_text=answer_text,
            stated_confidence=stated_confidence,
            evidence_density=evidence_density,
            hedging_count=hedging_count,
            specificity_score=specificity,
            recommended_confidence=recommended,
            reasoning=reasoning,
            flags=flags,
        )

        self.analyses.append(analysis)
        return analysis

    def _score_evidence_density(self, text: str) -> float:
        """Score evidence density: ratio of evidence keywords to total words."""
        words = text.lower().split()
        total_words = len(words)

        evidence_count = 0
        for keyword in self.EVIDENCE_KEYWORDS:
            evidence_count += text.lower().count(keyword)

        if total_words == 0:
            return 0.0

        # Normalize: expect 1-2 evidence indicators per 50 words
        expected = (total_words / 50) * 1.5
        actual = min(evidence_count, expected * 2)  # Cap at 2x expected
        density = min(actual / expected, 1.0) if expected > 0 else 0.0

        return round(density, 2)

    def _count_hedging_phrases(self, text: str) -> int:
        """Count hedging phrases in the text."""
        text_lower = text.lower()
        count = 0

        for phrase in self.HEDGING_PHRASES:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(phrase) + r'\b'
            count += len(re.findall(pattern, text_lower))

        return count

    def _score_specificity(self, text: str) -> float:
        """Score specificity: presence of specific numbers, percentages, dates."""
        words = text.split()

        # Count specific indicators
        specificity_markers = 0

        # Numbers and percentages
        numbers = len(re.findall(r'\d+\.?\d*', text))
        specificity_markers += min(numbers, 5)  # Cap at 5

        # Dates
        dates = len(re.findall(r'\d{4}|\d{1,2}/\d{1,2}', text))
        specificity_markers += min(dates, 3)  # Cap at 3

        # Concrete nouns (rough heuristic)
        total_words = len(words)

        # Normalize: expect 2-3 specific markers per 100 words
        expected = (total_words / 100) * 2.5
        actual = min(specificity_markers, expected * 2)  # Cap at 2x expected
        specificity = min(actual / (expected if expected > 0 else 1.0), 1.0)

        return round(specificity, 2)

    def _compute_recommended_confidence(
        self, evidence_density: float, hedging_count: int, specificity: float, stated: float
    ) -> float:
        """Compute recommended confidence based on factors."""
        # Base recommendation off stated, but adjust based on evidence

        # High evidence density → can support stated confidence
        # Low evidence density → should reduce confidence
        evidence_adjustment = (evidence_density - 0.5) * 0.1  # Range: -0.05 to +0.05

        # Hedging phrases → reduce confidence
        # Expected: 0-2 hedges per answer; more = problem
        hedging_adjustment = -0.02 * min(hedging_count, 3)  # -0.06 max

        # High specificity → supports confidence
        # Low specificity → suggests vagueness
        specificity_adjustment = (specificity - 0.5) * 0.05  # Range: -0.025 to +0.025

        # Compute adjusted confidence
        recommended = stated + evidence_adjustment + hedging_adjustment + specificity_adjustment

        # Bound to [0.0, 1.0]
        recommended = max(0.0, min(1.0, recommended))

        return round(recommended, 2)

    def _identify_flags(
        self, stated: float, recommended: float, hedging_count: int, evidence_density: float
    ) -> List[str]:
        """Identify potential issues with the confidence score."""
        flags = []

        # Over-confidence: stated >> recommended
        if stated > recommended + 0.15:
            flags.append(f"Over-confidence: stated {stated} >> recommended {recommended}")

        # Under-confidence: recommended >> stated
        if recommended > stated + 0.15:
            flags.append(f"Under-confidence: recommended {recommended} >> stated {stated}")

        # Excessive hedging
        if hedging_count > 3:
            flags.append(f"Excessive hedging: {hedging_count} hedging phrases (suggests uncertainty)")

        # Low evidence
        if evidence_density < 0.3:
            flags.append(f"Low evidence density ({evidence_density:.0%}): thin justification")

        # High evidence but low stated confidence
        if evidence_density > 0.6 and stated < 0.70:
            flags.append(f"High evidence ({evidence_density:.0%}) but low stated confidence ({stated}): possible under-confidence")

        return flags

    def _generate_reasoning(
        self, stated: float, recommended: float, evidence_density: float, hedging_count: int, specificity: float
    ) -> str:
        """Generate reasoning for the recommended confidence."""
        parts = []

        # Evidence assessment
        if evidence_density > 0.6:
            parts.append(f"Strong evidence base ({evidence_density:.0%})")
        elif evidence_density > 0.4:
            parts.append(f"Moderate evidence ({evidence_density:.0%})")
        else:
            parts.append(f"Limited evidence ({evidence_density:.0%})")

        # Hedging assessment
        if hedging_count == 0:
            parts.append("no hedging language")
        elif hedging_count <= 2:
            parts.append(f"minimal hedging ({hedging_count} phrases)")
        else:
            parts.append(f"significant hedging ({hedging_count} phrases)")

        # Specificity assessment
        if specificity > 0.6:
            parts.append(f"highly specific ({specificity:.0%})")
        elif specificity > 0.3:
            parts.append(f"moderately specific ({specificity:.0%})")
        else:
            parts.append(f"vague ({specificity:.0%})")

        reasoning = "Based on: " + ", ".join(parts) + "."

        if stated != recommended:
            diff = recommended - stated
            if diff > 0:
                reasoning += f" Consider increasing confidence by {abs(diff):.2f} points."
            else:
                reasoning += f" Consider decreasing confidence by {abs(diff):.2f} points."

        return reasoning

    def load_answers(self, filepath: str) -> None:
        """Load answers from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Handle both array and object formats
        if isinstance(data, list):
            answers = data
        elif isinstance(data, dict) and "sub_problems" in data:
            answers = data["sub_problems"]
        else:
            answers = [data]

        for item in answers:
            sp_id = item.get("id") or item.get("sub_problem_id") or "unknown"
            answer = item.get("answer") or item.get("answer_text") or ""
            confidence = item.get("confidence") or 0.5

            self.analyze_answer(sp_id, answer, confidence)

    def get_global_confidence(self) -> float:
        """Compute weighted global confidence across all sub-problems."""
        if not self.analyses:
            return 0.0

        # Weight by importance (if available), else equal weight
        total_weight = 0
        weighted_sum = 0

        for analysis in self.analyses:
            weight = 1.0  # Default equal weight
            weighted_sum += analysis.recommended_confidence * weight
            total_weight += weight

        return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0

    def below_target(self) -> List[ConfidenceAnalysis]:
        """Return analyses below target confidence."""
        return [a for a in self.analyses if a.recommended_confidence < self.target_confidence]

    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            "analyses": [asdict(a) for a in self.analyses],
            "global_confidence": self.get_global_confidence(),
            "target_confidence": self.target_confidence,
            "below_target": [a.sub_problem_id for a in self.below_target()],
            "summary": {
                "total_sub_problems": len(self.analyses),
                "at_or_above_target": len([a for a in self.analyses if a.recommended_confidence >= self.target_confidence]),
                "below_target_count": len(self.below_target()),
            }
        }

    def to_text(self) -> str:
        """Convert to human-readable text format."""
        lines = []
        lines.append("CONFIDENCE SCORING ANALYSIS\n")
        lines.append(f"Target confidence: {self.target_confidence}\n")

        # Per-answer analysis
        lines.append("PER-ANSWER BREAKDOWN:")
        for analysis in self.analyses:
            lines.append(f"\n{analysis.sub_problem_id}:")
            lines.append(f"  Stated: {analysis.stated_confidence:.2f}")
            lines.append(f"  Recommended: {analysis.recommended_confidence:.2f}")
            lines.append(f"  Evidence density: {analysis.evidence_density:.0%}")
            lines.append(f"  Hedging phrases: {analysis.hedging_count}")
            lines.append(f"  Specificity: {analysis.specificity_score:.0%}")

            if analysis.flags:
                lines.append(f"  Flags:")
                for flag in analysis.flags:
                    lines.append(f"    - {flag}")
            else:
                lines.append("  ✓ No flags")

            lines.append(f"  Reasoning: {analysis.reasoning}")

        # Global summary
        lines.append("\n\nGLOBAL SUMMARY:")
        global_conf = self.get_global_confidence()
        lines.append(f"Global confidence: {global_conf:.2f}")

        below = self.below_target()
        if below:
            lines.append(f"\nBelow target ({self.target_confidence}):")
            for a in below:
                gap = self.target_confidence - a.recommended_confidence
                lines.append(f"  - {a.sub_problem_id}: {a.recommended_confidence:.2f} (need +{gap:.2f})")
                lines.append(f"    Suggestion: {a.reasoning}")
        else:
            lines.append(f"\n✓ All sub-problems at or above target")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Score and calibrate confidence levels across answers"
    )
    parser.add_argument(
        "--answers",
        required=True,
        help="Path to JSON file with answers",
    )
    parser.add_argument(
        "--target",
        type=float,
        default=0.95,
        help="Target confidence threshold (default: 0.95)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON (default: human-readable text)",
    )

    args = parser.parse_args()

    scorer = ConfidenceScorer(args.target)
    scorer.load_answers(args.answers)

    if args.json:
        output = scorer.to_dict()
        print(json.dumps(output, indent=2))
    else:
        print(scorer.to_text())


if __name__ == "__main__":
    main()
