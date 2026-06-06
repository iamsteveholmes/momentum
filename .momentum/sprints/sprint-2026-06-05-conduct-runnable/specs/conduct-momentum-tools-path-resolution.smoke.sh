#!/usr/bin/env bash
# conduct-momentum-tools-path-resolution smoke contract
#
# === VERIFICATION HEADER (Part A) ===
# story_slug: conduct-momentum-tools-path-resolution
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-momentum-tools-path-resolution.smoke.sh
# how_dev_self_checks: |
#   Before you signal done, open a brand-new shell — the kind a launched helper would run in,
#   not your own customized login shell — and type `momentum-tools` with no path in front of it,
#   the same way you would type `git` or `ls`. Confirm the shell finds it: run
#   `command -v momentum-tools` and confirm it prints a real, existing location rather than
#   reporting "not found". Then run the bare command with a couple of harmless read-only
#   subcommands the practice uses during a build (for example, asking it for a sprint's status
#   and asking it to resolve a role) and confirm each prints a sensible result and exits without
#   a "command not found" error. Finally, confirm this works from at least two different working
#   directories (the repo root and a fresh temp directory) so the resolution does not depend on
#   where you happen to be standing. If any of these prints "not found" or fails to launch, the
#   environment precondition is not yet met.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/conduct-momentum-tools-path-resolution.md#acceptance-criteria
# platforms: [host]
#
# === VERIFIER CONTRACT BODY (Part B) ===
# Invocation:
#   bash .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-momentum-tools-path-resolution.smoke.sh
#
# Expected: bare `momentum-tools` resolves and runs from any working directory in a
#           non-interactive shell, with no "command not found".

set -uo pipefail

FAILED=0

note_fail() { echo "FAIL: $1"; FAILED=1; }

# --- Assert 1: bare name resolves to an existing executable location ---
LOCATION="$(command -v momentum-tools 2>/dev/null || true)"
if [ -z "$LOCATION" ]; then
  note_fail "bare 'momentum-tools' did not resolve (command -v returned nothing — equivalent to 'not found')"
else
  echo "resolved: momentum-tools -> $LOCATION"
fi

# --- Assert 2: bare command launches without a 'command not found' error ---
# Use a help/usage probe that does not depend on any sprint state.
HELP_OUT="$(momentum-tools --help 2>&1 || momentum-tools help 2>&1 || true)"
if printf '%s' "$HELP_OUT" | grep -qiE 'command not found|not found'; then
  note_fail "invoking bare 'momentum-tools' reported not found: $HELP_OUT"
else
  echo "bare invocation launched (no not-found error)"
fi

# --- Assert 3: a representative read-only build subcommand runs (resolve a role) ---
# We assert only that the binary resolves and runs — not its semantic output —
# so the check stays independent of any specific sprint's contents.
RESOLVE_OUT="$(momentum-tools agent resolve --help 2>&1 || momentum-tools agent resolve 2>&1 || true)"
if printf '%s' "$RESOLVE_OUT" | grep -qiE 'command not found'; then
  note_fail "'momentum-tools agent resolve' could not launch: $RESOLVE_OUT"
else
  echo "subcommand 'agent resolve' launched (binary is callable for build operations)"
fi

# --- Assert 4: resolution is location-independent (works from a fresh temp dir) ---
TMPDIR_CHECK="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_CHECK"' EXIT
FROM_TMP="$(cd "$TMPDIR_CHECK" && command -v momentum-tools 2>/dev/null || true)"
if [ -z "$FROM_TMP" ]; then
  note_fail "bare 'momentum-tools' does not resolve from an unrelated working directory ($TMPDIR_CHECK)"
else
  echo "resolves from unrelated directory: $FROM_TMP"
fi

if [ "$FAILED" -ne 0 ]; then
  echo "RESULT: FAIL — momentum-tools is not reliably resolvable as a bare command on PATH"
  exit 1
fi

echo "PASS — bare 'momentum-tools' resolves and runs from any working directory"
