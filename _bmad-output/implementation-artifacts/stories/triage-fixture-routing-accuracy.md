---
title: "triage fixture: routing accuracy"
story_key: triage-fixture-routing-accuracy
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quality-gates-enforced
story_type: practice
depends_on: []
touches: []
---

# triage fixture: routing accuracy

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:triage achieves >=80% classification accuracy across all six triage classes,
so that triage misclassifications (which silently route observations to the wrong downstream skill) are caught by an executable assertion rather than discovered in retro.

## Description

Build a behavioral micro-eval fixture that verifies the momentum:triage skill achieves >=80% classification accuracy when given mixed observations spanning all six classes (ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT). Catches misclassification → wrong downstream skill. Part of the ForgeCode-style retro→micro-eval loop.

**Pain context:** Triage misclassification is a silent failure — a wrong class routes the observation to the wrong downstream skill (e.g. an ARTIFACT mistakenly classified as DISTILL never becomes a story; a REJECT mistakenly classified as ARTIFACT pollutes the backlog). Without an executable accuracy fixture, regressions only surface in retro.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture provides a labeled corpus of observations spanning all six classes (ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT)
- Fixture asserts overall classification accuracy >= 80%
- Fixture reports per-class precision/recall (or at least confusion counts) so regressions are diagnosable
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern from retro-microeval-loop-analysis-2026-04-21.md
- Fixture fails with an actionable diff showing which observations were misrouted

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

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md
- Triage source: triage — conversation

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
