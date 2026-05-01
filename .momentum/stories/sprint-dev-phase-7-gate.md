---
title: Sprint-Dev Phase 7 Gate — Block Completion Until MANUAL Scenarios Are Developer-Signed-Off
story_key: sprint-dev-phase-7-gate
status: backlog
epic_slug: sprint-dev-workflow
depends_on: []
touches: []
---

# Sprint-Dev Phase 7 Gate — Block Completion Until MANUAL Scenarios Are Developer-Signed-Off

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Phase 7 of sprint-dev to be blocked when MANUAL verification scenarios remain unresolved,
so that no sprint merges to main without explicit developer sign-off on every unvalidated behavior.

## Description

The sprint-dev workflow currently proceeds to Phase 7 (sprint completion, merge to main) even when Phase 6 verification has unresolved MANUAL items from the E2E validator. MANUAL scenarios represent behaviors that cannot be automatically verified — they require a human to physically inspect, click, or make a visual judgment. These cannot be silently deferred; they must be explicitly resolved before the sprint is considered done.

The fix requires Phase 7 to inspect the E2E validation report for unresolved MANUAL items. If any exist, the orchestrator should present them to the developer and require either: (a) explicit sign-off that each MANUAL item was verified and passes, or (b) conversion of each unresolved MANUAL item to a follow-up backlog story before proceeding.

This was identified during sprint-2026-04-08 Team Review where the sprint merged before all E2E validation was complete and unresolved MANUALs were silently skipped.

**Pain context:** Discovered during sprint-2026-04-08 when sprint merged to main with unresolved MANUAL scenarios in the E2E validation report. The current workflow has no gate — Phase 7 proceeds unconditionally after Phase 6 reports any verdict including MANUAL items. This creates a systematic gap where any behavior requiring human verification can silently slip through sprint completion.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Before Phase 7 executes, sprint-dev checks whether the E2E validation report contains any MANUAL items
- If MANUAL items exist, the orchestrator presents each one to the developer with a sign-off prompt
- Developer can respond: "verified, PASS", "verified, FAIL" (creates follow-up story), or "defer" (creates follow-up backlog story)
- Phase 7 proceeds only after all MANUAL items are resolved (signed off or converted to follow-up stories)
- If no MANUAL items exist, Phase 7 proceeds without developer interruption (no change to happy path)
- Follow-up stories created from deferred/failed MANUAL items are added to backlog via momentum:intake

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
