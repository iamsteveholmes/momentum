---
title: sprint-planning goal_conditions declaration + plan-gate leads with the capability fork
story_key: sprint-planning-goal-conditions-declaration-plan-gate-leads
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# sprint-planning goal_conditions declaration + plan-gate leads with the capability fork

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint planning to declare `goal_conditions` on the sprint record and have the plan gate's first fork be a plain-language capability sign-off,
so that a plan gate review can never again pass without anyone saying out loud what capability (if any) will actually change for the GM this sprint.

## Description

Sprint planning declares `goal_conditions` on the sprint record — 0..n feature slugs
(from `.momentum/features.json`) whose acceptance conditions this sprint intends to
flip from failing to passing; maintenance sprints declare a verified-fix list in the
`goal` field instead. The plan gate's FIRST fork becomes a plain-language capability
sign-off: "After this sprint a GM will be able to ___ — approve / change / reject."

Cross-check during implementation: `plan-gate-renderer-fork-id` (ForkItem shape has no
`id` field) and `sprint-planning-pre-sprint-class-1-render-gate` touch the same renderer
surface — avoid ForkItem shape conflicts between the two efforts.

Source: DEC-040 D3
(`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`);
`architecture.md` Sprint Tracking Schema already documents the `goal_conditions` field
(implementation should verify alignment with that existing schema, not re-derive it).

**Pain context:** Nornspun discovery: sprint-2026-07-13's plan gate asked only
copy/scope questions; nobody said "nothing you can see will change for two sprints"
out loud. The developer relies on the sprint goal as the ultimate requirement, and the
gate never asked it.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Sprint record schema gains a `goal_conditions` field: 0..n feature slugs (from
  `.momentum/features.json`) whose acceptance conditions this sprint intends to flip
  from failing to passing.
- Maintenance sprints declare a verified-fix list in the `goal` field instead of
  `goal_conditions`.
- The plan gate's FIRST fork is a plain-language capability sign-off: "After this
  sprint a GM will be able to ___ — approve / change / reject."
- Implementation cross-checks `plan-gate-renderer-fork-id` (ForkItem shape has no `id`
  field) and `sprint-planning-pre-sprint-class-1-render-gate` — both touch the same
  renderer surface; resolve or avoid ForkItem shape conflicts between them.
- Verify alignment with `architecture.md` Sprint Tracking Schema, which already
  documents the `goal_conditions` field, rather than re-deriving the schema from
  scratch.

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
