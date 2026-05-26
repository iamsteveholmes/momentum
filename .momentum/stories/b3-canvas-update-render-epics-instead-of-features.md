---
title: "B3: Canvas update — render epics instead of features"
story_key: b3-canvas-update-render-epics-instead-of-features
status: backlog
epic_slug: ad-hoc
feature_slug: 
story_type: feature
depends_on: ["B1"]
touches: []
---

# B3: Canvas update — render epics instead of features

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the canvas server to render epics instead of features,
so that the canvas UI reflects the current epic-layer model after the features→epics consolidation.

## Description

Update `skills/momentum/skills/canvas/server.tsx` (TypeScript) to render epics. Per AES-003 Finding 9, this is a "hidden blocker" the original plan missed. Replace `readFeaturesJson()` + `readFeatureBySlug()` with `readEpicsJson()` + `readEpicBySlug()`. Update the `/lenses/features` route to `/lenses/epics`. Update the L2 detail view to render epic shape (lifecycle, audience, etc.). Sprint lens and cycle timeline lens unaffected. Practice-rendering path may need rework — verify against DEC-048 (practice project detection). Effort: 4–6 hours. Change types: script-code (TypeScript), skill-instruction (canvas SKILL.md + workflow.md). Verification: smoke test (run canvas server, visit /lenses/epics, confirm rendering) + manual review for visual correctness.

**Pain context:** Hidden blocker original plan missed per AES-003 Finding 9. User-visible canvas behavior. Depends on B1's epics.json.

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

**Proposed depends_on:** ["B1"]

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `readFeaturesJson()` and `readFeatureBySlug()` replaced by `readEpicsJson()` and `readEpicBySlug()` in `skills/momentum/skills/canvas/server.tsx`
- `/lenses/features` route renamed to `/lenses/epics`
- L2 detail view renders epic shape (lifecycle, audience, etc.)
- Sprint lens and cycle timeline lens remain functional and unchanged
- Practice-rendering path verified against DEC-048 (practice project detection); reworked if needed
- Canvas SKILL.md and workflow.md updated to reflect epic rendering
- Smoke test passes: canvas server runs, `/lenses/epics` renders correctly
- Manual visual review confirms correctness

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
