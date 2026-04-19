---
title: Harden sprint-dev Phase 5 spawn prompts (systemic)
story_key: harden-sprint-dev-phase5-spawn-prompts
status: backlog
epic_slug: sprint-dev-workflow
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Harden sprint-dev Phase 5 spawn prompts (systemic)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-dev Phase 5 spawn prompts and the validator/QA agent definitions hardened so that service state is not pre-announced and live testing is not bypassed,
so that E2E and QA gates reliably catch HTTP/SSE scenarios instead of misclassifying them as MANUAL.

## Description

Update sprint-dev workflow.md Phase 5 spawn block to (a) never pre-announce service state, (b) start services in workflow.md before Phase 5 spawns, (c) reference e2e-validation.md in the project, (d) constrain MANUAL classification. Additionally update e2e-validator.md and qa-reviewer.md agent definitions with start-services-first sections so the gates are robust even if future spawn prompts regress. Touches: skills/momentum/skills/sprint-dev/workflow.md, skills/momentum/agents/e2e-validator.md, skills/momentum/agents/qa-reviewer.md.

**Pain context:** auditor-review RQ-003, RQ-004 from nornspun sprint-2026-04-12 retro. Phase 5 E2E-validator spawn prompt pre-announced 'the backend is NOT currently running' and offered pytest as a fallback, giving the agent explicit permission to skip live testing. 8 HTTP/SSE scenarios misclassified as MANUAL. QA Reviewer prompt showed similar pre-declaration pattern. Signal type: Instruction. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- sprint-dev workflow.md Phase 5 spawn block no longer pre-announces service state (e.g., removes "the backend is NOT currently running" framing)
- sprint-dev workflow.md starts required services before Phase 5 spawns E2E-validator / QA Reviewer
- sprint-dev workflow.md Phase 5 spawn prompts reference the project's `e2e-validation.md`
- MANUAL classification is constrained in the spawn prompt (HTTP/SSE scenarios cannot be classified MANUAL)
- `skills/momentum/agents/e2e-validator.md` gains a start-services-first section so the gate holds even if spawn prompts regress
- `skills/momentum/agents/qa-reviewer.md` gains a start-services-first section so the gate holds even if spawn prompts regress
- Regression test: a rerun against nornspun-style HTTP/SSE scenarios no longer yields MANUAL misclassification

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
