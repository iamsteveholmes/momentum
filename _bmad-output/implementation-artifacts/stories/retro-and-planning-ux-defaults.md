---
title: Retro and Planning UX Defaults — Apply Established Workflow Patterns Without Asking
story_key: retro-and-planning-ux-defaults
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Retro and Planning UX Defaults — Apply Established Workflow Patterns Without Asking

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer running retros and sprint planning,
I want retro and planning skills to apply my established workflow patterns by default rather than asking for explicit instruction each time,
so that recurring preferences (batch retros, auto-open review artifacts, cross-retro dedup) are applied automatically every session.

## Description

Three separate skill interactions required the user to explicitly request behavior that should be the default given their established workflow:

1. **Batch retro**: When multiple sprints have `retro_run_at == null`, the retro skill presented an either/or choice instead of batching both. The user had to say "Can we do both?"
2. **Auto-open review artifacts**: After sprint-planning generated story files, the user had to explicitly request they be opened in cmux markdown panes for review. This is always wanted.
3. **Cross-retro dedup**: Findings deduplication against prior intake docs was not automatic — the user had to request it with "Make sure we dedup against the current one."

These are not one-off requests. They are the user's consistent expectations in every retro and planning session.

**Pain context:** 
- HF-18 (2026-04-10T07:21): "Can we do both?" — retro presented either/or when user wanted both sprints retro'd
- HF-14 (2026-04-11T05:43): "Please fire them up in CMUX pane/surface on the right so I can review them" — cmux review mode not offered by default
- HF-16 (2026-04-11T04:18): "Oof...sure. Make sure we dedup against the current one." — dedup across retros not automatic

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- momentum:retro: When multiple sprints have `retro_run_at == null`, batch-retro all of them by default rather than asking which one to retro
- momentum:retro: Automatically dedup findings against prior intake docs in `docs/intake/` before producing output — no user prompt needed
- momentum:sprint-planning: After generating story files, auto-open them in cmux markdown panes for review without requiring the user to ask
- Both skills check for established usage patterns (prior cmux usage, prior retro batch behavior) and apply them

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
