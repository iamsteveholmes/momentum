#!/usr/bin/env bash
# conduct-cleanup-dead-agent-paths-and-validate-resolve smoke contract
#
# === VERIFICATION HEADER (Part A) ===
# story_slug: conduct-cleanup-dead-agent-paths-and-validate-resolve
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-cleanup-dead-agent-paths-and-validate-resolve.smoke.sh
# how_dev_self_checks: |
#   Before you signal done, open a normal shell and ask the agent-routing tool to resolve every
#   role the routing table claims to know. For each role, the tool either points you at an agent
#   description that actually exists on disk, or it fails loudly and clearly — it must never report
#   success while handing back a path to a file that is not there. Pick a role the old table mapped
#   to a missing file (for example the architect role) and confirm one of two acceptable outcomes:
#   either that role is gone from the routing table entirely, or asking to resolve it returns a
#   visible failure that names the missing file rather than a cheerful success. Then resolve the
#   three roles the build actually relies on — the implementer/developer role, the code reviewer
#   role, and the end-to-end validator role — and confirm each one succeeds AND that the path it
#   returns is a file you can actually open. Finally, sweep every role the table still advertises
#   and confirm there is no remaining entry that resolves "successfully" to a file that does not
#   exist. If any role reports success but points at a missing file, the cleanup and the
#   existence check are not yet done.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/conduct-cleanup-dead-agent-paths-and-validate-resolve.md#acceptance-criteria
# platforms: [host]
#
# === VERIFIER CONTRACT BODY (Part B) ===
# Invocation:
#   bash .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-cleanup-dead-agent-paths-and-validate-resolve.smoke.sh
#
# Expected: resolving a role never reports success while returning a path to a missing file;
#           a previously-dead role is either gone or fails loudly; and the three roles the build
#           relies on (developer, code reviewer, end-to-end validator) each resolve to a file
#           that actually exists.

set -uo pipefail

FAILED=0
note_fail() { echo "FAIL: $1"; FAILED=1; }

# Resolve a role through the public agent-routing command and print the file path it claims,
# using only observable command output. We try common output shapes (JSON 'path'/'body' field,
# or a bare path line) without assuming internal field names beyond the public surface.
resolve_path() {
  local role="$1" out
  out="$(momentum-tools agent resolve --role "$role" --json 2>/dev/null \
        || momentum-tools agent resolve --role "$role" 2>/dev/null || true)"
  # Extract the first thing that looks like a file path ending in .md from the output.
  printf '%s' "$out" | grep -oE '[A-Za-z0-9_./-]+\.md' | head -n1
}

resolve_reports_success() {
  local role="$1" out
  out="$(momentum-tools agent resolve --role "$role" --json 2>/dev/null \
        || momentum-tools agent resolve --role "$role" 2>/dev/null || true)"
  printf '%s' "$out" | grep -qiE '"success"[[:space:]]*:[[:space:]]*true|success'
}

# --- Assert 1: a previously-dead role is either removed or fails loudly (not silent success) ---
DEAD_ROLE="architect"
DEAD_OUT="$(momentum-tools agent resolve --role "$DEAD_ROLE" --json 2>&1 \
           || momentum-tools agent resolve --role "$DEAD_ROLE" 2>&1 || true)"
DEAD_PATH="$(resolve_path "$DEAD_ROLE")"
if printf '%s' "$DEAD_OUT" | grep -qiE 'unknown role|not found|no such role|no entry'; then
  echo "dead role '$DEAD_ROLE' is removed from the routing table (resolve fails clearly)"
elif [ -n "$DEAD_PATH" ] && [ ! -e "$DEAD_PATH" ]; then
  note_fail "role '$DEAD_ROLE' resolved 'successfully' to a missing file: $DEAD_PATH"
elif [ -n "$DEAD_PATH" ] && [ -e "$DEAD_PATH" ]; then
  echo "role '$DEAD_ROLE' now resolves to an existing body: $DEAD_PATH"
else
  echo "role '$DEAD_ROLE' did not resolve to any path (acceptable if removed)"
fi

# --- Assert 2: the three roles the build relies on each resolve to a file that exists ---
for ROLE in dev qa-reviewer e2e-validator; do
  P="$(resolve_path "$ROLE")"
  if [ -z "$P" ]; then
    note_fail "build-critical role '$ROLE' did not resolve to any path"
  elif [ ! -e "$P" ]; then
    note_fail "build-critical role '$ROLE' resolved to a missing file: $P"
  else
    echo "build-critical role '$ROLE' resolves to an existing body: $P"
  fi
done

# --- Assert 3: no advertised role resolves 'successfully' to a non-existent file ---
# Sweep the roles named in this story's cleanup scope plus the build-critical set.
for ROLE in architect pm sm ux analyst researcher dev qa-reviewer e2e-validator; do
  P="$(resolve_path "$ROLE")"
  if [ -n "$P" ] && [ ! -e "$P" ] && resolve_reports_success "$ROLE"; then
    note_fail "role '$ROLE' reports success but points at a missing file: $P"
  fi
done
echo "swept advertised roles for success-pointing-at-missing-file"

if [ "$FAILED" -ne 0 ]; then
  echo "RESULT: FAIL — a role resolves successfully to a missing agent body, or a build-critical role is broken"
  exit 1
fi

echo "PASS — no role reports success for a missing file; build-critical roles resolve to existing bodies"
