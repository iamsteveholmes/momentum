---
title: Refresh README skill counts after sprint merge
story_key: refresh-readme-skill-counts-after-sprint-merge
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Refresh README skill counts after sprint merge

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the README's skill counts and bmad-vendoring claim (and the Pages site's stats strip) updated after sprint-2026-06-10 merges to main,
so that the freshly rebuilt README stays truthful instead of silently drifting on day one.

## Description

The README was rebuilt on 2026-06-12 (commits 1b009f5..fadf869 on main) around the six-phase cycle, with a skill catalog and a GitHub Pages site (`site/index.html`). It states "No bmad-* skills are vendored in this repo — dev and code-reviewer delegate to BMAD Method skills installed alongside Momentum" and counts 27 momentum skills. The active branch `sprint/sprint-2026-06-10` adds vendored `bmad-*` skill directories under `skills/` (67 directories observed) and may add momentum skills. When that sprint merges to main, the README's vendoring claim and counts become false.

Scope: update `README.md` (Skill Catalog section and the bmad note below it, plus any counts in prose) and `site/index.html` (stats strip and skill data arrays) to match the merged main.

**Pain context:** Silent drift is the exact failure mode the README rebuild was meant to eliminate — the previous README went three months stale without anyone noticing. This story is the guard against the rebuild inheriting the same fate at the first sprint merge. Blocked until sprint-2026-06-10 merges to main.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- README.md skill counts (catalog header, group counts) match the post-merge state of `skills/momentum/skills/`
- The "No bmad-* skills are vendored" line is corrected or removed to reflect the vendored `bmad-*` directories on merged main
- `site/index.html` stats strip (momentum skills / agents / AVFL workers / hooks) matches merged main
- Any new momentum skills added by the sprint appear in the README catalog and the site's phase/cross-cutting data arrays

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
