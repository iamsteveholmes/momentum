---
title: Conduct merge-gate completes by executing — merge + push + story transitions, never a report
story_key: conduct-merge-gate-completes-by-executing-merge-push-story
status: backlog
epic_slug: momentum-conductor-core
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Conduct merge-gate completes by executing — merge + push + story transitions, never a report

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the tier-1 merge gate in conductor/workflow.md ("is this code something we are
comfortable keeping on trunk?") to complete only by executing the real state transition
— merge to main, push, and story status updates — and to FAIL loudly if it cannot execute
that transition,
so that an approval always has real, executed consequence instead of leaving finished
work stranded on a sprint branch behind a rendered report.

## Description

The tier-1 merge gate in conductor/workflow.md ("is this code something we are
comfortable keeping on trunk?") completes ONLY by executing the state transition: merge
to main + push + story status updates. If it cannot execute, it FAILS loudly. The gate's
terminal state is never a rendered report. Distinct from sprint closure (tier 2, separate
decision per DEC-040 D2 two-tier gate).

Implementation cross-check: consolidate-state-model-and-cross-skill-contract-tests (same
epic) should include a contract test asserting the merge gate cannot terminate in a
non-executed state.

**Pain context:** Nornspun discovery: 53 finished commits sat stranded on sprint branches
for 11 days because the end-gate emitted HTML and nothing executed; an approval that
leaves commits stranded is an opinion, not an approval.

**Source:** DEC-040 D2 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`),
amending DEC-035; architecture.md Decision 59 two-tier-gate paragraph documents the
semantics.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- The tier-1 merge gate's terminal state is always an executed state transition: merge to
  main + push + story status updates — never a rendered report/HTML artifact standing in
  for execution.
- If the merge/push/status-transition cannot execute (conflicts, permissions, CI
  failure, etc.), the gate FAILS loudly — it does not silently degrade to "approved" or
  emit a report as if the transition happened.
- The tier-1 merge gate is explicitly distinct from tier-2 sprint closure — sprint
  closure remains a separate decision point per DEC-040 D2's two-tier gate model; this
  story does not change sprint-closure semantics.
- A contract test exists (likely in the sibling story
  consolidate-state-model-and-cross-skill-contract-tests, same epic) asserting the merge
  gate cannot terminate in a non-executed state.

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

- DEC-040 D2 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`
  (amends DEC-035)
- `architecture.md` Decision 59 — two-tier-gate paragraph documents the semantics
- `skills/momentum/skills/conductor/workflow.md` — tier-1 merge gate location
- Sibling story: consolidate-state-model-and-cross-skill-contract-tests (same epic)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
