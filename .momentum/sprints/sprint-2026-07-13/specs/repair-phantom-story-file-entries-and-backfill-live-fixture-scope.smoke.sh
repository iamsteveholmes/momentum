#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: repair-phantom-story-file-entries-and-backfill-live-fixture-scope
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-07-13/specs/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.md#acceptance-criteria
# platforms: [host]

# repair-phantom-story-file-entries-and-backfill-live-fixture-scope smoke contract
# Harness profile: bash
#
# Invocation:
#   ./.momentum/sprints/sprint-2026-07-13/specs/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.smoke.sh
#   (run from the project root)
#
# Expected: the project's story index carries zero entries that claim a
# backing story file with none present on disk; the six previously-phantom
# stories now exist on disk as enrichment-ready backlog stubs; and the
# story-registration command refuses to let a new phantom entry back in.
#
# Seam under test — Producer/Consumer:
#   Producer: the story-registration command that writes entries into the
#             project's story index.
#   Consumer: anything that trusts an index entry marked "has a story file"
#             (for example, a planning process that previously crashed when
#             it selected an entry with no backing file on disk).
#   Match scenario:    register a slug whose backing file already exists on
#                      disk -> the entry is accepted and marked as having a
#                      file.
#   Mismatch scenario: register a slug with no backing file on disk -> the
#                      command must not silently accept it as "has a file."

set -uo pipefail

FAIL=0

echo "== Assertion 1: every story-index entry claiming a file has one on disk =="
SCAN=$(python3 - <<'PYEOF'
import json, os
with open(".momentum/stories/index.json") as f:
    data = json.load(f)
count = 0
for slug, entry in data.items():
    if not isinstance(entry, dict):
        continue
    if entry.get("story_file") is True and not os.path.isfile(f".momentum/stories/{slug}.md"):
        print(f"PHANTOM: {slug}")
        count += 1
print(f"PHANTOMS: {count}")
PYEOF
)
echo "$SCAN"
echo "$SCAN" | grep -q "^PHANTOMS: 0$" || {
  echo "FAIL: story index still contains phantom entries (see PHANTOM lines above)"
  FAIL=1
}

echo "== Assertion 2: the six previously-phantom stories exist as enrichment-ready backlog stubs =="
PHANTOM_SLUGS=(
  "build-guidelines-invocation-surface-in-sprint-planning"
  "canvas-gate-review-surface-epic"
  "dag-dispatch-blast-radius-discovery"
  "endgate-format-spec-section00-alignment"
  "re-emit-frozen-app-ui-contracts-via-producer"
  "verification-method-two-column-smoke-ui-model"
)
for slug in "${PHANTOM_SLUGS[@]}"; do
  FILE=".momentum/stories/${slug}.md"
  if [ ! -f "$FILE" ]; then
    echo "FAIL: no backing file for $slug"
    FAIL=1
    continue
  fi
  grep -qi "status: backlog" "$FILE" || {
    echo "FAIL: $slug is missing status: backlog"
    FAIL=1
  }
  grep -qi "backlog stub" "$FILE" || {
    echo "FAIL: $slug is missing the enrichment-ready backlog-stub disclaimer"
    FAIL=1
  }
done

echo "== Assertion 3: the story-registration command rejects a phantom registration =="
SANDBOX=$(mktemp -d)
cleanup() { rm -rf "$SANDBOX"; }
trap cleanup EXIT

git init -q "$SANDBOX"
mkdir -p "$SANDBOX/.momentum/stories"
echo '{}' > "$SANDBOX/.momentum/stories/index.json"

# --- Mismatch scenario: register a slug with no backing file on disk ---
MISMATCH_SLUG="contract-probe-mismatch-$$"
MISMATCH_OUT=$(cd "$SANDBOX" && momentum-tools sprint story-add \
  --slug "$MISMATCH_SLUG" --title "Contract probe" --epic momentum-conductor-core 2>&1)
MISMATCH_STATUS=$?

if [ "$MISMATCH_STATUS" -ne 0 ]; then
  echo "Registration was refused outright for a missing-file slug (exit $MISMATCH_STATUS)."
else
  echo "$MISMATCH_OUT" | grep -q '"story_file": true' && {
    echo "FAIL: command accepted a phantom registration (story_file: true with no backing file on disk)"
    echo "$MISMATCH_OUT"
    FAIL=1
  }
fi

# --- Match scenario: register a slug whose backing file already exists on disk ---
MATCH_SLUG="contract-probe-match-$$"
echo "# probe" > "$SANDBOX/.momentum/stories/${MATCH_SLUG}.md"
MATCH_OUT=$(cd "$SANDBOX" && momentum-tools sprint story-add \
  --slug "$MATCH_SLUG" --title "Contract probe" --epic momentum-conductor-core 2>&1)
MATCH_STATUS=$?

if [ "$MATCH_STATUS" -ne 0 ]; then
  echo "FAIL: registration was refused for a slug whose backing file exists on disk"
  echo "$MATCH_OUT"
  FAIL=1
else
  echo "$MATCH_OUT" | grep -q '"story_file": true' || {
    echo "FAIL: command did not mark a file-backed registration as story_file: true"
    echo "$MATCH_OUT"
    FAIL=1
  }
fi

if [ "$FAIL" -ne 0 ]; then
  echo "FAIL"
  exit 1
fi

echo "PASS"
exit 0
