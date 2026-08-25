---
title: Make write_json atomic and lock-safe
story_key: make-write-json-atomic-and-lock-safe
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Make write_json atomic and lock-safe

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the house-wide write_json helper in momentum-tools.py to write atomically,
so that a crash or concurrent invocation mid-write can never leave a JSON state file (stories/index.json, sprints/index.json, etc.) truncated or corrupted.

## Description

The write_json helper used across momentum-tools.py is neither locked nor atomic — it writes directly to the target path. This is a CLI-hardening story: switch to temp-file + os.replace for atomicity, and add advisory locking if concurrent writers become a real scenario (multiple agents/subagents calling CLI mutators at once).

**Pain context:** Surfaced by code-review triage during sprint-2026-08-03 build wave (feature-verify story), triaged out as a house-wide CLI-hardening concern beyond this story's scope.

**Source:** triage — Conductor build wave sprint-2026-08-03 (feature-verify)

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- [ ] write_json writes to a temp file in the same directory then os.replace()s into place
- [ ] Existing callers unaffected (same function signature)
- [ ] Advisory locking added if concurrency risk is confirmed real (else documented as out of scope for now)
- [ ] Regression test: simulate interrupted write, confirm original file untouched

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
