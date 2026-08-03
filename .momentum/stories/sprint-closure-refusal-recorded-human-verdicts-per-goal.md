---
title: Sprint closure refusal — recorded human verdicts per goal_conditions, honest FAILED terminal state
story_key: sprint-closure-refusal-recorded-human-verdicts-per-goal
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Sprint closure refusal — recorded human verdicts per goal_conditions, honest FAILED terminal state

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want `momentum-tools sprint complete` to refuse closing a sprint unless every entry in the sprint record's goal_conditions carries a recorded human PASS/FAIL verdict, and for an honest FAILED terminal sprint state to exist alongside `done`,
so that sprints can never close on an unverified outcome, goal-critical work can't be silently punted without an explicit recorded decision, and maintenance sprints get an equivalent verified-fix confirmation gate.

## Description

`momentum-tools sprint complete` refuses to close a sprint unless every entry in the sprint record's goal_conditions carries a recorded human PASS/FAIL verdict (written via momentum-tools feature verify with paired-build SHAs). Adds FAILED as an honest terminal sprint state distinct from done — a sprint that cannot reach PASS in reasonable time closes FAILED, recorded, not silently reopened or punted. Punting goal-critical work to a future sprint requires an explicit recorded decision, never a default. Maintenance sprints (empty goal_conditions) instead require each named fix in the goal's verified-fix list confirmed in the running app. Source: DEC-040 D3 (_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md), completing DEC-039.

**Pain context:** Nornspun discovery: the punt was institutionalized — the end-gate's own recommendation for a broken keystone capability (2-of-7 reliability) was approve-and-defer; the recommended hardening story was never created; no sprint ever closed on an outcome question.

**Proposed dependency:** `momentum-tools-feature-verify-human-verdict-recorder-and` (the human-verdict recorder this story's gate is built on) — not yet validated against the actual story index; confirm during create-story.

**Source:** triage — decision:DEC-040

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- `momentum-tools sprint complete` refuses to close a sprint unless every entry in the sprint record's goal_conditions has a recorded human PASS/FAIL verdict, written via `momentum-tools feature verify` with paired-build SHAs.
- A new FAILED terminal sprint state exists, distinct from `done` — a sprint that cannot reach PASS within a reasonable time closes FAILED and is recorded, not silently reopened or punted forward.
- Punting goal-critical work to a future sprint requires an explicit recorded decision (not a default action) — the end-gate cannot approve-and-defer a broken keystone capability without a corresponding decision record.
- Maintenance sprints (empty goal_conditions) require each named fix in the goal's verified-fix list to be confirmed in the running app before the sprint can close.

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

DEC-040 D3, `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` — completes DEC-039.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
