---
title: momentum:micro-eval runner skill
story_key: momentum-micro-eval-runner-skill
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quality-gates-enforced
story_type: feature
depends_on: []
touches: []
---

# momentum:micro-eval runner skill

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a momentum:micro-eval runner skill that discovers, executes, and reports on fixture-based regression tests across all skills,
so that every fixture story in the backlog has the foundational infrastructure it depends on (per DEC-010), enabling probabilistic pass/fail validation against pinned models.

## Description

Build the momentum:micro-eval runner skill that discovers fixture YAML files at skills/**/evals/fixtures/*.yml across all skills, executes each fixture against the model and temperature pinned in its frontmatter, and reports probabilistic pass/fail (matching the failure_rate_in_range assertion within tolerance). Foundational infrastructure — required by every fixture story currently in the backlog (see DEC-010). MVI scope: discovery, execution against one model per fixture, basic pass/fail reporting per the lifecycle states (Candidate, Active, Protected, Stale, Retired, Suspect). Defer cross-model matrix and CI integration to follow-up stories. Decision source: dec-010-fixture-based-regression-testing-2026-04-22.md (D1 + D4). Analysis source: _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md §3, §4, §5, §9.

**Pain context:** Every fixture story currently in the backlog blocks on this runner skill — without it, fixtures cannot be executed or validated. DEC-010 established fixture-based regression testing as the chosen approach; this story delivers the minimum viable infrastructure to unblock the rest of the fixture work. Source: triage — conversation (DEC-010 follow-up).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Discovers fixture YAML files at `skills/**/evals/fixtures/*.yml` across all skills
- Executes each fixture against the model and temperature pinned in its frontmatter
- Reports probabilistic pass/fail matching the `failure_rate_in_range` assertion within tolerance
- Supports the six lifecycle states: Candidate, Active, Protected, Stale, Retired, Suspect
- MVI scope only — single model per fixture, basic pass/fail reporting
- Cross-model matrix deferred to a follow-up story
- CI integration deferred to a follow-up story
- Aligns with DEC-010 decisions D1 and D4

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

Decision source: `dec-010-fixture-based-regression-testing-2026-04-22.md` (D1 + D4)
Analysis source: `_bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md` §3, §4, §5, §9

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
