---
title: Momentum Cycle — Sprint Lens + Sprint Detail Drill-Down
story_key: momentum-cycle-sprint-lens-sprint-detail-drill-down
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: []
touches: []
---

# Momentum Cycle — Sprint Lens + Sprint Detail Drill-Down

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to see an active sprint summary card on the Momentum Cycle dashboard and drill into sprint story status with outcome-band grouping,
so that I can gauge sprint health at a glance without reading raw sprint files.

## Description

Implement the Sprint section of the Momentum Cycle dashboard AND the sprint detail view.

**Dashboard sprint section (dark mode):** Shows an active sprint card containing the sprint slug, start date, and a closure strip indicating retro/triage completion state.

**Sprint detail view (dark mode):** Reached by clicking the sprint card. Displays three outcome bands — Blocked (red left border), In Progress (amber), and Validated (green). Stories from `.momentum/stories/index.json` for the active sprint are sorted into bands by status. Each story row shows title + status; clicking a story row navigates to Story L3 via `hx-push-url="/stories/{slug}"`.

**Navigation:** HTMX partial swap with `hx-push-url="/sprints/{slug}"`. Breadcrumb OOB swap (`hx-swap-oob="true"`) adds a "Sprint" segment in blue and grays out "Dashboard". Back navigation: clicking "Dashboard" in the breadcrumb returns to the dashboard root. Polarity: sprint detail stays dark (same as dashboard) — no polarity flip.

**Source:** triage — conversation (design review session, 10-pass claude.ai/design prototype approved)

**Pain context:** No way to see sprint story status at a glance without reading raw sprint files. Sprint detail with outcome bands gives instant sense of sprint health.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Dashboard renders an active sprint card showing sprint slug, start date, and closure strip (retro/triage completion state)
- Clicking the sprint card performs an HTMX partial swap and navigates to the sprint detail view (`hx-push-url="/sprints/{slug}"`)
- Sprint detail view displays three outcome bands: Blocked (red left border), In Progress (amber), Validated (green)
- Stories for the active sprint are loaded from `.momentum/stories/index.json` and sorted into the correct band by status
- Each story row in the detail view shows title and status
- Clicking a story row navigates to Story L3 (`hx-push-url="/stories/{slug}"`)
- Breadcrumb OOB swap (`hx-swap-oob="true"`) adds a "Sprint" segment (blue) and grays out the "Dashboard" segment on drill-down
- Clicking "Dashboard" in the breadcrumb returns to the dashboard root
- Sprint detail view uses dark mode (no polarity flip from dashboard)
- All views are functional in dark mode consistent with the dashboard shell

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
