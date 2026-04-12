---
title: Retro Team Singleton Guard — Enforce Exactly-One Spawning for Documenter and Auditor Roles
story_key: retro-team-singleton-guard
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Retro Team Singleton Guard — Enforce Exactly-One Spawning for Documenter and Auditor Roles

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a retro workflow,
I want a singleton guard that prevents spawning duplicate roles during team-assemble,
so that each retro runs with exactly the intended team (1 documenter + 3 auditors) and doesn't burn tokens on idle duplicate agents.

## Description

The retro skill's team-assemble step spawns duplicate singleton roles in every run, and the problem is escalating. In the sprint-04-08 retro (2026-04-10): 5× documenter spawned, 2× auditor-review — 6 surplus agents for an intended 4-agent team. In the sprint-04-10 retro (2026-04-12): 10× documenter, 3× auditor-review, 2× auditor-human, 2× auditor-execution — 17 total agents for an intended team of 4. Only 1 documenter and 3 auditors were productive; all others consumed tokens waiting for messages that never arrived.

This was flagged as RV-05 in the sprint-04-08 retro and went unactioned. The multiplier grew from 5× to 10× duplicate documenters in a single retro interval.

**Pain context:** Burning tokens in every retro run. Escalating: 5× documenters (sprint-04-08 retro) → 10× documenters (sprint-04-10 retro). Was flagged in the prior retro as RV-05 and not actioned — each retro now costs ~9 wasted documenter agents. The root cause appears to be a state-accumulation or loop-count bug, not a fixed off-by-one, since the multiplier is growing.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Before team-assemble spawns agents, assert target counts: exactly 1 documenter, exactly 3 auditors (auditor-review, auditor-human, auditor-execution)
- If actual spawn count would exceed the target for any role, halt and report the count before proceeding
- A validation step confirms the assembled team is correctly sized before Phase 3 (extraction) begins
- Zero surplus agents spawned in any retro run — no idle documenters, no duplicate auditors
- Root cause of the state-accumulation or loop-count bug identified and fixed

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
