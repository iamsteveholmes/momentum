---
title: Consolidate capability-fork-rejection record format with coherence-gate Override Decisions convention
story_key: consolidate-capability-fork-rejection-record-format-with
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Consolidate capability-fork-rejection record format with coherence-gate Override Decisions convention

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want have the capability-fork-rejection path reuse the existing coherence-gate.md §7 'Override Decisions' record convention instead of inventing a new one,
so that there is one canonical override-record format instead of two parallel, undocumented-as-related formats that readers must learn separately.

## Description

The capability-fork-rejection path currently invents a new coherence-report.md heading/format rather than reusing coherence-gate.md §7's 'Override Decisions' convention. This is a record-format consolidation decision — a person needs to decide whether the new format should be folded into the existing convention (and how), since the two now describe overlapping concepts (a fork gets rejected/overridden) with divergent formats. Route through momentum:decision before implementation.

**Pain context:** Surfaced by code-review triage during sprint-2026-08-03 build wave (goal-conditions story) as a record-format consolidation concern.

**Source:** triage — Conductor build wave sprint-2026-08-03 (goal-conditions)

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- [ ] Decision recorded on whether/how to fold the new coherence-report.md format into coherence-gate.md §7's Override Decisions convention
- [ ] If consolidated: coherence-report.md updated to emit the shared format; coherence-gate.md §7 updated if the shared format needs to grow to cover the capability-fork case
- [ ] Any existing readers/parsers of either format updated to match

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
