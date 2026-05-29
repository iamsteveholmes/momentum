#!/usr/bin/env bash
# practice-ledger-hygiene-2026-05-26.sh
# One-shot hygiene script: close 12 stale entries from the pre-2026-05 archive.
# Story: A2 — Practice-ledger hygiene cleanup — close 12 stale entries
# Date: 2026-05-26
# DO NOT re-run after a successful pass — idempotency note in story A2 dev notes.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TOOLS="python3 ${PROJECT_ROOT}/skills/momentum/scripts/momentum-tools.py practice-ledger consume"

# Superseded entries (8)
${TOOLS} --entity-id iq-20260424205245-50b859cb --actor developer --source triage --outcome-ref "superseded:design-pass-4-7"
${TOOLS} --entity-id iq-20260516154102-22515545 --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-024"
${TOOLS} --entity-id iq-20260516154102-1ae5c62a --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-024"
${TOOLS} --entity-id iq-20260516154102-d032731e --actor developer --source triage --outcome-ref "superseded:DEC-020"
${TOOLS} --entity-id iq-20260516154102-f89de525 --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-025"
${TOOLS} --entity-id iq-20260516154102-221bdb70 --actor developer --source triage --outcome-ref "superseded:DEC-023"
${TOOLS} --entity-id iq-20260516154102-f098660a --actor developer --source triage --outcome-ref "superseded:DEC-026"
${TOOLS} --entity-id iq-20260518032341-976884b5 --actor developer --source triage --outcome-ref "superseded:DEC-029"

# Test/leftover entries (4)
${TOOLS} --entity-id iq-20260416054851-aec14053 --actor developer --source triage --outcome-ref "test-leftover"
${TOOLS} --entity-id iq-20260416055625-ab0b3dc4 --actor developer --source triage --outcome-ref "test-leftover"
${TOOLS} --entity-id iq-20260416055626-153bbdd3 --actor developer --source triage --outcome-ref "test-leftover"
${TOOLS} --entity-id iq-20260416055624-9f5c9655 --actor developer --source triage --outcome-ref "test-leftover"

echo "Done: 12 consumed events appended."
