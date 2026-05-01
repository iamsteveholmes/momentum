---
title: Story Spec Completeness Checklist — Templates, DRAFT Markers, and Lifecycle Validation
story_key: story-spec-completeness-checklist
status: backlog
epic_slug: story-cycles
depends_on: []
touches: []
---

# Story Spec Completeness Checklist — Templates, DRAFT Markers, and Lifecycle Validation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a create-story workflow,
I want validate that every enriched story has required sections, no orphaned DRAFT markers, and lifecycle field consistency before declaring dev-ready,
so that dev agents never encounter incomplete or inconsistently marked stories — spec quality is machine-validated, not eyeballed.

## Description

Stories passed to dev agents sometimes have orphaned DRAFT markers (not replaced by create-story), missing required sections, or lifecycle field inconsistencies (status: backlog in frontmatter but story text says in-progress). A completeness checklist, run as the final create-story step, would catch these before the story is marked dev-ready.

**Pain context:** Sprint-2026-04-08 retro (#9). Dev agents stumbled on incomplete stories twice. The DRAFT marker replacement step is manual and prone to omission.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Create-story final step includes completeness check
- Check validates: no DRAFT markers remain, all required sections populated, status field consistent
- Incomplete story flagged with specific location of the problem
- Story NOT marked dev-ready until checklist passes
- Checklist failures surfaced to developer for resolution

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
