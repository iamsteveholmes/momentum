#!/usr/bin/env bash
# b3-canvas-update-render-epics-instead-of-features smoke contract
# Harness profile: bash
#
# Black-box verification: with epics.json present, the canvas server starts,
# the epics lens route returns HTML with the new section id, the epic detail
# route renders lifecycle and audience, and the legacy features routes no
# longer respond as the primary surface.
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-05-26/specs/b3-canvas-update-render-epics-instead-of-features.smoke.sh

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

PORT=3456
BASE="http://localhost:$PORT"
EPICS_JSON="_bmad-output/planning-artifacts/epics.json"

test -f "$EPICS_JSON" || {
  echo "FAIL: $EPICS_JSON missing — B1 must land before B3 smoke runs"
  exit 1
}

# Pick a known epic_slug from epics.json to exercise the detail route.
KNOWN_SLUG=$(python3 -c "
import json
with open('$EPICS_JSON') as f:
    epics = json.load(f)
print(next(iter(epics.keys())))
")

[[ -n "$KNOWN_SLUG" ]] || {
  echo "FAIL: could not extract a known epic_slug from $EPICS_JSON"
  exit 1
}

# Pick a long-lived epic if any exists (for the human-review hint).
LONG_LIVED_SLUG=$(python3 -c "
import json
with open('$EPICS_JSON') as f:
    epics = json.load(f)
for slug, entry in epics.items():
    if entry.get('lifecycle') == 'long-lived':
        print(slug); break
" || true)

# --- Start the canvas server in the background ------------------------------

# Use the project's canonical launch path (per the canvas SKILL).
bun --hot skills/momentum/skills/canvas/server.tsx >/tmp/b3-canvas.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT

# Wait for readiness (poll up to 30s).
for i in $(seq 1 30); do
  if curl -sf "$BASE/" -o /dev/null; then
    break
  fi
  sleep 1
done

curl -sf "$BASE/" -o /dev/null || {
  echo "FAIL: canvas server did not become ready on $BASE within 30s"
  echo "--- server log ---"
  cat /tmp/b3-canvas.log || true
  exit 1
}

# --- /lenses/epics returns 200 HTML with the new section id ------------------

LENS_HTML=$(curl -sS "$BASE/lenses/epics")
echo "$LENS_HTML" | grep -q 'lens-epics' || {
  echo "FAIL: /lenses/epics response does not contain section id 'lens-epics'"
  exit 1
}
echo "$LENS_HTML" | grep -qiE 'epic' || {
  echo "FAIL: /lenses/epics response does not mention 'epic'"
  exit 1
}

# --- /epics/:slug renders the known epic with lifecycle + audience ----------

DETAIL_HTML=$(curl -sS "$BASE/epics/$KNOWN_SLUG")
echo "$DETAIL_HTML" | grep -qE 'finite-lived|long-lived' || {
  echo "FAIL: /epics/$KNOWN_SLUG response does not surface lifecycle"
  exit 1
}
echo "$DETAIL_HTML" | grep -qE 'user|internal' || {
  echo "FAIL: /epics/$KNOWN_SLUG response does not surface audience"
  exit 1
}

# --- Legacy /lenses/features should no longer be the primary epics surface --
# (Either 404, or alias/redirect to /lenses/epics — both acceptable.) The
# critical check is that no NEW feature-layer presence remains.
LEGACY_FEAT=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/features/$KNOWN_SLUG")
if [[ "$LEGACY_FEAT" == "200" ]]; then
  # If 200, it must serve the new epic content (alias), not a stale "feature" page.
  curl -sS "$BASE/features/$KNOWN_SLUG" | grep -qE 'No features found' && {
    echo "FAIL: /features/$KNOWN_SLUG still serves the legacy feature placeholder"
    exit 1
  } || true
fi

# --- A graceful not-found for an unknown slug -------------------------------

NF_HTML=$(curl -sS "$BASE/epics/definitely-not-a-real-epic-xyz")
echo "$NF_HTML" | grep -qiE 'not found|no epic' || {
  echo "FAIL: /epics/<unknown> does not render a graceful not-found fragment"
  exit 1
}

# --- Sprint lens still renders unchanged (regression check) -----------------

SPRINT_HTML=$(curl -sS "$BASE/lenses/sprint")
echo "$SPRINT_HTML" | grep -qiE 'sprint' || {
  echo "FAIL: /lenses/sprint response no longer renders"
  exit 1
}

# --- Cycle lens still renders unchanged --------------------------------------

CYCLE_HTML=$(curl -sS "$BASE/lenses/cycle")
echo "$CYCLE_HTML" | grep -qiE 'cycle|timeline' || {
  echo "FAIL: /lenses/cycle response no longer renders"
  exit 1
}

# --- Optional: long-lived epic detail also renders cleanly ------------------

if [[ -n "$LONG_LIVED_SLUG" && "$LONG_LIVED_SLUG" != "$KNOWN_SLUG" ]]; then
  LL_HTML=$(curl -sS "$BASE/epics/$LONG_LIVED_SLUG")
  echo "$LL_HTML" | grep -q 'long-lived' || {
    echo "FAIL: long-lived epic $LONG_LIVED_SLUG does not surface lifecycle: long-lived"
    exit 1
  }
fi

echo "PASS"
