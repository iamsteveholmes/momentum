---
title: Retro Phase 1 resilience — detect audited-but-unclosed sprint
story_key: retro-phase-1-resilience-audited-but-unclosed-sprint
status: backlog
epic_slug: quality-enforcement
feature_slug: 
story_type: maintenance
depends_on: []
touches: []
---

# Retro Phase 1 resilience — detect audited-but-unclosed sprint

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want retro Phase 1 to detect when a sprint has already been audited but not closed,
so that I can recover from a session truncation without re-running the full retro.

## Description

When `momentum:retro` is invoked and the most recent completed sprint has `retro_run_at == null` but already has a `retro-transcript-audit.md` artifact present in `.momentum/sprints/{{slug}}/`, the retro should detect this audited-but-unclosed state and offer a fast-path: skip the full audit and simply run `momentum-tools sprint retro-complete` to close the sprint.

This scenario occurs when a retro session completes Phase 5 (findings + story stubs, committed) but the session terminates before Phase 6 executes the closure command. Currently, re-invoking the retro would re-run the entire audit unnecessarily.

**Pain context:** Observed in sprint-2026-04-27 retro — session ended after the audit commit, `retro_run_at` stayed null, Impetus incorrectly flagged the sprint as needing a retro. Required manual diagnosis and a direct CLI call to fix. Will recur any time a retro session is interrupted after Phase 5.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- When retro is invoked and the target sprint has `retro_run_at == null` but `retro-transcript-audit.md` exists in the sprint directory, Phase 1 detects this as "audited-but-unclosed"
- The skill presents a fast-path offer: "Retro artifacts exist for {{slug}} but sprint is not closed. Run closure only?"
- On confirmation, runs `momentum-tools sprint retro-complete` and reports success
- On decline, continues with the full retro workflow (allowing re-audit if desired)
- Full retro path (no prior audit) is unaffected

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
