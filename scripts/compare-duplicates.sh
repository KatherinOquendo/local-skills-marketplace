#!/bin/bash
# compare-duplicates.sh — Analyze each duplicated skill, recommend canonical version
# Usage: ./scripts/compare-duplicates.sh [REPO_ROOT]

set -euo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

# Skill locations
declare -A LOCATIONS
LOCATIONS[atomic]="skills/javier-montano"
LOCATIONS[pm]="plugins/javier-montano/pm-project-framework/skills"
LOCATIONS[sa]="plugins/javier-montano/sovereign-architect/skills"
LOCATIONS[scriba]="plugins/javier-montano/scriba/skills"
LOCATIONS[mdf]="plugins/metodologia/metodologia-discovery-framework/skills"

# Location priority labels (for reporting)
declare -A LOC_LABELS
LOC_LABELS[atomic]="Atomic (skills/javier-montano)"
LOC_LABELS[sa]="Sovereign Architect"
LOC_LABELS[pm]="PM Framework (APEX)"
LOC_LABELS[mdf]="MetodologIA Discovery"
LOC_LABELS[scriba]="Scriba"

# Owner mapping
declare -A LOC_OWNER
LOC_OWNER[atomic]="javier-montano"
LOC_OWNER[sa]="javier-montano"
LOC_OWNER[pm]="javier-montano"
LOC_OWNER[mdf]="metodologia"
LOC_OWNER[scriba]="javier-montano"

# Output paths
GOVERNANCE_DIR="$REPO_ROOT/governance"
mkdir -p "$GOVERNANCE_DIR"

CSV_OUT="$GOVERNANCE_DIR/canonical-decisions.csv"
REPORT_OUT="$GOVERNANCE_DIR/canonical-decisions-report.md"

TMPDIR_CMP=$(mktemp -d)
trap "rm -rf $TMPDIR_CMP" EXIT

echo "=== Duplicate Skill Comparison Engine ==="
echo ""

# Collect all duplicates
ALL_SKILLS="$TMPDIR_CMP/all_skills.tsv"
> "$ALL_SKILLS"

for loc_key in "${!LOCATIONS[@]}"; do
  loc_path="${LOCATIONS[$loc_key]}"
  full_path="$REPO_ROOT/$loc_path"
  [ -d "$full_path" ] || continue

  for skill_dir in "$full_path"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    line_count=$(wc -l < "$skill_md" | tr -d ' ')

    # Structure score
    score=0
    [ -d "$skill_dir/references" ] && score=$((score + 1))
    [ -d "$skill_dir/agents" ] && score=$((score + 1))
    [ -d "$skill_dir/evals" ] && score=$((score + 1))
    [ -d "$skill_dir/prompts" ] && score=$((score + 1))
    [ -d "$skill_dir/examples" ] && score=$((score + 1))

    # Check for evidence tags in SKILL.md
    evidence_tags=$(grep -cE '\[(HECHO|INFERENCIA|SUPUESTO|EXPLICIT|INFERRED|OPEN)\]' "$skill_md" 2>/dev/null || echo 0)

    # Check for ## Procedure section (MOAT indicator)
    has_procedure="false"
    grep -q "## Procedure\|## Protocol\|## PROCEDURE" "$skill_md" 2>/dev/null && has_procedure="true"

    # Last git modification date
    last_modified=$(git -C "$REPO_ROOT" log -1 --format="%ai" -- "$loc_path/$skill_name/SKILL.md" 2>/dev/null | cut -d' ' -f1 || echo "unknown")

    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
      "$loc_key" "$skill_name" "$line_count" "$score" "$evidence_tags" "$has_procedure" "$last_modified" \
      >> "$ALL_SKILLS"
  done
done

# Find duplicates
DUPLICATES="$TMPDIR_CMP/duplicates.txt"
cut -f2 "$ALL_SKILLS" | sort | uniq -c | awk '$1 > 1 {print $2}' | sort > "$DUPLICATES"

dup_count=$(wc -l < "$DUPLICATES" | tr -d ' ')
echo "Analyzing $dup_count duplicated skills..."
echo ""

# Generate CSV header
echo "skill_name,recommended_source,recommended_owner,canonical_path,lines,completeness,evidence_tags,has_procedure,last_modified,reason,other_locations" > "$CSV_OUT"

# Generate report header
{
  echo "# Canonical Version Decisions"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "Total duplicated skills: $dup_count"
  echo ""
  echo "## Decision Summary"
  echo ""
  echo "| # | Skill | Recommended Source | Lines | Score | Reason |"
  echo "|---|-------|-------------------|-------|-------|--------|"
} > "$REPORT_OUT"

decision_num=0

while read -r dup_name; do
  decision_num=$((decision_num + 1))

  # Get all instances of this skill
  instances="$TMPDIR_CMP/instances.tsv"
  grep "	${dup_name}	" "$ALL_SKILLS" > "$instances"

  # Score each instance: lines * 0.3 + completeness * 20 + evidence * 5 + procedure * 15
  best_loc=""
  best_score=-1
  best_lines=0
  best_comp=0
  best_evidence=0
  best_procedure="false"
  best_modified=""
  all_locs=""

  while IFS=$'\t' read -r loc_key sname lines comp evtags hproc modified; do
    # Composite score
    proc_bonus=0
    [ "$hproc" = "true" ] && proc_bonus=15

    # Normalize: prefer more lines (deeper content) but cap at 500
    line_score=$((lines > 500 ? 150 : lines * 30 / 100))
    comp_score=$((comp * 20))
    ev_score=$((evtags * 5))

    total=$((line_score + comp_score + ev_score + proc_bonus))

    # Track all locations
    if [ -n "$all_locs" ]; then
      all_locs="$all_locs;$loc_key($lines lines)"
    else
      all_locs="$loc_key($lines lines)"
    fi

    if [ "$total" -gt "$best_score" ]; then
      best_score=$total
      best_loc=$loc_key
      best_lines=$lines
      best_comp=$comp
      best_evidence=$evtags
      best_procedure=$hproc
      best_modified=$modified
    fi
  done < "$instances"

  # Determine canonical owner and path
  owner="${LOC_OWNER[$best_loc]}"
  canonical_path="skills/$owner/$dup_name"

  # Build reason
  reason="Highest composite score ($best_score): ${best_lines} lines, ${best_comp}/5 completeness"
  [ "$best_evidence" -gt 0 ] && reason="$reason, $best_evidence evidence tags"
  [ "$best_procedure" = "true" ] && reason="$reason, has Procedure section"

  # Determine other locations (not the recommended one)
  other_locs=$(echo "$all_locs" | tr ';' '\n' | grep -v "^${best_loc}" | tr '\n' ';' | sed 's/;$//')

  # Write CSV row
  echo "$dup_name,$best_loc,$owner,$canonical_path,$best_lines,$best_comp,$best_evidence,$best_procedure,$best_modified,\"$reason\",\"$other_locs\"" >> "$CSV_OUT"

  # Write report row
  loc_label="${LOC_LABELS[$best_loc]}"
  echo "| $decision_num | $dup_name | **$best_loc** | $best_lines | $best_comp/5 | $reason |" >> "$REPORT_OUT"

done < "$DUPLICATES"

# Add detail section to report
{
  echo ""
  echo "## Detailed Analysis"
  echo ""

  while read -r dup_name; do
    echo "### $dup_name"
    echo ""
    echo "| Location | Lines | Completeness | Evidence Tags | Procedure | Last Modified |"
    echo "|----------|-------|-------------|--------------|-----------|---------------|"

    grep "	${dup_name}	" "$ALL_SKILLS" | while IFS=$'\t' read -r loc_key sname lines comp evtags hproc modified; do
      recommended=""
      # Check if this is the recommended one by finding it in CSV
      if grep -q "^${dup_name},${loc_key}," "$CSV_OUT"; then
        recommended=" **RECOMMENDED**"
      fi
      echo "| ${loc_key}${recommended} | $lines | $comp/5 | $evtags | $hproc | $modified |"
    done
    echo ""
  done < "$DUPLICATES"

  echo "## Statistics"
  echo ""
  echo "| Source Recommended | Count |"
  echo "|-------------------|-------|"
  for loc_key in atomic sa pm mdf scriba; do
    rec_count=$(awk -F',' -v lk="$loc_key" '$2 == lk' "$CSV_OUT" | wc -l | tr -d ' ')
    [ "$rec_count" -gt 0 ] && echo "| ${LOC_LABELS[$loc_key]:-$loc_key} | $rec_count |"
  done
  echo ""

  echo "## Owner Distribution"
  echo ""
  echo "| Owner | Count |"
  echo "|-------|-------|"
  for owner in javier-montano metodologia; do
    owner_count=$(awk -F',' -v o="$owner" '$3 == o' "$CSV_OUT" | wc -l | tr -d ' ')
    [ "$owner_count" -gt 0 ] && echo "| $owner | $owner_count |"
  done

} >> "$REPORT_OUT"

echo ""
echo "=== Comparison Complete ==="
echo "  CSV: $CSV_OUT"
echo "  Report: $REPORT_OUT"
echo ""
echo "Source recommendation distribution:"
for loc_key in atomic sa pm mdf scriba; do
  rec_count=$(awk -F',' -v lk="$loc_key" '$2 == lk' "$CSV_OUT" | wc -l | tr -d ' ')
  [ "$rec_count" -gt 0 ] && echo "  $loc_key: $rec_count skills"
done
