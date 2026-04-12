---
title: Retro Triage Handoff — Retro Findings Feed Sprint Planning Automatically
story_key: retro-triage-handoff
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Retro Triage Handoff — Retro Findings Feed Sprint Planning Automatically

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint planning workflow,
I want to automatically consume the most recent un-actioned retro findings during backlog synthesis,
so that retro-identified gaps and user-stated complaints are surfaced as story candidates before new work is proposed — without the user having to manually inject them.

## Description

The sprint-04-10 planning session started without consuming the sprint-04-08 retro findings. The user had to manually inject the three largest known gaps — Material 3 inconsistency, API stub status, and iOS coverage — before planning could proceed. The retro and sprint-planning skills have no shared state: planning's backlog-synthesis step reads `stories/index.json` and accepts user prompts, but does not read prior retro findings, cross-platform coverage gaps, or recent user-stated complaints.

The sprint-04-06 (D3) retro explicitly surfaced M3 inconsistency as a major user-visible problem. The sprint-04-08 retro ran on 2026-04-10. Sprint-04-10 planning also ran on 2026-04-10 — the same day — and the retro findings were not available to planning.

**Pain context:**
- HF-01 (2026-04-11T05:31): "Was the M3 migration captured in stories?" — user checking whether the prior retro's top finding was in the backlog
- HF-03 (2026-04-11T05:36): "Nooo...don't we need to add M3 stories? Also, what about ios? And last I checked we're STILL not hooked into the API, it's just stubbed" — user had to halt planning to manually inject all three gaps

The handoff is entirely manual today. This means retro findings are reliably lost or delayed between cycles.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- sprint-planning skill includes a "prior retro check" step at the start of backlog-synthesis: read the most recent un-actioned retro findings from `docs/intake/` or sprint retro artifacts
- Before proposing story candidates, planning enumerates: (a) unaddressed prior-retro findings, (b) cross-platform coverage gaps (Android/Desktop/iOS parity), (c) user-stated complaints from recent sessions that have no story
- Retro skill: at sprint closure, write a machine-readable `retro-summary.json` alongside the audit markdown with fields: `priority_action_items[]`, `unaddressed_platform_gaps[]`, `user_stated_complaints[]`
- Planning reads `retro-summary.json` if present; falls back to parsing the audit markdown if not
- Retro findings appear as story candidates in the planning output without manual user injection

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
