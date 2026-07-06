#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: live-e2e-compose-register-resolve-gen-2-agent
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-06-28/specs/live-e2e-compose-register-resolve-gen-2-agent.smoke.sh
# how_dev_self_checks: First run the real composition pipeline against the nornspun fixture (a real
#   manifest with a populated File Ownership field + the real KB) so the composed agent file and the
#   fixture's agents.json project entry exist. Then run the committed assertion driver against that
#   composed fixture state and observe exit 0 with a PASS for each assertion: resolution on a path
#   matching a declared ownership glob returns the composed {role}-{domain} slug (not dev); the
#   fixture agents.json has a project entry whose patterns equal the manifest ownership field
#   verbatim; the composed agent file contains both a base-body marker and the diagnostic-table
#   heading; and resolution on a NON-matching path returns the generic dev fallback. A committed
#   evidence artifact under docs/research/ captures the resolve output and per-assertion pass/fail.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/live-e2e-compose-register-resolve-gen-2-agent.md#acceptance-criteria
# platforms: [host]
#
# Harness profile: bash
#
# PRECONDITION (composition phase — AC1): the agent-composition pipeline has been run against the
#   real nornspun fixture, producing the composed .claude/guidelines/agents/{ROLE}-{DOMAIN}.md and a
#   momentum/agents.json project entry in that fixture. This composition beat is an LLM skill
#   invocation (no headless CLI); it is performed as an agent/developer step before this driver runs.
#   This script is the deterministic assertion phase (AC2-AC5) plus the evidence check (AC6).
#
# Invocation:
#   FIXTURE_DIR=/abs/path/to/nornspun \
#   COMPOSED_SLUG=dev-kotlin-compose \
#   MATCH_PATH="composeApp/src/commonMain/kotlin/Foo.kt" \
#   NONMATCH_PATH="README.md" \
#   OWNERSHIP_GLOBS='["composeApp/**/*.kt"]' \
#   EVIDENCE_GLOB='docs/research/live-e2e-compose-*.md' \
#   bash live-e2e-compose-register-resolve-gen-2-agent.smoke.sh
#
# Expected: exit 0 and "PASS" once composition has been performed against the fixture.

set -euo pipefail

: "${FIXTURE_DIR:?set FIXTURE_DIR to the nornspun fixture root}"
: "${COMPOSED_SLUG:?set COMPOSED_SLUG to the expected composed {role}-{domain} slug}"
: "${MATCH_PATH:?set MATCH_PATH to a file path matching a declared ownership glob}"
: "${NONMATCH_PATH:?set NONMATCH_PATH to a file path matching NO declared ownership glob}"
: "${OWNERSHIP_GLOBS:?set OWNERSHIP_GLOBS to the manifest File Ownership field (JSON list), verbatim}"
: "${EVIDENCE_GLOB:=docs/research/live-e2e-compose-*.md}"

AGENTS_JSON="$FIXTURE_DIR/momentum/agents.json"
COMPOSED_FILE="$FIXTURE_DIR/.claude/guidelines/agents/${COMPOSED_SLUG}.md"

fail() { echo "FAIL: $1"; exit 1; }

# --- AC5 (guard): the composed project entry actually exists in the fixture agents.json ---
[ -f "$AGENTS_JSON" ] || fail "fixture agents.json not found at $AGENTS_JSON (was composition run against FIXTURE_DIR?)"
python3 - "$AGENTS_JSON" "$COMPOSED_SLUG" "$OWNERSHIP_GLOBS" <<'PY' || fail "composed project entry missing or patterns != ownership field verbatim (AC3/AC5)"
import json,sys
agents=json.load(open(sys.argv[1])); slug=sys.argv[2]; want=json.loads(sys.argv[3])
proj=agents.get("project",[])
entry=next((e for e in proj if e.get("slug")==slug), None)
assert entry is not None, "no project entry for %s" % slug
pats=entry.get("patterns",[])
assert pats, "patterns is empty"
assert pats==want, "patterns %r != ownership field %r (verbatim)" % (pats, want)
PY
echo "  ok: fixture agents.json has project entry '$COMPOSED_SLUG' with patterns == ownership field verbatim (AC3/AC5-guard)"

# --- AC2 (headline): resolution on a MATCHING path returns the composed slug, not dev ---
GOT_MATCH=$(CLAUDE_PROJECT_DIR="$FIXTURE_DIR" momentum-tools agent resolve --touches "$MATCH_PATH" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); r=d.get('results') or d.get('resolved') or []; print((r[0].get('slug') if r else d.get('slug','')) or '')")
[ "$GOT_MATCH" = "$COMPOSED_SLUG" ] || fail "resolve on matching path returned '$GOT_MATCH', expected composed slug '$COMPOSED_SLUG' (AC2)"
[ "$GOT_MATCH" != "dev" ] || fail "resolve on matching path fell back to generic 'dev' (AC2)"
echo "  ok: resolve --touches '$MATCH_PATH' -> '$GOT_MATCH' (composed slug, not dev) (AC2)"

# --- AC4: composed agent file exists and contains base body + diagnostic table ---
[ -f "$COMPOSED_FILE" ] || fail "composed agent file not found at $COMPOSED_FILE (AC4)"
grep -qi "Diagnostic Table" "$COMPOSED_FILE" || fail "composed file missing '## Diagnostic Table' section (AC4)"
grep -qiE "base body|## (Permissions|Standing Rules|Quick Routing)|You are" "$COMPOSED_FILE" || fail "composed file missing a base-body marker (AC4)"
echo "  ok: composed file has base body + diagnostic table (AC4)"

# --- AC5 (negative control): resolution on a NON-matching path returns the dev fallback ---
GOT_NEG=$(CLAUDE_PROJECT_DIR="$FIXTURE_DIR" momentum-tools agent resolve --touches "$NONMATCH_PATH" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); r=d.get('results') or d.get('resolved') or []; print((r[0].get('slug') if r else d.get('slug','')) or '')")
[ "$GOT_NEG" = "dev" ] || fail "negative control: resolve on non-matching path returned '$GOT_NEG', expected generic 'dev' (AC5)"
echo "  ok: resolve --touches '$NONMATCH_PATH' -> 'dev' (genuine pattern match, not vacuous) (AC5)"

# --- AC6: committed running-app evidence artifact exists under docs/research/ ---
ls $EVIDENCE_GLOB >/dev/null 2>&1 || fail "no committed evidence artifact matching '$EVIDENCE_GLOB' (AC6)"
echo "  ok: committed evidence artifact present under docs/research/ (AC6)"

echo "PASS"
