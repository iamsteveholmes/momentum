---
title: Momentum Cycle — Feature L2 Drill-Down (Reading Mode)
story_key: momentum-cycle-feature-l2-drill-down-reading-mode
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-features-lens]
touches: []
---

# Momentum Cycle — Feature L2 Drill-Down (Reading Mode)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to navigate to a feature's L2 detail view rendered as a typographic reading document,
so that I can read feature details, value narrative, and story list without opening raw markdown files.

## Description

Implement the Feature Level-2 detail view. Polarity flips from dark dashboard to warm light reading mode (--readingPaper: #faf6ec background, Source Serif 4 body text, 65ch measure, 18px body, 1.70 line-height). A 140ms CSS cross-fade handles the dark→light polarity flip on navigation. Sections: feature name as Source Serif 4 heading, status badge + story fraction meta strip, value narrative (prose, 65ch column), acceptance condition (boxed, left border), system context (callout), stories list (Inter, each row shows status icon + title + status label — clicking a story navigates to L3). Dependencies render as list-only (no mode pill, no graph view — confirmed in design). Navigation: hx-push-url="/features/{slug}", breadcrumb OOB swap shows "Dashboard / Feature" with Feature in blue. "Dashboard" segment clickable back to root. Back affordance: breadcrumb Dashboard segment. Reading mode affordance: small "reading mode" label in meta strip (no hover explanation needed — simplified from Pass 7 design).

**Pain context:** Developers must open raw markdown story files to read feature details. The L2 view renders them as a typographic document, replacing direct file reads during sprint planning and grooming.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Navigating to `/features/{slug}` renders the L2 detail view with warm light reading mode background (`--readingPaper: #faf6ec`)
- Page background transitions from dark dashboard to light reading mode with a 140ms CSS cross-fade
- Feature heading renders in Source Serif 4; body text uses Source Serif 4 at 18px, 65ch measure, 1.70 line-height
- Meta strip shows status badge + story fraction (e.g., "3 / 7 stories done") and a small "reading mode" label
- Value narrative section renders as prose in the 65ch column
- Acceptance condition renders in a boxed container with a left border
- System context renders as a callout block
- Stories list renders in Inter; each row shows status icon + title + status label
- Clicking a story row navigates to the L3 story detail view
- Dependencies render as a plain list (no mode pill, no graph view)
- Breadcrumb OOB swap updates to "Dashboard / Feature" with Feature styled in blue; Dashboard segment is a clickable link back to root (`/`)
- `hx-push-url` is set to `/features/{slug}` on navigation so the URL updates correctly

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
