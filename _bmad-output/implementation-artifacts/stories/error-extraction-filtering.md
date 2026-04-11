---
title: Error Extraction Filtering — Exclude Informational Non-Zero Exits from Error Reports
story_key: error-extraction-filtering
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Error Extraction Filtering — Exclude Informational Non-Zero Exits from Error Reports

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a retro transcript analysis,
I want distinguish between informational non-zero exits (grep with no matches, diff with differences) and actual errors in transcript extraction,
so that error reports in retro analysis reflect real failures, not tool conventions — false positives don't obscure real errors.

## Description

Tools like grep exit 1 when no matches are found — this is not an error. Diff exits 1 when files differ — also not an error. The current error extractor treats all non-zero exits as errors, producing noise that obscures real failures. A whitelist of tools whose non-zero exits are informational would fix this.

**Pain context:** Sprint-2026-04-08 retro (#14). Informational exits inflated error counts. Note: transcript-query-calibration (done) fixed string-matching vs is_error flag for errors in agent messages. This story is about exit code interpretation in shell commands — a distinct gap.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Error extractor maintains a whitelist of tools with informational non-zero exits (grep, diff, test, etc.)
- Non-zero exits from whitelisted tools excluded from error reports
- Exit code + tool name combination used for classification (not exit code alone)
- Error count in retro reports reflects actual failures

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
