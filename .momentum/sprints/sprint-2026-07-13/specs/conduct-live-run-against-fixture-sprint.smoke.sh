#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: conduct-live-run-against-fixture-sprint
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-07-13/specs/conduct-live-run-against-fixture-sprint.smoke.sh
# how_dev_self_checks: Run this script; observe the driver's own PASS line and exit 0 echoed by the contract.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/conduct-live-run-against-fixture-sprint.md#acceptance-criteria
# platforms: [host]

# conduct-live-run-against-fixture-sprint smoke contract
# Harness profile: bash
#
# Invocation (from the Momentum repo root):
#   FIXTURE_DIR=~/projects/nornspun \
#   COMPOSED_SLUG=dev-kotlin-compose \
#   MATCH_PATH="composeApp/src/commonMain/kotlin/App.kt" \
#   NONMATCH_PATH="README.md" \
#   bash .momentum/sprints/sprint-2026-07-13/specs/conduct-live-run-against-fixture-sprint.smoke.sh
#
# Expected: the shipped driver is executed for real against the populated
# fixture, and its own stdout contains the line "PASS — all assertions
# hold." together with process exit code 0. This contract reads the
# verdict off that observed run only — never off a structured status
# field, a prior "done" marker, an agent self-report, or the mere
# existence of an evidence file. A harness "skip" or BLOCKED result is a
# FAILURE here, never a pass: this contract always executes the driver
# directly and reports its actual console output.

set -uo pipefail

FIXTURE_DIR="${FIXTURE_DIR:-$HOME/projects/nornspun}"
COMPOSED_SLUG="${COMPOSED_SLUG:-dev-kotlin-compose}"
MATCH_PATH="${MATCH_PATH:-composeApp/src/commonMain/kotlin/App.kt}"
NONMATCH_PATH="${NONMATCH_PATH:-README.md}"
DRIVER="skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh"

FAIL=0

echo "=== Precondition: fixture inputs present on disk ==="

MANIFESTO_PATH="${FIXTURE_DIR}/.claude/manifests/${COMPOSED_SLUG}.md"
AGENTS_JSON_PATH="${FIXTURE_DIR}/momentum/agents.json"
COMPOSED_AGENT_PATH="${FIXTURE_DIR}/.claude/guidelines/agents/${COMPOSED_SLUG}.md"

# Assert: fixture manifesto instance exists
if [ ! -f "$MANIFESTO_PATH" ]; then
  echo "FAIL: fixture manifesto not found at $MANIFESTO_PATH"
  FAIL=1
fi

# Assert: fixture agents.json exists
if [ ! -f "$AGENTS_JSON_PATH" ]; then
  echo "FAIL: fixture agents.json not found at $AGENTS_JSON_PATH"
  FAIL=1
fi

# Assert: composed agent file exists
if [ ! -f "$COMPOSED_AGENT_PATH" ]; then
  echo "FAIL: composed agent file not found at $COMPOSED_AGENT_PATH"
  FAIL=1
fi

# Assert: agents.json parses as JSON
if [ -f "$AGENTS_JSON_PATH" ] && ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$AGENTS_JSON_PATH" 2>/dev/null; then
  echo "FAIL: $AGENTS_JSON_PATH does not parse as JSON"
  FAIL=1
fi

# Assert: manifesto carries a non-empty File Ownership section
if [ -f "$MANIFESTO_PATH" ] && ! grep -q "## File Ownership" "$MANIFESTO_PATH"; then
  echo "FAIL: $MANIFESTO_PATH has no ## File Ownership section"
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo "FAIL: fixture preconditions not satisfied — see FAIL lines above."
  exit 1
fi

echo "Preconditions satisfied — fixture inputs present."
echo
echo "=== Executing shipped driver live against the fixture ==="

if [ ! -f "$DRIVER" ]; then
  echo "FAIL: driver not found at $DRIVER (run this contract from the Momentum repo root)"
  exit 1
fi

if DRIVER_OUTPUT=$(FIXTURE_DIR="$FIXTURE_DIR" \
  COMPOSED_SLUG="$COMPOSED_SLUG" \
  MATCH_PATH="$MATCH_PATH" \
  NONMATCH_PATH="$NONMATCH_PATH" \
  bash "$DRIVER" 2>&1); then
  DRIVER_EXIT=0
else
  DRIVER_EXIT=$?
fi

echo "----- observed driver stdout -----"
echo "$DRIVER_OUTPUT"
echo "----- end observed driver stdout -----"
echo "observed driver exit code: $DRIVER_EXIT"

# Acceptance is the driver's OWN observed console output + exit code —
# never a structured status field, a prior "done" marker, an agent
# self-report, or the mere presence of the evidence file. A harness
# "skip"/BLOCKED result is a FAILURE for this contract, not a pass: this
# contract always executes the driver directly, so no skip path exists.
if [ "$DRIVER_EXIT" -ne 0 ]; then
  echo "FAIL: driver exited $DRIVER_EXIT (expected 0). This is the observed FAILURE verdict — remediate the fixture and re-run."
  exit 1
fi

if ! echo "$DRIVER_OUTPUT" | grep -qF "PASS — all assertions hold."; then
  echo "FAIL: driver exited 0 but its stdout did not contain the required line 'PASS — all assertions hold.'"
  exit 1
fi

PASS_LINE_COUNT=$(echo "$DRIVER_OUTPUT" | grep -c "^PASS:" || true)
if [ "$PASS_LINE_COUNT" -lt 4 ]; then
  echo "FAIL: expected at least 4 named 'PASS:' assertion lines in the observed driver output, found $PASS_LINE_COUNT"
  exit 1
fi

echo "PASS"
