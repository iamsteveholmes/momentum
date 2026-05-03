---
title: Momentum Cycle — Story L3 Drill-Down (Reading Mode)
story_key: momentum-cycle-story-l3-drill-down-reading-mode
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-feature-l2, momentum-cycle-sprint-lens]
touches: []
---

# Momentum Cycle — Story L3 Drill-Down (Reading Mode)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to read a story's full detail in a polished, typography-focused view inside the practice pane,
so that I can review and approve stories without opening raw markdown files and breaking my flow.

## Description

Implement the Story Level-3 detail view — the deepest drill-down surface in the Momentum Cycle navigation hierarchy. Polarity: reading mode (warm light, same as L2 — no polarity flip when coming from L2, only flip when coming from Sprint detail dark surface).

Surface renders:
- Story frontmatter strip (slug, type, status, epic, derives_from) as JetBrains Mono meta
- Source Serif 4 title
- Value narrative (if present)
- Numbered acceptance criteria (Source Serif 4, numbered list)
- Workflow phases (if story has a workflow field)
- Dev notes section
- File list (if story touches files)

Reachable from TWO entry points:
1. Feature L2 stories list → breadcrumb becomes "Dashboard / Feature / Story"
2. Sprint detail outcome bands → breadcrumb becomes "Dashboard / Sprint / Story"

Single Hono route `/stories/{slug}` with a query param indicating entry context (`?from=feature` or `?from=sprint`) for correct breadcrumb OOB swap. Story data read from `.momentum/stories/` directory (individual story files).

Reading experience: 65ch measure, 18px body, 1.70 line-height, Source Serif 4 throughout except meta/code elements.

**Pain context:** Developers must open raw markdown story files to approve stories, which breaks flow. Story L3 renders stories as a polished reading surface directly in the practice pane. Designed and prototype-approved in a 10-pass design review session (claude.ai/design prototype approved).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Hono route `/stories/{slug}` renders story detail HTML
- Query param `?from=feature` swaps breadcrumb to "Dashboard / Feature / Story" via HTMX OOB
- Query param `?from=sprint` swaps breadcrumb to "Dashboard / Sprint / Story" via HTMX OOB
- Surface uses warm-light polarity (same as L2 — no flip when arriving from Feature L2)
- Frontmatter strip renders slug, type, status, epic, derives_from in JetBrains Mono
- Title renders in Source Serif 4 at appropriate heading scale
- Value narrative section renders if present in story frontmatter/body
- Acceptance criteria render as numbered list in Source Serif 4
- Workflow phases section renders if story has workflow field
- Dev notes section renders (collapsed or summary if long)
- File list renders if story has touches array with entries
- Reading measure is 65ch, body 18px, line-height 1.70
- Story data sourced from `.momentum/stories/{slug}.md`
- Navigation back to entry point works correctly from breadcrumb

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
