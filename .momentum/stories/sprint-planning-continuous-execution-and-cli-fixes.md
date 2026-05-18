---
title: "sprint-planning: fix continuous execution breaks and stale CLI namespace bugs"
story_key: sprint-planning-continuous-execution-and-cli-fixes
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-sprint-planning-to-ready
story_type: defect
depends_on: []
touches: []
---

# sprint-planning: fix continuous execution breaks and stale CLI namespace bugs

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want fix sprint-planning to run without inter-step confirmation halts and with correct CLI subcommands and skill namespaces,
so that sprint planning runs end-to-end without requiring manual re-invocation mid-workflow, and CLI calls succeed on first try.

## Description

Two concurrent defects in the sprint-planning workflow found in sprint-2026-05-16: (1) inter-step confirmation gates break continuous execution — the orchestrator halts for confirmations between steps, and a /model switch mid-workflow resets execution state; (2) stale CLI subcommands and wrong skill namespaces — sprint-current and sprint-stories CLI refs are stale, and bare skill names (avfl, create-story) are used instead of the momentum: prefix (momentum:avfl, momentum:create-story). Both defects degrade the quality of sprint planning sessions. Source: sprint-2026-05-16 retro handoff iq-20260518043634.

**Pain context:** Sprint planning broke twice in sprint-2026-05-16 — once from confirmation gate halts, once from stale CLI refs. Developer had to manually re-invoke multiple times. Blocks reliable sprint execution.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- (1) sprint-planning workflow runs continuously from invocation to activated sprint without inter-step confirmation gates
- (2) /model switch mid-workflow does not reset execution state
- (3) CLI calls use current sprint subcommands (not stale refs)
- (4) skill invocations use momentum: namespace prefix (momentum:avfl, momentum:create-story)
- (5) full sprint planning workflow produces an activated sprint in a single continuous run on a standard session

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
