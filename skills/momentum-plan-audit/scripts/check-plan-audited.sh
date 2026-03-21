#!/usr/bin/env bash
# PreToolUse hook for ExitPlanMode.
# Blocks plan mode exit if the active plan is missing a ## Spec Impact section.
#
# Exit codes:
#   0 — Spec Impact section present (or no plan files found) — allow ExitPlanMode
#   2 — Spec Impact section absent — block ExitPlanMode
#
# Environment:
#   PLANS_DIR — override plans directory (default: ~/.claude/plans)

PLANS_DIR="${PLANS_DIR:-$HOME/.claude/plans}"

# Find the most recently modified plan file
PLAN_FILE=$(stat -f "%m %N" "$PLANS_DIR"/*.md 2>/dev/null | sort -rn | head -1 | awk '{print $2}')

# No plan files — nothing to check, allow exit
[ -z "$PLAN_FILE" ] && exit 0

# Check for ## Spec Impact section (anchored to heading level 2)
if grep -q "^## Spec Impact" "$PLAN_FILE"; then
  exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Plan audit gate (safety net): Spec Impact missing."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Active plan: $PLAN_FILE"
echo "  Missing:     '## Spec Impact' section"
echo ""
echo "  This should have run automatically via the plan-audit"
echo "  rule. If it didn't, invoke momentum-plan-audit manually."
echo ""
exit 2
