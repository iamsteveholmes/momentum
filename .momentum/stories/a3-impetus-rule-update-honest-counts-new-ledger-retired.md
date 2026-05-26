---
title: "A3: Impetus rule update — honest counts, new ledger, retired signals"
story_key: a3-impetus-rule-update-honest-counts-new-ledger-retired
status: backlog
epic_slug: ad-hoc
feature_slug: ""
story_type: practice
depends_on: ["A1"]
touches: []
---

# A3: Impetus rule update — honest counts, new ledger, retired signals

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the experimental Impetus rule updated to surface honest practice-ledger counts via the new summary CLI and drop retired signal references,
so that session-start orientation reflects real practice state instead of test scaffolding noise.

## Description

Implement DEC-033 D9 in the experimental `.claude/rules/impetus.md`. Drop the "last 5" instruction (currently surfaces 80% test scaffolding per AES-003 Finding 4). Replace with honest count surfacing: "N open entries (X this week, Y older than 30 days, Z near auto-close)" plus recurring patterns from history. Use the new `momentum-tools practice-ledger summary` CLI. Update the "where state lives" table to point at `practice-ledger.jsonl` (not intake-queue.jsonl). Remove any references to `.momentum/signals/` (retired per DEC-033 D6). Document the subagent guard remains. Effort: 1–2 hours. Change type: rule-hook. Verification: behavioral trigger test (open fresh session, observe Impetus session-start matches new pattern).

**Pain context:** Implements DEC-033 D9 to fix Impetus session-start surfacing (currently 80% test scaffolding per AES-003 Findings 4, 10). Depends on A1's new summary CLI.

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `.claude/rules/impetus.md` no longer instructs reading "last 5" entries from the ledger
- Session-start surfaces honest counts: "N open entries (X this week, Y older than 30 days, Z near auto-close)" + recurring patterns
- Uses `momentum-tools practice-ledger summary` CLI (from A1)
- "Where state lives" table points at `practice-ledger.jsonl` (not `intake-queue.jsonl`)
- All references to `.momentum/signals/` removed (retired per DEC-033 D6)
- Subagent guard section preserved
- Behavioral trigger test: fresh session shows new pattern

> Note: The ACs above are rough captures from conversation. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
