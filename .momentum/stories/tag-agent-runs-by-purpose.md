---
title: tag-agent-runs-by-purpose
story_key: tag-agent-runs-by-purpose
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-spawn-orchestration
story_type: feature
depends_on: []
touches: []
---

# tag-agent-runs-by-purpose

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want agent runs tagged by purpose (sprint-story / benchmark / ingest / exploratory) in transcript metadata with filtering support in transcript-query,
so that sprint throughput metrics accurately reflect real story work — not benchmark or ingest noise — and retro efficiency analysis can isolate purpose-specific effort.

## Description

Tag agent runs by purpose (sprint-story / benchmark / ingest / exploratory) in transcript metadata and support filtering by purpose in transcript-query. In sprint-2026-05-03, 25-30% of sprint agent-effort was benchmark/ingest work commingled with real story work, obscuring sprint throughput metrics. The purpose tag should be: (1) set at spawn time by the orchestrator, (2) embedded in transcript metadata, (3) filterable in transcript-query and retro DuckDB analysis, (4) included in retro efficiency metrics.

**Pain context:** In sprint-2026-05-03, 25–30% of agent effort was benchmark/ingest work mixed into the same sprint transcript stream as real story work. The retro could not cleanly separate story throughput from incidental work, making efficiency metrics unreliable. Without purpose tagging, every future sprint with mixed-mode agent activity will have the same blind spot.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Orchestrators (sprint-dev, quick-fix, retro, etc.) set a `purpose` tag at agent spawn time
- Purpose tag is one of: `sprint-story`, `benchmark`, `ingest`, `exploratory`
- Purpose tag is embedded in transcript metadata so it persists with the transcript record
- `transcript-query` supports filtering by purpose (e.g., `--purpose sprint-story`)
- Retro DuckDB analysis can filter/group by purpose when computing efficiency metrics
- Retro report includes per-purpose effort breakdown (e.g., "72% sprint-story, 25% benchmark, 3% exploratory")

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
