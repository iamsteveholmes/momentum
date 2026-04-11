---
title: Backend Dev Pre-Work Diagnostic Step — Baseline Error Categorization Before Implementing
story_key: backend-dev-systematic-error-guidance
status: backlog
epic_slug: sprint-dev-workflow
depends_on: []
touches: []
---

# Backend Dev Pre-Work Diagnostic Step — Baseline Error Categorization Before Implementing

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a backend dev agent,
I want a mandatory pre-work diagnostic step that runs the full test suite before beginning implementation,
so that pre-existing errors are categorized as known baseline rather than wasted debugging turns for each agent that independently rediscovers them.

## Description

Momentum's dev agent prompts do not include: (1) known systematic error patterns for the project, (2) a "first run a smoke test before beginning" instruction, or (3) a mechanism for agents to share discoveries about systematic setup issues with subsequent agents.

When a project's test suite has a repeatable error sequence during setup (import errors, environment initialization, fixture issues), every dev agent hits it independently. Each wastes 3–5 turns diagnosing the same pre-existing condition before reaching their actual task.

The fix: a mandatory pre-work diagnostic step in sprint-dev skill:
1. Run the full test suite once before beginning
2. Categorize errors as: (a) pre-existing / known, (b) caused by your changes
3. Report pre-existing errors in the opening summary so the lead can update the spawn prompt for subsequent agents

Additionally: when the retro detects a pattern of identical error counts across many dev agents, it should flag it as a systematic environment issue requiring a one-time fix — not a per-agent debugging task.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 6, High). 20 backend-dev agents each produced exactly 19 errors — a suspiciously uniform count (212 errors / 20 agents = exactly 10.6, which rounds to 19 in per-agent tracking). The uniformity strongly suggests a systematic pre-work error sequence that every agent independently rediscovered. Combined cost: 60–100 wasted turns across 20 agents for a single fixable issue.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Sprint-dev skill includes a pre-work diagnostic step: run test suite once, categorize errors as pre-existing vs implementation-caused
- Dev agent opening summary includes pre-existing error count and categories
- Lead can update spawn prompt for subsequent agents with known-baseline errors
- Retro skill flags uniform error counts across many agents as a systematic environment issue signal

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
