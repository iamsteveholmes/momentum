---
title: Sprint Scope Tracking — Planned vs Unplanned Work Log
story_key: sprint-scope-tracking
status: backlog
epic_slug: sprint-dev-workflow
depends_on: []
touches: []
---

# Sprint Scope Tracking — Planned vs Unplanned Work Log

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint lead,
I want a lightweight scope log maintained in real time distinguishing planned vs unplanned work,
so that retros can report an accurate scope expansion ratio and unplanned items that recur across sprints become upstream candidates automatically.

## Description

Momentum has no mechanism for the lead to track planned vs unplanned work within a sprint. When scope expands legitimately (mid-sprint gap discovery), there's no record of what was planned vs discovered. This makes retros less precise and velocity measurements misleading.

Sprint-dev skill should maintain a lightweight scope log:
- PLANNED: list of sprint stories at sprint start
- UNPLANNED (discovered): item | reason | outcome

At sprint close, the scope log feeds into the retro automatically. The retro skill should report a **scope expansion ratio**: planned turns / total turns. A ratio below 50% flags a systematic practice gap — sprints should start with adequate guidelines rather than discovering their absence mid-execution. Unplanned items that recur across sprints become upstream candidates.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 10, Low). The D3 sprint was nominally a code sprint (D4 stories) but actual activity breakdown: D4 implementation was ~40% of activity. The rest was unplanned: E2E guidelines, emulator setup, cmux rules, BMad builder upgrade, UX discovery, next-sprint planning — none of which appeared in the original story list. No mechanism existed to distinguish planned from discovered work.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Sprint-dev skill maintains a scope log with PLANNED and UNPLANNED sections
- Scope log is updated in real time as unplanned work is discovered and undertaken
- Retro skill reads scope log and reports scope expansion ratio (planned turns / total turns)
- Ratio below 50% triggers a systemic practice gap flag in the retro output
- Unplanned items that appear in multiple sprints are surfaced as upstream candidates

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
