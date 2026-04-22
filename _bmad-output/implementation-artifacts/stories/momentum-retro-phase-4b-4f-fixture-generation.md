---
title: momentum:retro Phase 4b-4f extension — fixture generation from findings
story_key: momentum-retro-phase-4b-4f-fixture-generation
status: backlog
epic_slug: epic-6-the-practice-compounds
feature_slug: momentum-retro-and-flywheel
story_type: feature
depends_on: []
touches: []
---

# momentum:retro Phase 4b-4f extension — fixture generation from findings

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the momentum:retro skill to automatically convert auditor-team findings of severity >= medium into executable YAML fixtures,
so that quality regressions are captured as verifiable regression tests the moment they are discovered, completing the flywheel between retro findings and ongoing eval coverage.

## Description

Extend the existing momentum:retro skill with five new phases that take retro auditor-team findings of severity >= medium and convert each into an executable YAML fixture written to the corresponding skill's evals/fixtures/sprint-{N}-{class-slug}.yml. Each fixture is verified at creation by running 10 samples against the model-at-time-of-failure and accepted as Active if the failure reproduces at the observed rate, or marked Suspect otherwise. Retro output extended to include: N fixtures generated, M Active, K Suspect, J Protected.

The five new phases:
- **Phase 4b** — Error classification: categorize each qualifying finding by error class (hallucination, workflow-skip, format-violation, etc.)
- **Phase 4c** — State reconstruction: recover the input context that produced the failure from sprint transcript or retro evidence
- **Phase 4d** — Fixture generation: write the YAML fixture to `evals/fixtures/sprint-{N}-{class-slug}.yml` in the relevant skill directory
- **Phase 4e** — Fixture verification: run 10 samples against the model-at-time-of-failure; accept as Active if failure reproduces at observed rate, else mark Suspect
- **Phase 4f** — Fixture report: summarize fixture outcomes in retro output (N generated, M Active, K Suspect, J Protected)

**Decision source:** dec-010-fixture-based-regression-testing-2026-04-22.md (D1 — retro extension is the third pillar of the practice primitive alongside the runner and the schema).

**Analysis source:** `_bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md` §7.

**Pain context:** Without this extension, retro findings are documented but not automatically converted to regression tests. Failures recur because there is no mechanism to capture the failure as a fixture at discovery time. The flywheel only closes when retro, runner, and schema work together — this story implements the retro's share of that loop.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Phase 4b classifies each auditor-team finding of severity >= medium by error class (hallucination, workflow-skip, format-violation, etc.)
- Phase 4c reconstructs the failure input context from sprint transcript or retro evidence
- Phase 4d writes a YAML fixture to `evals/fixtures/sprint-{N}-{class-slug}.yml` within the appropriate skill directory; fixture conforms to the micro-eval fixture schema (depends on micro-eval-fixture-yaml-schema-schemamd story)
- Phase 4e runs 10 samples against the model-at-time-of-failure; marks fixture Active if failure reproduces at the observed rate, Suspect otherwise
- Phase 4f extends retro output section to include: N fixtures generated, M Active, K Suspect, J Protected
- Retro skill completes without error when zero qualifying findings exist (graceful no-op for phases 4b-4f)
- Fixture runner integration works via the momentum micro-eval runner skill (depends on momentum-micro-eval-runner-skill story)
- Protected fixtures (from prior sprints) are counted but not regenerated

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

- Decision: dec-010-fixture-based-regression-testing-2026-04-22.md (D1 — retro extension as third practice pillar)
- Analysis: `_bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md` §7
- Depends on: momentum-micro-eval-runner-skill (runner skill story)
- Depends on: micro-eval-fixture-yaml-schema-schemamd (schema story)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
