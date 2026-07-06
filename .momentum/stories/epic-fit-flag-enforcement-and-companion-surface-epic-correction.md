---
title: "Enforce unresolved epic-fit flags at grooming/planning + correct companion-surface-pre-sprint-plan-gate epic"
story_key: epic-fit-flag-enforcement-and-companion-surface-epic-correction
status: backlog
epic_slug: momentum-backlog-refinement
feature_slug:
story_type: maintenance
priority: medium
depends_on: []
touches: []
---

# Enforce unresolved epic-fit flags at grooming/planning + correct companion-surface-pre-sprint-plan-gate epic

<!-- RETRO STUB: created by momentum:retro from the sprint-2026-06-28 transcript audit
     (2026-07-06), approved at the Phase 5 stub gate. It is a stub, NOT a dev-ready story.
     All sections below marked DRAFT require full rewrite by create-story. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As the practice maintainer,
I want epic-fit flags raised by create-story to block sprint selection until resolved, and the known misassignment corrected,
so that stories stop shipping and merging under demonstrably wrong epics while a correct HIGH-confidence flag sits ignored.

## Description

`companion-surface-pre-sprint-plan-gate` shipped and merged under epic `momentum-impetus-experience`, which does not list it in its `stories[]` array. A dual-lens HIGH-confidence create-story finding said exactly this ("this slug isn't in that epic's stories[] array... Recommend reassigning before sprint selection") and went unactioned through planning and merge — the flag mechanism worked; nothing enforces acting on it. A second instance of the same pattern: `retro-audit-workflow-process-findings-return` was misfiled under `momentum-impetus-experience` (corrected during the 2026-07-06 retro).

Dedup note (verified): `encode-epic-semantic-model` does NOT absorb this — that story fixes classification-time ambiguity via a reference doc; this story adds selection-time enforcement of an already-raised flag. Distinct mechanisms.

## Acceptance Criteria

<!-- DRAFT: rough ACs from the retro audit return. NOT refined or validated.
     This section MUST be fully rewritten by create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- The story's `epic_slug` is corrected to an epic listing it in `stories[]` (or the target epic's `stories[]` is updated to include it)
- epic-grooming or sprint-planning gains a check for unresolved "flagged, not changed" epic-fit findings before a story is selected into a sprint

> Note: The ACs above are rough captures from the audit. Create-story will replace them
> with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Retro audit return: `.momentum/sprints/sprint-2026-06-28/audit-return.json` (priority item 7)
- Dedup refutation of `encode-epic-semantic-model` absorb-claim: workflow `wf_7b949d2b-a8e` (2026-07-06)

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
