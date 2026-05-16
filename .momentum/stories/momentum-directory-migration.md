---
title: momentum-directory-migration
story_key: momentum-directory-migration
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
story_type: maintenance
depends_on: []
touches: []
---

# momentum-directory-migration

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want all pipeline knowledge artifacts to live under `momentum/` instead of `_bmad-output/planning-artifacts/`,
so that the project directory structure reflects the architecture decisions codified in DEC-022 and paths are consistent across all skills and references.

## Description

Migrate `_bmad-output/planning-artifacts/` to `momentum/` — all subfolders (research/, analysis/, decisions/, ux/, architecture/, pm/, sprints/), and update all skill references throughout the codebase to use the new paths. `.momentum/` stays as operational state (no change). The `momentum/` directory becomes the home for all pipeline knowledge artifacts.

Per DEC-022. This migration must update:
- All skill `workflow.md` files that reference `_bmad-output/planning-artifacts/`
- All `CLAUDE.md` references
- All story specs with `derives_from` pointing to old paths
- The `features.json` path references

**Pain context:** The old `_bmad-output/planning-artifacts/` path is a historical artifact that predates the agent architecture redesign. With DEC-022 now recorded, having skills and references still pointing to the old path creates drift between the architecture decisions and the actual codebase. This will cause confusion for future agents and developers and must be resolved before the composition pipeline builds further on top of these paths.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- All files under `_bmad-output/planning-artifacts/` are moved to `momentum/` preserving subfolder structure (research/, analysis/, decisions/, ux/, architecture/, pm/, sprints/)
- `_bmad-output/planning-artifacts/` no longer exists after migration
- `.momentum/` operational state directory is untouched
- All skill `workflow.md` files updated to reference `momentum/` instead of `_bmad-output/planning-artifacts/`
- All `CLAUDE.md` files updated with correct paths
- All story spec files with `derives_from` updated to new paths
- `features.json` path references updated
- No broken path references remain in the codebase after migration

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

Source: triage — handoff agent-architecture-triage-2026-05-16.md (DEC-022)

_DRAFT — create-story will add additional source citations from architecture docs, PRD, and relevant code._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
