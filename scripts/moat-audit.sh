#!/bin/bash
# moat-audit.sh — Full MOAT compliance audit for all canonical skills
# Extends certify-canonical.sh with MOAT-specific checks (M1-M5)
# Usage: ./scripts/moat-audit.sh [--all] [--changed-only] [--skill=NAME] [REPO_ROOT]
#
# Outputs:
#   governance/moat-dashboard.md  — Human-readable progress dashboard
#   governance/moat-status.csv    — Machine-readable per-skill status

set -uo pipefail
# Note: NOT using set -e because grep -c returns exit 1 when 0 matches,
# which would abort the script. We handle errors explicitly.

MODE="all"
SKILL_FILTER=""
REPO_ROOT=""

for arg in "$@"; do
  case "$arg" in
    --all) MODE="all" ;;
    --changed-only) MODE="changed" ;;
    --skill=*) SKILL_FILTER="${arg#--skill=}" ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# Canonical locations
declare -a CANONICAL_DIRS=(
  "skills/javier-montano"
  "skills/metodologia"
)

DASHBOARD="$REPO_ROOT/governance/moat-dashboard.md"
CSV="$REPO_ROOT/governance/moat-status.csv"
DATE=$(date +%Y-%m-%d)

# Helper: safe integer from grep -c / wc -l (strips Windows \r\n)
safe_int() {
  local val
  val=$(cat | tr -dc '0-9')
  echo "${val:-0}"
}

# Helper: safe percentage (avoids div by zero)
pct() {
  local num=$1 den=$2
  if [ "$den" -gt 0 ] 2>/dev/null; then
    echo $((num * 100 / den))
  else
    echo 0
  fi
}

echo "=== MOAT Compliance Audit ==="
echo "  Date: $DATE"
echo "  Repo: $REPO_ROOT"
echo ""

# Counters
TOTAL=0
MOAT_PASS=0
CERTIFIED_ONLY=0
CONDITIONAL=0
BLOCKED=0

# Gap counters
GAP_M1_EVALS=0
GAP_M1B_COUNT=0
GAP_M2_FP=0
GAP_M2B_EDGE=0
GAP_M3_REFS=0
GAP_M4_TEMPLATE=0
GAP_M4B_LEGACY=0
GAP_M5_EVIDENCE=0
GAP_S_STRUCTURAL=0

# Tier counters
TIER_SKELETAL=0
TIER_PARTIAL=0
TIER_COMPLETE=0
TIER_NEAR_MOAT=0

# CSV header
echo "skill_name,namespace,tier,lines,subdirs,moat_status,m1_evals,m1b_count,m2_fp,m2b_edge,m3_refs,m4_template,m4b_legacy,m5_evidence,structural_pass,gaps" > "$CSV"

for canon_dir in "${CANONICAL_DIRS[@]}"; do
  full="$REPO_ROOT/$canon_dir"
  [ -d "$full" ] || continue
  namespace=$(basename "$canon_dir")

  for skill_dir in "$full"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    [[ "$skill_name" == "REGISTRY"* ]] && continue

    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    # Apply filter if specified
    if [ -n "$SKILL_FILTER" ] && [ "$skill_name" != "$SKILL_FILTER" ]; then
      continue
    fi

    TOTAL=$((TOTAL + 1))
    gaps=""

    # === Basic metrics ===
    lines=$(wc -l < "$skill_md" | tr -dc '0-9')
    lines=${lines:-0}

    # Count subdirectories
    subdir_count=0
    [ -d "$skill_dir/references" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/agents" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/evals" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/prompts" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/examples" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/scripts" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/knowledge" ] && subdir_count=$((subdir_count + 1))
    [ -d "$skill_dir/templates" ] && subdir_count=$((subdir_count + 1))

    # === Determine tier ===
    tier="utility"
    if [ "$lines" -ge 400 ]; then
      tier="orchestrator"
    elif [ "$lines" -ge 150 ]; then
      tier="standard"
    fi

    # === Structural checks (S1-S9 simplified) ===
    s_pass="PASS"

    # S2: under 500 lines
    if [ "$lines" -gt 500 ]; then
      s_pass="FAIL"
    fi

    # S3: kebab-case name (strip number prefix for check)
    base_name=$(echo "$skill_name" | sed 's/^[0-9]*-//')
    if ! echo "$base_name" | grep -qP '^[a-z0-9]+(-[a-z0-9]+)*$' 2>/dev/null; then
      # Fallback for systems without -P
      if echo "$base_name" | grep -q '[A-Z \<\>]' 2>/dev/null; then
        s_pass="FAIL"
      fi
    fi

    # S5: no angle brackets in frontmatter description
    if grep -q '[<>]' "$skill_md" 2>/dev/null; then
      # Only fail if in frontmatter description
      in_front=$(sed -n '/^---$/,/^---$/p' "$skill_md" | grep -c '[<>]' 2>/dev/null | safe_int)
      if [ "$in_front" -gt 0 ]; then
        s_pass="FAIL"
      fi
    fi

    if [ "$s_pass" != "PASS" ]; then
      GAP_S_STRUCTURAL=$((GAP_S_STRUCTURAL + 1))
      gaps="${gaps}structural,"
    fi

    # === M1: evals/evals.json exists ===
    m1="FAIL"
    if [ -f "$skill_dir/evals/evals.json" ]; then
      m1="PASS"
    fi
    if [ "$m1" = "FAIL" ]; then
      GAP_M1_EVALS=$((GAP_M1_EVALS + 1))
      gaps="${gaps}M1-no-evals,"
    fi

    # === M1b: >= 5 evals ===
    m1b="FAIL"
    if [ "$m1" = "PASS" ]; then
      eval_count=$(grep -c '"id"' "$skill_dir/evals/evals.json" 2>/dev/null | safe_int)
      if [ "$eval_count" -ge 5 ]; then
        m1b="PASS"
      fi
    fi
    if [ "$m1b" = "FAIL" ] && [ "$m1" = "PASS" ]; then
      GAP_M1B_COUNT=$((GAP_M1B_COUNT + 1))
      gaps="${gaps}M1b-few-evals,"
    fi

    # === M2: false-positive eval ===
    m2="FAIL"
    if [ "$m1" = "PASS" ]; then
      fp=$(grep -ci 'false.positive\|false_positive\|should-not\|negative' "$skill_dir/evals/evals.json" 2>/dev/null | safe_int)
      if [ "$fp" -gt 0 ]; then
        m2="PASS"
      fi
    fi
    if [ "$m2" = "FAIL" ] && [ "$m1" = "PASS" ]; then
      GAP_M2_FP=$((GAP_M2_FP + 1))
      gaps="${gaps}M2-no-fp-eval,"
    fi

    # === M2b: edge-case eval ===
    m2b="FAIL"
    if [ "$m1" = "PASS" ]; then
      edge=$(grep -ci 'edge.case\|edge_case\|boundary\|corner' "$skill_dir/evals/evals.json" 2>/dev/null | safe_int)
      if [ "$edge" -gt 0 ]; then
        m2b="PASS"
      fi
    fi
    if [ "$m2b" = "FAIL" ] && [ "$m1" = "PASS" ]; then
      GAP_M2B_EDGE=$((GAP_M2B_EDGE + 1))
      gaps="${gaps}M2b-no-edge-eval,"
    fi

    # === M3: references substantive ===
    m3="PASS"
    if [ -d "$skill_dir/references" ]; then
      for ref_file in "$skill_dir/references"/*.md; do
        [ -f "$ref_file" ] || continue
        ref_lines=$(wc -l < "$ref_file" | tr -dc '0-9')
        ref_lines=${ref_lines:-0}
        if [ "$ref_lines" -lt 20 ]; then
          m3="FAIL"
          break
        fi
        if grep -qci 'TBD\|TODO\|placeholder' "$ref_file" 2>/dev/null; then
          tbd_count=$(grep -ci 'TBD\|TODO\|placeholder' "$ref_file" 2>/dev/null | safe_int)
          if [ "$tbd_count" -gt 0 ]; then
            m3="FAIL"
            break
          fi
        fi
      done
    else
      # No references/ — PASS for utility, FAIL for standard/orchestrator
      if [ "$tier" != "utility" ]; then
        m3="FAIL"
      fi
    fi
    if [ "$m3" = "FAIL" ]; then
      GAP_M3_REFS=$((GAP_M3_REFS + 1))
      gaps="${gaps}M3-refs,"
    fi

    # === M4: Template A compliance ===
    m4="FAIL"
    has_usage=$(grep -ci '## Usage\|## When to Activate\|## When to Use' "$skill_md" 2>/dev/null | safe_int)
    has_gate=$(grep -ci '## Validation Gate\|## Quality Gate\|## Quality Criteria' "$skill_md" 2>/dev/null | safe_int)
    if [ "$has_usage" -gt 0 ] && [ "$has_gate" -gt 0 ]; then
      m4="PASS"
    fi
    if [ "$m4" = "FAIL" ]; then
      GAP_M4_TEMPLATE=$((GAP_M4_TEMPLATE + 1))
      gaps="${gaps}M4-template,"
    fi

    # === M4b: No Template B markers ===
    m4b="PASS"
    legacy=$(grep -ci '## The Physics\|## The Protocol' "$skill_md" 2>/dev/null | safe_int)
    if [ "$legacy" -gt 0 ]; then
      m4b="FAIL"
      GAP_M4B_LEGACY=$((GAP_M4B_LEGACY + 1))
      gaps="${gaps}M4b-legacy-template,"
    fi

    # === M5: Evidence tags ===
    m5="FAIL"
    tag_count=$(grep -ci '\[EXPLICIT\]\|\[INFERRED\]\|\[OPEN\]\|\[HECHO\]\|\[INFERENCIA\]\|\[SUPUESTO\]' "$skill_md" 2>/dev/null | safe_int)
    # Simple heuristic: count periods as sentence proxy
    sentence_count=$(grep -o '\.' "$skill_md" 2>/dev/null | wc -l | safe_int)
    sentence_count=${sentence_count:-1}

    if [ "$tier" = "utility" ]; then
      threshold=50
    else
      threshold=80
    fi

    if [ "$sentence_count" -gt 0 ] && [ "$tag_count" -gt 0 ]; then
      coverage=$((tag_count * 100 / sentence_count))
      if [ "$coverage" -ge "$threshold" ]; then
        m5="PASS"
      fi
    elif [ "$tag_count" -ge 5 ]; then
      m5="PASS"
    fi
    if [ "$m5" = "FAIL" ]; then
      GAP_M5_EVIDENCE=$((GAP_M5_EVIDENCE + 1))
      gaps="${gaps}M5-evidence,"
    fi

    # === Determine MOAT status ===
    if [ "$s_pass" != "PASS" ]; then
      status="BLOCKED"
      BLOCKED=$((BLOCKED + 1))
    elif [ "$m1" = "PASS" ] && [ "$m1b" = "PASS" ] && [ "$m3" = "PASS" ] && [ "$m4" = "PASS" ] && [ "$m4b" = "PASS" ]; then
      # Core MOAT checks pass (M2, M2b, M5 are warnings, not blockers)
      if [ "$m2" = "PASS" ] && [ "$m2b" = "PASS" ] && [ "$m5" = "PASS" ]; then
        status="MOAT"
        MOAT_PASS=$((MOAT_PASS + 1))
      else
        status="CERTIFIED"
        CERTIFIED_ONLY=$((CERTIFIED_ONLY + 1))
      fi
    else
      # Missing core checks
      fail_count=0
      [ "$m1" = "FAIL" ] && fail_count=$((fail_count + 1))
      [ "$m1b" = "FAIL" ] && fail_count=$((fail_count + 1))
      [ "$m3" = "FAIL" ] && fail_count=$((fail_count + 1))
      [ "$m4" = "FAIL" ] && fail_count=$((fail_count + 1))
      [ "$m4b" = "FAIL" ] && fail_count=$((fail_count + 1))

      if [ "$fail_count" -le 2 ]; then
        status="CONDITIONAL"
        CONDITIONAL=$((CONDITIONAL + 1))
      else
        status="BLOCKED"
        BLOCKED=$((BLOCKED + 1))
      fi
    fi

    # === Determine current tier classification ===
    if [ "$lines" -lt 50 ] && [ "$subdir_count" -eq 0 ]; then
      tier_class="skeletal"
      TIER_SKELETAL=$((TIER_SKELETAL + 1))
    elif [ "$subdir_count" -le 3 ]; then
      tier_class="partial"
      TIER_PARTIAL=$((TIER_PARTIAL + 1))
    elif [ "$status" = "MOAT" ] || ([ "$status" = "CERTIFIED" ] && [ "$subdir_count" -ge 4 ]); then
      tier_class="near-moat"
      TIER_NEAR_MOAT=$((TIER_NEAR_MOAT + 1))
    else
      tier_class="complete"
      TIER_COMPLETE=$((TIER_COMPLETE + 1))
    fi

    # Remove trailing comma from gaps
    gaps=$(echo "$gaps" | sed 's/,$//')
    [ -z "$gaps" ] && gaps="none"

    # Write CSV row
    echo "$skill_name,$namespace,$tier_class,$lines,$subdir_count,$status,$m1,$m1b,$m2,$m2b,$m3,$m4,$m4b,$m5,$s_pass,$gaps" >> "$CSV"

  done
done

# === Generate Dashboard ===
echo "Generating MOAT Dashboard..."

cat > "$DASHBOARD" << DASHBOARD_EOF
# MOAT Dashboard — Generated $DATE

## Progress

| Metric | Count | % |
|--------|-------|---|
| Total canonical skills | $TOTAL | 100% |
| MOAT | $MOAT_PASS | $(pct $MOAT_PASS $TOTAL)% |
| CERTIFIED (not MOAT) | $CERTIFIED_ONLY | $(pct $CERTIFIED_ONLY $TOTAL)% |
| CONDITIONAL | $CONDITIONAL | $(pct $CONDITIONAL $TOTAL)% |
| BLOCKED | $BLOCKED | $(pct $BLOCKED $TOTAL)% |

## Current Tier Distribution

| Tier | Count | Description |
|------|-------|-------------|
| Skeletal (T1) | $TIER_SKELETAL | SKILL.md only, < 50 lines, no subdirs |
| Partial (T2) | $TIER_PARTIAL | SKILL.md + 1-3 subdirs |
| Complete (T3) | $TIER_COMPLETE | SKILL.md + 4+ subdirs, some gaps |
| Near-MOAT (T4) | $TIER_NEAR_MOAT | MOAT or CERTIFIED with 4+ subdirs |

## Gap Distribution (skills affected)

| Gap | Count | Priority | Fix |
|-----|-------|----------|-----|
| M1: Missing evals | $GAP_M1_EVALS | BLOCKER | Create evals/evals.json with >= 5 tests |
| M1b: < 5 evals | $GAP_M1B_COUNT | BLOCKER | Add more test prompts to evals.json |
| M2: No false-positive eval | $GAP_M2_FP | WARNING | Add eval that should NOT trigger behavior |
| M2b: No edge-case eval | $GAP_M2B_EDGE | WARNING | Add boundary/edge scenario eval |
| M3: References gap | $GAP_M3_REFS | BLOCKER | Fill references/ with >= 20-line files |
| M4: Missing Template A sections | $GAP_M4_TEMPLATE | BLOCKER | Add Usage + Validation Gate sections |
| M4b: Legacy Template B | $GAP_M4B_LEGACY | BLOCKER | Migrate Physics/Protocol to Template A |
| M5: Low evidence tag coverage | $GAP_M5_EVIDENCE | WARNING | Add [EXPLICIT]/[INFERRED]/[OPEN] tags |
| Structural failures | $GAP_S_STRUCTURAL | BLOCKER | Fix S1-S9 issues |

## Wave Assignment

| Wave | Skills | Target | Focus |
|------|--------|--------|-------|
| Wave 1 (T4 Near-MOAT) | $TIER_NEAR_MOAT | MOAT in 2 weeks | Polish + certify |
| Wave 2 (T3 Complete) | $TIER_COMPLETE | MOAT in 4 weeks | Add evals + fill gaps |
| Wave 3 (T2 Partial) | $TIER_PARTIAL | MOAT in 6 weeks | Template migrate + evals |
| Wave 4 (T1 Skeletal) | $TIER_SKELETAL | MOAT in 8 weeks | Triage + full build |

## MOAT Formula Reference

\`\`\`
MOAT = CERTIFIED (all rubric dims >= 7, avg >= 8, S1-S9 pass)
     + M1: evals/evals.json with >= 5 distinct tests
     + M2: >= 1 false-positive eval + >= 1 edge-case eval
     + M3: All references/ files >= 20 lines, no TBD/TODO
     + M4: Template A (Usage + Validation Gate sections present)
     + M5: Evidence tags on >= 80% factual claims (50% for Utility)
\`\`\`

---
*Generated by \`scripts/moat-audit.sh\` on $DATE*
DASHBOARD_EOF

echo ""
echo "=== MOAT Audit Complete ==="
echo "  Total: $TOTAL skills"
echo "  MOAT:        $MOAT_PASS ($(pct $MOAT_PASS $TOTAL)%)"
echo "  CERTIFIED:   $CERTIFIED_ONLY ($(pct $CERTIFIED_ONLY $TOTAL)%)"
echo "  CONDITIONAL: $CONDITIONAL ($(pct $CONDITIONAL $TOTAL)%)"
echo "  BLOCKED:     $BLOCKED ($(pct $BLOCKED $TOTAL)%)"
echo ""
echo "  Dashboard: $DASHBOARD"
echo "  CSV:       $CSV"
