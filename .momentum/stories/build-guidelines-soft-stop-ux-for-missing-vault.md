---
title: build-guidelines soft-stop UX for missing vault
story_key: build-guidelines-soft-stop-ux-for-missing-vault
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-practice-knowledge-base
story_type: feature
depends_on: []
touches: []
---

# build-guidelines soft-stop UX for missing vault

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want build-guidelines to soft-stop with a clear error and recovery instructions when no vault exists,
so that I know exactly what to do next rather than receiving a cryptic failure or silently degraded output.

## Description

Implement the soft-stop behavior in build-guidelines (per DEC-008 D2) when no vault exists: error text shown to developer, instructions on next action (run /momentum:kb-init then /momentum:kb-ingest), expected developer response. The decision is recorded but the implementation detail must be captured before it can be tested.

**Pain context:** DEC-008 D2 records the decision that build-guidelines soft-stops when no vault is found, but the implementation detail (exact error text, recovery instructions, expected developer response) has not been specified. Without this story, the soft-stop behavior is undefined and cannot be tested or validated against the acceptance condition.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- build-guidelines detects when no vault exists and halts with a soft-stop (not a crash or silent degradation)
- The error message clearly explains the missing vault condition to the developer
- Recovery instructions are shown: run /momentum:kb-init then /momentum:kb-ingest
- The soft-stop behavior is testable (verifiable in AVFL checkpoint)
- The implementation is consistent with DEC-008 D2

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
