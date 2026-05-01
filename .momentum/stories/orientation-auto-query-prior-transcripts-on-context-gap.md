---
title: Impetus orientation — auto-query prior transcripts on context gap
story_key: orientation-auto-query-prior-transcripts-on-context-gap
status: backlog
epic_slug: stay-oriented-impetus
feature_slug: 
story_type: exploration
depends_on: []
touches: []
---

# Impetus orientation — auto-query prior transcripts on context gap

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Impetus to detect context gaps and auto-query prior session transcripts,
so that I don't have to manually remind the agent of earlier decisions.

## Description

Investigate whether the session-orientation skill (momentum:impetus) can detect a context-gap (e.g., user references an earlier decision not in current context) and auto-query prior session transcripts via DuckDB (the existing transcript-query.py tool) to recover the missing context. Touches: skills/momentum/skills/impetus/workflow.md, skills/momentum/scripts/transcript-query.py.

**Pain context:** auditor-human H30 ('Do you still have the context of our story selection?') from nornspun sprint-2026-04-12 retro. Signal type: Context.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Explore whether Impetus can reliably detect a context-gap signal (user referencing prior decisions not in current session context)
- Evaluate feasibility of Impetus auto-invoking transcript-query.py (DuckDB) to recover missing context
- Produce a decision on whether to build this capability, with triggering heuristics if proceeding
- Source signal: retro auditor-human finding H30 from nornspun sprint-2026-04-12

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
