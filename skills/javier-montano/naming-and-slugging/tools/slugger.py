#!/usr/bin/env python3
"""
Naming & Slugging tool: converts raw text to URL-safe kebab-case slugs,
validates existing names, and cleans up messy filenames.

Three modes:
  slugger.py "Raw Name"              → basic slug (normalize characters)
  slugger.py --clean "name-v2-final" → clean slug (strip versions + status)
  slugger.py --validate "some-name"  → validate against conventions + suggest fix
"""

import os
import re
import sys
import unicodedata

VERSION_PATTERN = re.compile(r'[-.]?v\d+[-.]?')
STATUS_PREFIXES = re.compile(r'^(new|old|temp|wip|final|draft|copy)-')
TRAILING_NOISE = re.compile(r'-(final|copy|backup|old|bak|tmp)$')


def slugify(value: str) -> str:
    """Convert any string to a valid kebab-case slug.

    Normalizes unicode, lowercases, replaces separators with hyphens,
    and removes everything that isn't [a-z0-9-].
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[_\s]+', '-', value)
    value = re.sub(r'[^a-z0-9-]', '', value)
    value = re.sub(r'-{2,}', '-', value)
    return value.strip('-')


def clean_name(value: str) -> str:
    """Slugify + strip version markers, status prefixes, and trailing noise.

    Use this when renaming existing files to their canonical form.
    Examples:
      "new-api-client-v2-final" → "api-client"
      "old-dashboard-v3.ts"    → "dashboard"  (extension handled separately)
    """
    # Separate extension if present
    ext = ''
    if '.' in value:
        parts = value.rsplit('.', 1)
        # Handle compound extensions (.test.ts, .module.css, .spec.tsx)
        compound_check = value.rsplit('.', 2) if value.count('.') >= 2 else None
        if compound_check and len(compound_check) == 3:
            mid = compound_check[1].lower()
            if mid in ('test', 'spec', 'module', 'stories', 'styles', 'config', 'd'):
                ext = f'.{mid}.{compound_check[2].lower()}'
                value = compound_check[0]
            else:
                ext = f'.{parts[1].lower()}'
                value = parts[0]
        else:
            ext = f'.{parts[1].lower()}'
            value = parts[0]

    slug = slugify(value)

    # Strip version markers (v1, v2, etc.) — replace with hyphen to preserve word boundaries
    slug = VERSION_PATTERN.sub('-', slug)

    # Strip status prefixes (new-, old-, draft-, etc.)
    slug = STATUS_PREFIXES.sub('', slug)

    # Strip trailing noise (-final, -copy, -backup, etc.)
    slug = TRAILING_NOISE.sub('', slug)

    # Clean up consecutive hyphens and trim (stripping creates artifacts)
    slug = re.sub(r'-{2,}', '-', slug).strip('-')

    return slug + ext if slug else ext.lstrip('.')


def validate_slug(slug: str) -> dict:
    """Validate a slug against naming conventions.

    Returns dict with 'issues' (list of problems) and 'suggestion' (cleaned version).
    """
    issues = []

    # Separate extension for validation
    base = slug
    ext = ''
    if '.' in slug:
        parts = slug.rsplit('.', 1)
        base = parts[0]
        ext = f'.{parts[1]}'

    if base != base.lower():
        issues.append("Contains uppercase letters")

    if '_' in base:
        issues.append("Contains underscores (use hyphens)")

    if ' ' in base:
        issues.append("Contains spaces")

    if re.search(r'[^a-z0-9-]', base):
        issues.append("Contains invalid characters (only a-z, 0-9, - allowed)")

    if '--' in base:
        issues.append("Contains consecutive hyphens")

    words = [w for w in base.split('-') if w]
    if len(words) > 5:
        issues.append(f"Too long ({len(words)} words, aim for 2-4)")
    elif len(words) < 1:
        issues.append("Empty name")

    version_match = re.search(r'\bv\d+\b', base)
    if version_match:
        issues.append(f"Contains version marker '{version_match.group()}' (use git tags)")

    status_prefixes = ['new-', 'old-', 'temp-', 'wip-', 'final-', 'draft-']
    for prefix in status_prefixes:
        if base.startswith(prefix):
            issues.append(f"Starts with status prefix '{prefix[:-1]}' (name should describe content)")

    # Generate suggestion if there are issues
    suggestion = None
    if issues:
        suggestion = clean_name(slug)

    return {'issues': issues, 'suggestion': suggestion}


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  slugger.py \"Raw Name Here\"              Generate kebab-case slug")
        print("  slugger.py --clean \"name-v2-final\"       Slug + strip versions/status")
        print("  slugger.py --validate \"existing-name\"    Check conventions + suggest fix")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == '--validate':
        if len(sys.argv) < 3:
            print("Error: --validate requires a name argument")
            sys.exit(1)
        slug = sys.argv[2]
        result = validate_slug(slug)
        if result['issues']:
            print(f"Issues with '{slug}':")
            for issue in result['issues']:
                print(f"  - {issue}")
            if result['suggestion']:
                print(f"  Suggested: {result['suggestion']}")
            sys.exit(1)
        else:
            print(f"'{slug}' is valid.")
            sys.exit(0)

    elif mode == '--clean':
        if len(sys.argv) < 3:
            print("Error: --clean requires a name argument")
            sys.exit(1)
        raw = ' '.join(sys.argv[2:])
        print(clean_name(raw))

    else:
        raw = ' '.join(sys.argv[1:])
        print(slugify(raw))


if __name__ == "__main__":
    main()
