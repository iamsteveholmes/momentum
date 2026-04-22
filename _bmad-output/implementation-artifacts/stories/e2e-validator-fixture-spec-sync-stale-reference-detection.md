---
title: "e2e-validator fixture: spec-sync stale reference detection"
story_key: e2e-validator-fixture-spec-sync-stale-reference-detection
status: backlog
epic_slug: epic-3-automatic-quality-enforcement
feature_slug: momentum-quality-gates-enforced
story_type: practice
depends_on: []
touches: []
---

# e2e-validator fixture: spec-sync stale reference detection

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:e2e-validator detects stale references in Maestro / E2E test fixtures after a UX copy change,
so that the spec-sync class of failure surfaced in the nornspun retro is guarded against regression.

## Description

Build a behavioral micro-eval fixture that verifies momentum:e2e-validator detects stale references in Maestro / E2E test fixtures after a UX copy change. Real failure class from nornspun retro — stale "The Nornspun Experience" copy referenced in a Maestro test after the UX story removed it.

**Pain context:** This is a real, documented failure class from the nornspun retro. UX copy changes that ripple into E2E fixtures are a common spec-sync hazard. Without an executable fixture, e2e-validator regressions on stale-reference detection will only surface after a real divergence costs another retro.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture sets up a synthetic UX spec with a copy change that removes a string
- Fixture sets up a Maestro / E2E test fixture that still references the removed string
- Fixture invokes momentum:e2e-validator against the diff/state
- Fixture asserts the validator surfaces the stale reference as a finding
- Fixture asserts the finding identifies the offending file and line
- Fixture is wired into the practice micro-eval suite

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
