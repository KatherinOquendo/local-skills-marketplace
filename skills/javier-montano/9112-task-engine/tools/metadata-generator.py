#!/usr/bin/env python3
"""
Metadata Generator: Create standardized reasoning metadata blocks for responses.

Usage:
  python metadata-generator.py --input results.json
  python metadata-generator.py --input results.json --markdown
  python metadata-generator.py --input results.json --json
"""

import argparse
import json
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ReasoningMetadata:
    """Structured reasoning metadata for a response."""
    global_confidence: float
    sub_problem_confidences: Dict[str, float]
    sources: List[str]
    weaknesses: List[str]
    rigidity_level: str
    verification_status: str
    notes: str


class MetadataGenerator:
    """Generates standardized reasoning metadata."""

    RIGIDITY_LEVELS = {
        0.95: "executive",
        0.85: "analytical",
        0.70: "exploratory",
    }

    def __init__(self):
        self.results = None

    def load_results(self, filepath: str) -> None:
        """Load results from JSON file."""
        with open(filepath, 'r') as f:
            self.results = json.load(f)

    def generate_metadata(self) -> ReasoningMetadata:
        """Generate metadata from results."""
        # Extract global confidence
        global_conf = self._extract_global_confidence()

        # Extract sub-problem confidences
        sub_confs = self._extract_sub_confidences()

        # Identify sources
        sources = self._identify_sources()

        # Identify weaknesses
        weaknesses = self._identify_weaknesses()

        # Determine rigidity level
        rigidity = self._determine_rigidity_level(global_conf)

        # Determine verification status
        verification = self._determine_verification_status()

        # Generate notes
        notes = self._generate_notes(global_conf)

        return ReasoningMetadata(
            global_confidence=global_conf,
            sub_problem_confidences=sub_confs,
            sources=sources,
            weaknesses=weaknesses,
            rigidity_level=rigidity,
            verification_status=verification,
            notes=notes,
        )

    def _extract_global_confidence(self) -> float:
        """Extract global confidence from results."""
        if isinstance(self.results, dict):
            if "global_confidence" in self.results:
                return self.results["global_confidence"]
            if "confidence" in self.results:
                return self.results["confidence"]

        # Default to 0.75 if not found
        return 0.75

    def _extract_sub_confidences(self) -> Dict[str, float]:
        """Extract per-sub-problem confidence scores."""
        sub_confs = {}

        if isinstance(self.results, dict):
            # Check for sub_problems array
            if "sub_problems" in self.results:
                for sp in self.results["sub_problems"]:
                    sp_id = sp.get("id") or sp.get("sub_problem_id") or "unknown"
                    conf = sp.get("confidence") or 0.5
                    sub_confs[sp_id] = conf

            # Check for analysis results
            if "analyses" in self.results:
                for analysis in self.results["analyses"]:
                    sp_id = analysis.get("sub_problem_id") or "unknown"
                    conf = analysis.get("recommended_confidence") or analysis.get("confidence") or 0.5
                    sub_confs[sp_id] = conf

        return sub_confs

    def _identify_sources(self) -> List[str]:
        """Identify sources used in analysis."""
        sources = []

        if isinstance(self.results, dict):
            if "sources" in self.results:
                sources = self.results["sources"]
                if isinstance(sources, str):
                    sources = [sources]

            # Check for source information in results
            if "thread_messages" in self.results:
                count = self.results["thread_messages"]
                sources.append(f"Thread context ({count} messages)")

            if "attachments" in self.results:
                attachments = self.results["attachments"]
                if isinstance(attachments, list):
                    sources.append(f"Attachments: {', '.join(attachments)}")
                elif isinstance(attachments, int):
                    sources.append(f"Attachments ({attachments} files)")

        if not sources:
            sources = ["Internal knowledge", "Reasoning and inference"]

        return sources

    def _identify_weaknesses(self) -> List[str]:
        """Identify weaknesses or gaps in the analysis."""
        weaknesses = []

        if isinstance(self.results, dict):
            # Check for explicit weakness information
            if "weaknesses" in self.results:
                ws = self.results["weaknesses"]
                if isinstance(ws, list):
                    weaknesses = ws
                elif isinstance(ws, str):
                    weaknesses = [ws]

            # Check for information gaps
            if "information_gaps" in self.results:
                gaps = self.results["information_gaps"]
                if isinstance(gaps, list):
                    weaknesses.extend([f"Missing: {g}" for g in gaps])

            # Check for assumptions
            if "assumptions" in self.results:
                assumptions = self.results["assumptions"]
                if isinstance(assumptions, list):
                    weaknesses.extend([f"Assumes: {a}" for a in assumptions])

            # Check for low-confidence sub-problems
            sub_confs = self._extract_sub_confidences()
            low_conf = [
                f"{sp_id} is low-confidence ({conf:.2f})"
                for sp_id, conf in sub_confs.items()
                if conf < 0.75
            ]
            if low_conf:
                weaknesses.append("Low-confidence sub-problems: " + ", ".join(low_conf))

        return weaknesses

    def _determine_rigidity_level(self, confidence: float) -> str:
        """Determine rigidity level based on confidence."""
        if confidence >= 0.90:
            return "executive"
        elif confidence >= 0.80:
            return "analytical"
        else:
            return "exploratory"

    def _determine_verification_status(self) -> str:
        """Determine verification status."""
        if isinstance(self.results, dict):
            if "verification_status" in self.results:
                return self.results["verification_status"]

            # Check for verification flags
            if "verification_flags" in self.results:
                flags = self.results["verification_flags"]
                if not flags:
                    return "All checks passed"
                else:
                    return f"{len(flags)} flags raised"

        return "Verification complete"

    def _generate_notes(self, confidence: float) -> str:
        """Generate explanatory notes."""
        if confidence >= 0.95:
            return "High confidence. Ready for critical decisions."
        elif confidence >= 0.85:
            return "Solid confidence with reasonable assumptions. Suitable for most decisions."
        elif confidence >= 0.70:
            return "Moderate confidence. Gaps remain; recommend validation before critical decisions."
        else:
            return "Low confidence. Exploratory only. Significant gaps; require additional research."

    def to_markdown(self) -> str:
        """Format metadata as markdown."""
        metadata = self.generate_metadata()

        lines = []
        lines.append("---")
        lines.append("📊 REASONING METADATA")
        lines.append("---")

        # Global confidence
        lines.append(f"**Global Confidence:** {metadata.global_confidence:.2f}")

        # Sub-problem confidence
        if metadata.sub_problem_confidences:
            lines.append("\n**Sub-Problem Breakdown:**")
            for sp_id, conf in sorted(metadata.sub_problem_confidences.items()):
                lines.append(f"- {sp_id}: {conf:.2f}")

        # Rigidity level
        lines.append(f"\n**Rigidity Level:** {metadata.rigidity_level.title()}")

        # Sources
        if metadata.sources:
            lines.append("\n**Sources Consulted:**")
            for source in metadata.sources:
                lines.append(f"- {source}")

        # Weaknesses
        if metadata.weaknesses:
            lines.append("\n**Identified Weaknesses:**")
            for weakness in metadata.weaknesses:
                lines.append(f"- {weakness}")

        # Verification
        lines.append(f"\n**Verification Status:** {metadata.verification_status}")

        # Notes
        lines.append(f"\n**Notes:** {metadata.notes}")

        lines.append("\n---")

        return "\n".join(lines)

    def to_compact_markdown(self) -> str:
        """Format metadata as compact markdown."""
        metadata = self.generate_metadata()

        lines = []
        lines.append("---")
        lines.append("📊 REASONING METADATA:")
        lines.append(f"• Global confidence: {metadata.global_confidence:.2f}")

        if metadata.sub_problem_confidences:
            conf_str = ", ".join([
                f"{sp_id}: {conf:.2f}"
                for sp_id, conf in sorted(metadata.sub_problem_confidences.items())
            ])
            lines.append(f"• Sub-problem confidence: {conf_str}")

        if metadata.sources:
            sources_str = ", ".join(metadata.sources)
            lines.append(f"• Sources consulted: {sources_str}")

        if metadata.weaknesses:
            weaknesses_str = ", ".join(metadata.weaknesses)
            lines.append(f"• Weaknesses identified: {weaknesses_str}")

        lines.append(f"• Rigidity level: {metadata.rigidity_level}")
        lines.append(f"• Verification status: {metadata.verification_status}")

        lines.append("---")

        return "\n".join(lines)

    def to_json(self) -> Dict[str, Any]:
        """Format metadata as JSON."""
        metadata = self.generate_metadata()

        return {
            "global_confidence": metadata.global_confidence,
            "sub_problem_confidences": metadata.sub_problem_confidences,
            "sources": metadata.sources,
            "weaknesses": metadata.weaknesses,
            "rigidity_level": metadata.rigidity_level,
            "verification_status": metadata.verification_status,
            "notes": metadata.notes,
        }

    def to_text(self) -> str:
        """Format metadata as plain text."""
        metadata = self.generate_metadata()

        lines = []
        lines.append("REASONING METADATA")
        lines.append("=" * 50)

        lines.append(f"\nGlobal Confidence: {metadata.global_confidence:.2f}")
        lines.append(f"Rigidity Level: {metadata.rigidity_level.title()}")

        if metadata.sub_problem_confidences:
            lines.append("\nSub-Problem Breakdown:")
            for sp_id, conf in sorted(metadata.sub_problem_confidences.items()):
                lines.append(f"  {sp_id}: {conf:.2f}")

        if metadata.sources:
            lines.append("\nSources Consulted:")
            for source in metadata.sources:
                lines.append(f"  - {source}")

        if metadata.weaknesses:
            lines.append("\nIdentified Weaknesses:")
            for weakness in metadata.weaknesses:
                lines.append(f"  - {weakness}")

        lines.append(f"\nVerification Status: {metadata.verification_status}")
        lines.append(f"\nNotes: {metadata.notes}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate standardized reasoning metadata"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON file with results",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Output as markdown (default if no format specified)",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Use compact markdown format",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Output as plain text",
    )

    args = parser.parse_args()

    generator = MetadataGenerator()
    generator.load_results(args.input)

    # Default to markdown if no format specified
    if not (args.markdown or args.json or args.text):
        args.markdown = True

    if args.json:
        output = generator.to_json()
        print(json.dumps(output, indent=2))
    elif args.compact:
        print(generator.to_compact_markdown())
    elif args.text:
        print(generator.to_text())
    else:
        print(generator.to_markdown())


if __name__ == "__main__":
    main()
