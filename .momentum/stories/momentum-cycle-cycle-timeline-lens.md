---
title: Momentum Cycle — Cycle Timeline Lens
story_key: momentum-cycle-cycle-timeline-lens
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-dashboard-shell]
touches: []
---

# Momentum Cycle — Cycle Timeline Lens

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a horizontal timeline showing the current cycle's phase progression with clear node states,
so that I can instantly see which phases ran, what's next required, and where I am in the cycle without digging through files.

## Description

Implement the Cycle Timeline section of the Momentum Cycle dashboard. Shows a horizontal 7-node timeline representing the current cycle's phase progression.

Phases in canonical order: triage → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro. (Note: intake is a sub-step of triage, not a separate node.)

Node states:
- **done** — filled indigo dot, dark label
- **next-required** — indigo ring + 3px glow box-shadow, accent-colored label; travels through planning→dev→retro as each completes
- **not-run** — gray dot, faint label (optional phases that were skipped)
- **pending** — gray dot, faint label (not yet reached)

Required phases: sprint-planning, sprint-dev, retro. Optional: triage, feature-grooming, epic-grooming, refine.

The "next required" outline moves forward only when required phases complete — optional phases have no outline state.

Below the timeline: "cycle started · next required: {phase} · last sprint: {slug}".

Reads sprint state from `.momentum/sprints/` directory.

Design reference: `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` (cycle-nodes CSS section, `.cycle-node` states). Design was prototyped in a 10-pass claude.ai/design session and approved.

**Pain context:** Developers have no at-a-glance view of where they are in the current cycle. The timeline makes "what did we run, what's next required" instantly visible.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- 7-node horizontal timeline renders in the Momentum Cycle dashboard for the current cycle
- Nodes appear in canonical order: triage → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro
- done state: filled indigo dot, dark label
- next-required state: indigo ring + 3px glow box-shadow, accent-colored label
- not-run state (optional phases skipped): gray dot, faint label
- pending state (not yet reached): gray dot, faint label
- The "next required" outline applies only to required phases (sprint-planning, sprint-dev, retro); optional phases never show the outline state
- The outline advances to the next required phase as each required phase completes
- Status line below timeline shows: "cycle started · next required: {phase} · last sprint: {slug}"
- Phase state is derived by reading `.momentum/sprints/` directory
- Matches approved design reference: cycle-nodes CSS section and `.cycle-node` states from Final.html

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
