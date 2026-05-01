---
title: Retro Pipeline Idempotency — Detect Prior Attempt and Resume or Restart
story_key: retro-pipeline-idempotency
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Retro Pipeline Idempotency — Detect Prior Attempt and Resume or Restart

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a retro workflow,
I want detect a prior incomplete retro attempt for the same sprint and offer to resume from the last checkpoint or restart cleanly,
so that retro is not re-attempted from scratch when interrupted — up to 3x wasted effort eliminated.

## Description

The retro pipeline was attempted 3 times for sprint-2026-04-08 due to interruptions and partial failures. Each restart discarded prior preprocessing work. Idempotency means the workflow checks for a partial retro artifact, presents the developer with the prior state, and offers resume or restart options.

**Pain context:** Sprint-2026-04-08 retro (#6). 3 restart attempts wasted significant compute. The retro is one of the most expensive workflows (~30 min, multiple subagents). Restarts should be cheap checkpointed resumes, not full reruns.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Retro workflow checks for existing partial retro artifact at sprint start
- If found: presents last checkpoint state, offers [R]esume or [S]tart over
- Preprocessing step (DuckDB extraction) cached — not re-run if output exists and sprint logs unchanged
- Auditor team phase resumable from last completed auditor
- Clean restart removes all partial artifacts before beginning

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
