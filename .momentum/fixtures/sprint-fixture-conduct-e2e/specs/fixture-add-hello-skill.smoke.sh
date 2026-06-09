#!/usr/bin/env bash
# fixture-add-hello-skill smoke contract
#
# === VERIFICATION HEADER (Part A) ===
# story_slug: fixture-add-hello-skill
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/fixtures/sprint-fixture-conduct-e2e/specs/fixture-add-hello-skill.smoke.sh
# how_dev_self_checks: |
#   This is a fixture story for end-to-end conductor testing.
#   Run this script directly: it asserts the fixture output file exists at the
#   expected path, confirming a trivial "add file" story was completed.
#   Pass = file present at expected location; Fail = file absent.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/fixtures/sprint-fixture-conduct-e2e/stories/fixture-add-hello-skill.md#acceptance-criteria
# platforms: [host]
#
# === VERIFIER CONTRACT BODY (Part B) ===
# Invocation:
#   bash .momentum/fixtures/sprint-fixture-conduct-e2e/specs/fixture-add-hello-skill.smoke.sh
#
# Expected: The fixture output file exists at the expected location.

set -uo pipefail

FAILED=0
note_fail() { echo "FAIL: $1"; FAILED=1; }

# Determine project root (two levels up from this script's .momentum/fixtures/... path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"

EXPECTED_FILE="$PROJECT_ROOT/.momentum/fixtures/sprint-fixture-conduct-e2e/output/hello-skill-output.txt"

if [ -f "$EXPECTED_FILE" ]; then
  echo "found: $EXPECTED_FILE"
else
  note_fail "expected fixture output file not found: $EXPECTED_FILE"
fi

if [ "$FAILED" -ne 0 ]; then
  echo "RESULT: FAIL — fixture-add-hello-skill output file absent"
  exit 1
fi

echo "PASS — fixture-add-hello-skill output file present"
