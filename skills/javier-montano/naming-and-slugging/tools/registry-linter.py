#!/usr/bin/env python3
"""
Audits naming compliance across a project directory.

Checks all files and folders against kebab-case conventions,
with awareness of entity-specific patterns (R- prefix for rules,
SKILL.md/README.md as uppercase exceptions, compound extensions).

Usage:
  registry_linter.py /path/to/project
  registry_linter.py /path/to/project --strict    Fail on warnings too
  registry_linter.py /path/to/project --json      Output JSON for tooling
"""

import json
import os
import re
import sys

SLUG_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
RULE_PATTERN = re.compile(r'^R-[a-z0-9]+(-[a-z0-9]+)*$')
VERSION_PATTERN = re.compile(r'\bv\d+\b')
STATUS_PREFIXES = ['new-', 'old-', 'temp-', 'wip-', 'final-', 'draft-']

# Files that are conventionally uppercase (exceptions to kebab-case)
UPPERCASE_CONVENTIONS = {
    'SKILL.md', 'README.md', 'REFERENCE.md', 'LICENSE', 'LICENSE.txt',
    'LICENSE.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'Makefile', 'Dockerfile',
}

# Compound extensions that are semantic, not naming violations
COMPOUND_EXTENSIONS = {'.test.ts', '.test.tsx', '.test.js', '.spec.ts', '.spec.tsx',
                       '.spec.js', '.module.css', '.module.scss', '.stories.tsx',
                       '.stories.ts', '.config.ts', '.config.js', '.d.ts'}

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.DS_Store', 'venv',
               '.venv', 'dist', 'build', '.next', '.cache', 'coverage'}
IGNORE_PATTERNS = {'.DS_Store', '.gitignore', '.gitkeep', '.env', '.npmrc',
                   '.eslintrc', '.prettierrc'}


def extract_base_name(filename: str) -> tuple[str, str]:
    """Separate a filename into base name and extension, handling compound extensions."""
    for compound in sorted(COMPOUND_EXTENSIONS, key=len, reverse=True):
        if filename.lower().endswith(compound):
            base = filename[:len(filename) - len(compound)]
            return base, compound
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        return parts[0], f'.{parts[1]}'
    return filename, ''


def lint_name(name: str, is_dir: bool = False) -> dict:
    """Lint a single file or directory name. Returns dict with errors and warnings."""
    errors = []
    warnings = []

    # Skip uppercase convention files
    if name in UPPERCASE_CONVENTIONS:
        return {'errors': [], 'warnings': []}

    if is_dir:
        base = name
    else:
        base, ext = extract_base_name(name)

        # Check extension is lowercase
        if ext and ext != ext.lower():
            errors.append(f"Extension should be lowercase in '{name}'")

    # Check for rule pattern (R- prefix is valid for rules)
    if RULE_PATTERN.match(base):
        # Valid rule name, skip normal kebab-case check
        pass
    elif not SLUG_PATTERN.match(base):
        if base != base.lower():
            errors.append(f"Uppercase letters in '{name}'")
        if '_' in base:
            errors.append(f"Underscores in '{name}' (use hyphens)")
        if ' ' in name:
            errors.append(f"Spaces in '{name}'")
        if not errors:
            # Only report generic pattern failure if we didn't find specific issues
            errors.append(f"'{name}' doesn't match kebab-case pattern")

    # Warnings (valid but suboptimal)
    if VERSION_PATTERN.search(base):
        warnings.append(f"Version marker in '{name}' (use git tags instead)")

    for prefix in STATUS_PREFIXES:
        if base.lower().startswith(prefix):
            warnings.append(f"Status prefix '{prefix[:-1]}' in '{name}'")

    words = [w for w in base.replace('R-', '', 1).split('-') if w] if base.startswith('R-') else base.split('-')
    if len(words) > 5:
        warnings.append(f"'{name}' has {len(words)} words (aim for 2-4)")

    return {'errors': errors, 'warnings': warnings}


def lint_directory(path: str) -> list[dict]:
    """Lint all names in a directory tree. Returns list of issue dicts."""
    all_issues = []

    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.'))

        rel_root = os.path.relpath(root, path)

        for d in dirs:
            result = lint_name(d, is_dir=True)
            rel_path = os.path.join(rel_root, d) if rel_root != '.' else d
            for err in result['errors']:
                all_issues.append({'level': 'error', 'path': rel_path, 'message': err})
            for warn in result['warnings']:
                all_issues.append({'level': 'warning', 'path': rel_path, 'message': warn})

        for f in sorted(files):
            if f in IGNORE_PATTERNS or f.startswith('.'):
                continue
            result = lint_name(f)
            rel_path = os.path.join(rel_root, f) if rel_root != '.' else f
            for err in result['errors']:
                all_issues.append({'level': 'error', 'path': rel_path, 'message': err})
            for warn in result['warnings']:
                all_issues.append({'level': 'warning', 'path': rel_path, 'message': warn})

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: registry_linter.py /path/to/project [--strict] [--json]")
        sys.exit(1)

    target_path = sys.argv[1]
    strict_mode = '--strict' in sys.argv
    json_mode = '--json' in sys.argv

    if not os.path.isdir(target_path):
        print(f"Error: '{target_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    issues = lint_directory(target_path)

    errors = [i for i in issues if i['level'] == 'error']
    warnings = [i for i in issues if i['level'] == 'warning']

    if json_mode:
        output = {
            'path': os.path.abspath(target_path),
            'errors': len(errors),
            'warnings': len(warnings),
            'issues': issues,
            'passed': len(errors) == 0 and (not strict_mode or len(warnings) == 0),
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Linting names in: {target_path}")
        print("=" * 60)

        if errors:
            for e in errors:
                print(f"  ERROR  {e['path']} — {e['message']}")
        if warnings:
            for w in warnings:
                print(f"  WARN   {w['path']} — {w['message']}")

        print(f"\n{'=' * 60}")
        if not errors and not warnings:
            print("All names pass naming conventions.")
        else:
            print(f"{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors or (strict_mode and warnings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
