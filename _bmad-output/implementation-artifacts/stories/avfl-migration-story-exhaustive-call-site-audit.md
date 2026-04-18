---
title: AVFL migration-story finding template — exhaustive call-site audit
story_key: avfl-migration-story-exhaustive-call-site-audit
status: backlog
epic_slug: quality-enforcement
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# AVFL migration-story finding template — exhaustive call-site audit

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want AVFL finding templates for migration-type stories to require a grep-based call-site audit of every production reference to the symbol being moved/renamed/deleted,
so that no import sites slip through to post-dev and the system converges in a single dev pass rather than requiring multiple fix iterations.

## Description

For migration-type stories, the AVFL finding template must require enumeration of every production reference site: a grep-based call-site audit of the symbol being moved/renamed/deleted, as an explicit checklist item before marking the fix complete. Touches: skills/momentum/skills/avfl/references/framework.json, possibly skills/momentum/skills/avfl/SKILL.md.

**Pain context:** auditor-review RQ-005, RQ-013 from nornspun sprint-2026-04-12 retro. InMemoryAppPrefs defect caught at plan level (CRIT-001) but 3 androidMain import sites slipped through to post-dev. System converged via 2-pass dev execution — not a thrash, but evidence the AVFL finding was under-scoped. Signal type: Workflow. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- When AVFL generates a finding for a migration-type story (rename/move/delete of a symbol), the finding template includes an explicit checklist item: "Grep all production source trees for references to `<symbol>` and enumerate every call site."
- The call-site checklist item must be satisfied (checked) before the finding can be marked resolved/complete.
- The audit covers all production source trees (e.g., androidMain, commonMain, iosMain) — not just the primary source set.
- framework.json updated to encode the call-site audit requirement for migration finding types.
- SKILL.md updated (if needed) to document the new template requirement for auditors.

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
