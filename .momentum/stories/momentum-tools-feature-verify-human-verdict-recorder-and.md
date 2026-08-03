---
title: momentum-tools feature verify — human verdict recorder and sole writer of features.json
story_key: momentum-tools-feature-verify-human-verdict-recorder-and
status: backlog
epic_slug: momentum-feature-taxonomy-maintenance
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# momentum-tools feature verify — human verdict recorder and sole writer of features.json

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a new `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>` CLI subcommand that records a HUMAN PASS/FAIL verdict against a feature's acceptance_condition in `.momentum/features.json`,
so that feature completion becomes a real, verified field in the practice's state instead of an orphaned file nobody writes to — closing the gap where 0 of 15 features ever reached done across 10 sprints while story throughput rose.

## Description

New CLI subcommand `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>`. Records a HUMAN PASS/FAIL verdict against a feature's acceptance_condition in `.momentum/features.json`, stamping `last_verified {date, build SHAs, verdict}`. Failing-by-default status model: `absent | failing | passing`. This command is the SOLE write path to `.momentum/features.json` — no agent, skill, or workflow may write feature status any other way (registry is per-project; features are acceptance-testing entities, deliberately separate from work-tracking epics).

Source: DEC-040 D1 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`), which amends DEC-034.

Downstream consumers (read-only — not implemented by this story): sprint-planning `goal_conditions` declaration, sprint closure refusal, Impetus N-passing report, daily tasting brief.

**Pain context:** Nornspun delivery discovery (`docs/research/nornspun-delivery-discovery-2026-08-02/`): 0 of 15 features ever reached done across 10 sprints while story throughput rose — feature completion was not a field that existed anywhere in sprint state, and `features.json` was orphaned with zero workflow references.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- New CLI subcommand `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>` exists and is invocable.
- Command records a HUMAN PASS/FAIL verdict against the target feature's `acceptance_condition` in `.momentum/features.json`.
- Command stamps `last_verified` with `{date, build SHAs, verdict}` on the target feature entry.
- Status model is failing-by-default: `absent | failing | passing` — a feature with no recorded verdict is never silently treated as passing.
- This command is the SOLE write path to `.momentum/features.json` — no agent, skill, or workflow may write feature status any other way.
- `.momentum/features.json` remains per-project; features stay a distinct acceptance-testing entity, deliberately separate from work-tracking epics (per DEC-040 D1 amending DEC-034).
- Downstream read-only consumers (sprint-planning `goal_conditions`, sprint closure refusal, Impetus N-passing report, daily tasting brief) are out of scope for this story but must be able to read the shape this command writes.

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

- DEC-040 D1 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (amends DEC-034)
- `docs/research/nornspun-delivery-discovery-2026-08-02/` — pain-context research

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
