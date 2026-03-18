#!/usr/bin/env python3
"""
Refinement Suggester: Generate specific improvement suggestions per criterion.

Usage:
    python refinement-suggester.py <file_path> [--criterion <name>] [--top N] [--json]

Examples:
    python refinement-suggester.py content.md --criterion clarity
    python refinement-suggester.py content.md --top 3
    python refinement-suggester.py content.md --json

Output:
    - Specific suggestions for improving low-scoring criteria
    - Before/after examples where applicable
    - Expected impact estimation
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Import the evaluator from same directory
import importlib.util
spec = importlib.util.spec_from_file_location(
    "rubric_evaluator",
    Path(__file__).parent / 'rubric-evaluator.py'
)
rubric_eval_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rubric_eval_module)
RubricEvaluator = rubric_eval_module.RubricEvaluator


class RefinementSuggester:
    """Generates specific refinement suggestions based on criterion scores."""

    SUGGESTIONS = {
        'fundamento': [
            {
                'title': 'Add missing introduction',
                'description': 'Establish context, problem statement, and scope before diving into details',
                'tactic': 'Add a 2-3 sentence intro explaining what problem this solves and who it\'s for',
                'impact': 'medium',
                'effort': 'low'
            },
            {
                'title': 'Add conclusion/summary',
                'description': 'Tie together all sections and provide clear takeaways',
                'tactic': 'Add a final section that recaps main points and recommends next steps',
                'impact': 'medium',
                'effort': 'low'
            },
            {
                'title': 'Flatten heading hierarchy',
                'description': 'If heading levels exceed 4, convert nested sections to parallel sections',
                'tactic': 'Convert ### ### #### to ### ### ### (parallel structure)',
                'impact': 'low',
                'effort': 'medium'
            },
        ],

        'veracidad': [
            {
                'title': 'Remove weasel words',
                'description': 'Replace vague hedging words with specific claims or caveats',
                'tactic': 'Search for: somehow, mysteriously, appears to, seems to, allegedly. Replace or cite source.',
                'before': 'This somehow improves performance.',
                'after': 'This improves throughput by 20-30% (see benchmark results).',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Add sources for factual claims',
                'description': 'Support numeric claims and specific assertions with citations',
                'tactic': 'For each number: add "According to [source]" or cite the study',
                'before': 'Studies show that 85% of users prefer X.',
                'after': 'Studies show that 85% of users prefer X (Nielsen 2023, n=1000).',
                'impact': 'high',
                'effort': 'medium'
            },
            {
                'title': 'Clarify speculative statements',
                'description': 'Mark speculation as such with "could", "may", "likely" where appropriate',
                'tactic': 'For uncertain claims, prefix with: "This likely...", "Could result in...", "May happen if..."',
                'before': 'This causes performance issues.',
                'after': 'This could cause performance issues in scenarios with [specific condition].',
                'impact': 'medium',
                'effort': 'low'
            },
        ],

        'calidad': [
            {
                'title': 'Convert passive to active voice',
                'description': 'Replace "was done by X" with "X did it" for clarity',
                'tactic': 'Find "[to be] + past participle" patterns. Restructure as [agent] + [verb].',
                'before': 'The system was optimized by engineers to improve latency.',
                'after': 'Engineers optimized the system to improve latency.',
                'impact': 'high',
                'effort': 'medium'
            },
            {
                'title': 'Remove filler words',
                'description': 'Delete meaningless amplifiers (very, really, quite, basically)',
                'tactic': 'Search for: very, really, quite, basically, somewhat. Delete or replace with specific.',
                'before': 'This is very important and quite effective.',
                'after': 'This improves latency by 40%.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Ensure consistent register',
                'description': 'Match formality level across all sections',
                'tactic': 'Sample each section. If tone shifts, rewrite to match the dominant register.',
                'impact': 'medium',
                'effort': 'medium'
            },
        ],

        'densidad': [
            {
                'title': 'Apply 2x density constraint',
                'description': 'Merge sentences that say the same thing; eliminate duplication',
                'tactic': 'Read pairs of consecutive sentences. If they express the same idea, merge.',
                'before': 'Indexes improve query speed. They make lookups faster.',
                'after': 'Indexes improve query speed.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Convert prose lists to tables',
                'description': 'Replace 3+ related items in prose with a structured table',
                'tactic': 'If you list 3+ related items, convert to table with consistent attributes.',
                'before': 'X is fast but expensive. Y is cheap but slow.',
                'after': '| | Speed | Cost |\n| X | Fast | Expensive |\n| Y | Slow | Cheap |',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Remove filler sentences',
                'description': 'Delete sentences that add no new information',
                'tactic': 'Read each sentence. Does it advance the argument? If not, delete.',
                'before': 'It goes without saying that X. As mentioned above, Y.',
                'after': '[Sentence deleted. Content merged above.]',
                'impact': 'high',
                'effort': 'low'
            },
        ],

        'simplicidad': [
            {
                'title': 'Flatten heading hierarchy',
                'description': 'If hierarchy exceeds 3 levels, restructure as parallel sections',
                'tactic': 'Convert deep nesting to sibling sections at similar depth',
                'impact': 'high',
                'effort': 'medium'
            },
            {
                'title': 'Explain jargon on first use',
                'description': 'Add brief definition when introducing domain-specific terms',
                'tactic': 'First mention of each jargon term: add parenthetical or glossary link',
                'before': 'Use memoization to optimize.',
                'after': 'Use memoization (caching computed results) to optimize.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Start with simple examples',
                'description': 'Lead with the simplest case; progress to complex',
                'tactic': 'Reorder examples: basic first, advanced last',
                'impact': 'medium',
                'effort': 'medium'
            },
        ],

        'claridad': [
            {
                'title': 'Replace vague qualifiers',
                'description': 'Convert words like "appropriate", "sometimes", "significant" to specifics',
                'tactic': 'Build replacement table: "appropriate" → [criteria], "sometimes" → [condition]',
                'before': 'Use appropriate tools for this situation.',
                'after': 'Use tools that match your [budget, team skill, integration needs].',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Clarify pronoun references',
                'description': 'Replace ambiguous pronouns with explicit nouns',
                'tactic': 'Mark every "it", "they", "this". If multiple antecedents possible, use noun.',
                'before': 'X affects Y. It increases when it rises.',
                'after': 'X affects Y. Revenue increases when X rises.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Clarify implicit conditions',
                'description': 'When an action is conditional, make the condition explicit',
                'tactic': 'Every "do X" should have "when Y" nearby; add if missing',
                'before': 'You should validate input.',
                'after': 'Validate input for all external sources (skip for trusted internal APIs).',
                'impact': 'high',
                'effort': 'low'
            },
        ],

        'precision': [
            {
                'title': 'Convert aspirational to testable',
                'description': 'Replace vague imperatives with measurable constraints',
                'tactic': 'For each "be X" or "make X better", add specific criterion: [exact metric]',
                'before': 'Be concise and write clearly.',
                'after': 'Maximum 300 words per section. Maximum 2 vague qualifiers per paragraph.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Add units to numeric claims',
                'description': 'Every number needs units and context',
                'tactic': 'Audit all numbers: add units (words, ms, %, items) and context',
                'before': 'Process 100 items in 50.',
                'after': 'Process 100 items in 50 milliseconds.',
                'impact': 'high',
                'effort': 'low'
            },
            {
                'title': 'Define success criteria',
                'description': 'For each recommendation, state how you\'ll know it worked',
                'tactic': 'Add "Success looks like: [observable, measurable outcome]"',
                'before': 'Implement caching.',
                'after': 'Implement caching. Success: request latency < 100ms, cache hit rate > 80%.',
                'impact': 'medium',
                'effort': 'low'
            },
        ],

        'profundidad': [
            {
                'title': 'Identify edge cases',
                'description': 'Ask: What if data is missing/contradictory/extreme?',
                'tactic': 'For each component, document: missing data → fallback, conflict → priority rule, extreme → limit',
                'before': 'Parse the input and process it.',
                'after': 'Parse input. If unparseable: log error and skip record. If missing field X: use default [value].',
                'impact': 'high',
                'effort': 'medium'
            },
            {
                'title': 'Add error handling strategies',
                'description': 'For each likely failure, describe recovery or escalation',
                'tactic': 'Build 5-item failure mode list: [what fails?] → [symptom] → [recovery]',
                'impact': 'high',
                'effort': 'medium'
            },
            {
                'title': 'Document limitations',
                'description': 'Explicitly state what this does NOT handle',
                'tactic': 'Add "Limitations" section: [specific scenario] not supported because [reason]',
                'before': '[No limitations mentioned]',
                'after': 'Limitations: Assumes input < 1MB. Doesn\'t handle concurrent writes. Requires [dependency].',
                'impact': 'medium',
                'effort': 'low'
            },
        ],

        'coherencia': [
            {
                'title': 'Add cross-references',
                'description': 'Link related sections to show how they support each other',
                'tactic': 'In each section, add "See [section] for..." to relevant dependencies',
                'impact': 'medium',
                'effort': 'low'
            },
            {
                'title': 'Reconcile contradictions',
                'description': 'Find claims that seem to conflict; clarify the boundary',
                'tactic': 'Identify two related claims that could conflict. Clarify: "Always do X, except in case Y"',
                'impact': 'medium',
                'effort': 'medium'
            },
            {
                'title': 'Standardize terminology',
                'description': 'Ensure key terms are used consistently',
                'tactic': 'List all key terms. Audit for synonyms (user/customer). Use one term throughout.',
                'impact': 'medium',
                'effort': 'low'
            },
        ],

        'valor': [
            {
                'title': 'Inject domain expertise',
                'description': 'Add frameworks, best practices, or reasoning specific to the field',
                'tactic': 'Add [domain framework]: "Choose based on [criteria]: if X, then Y; if A, then B"',
                'before': 'Use a database.',
                'after': 'Choose persistence based on: if reads >> writes, optimize reads; if writes >> reads, optimize throughput.',
                'impact': 'high',
                'effort': 'high'
            },
            {
                'title': 'Add methodology/reasoning',
                'description': 'Explain WHY, not just WHAT. Add reasoning patterns from experts',
                'tactic': 'Prefix recommendations with: "The reasoning is: [principle]. This means [specific action]"',
                'impact': 'high',
                'effort': 'high'
            },
            {
                'title': 'Document common pitfalls',
                'description': 'Share insights about what usually goes wrong',
                'tactic': 'Add section: "Common mistakes: [pitfall 1] happens when [condition], avoid by [action]"',
                'impact': 'high',
                'effort': 'medium'
            },
        ],
    }

    def __init__(self, filepath: str):
        """Initialize suggester with content and evaluation."""
        self.filepath = Path(filepath)
        self.evaluator = RubricEvaluator(str(filepath))
        self.evaluator.evaluate()

    def get_suggestions_for_criterion(self, criterion: str) -> List[Dict]:
        """Get suggestions for a specific criterion."""
        if criterion not in self.SUGGESTIONS:
            return []
        return self.SUGGESTIONS[criterion]

    def get_top_n_suggestions(self, n: int = 3) -> Dict[str, List[Dict]]:
        """Get suggestions for the N lowest-scoring criteria."""
        # Sort criteria by score
        sorted_criteria = sorted(
            self.evaluator.scores.items(),
            key=lambda x: x[1]
        )

        result = {}
        for criterion, score in sorted_criteria[:n]:
            suggestions = self.get_suggestions_for_criterion(criterion)
            result[criterion] = {
                'score': score,
                'suggestions': suggestions,
                'issues': self.evaluator.issues.get(criterion, []),
            }

        return result

    def format_text(self, criterion: str = None, top_n: int = 3) -> str:
        """Format suggestions as readable text."""
        lines = [
            "\n" + "=" * 70,
            "REFINEMENT SUGGESTIONS",
            "=" * 70,
        ]

        if criterion:
            # Single criterion
            suggestions = self.get_suggestions_for_criterion(criterion)
            score = self.evaluator.scores.get(criterion, 0)
            issues = self.evaluator.issues.get(criterion, [])

            lines.extend([
                f"\nCriterion: {criterion.upper()}",
                f"Current Score: {score}/10",
            ])

            if issues:
                lines.extend(["\nIssues Detected:"])
                for issue in issues:
                    lines.append(f"  • {issue}")

            if suggestions:
                lines.extend(["\nSuggestions:"])
                for i, sugg in enumerate(suggestions, 1):
                    lines.extend([
                        f"\n{i}. {sugg['title']}",
                        f"   Description: {sugg['description']}",
                        f"   Tactic: {sugg['tactic']}",
                        f"   Impact: {sugg['impact']} | Effort: {sugg['effort']}",
                    ])
                    if 'before' in sugg:
                        lines.extend([
                            f"   Before: {sugg['before']}",
                            f"   After:  {sugg['after']}",
                        ])
        else:
            # Top N criteria
            top = self.get_top_n_suggestions(top_n)
            lines.append(f"\nTop {min(len(top), top_n)} Lowest-Scoring Criteria:\n")

            for criterion, data in top.items():
                score = data['score']
                issues = data['issues']
                suggestions = data['suggestions']

                lines.extend([
                    f"\n{criterion.upper()}: {score}/10",
                    "-" * 50,
                ])

                if issues:
                    lines.append("Issues:")
                    for issue in issues:
                        lines.append(f"  • {issue}")
                    lines.append("")

                if suggestions:
                    lines.append("Top 2 Suggestions:")
                    for i, sugg in enumerate(suggestions[:2], 1):
                        lines.extend([
                            f"\n  {i}. {sugg['title']}",
                            f"     Tactic: {sugg['tactic']}",
                            f"     Impact: {sugg['impact']}",
                        ])
                        if 'before' in sugg:
                            lines.extend([
                                f"     Before: {sugg['before']}",
                                f"     After:  {sugg['after']}",
                            ])

        lines.extend([
            "",
            "=" * 70,
        ])
        return "\n".join(lines)

    def format_json(self, criterion: str = None, top_n: int = 3) -> str:
        """Format suggestions as JSON."""
        if criterion:
            data = {
                'criterion': criterion,
                'score': self.evaluator.scores.get(criterion, 0),
                'issues': self.evaluator.issues.get(criterion, []),
                'suggestions': self.get_suggestions_for_criterion(criterion),
            }
        else:
            data = {
                'top_n': top_n,
                'suggestions': self.get_top_n_suggestions(top_n),
            }

        return json.dumps(data, indent=2)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate refinement suggestions based on criterion scores.',
    )
    parser.add_argument('filepath', help='Path to content file')
    parser.add_argument(
        '--criterion',
        type=str,
        help='Target a specific criterion (e.g., clarity, densidad)',
    )
    parser.add_argument(
        '--top',
        type=int,
        default=3,
        help='Show suggestions for top N lowest-scoring criteria (default: 3)',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format',
    )

    args = parser.parse_args()

    try:
        suggester = RefinementSuggester(args.filepath)

        if args.json:
            print(suggester.format_json(
                criterion=args.criterion,
                top_n=args.top
            ))
        else:
            print(suggester.format_text(
                criterion=args.criterion,
                top_n=args.top
            ))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
