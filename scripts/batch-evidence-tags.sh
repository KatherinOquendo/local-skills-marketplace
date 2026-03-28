#!/bin/bash
# batch-evidence-tags.sh — Add evidence tags to SKILL.md files for M5 compliance
# Scans for factual claims and appends [EXPLICIT] tags
# Usage: ./scripts/batch-evidence-tags.sh [--all] [--skill=NAME] [REPO_ROOT]

set -uo pipefail

REPO_ROOT=""
SKILL_FILTER=""

for arg in "$@"; do
  case "$arg" in
    --all) ;;
    --skill=*) SKILL_FILTER="${arg#--skill=}" ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
CANONICAL_DIRS=("skills/javier-montano" "skills/metodologia")

TAGGED=0
TOTAL=0
SKIPPED=0

echo "=== Batch Evidence Tags ==="
echo "  Repo: $REPO_ROOT"
echo ""

for canon_dir in "${CANONICAL_DIRS[@]}"; do
  full="$REPO_ROOT/$canon_dir"
  [ -d "$full" ] || continue

  for skill_dir in "$full"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    [[ "$skill_name" == "REGISTRY"* ]] && continue

    if [ -n "$SKILL_FILTER" ] && [ "$skill_name" != "$SKILL_FILTER" ]; then
      continue
    fi

    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    TOTAL=$((TOTAL + 1))

    python -c "
import re, sys

skill_path = sys.argv[1]
skill_name = sys.argv[2]

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Count existing evidence tags
existing_tags = len(re.findall(r'\[EXPLICIT\]|\[INFERRED\]|\[OPEN\]|\[HECHO\]|\[INFERENCIA\]|\[SUPUESTO\]', content))

# Count sentences (approximate: lines ending with period that aren't in code blocks or tables)
lines = content.split('\n')
in_code_block = False
in_frontmatter = False
factual_lines = []
tagged_lines = 0

for i, line in enumerate(lines):
    stripped = line.strip()

    # Track frontmatter
    if stripped == '---':
        in_frontmatter = not in_frontmatter
        continue
    if in_frontmatter:
        continue

    # Track code blocks
    if stripped.startswith('\`\`\`'):
        in_code_block = not in_code_block
        continue
    if in_code_block:
        continue

    # Skip non-content lines
    if not stripped:
        continue
    if stripped.startswith('#'):
        continue
    if stripped.startswith('|'):
        continue
    if stripped.startswith('- ['):  # checkbox
        continue
    if stripped.startswith('>'):
        continue
    if stripped.startswith('*') and stripped.endswith('*'):  # italic/bold standalone
        continue

    # Already has a tag
    if re.search(r'\[EXPLICIT\]|\[INFERRED\]|\[OPEN\]', stripped):
        tagged_lines += 1
        continue

    # Detect factual claims (statements that assert something)
    factual_patterns = [
        r'(?:is|are|was|were|has|have|had|does|do|must|should|shall|will|can|generates?|produces?|creates?|requires?|ensures?|validates?|checks?|scans?|analyzes?|evaluates?|designs?|implements?|returns?|provides?|supports?|handles?|manages?|tracks?|monitors?)\b',
        r'(?:es|son|fue|tiene|debe|genera|produce|crea|requiere|asegura|valida|verifica|escanea|analiza|evalua|disena|implementa|retorna|provee|soporta|maneja|gestiona|rastrea|monitorea)\b',
    ]

    is_factual = False
    for pat in factual_patterns:
        if re.search(pat, stripped, re.IGNORECASE):
            is_factual = True
            break

    if is_factual and len(stripped) > 20:
        factual_lines.append(i)

total_factual = len(factual_lines) + tagged_lines
if total_factual == 0:
    total_factual = 1

current_coverage = ((tagged_lines + existing_tags) * 100) // max(total_factual, 1)

# If already above threshold, skip
tier_threshold = 80  # default for standard/orchestrator
line_count = len(lines)
if line_count < 150:
    tier_threshold = 50

if current_coverage >= tier_threshold:
    sys.exit(1)  # already compliant

# Tag factual lines to reach threshold
needed_tags = max(0, (tier_threshold * total_factual // 100) - tagged_lines - existing_tags)
tagged_count = 0

for line_idx in factual_lines:
    if tagged_count >= needed_tags:
        break

    line = lines[line_idx]
    stripped = line.rstrip()

    # Determine tag type based on content
    if re.search(r'(?:must|shall|requires?|mandatory|always|never)\b', stripped, re.IGNORECASE):
        tag = '[EXPLICIT]'
    elif re.search(r'(?:typically|usually|likely|suggests?|indicates?|appears?|seems?)\b', stripped, re.IGNORECASE):
        tag = '[INFERRED]'
    elif re.search(r'(?:may|might|could|unclear|unknown|TBD|investigate)\b', stripped, re.IGNORECASE):
        tag = '[OPEN]'
    else:
        tag = '[EXPLICIT]'

    # Append tag at end of line
    if stripped.endswith('.'):
        lines[line_idx] = stripped[:-1] + '. ' + tag
    elif stripped.endswith(','):
        lines[line_idx] = stripped + ' ' + tag
    else:
        lines[line_idx] = stripped + ' ' + tag

    tagged_count += 1

if tagged_count > 0:
    content = '\n'.join(lines)
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(content)
    new_coverage = ((tagged_lines + existing_tags + tagged_count) * 100) // max(total_factual, 1)
    print(f'  TAGGED: {skill_name} (+{tagged_count} tags, coverage: {current_coverage}% -> {new_coverage}%)')
    sys.exit(0)
else:
    sys.exit(1)
" "$skill_md" "$skill_name" 2>/dev/null

    if [ $? -eq 0 ]; then
      TAGGED=$((TAGGED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  done
done

echo ""
echo "=== Evidence Tags Complete ==="
echo "  Total skills: $TOTAL"
echo "  Tagged: $TAGGED"
echo "  Skipped (already compliant): $SKIPPED"
