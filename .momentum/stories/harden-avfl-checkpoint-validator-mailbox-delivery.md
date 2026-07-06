---
title: "Harden AVFL checkpoint-validator mailbox delivery — no self-read fallback, degraded state on failure"
story_key: harden-avfl-checkpoint-validator-mailbox-delivery
status: backlog
epic_slug: momentum-quality-gates-enforced
feature_slug:
story_type: defect
priority: high
depends_on: []
touches: []
---

# Harden AVFL checkpoint-validator mailbox delivery — no self-read fallback, degraded state on failure

<!-- RETRO STUB: created by momentum:retro from the sprint-2026-06-28 transcript audit
     (2026-07-06), approved at the Phase 5 stub gate. It is a stub, NOT a dev-ready story.
     All sections below marked DRAFT require full rewrite by create-story. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As the practice maintainer,
I want AVFL checkpoint validators to deliver findings through the mailbox path with hard failure semantics,
so that a plan gate can never ship a scored CLEAN verdict that no validator actually earned.

## Description

The sprint-2026-06-28 pre-sprint plan gate shipped a "CLEAN/95" verdict that was a single orchestrator's self-graded artifact read: all 3 async-spawned checkpoint validators (structural/coherence/domain) failed to deliver structured findings back via the mailbox path. The orchestrator disclosed this honestly as a caveat on the shipped HTML, but nothing in the pipeline enforces that disclosure — a differently-behaved orchestrator could report CLEAN/95 with no caveat and nothing would catch it.

**Pain context:** the single mandatory pre-build quality verdict was structurally unearned; the failure mode is silent and repeats on every plan gate until fixed.

## Acceptance Criteria

<!-- DRAFT: rough ACs from the retro audit return. NOT refined or validated.
     This section MUST be fully rewritten by create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Structural/Coherence/Domain checkpoint validators deliver findings back to the orchestrator via the mailbox path without requiring a self-read fallback
- If mailbox delivery fails, the consolidator surfaces an explicit degraded/BLOCKED state rather than a scored CLEAN/N verdict
- A dry run confirms end-to-end 3-lens finding delivery before the next plan gate ships

> Note: The ACs above are rough captures from the audit. Create-story will replace them
> with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Retro audit return: `.momentum/sprints/sprint-2026-06-28/audit-return.json` (priority item 2)
- Dedup: zero collisions across 285 open stories + 17 open ledger entries (workflow `wf_7b949d2b-a8e`, 2026-07-06)

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
