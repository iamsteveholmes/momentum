---
title: quick-fix fixture: epic_slug "ad-hoc" used silently
story_key: quick-fix-fixture-epic-slug-ad-hoc-used-silently
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quick-fix-workflow
story_type: practice
depends_on: []
touches: []
---

# quick-fix fixture: epic_slug "ad-hoc" used silently

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:quick-fix uses epic_slug "ad-hoc" silently,
so that the quick-fix orchestrator never asks the developer for an epic and the `feedback_quickfix_epic_ad_hoc` user memory is enforced as an executable test.

## Description

Build a behavioral micro-eval fixture that verifies momentum:quick-fix uses epic_slug "ad-hoc" silently and never asks the developer. Encodes the `feedback_quickfix_epic_ad_hoc` user memory as an executable test.

**Pain context:** This feedback memory keeps surfacing — without an executable fixture, regressions in quick-fix that prompt the developer for an epic_slug will go undetected until the developer notices and corrects them again. Encoding the rule as a behavioral micro-eval converts a recurring soft preference into a hard guarantee.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture invokes momentum:quick-fix with a representative defect input
- Fixture asserts the orchestrator never emits a question/prompt about epic_slug to the developer
- Fixture asserts the resulting story is created under epic_slug "ad-hoc"
- Fixture fails loudly (non-zero exit) when the orchestrator asks for an epic or uses any other epic_slug
- Fixture is wired into the practice micro-eval suite alongside other behavioral fixtures

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
