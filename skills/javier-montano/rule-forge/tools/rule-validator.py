#!/usr/bin/env python3
"""
Validates governance rules against the rule-forge standard.

Validates single rules or all rules in a directory. Checks structure
(frontmatter, sections, examples), enforceability (binary language,
scope precision), and naming (R-kebab-case).

Usage:
  rule-validator.py <rule.md>              Validate one rule
  rule-validator.py <directory/>           Validate all .md files in directory
  rule-validator.py <rule.md> --strict     Fail on warnings too
  rule-validator.py <directory/> --json    JSON output for tooling
"""

import json
import os
import re
import sys


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract frontmatter and body from markdown content."""
    lines = content.strip().split('\n')
    if not lines or lines[0].strip() != '---':
        return {}, content

    end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end = i
            break

    if end < 0:
        return {}, content

    fm_text = '\n'.join(lines[1:end])
    body = '\n'.join(lines[end + 1:])

    # Simple YAML key:value extraction
    fm = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"').strip("'")

    return fm, body


def extract_constraint_section(body: str) -> str:
    """Extract just the constraint section text for advisory language checking."""
    match = re.search(
        r'##\s*(the\s+)?(constraint|law|rule)\s*\n(.*?)(?=\n##\s|\Z)',
        body, re.IGNORECASE | re.DOTALL
    )
    return match.group(3) if match else ''


def validate_rule(filepath: str) -> dict:
    """Validate a single rule file. Returns structured result."""
    errors = []
    warnings = []

    if not os.path.isfile(filepath):
        return {'file': filepath, 'errors': ['File not found'], 'warnings': [], 'passed': False}

    with open(filepath, 'r') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    name_base = filename.rsplit('.', 1)[0] if '.' in filename else filename

    # --- Frontmatter ---
    fm, body = parse_frontmatter(content)
    if not fm:
        errors.append("Missing or malformed YAML frontmatter")
    else:
        if 'description' not in fm:
            errors.append("Frontmatter missing 'description'")
        if 'globs' not in fm:
            errors.append("Frontmatter missing 'globs'")
        elif fm.get('globs') in ('*', '**/*'):
            errors.append(f"Glob '{fm['globs']}' is too broad — specify file types or paths")

    # --- Naming ---
    if not re.match(r'^R-[a-z0-9]+(-[a-z0-9]+)*$', name_base):
        warnings.append(f"Filename '{filename}' doesn't follow R-kebab-case pattern")

    # --- Required sections ---
    checks = [
        (r'##\s*(the\s+)?(constraint|law|rule)', "Missing '## The Constraint' section"),
        (r'##\s*(why|reason|rationale)', "Missing '## Why' reasoning section"),
        (r'###?\s*(bad|violation|wrong|❌)', "Missing Bad/Violation example"),
        (r'###?\s*(good|compliance|correct|✅)', "Missing Good/Compliance example"),
    ]
    for pattern, msg in checks:
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(msg)

    # --- Code blocks (examples should have actual code) ---
    code_fences = len(re.findall(r'^```', content, re.MULTILINE))
    if code_fences < 4:  # Need at least 2 code blocks (open+close for Bad and Good)
        warnings.append("Expected at least 2 code blocks for Bad and Good examples")

    # --- Enforceability: advisory language IN THE CONSTRAINT SECTION ONLY ---
    constraint_text = extract_constraint_section(body)
    advisory_terms = ['try to', 'consider', 'prefer', 'generally', 'should avoid', 'might want']
    for term in advisory_terms:
        if term in constraint_text.lower():
            warnings.append(f"Constraint uses advisory language ('{term}') — rules should be binary")

    return {
        'file': filepath,
        'errors': errors,
        'warnings': warnings,
        'passed': len(errors) == 0,
    }


def validate_directory(dirpath: str) -> list[dict]:
    """Validate all .md rule files in a directory."""
    results = []
    for f in sorted(os.listdir(dirpath)):
        if f.endswith('.md') and not f.startswith('.'):
            results.append(validate_rule(os.path.join(dirpath, f)))
    return results


def print_result(result: dict):
    """Print a single validation result."""
    label = os.path.basename(result['file'])
    if result['errors']:
        print(f"\n  {label}")
        for e in result['errors']:
            print(f"    ERROR  {e}")
    if result['warnings']:
        if not result['errors']:
            print(f"\n  {label}")
        for w in result['warnings']:
            print(f"    WARN   {w}")
    if not result['errors'] and not result['warnings']:
        print(f"  {label} — all checks passed")


def main():
    if len(sys.argv) < 2:
        print("Usage: rule-validator.py <rule.md | directory/> [--strict] [--json]")
        sys.exit(1)

    target = sys.argv[1]
    strict = '--strict' in sys.argv
    json_mode = '--json' in sys.argv

    if os.path.isdir(target):
        results = validate_directory(target)
    elif os.path.isfile(target):
        results = [validate_rule(target)]
    else:
        print(f"Error: '{target}' not found", file=sys.stderr)
        sys.exit(1)

    total_errors = sum(len(r['errors']) for r in results)
    total_warnings = sum(len(r['warnings']) for r in results)
    all_passed = all(r['passed'] for r in results)

    if json_mode:
        output = {
            'files_checked': len(results),
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'all_passed': all_passed and (not strict or total_warnings == 0),
            'results': results,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Validating {len(results)} rule(s)...")
        for r in results:
            print_result(r)
        print(f"\n{'=' * 50}")
        print(f"{total_errors} error(s), {total_warnings} warning(s)")

    if total_errors > 0 or (strict and total_warnings > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
