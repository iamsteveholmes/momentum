---
title: Commit summary template — enumerate in-scope and out-of-scope by AC
story_key: commit-summary-template-enumerates-in-scope-out-of-scope-by-ac
status: backlog
epic_slug: story-cycles
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# Commit summary template — enumerate in-scope and out-of-scope by AC

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want commit messages produced by dev skills to include explicit "Covered ACs:" and "Out of scope:" sections,
so that auditors and reviewers can immediately understand what was addressed in each commit and what was intentionally deferred.

## Description

Dev skill commit template must produce 'Covered ACs:' and 'Out of scope:' sections; partial fixes must explicitly declare remaining work. Applies to momentum:dev and any skill that authors commits. Touches: skills/momentum/skills/dev/ (commit template), skills/momentum/skills/quick-fix/ (commit template).

**Pain context:** auditor-human H13 ('Good lord I wish you had told me that before' — stub disclosure), H24 ('What fix did you commit? Did you move...every ViewModel?' — disclosure scope) from nornspun sprint-2026-04-12 retro. Signal type: Instruction. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Commit messages authored by momentum:dev include a "Covered ACs:" section listing each AC addressed by the commit
- Commit messages authored by momentum:dev include an "Out of scope:" section explicitly listing ACs or work items not addressed
- When a fix is partial, remaining work is declared in "Out of scope:" — not silently omitted
- momentum:quick-fix applies the same commit template structure
- Any other skill that authors commits follows the same template pattern
- Auditors reading commit history can determine scope without reviewing diffs

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
