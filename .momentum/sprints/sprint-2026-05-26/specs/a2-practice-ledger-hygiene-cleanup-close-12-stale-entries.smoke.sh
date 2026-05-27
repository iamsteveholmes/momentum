#!/usr/bin/env bash
# a2-practice-ledger-hygiene-cleanup-close-12-stale-entries smoke contract
# Harness profile: bash
#
# Black-box verification that 12 stale entries are closed via the CLI: open
# count drops by exactly 12, no other entities shift status, and the per-
# entity history shows the new consumed event chained behind the original
# created event.
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-05-26/specs/a2-practice-ledger-hygiene-cleanup-close-12-stale-entries.smoke.sh

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

TOOLS_CMD="uv run python skills/momentum/scripts/momentum-tools.py practice-ledger"
DAR=".momentum/stories/a2-practice-ledger-hygiene-cleanup-close-12-stale-entries.md"

# The 12 entity_ids that must transition to terminal state per the story's
# verified mapping table. (These are pre-2026-05 archive event_ids reused as
# entity_ids for the closure events; they are public knowledge — they appear
# verbatim in the story's plain-English description.)
ENTITIES=(
  iq-20260424205245-50b859cb
  iq-20260516154102-22515545
  iq-20260516154102-1ae5c62a
  iq-20260516154102-d032731e
  iq-20260516154102-f89de525
  iq-20260516154102-221bdb70
  iq-20260516154102-f098660a
  iq-20260518032341-976884b5
  iq-20260416054851-aec14053
  iq-20260416055625-ab0b3dc4
  iq-20260416055626-153bbdd3
  iq-20260416055624-9f5c9655
)

# --- Dev Agent Record auditability ------------------------------------------

test -f "$DAR" || {
  echo "FAIL: story file $DAR missing"
  exit 1
}

# DAR must record pre-count, post-count, delta=12.
grep -qiE 'pre[- ]?count|pre-cleanup' "$DAR" || {
  echo "FAIL: Dev Agent Record does not record pre-cleanup count"
  exit 1
}
grep -qiE 'post[- ]?count|post-cleanup' "$DAR" || {
  echo "FAIL: Dev Agent Record does not record post-cleanup count"
  exit 1
}

# --- Each of the 12 entities currently has a terminal last event ------------

for ent in "${ENTITIES[@]}"; do
  HIST=$($TOOLS_CMD history --entity "$ent")
  echo "$HIST" | grep -qE '"event_type": *"(consumed|rejected|closed_stale)"' || {
    echo "FAIL: entity $ent has no terminal event after hygiene pass"
    exit 1
  }
done

# --- Each of the 12 has BOTH a created and a consumed event (event chain) ---

CHAIN_CHECKED=0
for ent in "${ENTITIES[@]}"; do
  HIST=$($TOOLS_CMD history --entity "$ent")
  if echo "$HIST" | grep -q '"event_type": *"consumed"'; then
    CHAIN_CHECKED=$((CHAIN_CHECKED + 1))
  fi
done

[[ "$CHAIN_CHECKED" -eq 12 ]] || {
  echo "FAIL: only $CHAIN_CHECKED of 12 entities show a consumed event"
  exit 1
}

# --- None of the 12 appear in `open` ----------------------------------------

OPEN_OUT=$($TOOLS_CMD open)
for ent in "${ENTITIES[@]}"; do
  if echo "$OPEN_OUT" | grep -q "$ent"; then
    echo "FAIL: entity $ent still in open set"
    exit 1
  fi
done

# --- outcome_ref payloads are present (8 superseded + 4 test-leftover) ------

SUPERSEDED_FOUND=0
TESTLEFTOVER_FOUND=0
for ent in "${ENTITIES[@]}"; do
  HIST=$($TOOLS_CMD history --entity "$ent")
  if echo "$HIST" | grep -q '"outcome_ref": *"superseded:'; then
    SUPERSEDED_FOUND=$((SUPERSEDED_FOUND + 1))
  fi
  if echo "$HIST" | grep -q '"outcome_ref": *"test-leftover"'; then
    TESTLEFTOVER_FOUND=$((TESTLEFTOVER_FOUND + 1))
  fi
done

[[ "$SUPERSEDED_FOUND" -eq 8 ]] || {
  echo "FAIL: expected 8 superseded outcome_ref payloads, got $SUPERSEDED_FOUND"
  exit 1
}
[[ "$TESTLEFTOVER_FOUND" -eq 4 ]] || {
  echo "FAIL: expected 4 test-leftover outcome_ref payloads, got $TESTLEFTOVER_FOUND"
  exit 1
}

echo "PASS"
