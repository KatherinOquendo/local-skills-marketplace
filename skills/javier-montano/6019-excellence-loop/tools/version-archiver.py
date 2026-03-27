#!/usr/bin/env python3
"""
Version Archiver: Track iteration history with scores and changes.

Usage:
    python version-archiver.py --input <file> --iteration N --scores "9,8,10,7,..." [--changes "description"]
    python version-archiver.py --show-history <file>

Examples:
    python version-archiver.py --input content.md --iteration 1 --scores "7,6,8,5,7,6,7,8,7,6" --changes "Initial draft"
    python version-archiver.py --input content.md --iteration 2 --scores "8,7,9,8,8,8,8,9,8,7" --changes "Merged duplicates, replaced vague qualifiers"
    python version-archiver.py --show-history content.md

Output:
    - Stores version history in {filename}.history.json
    - Displays iteration progression with score changes
    - Calculates delta (improvement) between iterations
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


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

CRITERIA_SHORT = {
    'fundamento': 'F',
    'veracidad': 'V',
    'calidad': 'C',
    'densidad': 'D',
    'simplicidad': 'S',
    'claridad': 'Cl',
    'precision': 'P',
    'profundidad': 'Pr',
    'coherencia': 'Co',
    'valor': 'Va',
}


class VersionArchiver:
    """Manages iteration history for content refinement."""

    def __init__(self, filepath: str):
        """Initialize archiver for content file."""
        self.filepath = Path(filepath)
        self.history_path = self.filepath.with_suffix(
            self.filepath.suffix + '.history.json'
        )

        # Load existing history or create new
        if self.history_path.exists():
            with open(self.history_path, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = {
                'content_name': self.filepath.name,
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'iterations': [],
            }

    def add_iteration(
        self,
        iteration: int,
        scores: List[int],
        changes: str = "",
        notes: str = "",
        status: str = "in_progress",
    ) -> None:
        """Add a new iteration to history."""
        if len(scores) != len(CRITERIA):
            raise ValueError(
                f"Expected {len(CRITERIA)} scores, got {len(scores)}"
            )

        # Calculate average
        avg_score = sum(scores) / len(scores)

        # Calculate delta from previous iteration
        delta = None
        if self.history['iterations']:
            prev_avg = self.history['iterations'][-1]['average_score']
            delta = round(avg_score - prev_avg, 2)

        # Calculate weaknesses (lowest 3 criteria)
        score_pairs = list(zip(CRITERIA, scores))
        sorted_pairs = sorted(score_pairs, key=lambda x: x[1])
        weaknesses = [c for c, _ in sorted_pairs[:3] if _ < 10]

        # Build iteration record
        iteration_record = {
            'iteration': iteration,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'scores': {c: s for c, s in zip(CRITERIA, scores)},
            'average_score': round(avg_score, 2),
            'weaknesses': weaknesses,
            'changes_made': changes if isinstance(changes, list) else [changes] if changes else [],
            'status': status,
        }

        if delta is not None:
            iteration_record['delta_from_previous'] = delta

        if notes:
            iteration_record['notes'] = notes

        self.history['iterations'].append(iteration_record)

    def save(self) -> None:
        """Save history to file."""
        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)

    def display_history(self) -> str:
        """Format and display full history."""
        if not self.history['iterations']:
            return "No iterations recorded yet."

        lines = [
            "\n" + "=" * 70,
            f"VERSION HISTORY: {self.filepath.name}",
            "=" * 70,
        ]

        for record in self.history['iterations']:
            iteration = record['iteration']
            timestamp = record['timestamp'][:10]  # YYYY-MM-DD
            avg = record['average_score']
            delta = record.get('delta_from_previous')

            lines.append(f"\nIteration {iteration} ({timestamp})")
            lines.append("-" * 70)

            # Score bar
            filled = "█" * int(avg)
            empty = "░" * (10 - int(avg))
            bar = f"{filled}{empty}"
            lines.append(f"Average: {avg}/10 {bar}", )

            if delta is not None:
                sign = "+" if delta > 0 else ""
                lines.append(f"Delta: {sign}{delta}")

            # Individual scores
            scores = record['scores']
            score_str = " ".join(
                f"{CRITERIA_SHORT[c]}:{scores[c]}"
                for c in CRITERIA
            )
            lines.append(f"Scores: {score_str}")

            # Weaknesses
            if record['weaknesses']:
                weaknesses_str = ", ".join(record['weaknesses'])
                lines.append(f"Weaknesses: {weaknesses_str}")

            # Changes
            changes = record.get('changes_made', [])
            if changes and (isinstance(changes, list) and changes[0] or changes):
                lines.append("Changes:")
                if isinstance(changes, str):
                    lines.append(f"  • {changes}")
                else:
                    for change in changes:
                        if change:
                            lines.append(f"  • {change}")

            # Status
            status = record.get('status', '')
            if status:
                lines.append(f"Status: {status.upper()}")

            # Notes
            notes = record.get('notes', '')
            if notes:
                lines.append(f"Notes: {notes}")

        lines.extend([
            "",
            "=" * 70,
            f"Total Iterations: {len(self.history['iterations'])}",
            "=" * 70,
        ])

        return "\n".join(lines)

    def display_summary(self) -> str:
        """Display summary table of all iterations."""
        if not self.history['iterations']:
            return "No iterations recorded yet."

        lines = [
            "\n" + "=" * 80,
            f"SUMMARY: {self.filepath.name}",
            "=" * 80,
            "\n| Iter | Average | Delta | " + " | ".join(
                f"{CRITERIA_SHORT[c]}" for c in CRITERIA
            ) + " |",
            "|------|---------|-------|" + "|------|" * 10,
        ]

        for record in self.history['iterations']:
            it = record['iteration']
            avg = record['average_score']
            delta = record.get('delta_from_previous')
            scores = record['scores']

            delta_str = f"+{delta}" if delta and delta > 0 else str(delta) if delta else "—"

            score_parts = [
                f" {scores[c]}" for c in CRITERIA
            ]

            lines.append(
                f"| {it:4d} | {avg:7.1f} | {delta_str:5s} |" +
                "|".join(score_parts) + " |"
            )

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Manage iteration history for content refinement.',
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Add iteration
    add_parser = subparsers.add_parser(
        'add',
        aliases=['--input'],
        help='Add a new iteration to history',
    )
    add_parser.add_argument('--input', required=True, help='Content file path')
    add_parser.add_argument(
        '--iteration',
        type=int,
        required=True,
        help='Iteration number',
    )
    add_parser.add_argument(
        '--scores',
        required=True,
        help='Comma-separated scores (10 values, 0-10)',
    )
    add_parser.add_argument(
        '--changes',
        help='Description of changes made',
    )
    add_parser.add_argument(
        '--notes',
        help='Additional notes',
    )
    add_parser.add_argument(
        '--status',
        default='in_progress',
        help='Status: in_progress, delivered (default: in_progress)',
    )

    # Show history
    hist_parser = subparsers.add_parser(
        'show',
        aliases=['--show-history'],
        help='Display iteration history',
    )
    hist_parser.add_argument('filepath', help='Content file path')
    hist_parser.add_argument(
        '--summary',
        action='store_true',
        help='Show summary table instead of detailed view',
    )
    hist_parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON history',
    )

    # Parse arguments
    # Handle legacy format: version-archiver.py --input FILE --iteration N --scores "..."
    args = None
    try:
        args = parser.parse_args()
    except SystemExit:
        # Check if using legacy format
        import sys as sys_module
        argv = sys_module.argv[1:]
        if '--input' in argv and '--iteration' in argv and '--scores' in argv:
            # Parse manually
            filepath = argv[argv.index('--input') + 1]
            iteration = int(argv[argv.index('--iteration') + 1])
            scores_str = argv[argv.index('--scores') + 1]
            changes = None
            if '--changes' in argv:
                changes = argv[argv.index('--changes') + 1]

            try:
                scores = [int(s.strip()) for s in scores_str.split(',')]
                archiver = VersionArchiver(filepath)
                archiver.add_iteration(iteration, scores, changes or "")
                archiver.save()
                print(f"✓ Archived iteration {iteration}: {scores}")
                sys_module.exit(0)
            except Exception as e:
                print(f"Error: {e}", file=sys_module.stderr)
                sys_module.exit(1)
        else:
            raise

    # Execute command
    try:
        if args.command in ['add', '--input']:
            # Explicitly handle --input namespace
            filepath = getattr(args, 'input', None)
            if not filepath:
                raise ValueError("--input (filepath) is required")

            iteration = args.iteration
            scores = [int(s.strip()) for s in args.scores.split(',')]

            if len(scores) != len(CRITERIA):
                raise ValueError(
                    f"Expected {len(CRITERIA)} scores, got {len(scores)}"
                )

            archiver = VersionArchiver(filepath)
            archiver.add_iteration(
                iteration=iteration,
                scores=scores,
                changes=args.changes or "",
                notes=args.notes or "",
                status=args.status,
            )
            archiver.save()

            print(f"✓ Archived iteration {iteration}")
            print(f"  Average: {sum(scores) / len(scores):.1f}/10")
            print(f"  Saved to: {archiver.history_path}")

        elif args.command in ['show', '--show-history']:
            filepath = args.filepath
            archiver = VersionArchiver(filepath)

            if args.json:
                print(json.dumps(archiver.history, indent=2))
            elif args.summary:
                print(archiver.display_summary())
            else:
                print(archiver.display_history())

        else:
            parser.print_help()

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
