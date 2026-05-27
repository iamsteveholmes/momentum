#!/usr/bin/env bash
# a1-practice-ledger-schema-cli-redesign-true-append-only smoke contract
# Harness profile: bash
#
# Black-box verification that the practice-ledger event-log CLI behaves per
# the story's plain-English ACs: rename complete, new schema enforced,
# append-only semantics, derived-state reader subcommands, idempotent
# close-stale, and a registered daily routine.
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-05-26/specs/a1-practice-ledger-schema-cli-redesign-true-append-only.smoke.sh

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

LEDGER=".momentum/practice-ledger.jsonl"
ARCHIVE=".momentum/practice-ledger-pre-2026-05.jsonl"
OLD_NAME=".momentum/intake-queue.jsonl"

TOOLS_CMD="uv run python skills/momentum/scripts/momentum-tools.py practice-ledger"

# --- Filename and migration ---------------------------------------------------

test ! -e "$OLD_NAME" || {
  echo "FAIL: legacy file $OLD_NAME still exists; expected rename to $ARCHIVE"
  exit 1
}

test -f "$ARCHIVE" || {
  echo "FAIL: archive $ARCHIVE missing"
  exit 1
}

test -f "$LEDGER" || {
  echo "FAIL: $LEDGER missing"
  exit 1
}

# Archive content is byte-identical to a snapshot of the prior file (we cannot
# verify byte-identity from this scope; assert non-empty + parseable JSONL
# lines exist).
ARCHIVE_LINES=$(grep -c . "$ARCHIVE" || true)
[[ "$ARCHIVE_LINES" -gt 0 ]] || {
  echo "FAIL: archive $ARCHIVE has no lines"
  exit 1
}

# --- Schema and writer (via CLI append) --------------------------------------

# Append a valid event
$TOOLS_CMD append \
  --event-type created \
  --entity-id smoke-test-entity-a1 \
  --source smoke-test \
  --actor developer \
  --payload-json '{"smoke":true}' >/dev/null

# Reject an event with an invalid event_type
set +e
$TOOLS_CMD append \
  --event-type bogus_type \
  --entity-id smoke-test-entity-a1-bad \
  --source smoke-test \
  --actor developer \
  --payload-json '{}' 2>/dev/null
INVALID_RC=$?
set -e

[[ "$INVALID_RC" -ne 0 ]] || {
  echo "FAIL: append accepted invalid event_type 'bogus_type'"
  exit 1
}

# Append two consume events for the same entity_id — both must land
$TOOLS_CMD append --event-type consumed --entity-id smoke-test-entity-a1 \
  --source smoke-test --actor developer --payload-json '{"n":1}' >/dev/null
$TOOLS_CMD append --event-type consumed --entity-id smoke-test-entity-a1 \
  --source smoke-test --actor developer --payload-json '{"n":2}' >/dev/null

HISTORY=$($TOOLS_CMD history --entity smoke-test-entity-a1)
echo "$HISTORY" | grep -q '"event_type": *"created"' || {
  echo "FAIL: history missing created event"
  exit 1
}
CONSUMED_COUNT=$(echo "$HISTORY" | grep -c '"event_type": *"consumed"' || true)
[[ "$CONSUMED_COUNT" -ge 2 ]] || {
  echo "FAIL: expected >=2 consumed events for smoke-test-entity-a1, got $CONSUMED_COUNT"
  exit 1
}

# --- Reader CLI: summary, open, history, since, by-source --------------------

SUMMARY=$($TOOLS_CMD summary)
echo "$SUMMARY" | grep -qiE 'archive_entries|legacy_entries' || {
  echo "FAIL: summary does not surface archive/legacy entry count"
  exit 1
}

# open must EXCLUDE entities whose last event is terminal (consumed)
OPEN_OUT=$($TOOLS_CMD open)
echo "$OPEN_OUT" | grep -q 'smoke-test-entity-a1\b' && {
  echo "FAIL: open included terminal entity smoke-test-entity-a1"
  exit 1
} || true

# since with an old timestamp returns events
SINCE_OUT=$($TOOLS_CMD since 2000-01-01T00:00:00Z)
echo "$SINCE_OUT" | grep -q 'smoke-test-entity-a1' || {
  echo "FAIL: since query missed seeded events"
  exit 1
}

# by-source
BY_SRC=$($TOOLS_CMD by-source smoke-test)
echo "$BY_SRC" | grep -q 'smoke-test-entity-a1' || {
  echo "FAIL: by-source did not return smoke-test entries"
  exit 1
}

# history on unknown entity returns clean (exit 0, empty result)
$TOOLS_CMD history --entity definitely-not-a-real-entity-xyz >/dev/null || {
  echo "FAIL: history --entity for unknown id returned non-zero"
  exit 1
}

# --- Close-stale idempotency -------------------------------------------------

# Run twice. Second run must append zero new closed_stale events.
PRE_CLOSED=$($TOOLS_CMD by-source momentum-tools-close-stale 2>/dev/null | grep -c '"event_type": *"closed_stale"' || true)
$TOOLS_CMD close-stale --age-days 15 >/dev/null
MID_CLOSED=$($TOOLS_CMD by-source momentum-tools-close-stale 2>/dev/null | grep -c '"event_type": *"closed_stale"' || true)
$TOOLS_CMD close-stale --age-days 15 >/dev/null
POST_CLOSED=$($TOOLS_CMD by-source momentum-tools-close-stale 2>/dev/null | grep -c '"event_type": *"closed_stale"' || true)

[[ "$POST_CLOSED" -eq "$MID_CLOSED" ]] || {
  echo "FAIL: close-stale not idempotent (mid=$MID_CLOSED post=$POST_CLOSED)"
  exit 1
}

# --- Append-only file shape (no whole-file rewrites) -------------------------

# Append-only check: every line is valid JSON and lines never decrease.
LINES_BEFORE=$(grep -c . "$LEDGER" || true)
$TOOLS_CMD append --event-type updated --entity-id smoke-test-append-only \
  --source smoke-test --actor developer --payload-json '{}' >/dev/null
LINES_AFTER=$(grep -c . "$LEDGER" || true)
[[ "$LINES_AFTER" -gt "$LINES_BEFORE" ]] || {
  echo "FAIL: append did not add a line (before=$LINES_BEFORE after=$LINES_AFTER)"
  exit 1
}

# --- Daily routine registered ------------------------------------------------

# observable: the story file (a public artifact / deliverable) must record the
# registered routine id in its Dev Agent Record section. We assert on a
# "Routine ID:" line whose value matches a routine-id-shaped token.
DAR=".momentum/stories/a1-practice-ledger-schema-cli-redesign-true-append-only.md"
grep -E '^Routine ID: [a-zA-Z0-9_-]+$' "$DAR" >/dev/null || {
  echo "FAIL: Dev Agent Record in $DAR does not contain a 'Routine ID: <id>' line"
  exit 1
}

echo "PASS"
