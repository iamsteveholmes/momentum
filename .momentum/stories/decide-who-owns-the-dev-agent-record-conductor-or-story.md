---
title: Decide who owns the Dev Agent Record: Conductor or story template
story_key: decide-who-owns-the-dev-agent-record-conductor-or-story
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Decide who owns the Dev Agent Record: Conductor or story template

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want have a resolved, consistent answer for who fills the Dev Agent Record section of a story spec during a Conductor-built sprint,
so that build agents and the story-template DoD stop contradicting each other, and every conduct-built story can actually satisfy its own Definition of Done.

## Description

The story-template DoD requires developers to fill the 'Dev Agent Record' section of the story spec file, but the Conductor's write-scope forbids build agents from editing the story's own spec file. This template/authority conflict was observed on at least 3 stories this sprint (goal-conditions, greeting, verification-routing). This is a decision, not a bounded fix: either (a) the Conductor gains narrow write authority to append the Dev Agent Record, or (b) the story template drops that DoD requirement for conduct-built stories in favor of some other record location. This stub captures the decision to be made — route through momentum:decision before implementation.

**Pain context:** Systemic — observed independently on 3+ stories in sprint-2026-08-03 build wave (goal-conditions, greeting, verification-routing), not a one-off.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- [ ] Decision recorded: Conductor writes the record, OR template drops the requirement for conduct-built stories
- [ ] If Conductor writes it: write-scope rule updated to grant narrow, auditable permission for exactly that section
- [ ] If template changes: story-template.md DoD section updated, and a clear statement of where dev-agent provenance is captured instead
- [ ] Fix applied consistently across affected stories/templates

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

## Source

triage — Conductor build wave sprint-2026-08-03 (verification-routing + goal-conditions + greeting, systemic)
