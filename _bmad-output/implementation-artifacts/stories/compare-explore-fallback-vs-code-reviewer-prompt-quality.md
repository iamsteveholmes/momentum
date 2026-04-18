---
title: Compare Explore-fallback vs code-reviewer prompt-quality parity
story_key: compare-explore-fallback-vs-code-reviewer-prompt-quality
status: backlog
epic_slug: quality-enforcement
feature_slug: 
story_type: exploration
depends_on: []
touches: []
---

# Compare Explore-fallback vs code-reviewer prompt-quality parity

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to compare the output quality of Explore-as-fallback vs a direct momentum:code-reviewer Skill invocation on the same story,
so that I can determine whether fixing the code-reviewer mis-routing is high or low priority.

## Description

Investigation story (writes findings doc; no direct implementation changes). Sample one Explore-as-fallback output vs a direct momentum:code-reviewer Skill output on the same story. If quality is comparable, avfl-invoke-code-reviewer-via-skill-not-task is lower priority; if divergent, it becomes more valuable.

**Pain context:** auditor-execution E16 from nornspun sprint-2026-04-12 retro. The 8 ViewModel-consolidation review-lens agents were typed Explore (fallback from code-reviewer mis-routing) yet produced real quality findings. Unclear whether fallback matches the real momentum:code-reviewer template. Signal type: Workflow. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Select one story from the nornspun sprint-2026-04-12 ViewModel-consolidation batch as the comparison target
- Run momentum:code-reviewer directly (as a Skill) on that story and capture output
- Compare side-by-side with the Explore-fallback output from the retro record
- Produce a findings doc noting: finding count, finding quality, structural differences (prompt adherence, format, depth)
- Conclude with a priority recommendation for the avfl-invoke-code-reviewer-via-skill-not-task story

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
