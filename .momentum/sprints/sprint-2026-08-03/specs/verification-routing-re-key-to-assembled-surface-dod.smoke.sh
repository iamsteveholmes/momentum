#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: verification-routing-re-key-to-assembled-surface-dod
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-08-03/specs/verification-routing-re-key-to-assembled-surface-dod.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/verification-routing-re-key-to-assembled-surface-dod.md#acceptance-criteria
# platforms: [host]

# verification-routing-re-key-to-assembled-surface-dod smoke contract
# Harness profile: bash
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-08-03/specs/verification-routing-re-key-to-assembled-surface-dod.smoke.sh
#
# Expected: after the re-key, the public `momentum-tools` CLI routes verification
# by declared assembled surface first and falls back to change_type inference
# only when no surface is declared. A story that declares `surface: chat-ui`
# resolves to `smoke` even when its change_type is backend — the backend->curl
# misroute is gone as an observable routing outcome. Stories with no declared
# surface keep resolving to a valid method token (no in-flight sprint breaks),
# including multi-value, empty, and unknown change_type inputs. The method enum
# stays closed at the six existing tokens, and the harness config's driver
# bindings remain keyed on exactly those six.
#
# Scope note (routing per verification-standard.md §1): the story's
# document-side claims — the standard's routing table keyed on surface with its
# prose definition and chat-UI example, the single reconciled override path, the
# universal reachability Definition-of-Done item in the standard and in the
# generated-story templates, and word-for-word agreement across every published
# copy of the table — are document/config artifacts. They are verified at QA by
# document review of the story's touched artifacts against its Acceptance
# Criteria. This black-box contract asserts the runtime routing behavior only:
# what an outsider observes by invoking the CLI.

set -euo pipefail

fail() { echo "FAIL: $1"; exit 1; }

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

WORK="$(mktemp -d "${TMPDIR:-/tmp}/routing-smoke.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

FIXTURE="$WORK/project"
mkdir -p "$FIXTURE/.momentum/stories"

# Fixture stories: one per assertion. Surface and change_type live on the story
# index entry, the same observable state file every sprint tool reads.
python3 - "$FIXTURE/.momentum/stories/index.json" <<'PY'
import json, sys
stories = {
    # Declared surface must win over change_type inference.
    "fx-chat-surface-backend-diff": {
        "status": "backlog", "epic_slug": "fx", "story_type": "practice",
        "priority": "medium", "depends_on": [], "touches": [],
        "change_type": "backend", "surface": "chat-ui",
    },
    # Inference fallback: multi-value change_type, no declared surface.
    "fx-inference-multi": {
        "status": "backlog", "epic_slug": "fx", "story_type": "practice",
        "priority": "medium", "depends_on": [], "touches": [],
        "change_type": "script-code + skill-instruction",
    },
    # Degradation: empty change_type, no declared surface.
    "fx-inference-empty": {
        "status": "backlog", "epic_slug": "fx", "story_type": "practice",
        "priority": "medium", "depends_on": [], "touches": [],
        "change_type": "",
    },
    # Degradation: unknown change_type token, no declared surface.
    "fx-inference-unknown": {
        "status": "backlog", "epic_slug": "fx", "story_type": "practice",
        "priority": "medium", "depends_on": [], "touches": [],
        "change_type": "not-a-real-type",
    },
}
# Enum closure: one surface-less fixture per known change_type.
for ct in ["skill-instruction", "agent-definition", "rule-hook", "script-code",
           "script-cli", "backend", "app-ui", "research-spike", "specification",
           "config-structure"]:
    stories[f"fx-ct-{ct}"] = {
        "status": "backlog", "epic_slug": "fx", "story_type": "practice",
        "priority": "medium", "depends_on": [], "touches": [],
        "change_type": ct,
    }
json.dump(stories, open(sys.argv[1], "w"), indent=2)
PY

resolve() {
  CLAUDE_PROJECT_DIR="$FIXTURE" "$MT" sprint compute-verification-method --story "$1" 2>&1
}
token_of() {
  echo "$1" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("verification_method",""))' 2>/dev/null || true
}

ENUM="skill-invoke behavioral-trigger bash smoke curl document-review"
in_enum() { case " $ENUM " in *" $1 "*) return 0;; *) return 1;; esac; }

# ---------------------------------------------------------------------------
# Assert 1 — Declared surface wins: a backend-only diff with surface chat-ui
# resolves to smoke, never curl. This is the observable end of the re-key.
# ---------------------------------------------------------------------------
OUT1="$(resolve fx-chat-surface-backend-diff)" \
  || fail "resolver errored on a story with a declared surface: $OUT1"
TOK1="$(token_of "$OUT1")"
[ "$TOK1" != "curl" ] \
  || fail "a backend-diff story with declared surface chat-ui routed to curl — the declared surface did not override change_type inference"
[ "$TOK1" = "smoke" ] \
  || fail "a story with declared surface chat-ui resolved to '$TOK1' — expected smoke (chat-ui and application-ui route to smoke)"

# ---------------------------------------------------------------------------
# Assert 2 — Inference fallback holds: surface-less stories still resolve to a
# valid token, including multi-value, empty, and unknown change_type inputs.
# ---------------------------------------------------------------------------
for s in fx-inference-multi fx-inference-empty fx-inference-unknown; do
  OUT="$(resolve "$s")" || fail "resolver errored on surface-less story $s: $OUT"
  TOK="$(token_of "$OUT")"
  [ -n "$TOK" ] || fail "resolver returned an empty method for surface-less story $s: $OUT"
  in_enum "$TOK" || fail "resolver returned '$TOK' for $s — not one of the six method tokens"
done

# ---------------------------------------------------------------------------
# Assert 3 — Enum closure: across every known change_type with no declared
# surface, the resolver's answer is always one of the six existing tokens —
# no token added, removed, or renamed by the re-key.
# ---------------------------------------------------------------------------
for ct in skill-instruction agent-definition rule-hook script-code script-cli \
          backend app-ui research-spike specification config-structure; do
  OUT="$(resolve "fx-ct-$ct")" || fail "resolver errored on change_type $ct: $OUT"
  TOK="$(token_of "$OUT")"
  in_enum "$TOK" || fail "change_type $ct resolved to '$TOK' — outside the closed six-token enum"
done

# ---------------------------------------------------------------------------
# Assert 4 — The harness config still parses and its driver bindings are keyed
# on exactly the six method tokens (the config file is a declared observable
# artifact of the story's Acceptance Criteria).
# ---------------------------------------------------------------------------
HARNESS="$REPO_ROOT/momentum/verification-harness.json"
[ -f "$HARNESS" ] || fail "momentum/verification-harness.json not found"
python3 - "$HARNESS" <<'PY' || fail "driver_bindings keys in momentum/verification-harness.json are not exactly the six existing method tokens"
import json, sys
d = json.load(open(sys.argv[1]))
expected = {"skill-invoke", "behavioral-trigger", "bash", "smoke", "curl", "document-review"}
sys.exit(0 if set(d["driver_bindings"].keys()) == expected else 1)
PY

echo "PASS"
