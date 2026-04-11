---
title: Shared File Contention Fix — Serialize Access During Parallel Dev
story_key: shared-file-contention-fix
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Shared File Contention Fix — Serialize Access During Parallel Dev

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint-dev orchestrator,
I want serialize write access to shared files (index.json, sprint status) when multiple dev agents run in parallel,
so that race conditions between parallel dev agents writing to shared files are eliminated — no more corrupted sprint state.

## Description

When multiple dev agents run in parallel (sprint-dev Phase 2 wave), they each try to write to stories/index.json and sprint-status files. Without serialization, concurrent writes corrupt the JSON. A file-level lock or a queue-based write pattern is needed.

**Pain context:** Sprint-2026-04-08 retro (#11). JSON corruption from parallel writes was observed. The parallel dev wave is the core performance feature of sprint-dev — removing it is not acceptable. Serialization must be added without breaking parallelism for the implementation work.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- stories/index.json writes are serialized via a file lock or queue
- Sprint status updates serialized via the same mechanism
- Dev agents wait for lock rather than failing on contention
- Parallel implementation work unaffected — only shared-file writes are serialized
- Unit test demonstrates concurrent write safety

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
