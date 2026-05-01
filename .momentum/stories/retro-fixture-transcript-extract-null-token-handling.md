---
title: "retro fixture: transcript-extract null token handling"
story_key: retro-fixture-transcript-extract-null-token-handling
status: backlog
epic_slug: epic-4-complete-story-cycles
feature_slug: momentum-retro-and-flywheel
story_type: defect
depends_on:
  - fix-transcript-extract-repr-null-tokens
touches: []
---

# retro fixture: transcript-extract null token handling

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies the retro documenter handles null tokens in audit_extracts gracefully,
so that the transcript-extract null-token defect cannot silently regress and corrupt retro outputs.

## Description

Build a behavioral micro-eval fixture that verifies the retro documenter handles null tokens in audit_extracts gracefully and does not silently fail. Depends on the existing story `fix-transcript-extract-repr-null-tokens`.

**Pain context:** The transcript-extract null-token defect previously caused silent failures in retro output. Once the underlying fix lands, this fixture pins the contract so future changes to extract handling cannot reintroduce the silent-failure mode. Defect-class fixtures are the most cost-effective regression guards because the failure mode is already proven.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture provides a synthetic audit_extracts payload containing null tokens
- Fixture invokes the retro documenter against the payload
- Fixture asserts the documenter does not silently fail (no swallowed exceptions, no missing output)
- Fixture asserts either a successful documented retro or a loud, structured error — never a silent partial result
- Fixture is wired into the practice micro-eval suite
- Fixture is gated to run only after `fix-transcript-extract-repr-null-tokens` is merged

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
