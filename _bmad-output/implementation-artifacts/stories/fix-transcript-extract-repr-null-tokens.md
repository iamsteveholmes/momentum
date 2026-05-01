---
title: Fix transcript extract repr() NULL tokens in tool-result fields
story_key: fix-transcript-extract-repr-null-tokens
status: backlog
epic_slug: impetus-core
feature_slug: 
story_type: defect
depends_on: []
touches: []
---

# Fix transcript extract repr() NULL tokens in tool-result fields

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want transcript extract output to be valid JSON (no bare NULL tokens in tool-result fields),
so that downstream JSON parsers do not fail on transcript-query.py output.

## Description

Distinct from transcript-query-calibration (which fixed error-detection false-positives via structural indicators). This defect concerns extract OUTPUT encoding: Python repr() in transcript-query.py produces bare NULL tokens in tool-result fields, which break downstream JSON parsing. Replace Python repr() with json.dumps() for tool-result fields; add downstream validator to reject bare NULL tokens. Note: parse-error count of 16/122 was largely driven by replica transcripts from the PA-04 retro fan-out bug, not extractor failure — re-verify parse-error rate after fix-retro-documenter-replication-defect lands. If below tolerance at that point, this may be deferrable. Touches: skills/momentum/scripts/transcript-query.py. Cites: transcript-query-calibration story.

**Pain context:** auditor-execution E12 reframed via E15 from nornspun sprint-2026-04-12 retro. Signal type: Failure.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Replace Python `repr()` with `json.dumps()` for tool-result fields in `skills/momentum/scripts/transcript-query.py`
- Add a downstream validator that rejects bare NULL tokens in extractor output
- Re-verify parse-error rate after `fix-retro-documenter-replication-defect` lands; if below tolerance, reassess priority or defer
- Output from transcript-query.py must parse cleanly as JSON with no bare NULL literals in tool-result fields

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
