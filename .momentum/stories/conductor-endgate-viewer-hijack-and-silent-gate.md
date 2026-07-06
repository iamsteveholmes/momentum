---
title: Conductor end-gate — stop viewer pane hijack and silent gate turn-end
story_key: conductor-endgate-viewer-hijack-and-silent-gate
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
depends_on: []
touches: []
---

# Conductor end-gate — stop viewer pane hijack and silent gate turn-end

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the conductor to open gate reports without stealing focus or churning cmux panes, and to always present the end-gate approval ask after rendering,
so that my session view is never hijacked and a sprint never parks silently at an unpresented HITL gate.

## Description

Observed in the sprint-2026-06-28 conduct run (2026-07-06). Three compounding defects made the developer's session appear to "disappear," replaced by the End-Gate document, and left the sprint parked at an unanswered gate:

1. **Focus-steal against spec:** the end-gate open executed `cmux browser new … --focus true`, violating the skill's own instructions at `skills/momentum/skills/conductor/workflow.md:2337` and `:2610`, which both mandate `--focus false` ("keeps the developer in context").
2. **Stale placement assumption:** `workflow.md:2336` and `references/endgate-report-renderer.md` assume `cmux browser new` adds a tab to an existing viewer pane (`placement=reuse`). Verified false by live test 2026-07-06: it ALWAYS returns `placement=split` and creates a new structural pane — even when a browser viewer pane exists and is focused. Every gate open churns the layout. Fix: when a viewer browser surface already exists and its content is superseded (e.g. plan gate → end gate), navigate it in place with `cmux browser <surface> goto <url>`; use `browser new --focus false` only when no viewer surface exists.
3. **Silent gate:** the conductor ended its turn immediately after opening the report, WITHOUT presenting the `workflow.md:2341` end-gate ask ("approve to merge to main, or request changes"). The session transcript (83ea46d8) ends at 18:01:49Z with a turn_duration event and no ask — the developer's terminal showed nothing, and the sprint sat un-merged until manually rediscovered in a later session.

Fix all three in `skills/momentum/skills/conductor/workflow.md` and `references/endgate-report-renderer.md`; make the end-gate ask un-skippable (the turn must not end between report render and the ask).

**Pain context:** First occurrence, but on the highest-stakes surface in the practice — the single mandatory human gate of a sprint build. The developer lost their session view mid-review, believed the session had been destroyed, and the merge-to-main approval was delayed a full session cycle. Recurrence risk is every future conduct run until fixed.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Gate/report opens never use `--focus true`; the workflow states this as a hard MUST, not a parenthetical.
- When a viewer browser surface already exists in the workspace and its content is superseded, the conductor reuses it via `cmux browser <surface> goto <url>` instead of `cmux browser new` (which always splits a new pane — verified behavior, not placement=reuse as previously documented).
- `cmux browser new --focus false` is used only when no viewer browser surface exists (first viewer open of the session).
- The stale "does not create a new structural pane / placement=reuse" language is corrected in both workflow.md and endgate-report-renderer.md.
- After rendering and opening the end-gate report, the conductor MUST present the end-gate ask in the same turn — the turn may not end between render and ask.

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
