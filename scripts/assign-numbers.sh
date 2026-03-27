#!/bin/bash
# assign-numbers.sh — Assign canonical numbers to all unnumbered skills
# Classifies by name patterns into 0000-9999 ranges, then renames
# Usage: ./scripts/assign-numbers.sh [--execute] [REPO_ROOT]

set -euo pipefail

EXECUTE=false
REPO_ROOT=""
for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=true ;;
    *) REPO_ROOT="$arg" ;;
  esac
done
REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

echo "=== Canonical Number Assignment Engine ==="
echo "  Mode: $([ "$EXECUTE" = true ] && echo 'EXECUTE' || echo 'DRY RUN')"
echo ""

# Track next available number per range
declare -A NEXT_NUM
NEXT_NUM[0]=16    # 0000 range: after 0015 (existing)
NEXT_NUM[1]=13    # 1000 range: after 1012
NEXT_NUM[2]=16    # 2000 range: after 2015
NEXT_NUM[3]=13    # 3000 range: after 3012
NEXT_NUM[4]=9     # 4000 range: after 4008
NEXT_NUM[5]=9     # 5000 range: after 5008
NEXT_NUM[6]=10    # 6000 range: after 6009
NEXT_NUM[7]=9     # 7000 range: after 7008
NEXT_NUM[8]=6     # 8000 range: after 8005
NEXT_NUM[9]=10    # 9000 range: after 9009

# Classification function: skill name -> range (0-9)
classify() {
  local name="$1"
  case "$name" in
    # 0000 — Input & Analysis (user needs, discovery, business strategy)
    input-*|asis-*|discovery-*|stakeholder-*|competitive-*|scenario-*|risk-assess*|risk-controlling*|cost-estim*|technical-feasib*|dependency-analy*|assumption-*|user-story*|user-research*|user-testing*|user-representative*|product-strat*|product-roadmap*|functional-spec*|functional-tool*|flow-map*|sector-*|dynamic-sme*|commercial-*|executive-*|market-*|client-*|requirement*|business-process*|benchmarking*|benchmark-skill*|kpi-*|okr-*|survey-*|trade-off*|feasibility-*|poc-*|cv-*|lead-gen*|b2b-*|partnership-*|proposal-*|contract-*|vendor-*|sales-*|pricing-*|cohort-*|funnel-analyt*|conversion-*|reporting-*|competitive-position*|case-study*|budget-manage*|capacity-plan*|change-manage*|change-readiness*|maturity-assess*|governance-framework*|project-program*|retrospective-*|finops*|sla-*|incident-*|software-viab*) echo 0 ;;

    # 1000 — Design & Architecture (system design, all architecture)
    system-*|architect*|component-*|responsive-design*|state-manage*|data-flow*|integration-arch*|api-design*|api-architect*|database-arch*|firebase-arch*|auth-arch*|pwa-*|software-arch*|solutions-arch*|infrastructure-arch*|infrastructure-design*|cloud-*|enterprise-*|event-arch*|devsecops*|micro*|data-model*|design-system*|design-critique*|genai-*|ai-architect*|ai-conops*|ai-design*|ai-pipeline*|ai-software*|aws-*|domain-driven*|realtime-arch*|data-mesh*|observability-arch*|observability-design*|observability|schema-*|roadmap-*|solution-roadmap*|scaffold-*|data-science-arch*|workshop-design*|workshop-proposal*|workshop-facilitator*|bi-architect*|mobile-architect*|mobile-assess*|mobile-pattern*|team-topology*|migration-plan*|chatbot-design*|voice-interface*) echo 1 ;;

    # 2000 — Frontend & UI (visual, user-facing)
    html-*|css-*|javascript-*|react-*|angular-*|vue-*|form-*|ui-*|animation-*|spa-*|data-viz*|landing-*|email-template*|dark-mode*|color-*|grid-*|typography-*|iconography*|navigation-*|modal-*|scroll-*|empty-*|micro-interaction*|motion-*|onboarding-ux*|notification-ux*|search-ux*|table-ux*|web-component*|print-*|font-*|ecommerce-*|portfolio-*|newsletter-*|blog-*|admin-dashboard*|dashboard-design*|presentation-*|accessibility-design*|accessibility-writing*|branded-html*|brand-html*|brand-docx*|brand-xlsx*|brand-voice*|microcopy-*|social-proof*|vanilla-*|typescript-*|prototyping*) echo 2 ;;

    # 3000 — Backend & Logic (server, APIs, services)
    node-*|firebase-func*|firebase-ext*|firebase-setup*|firebase-storage*|server-*|webhook-*|background-*|notification-serv*|notification-hand*|file-storage*|file-watcher*|google-api*|google-map*|google-workspace*|error-handling*|error-recovery*|error-messaging*|caching-*|serverless-*|rest-api*|api-surface*|api-document*|middleware*|payment-*|email-send*|push-notif*|scheduled-*|cloud-func*|rate-limit*|parallel-*|structured-out*|task-auto*|workflow-orch*|health-check*|cdn-*) echo 3 ;;

    # 4000 — Data & Storage (databases, data pipelines)
    firestore-*|realtime-data*|data-migrat*|data-valid*|analytics-impl*|analytics-engineer*|search-impl*|backup-*|data-export*|data-document*|data-privacy*|data-strat*|data-engineer*|data-governance*|data-quality*|data-storytell*|database-design*|etl-*|embedding-*|rag-*|fine-tuning*|vector-*) echo 4 ;;

    # 5000 — Security & Auth
    firebase-auth*|role-based*|oauth-*|web-security*|api-security*|secrets-*|privacy-*|penetration*|security-architect*|security-*|compliance-*|rbac-*|input-sanit*|cors-*|ssl-*|http-header*|audit-trail*|ai-safety*|ai-content-detect*) echo 5 ;;

    # 6000 — Testing & Quality
    unit-test*|integration-test*|e2e-test*|accessibility-audit*|accessibility-test*|code-review*|quality-*|test-*|visual-regres*|firebase-emul*|bdd-*|cross-browser*|performance-test*|security-test*|ai-assisted-test*|ai-testing*|certify-*|x-ray-*|assembly-*|surgeon-*|generate-qa*|llm-eval*|excellence-*) echo 6 ;;

    # 7000 — DevOps & Deployment
    hostinger-*|firebase-hosting*|firebase-deploy*|ci-*|ci-cd*|environment-*|monitoring-*|domain-*|release-*|build-optim*|docker-*|git-*|github-*|ssh-*|dns-*|deployment-*|infrastructure-map*|linting-*|repository-*|changelog-*|log-manage*|alerting-*|workspace-govern*|pipeline-govern*) echo 7 ;;

    # 8000 — Performance & Optimization
    web-perform*|seo-*|image-optim*|bundle-*|firebase-cost*|performance-engineer*|performance-budget*|performance-bottleneck*|performance-profil*|lighthouse-*|indexab*|real-time-analyt*|funnel-design*|google-analyt*|content-calendar*|event-market*|marketing-*|ab-test*|recaptcha*|metrics-instru*) echo 8 ;;

    # 9000 — Meta & Orchestration (skills about skills, tooling, documentation, content)
    skill-*|skill-search*|workflow-*|kit-orch*|scope-guard*|quality-gate*|context-optim*|context-window*|session-*|output-*|intelligent-*|auto-*|meta-*|plugin-*|find-skill*|create-*|creator-*|design-skill*|design-agent*|spec-*|validate-*|build-moat*|build-plugin*|plan-architect*|plan-moat*|ideate-*|fix-common*|audit-content*|audit-security*|iikit-*|iic-*|bmad-*|sofka-*|prompt-*|guardrails-*|triad-*|socratic-*|dual-layer*|permission-*|pre-compact*|pre-tool*|post-tool*|stop-valid*|user-prompt-*|subagent-*|tasklog-*|task-engine*|continuous-learn*|technical-doc*|documentation-*|technical-writ*|copywriting*|storytelling*|video-*|podcast-*|press-*|whitepaper*|training-*|internal-*|localization*|international*|knowledge-*|onboarding-playbook*|developer-onboard*|naming-*|step-*|rule-*|hook-*|trigger-*|open-claw*|ecosystem-*|xlsx-*|mcp-*|rendering-*|cross-platform*|ai-code-review*|ai-document*|ai-workflow*|agent-*|multi-model*|mermaid-*|data-storytelling*) echo 9 ;;

    # Default: 0000 (unclassified → closer to user)
    *) echo 0 ;;
  esac
}

# Process both directories
total_assigned=0

for base_dir in "skills/javier-montano" "skills/metodologia"; do
  full_base="$REPO_ROOT/$base_dir"
  [ -d "$full_base" ] || continue

  for skill_dir in "$full_base"/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")

    # Skip already numbered
    [[ "$name" =~ ^[0-9] ]] && continue
    # Skip hidden
    [[ "$name" == .* ]] && continue
    # Must have SKILL.md
    [ -f "$skill_dir/SKILL.md" ] || continue

    # Classify
    range=$(classify "$name")
    num=${NEXT_NUM[$range]}
    padded=$(printf "%04d" $((range * 1000 + num)))
    new_name="${padded}-${name}"
    new_dir="$full_base/$new_name"

    NEXT_NUM[$range]=$((num + 1))
    total_assigned=$((total_assigned + 1))

    if [ "$EXECUTE" = true ]; then
      mv "$skill_dir" "$new_dir"
      echo "  $name → $new_name"
    else
      echo "  [$padded] $name → $new_name"
    fi
  done
done

echo ""
echo "=== Assignment Summary ==="
echo "  Total assigned: $total_assigned"
echo ""
echo "  Range distribution:"
for r in 0 1 2 3 4 5 6 7 8 9; do
  count=$((${NEXT_NUM[$r]} - 1))
  case $r in
    0) label="Input & Analysis" ;;
    1) label="Design & Architecture" ;;
    2) label="Frontend & UI" ;;
    3) label="Backend & Logic" ;;
    4) label="Data & Storage" ;;
    5) label="Security & Auth" ;;
    6) label="Testing & Quality" ;;
    7) label="DevOps & Deployment" ;;
    8) label="Performance & Optimization" ;;
    9) label="Meta & Orchestration" ;;
  esac
  # Calculate total including existing numbered
  echo "  ${r}000: $label — ${NEXT_NUM[$r]} total (includes pre-existing)"
done

[ "$EXECUTE" != true ] && echo "" && echo "  (DRY RUN — use --execute to apply)"
