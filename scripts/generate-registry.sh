#!/bin/bash
# generate-registry.sh — Scan all skill locations and produce REGISTRY.json + REGISTRY-REPORT.md
# Usage: ./scripts/generate-registry.sh [REPO_ROOT]

set -euo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

# Skill locations to scan
declare -A LOCATIONS
LOCATIONS[atomic]="skills/javier-montano"
LOCATIONS[pm]="plugins/javier-montano/pm-project-framework/skills"
LOCATIONS[sa]="plugins/javier-montano/sovereign-architect/skills"
LOCATIONS[scriba]="plugins/javier-montano/scriba/skills"
LOCATIONS[mdf]="plugins/metodologia/metodologia-discovery-framework/skills"

REGISTRY_JSON="$REPO_ROOT/skills/javier-montano/REGISTRY.json"
REGISTRY_REPORT="$REPO_ROOT/skills/javier-montano/REGISTRY-REPORT.md"

# Temp files
TMPDIR_REG=$(mktemp -d)
ALL_SKILLS="$TMPDIR_REG/all_skills.tsv"
DUPLICATES="$TMPDIR_REG/duplicates.txt"

trap "rm -rf $TMPDIR_REG" EXIT

echo "=== JM Labs Skill Registry Generator ==="
echo "Repo root: $REPO_ROOT"
echo ""

# Phase 1: Scan all locations
> "$ALL_SKILLS"

for loc_key in "${!LOCATIONS[@]}"; do
  loc_path="${LOCATIONS[$loc_key]}"
  full_path="$REPO_ROOT/$loc_path"

  if [ ! -d "$full_path" ]; then
    echo "WARN: $loc_path does not exist, skipping"
    continue
  fi

  echo "Scanning $loc_key ($loc_path)..."

  for skill_dir in "$full_path"/*/; do
    [ -d "$skill_dir" ] || continue

    skill_name=$(basename "$skill_dir")

    # Skip hidden dirs and non-skill dirs
    [[ "$skill_name" == .* ]] && continue
    [[ "$skill_name" == "__MACOSX" ]] && continue

    skill_md="$skill_dir/SKILL.md"
    if [ ! -f "$skill_md" ]; then
      continue
    fi

    # Extract metadata
    line_count=$(wc -l < "$skill_md" 2>/dev/null || echo 0)
    line_count=$(echo "$line_count" | tr -d ' ')

    has_references="false"
    has_agents="false"
    has_evals="false"
    has_prompts="false"
    has_examples="false"

    [ -d "$skill_dir/references" ] && has_references="true"
    [ -d "$skill_dir/agents" ] && has_agents="true"
    [ -d "$skill_dir/evals" ] && has_evals="true"
    [ -d "$skill_dir/prompts" ] && has_prompts="true"
    [ -d "$skill_dir/examples" ] && has_examples="true"

    # Count subdirs for completeness score (0-5)
    completeness=0
    [ "$has_references" = "true" ] && completeness=$((completeness + 1))
    [ "$has_agents" = "true" ] && completeness=$((completeness + 1))
    [ "$has_evals" = "true" ] && completeness=$((completeness + 1))
    [ "$has_prompts" = "true" ] && completeness=$((completeness + 1))
    [ "$has_examples" = "true" ] && completeness=$((completeness + 1))

    # Output: location_key \t skill_name \t line_count \t completeness \t refs \t agents \t evals \t prompts \t examples \t relative_path
    rel_path="$loc_path/$skill_name"
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
      "$loc_key" "$skill_name" "$line_count" "$completeness" \
      "$has_references" "$has_agents" "$has_evals" "$has_prompts" "$has_examples" \
      "$rel_path" >> "$ALL_SKILLS"
  done
done

# Sort by skill name
sort -t$'\t' -k2,2 "$ALL_SKILLS" > "$ALL_SKILLS.sorted"
mv "$ALL_SKILLS.sorted" "$ALL_SKILLS"

total_entries=$(wc -l < "$ALL_SKILLS" | tr -d ' ')
unique_names=$(cut -f2 "$ALL_SKILLS" | sort -u | wc -l | tr -d ' ')

echo ""
echo "Total skill entries: $total_entries"
echo "Unique skill names: $unique_names"

# Phase 2: Find duplicates (skills appearing in 2+ locations)
cut -f2 "$ALL_SKILLS" | sort | uniq -c | sort -rn | awk '$1 > 1 {print $2}' > "$DUPLICATES"
dup_count=$(wc -l < "$DUPLICATES" | tr -d ' ')
echo "Duplicated skill names: $dup_count"

# Phase 3: Generate REGISTRY.json
echo ""
echo "Generating $REGISTRY_JSON ..."

{
  echo "{"
  echo '  "version": "1.0.0",'
  echo "  \"generated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"total_entries\": $total_entries,"
  echo "  \"unique_skills\": $unique_names,"
  echo "  \"duplicated_skills\": $dup_count,"
  echo '  "locations": {'

  first_loc=true
  for loc_key in "${!LOCATIONS[@]}"; do
    loc_count=$(grep -c "^${loc_key}	" "$ALL_SKILLS" || echo 0)
    if [ "$first_loc" = true ]; then first_loc=false; else echo ","; fi
    printf '    "%s": { "path": "%s", "count": %s }' "$loc_key" "${LOCATIONS[$loc_key]}" "$loc_count"
  done
  echo ""
  echo "  },"

  echo '  "skills": {'

  prev_name=""
  first_skill=true

  while IFS=$'\t' read -r loc_key skill_name line_count completeness has_refs has_agents has_evals has_prompts has_examples rel_path; do
    if [ "$skill_name" != "$prev_name" ]; then
      # Close previous skill entry
      if [ "$prev_name" != "" ]; then
        echo ""
        echo "      ]"
        echo "    },"
      fi

      # Check if duplicate
      is_dup="false"
      grep -qx "$skill_name" "$DUPLICATES" 2>/dev/null && is_dup="true"

      if [ "$first_skill" = true ]; then first_skill=false; fi
      echo "    \"$skill_name\": {"
      echo "      \"is_duplicate\": $is_dup,"
      echo "      \"instances\": ["
      prev_name="$skill_name"
      first_instance=true
    else
      first_instance=false
    fi

    if [ "$first_instance" != "true" ]; then
      echo ","
    fi

    printf '        { "location": "%s", "path": "%s", "lines": %s, "completeness": %s, "structure": { "references": %s, "agents": %s, "evals": %s, "prompts": %s, "examples": %s } }' \
      "$loc_key" "$rel_path" "$line_count" "$completeness" \
      "$has_refs" "$has_agents" "$has_evals" "$has_prompts" "$has_examples"
  done < "$ALL_SKILLS"

  # Close last entry
  if [ "$prev_name" != "" ]; then
    echo ""
    echo "      ]"
    echo "    }"
  fi

  echo "  }"
  echo "}"
} > "$REGISTRY_JSON"

# Phase 4: Generate REGISTRY-REPORT.md
echo "Generating $REGISTRY_REPORT ..."

{
  echo "# JM Labs Skill Registry Report"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "## Summary"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| Total skill entries | $total_entries |"
  echo "| Unique skill names | $unique_names |"
  echo "| Duplicated skill names | $dup_count |"
  echo ""

  echo "## Skills by Location"
  echo ""
  echo "| Location | Key | Count |"
  echo "|----------|-----|-------|"
  for loc_key in atomic sa pm mdf scriba; do
    loc_count=$(grep -c "^${loc_key}	" "$ALL_SKILLS" || echo 0)
    echo "| ${LOCATIONS[$loc_key]} | $loc_key | $loc_count |"
  done
  echo ""

  echo "## Duplicated Skills ($dup_count)"
  echo ""
  if [ "$dup_count" -gt 0 ]; then
    echo "| Skill Name | Locations | Lines (per location) | Best Completeness |"
    echo "|------------|-----------|---------------------|-------------------|"

    while read -r dup_name; do
      locs=$(grep "	${dup_name}	" "$ALL_SKILLS" | cut -f1 | tr '\n' ',' | sed 's/,$//')
      lines=$(grep "	${dup_name}	" "$ALL_SKILLS" | cut -f3 | tr '\n' '/' | sed 's/\/$//')
      best_comp=$(grep "	${dup_name}	" "$ALL_SKILLS" | cut -f4 | sort -rn | head -1)
      echo "| $dup_name | $locs | $lines | $best_comp/5 |"
    done < "$DUPLICATES"
  else
    echo "No duplicates found."
  fi
  echo ""

  echo "## Unique Skills (appear in only one location)"
  echo ""
  echo "| Location | Count | Skills |"
  echo "|----------|-------|--------|"
  for loc_key in atomic sa pm mdf scriba; do
    unique_in_loc=""
    loc_skill_count=0
    while IFS=$'\t' read -r lk sn rest; do
      if [ "$lk" = "$loc_key" ]; then
        # Check if this skill is NOT in duplicates
        if ! grep -qx "$sn" "$DUPLICATES" 2>/dev/null; then
          loc_skill_count=$((loc_skill_count + 1))
        fi
      fi
    done < "$ALL_SKILLS"
    echo "| $loc_key | $loc_skill_count | *(see REGISTRY.json for full list)* |"
  done
  echo ""

  echo "## Completeness Distribution"
  echo ""
  echo "| Score | Count | Percentage |"
  echo "|-------|-------|------------|"
  for score in 0 1 2 3 4 5; do
    score_count=$(awk -F'\t' -v s="$score" '$4 == s' "$ALL_SKILLS" | wc -l | tr -d ' ')
    if [ "$total_entries" -gt 0 ]; then
      pct=$((score_count * 100 / total_entries))
    else
      pct=0
    fi
    echo "| $score/5 | $score_count | ${pct}% |"
  done
  echo ""

  echo "## Next Steps"
  echo ""
  echo "1. Run \`scripts/compare-duplicates.sh\` to analyze each duplicate pair"
  echo "2. Review \`governance/canonical-decisions.csv\` for canonical version selection"
  echo "3. Approve and proceed to consolidation (Phase 3)"

} > "$REGISTRY_REPORT"

echo ""
echo "=== Registry Generation Complete ==="
echo "  JSON: $REGISTRY_JSON"
echo "  Report: $REGISTRY_REPORT"
echo ""
echo "Duplicated skills ($dup_count):"
cat "$DUPLICATES" 2>/dev/null || echo "(none)"
