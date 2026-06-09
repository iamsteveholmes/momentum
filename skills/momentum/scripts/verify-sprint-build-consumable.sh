#!/usr/bin/env bash
# verify-sprint-build-consumable.sh
#
# Producer→consumer verification artifact for Momentum sprint records.
#
# PURPOSE:
#   Asserts that a sprint record (from sprints/index.json active block, OR a named
#   fixture sprint index.json) is BUILD-CONSUMABLE by the Conductor. For each story
#   in the sprint's story_assignments, checks:
#     (a) contract.path exists on disk
#     (b) frozen_sha256 matches the on-disk file's sha256
#     (c) contract carries a standard Part-A "=== VERIFICATION HEADER ===" header
#     (d) verification_method is a valid driver_bindings key in verification-harness.json
#     (e) coverage_disposition is a recognized value (dedicated-run|covered-by-composition)
#
# USAGE:
#   # Check live active sprint (default):
#   bash skills/momentum/scripts/verify-sprint-build-consumable.sh
#
#   # Check a named fixture sprint index.json:
#   bash skills/momentum/scripts/verify-sprint-build-consumable.sh \
#       --sprint-index .momentum/fixtures/sprint-fixture-conduct-e2e/index.json
#
# EXIT CODES:
#   0 — all stories PASS (sprint record is build-consumable)
#   1 — one or more stories FAIL (names the offending story + field)
#
# LOCATION: skills/momentum/scripts/verify-sprint-build-consumable.sh

set -uo pipefail

# --- Argument parsing ---

SPRINT_INDEX=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --sprint-index)
      SPRINT_INDEX="$2"
      shift 2
      ;;
    --help|-h)
      grep '^#' "$0" | grep -v '#!/' | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# --- Locate project root (directory containing skills/ and .momentum/) ---

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# --- Locate Python for JSON parsing ---

if ! command -v python3 &>/dev/null; then
  echo "FATAL: python3 is required but not found on PATH" >&2
  exit 1
fi

# --- Resolve sprint index path ---

if [[ -z "$SPRINT_INDEX" ]]; then
  SPRINT_INDEX="$PROJECT_ROOT/.momentum/sprints/index.json"
  SPRINT_SOURCE="live active sprint"
else
  # If relative, anchor to working directory
  if [[ "$SPRINT_INDEX" != /* ]]; then
    SPRINT_INDEX="$PWD/$SPRINT_INDEX"
  fi
  SPRINT_SOURCE="fixture: $SPRINT_INDEX"
fi

if [[ ! -f "$SPRINT_INDEX" ]]; then
  echo "FATAL: sprint index not found: $SPRINT_INDEX" >&2
  exit 1
fi

echo "=== verify-sprint-build-consumable ==="
echo "Project root : $PROJECT_ROOT"
echo "Sprint index : $SPRINT_INDEX ($SPRINT_SOURCE)"
echo ""

# --- Load valid driver_bindings keys from verification-harness.json ---

HARNESS_FILE="$PROJECT_ROOT/momentum/verification-harness.json"
if [[ ! -f "$HARNESS_FILE" ]]; then
  echo "FATAL: verification-harness.json not found: $HARNESS_FILE" >&2
  exit 1
fi

# Extract driver_bindings keys (valid verification_method values)
VALID_VERIFICATION_METHODS="$(python3 - "$HARNESS_FILE" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    h = json.load(f)
keys = list(h.get("defaults", {}).get("driver_bindings", {}).keys())
print(" ".join(keys))
PYEOF
)"

if [[ -z "$VALID_VERIFICATION_METHODS" ]]; then
  echo "FATAL: could not extract driver_bindings keys from $HARNESS_FILE" >&2
  exit 1
fi

echo "Valid verification_method values: $VALID_VERIFICATION_METHODS"
echo ""

# Recognized coverage_disposition values
VALID_DISPOSITIONS="dedicated-run covered-by-composition"

# --- Extract story_assignments from sprint record ---
# Handle both:
#   Live sprints/index.json  → .active.team.story_assignments
#   Fixture sprint index.json → .team.story_assignments (has _fixture_note at root)

STORY_ASSIGNMENTS_JSON="$(python3 - "$SPRINT_INDEX" <<'PYEOF'
import json, sys

with open(sys.argv[1]) as f:
    d = json.load(f)

# Determine if this is a fixture file (has root-level _fixture_note or team at root)
# or a live sprints/index.json (has .active at root)
if "active" in d:
    # Live sprints/index.json
    active = d.get("active") or {}
    sa = active.get("team", {}).get("story_assignments", {})
    print(json.dumps(sa))
elif "team" in d:
    # Fixture sprint index (has team at root)
    sa = d.get("team", {}).get("story_assignments", {})
    print(json.dumps(sa))
else:
    print("{}")
PYEOF
)"

STORY_COUNT="$(python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(len(d))" <<< "$STORY_ASSIGNMENTS_JSON")"

if [[ "$STORY_COUNT" -eq 0 ]]; then
  echo "WARN: No story_assignments found in sprint record."
  echo "      If this is the live active sprint, it may not have contract blocks set yet."
  echo "      Against a fixture, this means the fixture is malformed."
  echo ""
  echo "RESULT: INCONCLUSIVE — 0 story_assignments to check"
  exit 1
fi

echo "Checking $STORY_COUNT story_assignments..."
echo ""

# --- Per-story validation ---

FAILED=0
PASS_COUNT=0
FAIL_COUNT=0

note_fail() {
  local story="$1"
  local field="$2"
  local reason="$3"
  echo "  FAIL [story=$story field=$field]: $reason"
  FAILED=1
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

note_pass() {
  local story="$1"
  echo "  PASS [$story]"
  PASS_COUNT=$((PASS_COUNT + 1))
}

# Iterate stories using Python to produce per-story data lines
python3 - "$STORY_ASSIGNMENTS_JSON" <<'PYEOF'
import json, sys

sa = json.loads(sys.argv[1])
for slug, assignment in sa.items():
    contract = assignment.get("contract") or {}
    vm = assignment.get("verification_method", "")
    path = contract.get("path", "")
    harness = contract.get("harness_profile", "")
    disposition = contract.get("coverage_disposition", "")
    covered_by = contract.get("covered_by_scenario", "")
    sha = contract.get("frozen_sha256", "")
    print(f"STORY|{slug}|{vm}|{path}|{harness}|{disposition}|{covered_by or ''}|{sha}")
PYEOF

while IFS='|' read -r tag slug vm path harness disposition covered_by sha; do
  [[ "$tag" != "STORY" ]] && continue

  echo "--- $slug ---"
  story_failed=0

  # (a) contract.path exists on disk
  if [[ -z "$path" ]]; then
    note_fail "$slug" "contract.path" "field is absent or empty"
    story_failed=1
  else
    FULL_PATH="$PROJECT_ROOT/$path"
    if [[ ! -f "$FULL_PATH" ]]; then
      note_fail "$slug" "contract.path" "file not found on disk: $path"
      story_failed=1
    else
      echo "  (a) contract.path: OK — $path"

      # (b) frozen_sha256 matches on-disk file
      if [[ -z "$sha" ]]; then
        note_fail "$slug" "frozen_sha256" "field is absent or empty"
        story_failed=1
      else
        ACTUAL_SHA="$(sha256sum "$FULL_PATH" | awk '{print $1}')"
        if [[ "$ACTUAL_SHA" != "$sha" ]]; then
          note_fail "$slug" "frozen_sha256" "mismatch — recorded=$sha actual=$ACTUAL_SHA"
          story_failed=1
        else
          echo "  (b) frozen_sha256: OK — $sha"
        fi
      fi

      # (c) contract carries standard Part-A VERIFICATION HEADER
      if ! grep -q '=== VERIFICATION HEADER' "$FULL_PATH"; then
        note_fail "$slug" "contract.header" "contract file missing standard '=== VERIFICATION HEADER' (Part A) header: $path"
        story_failed=1
      else
        echo "  (c) Part-A header: OK"
      fi
    fi
  fi

  # (d) verification_method is a valid driver_bindings key
  if [[ -z "$vm" ]]; then
    note_fail "$slug" "verification_method" "field is absent or empty"
    story_failed=1
  else
    vm_valid=0
    for valid_vm in $VALID_VERIFICATION_METHODS; do
      if [[ "$vm" == "$valid_vm" ]]; then
        vm_valid=1
        break
      fi
    done
    if [[ "$vm_valid" -eq 0 ]]; then
      note_fail "$slug" "verification_method" "unrecognized value '$vm' — valid: $VALID_VERIFICATION_METHODS"
      story_failed=1
    else
      echo "  (d) verification_method: OK — $vm"
    fi
  fi

  # (e) coverage_disposition is a recognized value
  if [[ -z "$disposition" ]]; then
    note_fail "$slug" "coverage_disposition" "field is absent or empty"
    story_failed=1
  else
    disp_valid=0
    for valid_disp in $VALID_DISPOSITIONS; do
      if [[ "$disposition" == "$valid_disp" ]]; then
        disp_valid=1
        break
      fi
    done
    if [[ "$disp_valid" -eq 0 ]]; then
      note_fail "$slug" "coverage_disposition" "unrecognized value '$disposition' — valid: $VALID_DISPOSITIONS"
      story_failed=1
    else
      echo "  (e) coverage_disposition: OK — $disposition"
    fi
  fi

  if [[ "$story_failed" -eq 0 ]]; then
    note_pass "$slug"
  fi
  echo ""

done < <(python3 - "$STORY_ASSIGNMENTS_JSON" <<'PYEOF'
import json, sys
sa = json.loads(sys.argv[1])
for slug, assignment in sa.items():
    contract = assignment.get("contract") or {}
    vm = assignment.get("verification_method", "")
    path = contract.get("path", "")
    harness = contract.get("harness_profile", "")
    disposition = contract.get("coverage_disposition", "")
    covered_by = contract.get("covered_by_scenario", "")
    sha = contract.get("frozen_sha256", "")
    print(f"STORY|{slug}|{vm}|{path}|{harness}|{disposition}|{covered_by or ''}|{sha}")
PYEOF
)

# --- Summary ---

echo "=== SUMMARY ==="
echo "Total stories : $STORY_COUNT"
echo "Passed        : $PASS_COUNT"
echo "Failed        : $FAIL_COUNT"
echo ""

if [[ "$FAILED" -ne 0 ]]; then
  echo "RESULT: FAIL — sprint record is NOT build-consumable"
  echo "        Fix the failing story/field entries above before running the conductor."
  exit 1
fi

echo "RESULT: PASS — sprint record is build-consumable"
echo "        All $PASS_COUNT stories have valid contracts, sha256 matches, Part-A headers, valid verification_method, and recognized coverage_disposition."
