---
title: "upstream-fix fixture: root-cause-not-symptom"
story_key: upstream-fix-fixture-root-cause-not-symptom
status: backlog
epic_slug: epic-6-the-practice-compounds
feature_slug: momentum-retro-and-flywheel
story_type: practice
depends_on: []
touches: []
---

# upstream-fix fixture: root-cause-not-symptom

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:upstream-fix proposes the spec/rule fix when a quality failure has both a spec gap and a code gap,
so that we catch surface fixes that don't prevent recurrence.

## Description

Build a behavioral micro-eval fixture that verifies momentum:upstream-fix proposes the spec/rule fix when a quality failure has both a spec gap and a code gap, instead of jumping to the surface code patch. Catches surface fixes that don't prevent recurrence.

**Pain context:** Surface-level fixes that patch symptoms without addressing the spec or rule gap allow the same failure mode to recur. Without an executable regression check, drift in upstream-fix's root-cause discipline is invisible until a retro surfaces a recurrence.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture exists in the micro-eval fixture directory targeting skill `momentum:upstream-fix`
- Fixture provides a synthetic quality failure scenario with both a spec gap and a code gap
- Fixture asserts that the proposed fix targets the spec/rule level, not the surface code patch
- Fixture conforms to the canonical SCHEMA.md (depends on M2)
- Fixture documents the source finding/sprint that motivated it

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
