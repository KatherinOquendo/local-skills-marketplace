#!/usr/bin/env python3
"""
Task Decomposer: Break complex problems into atomic sub-problems with dependency mapping.

Usage:
  python task-decomposer.py "Your complex problem here"
  python task-decomposer.py "Your problem" --max-depth 4
  python task-decomposer.py "Your problem" --json
"""

import argparse
import json
import re
from typing import List, Dict, Set
from dataclasses import dataclass, asdict


@dataclass
class SubProblem:
    """Represents a single sub-problem in decomposition."""
    id: str
    description: str
    domain: str
    dependencies: List[str]
    priority: int
    indicators: List[str]


class TaskDecomposer:
    """Decomposes complex problems into atomic sub-problems."""

    # Domain keywords for classification
    DOMAIN_KEYWORDS = {
        "technical": ["code", "system", "architecture", "database", "api", "algorithm", "implementation", "framework", "library", "performance", "optimization", "infrastructure"],
        "business": ["revenue", "market", "strategy", "competition", "roe", "roi", "profit", "cost", "pricing", "customer", "business", "growth", "sales"],
        "creative": ["design", "ui", "ux", "brand", "messaging", "positioning", "user experience", "visual", "layout", "copy"],
        "factual": ["data", "research", "verify", "fact", "evidence", "metric", "measurement", "analysis", "history"],
        "analytical": ["logic", "reasoning", "inference", "evaluate", "assess", "compare", "trade-off", "pros", "cons", "decision"],
        "human": ["team", "culture", "motivation", "psychology", "relationship", "communication", "leadership", "collaboration", "behavior"],
    }

    # Dependency keywords
    DEPENDENCY_KEYWORDS = {
        "conditional": ["if", "only if", "depends on", "requires", "assumes"],
        "sequential": ["before", "after", "first", "then", "subsequently", "once"],
        "causal": ["because", "caused", "result in", "leads to", "due to"],
        "contingent": ["unless", "otherwise", "except", "provided that"],
    }

    def __init__(self):
        self.sub_problems: List[SubProblem] = []
        self.dependency_graph: Dict[str, Set[str]] = {}

    def decompose(self, problem: str, max_depth: int = 3) -> List[SubProblem]:
        """Decompose a problem into sub-problems."""
        # Step 1: Identify core question
        core = self._extract_core_question(problem)

        # Step 2: Split by conjunctions and indicators
        candidates = self._extract_sub_questions(problem)

        # Step 3: Analyze each candidate
        sub_problems = []
        for idx, candidate in enumerate(candidates[:max_depth], 1):
            sp = self._analyze_sub_problem(candidate, f"SP-{idx}")
            sub_problems.append(sp)
            self.sub_problems.append(sp)

        # Step 4: Map dependencies
        self._map_dependencies(sub_problems)

        # Step 5: Assign priorities based on dependencies
        self._assign_priorities(sub_problems)

        return sub_problems

    def _extract_core_question(self, problem: str) -> str:
        """Extract the core question by removing context and details."""
        # Remove parenthetical asides
        cleaned = re.sub(r'\([^)]*\)', '', problem)
        # Remove excessive qualifiers
        cleaned = re.sub(r'(by the way|also|additionally|furthermore)', '', cleaned, flags=re.IGNORECASE)
        # Extract first sentence or clause
        sentences = cleaned.split('.')
        if sentences:
            return sentences[0].strip()
        return problem.strip()

    def _extract_sub_questions(self, problem: str) -> List[str]:
        """Extract potential sub-questions from the problem."""
        sub_qs = []

        # Split by "and" (indicates parallel sub-problems)
        and_splits = re.split(r'\s+and\s+', problem, flags=re.IGNORECASE)
        for part in and_splits:
            # Split by "or" (indicates alternatives/options)
            or_splits = re.split(r'\s+or\s+', part, flags=re.IGNORECASE)
            sub_qs.extend(or_splits)

        # Extract parenthetical questions
        parens = re.findall(r'\(([^)]*\?[^)]*)\)', problem)
        sub_qs.extend(parens)

        # Extract embedded questions (questions within the narrative)
        embedded = re.findall(r'([^.?]*\?)', problem)
        sub_qs.extend(embedded)

        # Clean up and deduplicate
        cleaned = []
        seen = set()
        for sq in sub_qs:
            sq = sq.strip()
            if sq and sq not in seen and len(sq) > 5:
                cleaned.append(sq)
                seen.add(sq)

        # If no sub-questions found, return the original as a single problem
        if not cleaned:
            cleaned = [problem]

        return cleaned

    def _analyze_sub_problem(self, description: str, sp_id: str) -> SubProblem:
        """Analyze a sub-problem and classify it."""
        # Determine domain
        domain = self._detect_domain(description)

        # Extract indicators (words that signal this problem type)
        indicators = self._extract_indicators(description)

        return SubProblem(
            id=sp_id,
            description=description.strip(),
            domain=domain,
            dependencies=[],
            priority=0,
            indicators=indicators,
        )

    def _detect_domain(self, text: str) -> str:
        """Detect the domain of a sub-problem using keyword analysis."""
        text_lower = text.lower()
        scores = {domain: 0 for domain in self.DOMAIN_KEYWORDS}

        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[domain] += 1

        # Return the domain with the highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return "analytical"  # Default domain

    def _extract_indicators(self, text: str) -> List[str]:
        """Extract words that indicate problem type."""
        words = text.split()
        # Take significant words (longer than 4 chars, not common)
        common = {"this", "that", "what", "when", "where", "which", "should", "would", "could"}
        indicators = [w for w in words if len(w) > 4 and w.lower() not in common]
        return indicators[:5]  # Top 5 indicators

    def _map_dependencies(self, sub_problems: List[SubProblem]) -> None:
        """Identify dependencies between sub-problems."""
        problem_texts = {sp.id: sp.description for sp in sub_problems}

        for sp in sub_problems:
            deps = set()
            sp_text = sp.description.lower()

            # Check for dependency keywords
            for other_sp in sub_problems:
                if other_sp.id == sp.id:
                    continue

                other_keywords = other_sp.description.lower().split()
                # Simple heuristic: if current problem mentions keywords from other, there's a dependency
                if any(keyword in sp_text for keyword in other_keywords if len(keyword) > 4):
                    deps.add(other_sp.id)

            sp.dependencies = list(deps)
            self.dependency_graph[sp.id] = deps

    def _assign_priorities(self, sub_problems: List[SubProblem]) -> None:
        """Assign priorities based on dependency chains."""
        # Priority 1: No dependencies (foundation)
        # Priority 2: Depends on priority 1
        # Priority 3: Depends on priority 2

        priority_levels = {}

        for sp in sub_problems:
            if not sp.dependencies:
                priority_levels[sp.id] = 1
            else:
                # Max priority of dependencies + 1
                max_dep_priority = max(
                    (priority_levels.get(dep, 1) for dep in sp.dependencies),
                    default=0
                )
                priority_levels[sp.id] = max_dep_priority + 1

        for sp in sub_problems:
            sp.priority = priority_levels.get(sp.id, 1)

    def to_dict(self) -> Dict:
        """Convert decomposition to dictionary."""
        return {
            "sub_problems": [asdict(sp) for sp in self.sub_problems],
            "dependency_graph": {k: list(v) for k, v in self.dependency_graph.items()},
            "solve_order": self._get_solve_order(),
        }

    def _get_solve_order(self) -> List[str]:
        """Get recommended solve order based on priorities and dependencies."""
        by_priority = {}
        for sp in self.sub_problems:
            if sp.priority not in by_priority:
                by_priority[sp.priority] = []
            by_priority[sp.priority].append(sp.id)

        # Sort by priority, maintaining order within each priority
        order = []
        for priority in sorted(by_priority.keys()):
            order.extend(by_priority[priority])

        return order

    def to_text(self) -> str:
        """Convert decomposition to human-readable text format."""
        lines = []
        lines.append("DECOMPOSITION ANALYSIS\n")
        lines.append(f"Sub-problems identified: {len(self.sub_problems)}\n")

        # Group by priority
        by_priority = {}
        for sp in self.sub_problems:
            if sp.priority not in by_priority:
                by_priority[sp.priority] = []
            by_priority[sp.priority].append(sp)

        for priority in sorted(by_priority.keys()):
            lines.append(f"\nPriority {priority} (foundational):" if priority == 1 else f"\nPriority {priority}:")
            for sp in by_priority[priority]:
                dep_str = ", ".join(sp.dependencies) if sp.dependencies else "none"
                lines.append(f"  {sp.id}: {sp.description}")
                lines.append(f"    Domain: {sp.domain}")
                lines.append(f"    Dependencies: {dep_str}")

        lines.append("\n\nRecommended solve order:")
        solve_order = self._get_solve_order()
        lines.append(" → ".join(solve_order))

        lines.append("\n\nDependency Summary:")
        for sp in self.sub_problems:
            if sp.dependencies:
                lines.append(f"  {sp.id} requires: {', '.join(sp.dependencies)}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Decompose a complex problem into atomic sub-problems"
    )
    parser.add_argument("problem", help="The problem to decompose")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum decomposition depth (default: 3)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON (default: human-readable text)",
    )

    args = parser.parse_args()

    decomposer = TaskDecomposer()
    sub_problems = decomposer.decompose(args.problem, args.max_depth)

    if args.json:
        output = decomposer.to_dict()
        print(json.dumps(output, indent=2))
    else:
        print(decomposer.to_text())


if __name__ == "__main__":
    main()
