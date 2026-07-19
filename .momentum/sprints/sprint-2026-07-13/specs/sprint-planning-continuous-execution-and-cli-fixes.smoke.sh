#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: sprint-planning-continuous-execution-and-cli-fixes
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-07-13/specs/sprint-planning-continuous-execution-and-cli-fixes.smoke.sh
# how_dev_self_checks: Run this script (bash .momentum/sprints/sprint-2026-07-13/specs/sprint-planning-continuous-execution-and-cli-fixes.smoke.sh) and observe exit 0 with a final PASS line -- this confirms the planning sprint slug is settable via momentum-tools and reads back through a CLI or state query, and that the sprint-planning CLI surfaces resolve with no stale-subcommand errors. Separately, since a script cannot drive this leg, run a sprint-planning session on a clean input and observe it proceeds continuously, pausing only at three points -- story selection, per-story approve-or-reject-or-jettison decision, and the plan-gate sign-off -- with no other informational proceed-or-revise confirmation blocking the run.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/sprint-planning-continuous-execution-and-cli-fixes.md#acceptance-criteria
# platforms: [host]

# sprint-planning-continuous-execution-and-cli-fixes smoke contract
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-07-13/specs/sprint-planning-continuous-execution-and-cli-fixes.smoke.sh
#
# Expected:
#   1. momentum-tools exposes a CLI surface that sets the planning sprint's slug;
#      the slug set through that surface is readable back through a CLI/state query.
#   2. Every momentum-tools CLI surface the sprint-planning workflow relies on
#      (sprint plan, sprint activate) resolves as a real, registered subcommand --
#      no stale or unknown-subcommand errors, including for the previously-stale
#      names (sprint-current, sprint-stories) which must stay unresolvable.
#
# SCOPE NOTE (split between this script and how_dev_self_checks above): this story
# also requires that a clean sprint-planning run proceeds continuously, pausing only
# at its three designed decision gates (story selection, per-story approve/reject/
# jettison, and the plan-gate sign-off) rather than at gratuitous informational
# confirmations. That workflow-behavior leg cannot be driven or observed by a
# non-interactive shell script, so it is captured only as a plain-language
# self-check in how_dev_self_checks above. Everything asserted below is the
# CLI-observable leg only.

set -uo pipefail
# Note: -e is intentionally omitted. Some assertions below (the stale-subcommand
# regression guard) treat a NON-ZERO exit as the passing condition, so each
# command's exit status is captured and checked explicitly instead of relying on
# early-exit-on-failure.

FAIL=0
fail() {
  echo "FAIL: $1"
  FAIL=1
}
ok() {
  echo "ok: $1"
}

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
TOOLS="$REPO_ROOT/skills/momentum/scripts/momentum-tools.py"

if [ ! -f "$TOOLS" ]; then
  echo "FAIL: momentum-tools CLI entry point not found at $TOOLS"
  exit 1
fi

# --- Isolation: never touch the real, in-flight planning sprint -----------
# momentum-tools resolves project state (.momentum/sprints/index.json etc.) under
# a project root that CLAUDE_PROJECT_DIR points at. To exercise the slug-setting
# CLI surface without mutating the real planning sprint, this contract points
# CLAUDE_PROJECT_DIR at a disposable scratch directory seeded with a minimal
# planning entry in the documented shape -- {"locked": false, "status": "planning",
# "stories": [], "waves": []}, no "slug" field -- matching the story's own
# description of a freshly created planning entry, then invokes momentum-tools
# against that scratch root only. The scratch directory is removed on exit.
SCRATCH_DIR="$(mktemp -d)"
trap 'rm -rf "$SCRATCH_DIR"' EXIT
mkdir -p "$SCRATCH_DIR/.momentum/sprints" "$SCRATCH_DIR/.momentum/stories"
cat > "$SCRATCH_DIR/.momentum/sprints/index.json" <<'EOF'
{
  "active": null,
  "planning": {"locked": false, "status": "planning", "stories": [], "waves": []},
  "completed": [],
  "quickfixes": []
}
EOF
echo '{"stories": []}' > "$SCRATCH_DIR/.momentum/stories/index.json"
export CLAUDE_PROJECT_DIR="$SCRATCH_DIR"

TEST_SLUG="sprint-contract-smoke-test"
TEST_STORY="contract-smoke-placeholder-story"

# --- Assertion 1: the planning sprint slug is settable via the CLI, and ----
# --- reads back through a CLI/state query ----------------------------------
PLAN_OUT=$(python3 "$TOOLS" sprint plan --operation add --stories "$TEST_STORY" --slug "$TEST_SLUG" 2>&1)
PLAN_STATUS=$?
if [ "$PLAN_STATUS" -ne 0 ]; then
  fail "momentum-tools sprint plan --slug did not run cleanly (exit $PLAN_STATUS): $PLAN_OUT"
else
  READBACK_SLUG=$(python3 -c "
import json
with open('$SCRATCH_DIR/.momentum/sprints/index.json') as f:
    data = json.load(f)
print(data.get('planning', {}).get('slug') or '')
")
  if [ "$READBACK_SLUG" != "$TEST_SLUG" ]; then
    fail "expected the planning sprint slug to read back as '$TEST_SLUG' via CLI/state query, got: '${READBACK_SLUG:-<absent>}'"
  else
    ok "planning sprint slug set via CLI reads back as '$TEST_SLUG'"
  fi
fi

# --- Assertion 2: the CLI surfaces the planning workflow relies on all -----
# --- resolve -- no stale/unknown subcommand errors --------------------------
for SUBCOMMAND in "sprint plan" "sprint activate"; do
  # Intentionally unquoted: $SUBCOMMAND is meant to word-split into separate args.
  HELP_OUT=$(python3 "$TOOLS" $SUBCOMMAND --help 2>&1)
  HELP_STATUS=$?
  if [ "$HELP_STATUS" -ne 0 ] || echo "$HELP_OUT" | grep -qiE "invalid choice|unrecognized|no such|unknown"; then
    fail "momentum-tools $SUBCOMMAND does not resolve as a registered subcommand: $HELP_OUT"
  else
    ok "momentum-tools $SUBCOMMAND resolves"
  fi
done

# Regression guard: the previously-stale subcommand names named in the story
# (sprint-current, sprint-stories) must remain unresolvable. If either now
# resolves, the stale-subcommand defect has resurfaced.
for STALE in "sprint-current" "sprint-stories"; do
  STALE_OUT=$(python3 "$TOOLS" sprint "$STALE" --help 2>&1)
  STALE_STATUS=$?
  if [ "$STALE_STATUS" -eq 0 ]; then
    fail "stale subcommand '$STALE' unexpectedly resolves -- regression"
  else
    ok "stale subcommand '$STALE' correctly does not resolve"
  fi
done

if [ "$FAIL" -ne 0 ]; then
  exit 1
fi

echo "PASS"
