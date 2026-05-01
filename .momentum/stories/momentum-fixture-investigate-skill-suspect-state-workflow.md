---
title: momentum:fixture-investigate skill — Suspect state workflow
story_key: momentum-fixture-investigate-skill-suspect-state-workflow
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quality-gates-enforced
story_type: feature
depends_on: []
touches: []
---

# momentum:fixture-investigate skill — Suspect state workflow

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a `momentum:fixture-investigate` skill that walks the structured five-cause investigation for a Suspect-state fixture,
so that I can deterministically re-classify suspect fixtures as Active, Protected, or Retired with documented reasoning rather than ad-hoc guessing.

## Description

Build the momentum:fixture-investigate skill that takes a Suspect-state fixture (one that should fail per its observed rate but passes on replay) and walks the structured five-cause investigation: (1) re-run with higher sample count (30), (2) diff the skill since fixture creation, (3) diff the model (run against model-at-time-of-failure), (4) enrich context reconstruction and re-verify, (5) retire as false positive only after 1-4 return negative. Outcome: re-classify the fixture as Active, Protected, or Retired with documented reasoning. Per DEC-010 D4, this skill ships AFTER momentum:micro-eval has been in operation for several sprints and the Suspect state has become observable in real fixture runs — so this is intentionally a deferred story. Decision source: dec-010-fixture-based-regression-testing-2026-04-22.md (D3 + D4). Analysis source: _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md §6. Decision Gate 3 in DEC-010 is the explicit trigger to move this from low-priority deferred to ready-for-dev: "at least 2 distinct Suspect-state cases observed in the running suite".

**Pain context:** Without a structured investigation skill, Suspect-state fixtures (those that should fail per observed rate but pass on replay) get triaged ad-hoc — risking either premature retirement of valid signals or indefinite carrying of broken fixtures. The five-cause walk encodes the diagnostic discipline so re-classification is reproducible and auditable. Deferral is intentional: skill is only useful once micro-eval has produced enough Suspect cases to validate the workflow against real data (DEC-010 Decision Gate 3: ≥2 distinct Suspect-state cases observed).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- New skill `momentum:fixture-investigate` exists and is invokable on a Suspect-state fixture
- Skill walks the five-cause investigation in order:
  1. Re-run fixture with higher sample count (30)
  2. Diff the skill since fixture creation
  3. Diff the model (run against model-at-time-of-failure)
  4. Enrich context reconstruction and re-verify
  5. Retire as false positive only after steps 1–4 return negative
- Outcome of investigation re-classifies the fixture as Active, Protected, or Retired
- Re-classification is written back to fixture metadata with documented reasoning trail
- Skill respects DEC-010 D4 sequencing — depends on momentum:micro-eval and the Suspect state being observable
- Decision Gate 3 trigger is documented: ship when ≥2 distinct Suspect-state cases observed in the running suite
- References to source decisions and analysis are linked from the skill's prompt/docs

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

- Decision source: `_bmad-output/decisions/dec-010-fixture-based-regression-testing-2026-04-22.md` (D3 + D4)
- Analysis source: `_bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md` §6

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
