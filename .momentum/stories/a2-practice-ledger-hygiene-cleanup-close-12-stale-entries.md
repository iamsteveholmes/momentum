---
title: "A2: Practice-ledger hygiene cleanup — close 12 stale entries"
story_key: a2-practice-ledger-hygiene-cleanup-close-12-stale-entries
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: ["A1"]
touches: []
---

# A2: Practice-ledger hygiene cleanup — close 12 stale entries

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to close out the 12 stale practice-ledger entries flagged in AES-003 Finding 3 using the new ledger CLI from A1,
so that the ledger reflects only genuinely open work and `momentum-tools practice-ledger open` returns an accurate count.

## Description

Implement the one-time hygiene pass referenced in AES-003 Finding 3. Using the new CLI from A1, append `consumed` events for the 10 entries with "superseded by DEC-..." in titles (outcome_ref: `"superseded:<dec-id>"`), the 3 entries with "Test:" prefix or "Old triage-inbox.md approach" (outcome_ref: `"test-leftover"`). Verify post-cleanup that `momentum-tools practice-ledger open` returns the expected reduced count. May be implementable as a shell script or just a sequence of CLI invocations — work is data hygiene, not new code. Effort: 1–2 hours. Change type: config-structure. Verification: smoke test (run CLI calls, confirm count drops).

**Pain context:** One-time hygiene pass referenced in AES-003 Finding 3. Depends on A1's new CLI.

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

**Note on depends_on:** Listed as `["A1"]` — the practice-ledger CLI redesign. Final slug to be resolved after A1 intake completes; update this story's `depends_on` to the real A1 slug at create-story time.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Append `consumed` events for the 10 practice-ledger entries whose titles contain "superseded by DEC-..." using outcome_ref `"superseded:<dec-id>"` (with the specific DEC-id extracted per entry).
- Append `consumed` events for the 3 entries with "Test:" prefix or matching "Old triage-inbox.md approach", using outcome_ref `"test-leftover"`.
- All 13 events appended via the new ledger CLI shipped in A1 — no direct edits to the JSONL file.
- Post-cleanup: `momentum-tools practice-ledger open` returns the expected reduced count (12 fewer open entries than pre-cleanup).
- Implementation may be a shell script or a sequence of CLI invocations — both acceptable.
- Smoke test recorded in the story showing pre-count, the CLI calls executed, and post-count.

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
