---
title: Momentum Cycle — Features Lens
story_key: momentum-cycle-features-lens
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: []
touches: []
---

# Momentum Cycle — Features Lens

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a live Features lens in the Momentum Cycle dashboard that shows feature status, gap flags, and story coverage,
so that I always see current feature state without re-running the feature-status skill manually.

## Description

Implement the Features lens section of the Momentum Cycle dashboard. Reads `features.json` (`_bmad-output/planning-artifacts/features.json`) and `stories/index.json` (`.momentum/stories/index.json`) to render a live table. Each row shows: feature name, status badge (working=indigo, partial=amber, not-working=red, not-started=gray), gap flag (terracotta `#a85a2a` background if `has_gap=true`), story fraction (N/total) with a mini progress bar. Rows sorted: gap features first, then by status (not-working → partial → working → not-started). The lens container uses `hx-get="/lenses/features"` `hx-trigger="every 2s"` for live refresh from the Hono server. Gap analysis logic: a feature has a gap if its `acceptance_condition` is not plausibly met by the assigned stories (same logic as current feature-status skill workflow.md Step 5). Design tokens from Momentum Cycle Final design (dark mode: `--paperDark #16140f` background, `--inkOnDark #f0eee9` text, `--accent #5863a8`, `--gap #a85a2a`).

**Pain context:** Current feature-status skill requires a manual re-run to see updated status. Features lens polls live so the developer always sees current state without re-running.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The Features lens renders a table row for each feature in `features.json`
- Each row displays: feature name, status badge, gap flag indicator, story fraction (N/total), and a mini progress bar
- Status badges use design token colors: working=indigo (`--accent #5863a8`), partial=amber, not-working=red, not-started=gray
- Rows with `has_gap=true` display a terracotta (`--gap #a85a2a`) background
- Row sort order: gap features first, then not-working → partial → working → not-started
- The lens container polls via `hx-get="/lenses/features"` `hx-trigger="every 2s"` against the Hono server endpoint
- Gap analysis uses the same acceptance_condition coverage logic as feature-status skill workflow.md Step 5
- The lens respects dark mode design tokens: `--paperDark #16140f` background, `--inkOnDark #f0eee9` text
- The Hono server exposes a `/lenses/features` route that reads both `features.json` and `stories/index.json` and returns the rendered HTML partial
- The lens renders correctly when `features.json` is missing or empty (graceful empty state)

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
