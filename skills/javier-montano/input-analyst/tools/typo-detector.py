#!/usr/bin/env python3
"""
Typo Detector: Surface-level error detection and correction.

Detects and corrects common spelling errors, typos, autocorrect artifacts,
and punctuation issues using pattern matching and dictionary-based approaches.

Usage:
    python typo-detector.py "raw text here"
    python typo-detector.py "raw text here" --json
    python typo-detector.py "raw text here" --language es
    python typo-detector.py "raw text here" --json --language es
"""

import json
import re
import argparse
from typing import List, Tuple, Dict, Any


class TypoDetector:
    """Detects and corrects common typos, misspellings, and punctuation errors."""

    # High-confidence spelling errors (almost always wrong)
    HIGH_CONFIDENCE_CORRECTIONS = {
        'teh': 'the',
        'hte': 'the',
        'taht': 'that',
        'ahve': 'have',
        'recieve': 'receive',
        'recieved': 'received',
        'thier': 'their',
        'beleive': 'believe',
        'beleived': 'believed',
        'concieve': 'conceive',
        'occured': 'occurred',
        'occuring': 'occurring',
        'occurance': 'occurrence',
        'seperate': 'separate',
        'doesnt': "doesn't",
        'cant': "can't",
        'wont': "won't",
        'shouldnt': "shouldn't",
        'wouldnt': "wouldn't",
        'couldnt': "couldn't",
        'arent': "aren't",
        'isnt': "isn't",
        'hes': "he's",
        'shes': "she's",
        'its': "it's",  # when meaning "it is", not possessive
        'youre': "you're",
        'theres': "there's",
        'wheres': "where's",
        'becuz': 'because',
        'becuse': 'because',
        'becuase': 'because',
        'becaus': 'because',
        'frend': 'friend',
        'frendly': 'friendly',
        'intrested': 'interested',
        'untill': 'until',
        'succeded': 'succeeded',
        'reccomend': 'recommend',
        'accomodate': 'accommodate',
    }

    # Homophones and near-homophones (context-dependent, use with care)
    CONTEXT_DEPENDENT = {
        'there': ['their', 'they\'re'],
        'their': ['there', 'they\'re'],
        'they\'re': ['there', 'their'],
        'to': ['too', 'two'],
        'too': ['to', 'two'],
        'two': ['to', 'too'],
        'would': ['wood'],
        'through': ['threw'],
        'wear': ['where', 'ware'],
        'where': ['wear', 'ware'],
    }

    # Language-specific patterns (English)
    EN_PATTERNS = {
        'doubled_letters': r'([a-z])\1{3,}',  # 4+ same letter
        'missing_apostrophe_contraction': r'\b(dont|cant|wont|shouldnt|would|couldnt|arent|isnt|hes|shes)\b',
        'excessive_punctuation': r'([.!?])\1{2,}',
        'missing_period': r'[a-z]\s+[a-z]{3,}\s+and\s+[a-z]',  # run-on with 'and'
    }

    # Language-specific patterns (Spanish)
    ES_PATTERNS = {
        'doubled_letters': r'([a-záéíóú])\1{3,}',
        'missing_punctuation': r'^[a-zá-ú]',  # lowercase start
    }

    def __init__(self, language: str = 'en'):
        """
        Initialize the detector.

        Args:
            language: Language code ('en' for English, 'es' for Spanish)
        """
        self.language = language
        self.corrections: List[Dict[str, Any]] = []
        self.patterns = self.EN_PATTERNS if language == 'en' else self.ES_PATTERNS

    def detect_and_correct(self, text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Detect and correct errors in text.

        Args:
            text: Raw input text

        Returns:
            Tuple of (corrected_text, list_of_corrections)
        """
        self.corrections = []
        corrected_text = text

        # Pass 1: High-confidence corrections
        corrected_text = self._apply_high_confidence_corrections(corrected_text)

        # Pass 2: Pattern-based corrections
        corrected_text = self._apply_pattern_corrections(corrected_text)

        # Pass 3: Punctuation normalization
        corrected_text = self._normalize_punctuation(corrected_text)

        # Pass 4: Missing vowel detection (for longer words)
        corrected_text = self._detect_missing_vowels(corrected_text)

        return corrected_text, self.corrections

    def _apply_high_confidence_corrections(self, text: str) -> str:
        """Apply high-confidence spelling corrections."""
        words = text.split()
        corrected_words = []

        for word in words:
            # Check word without trailing punctuation
            word_clean = word.rstrip('.,!?;:\'"')
            trailing_punct = word[len(word_clean):]

            if word_clean.lower() in self.HIGH_CONFIDENCE_CORRECTIONS:
                corrected = self.HIGH_CONFIDENCE_CORRECTIONS[word_clean.lower()]

                # Preserve case (first letter uppercase if original was)
                if word_clean and word_clean[0].isupper():
                    corrected = corrected[0].upper() + corrected[1:]

                corrected_word = corrected + trailing_punct
                self.corrections.append({
                    'type': 'high_confidence_spelling',
                    'original': word,
                    'corrected': corrected_word,
                    'confidence': 'high'
                })
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)

        return ' '.join(corrected_words)

    def _apply_pattern_corrections(self, text: str) -> str:
        """Apply regex pattern-based corrections."""

        # Fix excessive punctuation
        text = re.sub(r'([.!?])\1{2,}', r'\1', text)
        if re.search(r'([.!?])\1{2,}', text):
            self.corrections.append({
                'type': 'excessive_punctuation',
                'pattern': 'Multiple punctuation marks',
                'confidence': 'high'
            })

        # Fix doubled letters (very high confidence)
        def fix_doubled(match):
            char = match.group(1)
            self.corrections.append({
                'type': 'doubled_letter',
                'original': match.group(0),
                'corrected': char * 2,
                'confidence': 'high'
            })
            return char * 2

        text = re.sub(self.patterns['doubled_letters'], fix_doubled, text)

        return text

    def _normalize_punctuation(self, text: str) -> str:
        """Normalize punctuation (spacing, missing periods, etc.)."""

        # Add space after periods if missing
        text = re.sub(r'\.([A-Z])', r'. \1', text)

        # Fix space before punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)

        # Ensure space after punctuation
        text = re.sub(r'([.!?])\s*([A-Za-z])', r'\1 \2', text)

        return text

    def _detect_missing_vowels(self, text: str) -> str:
        """
        Detect patterns where vowels might be missing.

        This is more conservative; we only flag obvious cases.
        """
        # Pattern: 3+ consonants in a row (likely missing vowels)
        pattern = r'\b([bcdfghjklmnpqrstvwxyz]{3,})\b'

        def check_vowel_insertion(match):
            word = match.group(0)

            # Dictionary of common patterns with missing vowels
            missing_vowel_corrections = {
                'bcs': 'because',  # b-c-s likely missing vowels
                'cld': 'could',
                'wld': 'would',
                'shld': 'should',
                'dffrnt': 'different',
                'imprtnt': 'important',
            }

            if word in missing_vowel_corrections:
                corrected = missing_vowel_corrections[word]
                self.corrections.append({
                    'type': 'missing_vowels',
                    'original': word,
                    'corrected': corrected,
                    'confidence': 'medium'
                })
                return corrected

            return word

        text = re.sub(pattern, check_vowel_insertion, text, flags=re.IGNORECASE)
        return text


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Detect and correct common typos, spelling errors, and punctuation issues.'
    )
    parser.add_argument('text', help='Text to analyze')
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

    detector = TypoDetector(language=args.language)
    corrected_text, corrections = detector.detect_and_correct(args.text)

    output = {
        'original': args.text,
        'corrected': corrected_text,
        'corrections': corrections,
        'corrections_count': len(corrections),
        'language': args.language,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print('ORIGINAL:')
        print(f'  {args.text}')
        print()
        print('CORRECTED:')
        print(f'  {corrected_text}')
        print()

        if corrections:
            print(f'CORRECTIONS ({len(corrections)}):')
            for i, correction in enumerate(corrections, 1):
                if 'original' in correction:
                    print(f'  {i}. {correction["original"]} → {correction["corrected"]} ({correction["type"]})')
                else:
                    print(f'  {i}. {correction["pattern"]} ({correction["type"]})')
        else:
            print('No corrections needed.')


if __name__ == '__main__':
    main()
