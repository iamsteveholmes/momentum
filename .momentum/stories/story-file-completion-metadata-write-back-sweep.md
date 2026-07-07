---
title: "Sweep and fix the index-done / story-file-stale drift class (completion metadata never written back)"
story_key: story-file-completion-metadata-write-back-sweep
status: backlog
epic_slug: momentum-conductor-core
feature_slug:
story_type: maintenance
priority: medium
depends_on: []
touches: []
---

# Sweep and fix the index-done / story-file-stale drift class

<!-- INTAKE STUB: This story was captured from momentum:refine consolidated gate. It is a
     backlog stub, NOT a dev-ready story. All sections below marked DRAFT require full
     rewrite by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a Momentum developer,
I want the conduct build to write completion metadata back into the story .md files so that index status and story file state stay in sync,
so that the single source of truth for story status is not fragmented between index.json and the story files.

## Description

The conduct build updates `.momentum/stories/index.json` status to `done` but never writes completion metadata back into the story .md file — the story file's status line stays `ready-for-dev`, and the Dev Agent Record remains blank. This creates a systemic drift class where ~160 stories show index status `done` while the story file is stale (verified by the 2026-07-06 refine scan). At least 3 sprint-2026-06-28 stories were confirmed in the retro with index status `done` but story file still showing `ready-for-dev` and blank Dev Agent Record.

This story addresses the metadata write-back gap and ensures the drift class cannot regrow.

**Scope exclusion:** Phantom story_file:true entries (8 identified) are owned by the existing stub `repair-phantom-story-file-entries-and-backfill-live-fixture-scope`.

**Origin:** 2026-07-06 momentum:refine consolidated gate, Fork 3 "Create both" — developer-approved stub; root finding from handoff `next-sprint-cohort-review-2026-07-06.md` §3.2.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from the problem statement. They
     have NOT been validated against architecture or refined for completeness. This section
     MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following acceptance criteria are drafted from the scope statement:

- A one-time sweep reconciles existing stale story files with their index status
  - For each story in .momentum/stories/index.json with status `done`, update the corresponding .md file's status line to `done` if it shows `ready-for-dev`
  - Populate the Dev Agent Record in each swept story file with completion metadata (e.g., timestamp, story state summary)
  - The sweep completes without errors and reports count of stories updated

- The conduct completion path writes status and completion metadata back to the story file
  - When conduct completes a story and writes `done` to index.json, it also writes the status line and metadata to the story .md file
  - Dev Agent Record is populated with conductor-recorded state (merge commit, completion timestamp, story key)
  - Story file status and index status remain synchronized after each conduct completion

- The drift class does not regrow
  - Subsequent conduct builds maintain metadata write-back to story files
  - The sweep and the ongoing write-back together prevent index/file desynchronization

## Dev Notes

### References

- Refinding: 2026-07-06 momentum:refine consolidated gate, Fork 3
- Handoff: `_momentum/handoffs/next-sprint-cohort-review-2026-07-06.md` §3.2
- Related epic: `momentum-conductor-core`
