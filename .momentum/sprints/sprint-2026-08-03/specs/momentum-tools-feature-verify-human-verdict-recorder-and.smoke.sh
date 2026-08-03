#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: momentum-tools-feature-verify-human-verdict-recorder-and
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-08-03/specs/momentum-tools-feature-verify-human-verdict-recorder-and.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/momentum-tools-feature-verify-human-verdict-recorder-and.md#acceptance-criteria
# platforms: [host]

# momentum-tools-feature-verify-human-verdict-recorder-and smoke contract
# Harness profile: bash
#
# Invocation:
#   Run this script from anywhere inside the repository. It builds throwaway
#   fixture projects in temp directories and drives the public CLI:
#     momentum-tools feature verify <feature-slug> --verdict pass|fail \
#       --evidence <text> --build <backendSha>:<clientSha>
#
# Expected: the command records a human PASS/FAIL verdict against an existing
# feature entry in the fixture project's .momentum/features.json, stamping a
# complete last_verified (verdict, ISO date, both build SHAs, evidence text);
# every rejection path (malformed build pair, empty evidence, unknown slug,
# missing registry) exits non-zero and leaves the registry byte-identical.
#
# ── Producer / Consumer scope (seam declaration) ────────────────────────────
# This contract verifies the PRODUCER side of the .momentum/features.json seam.
# Producer: the `momentum-tools feature verify` command — the sole write path
# for feature status and last_verified in .momentum/features.json.
# Consumers (verified by their own contracts elsewhere in this sprint):
#   1. Sprint closure refusal — refuses to close without recorded verdicts.
#   2. The daily tasting brief — reads verdicts and evidence.
#   3. The Impetus session greeting — reports N-of-M features passing.
# Scenario 7 below is the shared shape gate: it asserts the written registry
# entry carries exactly the shape the story ACs pin (status enum value,
# last_verified with verdict + ISO date + both build SHAs distinguishable +
# evidence text). Consumer-side contracts key against this same shape; any
# pinned field absent from the written entry is reported as a cross-side
# field-shape incompatibility.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

fail() {
  echo "FAIL: $1"
  exit 1
}

# ── Locate the CLI (public PATH shim) ────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
if command -v momentum-tools >/dev/null 2>&1; then
  MT="momentum-tools"
elif [ -x "$REPO_ROOT/skills/momentum/bin/momentum-tools" ]; then
  MT="$REPO_ROOT/skills/momentum/bin/momentum-tools"
else
  fail "momentum-tools CLI not found on PATH"
fi

# ── Fixture data ─────────────────────────────────────────────────────────────
BACKEND_SHA="0a1b2c3d4e5f60718293a4b5c6d7e8f901234567"
CLIENT_SHA="fedcba9876543210fedcba9876543210fedcba98"
BUILD_PAIR="${BACKEND_SHA}:${CLIENT_SHA}"
EVIDENCE_OK="Wove and exported a tapestry; the export opened cleanly on a second machine."
EVIDENCE_BAD="Export produced an empty file on the demo build."
TARGET_SLUG="loom-export"
OTHER_SLUG="gate-crossing"

P1="$(mktemp -d)"
P2="$(mktemp -d)"
trap 'rm -rf "$P1" "$P2"' EXIT

mkdir -p "$P1/.momentum"
git init -q "$P1" 2>/dev/null || true
REG="$P1/.momentum/features.json"

# Fixture registry: two entries, target carries the optional informational
# links (epic_slugs names an epic that does not exist in this fixture — the
# story pins that this is never validated and never blocking).
cat > "$REG" <<'JSON'
{
  "gate-crossing": {
    "slug": "gate-crossing",
    "name": "Gate Crossing",
    "acceptance_condition": "A user crosses the gate end to end without manual intervention.",
    "status": "absent"
  },
  "loom-export": {
    "slug": "loom-export",
    "name": "Loom Export",
    "acceptance_condition": "A woven piece exports to a shareable file that opens elsewhere.",
    "status": "failing",
    "epic_slugs": ["weaving-epic-that-does-not-exist"],
    "design_ref": "docs/design/loom-export.md"
  }
}
JSON

export CLAUDE_PROJECT_DIR="$P1"

# Second fixture project: .momentum exists, features.json deliberately absent.
mkdir -p "$P2/.momentum"
git init -q "$P2" 2>/dev/null || true

# ── JSON helpers (read-back of the observable registry file only) ───────────
entry_json() { # $1 = registry path, $2 = feature slug → compact JSON or MISSING
  REG_PATH="$1" FEATURE_SLUG="$2" python3 <<'PY'
import json, os
doc = json.load(open(os.environ["REG_PATH"]))
slug = os.environ["FEATURE_SLUG"]
entry = None
if isinstance(doc, dict):
    if isinstance(doc.get(slug), dict):
        entry = doc[slug]
    elif isinstance(doc.get("features"), dict) and isinstance(doc["features"].get(slug), dict):
        entry = doc["features"][slug]
    elif isinstance(doc.get("features"), list):
        entry = next((e for e in doc["features"] if isinstance(e, dict) and e.get("slug") == slug), None)
elif isinstance(doc, list):
    entry = next((e for e in doc if isinstance(e, dict) and e.get("slug") == slug), None)
print(json.dumps(entry, sort_keys=True) if entry is not None else "MISSING")
PY
}

status_of() { # $1 = entry JSON → status value
  ENTRY="$1" python3 -c 'import json, os; print(json.loads(os.environ["ENTRY"]).get("status"))'
}

expect_reject() { # $1 = description; rest = command. Asserts non-zero exit + byte-identical registry.
  local desc="$1"
  shift
  local rc=0
  set +e
  REJECT_OUT="$("$@" 2>&1)"
  rc=$?
  set -e
  [ "$rc" -ne 0 ] || fail "$desc: expected a non-zero exit, got 0 (output: $REJECT_OUT)"
  cmp -s "$REG" "$SNAP" || fail "$desc: registry changed after a rejected run — rejection must leave .momentum/features.json byte-identical"
}

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 1 — The subcommand exists and documents its flags (AC1)
# ═════════════════════════════════════════════════════════════════════════════
set +e
HELP_OUT="$("$MT" feature verify --help 2>&1)"
help_rc=$?
set -e
[ "$help_rc" -eq 0 ] || fail "『feature verify --help』 exited $help_rc — the subcommand is not registered (output: $HELP_OUT)"
for flag in --verdict --evidence --build; do
  echo "$HELP_OUT" | grep -q -- "$flag" || fail "『feature verify --help』 does not document the $flag option"
done
echo "ok: scenario 1 — subcommand registered and help documents --verdict/--evidence/--build"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 2 — Malformed build pairs are rejected before anything is written (AC4)
# ═════════════════════════════════════════════════════════════════════════════
SNAP="$P1/registry.snapshot"
cp "$REG" "$SNAP"

set +e
BAD_OUT="$("$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "$BACKEND_SHA" 2>&1)"
bad_rc=$?
set -e
[ "$bad_rc" -ne 0 ] || fail "single-SHA build value accepted — expected rejection with non-zero exit"
echo "$BAD_OUT" | grep -qi "build" || fail "malformed-build rejection message does not name the problem (no mention of the build pair): $BAD_OUT"
cmp -s "$REG" "$SNAP" || fail "registry changed after malformed-build rejection"

expect_reject "empty client side of build pair"  "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "${BACKEND_SHA}:"
expect_reject "empty backend side of build pair" "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build ":${CLIENT_SHA}"
expect_reject "extra colon in build pair"        "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "${BACKEND_SHA}:${CLIENT_SHA}:deadbeef"
expect_reject "non-hex build value"              "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "zz99zz:${CLIENT_SHA}"
echo "ok: scenario 2 — every malformed build pair rejected, registry byte-identical"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 3 — Empty or missing evidence is rejected before anything is written (AC5)
# ═════════════════════════════════════════════════════════════════════════════
expect_reject "empty evidence"           "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "" --build "$BUILD_PAIR"
expect_reject "whitespace-only evidence" "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "   " --build "$BUILD_PAIR"
expect_reject "missing evidence flag"    "$MT" feature verify "$TARGET_SLUG" --verdict pass --build "$BUILD_PAIR"
echo "ok: scenario 3 — verdicts without an observation behind them are not recordable"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 4 — Unknown slug rejected, never invented; failure emits the JSON
#              result envelope with exit 1 (AC6, AC10)
# ═════════════════════════════════════════════════════════════════════════════
set +e
UNK_OUT="$("$MT" feature verify no-such-feature --verdict pass --evidence "$EVIDENCE_OK" --build "$BUILD_PAIR" 2>&1)"
unk_rc=$?
set -e
[ "$unk_rc" -eq 1 ] || fail "unknown slug: expected exit 1, got $unk_rc (output: $UNK_OUT)"
echo "$UNK_OUT" | grep -q "no-such-feature" || fail "unknown-slug error does not name the slug: $UNK_OUT"
echo "$UNK_OUT" | grep -q "features.json"   || fail "unknown-slug error does not name the registry path: $UNK_OUT"
echo "$UNK_OUT" | grep -q '"success"' || fail "failure output is missing the standard JSON result envelope (no \"success\" field): $UNK_OUT"
echo "$UNK_OUT" | grep -q '"action"'  || fail "failure output is missing the standard JSON result envelope (no \"action\" field): $UNK_OUT"
cmp -s "$REG" "$SNAP" || fail "registry changed after unknown-slug rejection"
[ "$(entry_json "$REG" no-such-feature)" = "MISSING" ] || fail "unknown slug was invented as a new registry entry"
echo "ok: scenario 4 — unknown slug rejected by name with envelope, no entry created"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 5 — Missing registry is a clear error, not a silent bootstrap (AC7)
# ═════════════════════════════════════════════════════════════════════════════
set +e
MISS_OUT="$(CLAUDE_PROJECT_DIR="$P2" "$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "$BUILD_PAIR" 2>&1)"
miss_rc=$?
set -e
[ "$miss_rc" -ne 0 ] || fail "missing registry: expected non-zero exit, got 0 (output: $MISS_OUT)"
echo "$MISS_OUT" | grep -q "features.json" || fail "missing-registry error does not name the expected path: $MISS_OUT"
[ ! -e "$P2/.momentum/features.json" ] || fail "missing registry was silently bootstrapped — .momentum/features.json was created"
echo "ok: scenario 5 — missing registry errors by path and is never created"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 6 — Happy path: a pass verdict sets passing, exit 0, JSON envelope (AC2, AC10)
# ═════════════════════════════════════════════════════════════════════════════
PRE_TARGET="$(entry_json "$REG" "$TARGET_SLUG")"
PRE_OTHER="$(entry_json "$REG" "$OTHER_SLUG")"

set +e
PASS_OUT="$("$MT" feature verify "$TARGET_SLUG" --verdict pass --evidence "$EVIDENCE_OK" --build "$BUILD_PAIR")"
pass_rc=$?
set -e
[ "$pass_rc" -eq 0 ] || fail "pass-verdict run exited $pass_rc, expected 0 (output: $PASS_OUT)"
echo "$PASS_OUT" | python3 -c '
import json, sys
d = json.load(sys.stdin)
sys.exit(0 if (d.get("success") is True and "action" in d) else 1)
' || fail "success output is not the standard JSON result envelope (action + success:true): $PASS_OUT"

POST_TARGET="$(entry_json "$REG" "$TARGET_SLUG")"
[ "$POST_TARGET" != "MISSING" ] || fail "target entry vanished from the registry after a successful run"
[ "$(status_of "$POST_TARGET")" = "passing" ] || fail "pass verdict did not set status to the enum value 『passing』 (got: $(status_of "$POST_TARGET"))"
echo "ok: scenario 6 — pass verdict recorded with exit 0 and the standard envelope"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 7 — Seam shape gate: the written entry carries exactly the pinned
#              shape consumers key against (AC3, AC8)
# ═════════════════════════════════════════════════════════════════════════════
MISSING_FIELDS="$(ENTRY="$POST_TARGET" BSHA="$BACKEND_SHA" CSHA="$CLIENT_SHA" EVIDENCE="$EVIDENCE_OK" python3 <<'PY'
import json, os, re
entry = json.loads(os.environ["ENTRY"])
problems = []
if entry.get("status") != "passing":
    problems.append("status enum value 'passing'")
lv = entry.get("last_verified")
if not isinstance(lv, dict) or not lv:
    problems.append("last_verified object")
else:
    blob = json.dumps(lv)
    if '"pass"' not in blob:
        problems.append("verdict 'pass' inside last_verified")
    if not re.search(r"\d{4}-\d{2}-\d{2}", blob):
        problems.append("ISO date inside last_verified")
    if os.environ["BSHA"] not in blob:
        problems.append("backend build SHA inside last_verified")
    if os.environ["CSHA"] not in blob:
        problems.append("client build SHA inside last_verified")
    if os.environ["EVIDENCE"] not in blob:
        problems.append("evidence text inside last_verified")
print("NONE" if not problems else "; ".join(problems))
PY
)"
[ "$MISSING_FIELDS" = "NONE" ] || fail "cross-side field-shape incompatibility: the written registry entry is missing pinned field(s): $MISSING_FIELDS — the consumer contracts (sprint closure refusal, daily tasting brief, Impetus session greeting) key against this exact shape"
echo "ok: scenario 7 — written entry matches the pinned producer shape consumers read"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 8 — The write is surgical and touches no fourth seam (AC9, AC11)
# ═════════════════════════════════════════════════════════════════════════════
POST_OTHER="$(entry_json "$REG" "$OTHER_SLUG")"
[ "$POST_OTHER" = "$PRE_OTHER" ] || fail "the untouched neighbor entry 『$OTHER_SLUG』 changed during a run against 『$TARGET_SLUG』"

FIELD_DRIFT="$(PRE="$PRE_TARGET" POST="$POST_TARGET" python3 <<'PY'
import json, os
pre = json.loads(os.environ["PRE"])
post = json.loads(os.environ["POST"])
for k in ("status", "last_verified"):
    pre.pop(k, None)
    post.pop(k, None)
changed = sorted(set(k for k in set(pre) | set(post) if pre.get(k) != post.get(k)))
print("NONE" if not changed else ", ".join(changed))
PY
)"
[ "$FIELD_DRIFT" = "NONE" ] || fail "a successful run changed fields beyond status and last_verified on the target entry: $FIELD_DRIFT (slug, name, acceptance_condition, epic_slugs, design_ref must survive unchanged)"

MOMENTUM_FILES="$(cd "$P1/.momentum" && find . -type f | sort | tr '\n' ' ')"
[ "$MOMENTUM_FILES" = "./features.json " ] || fail "fourth-seam violation: a run touched or created state beyond .momentum/features.json — found: $MOMENTUM_FILES"
echo "ok: scenario 8 — exactly two fields on exactly one entry changed; no other state file exists"

# ═════════════════════════════════════════════════════════════════════════════
# Scenario 9 — A fail verdict moves the feature back to failing; the
#              never-verified neighbor is never passing (AC2, AC8)
# ═════════════════════════════════════════════════════════════════════════════
set +e
FAIL_OUT="$("$MT" feature verify "$TARGET_SLUG" --verdict fail --evidence "$EVIDENCE_BAD" --build "$BUILD_PAIR")"
fail_rc=$?
set -e
[ "$fail_rc" -eq 0 ] || fail "fail-verdict run exited $fail_rc, expected 0 (output: $FAIL_OUT)"

FLIPPED="$(entry_json "$REG" "$TARGET_SLUG")"
[ "$(status_of "$FLIPPED")" = "failing" ] || fail "fail verdict did not move status back to the enum value 『failing』 (got: $(status_of "$FLIPPED"))"
FLIP_BLOB="$(ENTRY="$FLIPPED" python3 -c 'import json, os; print(json.dumps(json.loads(os.environ["ENTRY"]).get("last_verified")))')"
echo "$FLIP_BLOB" | grep -q '"fail"' || fail "last_verified does not carry the fail verdict after the flip: $FLIP_BLOB"
echo "$FLIP_BLOB" | grep -qF "$EVIDENCE_BAD" || fail "last_verified does not carry the new evidence text after the flip: $FLIP_BLOB"

NEIGHBOR="$(entry_json "$REG" "$OTHER_SLUG")"
[ "$(status_of "$NEIGHBOR")" != "passing" ] || fail "failing-by-default broken: 『$OTHER_SLUG』 reports passing with no recorded human pass verdict"
echo "ok: scenario 9 — fail verdict flips to failing; never-verified feature is never passing"

echo "PASS"
