#!/usr/bin/env bash
# live-compose-resolve.sh — deterministic assertion phase of the build-guidelines live E2E.
#
# PURPOSE
#   Asserts the observable outputs of the build-guidelines + agent-builder composition
#   pipeline against the real nornspun fixture. Covers ACs 2–5 of story
#   live-e2e-compose-register-resolve-gen-2-agent and produces a committed evidence artifact
#   (AC6) under docs/research/.
#
# PRECONDITION (composition phase — AC1)
#   The agent-composition pipeline (momentum:build-guidelines → momentum:agent-builder) has
#   been run against the fixture. See e2e/README.md for the full two-phase E2E procedure.
#   This script is the deterministic assertion phase only.
#
# USAGE (from Momentum repo root)
#   bash skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
#
# ENV VARS (all have defaults for the standard nornspun / dev-kotlin-compose fixture)
#   FIXTURE_DIR       abs path to the composed fixture root
#                     default: ~/projects/nornspun
#   COMPOSED_SLUG     expected {role}-{domain} slug
#                     default: dev-kotlin-compose
#   MATCH_PATH        a file path that matches a declared ownership glob
#                     default: composeApp/src/commonMain/kotlin/App.kt
#   NONMATCH_PATH     a file path that does NOT match any declared ownership glob
#                     default: README.md
#   OWNERSHIP_GLOBS   (optional) override — the manifest File Ownership field as a JSON array
#                     string, e.g. '["composeApp/**","shared/**"]'
#                     If unset, the driver parses the ## File Ownership field directly from
#                     ${FIXTURE_DIR}/.claude/manifests/${COMPOSED_SLUG}.md (the authoritative
#                     source) so the assertion proves "patterns == the manifesto field on disk",
#                     not "patterns == what was typed at the command line" (AC3/AC7).
#   EVIDENCE_OUT_DIR  directory to write the evidence artifact into
#                     default: docs/research   (relative to cwd = Momentum repo root)
#
# EXIT CODES
#   0 — every assertion passed; evidence artifact written
#   1 — a named assertion failed; partial evidence artifact written

set -euo pipefail

FIXTURE_DIR="${FIXTURE_DIR:-$HOME/projects/nornspun}"
COMPOSED_SLUG="${COMPOSED_SLUG:-dev-kotlin-compose}"
MATCH_PATH="${MATCH_PATH:-composeApp/src/commonMain/kotlin/App.kt}"
NONMATCH_PATH="${NONMATCH_PATH:-README.md}"
EVIDENCE_OUT_DIR="${EVIDENCE_OUT_DIR:-docs/research}"

AGENTS_JSON="$FIXTURE_DIR/momentum/agents.json"
COMPOSED_FILE="$FIXTURE_DIR/.claude/guidelines/agents/${COMPOSED_SLUG}.md"
MANIFESTO_FILE="$FIXTURE_DIR/.claude/manifests/${COMPOSED_SLUG}.md"

# Fixed evidence filename — no embedded date; timestamp lives inside the file.
# This ensures exactly one regenerable artifact exists under EVIDENCE_OUT_DIR:
# the driver always overwrites it on each run. A pre-composition partial artifact
# is replaced automatically the next time the driver succeeds.
EVIDENCE_FILE="${EVIDENCE_OUT_DIR}/live-e2e-compose-resolve-evidence.md"

# --- helpers ---

mkdir -p "$EVIDENCE_OUT_DIR"

_log() { echo "$1" | tee -a "$EVIDENCE_FILE"; }
pass()  { _log "  PASS: $1"; }
# fail() emits ALL arguments so multi-arg diagnostic messages reach output + evidence.
fail()  {
  _log "  FAIL: $*"
  _log ""
  _log "Driver exited non-zero. Evidence (partial): $EVIDENCE_FILE"
  exit 1
}

# --- resolve OWNERSHIP_GLOBS from manifesto if not supplied as env override ---
#
# Manifesto path: ${FIXTURE_DIR}/.claude/manifests/${COMPOSED_SLUG}.md
# Expected section format:
#   ## File Ownership
#   file_ownership:
#     - "composeApp/**"
#     - "shared/**"
#
# The parsed list is used verbatim for the AC3/AC7 equality assertion against agents.json,
# so the assertion proves "agents.json patterns == the ## File Ownership field on disk"
# (deterministic-path proof) rather than "patterns == what the operator typed at the prompt".

if [ -z "${OWNERSHIP_GLOBS:-}" ]; then
  [ -f "$MANIFESTO_FILE" ] || \
    fail "AC3/AC7: manifesto not found at $MANIFESTO_FILE — cannot parse ## File Ownership. " \
         "Set OWNERSHIP_GLOBS to override, or stage the manifesto per e2e/README.md."

  OWNERSHIP_GLOBS=$(python3 - "$MANIFESTO_FILE" <<'PY'
import re, json, sys

text = open(sys.argv[1]).read()
m = re.search(
    r'## File Ownership\s+file_ownership:\s+((?:\s*-\s+"[^"]+"\s*)+)',
    text
)
if not m:
    raise SystemExit(
        "## File Ownership section not found or malformed in %s" % sys.argv[1]
    )
entries = re.findall(r'-\s+"([^"]+)"', m.group(1))
if not entries:
    raise SystemExit(
        "No file_ownership entries parsed from ## File Ownership in %s" % sys.argv[1]
    )
print(json.dumps(entries))
PY
  )
fi

# --- initialize evidence artifact ---

cat > "$EVIDENCE_FILE" <<HEADER
# Live E2E Evidence — build-guidelines compose + register + resolve

Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Driver:    skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
Fixture:   $FIXTURE_DIR
Slug:      $COMPOSED_SLUG
Ownership: $OWNERSHIP_GLOBS

Supersedes: sprint-2026-06-18 integration-TRACE (a hand-walked instruction trace, not live
execution). This artifact is generated by running the assertion driver against the real
composed fixture state, per story live-e2e-compose-register-resolve-gen-2-agent AC6.

HEADER

echo ""
echo "--- build-guidelines E2E: asserting composed fixture state ---"
echo "  fixture : $FIXTURE_DIR"
echo "  slug    : $COMPOSED_SLUG"
echo "  match   : $MATCH_PATH"
echo "  nonmatch: $NONMATCH_PATH"
echo ""

# ============================================================
# AC5-guard: the composed project[] entry exists in agents.json
# with patterns equal to the manifest File Ownership field verbatim.
# This must be checked FIRST so a mis-targeted resolver fails loudly
# here rather than silently returning dev in AC2.
# ============================================================

_log "## AC3 / AC5-guard — fixture agents.json project entry + verbatim patterns"
_log ""

[ -f "$AGENTS_JSON" ] || \
  fail "fixture agents.json not found at $AGENTS_JSON — was the composition pipeline run against FIXTURE_DIR?"

python3 - "$AGENTS_JSON" "$COMPOSED_SLUG" "$OWNERSHIP_GLOBS" <<'PY' || \
  fail "composed project entry missing or patterns != manifesto File Ownership field verbatim (AC3 / AC5-guard)"
import json, sys
agents = json.load(open(sys.argv[1]))
slug   = sys.argv[2]
want   = json.loads(sys.argv[3])
proj   = agents.get("project", [])
entry  = next((e for e in proj if e.get("slug") == slug), None)
assert entry is not None, \
  "no project[] entry for slug '%s' in %s" % (slug, sys.argv[1])
pats = entry.get("patterns", [])
assert pats, \
  "patterns[] is empty for project entry '%s'" % slug
assert pats == want, \
  "patterns %r != ownership field %r  (verbatim equality required for deterministic-path assertion AC7)" % (pats, want)
print("  registered patterns:", json.dumps(pats))
PY

pass "agents.json project entry '$COMPOSED_SLUG' exists; patterns == manifesto File Ownership verbatim (AC3 / AC5-guard)"
_log ""

# ============================================================
# AC2: resolve on a MATCHING path returns the composed slug, not dev.
# Deterministic-path proof: the match is driven by the declared
# file_ownership list, not by LLM inference from ## Project Stack.
# ============================================================

_log "## AC2 — resolve --touches on matching path"
_log ""
_log "Path: $MATCH_PATH"
_log ""

# Wrap in set +e so a non-zero exit surfaces as a named AC2 failure
# rather than a cryptic bash abort under set -euo pipefail.
set +e
RESOLVE_JSON=$(CLAUDE_PROJECT_DIR="$FIXTURE_DIR" momentum-tools agent resolve --touches "$MATCH_PATH")
RESOLVE_AC2_EXIT=$?
set -e

if [ "$RESOLVE_AC2_EXIT" -ne 0 ]; then
  fail "AC2: momentum-tools exited $RESOLVE_AC2_EXIT for '$MATCH_PATH' — resolver failed before returning JSON"
fi

_log '```json'
_log "$RESOLVE_JSON"
_log '```'
_log ""

GOT_MATCH=$(echo "$RESOLVE_JSON" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d.get('results') or []
print((r[0].get('slug') if r else '') or '')
")

[ "$GOT_MATCH" = "$COMPOSED_SLUG" ] || \
  fail "AC2: resolve on '$MATCH_PATH' returned slug '$GOT_MATCH', expected '$COMPOSED_SLUG'"
[ "$GOT_MATCH" != "dev" ] || \
  fail "AC2: resolve on '$MATCH_PATH' fell back to generic 'dev' — patterns are not being matched"

pass "AC2: resolve --touches '$MATCH_PATH' → '$GOT_MATCH' (composed slug, not dev)"
_log ""

# ============================================================
# AC4: composed agent file exists and contains:
#   (a) a base-body marker specific to dev.md
#   (b) the ## Diagnostic Table section from the manifesto
# ============================================================

_log "## AC4 — composed agent file: $COMPOSED_FILE"
_log ""

[ -f "$COMPOSED_FILE" ] || \
  fail "AC4: composed agent file not found at $COMPOSED_FILE"

grep -qi "Diagnostic Table" "$COMPOSED_FILE" || \
  fail "AC4: composed file missing '## Diagnostic Table' section"

# Require the dev.md-specific base-body marker "You are a dev agent".
# Generic headings (## Process, ## Critical Constraints) are intentionally
# excluded — they can appear in constitution/manifesto content and would
# give a false-positive if the base body was not actually merged.
grep -qi "You are a dev agent" "$COMPOSED_FILE" || \
  fail "AC4: composed file missing dev.md base-body marker ('You are a dev agent' not found)"

{
  echo "File:                  $COMPOSED_FILE"
  echo "Lines:                 $(wc -l < "$COMPOSED_FILE")"
  echo "Diagnostic Table hits: $(grep -ci 'Diagnostic Table' "$COMPOSED_FILE")"
  echo "Base-body marker:      present (You are a dev agent)"
}  | tee -a "$EVIDENCE_FILE"
_log ""

pass "AC4: composed file has base body + '## Diagnostic Table' section"
_log ""

# ============================================================
# AC5 (negative control): resolve on a NON-matching path returns
# the generic 'dev' fallback, proving the AC2 match is genuine.
# ============================================================

_log "## AC5 — negative control: resolve --touches on non-matching path"
_log ""
_log "Path: $NONMATCH_PATH"
_log ""

# Use set +e so a missing defaults.dev path (common on fresh fixtures)
# surfaces as a named failure rather than a cryptic bash exit.
# Capture stdout only (not 2>&1) so any stderr does not contaminate the
# JSON variable and crash python3 -c json.load with a traceback.
set +e
RESOLVE_NEG_STDERR_TMP=$(mktemp)
RESOLVE_NEG_JSON=$(CLAUDE_PROJECT_DIR="$FIXTURE_DIR" momentum-tools agent resolve \
  --touches "$NONMATCH_PATH" 2>"$RESOLVE_NEG_STDERR_TMP")
RESOLVE_NEG_EXIT=$?
RESOLVE_NEG_STDERR=$(cat "$RESOLVE_NEG_STDERR_TMP"; rm -f "$RESOLVE_NEG_STDERR_TMP")
set -e

_log '```json'
_log "$RESOLVE_NEG_JSON"
_log '```'
_log ""

if [ "$RESOLVE_NEG_EXIT" -ne 0 ]; then
  # momentum-tools exited non-zero — most likely defaults.dev path is missing
  # in the fixture's agents.json. Surface as a named failure.
  fail "AC5 (negative control): momentum-tools exited $RESOLVE_NEG_EXIT for '$NONMATCH_PATH'. " \
       "Likely cause: defaults.dev in $AGENTS_JSON points to a missing file. " \
       "See e2e/README.md § Fixture Setup for how to set defaults.dev." \
       "${RESOLVE_NEG_STDERR:+stderr: $RESOLVE_NEG_STDERR}"
fi

GOT_NEG=$(echo "$RESOLVE_NEG_JSON" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d.get('results') or []
print((r[0].get('slug') if r else '') or '')
")

[ "$GOT_NEG" = "dev" ] || \
  fail "AC5 (negative control): resolve on '$NONMATCH_PATH' returned '$GOT_NEG', expected 'dev'"

pass "AC5: resolve --touches '$NONMATCH_PATH' → 'dev' (genuine pattern match, not vacuous)"
_log ""

# ============================================================
# Finalize evidence artifact
# ============================================================

_log "## Summary"
_log ""
_log "| Assertion | Result |"
_log "|---|---|"
_log "| AC3 / AC5-guard: agents.json project entry + verbatim patterns | PASS |"
_log "| AC2: resolve '$MATCH_PATH' → $COMPOSED_SLUG (not dev) | PASS |"
_log "| AC4: composed file has base body + Diagnostic Table | PASS |"
_log "| AC5 negative: resolve '$NONMATCH_PATH' → dev | PASS |"
_log ""
_log "All assertions passed. Driver exited 0."

echo ""
echo "PASS — all assertions hold."
echo "Evidence artifact: $EVIDENCE_FILE"
