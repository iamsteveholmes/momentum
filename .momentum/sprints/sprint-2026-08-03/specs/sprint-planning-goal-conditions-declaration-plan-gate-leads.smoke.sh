#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: sprint-planning-goal-conditions-declaration-plan-gate-leads
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-08-03/specs/sprint-planning-goal-conditions-declaration-plan-gate-leads.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/sprint-planning-goal-conditions-declaration-plan-gate-leads.md#acceptance-criteria
# platforms: [host]

# sprint-planning-goal-conditions-declaration-plan-gate-leads smoke contract
# Harness profile: bash
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-08-03/specs/sprint-planning-goal-conditions-declaration-plan-gate-leads.smoke.sh
#   Self-contained: builds a throwaway fixture project in a temp directory and
#   removes it on exit. Requires `momentum-tools` and `python3` on PATH. Never
#   touches the real project's .momentum state.
#
# Expected: `momentum-tools sprint plan` accepts --goal and --goal-conditions
# (comma-separated feature slugs; empty string allowed), persists both onto the
# planning sprint record in .momentum/sprints/index.json, reads them back after
# the command returns, is idempotent on repeat calls with identical values,
# refuses on a locked sprint, and `momentum-tools sprint activate` carries both
# fields onto the active sprint record unchanged.
#
# Producer / Consumer scope (seam declaration):
#   PRODUCER (this contract): sprint planning writes `goal` (a string) and
#     `goal_conditions` (an array of feature slugs) onto the sprint record via
#     the CLI. A maintenance sprint (zero conditions) writes a verified-fix
#     list into `goal` as line-break-separated entries after a fix-list
#     lead-in line, and `goal_conditions` persists as an empty array.
#   CONSUMER (verified elsewhere — the sprint-closure-refusal contract):
#     sprint closure keys its per-condition human-verdict checks off the
#     `goal_conditions` array, and for maintenance sprints parses the
#     verified-fix list by line-break-splitting the `goal` text after the
#     lead-in. Scenario 2 below freezes the produced record shape both sides
#     must agree on; a failure there is a cross-side field-shape
#     incompatibility, not a single-story bug.
#
# Scope note: this script covers the CLI-observable producer surface. The
# plan-gate presentation behaviors (capability card rendered first, written
# capability verdict required, purpose hero wording, change/reject effects)
# are verified by invoking the sprint-planning skill and observing the
# rendered gate — outside what a shell script can drive.

set -euo pipefail

command -v momentum-tools >/dev/null 2>&1 || { echo "FAIL: momentum-tools not found on PATH"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: python3 not found on PATH"; exit 1; }

# --- Fixture: throwaway project directory ---------------------------------
FIXTURE_DIR="$(mktemp -d)"
trap 'rm -rf "$FIXTURE_DIR"' EXIT
mkdir -p "$FIXTURE_DIR/.momentum/sprints"
cd "$FIXTURE_DIR"
export CLAUDE_PROJECT_DIR="$FIXTURE_DIR"

INDEX=".momentum/sprints/index.json"
SPRINT_SLUG="sprint-smoke-goal-conditions"

# Read one field off the sprint record (planning or active) as JSON, from the
# observable record file the story's ACs name as the persistence target.
record_field() {
  python3 - "$1" <<'PY'
import json, sys

field = sys.argv[1]
with open(".momentum/sprints/index.json") as fh:
    data = json.load(fh)

def records(node):
    if isinstance(node, dict):
        if "goal" in node or "goal_conditions" in node or "stories" in node:
            yield node
        for value in node.values():
            yield from records(value)
    elif isinstance(node, list):
        for value in node:
            yield from records(value)

match = next((rec for rec in records(data) if field in rec), None)
print("null" if match is None else json.dumps(match[field]))
PY
}

json_type() {
  python3 -c 'import json, sys; print(type(json.loads(sys.argv[1])).__name__)' "$1"
}

# Fixture-only manipulation: flip the locked flag on the fixture's sprint
# record to simulate a locked sprint (the locked state named by the ACs).
# This is test setup inside a throwaway temp dir — never done to a real project.
set_locked() {
  python3 - "$1" <<'PY'
import json, sys

flag = sys.argv[1] == "true"
path = ".momentum/sprints/index.json"
with open(path) as fh:
    data = json.load(fh)

def walk(node):
    if isinstance(node, dict):
        if "locked" in node:
            node["locked"] = flag
        for value in node.values():
            walk(value)
    elif isinstance(node, list):
        for value in node:
            walk(value)

walk(data)
with open(path, "w") as fh:
    json.dump(data, fh, indent=2)
PY
}

# --- Scenario 1: a planning record exists to declare against ----------------
momentum-tools sprint plan --operation add --stories smoke-fixture-story --slug "$SPRINT_SLUG" >/dev/null

[ -f "$INDEX" ] || {
  echo "FAIL: expected $INDEX to exist after 'momentum-tools sprint plan --operation add'"
  exit 1
}
echo "ok: scenario 1 — planning sprint record created via the CLI"

# --- Scenario 2 (seam shape): maintenance sprint — empty conditions + -------
# --- line-separated verified-fix list — the record shape the consumer parses
MAINT_GOAL='Verified fixes:
- Re-running sprint plan no longer drops the declared wave
- The build handoff shows the captured goal instead of the fallback line'

momentum-tools sprint plan --goal "$MAINT_GOAL" --goal-conditions "" >/dev/null

GOAL_JSON="$(record_field goal)"
COND_JSON="$(record_field goal_conditions)"

[ "$(json_type "$GOAL_JSON")" = "str" ] || {
  echo "FAIL: goal must read back from the sprint record as a string; got type $(json_type "$GOAL_JSON") value $GOAL_JSON"
  exit 1
}
[ "$(json_type "$COND_JSON")" = "list" ] || {
  echo "FAIL: cross-side field-shape incompatibility — goal_conditions read back as $(json_type "$COND_JSON"), not an array; sprint closure keys per-condition verdicts off an array of feature slugs. Got: $COND_JSON"
  exit 1
}
COND_LEN="$(python3 -c 'import json, sys; print(len(json.loads(sys.argv[1])))' "$COND_JSON")"
[ "$COND_LEN" = "0" ] || {
  echo "FAIL: an empty --goal-conditions must persist as an empty array [] on the record; got: $COND_JSON"
  exit 1
}
FIX_COUNT="$(python3 -c '
import json, sys
goal = json.loads(sys.argv[1])
lines = [line.strip() for line in goal.splitlines()]
print(len([line for line in lines[1:] if line]))
' "$GOAL_JSON")"
[ "$FIX_COUNT" = "2" ] || {
  echo "FAIL: cross-side field-shape incompatibility — verified-fix entries must survive as line-break-separated lines after the fix-list lead-in (sprint closure parses the fix list by line split); expected 2 entries, got $FIX_COUNT from goal: $GOAL_JSON"
  exit 1
}
echo "ok: scenario 2 — maintenance record shape holds (goal string, goal_conditions array, line-splittable fix list)"

# --- Scenario 3: feature-backed declaration persists and reads back ---------
FEATURE_GOAL="After this sprint a GM will be able to capture a session and name a campaign"

momentum-tools sprint plan --goal "$FEATURE_GOAL" --goal-conditions "session-capture,campaign-identity" >/dev/null

GOAL_JSON="$(record_field goal)"
COND_JSON="$(record_field goal_conditions)"

[ "$GOAL_JSON" = "\"$FEATURE_GOAL\"" ] || {
  echo "FAIL: declared goal did not read back from the sprint record; expected \"$FEATURE_GOAL\", got $GOAL_JSON"
  exit 1
}
[ "$(json_type "$COND_JSON")" = "list" ] || {
  echo "FAIL: cross-side field-shape incompatibility — goal_conditions read back as $(json_type "$COND_JSON"), not an array of feature slugs. Got: $COND_JSON"
  exit 1
}
COND_LEN="$(python3 -c 'import json, sys; print(len(json.loads(sys.argv[1])))' "$COND_JSON")"
[ "$COND_LEN" = "2" ] || {
  echo "FAIL: expected exactly 2 declared goal conditions on the record, got $COND_LEN: $COND_JSON"
  exit 1
}
echo "$COND_JSON" | grep -q '"session-capture"' || {
  echo "FAIL: declared slug session-capture missing from goal_conditions: $COND_JSON"
  exit 1
}
echo "$COND_JSON" | grep -q '"campaign-identity"' || {
  echo "FAIL: declared slug campaign-identity missing from goal_conditions: $COND_JSON"
  exit 1
}
echo "ok: scenario 3 — feature-backed declaration persisted and read back"

# --- Scenario 4: the identical call again is idempotent ---------------------
momentum-tools sprint plan --goal "$FEATURE_GOAL" --goal-conditions "session-capture,campaign-identity" >/dev/null

GOAL_AGAIN="$(record_field goal)"
COND_AGAIN="$(record_field goal_conditions)"

[ "$GOAL_AGAIN" = "$GOAL_JSON" ] || {
  echo "FAIL: repeating the identical declaration changed goal (expected idempotence): before=$GOAL_JSON after=$GOAL_AGAIN"
  exit 1
}
[ "$COND_AGAIN" = "$COND_JSON" ] || {
  echo "FAIL: repeating the identical declaration changed goal_conditions (expected idempotence, no duplication): before=$COND_JSON after=$COND_AGAIN"
  exit 1
}
echo "ok: scenario 4 — repeat declaration with identical values is idempotent"

# --- Scenario 5: a locked sprint refuses the declaration --------------------
set_locked true

if momentum-tools sprint plan --goal "should not land" --goal-conditions "should-not-land" >/dev/null 2>&1; then
  echo "FAIL: a locked sprint accepted a goal declaration; expected a refusal matching the existing flags' locked-sprint behavior"
  exit 1
fi

GOAL_LOCKED="$(record_field goal)"
[ "$GOAL_LOCKED" = "\"$FEATURE_GOAL\"" ] || {
  echo "FAIL: locked-sprint refusal still altered the record; goal is now $GOAL_LOCKED"
  exit 1
}
set_locked false
echo "ok: scenario 5 — locked sprint refuses and the record is unchanged"

# --- Scenario 6: activation carries both fields unchanged -------------------
momentum-tools sprint activate >/dev/null

GOAL_ACTIVE="$(record_field goal)"
COND_ACTIVE="$(record_field goal_conditions)"

[ "$GOAL_ACTIVE" = "\"$FEATURE_GOAL\"" ] || {
  echo "FAIL: sprint activation dropped or changed goal; expected \"$FEATURE_GOAL\", got $GOAL_ACTIVE"
  exit 1
}
[ "$COND_ACTIVE" = "$COND_JSON" ] || {
  echo "FAIL: sprint activation dropped or changed goal_conditions; expected $COND_JSON, got $COND_ACTIVE"
  exit 1
}
echo "ok: scenario 6 — activation carried goal and goal_conditions onto the active record unchanged"

echo "PASS"
