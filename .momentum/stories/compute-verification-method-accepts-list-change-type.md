---
title: compute-verification-method accepts list-valued change_type — stop crashing on multi-type stories
story_key: compute-verification-method-accepts-list-change-type
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: defect
depends_on: []
touches: []
---

# compute-verification-method accepts list-valued change_type — stop crashing on multi-type stories

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer running sprint planning,
I want `momentum-tools sprint compute-verification-method` to accept `change_type` in both its string form ("skill-instruction + agent-definition") and its list form (the YAML/JSON array stories/index.json actually stores for multi-type stories),
so that Step 3.5 contract authoring computes verification methods from the tool instead of crashing and forcing the planner to route manually.

## Description

`compute_verification_method()` at `skills/momentum/scripts/momentum-tools.py:514` calls
`re.split(r"\s*\+\s*|,\s*", change_type_raw)` assuming a string, but `stories/index.json`
stores `change_type` as a list for multi-type stories. The call dies with
`TypeError: expected string or bytes-like object, got 'list'`.

**Pain context:** Crashed on 4 of 5 conductor seam-fix stories during sprint-2026-06-10
planning Step 3.5 (contract authoring). The planner had to bypass the tool and route
manually via the verification-standard.md §1 table. Every future multi-change-type story
hits this until fixed — multi-type stories are common (any story touching both a skill
workflow and an agent definition).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `compute-verification-method` accepts `change_type` as a string ("skill-instruction", "skill-instruction + agent-definition", comma-separated) AND as a JSON/YAML list, producing identical routing for equivalent inputs
- A multi-type story (e.g., [skill-instruction, agent-definition, specification]) resolves per the verification-standard.md §1 table and the established multi-type precedence — no TypeError
- The five conductor seam-fix stories' index entries all compute successfully

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
