#!/bin/bash
# pre-commit-moat.sh — Lightweight MOAT checks for pre-commit hook
# Checks staged skill files for basic compliance (< 5 seconds)
# Install: cp scripts/pre-commit-moat.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -uo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
ERRORS=0

# Get staged skill files
STAGED_SKILLS=$(git diff --cached --name-only --diff-filter=ACM | grep "skills/.*/SKILL.md$" || true)

if [ -z "$STAGED_SKILLS" ]; then
  exit 0  # No skill files staged
fi

echo "🔍 MOAT Pre-commit Check..."

for skill_md in $STAGED_SKILLS; do
  full="$REPO_ROOT/$skill_md"
  [ -f "$full" ] || continue
  skill_name=$(basename "$(dirname "$full")")

  # S1: SKILL.md exists (implicit — we're checking it)

  # S2: Under 500 lines
  lines=$(wc -l < "$full" | tr -dc '0-9')
  if [ "${lines:-0}" -gt 500 ]; then
    echo "  ❌ $skill_name: SKILL.md exceeds 500 lines ($lines)"
    ERRORS=$((ERRORS + 1))
  fi

  # S3: Kebab-case name
  base_name=$(echo "$skill_name" | sed 's/^[0-9]*-//')
  if echo "$base_name" | grep -qE '[A-Z ]'; then
    echo "  ❌ $skill_name: Name not kebab-case"
    ERRORS=$((ERRORS + 1))
  fi

  # S5: No angle brackets in frontmatter
  in_front=$(sed -n '1,/^---$/p' "$full" | tail -n +2 | grep -c '<' 2>/dev/null | tr -dc '0-9')
  if [ "${in_front:-0}" -gt 0 ]; then
    echo "  ❌ $skill_name: Angle brackets in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  # M4b: No Template B markers
  legacy=$(grep -c '## The Physics\|## The Protocol' "$full" 2>/dev/null | tr -dc '0-9')
  if [ "${legacy:-0}" -gt 0 ]; then
    echo "  ❌ $skill_name: Template B markers found (deprecated)"
    ERRORS=$((ERRORS + 1))
  fi

  # M4: Has Usage + Validation Gate
  has_usage=$(grep -c '^## Usage\|^## When to Activate\|^## When to Use' "$full" 2>/dev/null | tr -dc '0-9')
  has_gate=$(grep -c '^## Validation Gate\|^## Quality Gate\|^## Quality Criteria' "$full" 2>/dev/null | tr -dc '0-9')
  if [ "${has_usage:-0}" -eq 0 ]; then
    echo "  ❌ $skill_name: Missing ## Usage section"
    ERRORS=$((ERRORS + 1))
  fi
  if [ "${has_gate:-0}" -eq 0 ]; then
    echo "  ❌ $skill_name: Missing ## Validation Gate section"
    ERRORS=$((ERRORS + 1))
  fi
done

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "❌ MOAT pre-commit: $ERRORS error(s) found. Fix before committing."
  exit 1
else
  echo "✅ MOAT pre-commit: All staged skills pass."
  exit 0
fi
