---
title: Add Evals for constitution-builder Phases 2 and 3
story_key: constitution-builder-evals-phases-2-and-3
status: backlog
epic_slug: practice-compounds
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# Add Evals for constitution-builder Phases 2 and 3

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want eval test cases for constitution-builder Phases 2 and 3,
so that permissions generation and standing rules extraction are verified alongside the existing Quick Routing evals.

## Description

The constitution-builder skill currently has 3 evals in `skills/momentum/skills/constitution-builder/evals/evals.json`, all of which test Phase 6 (Quick Routing generation). Phases 2 and 3 have no test coverage.

Phase 2 (Permission Scoping) walks through 5 questions (owns, can't-write, can't-read, bash-allow, bash-deny) and generates a `## Permissions` block with a `settings.json` snippet. Phase 3 (Standing Rules) extracts always-on behavioral constraints from KB principle pages and developer input.

This story adds evals that exercise both phases end-to-end using the skill-creator eval framework.

**Pain context:** Discovered during the skill-creator eval loop session (2026-05-09) — after running 3 evals through the full loop and scoring 100%, we noted that none of the evals touched Phases 2 or 3. A bug in either phase would go undetected. Constitution-builder was just released at plugin v0.20.0, making this a higher-priority gap.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Eval for Phase 2: given a target skill and simulated developer answers (owns/deny/bash), the skill generates a `## Permissions` block containing owns, off-limits write, off-limits read, bash allowlist, bash denylist, and a valid `settings.json` snippet
- Eval for Phase 3: given a target skill and KB with principle pages on a declared practice (e.g. TDD), the skill extracts actionable, unconditional standing rules from those pages
- Both evals use the skill-creator assertion format in `evals/evals.json` with programmatic grep-based checks
- Both evals have baseline (without_skill) counterparts

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Skill: `skills/momentum/skills/constitution-builder/SKILL.md`
- Existing evals: `skills/momentum/skills/constitution-builder/evals/evals.json`
- Eval workspace: `skills/momentum/skills/constitution-builder-workspace/`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
