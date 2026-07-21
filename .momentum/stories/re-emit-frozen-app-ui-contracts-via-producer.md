---
title: "Re-emit frozen app-ui contracts via the producer so headers match the smoke decision (contract-quality)"
story_key: re-emit-frozen-app-ui-contracts-via-producer
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: low
depends_on: []
touches: []
---

# Re-emit frozen app-ui contracts via the producer so headers match the smoke decision (contract-quality)

<!-- BACKFILL STUB: this story's index entry (stories/index.json) claimed
     story_file: true with no backing file — a phantom entry found by the
     2026-07-06 retro audit of sprint-2026-06-28. This stub repairs the
     phantom by giving the entry a real backing file. It is a backlog stub,
     NOT a dev-ready story. Dedup-confirmed distinct from the other
     `momentum-sprint-orchestration` phantom-repaired stories. -->

_This story is a backlog stub — run `momentum:create-story` on it when ready to
make it dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a practice maintainer,
I want the frozen app-ui verification contracts re-emitted through their producer (rather than hand-edited),
so that each contract's header metadata matches the smoke-vs-driver method decision actually made for it, instead of drifting out of sync with a manual edit.

## Description

This story's own scope is contract-quality maintenance: identify the frozen app-ui contracts whose headers no longer match their smoke decision, and re-emit them through the producer so the fix is a regeneration, not a hand patch that can drift again. This scope belongs to this slug alone; it does not absorb or duplicate the two-column verification-model decision owned by `verification-method-two-column-smoke-ui-model` or any other sprint-orchestration story.

## Acceptance Criteria

_Not yet defined — run `momentum:create-story` to enrich this stub with validated, testable acceptance criteria._

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Source: 2026-07-06 retro transcript audit of sprint-2026-06-28 (`audit-return.json` priority items 1 + 3), dedup-verified 2026-07-06 (confirmed distinct from other `momentum-sprint-orchestration` phantom entries).
- Repaired by: `.momentum/stories/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.md` (this story's backing-file repair, not its scope).
- Related (separate scope, do not merge): `.momentum/stories/verification-method-two-column-smoke-ui-model.md`.
- Epic context: `momentum-sprint-orchestration` (from `_bmad-output/planning-artifacts/epics.json`).

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
