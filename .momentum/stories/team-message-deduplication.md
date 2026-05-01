---
title: Team Message Noise Reduction — Idle Notification Dedup and Log Write Dedup
story_key: team-message-deduplication
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Team Message Noise Reduction — Idle Notification Dedup and Log Write Dedup

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint orchestrator and retro analyst,
I want team message noise reduced at both the runtime layer (idle notification deduplication) and the log layer (write deduplication),
so that substantive team communication isn't buried in idle pings during sprints, and retro signal isn't skewed by logging artifacts after.

## Description

Two layers of team message noise, both requiring fixes:

**Layer 1 — Runtime idle spam (High, D3):** During active sprints, 40–50%+ of all team messages are idle notifications — often 3–5 in rapid succession from the same agent within seconds. Substantive messages (bug reports, fix confirmations, validation results) are buried. The idle notification system fires on a timer with no deduplication or backoff. Fix: one notification per agent per idle period; backoff if agent has been idle >60 seconds without new output; visual distinction between idle pings and substantive messages.

**Layer 2 — Log write artifact (Low, original):** Team messages in sprint JSONL logs have a 3:1 duplication ratio — each message is logged 3 times with identical content. This inflates message counts in retro analysis and makes communication pattern metrics misleading. Fix: deduplication at write time or during extraction.

**Pain context (Layer 1):** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 4, High). 451 team messages across the sprint; estimated 40–50%+ were idle notifications rather than substantive communication. Messages 60–70 show 10+ idle notifications in rapid succession. The same pattern recurred in the retro session itself. **Pain context (Layer 2):** Sprint-2026-04-08 retro. 3:1 ratio in JSONL logs discovered during retro analysis — 67% of logged volume was noise.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Team message logging writes each message once (not 3x)
- OR: retro extraction deduplicates by message content + timestamp within 1-second window
- Team message count in retro report reflects actual messages
- Deduplication doesn't lose legitimately distinct messages with same content at different times

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
