#!/bin/bash
# batch-evals-scaffold.sh — Scaffold evals/evals.json for skills missing them
# Generates 7 test prompts per skill derived from frontmatter description and triggers
# Includes false_positive + edge_case evals for M2 compliance
# Usage: ./scripts/batch-evals-scaffold.sh [--all] [--skill=NAME] [REPO_ROOT]

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

CREATED=0
TOTAL=0
SKIPPED=0
ENRICHED=0

echo "=== Batch Evals Scaffold ==="
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

    evals_dir="$skill_dir/evals"
    evals_json="$evals_dir/evals.json"

    # If evals.json exists with >= 5 entries + false_positive + edge_case, skip
    if [ -f "$evals_json" ]; then
      eval_count=$(grep -c '"id"' "$evals_json" 2>/dev/null | tr -dc '0-9')
      eval_count=${eval_count:-0}
      has_fp=$(grep -ci 'false.positive\|false_positive\|should-not\|negative' "$evals_json" 2>/dev/null | tr -dc '0-9')
      has_fp=${has_fp:-0}
      has_edge=$(grep -ci 'edge.case\|edge_case\|boundary\|corner' "$evals_json" 2>/dev/null | tr -dc '0-9')
      has_edge=${has_edge:-0}

      if [ "$eval_count" -ge 5 ] && [ "$has_fp" -gt 0 ] && [ "$has_edge" -gt 0 ]; then
        SKIPPED=$((SKIPPED + 1))
        continue
      fi
    fi

    # Generate evals.json using python
    python -c "
import re, sys, os, json

skill_path = sys.argv[1]
skill_name = sys.argv[2]
evals_json_path = sys.argv[3]
evals_dir = os.path.dirname(evals_json_path)

base_name = re.sub(r'^\d+-', '', skill_name)
readable_name = base_name.replace('-', ' ')

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract description from frontmatter
desc_match = re.search(r'description:\s*[>|]?\s*\n?\s*(.*?)(?:\n\w|\n---)', content, re.DOTALL)
if desc_match:
    description = desc_match.group(1).strip()
    description = re.sub(r'\s+', ' ', description)[:200]
else:
    # Try single-line description
    desc_match = re.search(r'description:\s*(.+)', content)
    description = desc_match.group(1).strip() if desc_match else f'{readable_name} skill'

# Extract trigger words from description
trigger_words = []
trigger_patterns = [
    r'\"([^\"]+)\"',  # quoted phrases
    r'activate[sd]?\s+(?:when|for)\s+(.*?)(?:\.|,|\n)',
    r'used?\s+(?:when|for)\s+(.*?)(?:\.|,|\n)',
]
for pat in trigger_patterns:
    matches = re.findall(pat, description, re.IGNORECASE)
    trigger_words.extend(matches[:3])

if not trigger_words:
    trigger_words = [readable_name, f'run {readable_name}', f'analyze with {readable_name}']

# Check if existing evals.json needs enrichment
existing_evals = []
if os.path.exists(evals_json_path):
    try:
        with open(evals_json_path, 'r', encoding='utf-8') as f:
            existing_evals = json.load(f)
    except:
        existing_evals = []

existing_ids = {e.get('id', '') for e in existing_evals}

# Generate evals
new_evals = list(existing_evals)  # preserve existing

# Happy path evals
happy_templates = [
    {
        'id': f'{base_name}-happy-path',
        'type': 'happy_path',
        'input': f'Run {readable_name} on this project',
        'expected_behavior': f'Skill activates and produces the expected {readable_name} output following the defined process',
        'tags': ['basic', 'activation']
    },
    {
        'id': f'{base_name}-explicit-trigger',
        'type': 'happy_path',
        'input': trigger_words[0] if trigger_words else f'{readable_name}',
        'expected_behavior': f'Skill recognizes the trigger phrase and executes the {readable_name} workflow',
        'tags': ['trigger', 'recognition']
    },
    {
        'id': f'{base_name}-with-context',
        'type': 'happy_path',
        'input': f'Apply {readable_name} to analyze the current codebase with detailed output',
        'expected_behavior': f'Skill produces comprehensive {readable_name} analysis with evidence-tagged findings and actionable recommendations',
        'tags': ['detailed', 'comprehensive']
    },
    {
        'id': f'{base_name}-minimal-input',
        'type': 'happy_path',
        'input': f'Quick {readable_name}',
        'expected_behavior': f'Skill activates even with minimal input, applies reasonable defaults, produces concise output',
        'tags': ['minimal', 'defaults']
    },
]

# False positive eval (M2 requirement)
false_positive = {
    'id': f'{base_name}-false-positive',
    'type': 'false_positive',
    'input': f'What is the weather forecast for tomorrow?',
    'expected_behavior': f'Skill should NOT activate — this input has no relation to {readable_name}. The system should route to a different skill or respond that this is outside scope.',
    'tags': ['false_positive', 'should-not-activate']
}

# Edge case evals (M2b requirement)
edge_cases = [
    {
        'id': f'{base_name}-edge-empty-input',
        'type': 'edge_case',
        'input': f'Run {readable_name} but I have no files or documentation yet',
        'expected_behavior': f'Skill handles gracefully — requests minimum viable input or produces a gap analysis showing what is needed before {readable_name} can proceed',
        'tags': ['edge_case', 'empty-input', 'boundary']
    },
    {
        'id': f'{base_name}-edge-conflicting',
        'type': 'edge_case',
        'input': f'Apply {readable_name} but the requirements contradict each other — requirement A says X and requirement B says not-X',
        'expected_behavior': f'Skill detects contradiction, flags it explicitly with [OPEN] evidence tag, and proposes resolution options rather than proceeding with assumptions',
        'tags': ['edge_case', 'conflict', 'corner']
    },
]

# Add only evals not already present
for eval_item in happy_templates + [false_positive] + edge_cases:
    if eval_item['id'] not in existing_ids:
        new_evals.append(eval_item)

# Ensure we have at least 5
if len(new_evals) < 5:
    extra = {
        'id': f'{base_name}-integration',
        'type': 'happy_path',
        'input': f'Use {readable_name} as part of a larger analysis pipeline',
        'expected_behavior': f'Skill integrates cleanly with pipeline context, accepts upstream input and produces output compatible with downstream consumption',
        'tags': ['integration', 'pipeline']
    }
    if extra['id'] not in existing_ids:
        new_evals.append(extra)

# Write evals.json
os.makedirs(evals_dir, exist_ok=True)
with open(evals_json_path, 'w', encoding='utf-8') as f:
    json.dump(new_evals, f, indent=2, ensure_ascii=False)

action = 'ENRICHED' if existing_evals else 'CREATED'
print(f'  {action}: {skill_name} ({len(new_evals)} evals)')
sys.exit(0 if not existing_evals else 2)
" "$skill_md" "$skill_name" "$evals_json" 2>/dev/null

    exit_code=$?
    if [ $exit_code -eq 0 ]; then
      CREATED=$((CREATED + 1))
    elif [ $exit_code -eq 2 ]; then
      ENRICHED=$((ENRICHED + 1))
    fi
  done
done

echo ""
echo "=== Evals Scaffold Complete ==="
echo "  Total skills: $TOTAL"
echo "  Created new: $CREATED"
echo "  Enriched existing: $ENRICHED"
echo "  Skipped (already compliant): $SKIPPED"
