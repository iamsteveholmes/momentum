---
title: Citation integrity validation in build-guidelines AVFL
story_key: citation-integrity-validation-in-build-guidelines-avfl
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-practice-knowledge-base
story_type: feature
depends_on: []
touches: []
---

# Citation integrity validation in build-guidelines AVFL

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want build-guidelines' AVFL checkpoint to verify that all generated citations resolve to real vault pages,
so that the KB feature acceptance condition ("guidelines cite specific KB passages") is testable and enforced.

## Description

Add a validation step to build-guidelines' AVFL checkpoint that verifies all generated citations resolve to real vault pages. The KB feature acceptance condition hinges on guidelines citing 'specific KB passages' — testable only if the AVFL pass checks citation references against the vault index.

**Pain context:** The KB feature acceptance condition requires guidelines cite "specific KB passages." This condition cannot be tested or enforced if the AVFL checkpoint doesn't verify citation integrity. Without this validation, build-guidelines may generate plausible-looking but broken citation references, silently failing the acceptance condition.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- build-guidelines AVFL checkpoint includes a citation integrity validation step
- The validation verifies each generated citation resolves to a real page in the vault index
- Broken or unresolvable citations cause the AVFL checkpoint to fail with a clear error
- The validation step is documented in the build-guidelines skill spec

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
