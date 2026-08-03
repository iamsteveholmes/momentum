#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: daily-tasting-reminder-expected-vs-reality-brief-generator
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-08-03/specs/daily-tasting-reminder-expected-vs-reality-brief-generator.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/daily-tasting-reminder-expected-vs-reality-brief-generator.md#acceptance-criteria
# platforms: [host]

# daily-tasting-reminder-expected-vs-reality-brief-generator smoke contract
# Harness profile: bash
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-08-03/specs/daily-tasting-reminder-expected-vs-reality-brief-generator.smoke.sh
#
# Expected: `momentum-tools tasting brief` writes a dated brief to
# .momentum/tasting/brief-<YYYY-MM-DD>.md that quotes the registry's passing
# acceptance conditions verbatim (capped at 7, remainder collapsed), states in
# plain language which walkthrough window it used (never wider than the 14-day
# bounded default), and closes with findings routing to intake at critical
# priority. `momentum-tools tasting status --json` reports due-ness, the
# days-since count, and a prominence tier (quiet / insistent / leading). Both
# commands treat .momentum/features.json as strictly read-only and exit 0 on
# every input — including absent, empty, malformed, and field-degraded
# registries, and a project directory with no git history (every fixture below
# is a bare temp dir with no git history at all).
#
# Producer / Consumer scope (seam story — CONSUMER side):
#   Producer: `momentum-tools feature verify` — the sole writer of
#     .momentum/features.json (built by the sibling story in this sprint). This
#     contract never invokes the producer.
#   Consumer (under test here): `momentum-tools tasting brief` and
#     `momentum-tools tasting status` — read-only consumers of
#     .momentum/features.json. This contract exercises the consumer side only,
#     against fixture registries in the shape the producer contract pins: a flat
#     top-level map keyed by feature slug (no wrapper object), each entry
#     carrying name, acceptance_condition, status (absent | failing | passing),
#     and last_verified {date (ISO), verdict ("pass"/"fail" lowercase),
#     backend_sha, client_sha} — plus an optional evidence text that is
#     present-but-not-asserted here pending the flagged D1 extension.
#   Seam failure mode, named: if the consumer crashes on — or silently accepts
#     but misreads — a registry entry whose expected fields are missing or
#     shaped differently (e.g. last_verified without a date, a passing feature
#     without an acceptance_condition), that is a cross-side field-shape
#     incompatibility and a FAIL here. The required behavior is honest
#     degradation: exit 0 and a plain-language statement of the degraded
#     window/claims.

set -euo pipefail

fail() { echo "FAIL: $1"; exit 1; }
json_ok() { python3 -c 'import json,sys; json.load(sys.stdin)' >/dev/null 2>&1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
MT="${MOMENTUM_TOOLS:-$REPO_ROOT/skills/momentum/bin/momentum-tools}"
if [ ! -x "$MT" ]; then
  if command -v momentum-tools >/dev/null 2>&1; then
    MT="$(command -v momentum-tools)"
  else
    fail "momentum-tools CLI not found (looked at $MT and on PATH)"
  fi
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/tasting-smoke.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

TODAY="$(date +%Y-%m-%d)"
D2="$(python3 -c 'import datetime;print((datetime.date.today()-datetime.timedelta(days=2)).isoformat())')"
D5="$(python3 -c 'import datetime;print((datetime.date.today()-datetime.timedelta(days=5)).isoformat())')"

# ---------------------------------------------------------------------------
# Scenario 1 — seam AGREE case: populated registry with passing entries and
# last_verified dates -> brief names those features, quotes their acceptance
# conditions verbatim, and states the 14-day-capped window in plain language.
# ---------------------------------------------------------------------------
echo "--- Scenario 1: populated registry (seam agree case)"
P1="$WORK/populated"; mkdir -p "$P1/.momentum"
cat > "$P1/.momentum/features.json" <<'EOF'
{
  "tide-chart-overlay": {
    "name": "Tide chart overlay",
    "acceptance_condition": "Owner sees the seven-day tide chart overlay render on the harbor screen",
    "status": "passing",
    "last_verified": { "date": "2026-01-05", "verdict": "pass", "backend_sha": "a1b2c3d", "client_sha": "e7f8a9b" }
  },
  "catch-log-quick-entry": {
    "name": "Catch log quick entry",
    "acceptance_condition": "Owner records a catch in under fifteen seconds from the home screen",
    "status": "passing",
    "last_verified": { "date": "2026-01-03", "verdict": "pass", "backend_sha": "d4e5f6a", "client_sha": "b1c2d3e" }
  },
  "route-replay": {
    "name": "Route replay",
    "acceptance_condition": "Owner replays yesterday's route as an animated track",
    "status": "failing"
  }
}
EOF
REG1="$P1/.momentum/features.json"
BEFORE1="$(cksum "$REG1")"

if ! CLAUDE_PROJECT_DIR="$P1" "$MT" tasting brief > "$WORK/s1-brief.out" 2>&1; then
  fail "tasting brief exited non-zero on a well-formed populated registry (cross-side field-shape incompatibility on the agree case) — output: $(cat "$WORK/s1-brief.out")"
fi
BRIEF1="$P1/.momentum/tasting/brief-$TODAY.md"
[ -f "$BRIEF1" ] || fail "expected brief at .momentum/tasting/brief-$TODAY.md was not written"

grep -qF "Owner sees the seven-day tide chart overlay render on the harbor screen" "$BRIEF1" \
  || fail "brief does not quote the first passing acceptance condition verbatim (if the command ran but surfaced no claims from well-formed entries, treat as cross-side field-shape incompatibility between fixture entries and the registry reader)"
grep -qF "Owner records a catch in under fifteen seconds from the home screen" "$BRIEF1" \
  || fail "brief does not quote the second passing acceptance condition verbatim"
if grep -qF "Owner replays yesterday's route as an animated track" "$BRIEF1"; then
  fail "brief presents a failing feature's acceptance condition as a claim to test — only features marked passing are claims"
fi
grep -Eq 'tide-chart-overlay|catch-log-quick-entry' "$BRIEF1" \
  || fail "brief never names a passing feature slug — each probe must name the feature slug whose claim it tests"
grep -Eqi '14[- ]day' "$BRIEF1" \
  || fail "brief does not state the 14-day-capped window in plain language (newest recorded verdict predates the bound, so the bounded 14-day default window applies and must be stated with its reason)"
grep -qi 'intake' "$BRIEF1" \
  || fail "brief lacks the findings-routing footer directing walkthrough observations to intake"
grep -qi 'critical' "$BRIEF1" \
  || fail "brief's findings-routing footer does not state critical priority for owner-sourced findings"

AFTER1="$(cksum "$REG1")"
[ "$BEFORE1" = "$AFTER1" ] || fail "tasting brief modified .momentum/features.json — this consumer is read-only; only the feature verify command writes the registry"

if ! CLAUDE_PROJECT_DIR="$P1" "$MT" tasting brief --json > "$WORK/s1-json.out" 2>"$WORK/s1-json.err"; then
  fail "tasting brief --json exited non-zero"
fi
json_ok < "$WORK/s1-json.out" \
  || fail "tasting brief --json did not print a machine-readable JSON summary to stdout"

# ---------------------------------------------------------------------------
# Scenario 2 — same-day rerun regenerates the brief in place.
# ---------------------------------------------------------------------------
echo "--- Scenario 2: same-day rerun is safe"
if ! CLAUDE_PROJECT_DIR="$P1" "$MT" tasting brief > "$WORK/s2.out" 2>&1; then
  fail "same-day rerun of tasting brief exited non-zero — rerun must regenerate, not error"
fi
COUNT_TODAY="$(find "$P1/.momentum/tasting" -name "*${TODAY}*" | wc -l | tr -d ' ')"
[ "$COUNT_TODAY" = "1" ] || fail "same-day reruns left $COUNT_TODAY files for $TODAY — expected exactly one brief, regenerated in place, no duplicates"

# ---------------------------------------------------------------------------
# Scenario 3 — status tiers rise with days-since; status never writes.
# ---------------------------------------------------------------------------
echo "--- Scenario 3: status due-ness and prominence tiers"
BEFORE3="$(cksum "$REG1")"
if ! CLAUDE_PROJECT_DIR="$P1" "$MT" tasting status --json > "$WORK/s3-leading.out" 2>&1; then
  fail "tasting status --json exited non-zero on a populated registry"
fi
json_ok < "$WORK/s3-leading.out" || fail "tasting status --json output is not valid JSON"
grep -q 'leading' "$WORK/s3-leading.out" \
  || fail "status does not report the leading tier when the last verdict is months old (8 or more days => leading)"
grep -qi 'days' "$WORK/s3-leading.out" \
  || fail "status --json does not report the days-since count"
AFTER3="$(cksum "$REG1")"
[ "$BEFORE3" = "$AFTER3" ] || fail "tasting status modified .momentum/features.json — the registry is read-only for this consumer"

P3Q="$WORK/recent-quiet"; mkdir -p "$P3Q/.momentum"
cat > "$P3Q/.momentum/features.json" <<EOF
{ "tide-chart-overlay": {
  "name": "Tide chart overlay",
  "acceptance_condition": "Owner sees the seven-day tide chart overlay render on the harbor screen",
  "status": "passing",
  "last_verified": { "date": "$D2", "verdict": "pass", "backend_sha": "a1b2c3d", "client_sha": "e7f8a9b" }
} }
EOF
if ! CLAUDE_PROJECT_DIR="$P3Q" "$MT" tasting status --json > "$WORK/s3-quiet.out" 2>&1; then
  fail "tasting status --json exited non-zero on a registry verified 2 days ago"
fi
grep -q 'quiet' "$WORK/s3-quiet.out" \
  || fail "status does not report the quiet tier at 2 days since the last verdict (1-3 days => quiet)"

if ! CLAUDE_PROJECT_DIR="$P3Q" "$MT" tasting brief > "$WORK/s3-brief.out" 2>&1; then
  fail "tasting brief exited non-zero on a registry verified 2 days ago"
fi
BRIEF3="$P3Q/.momentum/tasting/brief-$TODAY.md"
[ -f "$BRIEF3" ] || fail "brief was not written for the recently-verified registry"
grep -Eq "($D2|2[- ]day)" "$BRIEF3" \
  || fail "brief does not state the walkthrough window it derived from the newest recorded verdict date ($D2)"

P3I="$WORK/recent-insistent"; mkdir -p "$P3I/.momentum"
cat > "$P3I/.momentum/features.json" <<EOF
{ "tide-chart-overlay": {
  "name": "Tide chart overlay",
  "acceptance_condition": "Owner sees the seven-day tide chart overlay render on the harbor screen",
  "status": "passing",
  "last_verified": { "date": "$D5", "verdict": "pass", "backend_sha": "a1b2c3d", "client_sha": "e7f8a9b" }
} }
EOF
if ! CLAUDE_PROJECT_DIR="$P3I" "$MT" tasting status --json > "$WORK/s3-insistent.out" 2>&1; then
  fail "tasting status --json exited non-zero on a registry verified 5 days ago"
fi
grep -q 'insistent' "$WORK/s3-insistent.out" \
  || fail "status does not report the insistent tier at 5 days since the last verdict (4-7 days => insistent)"

# ---------------------------------------------------------------------------
# Scenario 4 — claims cap: with more than 7 passing features, the 7 most
# recently verified are quoted and the remainder collapses (their acceptance
# conditions do not appear).
# ---------------------------------------------------------------------------
echo "--- Scenario 4: claims capped at 7, remainder collapsed"
PCAP="$WORK/cap"; mkdir -p "$PCAP/.momentum"
python3 - "$PCAP/.momentum/features.json" <<'PY'
import json, sys
feats = {}
for i in range(1, 10):
    feats[f"cap-feature-{i:02d}"] = {
        "name": f"Cap feature {i:02d}",
        "acceptance_condition": f"Owner verifies claim number {i:02d} in the running app",
        "status": "passing",
        "last_verified": {"date": f"2026-07-{i:02d}", "verdict": "pass", "backend_sha": "abc1234", "client_sha": "def5678"},
    }
with open(sys.argv[1], "w") as fh:
    json.dump(feats, fh, indent=2)
PY
if ! CLAUDE_PROJECT_DIR="$PCAP" "$MT" tasting brief > "$WORK/s4.out" 2>&1; then
  fail "tasting brief exited non-zero on a registry with 9 passing features"
fi
BRIEF4="$PCAP/.momentum/tasting/brief-$TODAY.md"
[ -f "$BRIEF4" ] || fail "brief was not written for the 9-passing-feature registry"
grep -qF "Owner verifies claim number 09 in the running app" "$BRIEF4" \
  || fail "brief omits the most recently verified passing claim — the 7 most recently verified must appear"
grep -qF "Owner verifies claim number 03 in the running app" "$BRIEF4" \
  || fail "brief omits the 7th most recently verified passing claim — the cap is 7, not fewer"
if grep -qF "Owner verifies claim number 01 in the running app" "$BRIEF4"; then
  fail "brief quotes an 8th+ passing claim (oldest verified) — beyond 7, claims must collapse to a single count line"
fi
if grep -qF "Owner verifies claim number 02 in the running app" "$BRIEF4"; then
  fail "brief quotes an 8th+ passing claim (second oldest verified) — beyond 7, claims must collapse to a single count line"
fi

# ---------------------------------------------------------------------------
# Scenario 5 — seam DISAGREE case: entries missing last_verified.date or
# acceptance_condition. The command must still exit 0 and state the degraded
# window/claims in plain language. A crash — or silent acceptance of a wrong
# shape that misreads the registry — is the FAIL: cross-side field-shape
# incompatibility between producer-written entries and this consumer.
# ---------------------------------------------------------------------------
echo "--- Scenario 5: degraded field shapes (seam disagree case)"
P5="$WORK/degraded"; mkdir -p "$P5/.momentum"
cat > "$P5/.momentum/features.json" <<'EOF'
{
  "fog-horn-alerts": {
    "name": "Fog horn alerts",
    "status": "passing",
    "last_verified": { "verdict": "pass", "backend_sha": "f0f0f0f", "client_sha": "0a0a0a0" }
  },
  "mooring-fee-tracker": {
    "name": "Mooring fee tracker",
    "acceptance_condition": "Owner logs a mooring fee and sees the season total update",
    "status": "passing"
  }
}
EOF
REG5="$P5/.momentum/features.json"
BEFORE5="$(cksum "$REG5")"
if ! CLAUDE_PROJECT_DIR="$P5" "$MT" tasting brief > "$WORK/s5-brief.out" 2>&1; then
  fail "tasting brief crashed on entries missing last_verified.date / acceptance_condition — cross-side field-shape incompatibility; required behavior is exit 0 with plain-language degradation — output: $(cat "$WORK/s5-brief.out")"
fi
BRIEF5="$P5/.momentum/tasting/brief-$TODAY.md"
[ -f "$BRIEF5" ] || fail "brief was not written for the degraded-shape registry"
grep -Eqi '14[- ]day' "$BRIEF5" \
  || fail "brief does not state the degraded window in plain language (no usable verdict date anywhere => the bounded 14-day default window applies and must be stated)"
grep -qF "Owner logs a mooring fee and sees the season total update" "$BRIEF5" \
  || fail "brief dropped the well-formed passing claim because a sibling entry was degraded — degradation must be per-entry, not registry-wide"
AFTER5="$(cksum "$REG5")"
[ "$BEFORE5" = "$AFTER5" ] || fail "tasting brief modified the degraded registry — read-only holds on every code path, including degradation"

if ! CLAUDE_PROJECT_DIR="$P5" "$MT" tasting status --json > "$WORK/s5-status.out" 2>&1; then
  fail "tasting status --json exited non-zero on the degraded-shape registry — the tasting-due signal never errors under any input"
fi
json_ok < "$WORK/s5-status.out" || fail "tasting status --json output is not valid JSON on the degraded-shape registry"

# ---------------------------------------------------------------------------
# Scenario 6 — absent registry: honest degradation, zero probes, exit 0.
# ---------------------------------------------------------------------------
echo "--- Scenario 6: absent registry"
P6="$WORK/absent"; mkdir -p "$P6/.momentum"
if ! CLAUDE_PROJECT_DIR="$P6" "$MT" tasting brief > "$WORK/s6-brief.out" 2>&1; then
  fail "tasting brief exited non-zero when .momentum/features.json is absent — required behavior is a brief that states there are no recorded claims, exit 0"
fi
BRIEF6="$P6/.momentum/tasting/brief-$TODAY.md"
[ -f "$BRIEF6" ] || fail "brief was not written for the absent-registry case"
grep -qi 'no recorded claims' "$BRIEF6" \
  || fail "absent-registry brief does not state plainly that there are no recorded claims to test"
[ ! -f "$P6/.momentum/features.json" ] \
  || fail "tasting brief created .momentum/features.json — this consumer must never create the registry"

if ! CLAUDE_PROJECT_DIR="$P6" "$MT" tasting status --json > "$WORK/s6-status.out" 2>&1; then
  fail "tasting status --json exited non-zero when the registry is absent — the tasting-due signal never fails a session"
fi
json_ok < "$WORK/s6-status.out" || fail "tasting status --json output is not valid JSON when the registry is absent"
grep -qi 'due' "$WORK/s6-status.out" \
  || fail "status does not report due-ness when the registry holds no verdict at all — a session is always due in that state"

# ---------------------------------------------------------------------------
# Scenario 7 — malformed and empty registry: degrade, never repair, exit 0.
# ---------------------------------------------------------------------------
echo "--- Scenario 7: malformed and empty registry"
P7="$WORK/malformed"; mkdir -p "$P7/.momentum"
printf '{ this is not json' > "$P7/.momentum/features.json"
REG7="$P7/.momentum/features.json"
BEFORE7="$(cksum "$REG7")"
if ! CLAUDE_PROJECT_DIR="$P7" "$MT" tasting brief > "$WORK/s7-brief.out" 2>&1; then
  fail "tasting brief exited non-zero on an unparseable registry — required behavior is honest degradation with exit 0"
fi
grep -qi 'no recorded claims' "$P7/.momentum/tasting/brief-$TODAY.md" \
  || fail "malformed-registry brief does not state plainly that there are no recorded claims to test"
AFTER7="$(cksum "$REG7")"
[ "$BEFORE7" = "$AFTER7" ] || fail "the command rewrote or repaired the malformed registry — read-only means never a byte written back, even to fix it"
if ! CLAUDE_PROJECT_DIR="$P7" "$MT" tasting status --json > "$WORK/s7-status.out" 2>&1; then
  fail "tasting status --json exited non-zero on an unparseable registry"
fi
json_ok < "$WORK/s7-status.out" || fail "tasting status --json output is not valid JSON on an unparseable registry"

P7E="$WORK/empty"; mkdir -p "$P7E/.momentum"
: > "$P7E/.momentum/features.json"
if ! CLAUDE_PROJECT_DIR="$P7E" "$MT" tasting brief > "$WORK/s7e-brief.out" 2>&1; then
  fail "tasting brief exited non-zero on an empty registry file"
fi
grep -qi 'no recorded claims' "$P7E/.momentum/tasting/brief-$TODAY.md" \
  || fail "empty-registry brief does not state plainly that there are no recorded claims to test"
[ ! -s "$P7E/.momentum/features.json" ] \
  || fail "the command wrote content into the empty registry file — the registry is read-only"

# ---------------------------------------------------------------------------
# Scenario 8 — the tier vocabulary is closed: across the three fixtures already
# exercised in Scenario 3, each status output names exactly its own tier and
# never any other tier token. (The session-start nudge that renders these tiers
# is rule-hook behavior — verified functionally at QA per the story's ACs, not
# by this black-box script.)
# ---------------------------------------------------------------------------
echo "--- Scenario 8: closed tier vocabulary in status output"
check_only_tier() { # file expected-tier
  local f="$1" expected="$2" t
  for t in quiet insistent leading; do
    if [ "$t" = "$expected" ]; then
      grep -q "$t" "$f" || fail "status output $f does not name its expected tier '$t'"
    else
      grep -q "$t" "$f" && fail "status output $f names tier '$t' alongside '$expected' — the tier vocabulary must be exactly one of quiet/insistent/leading per response"
    fi
  done
  return 0
}
check_only_tier "$WORK/s3-leading.out" leading
check_only_tier "$WORK/s3-quiet.out" quiet
check_only_tier "$WORK/s3-insistent.out" insistent

echo "PASS"
