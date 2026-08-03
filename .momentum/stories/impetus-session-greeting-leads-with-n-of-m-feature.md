---
title: Impetus session greeting leads with N-of-M feature conditions passing
story_key: impetus-session-greeting-leads-with-n-of-m-feature
status: backlog
epic_slug: momentum-impetus-session-orientation
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Impetus session greeting leads with N-of-M feature conditions passing

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Impetus session greeting to lead with the practice's headline number — N of M feature acceptance conditions passing, read from `.momentum/features.json` — alongside the existing honest ledger counts,
so that story counts no longer mislead about actual delivered capability.

## Description

The session greeting carries the practice's headline number: N of M feature acceptance conditions passing, read from `.momentum/features.json`, alongside the existing honest ledger counts. Story counts no longer lead any report surface. Source: DEC-040 D1 integration seam 3 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`).

**Pain context:** Nornspun discovery: story throughput rose 3→9/sprint while 0 of 15 features ever passed — story counts actively misled; the only number that should greet the developer is verified user capability.

**Proposed dependency:** `momentum-tools-feature-verify-human-verdict-recorder-and` (feature-verify recorder must exist to populate `.momentum/features.json` before this greeting change can read real N-of-M data).

**Source:** triage — decision:DEC-040

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Impetus session-start greeting reads `.momentum/features.json` and computes N (features with passing acceptance conditions) of M (total features).
- The greeting leads with this N-of-M number, alongside existing honest ledger counts (open/this-week/older-than-30-days/near-auto-close).
- Story counts (e.g., stories completed this sprint) no longer lead the greeting or any other report surface — they may still appear as supporting detail, not the headline.
- Behavior degrades gracefully if `.momentum/features.json` does not yet exist or has zero features (e.g., "0 of 0" or an explicit "no features tracked yet" state), without erroring the greeting.

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

- `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (D1 integration seam 3)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
