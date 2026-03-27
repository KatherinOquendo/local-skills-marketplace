#!/usr/bin/env python3
"""
Text Analyzer: Complete 5-pass input analysis pipeline.

Orchestrates five sequential analysis passes on raw user input:
- Pass 1: Surface analysis (typos, spelling, punctuation) via TypoDetector
- Pass 2: Five Whys (root cause analysis) — generates template for manual completion
- Pass 3: Seven So Whats (value chain analysis) — generates template for manual completion
- Pass 4: Intent analysis (gap detection across 5 gap types: vocabulary, scope, expertise, emotional, context)
- Pass 5: Reformulation (synthesize all passes into structured GOAL/CONTEXT/INTENT/CONSTRAINTS prompt)

Architecture:
    Pass 1 is fully automated (dictionary + pattern matching via typo_detector.py).
    Passes 2-5 generate structured templates that require human/LLM completion.
    Each pass produces a discrete JSON artifact that feeds the next pass.

Usage:
    python text-analyzer.py "raw user input text"           # All passes, human-readable
    python text-analyzer.py "input" --passes 1,4,5          # Specific passes only
    python text-analyzer.py "input" --json                  # JSON output for integration
    python text-analyzer.py "input" --language es           # Language hint for detection
    python text-analyzer.py "input" --passes 1,2,3 --json  # Combined

Exit codes:
    0: Success
    1: No input provided or argument error
    2: Pass execution error (partial results may be available in JSON mode)

Dependencies:
    - typo_detector.py (same directory) for Pass 1. Falls back to inline minimal version if unavailable.
"""

import json
import argparse
import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add scripts directory to path for imports
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

try:
    from typo_detector import TypoDetector
except ImportError:
    # If import fails, inline a minimal version
    import re
    class TypoDetector:
        HIGH_CONFIDENCE_CORRECTIONS = {
            'teh': 'the', 'hte': 'the', 'taht': 'that',
            'recieve': 'receive', 'thier': 'their',
            'becuz': 'because', 'frend': 'friend',
        }
        def __init__(self, language='en'):
            self.language = language
            self.corrections = []
        def detect_and_correct(self, text):
            self.corrections = []
            corrected = text
            for wrong, right in self.HIGH_CONFIDENCE_CORRECTIONS.items():
                if wrong in corrected.lower():
                    corrected = re.sub(r'\b' + wrong + r'\b', right, corrected, flags=re.IGNORECASE)
                    self.corrections.append({'type': 'spelling', 'original': wrong, 'corrected': right, 'confidence': 'high'})
            return corrected, self.corrections


class TextAnalyzer:
    """Orchestrates five analysis passes on raw user input."""

    def __init__(self, language: str = 'en'):
        """Initialize analyzer with language setting."""
        self.language = language
        self.typo_detector = TypoDetector(language=language)
        self.analysis_results = {}

    def analyze(self, text: str, passes: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Run analysis passes on the input text.

        Args:
            text: Raw user input
            passes: List of pass numbers to run (1-5). If None, run all.

        Returns:
            Dictionary with analysis results from all selected passes
        """
        if passes is None:
            passes = [1, 2, 3, 4, 5]

        results = {
            'original': text,
            'language': self.language,
            'passes_requested': passes,
            'analysis': {}
        }

        if 1 in passes:
            results['analysis']['pass_1_surface'] = self._pass_1_surface(text)

        if 2 in passes:
            results['analysis']['pass_2_five_whys'] = self._pass_2_five_whys(text)

        if 3 in passes:
            results['analysis']['pass_3_seven_so_whats'] = self._pass_3_seven_so_whats(text)

        if 4 in passes:
            results['analysis']['pass_4_intent'] = self._pass_4_intent(text)

        if 5 in passes:
            pass_1_result = results['analysis'].get('pass_1_surface', self._pass_1_surface(text))
            results['analysis']['pass_5_reformulation'] = self._pass_5_reformulation(
                text, results['analysis']
            )

        return results

    def _pass_1_surface(self, text: str) -> Dict[str, Any]:
        """
        Pass 1: Surface Analysis

        Detect and catalog surface-level issues:
        - Typos and misspellings
        - Punctuation errors
        - Run-on sentences
        - Autocorrect artifacts
        - Missing punctuation

        Returns: Corrected text + list of corrections
        """
        corrected_text, corrections = self.typo_detector.detect_and_correct(text)

        # Analyze sentence structure
        sentences = re.split(r'[.!?]+', text)
        run_ons = [s for s in sentences if len(s.split()) > 20]  # sentences >20 words likely run-ons
        missing_period = bool(text and text[-1] not in '.!?')

        analysis = {
            'status': 'complete',
            'original': text,
            'corrected': corrected_text,
            'corrections': {
                'count': len(corrections),
                'details': corrections,
            },
            'surface_issues': {
                'typos_found': len([c for c in corrections if 'spelling' in c['type'].lower()]),
                'punctuation_issues': len([c for c in corrections if 'punctuation' in c['type'].lower()]),
                'run_on_sentences': len(run_ons),
                'missing_final_punctuation': missing_period,
                'has_emoji': any(ord(char) > 127 for char in text),
            },
            'quality_signals': {
                'needs_surface_cleanup': len(corrections) > 0 or missing_period,
                'clarity_issues': len(run_ons) > 0,
            }
        }

        return analysis

    def _pass_2_five_whys(self, text: str) -> Dict[str, Any]:
        """
        Pass 2: Five Whys Analysis

        Guide LLM through root cause analysis.
        Returns: Template for 5 Whys chain + prompts

        Note: This provides the structure. The actual 5 Whys
        chain should be completed by an LLM or human analyst.
        """
        # Extract main request from text (often the first sentence)
        main_request = text.split('.')[0] if '.' in text else text[:100]

        analysis = {
            'status': 'template_ready',
            'original_request': main_request,
            'five_whys_template': {
                'why_1': {
                    'question': 'What prompted this request? What\'s the immediate trigger or context?',
                    'answer': '[To be filled in by analyst]',
                    'signal': 'Look for business context, timeline, immediate driver'
                },
                'why_2': {
                    'question': 'What\'s the broader situation or context behind that?',
                    'answer': '[To be filled in by analyst]',
                    'signal': 'Should expand from immediate trigger to business context'
                },
                'why_3': {
                    'question': 'What decision or outcome does this lead to?',
                    'answer': '[To be filled in by analyst]',
                    'signal': 'Stakes and consequences should become visible'
                },
                'why_4': {
                    'question': 'Why is that decision or outcome critical right now?',
                    'answer': '[To be filled in by analyst]',
                    'signal': 'Optional: only if root isn\'t clear by Why 3'
                },
                'why_5': {
                    'question': 'What\'s the ultimate need or value being protected?',
                    'answer': '[To be filled in by analyst]',
                    'signal': 'Optional: only if Why 4 didn\'t reveal root cause'
                }
            },
            'instructions': {
                'stop_early': 'If root cause is clear before Why 5, stop there.',
                'grounding': 'Only use what they explicitly stated or what\'s directly inferable.',
                'output': 'Synthesize into one sentence: "The user\'s real need is..."'
            }
        }

        return analysis

    def _pass_3_seven_so_whats(self, text: str) -> Dict[str, Any]:
        """
        Pass 3: Seven So Whats Analysis

        Trace implications forward to understand value chain and
        calibrate response depth.

        Returns: Template for value chain + prompts
        """
        analysis = {
            'status': 'template_ready',
            'purpose': 'Trace implications forward from root need to ultimate value',
            'seven_so_whats_template': {
                'so_what_1': {
                    'question': 'If we solve this, what directly happens?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Functional outcome'
                },
                'so_what_2': {
                    'question': 'What does that enable for users?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'User behavior/experience shift'
                },
                'so_what_3': {
                    'question': 'What happens to the business/operation?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Operational/business metric impact'
                },
                'so_what_4': {
                    'question': 'How does this affect growth or stability?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Business growth trajectory'
                },
                'so_what_5': {
                    'question': 'Who else cares, and why?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Stakeholder/investor perspective'
                },
                'so_what_6': {
                    'question': 'What new capability does the organization gain?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Strategic capability'
                },
                'so_what_7': {
                    'question': 'What\'s the ultimate, long-term value?',
                    'answer': '[To be filled in by analyst]',
                    'level': 'Competitive/market advantage'
                }
            },
            'calibration_guide': {
                'stops_at_so_what_2': 'Basic quality — standard effort',
                'stops_at_so_what_4': 'Standard quality — increased effort',
                'reaches_so_what_6': 'Premium quality — high investment',
                'reaches_so_what_7': 'Flagship quality — maximum investment'
            },
            'instructions': {
                'stop_at_speculation': 'Stop if implications become purely speculative',
                'outside_control': 'Stop if dependent on external forces (market, competitors)',
                'output': 'Use final chain to calibrate response depth and quality'
            }
        }

        return analysis

    def _pass_4_intent(self, text: str) -> Dict[str, Any]:
        """
        Pass 4: Intent Analysis

        Identify gaps between what was typed and what was meant.
        Detect five gap types: vocabulary, scope, expertise, emotional, context.

        Returns: Gap analysis + detected signals
        """
        gaps_detected = []
        signals = {
            'vocabulary_signals': self._detect_vocabulary_gaps(text),
            'scope_signals': self._detect_scope_gaps(text),
            'expertise_signals': self._detect_expertise_gaps(text),
            'emotional_signals': self._detect_emotional_gaps(text),
            'context_signals': self._detect_context_gaps(text),
        }

        # Count detected signals
        for signal_type, signal_list in signals.items():
            if signal_list:
                gaps_detected.append(signal_type)

        analysis = {
            'status': 'analysis_complete',
            'gaps_detected': gaps_detected,
            'signals': signals,
            'gap_analysis_template': {
                'explicit_statements': {
                    'prompt': 'What did the user explicitly ask for?',
                    'answer': '[To be filled in by analyst]'
                },
                'implicit_signals': {
                    'prompt': 'What can you infer from word choice, tone, context?',
                    'answer': '[To be filled in by analyst]'
                },
                'gaps_between_explicit_and_implicit': {
                    'prompt': 'Where is the mismatch?',
                    'answer': '[To be filled in by analyst]'
                },
                'real_ask': {
                    'prompt': 'What does the user really need?',
                    'answer': '[To be filled in by analyst]'
                }
            },
            'instructions': 'Fill in template to identify actual user intent'
        }

        return analysis

    def _detect_vocabulary_gaps(self, text: str) -> List[str]:
        """Detect vocabulary gap signals."""
        signals = []
        patterns = {
            'technical_jargon': r'\b(algorithm|machine learning|AI|blockchain|database|API|query)\b',
            'domain_mixing': r'(SQL|JSON|function|variable|library)',
            'vague_placeholders': r'\b(thing|stuff|it|that|something|whatever)\b',
        }

        for gap_type, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                signals.append(gap_type)

        return signals

    def _detect_scope_gaps(self, text: str) -> List[str]:
        """Detect scope gap signals."""
        signals = []

        # Minimizing language
        if re.search(r'\b(just|quickly|simple|maybe|quickly|while you\'re at it)\b', text, re.IGNORECASE):
            signals.append('minimizing_language')

        # Symptom language (not root cause)
        if re.search(r'\b(fix|make it|improve|better|handle|deal with)\b', text, re.IGNORECASE):
            signals.append('symptom_language')

        # Vague deliverable
        if re.search(r'\b(dashboard|report|tool|thing|system)\b', text, re.IGNORECASE):
            signals.append('vague_deliverable')

        # Multiple bundled requests
        if text.count('also') > 0 or text.count('and then') > 1:
            signals.append('bundled_requests')

        return signals

    def _detect_expertise_gaps(self, text: str) -> List[str]:
        """Detect expertise gap signals."""
        signals = []

        # Over-engineering
        if re.search(r'\b(microservices|Kafka|distributed|Kubernetes|graph database)\b', text, re.IGNORECASE):
            signals.append('possible_over_engineering')

        # Under-engineering
        if re.search(r'\b(make it smart|use AI|automate|intelligent)\b', text, re.IGNORECASE):
            signals.append('possible_under_engineering')

        # Tool confusion
        if re.search(r'\b(install|use|setup|configure) (Docker|Kubernetes|database|framework)\b', text, re.IGNORECASE):
            signals.append('tool_confusion')

        return signals

    def _detect_emotional_gaps(self, text: str) -> List[str]:
        """Detect emotional gap signals."""
        signals = []

        # Hedging
        if re.search(r'\b(maybe|probably|I guess|I think|perhaps|might)\b', text, re.IGNORECASE):
            signals.append('hedging_language')

        # Frustration/negative framing
        if re.search(r'\b(terrible|awful|horrible|worst|impossible|frustrated|worried)\b', text, re.IGNORECASE):
            signals.append('emotional_frustration')

        # Blame language
        if re.search(r'\b(incompetent|stupid|lazy|broken|doesn\'t work)\b', text, re.IGNORECASE):
            signals.append('blame_language')

        # Capitalized emphasis
        if re.search(r'[A-Z]{2,}', text):
            signals.append('emphasis_capitalization')

        return signals

    def _detect_context_gaps(self, text: str) -> List[str]:
        """Detect context gap signals."""
        signals = []

        # Dangling pronouns
        if re.search(r'\b(it|this|that|they|them)\b', text) and len(text) < 100:
            signals.append('possible_dangling_pronouns')

        # No background/setup
        if len(text.split()) < 20:
            signals.append('very_brief_no_context')

        # Assumed knowledge
        if re.search(r'\b(the|this|that) [a-z]{1,3}\b', text):
            signals.append('possible_assumed_knowledge')

        return signals

    def _pass_5_reformulation(self, text: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pass 5: Reformulation

        Synthesize all four passes into a high-quality prompt template
        that captures real intent and follows Playbook quality standard.

        Returns: Reformulation template
        """
        pass_1 = analysis.get('pass_1_surface', {})
        corrected_text = pass_1.get('corrected', text)

        analysis_obj = {
            'status': 'reformulation_template',
            'input_quality_assessment': {
                'surface_issues_count': pass_1.get('corrections', {}).get('count', 0),
                'needs_clarification': len(analysis.get('pass_4_intent', {}).get('gaps_detected', [])) > 0,
                'overall_clarity': 'clear' if len(analysis.get('pass_4_intent', {}).get('gaps_detected', [])) == 0 else 'needs_work',
            },
            'reformulated_prompt_template': {
                'goal': {
                    'prompt': 'What is the clear, measurable objective?',
                    'guidance': 'Use action verb + measurable outcome'
                },
                'context': {
                    'prompt': 'What\'s the background inferred from 5 Whys + 7 So Whats?',
                    'guidance': 'Explain why this matters, what changed, what\'s at stake'
                },
                'intent': {
                    'prompt': 'What\'s the real ask from Pass 4 gap analysis?',
                    'guidance': 'Explain the gap between typed and meant'
                },
                'constraints': {
                    'prompt': 'What must be included/excluded?',
                    'guidance': 'Format, scope, format, length, audience, quality level'
                },
                'expected_output': {
                    'prompt': 'What is the deliverable?',
                    'guidance': 'Type, structure, format, length, success criteria'
                }
            },
            'reformulation_example': """
ORIGINAL REQUEST:
"Make our error messages better"

REFORMULATED PROMPT:
Goal: Improve error message clarity to reduce trial-to-paid conversion drop from 8% to >10%.

Context:
- Users are bouncing when errors occur (don't retry)
- Error messages use technical jargon, not user-facing language
- This is conversion-critical; affects Series A metrics

Intent:
- Real need: Reduce friction at error states, not just improve copy
- User is frustrated with low conversion, not just asking for UX improvement

Constraints:
- Must work across all 50+ error states
- Must be plain language (no jargon like "Socket timeout")
- Must suggest actionable next steps
- Must maintain brand voice (friendly, not patronizing)
- NOT in scope: Full onboarding redesign (that's phase 2)

Expected Output:
- Rewritten error messages for top 10 error paths
- Before/after examples
- Bounce rate targets: <8% at errors (down from 15%)
- Conversion targets: >10% trial-to-paid (up from 8%)
- User feedback survey results: >80% "clear next step"

Quality Level: Premium (affects fundraising metrics)
Timeline: 3 weeks (1 week audit + messaging, 2 weeks implementation + testing)
""",
            'quality_standard': 'Playbook format: clear objective + specific constraints + context + output format',
            'next_steps': 'Use this template to guide reformulation. Submit filled-in template for task-engine processing.'
        }

        return analysis_obj


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Complete 5-pass input analysis pipeline.'
    )
    parser.add_argument('text', help='Raw user input text to analyze')
    parser.add_argument(
        '--passes',
        type=str,
        default='1,2,3,4,5',
        help='Comma-separated list of passes to run (e.g., "1,4,5"). Default: all passes'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as machine-readable JSON'
    )
    parser.add_argument(
        '--language',
        choices=['en', 'es'],
        default='en',
        help='Language code (en=English, es=Spanish)'
    )

    args = parser.parse_args()

    # Parse passes
    passes = [int(p.strip()) for p in args.passes.split(',')]
    passes = [p for p in passes if 1 <= p <= 5]

    analyzer = TextAnalyzer(language=args.language)
    results = analyzer.analyze(args.text, passes=passes)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable output
        print('INPUT ANALYSIS RESULTS')
        print('=' * 60)
        print(f'Original: {args.text[:80]}...' if len(args.text) > 80 else f'Original: {args.text}')
        print(f'Language: {args.language}')
        print(f'Passes run: {args.passes}')
        print()

        for pass_num in sorted(passes):
            pass_key = f'pass_{pass_num}_' + ['surface', 'five_whys', 'seven_so_whats', 'intent', 'reformulation'][pass_num - 1]
            if pass_key in results['analysis']:
                print(f'\n--- PASS {pass_num} ---')
                pass_result = results['analysis'][pass_key]

                if pass_num == 1:
                    print(f'Corrected: {pass_result.get("corrected", args.text)}')
                    if pass_result['corrections']['count'] > 0:
                        print(f'Corrections ({pass_result["corrections"]["count"]}):')
                        for c in pass_result['corrections']['details'][:5]:
                            if 'original' in c:
                                print(f'  - {c["original"]} → {c["corrected"]}')
                        if len(pass_result['corrections']['details']) > 5:
                            print(f'  ... and {len(pass_result["corrections"]["details"]) - 5} more')

                elif pass_num == 4:
                    gaps = pass_result.get('gaps_detected', [])
                    print(f'Gaps detected: {len(gaps)}')
                    for gap in gaps:
                        print(f'  - {gap}')

                else:
                    print(f'Status: {pass_result.get("status", "unknown")}')


if __name__ == '__main__':
    main()
