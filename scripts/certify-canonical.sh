#!/bin/bash
# certify-canonical.sh — Audit every canonical skill against ALL instances everywhere
# Ensures the canonical is the most robust version. Flags and auto-fixes when it's not.
# Usage: ./scripts/certify-canonical.sh [--fix] [--verbose] [REPO_ROOT]
#
# Without --fix: report only (dry run)
# With --fix: automatically replace inferior canonicals with the best version found

set -euo pipefail

AUTO_FIX=false
VERBOSE=false
REPO_ROOT=""

for arg in "$@"; do
  case "$arg" in
    --fix) AUTO_FIX=true ;;
    --verbose) VERBOSE=true ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# All locations to scan (canonical + plugins)
declare -a ALL_LOCATIONS=(
  "skills/javier-montano"
  "skills/metodologia"
  "plugins/javier-montano/sovereign-architect/skills"
  "plugins/javier-montano/pm-project-framework/skills"
  "plugins/javier-montano/scriba/skills"
  "plugins/metodologia/metodologia-discovery-framework/skills"
)

# Canonical locations (where the source of truth lives)
declare -A CANONICAL_LOCS
CANONICAL_LOCS["skills/javier-montano"]=1
CANONICAL_LOCS["skills/metodologia"]=1

TMPDIR_CERT=$(mktemp -d)
trap "rm -rf $TMPDIR_CERT" EXIT

REPORT="$REPO_ROOT/governance/certification-report.md"
ISSUES_CSV="$REPO_ROOT/governance/certification-issues.csv"

echo "=== Canonical Certification Engine ==="
echo "  Mode: $([ "$AUTO_FIX" = true ] && echo 'AUTO-FIX' || echo 'AUDIT ONLY')"
echo "  Repo: $REPO_ROOT"
echo ""

# Phase 1: Build comprehensive index of ALL skill instances
echo "Phase 1: Scanning all locations..."
INDEX="$TMPDIR_CERT/full_index.tsv"
> "$INDEX"

for loc in "${ALL_LOCATIONS[@]}"; do
  full="$REPO_ROOT/$loc"
  [ -d "$full" ] || continue

  is_canonical="false"
  [ -n "${CANONICAL_LOCS[$loc]:-}" ] && is_canonical="true"

  for skill_dir in "$full"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    # === Quality metrics === (tr -d to strip \r\n from Windows wc output)

    # 1. Line count
    lines=$(wc -l < "$skill_md" | tr -dc '0-9')
    lines=${lines:-0}

    # 2. Structure completeness (0-5)
    struct=0
    [ -d "$skill_dir/references" ] && struct=$((struct + 1))
    [ -d "$skill_dir/agents" ] && struct=$((struct + 1))
    [ -d "$skill_dir/evals" ] && struct=$((struct + 1))
    [ -d "$skill_dir/prompts" ] && struct=$((struct + 1))
    [ -d "$skill_dir/examples" ] && struct=$((struct + 1))

    # 3. Evidence tags count
    evidence=$(grep -cE '\[(HECHO|INFERENCIA|SUPUESTO|EXPLICIT|INFERRED|OPEN|PLAN|METRIC|SCHEDULE)\]' "$skill_md" 2>/dev/null | tr -dc '0-9')
    evidence=${evidence:-0}

    # 4. Has Procedure/Protocol section (15 bonus)
    has_proc=0
    grep -qE '^## (Procedure|Protocol|PROCEDURE|PROTOCOL)' "$skill_md" 2>/dev/null && has_proc=1

    # 5. Has Guardrails/Constraints section (10 bonus)
    has_guard=0
    grep -qE '^## (Guardrails|Constraints|GUARDRAILS|Hard Rules|HARD RULES)' "$skill_md" 2>/dev/null && has_guard=1

    # 6. Has frontmatter (5 bonus)
    has_front=0
    head -1 "$skill_md" 2>/dev/null | grep -q '^---' && has_front=1

    # 7. Word count (richer content)
    words=$(wc -w < "$skill_md" | tr -dc '0-9')
    words=${words:-0}

    # 8. Number of ## sections (more structured)
    sections=$(grep -c '^## ' "$skill_md" 2>/dev/null | tr -dc '0-9')
    sections=${sections:-0}

    # 9. Sub-files count (agents, references, etc.)
    subfiles=$(find "$skill_dir" -type f -not -name "SKILL.md" 2>/dev/null | wc -l | tr -dc '0-9')
    subfiles=${subfiles:-0}

    # Composite robustness score
    line_score=$((lines > 500 ? 150 : lines * 30 / 100))
    score=$((line_score + struct * 20 + evidence * 5 + has_proc * 15 + has_guard * 10 + has_front * 5 + sections * 3 + subfiles * 2))

    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
      "$skill_name" "$loc" "$is_canonical" "$score" "$lines" "$words" "$struct" \
      "$evidence" "$has_proc" "$has_guard" "$has_front" "$sections" "$subfiles" \
      >> "$INDEX"
  done
done

total_entries=$(wc -l < "$INDEX" | tr -d ' ')
echo "  Total instances scanned: $total_entries"

# Phase 2: For each skill, compare canonical vs all instances
echo ""
echo "Phase 2: Comparing canonical vs all instances..."

CERT_PASS=0
CERT_FAIL=0
CERT_UPGRADE=0
CERT_NO_CANONICAL=0
CERT_ONLY_CANONICAL=0

echo "skill_name,canonical_loc,canonical_score,canonical_lines,best_loc,best_score,best_lines,status,action" > "$ISSUES_CSV"

{
  echo "# Canonical Certification Report"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "Mode: $([ "$AUTO_FIX" = true ] && echo 'AUTO-FIX' || echo 'AUDIT ONLY')"
  echo ""
} > "$REPORT"

# Get unique skill names
cut -f1 "$INDEX" | sort -u > "$TMPDIR_CERT/all_names.txt"
unique_count=$(wc -l < "$TMPDIR_CERT/all_names.txt" | tr -d ' ')

while read -r skill_name; do
  # Get all instances of this skill
  grep "^${skill_name}	" "$INDEX" > "$TMPDIR_CERT/instances.tsv" 2>/dev/null || continue

  # Find canonical instance(s)
  canonical_line=$(awk -F'\t' '$3 == "true"' "$TMPDIR_CERT/instances.tsv" | sort -t$'\t' -k4 -rn | head -1)

  # Find best instance overall
  best_line=$(sort -t$'\t' -k4 -rn "$TMPDIR_CERT/instances.tsv" | head -1)

  if [ -z "$canonical_line" ]; then
    # No canonical version exists (plugin-only skill)
    CERT_NO_CANONICAL=$((CERT_NO_CANONICAL + 1))
    continue
  fi

  c_loc=$(echo "$canonical_line" | cut -f2)
  c_score=$(echo "$canonical_line" | cut -f4)
  c_lines=$(echo "$canonical_line" | cut -f5)

  b_loc=$(echo "$best_line" | cut -f2)
  b_score=$(echo "$best_line" | cut -f4)
  b_lines=$(echo "$best_line" | cut -f5)

  instance_count=$(wc -l < "$TMPDIR_CERT/instances.tsv" | tr -d ' ')

  if [ "$instance_count" -eq 1 ]; then
    # Only one instance and it's canonical — auto pass
    CERT_ONLY_CANONICAL=$((CERT_ONLY_CANONICAL + 1))
    echo "$skill_name,$c_loc,$c_score,$c_lines,$c_loc,$c_score,$c_lines,PASS_ONLY,none" >> "$ISSUES_CSV"
    continue
  fi

  # Compare canonical vs best
  if [ "$c_score" -ge "$b_score" ]; then
    # Canonical IS the best or tied — PASS
    CERT_PASS=$((CERT_PASS + 1))
    [ "$VERBOSE" = true ] && echo "  PASS: $skill_name (canonical=$c_score, best=$b_score)"
    echo "$skill_name,$c_loc,$c_score,$c_lines,$b_loc,$b_score,$b_lines,PASS,none" >> "$ISSUES_CSV"
  else
    # Canonical is INFERIOR — FAIL
    CERT_FAIL=$((CERT_FAIL + 1))
    delta=$((b_score - c_score))
    echo "  FAIL: $skill_name — canonical($c_loc: score=$c_score, ${c_lines}L) < best($b_loc: score=$b_score, ${b_lines}L) delta=$delta"

    echo "$skill_name,$c_loc,$c_score,$c_lines,$b_loc,$b_score,$b_lines,FAIL,upgrade" >> "$ISSUES_CSV"

    if [ "$AUTO_FIX" = true ]; then
      # Replace canonical with the better version
      src_dir="$REPO_ROOT/$b_loc/$skill_name"
      dst_dir="$REPO_ROOT/$c_loc/$skill_name"

      if [ -d "$src_dir" ] && [ -f "$src_dir/SKILL.md" ]; then
        # Backup canonical
        cp -r "$dst_dir" "$TMPDIR_CERT/backup_${skill_name}" 2>/dev/null || true
        # Copy better version
        cp -r "$src_dir"/* "$dst_dir/" 2>/dev/null || true
        CERT_UPGRADE=$((CERT_UPGRADE + 1))
        echo "    UPGRADED: $skill_name ($c_loc ← $b_loc, score $c_score → $b_score)"
      fi
    fi
  fi
done < "$TMPDIR_CERT/all_names.txt"

# Phase 3: Generate report
{
  echo "## Summary"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| Total unique skills | $unique_count |"
  echo "| Total instances scanned | $total_entries |"
  echo "| Canonical = best (PASS) | $CERT_PASS |"
  echo "| Only one instance (auto-pass) | $CERT_ONLY_CANONICAL |"
  echo "| Canonical inferior (FAIL) | $CERT_FAIL |"
  echo "| No canonical (plugin-only) | $CERT_NO_CANONICAL |"
  [ "$AUTO_FIX" = true ] && echo "| Auto-upgraded | $CERT_UPGRADE |"
  echo ""

  if [ "$CERT_FAIL" -gt 0 ]; then
    echo "## Failed Certifications (canonical is NOT the best)"
    echo ""
    echo "| Skill | Canonical (loc/score/lines) | Best (loc/score/lines) | Delta |"
    echo "|-------|---------------------------|----------------------|-------|"
    awk -F',' '$8 == "FAIL" {printf "| %s | %s / %s / %s | %s / %s / %s | +%d |\n", $1, $2, $3, $4, $5, $6, $7, $6-$3}' "$ISSUES_CSV"
    echo ""
  fi

  if [ "$CERT_FAIL" -eq 0 ]; then
    echo "## CERTIFICATION: PASSED"
    echo ""
    echo "All canonical skills are the most robust version available."
  else
    if [ "$AUTO_FIX" = true ]; then
      echo "## CERTIFICATION: FIXED"
      echo ""
      echo "$CERT_UPGRADE canonical skills were auto-upgraded to superior versions."
    else
      echo "## CERTIFICATION: FAILED"
      echo ""
      echo "$CERT_FAIL canonical skills have superior versions elsewhere."
      echo "Run with --fix to auto-upgrade."
    fi
  fi
} >> "$REPORT"

echo ""
echo "=== Certification Complete ==="
echo "  PASS (canonical = best): $CERT_PASS"
echo "  PASS (only instance):    $CERT_ONLY_CANONICAL"
echo "  FAIL (inferior):         $CERT_FAIL"
echo "  No canonical:            $CERT_NO_CANONICAL"
[ "$AUTO_FIX" = true ] && echo "  Auto-upgraded:           $CERT_UPGRADE"
echo ""
echo "  Report: $REPORT"
echo "  CSV: $ISSUES_CSV"
