---
title: Base-body collapse rollback
story_key: base-body-collapse-rollback
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
depends_on: []
touches: []
---

# Base-body collapse rollback

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the plugin to ship only one dev.md base body per role (removing pre-shipped specialist bodies),
so that the composition mechanism works at the right layer and projects are not locked into Momentum's taxonomy guesses.

## Description

Remove pre-shipped dev-frontend.md, dev-build.md, dev-skills.md from the plugin and consolidate to one dev.md base body per role. The pre-shipped specialist bodies are at the wrong layer — they duplicate the composition mechanism that build-guidelines provides and lock projects into Momentum's taxonomy guesses. Required for the Gen-2 three-tier model to work: composed specialists live only in .claude/guidelines/agents/, produced per-project.

**Pain context:** The pre-shipped specialist files duplicate the composition mechanism and prevent the Gen-2 three-tier agent model from functioning correctly. Without removing these files, composed specialists cannot be the canonical source in .claude/guidelines/agents/.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- dev-frontend.md, dev-build.md, and dev-skills.md are removed from the plugin's shipped agent files
- A single dev.md base body exists per role in the plugin
- Composed specialist files are expected only in .claude/guidelines/agents/ per-project
- All references to the removed files in skills, workflows, and architecture docs are updated or removed
- The Gen-2 three-tier model can function without the removed pre-shipped specialists

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
