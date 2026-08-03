---
title: Conduct resume card + Impetus pending-gate agenda — session-start re-surfacing, never expiry-FAIL
story_key: conduct-resume-card-impetus-pending-gate-agenda-session
status: backlog
epic_slug: momentum-conductor-core
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Conduct resume card + Impetus pending-gate agenda — session-start re-surfacing, never expiry-FAIL

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Conductor to emit a compact resume card when a build finishes and Impetus to lead the next session with the pending gate as the agenda — re-surfacing with rising prominence until decided, never expiring to a FAIL state,
so that a nights-and-weekends practice never leaves me facing a wall of text or a decision that silently expired while I was away.

## Description

When a conduct build finishes, the Conductor emits a resume card: where we were, what
merged, the ONE question pending — never a wall of text (wall-of-text gate surfaces
are a defect under the Decision-Grade Presentation Standard). Impetus leads the next
session start, whenever it happens, with the pending gate as the agenda, re-surfacing
with rising prominence until decided. No expiry-FAIL — the practice serves a
nights-and-weekends developer; escalation is re-surfacing, not failure.

Design note: define the resume-card schema as an explicit seam contract between
Conductor (emitter) and Impetus (consumer) so the two skills cannot drift
independently (see inter-skill-seam-contracts).

**Pain context:** Steve, verbatim: "Sadly this is not an 8 hour/day job for me. It's
nights and weekends… when I finally get back I need to be reminded where we were… We
must do better than massive walls of text that lead to complete demoralization and
procrastination." The sprint-2026-07-13 gate hung undecided 11 days.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Conductor emits a resume card at end of build (or on pause/interrupt) capturing:
  where we were, what merged, and the single pending question/decision — not a full
  transcript or wall of text.
- Impetus, at the start of the next session (regardless of elapsed time), surfaces the
  pending resume card as the session's leading agenda item before anything else.
- Repeated sessions with the same pending gate re-surface it with increasing
  prominence (escalation via re-surfacing), not via a hard expiry/FAIL state.
- No mechanism exists that marks a pending gate as failed/expired purely due to
  elapsed time.
- The resume-card schema is defined as an explicit seam contract between Conductor
  (emitter) and Impetus (consumer) — see inter-skill-seam-contracts convention — so the
  two skills' expectations of the card's shape cannot silently drift apart.
- The resume card presentation complies with the Decision-Grade Presentation Standard
  (tight on the irrelevant, complete on the decision-relevant; no wall-of-text gate).

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

- Source decision: DEC-040 D5 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (amending DEC-036)
- Triage source: `decision:DEC-040`

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

