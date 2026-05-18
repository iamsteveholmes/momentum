---
title: "intake: discovered-from lineage capture for mid-sprint discovered work"
story_key: intake-discovered-from-lineage-capture
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-backlog-refinement
story_type: feature
depends_on:
  - epic-feature-collapse-closeable-grouping
touches: []
---

# intake: discovered-from lineage capture for mid-sprint discovered work

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to add discovered-from lineage capture to intake so mid-sprint discovered work carries its origin sprint and triggering story slug,
so that sprint scope drift is traceable — every discovered story has an audit trail back to how and when it was born.

## Description

Augmentation of the existing backlog story `consolidate-intake-invocation-and-fix-error`. Adds: (1) when intake captures a story born mid-sprint (outside of planning), it sets a `discovered-from` field pointing to the originating sprint + triggering story slug; (2) origin and closure navigation — from a discovered story you can navigate to the sprint it was discovered in and the story that triggered discovery. This is the intake half of DEC-030 D2's born-separate discovered work model.

Source: DEC-030 D2 (triage — DEC-030 blast-radius discovery).

**Pain context:** Without lineage, mid-sprint discovered work is invisible in sprint accounting. DEC-030 D2 requires born-separate origin/closure navigation.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- (1) intake accepts optional discovered-from fields: sprint_slug + triggering_story_slug
- (2) when set, the stub includes discovered-from in frontmatter
- (3) the discovered story can be navigated to its origin sprint
- (4) the triggering story can navigate to stories it spawned (closure navigation)
- (5) intake does not require discovered-from — it is nullable for normally-planned stories

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

- DEC-030 D2 — born-separate discovered work model
- `consolidate-intake-invocation-and-fix-error` — related intake story this augments

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
