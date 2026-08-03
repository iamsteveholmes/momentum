#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: sprint-closure-refusal-recorded-human-verdicts-per-goal
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-08-03/specs/sprint-closure-refusal-recorded-human-verdicts-per-goal.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/sprint-closure-refusal-recorded-human-verdicts-per-goal.md#acceptance-criteria
# platforms: [host]

# sprint-closure-refusal-recorded-human-verdicts-per-goal smoke contract
# Harness profile: bash
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-08-03/specs/sprint-closure-refusal-recorded-human-verdicts-per-goal.smoke.sh
#   Run from the project root. Requires python3. Uses `momentum-tools` from PATH when
#   available, otherwise the in-repo CLI entry point. Every scenario runs against a
#   throwaway mktemp project fixture — the real project's .momentum state is never touched.
#
# Expected:
#   `momentum-tools sprint complete` is a closure gate, not an unconditional closer. It
#   refuses to close a sprint as done unless every feature slug in the active sprint
#   record's goal_conditions carries a recorded human verdict in .momentum/features.json
#   (status "passing" plus a complete last_verified block: verdict and both paired build
#   SHAs). A recorded FAIL blocks done and points at FAILED closure as the honest exit.
#   `sprint complete --verdict failed --reason "<text>"` closes with status "failed" even
#   when conditions are unverified, recording which were unverified. Every successful
#   closure appends a truthful record to completed[] with retro_run_at null so retro
#   pickup is identical for both terminal states.
#
# Producer / Consumer scope (seam contract — consumer side, two producers):
#   Producer 1: `momentum-tools feature verify` — sole writer of the feature verdict
#               registry .momentum/features.json (per-slug status + last_verified block
#               carrying the human verdict and both paired build SHAs).
#   Producer 2: sprint planning (`momentum-tools sprint plan --goal / --goal-conditions`)
#               — writes the `goal` string and the `goal_conditions` array of feature
#               slugs onto the sprint record at planning time.
#   Consumer:   the sprint complete gate (`momentum-tools sprint complete`) — reads both
#               producers' outputs and decides closure. This contract exercises the
#               consumer against fixtures shaped exactly as the producers declare.
#   Scenario S1 is the cross-side AGREE case: a producer-shaped registry entry (status
#   passing + complete last_verified) satisfies a declared condition and closure proceeds.
#   Scenario S2 is the cross-side DISAGREE case: a registry entry lacking the paired
#   build SHAs the consumer requires is a field-shape incompatibility between the two
#   sides — closure refuses and names it with the machine-readable reason `no-build-shas`.
#
# SEAM PIN — registry fixture shape: the fixtures below encode the producer-declared
# entry shape (flat per-slug map, no wrapper object; entry = status +
# last_verified{date, verdict ("pass"/"fail" lowercase), backend_sha, client_sha},
# plus an optional evidence text — present-but-not-asserted here pending the flagged
# D1 extension). If the implementation lands a different registry shape, this contract
# fails loudly — that is exactly the seam mismatch it exists to expose. Reconcile at the
# cross-story coherence check; do not weaken the assertions.
#
# Out of scope for this smoke (covered by the story's own test suite): the maintenance
# fix-list gate and the punt-decision gate, both of which depend on pre-existing project
# state shapes (the free-text goal fix-list lead-in; the stories index) that a black-box
# fixture cannot pin without guessing.

set -euo pipefail

# --- Harness plumbing ---------------------------------------------------------------

REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
if command -v momentum-tools >/dev/null 2>&1; then
  TOOL=(momentum-tools)
elif [ -f "$REPO_ROOT/skills/momentum/scripts/momentum-tools.py" ]; then
  TOOL=(python3 "$REPO_ROOT/skills/momentum/scripts/momentum-tools.py")
else
  echo "FAIL: cannot locate the momentum-tools CLI (not on PATH, and no CLI entry point under \$CLAUDE_PROJECT_DIR)"
  exit 1
fi

FIXROOT="$(mktemp -d "${TMPDIR:-/tmp}/closure-gate.XXXXXX")"
trap 'rm -rf "$FIXROOT"' EXIT

SCENARIO=0
FIXTURE=""
OUT=""
RC=0

new_fixture() {
  SCENARIO=$((SCENARIO + 1))
  FIXTURE="$FIXROOT/s$SCENARIO"
  mkdir -p "$FIXTURE/.momentum/sprints"
}

run_gate() {
  set +e
  OUT=$(cd "$FIXTURE" && CLAUDE_PROJECT_DIR="$FIXTURE" "${TOOL[@]}" "$@" 2>&1)
  RC=$?
  set -e
}

fail() { echo "FAIL: $*"; exit 1; }

assert_ok()      { [ "$RC" -eq 0 ] || fail "$1 — expected exit 0, got $RC. Output: $OUT"; }
assert_refused() { [ "$RC" -ne 0 ] || fail "$1 — expected non-zero exit (refusal), got 0. Output: $OUT"; }
assert_out()     { grep -qF -- "$1" <<<"$OUT" || fail "$2 — expected output to contain \"$1\". Output: $OUT"; }
assert_out_i()   { grep -qi -- "$1" <<<"$OUT" || fail "$2 — expected output to mention \"$1\". Output: $OUT"; }

py_check() {
  python3 - "$FIXTURE/.momentum/sprints/index.json" "$1" <<'PY'
import json, sys
idx = json.load(open(sys.argv[1]))
sys.exit(0 if eval(sys.argv[2]) else 1)
PY
}

assert_state() { py_check "$1" || fail "$2"; }

assert_untouched() {
  py_check 'idx["active"] is not None and idx["active"]["slug"] == "seam-fixture-sprint" and idx["completed"] == []' \
    || fail "$1 — refusal must leave the active sprint untouched and append nothing to completed[]"
}

# --- Fixture seeds ------------------------------------------------------------------

seed_sprint() {  # $1 = JSON object for the active sprint record
  cat > "$FIXTURE/.momentum/sprints/index.json" <<JSON
{ "active": $1, "planning": null, "completed": [] }
JSON
}

# Producer 2's declared output: sprint record with goal + goal_conditions (array of slugs).
CONDITION_SPRINT='{ "slug": "seam-fixture-sprint", "status": "active", "locked": true, "stories": [], "waves": [], "goal": "The fixture feature works end to end in the running app", "goal_conditions": ["fixture-feature"] }'

# Producer 1's declared output: complete verified-PASS registry entry.
seed_features_complete_pass() {
  cat > "$FIXTURE/.momentum/features.json" <<'JSON'
{
  "fixture-feature": {
    "status": "passing",
    "last_verified": {
      "date": "2026-08-03",
      "verdict": "pass",
      "backend_sha": "aaaa1111",
      "client_sha": "bbbb2222",
      "evidence": "seen working end to end in the running app"
    }
  }
}
JSON
}

# Field-shape mismatch: a verdict recorded without the paired build SHAs.
seed_features_no_shas() {
  cat > "$FIXTURE/.momentum/features.json" <<'JSON'
{
  "fixture-feature": {
    "status": "passing",
    "last_verified": {
      "date": "2026-08-03",
      "verdict": "pass"
    }
  }
}
JSON
}

# Complete recorded FAIL: verdict FAIL with both paired build SHAs present.
seed_features_recorded_fail() {
  cat > "$FIXTURE/.momentum/features.json" <<'JSON'
{
  "fixture-feature": {
    "status": "failing",
    "last_verified": {
      "date": "2026-08-03",
      "verdict": "fail",
      "backend_sha": "aaaa1111",
      "client_sha": "bbbb2222",
      "evidence": "campaign context still missing in the running app"
    }
  }
}
JSON
}

# Registry present, but the declared condition slug is not in it.
seed_features_other_slug() {
  cat > "$FIXTURE/.momentum/features.json" <<'JSON'
{
  "some-other-feature": {
    "status": "passing",
    "last_verified": {
      "date": "2026-08-03",
      "verdict": "pass",
      "backend_sha": "cccc3333",
      "client_sha": "dddd4444",
      "evidence": "seen working end to end in the running app"
    }
  }
}
JSON
}

# --- S1: seam AGREE — verified-PASS condition lets done closure proceed --------------

new_fixture
seed_sprint "$CONDITION_SPRINT"
seed_features_complete_pass
run_gate sprint complete
assert_ok "S1: a condition with status passing and a complete last_verified block must allow done closure"
assert_state 'idx["active"] is None' \
  "S1: active must be cleared after successful closure"
assert_state 'len(idx["completed"]) == 1 and idx["completed"][0]["status"] == "done"' \
  "S1: the closed record must land in completed[] with status done"
assert_state 'idx["completed"][0].get("retro_run_at", "MISSING") is None' \
  "S1: the closed record must carry retro_run_at: null for retro pickup"
assert_state 'bool(idx["completed"][0].get("completed"))' \
  "S1: the closed record must stamp the completion date"
assert_state '"fixture-feature" in json.dumps(idx["completed"][0]) and "aaaa1111" in json.dumps(idx["completed"][0]) and "bbbb2222" in json.dumps(idx["completed"][0])' \
  "S1: the closure block must snapshot the per-condition verdict (slug and paired build SHAs)"
echo "ok S1 — seam agree: producer-shaped passing verdict satisfies the declared condition; closure proceeds and records the truth"

# --- S2: seam DISAGREE — verdict without paired build SHAs is refused ----------------

new_fixture
seed_sprint "$CONDITION_SPRINT"
seed_features_no_shas
run_gate sprint complete
assert_refused "S2: a verdict recorded without both paired build SHAs must refuse done closure"
assert_out "no-build-shas" \
  "S2: the refusal must name the cross-side field-shape gap with the machine-readable reason no-build-shas"
assert_out "fixture-feature" \
  "S2: the refusal must name the blocking condition"
assert_untouched "S2"
echo "ok S2 — seam disagree: registry entry missing the paired build SHAs is a field-shape incompatibility; the consumer refuses and names it"

# --- S3: unverified conditions — absent registry and unregistered slug ---------------

new_fixture
seed_sprint "$CONDITION_SPRINT"
# 3a: no .momentum/features.json at all — a missing registry is never a pass
run_gate sprint complete
assert_refused "S3a: an absent verdict registry must refuse done closure"
assert_out "missing-entry" "S3a: the refusal reason for an unregistered condition must be missing-entry"
assert_out "fixture-feature" "S3a: the refusal must name the blocking condition"
assert_untouched "S3a"
# 3b: registry exists but the declared slug is not in it
seed_features_other_slug
run_gate sprint complete
assert_refused "S3b: a condition slug absent from the registry must refuse done closure"
assert_out "missing-entry" "S3b: the refusal reason for a slug absent from the registry must be missing-entry"
assert_untouched "S3b"
echo "ok S3 — unverified conditions (absent registry, unregistered slug) block done closure with reason missing-entry"

# --- S4: recorded FAIL blocks done and points at the honest FAILED exit --------------

new_fixture
seed_sprint "$CONDITION_SPRINT"
seed_features_recorded_fail
run_gate sprint complete
assert_refused "S4: a complete recorded FAIL must block done closure"
assert_out "fixture-feature" "S4: the refusal must name the failing condition"
assert_out_i "failed" "S4: the refusal must state that FAILED closure is the available honest exit"
if grep -qF -- "missing-entry" <<<"$OUT" || grep -qF -- "no-verdict" <<<"$OUT" || grep -qF -- "no-build-shas" <<<"$OUT"; then
  fail "S4: a complete recorded FAIL is not an unverified condition — the refusal must not use the unverified reason tokens. Output: $OUT"
fi
assert_untouched "S4"
echo "ok S4 — recorded FAIL blocks done, names the condition, and routes to FAILED closure instead of an unverified-reason token"

# --- S5: FAILED is a real terminal state, honest about unverified conditions ---------

new_fixture
seed_sprint "$CONDITION_SPRINT"
# No registry seeded: the condition is unverified — FAILED closure must still succeed.
run_gate sprint complete --verdict failed --reason "keystone condition never verified in the running app"
assert_ok "S5: FAILED closure with a non-empty reason must succeed even when conditions are unverified"
assert_state 'idx["active"] is None' \
  "S5: active must be cleared after FAILED closure"
assert_state 'len(idx["completed"]) == 1 and idx["completed"][0]["status"] == "failed"' \
  "S5: the closed record must land in completed[] with status failed"
assert_state 'idx["completed"][0].get("retro_run_at", "MISSING") is None' \
  "S5: the FAILED record must carry retro_run_at: null so retro discovers it exactly like a done sprint"
assert_state 'bool(idx["completed"][0].get("completed"))' \
  "S5: the FAILED record must stamp the completion date"
assert_state '"keystone condition never verified" in json.dumps(idx["completed"][0])' \
  "S5: the FAILED reason must be recorded on the closed record"
assert_state '"fixture-feature" in json.dumps(idx["completed"][0])' \
  "S5: the conditions unverified at FAILED closure must be recorded on the closed record"
echo "ok S5 — FAILED closure is honest: it succeeds past unverified conditions, records them, and stays retro-discoverable"

# --- S6: FAILED closure without a reason is refused -----------------------------------

new_fixture
seed_sprint "$CONDITION_SPRINT"
run_gate sprint complete --verdict failed
assert_refused "S6: FAILED closure without --reason must be refused"
assert_out_i "reason" "S6: the refusal must say a reason is required"
assert_untouched "S6"
echo "ok S6 — FAILED closure demands a recorded reason"

# --- S7: a sprint with no declared outcome cannot close silently ---------------------

new_fixture
seed_sprint '{ "slug": "seam-fixture-sprint", "status": "active", "locked": true, "stories": [], "waves": [], "goal": "General cleanup" }'
run_gate sprint complete
assert_refused "S7: done closure with no goal_conditions and no verified-fix list must be refused"
assert_out_i "condition" "S7: the refusal must offer declaring the sprint's conditions as one exit"
assert_out_i "failed" "S7: the refusal must offer FAILED closure with a reason as the other exit"
assert_untouched "S7"
echo "ok S7 — undeclared outcome refuses done closure and states both honest exits"

# --- S8: no active sprint — existing behavior preserved ------------------------------

new_fixture
cat > "$FIXTURE/.momentum/sprints/index.json" <<'JSON'
{ "active": null, "planning": null, "completed": [] }
JSON
run_gate sprint complete
assert_refused "S8: completing with no active sprint must still exit non-zero"
assert_out "No active sprint to complete" "S8: the existing no-active message must be preserved verbatim"
echo "ok S8 — no-active behavior unchanged, so idempotent-resume conventions keep holding"

echo "PASS"
