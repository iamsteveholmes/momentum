---
title: Rename base body files to canonical naming
story_key: rename-base-body-files-to-canonical-naming
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
depends_on: []
touches: []
---

# Rename base body files to canonical naming

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want qa-reviewer.md renamed to qa.md and e2e-validator.md renamed to e2e.md with all references updated,
so that base body file naming follows the canonical one-base-per-role convention consistently.

## Description

Rename qa-reviewer.md to qa.md and e2e-validator.md to e2e.md to match the canonical one-base-per-role naming convention. Update all references in skills, workflows, and architecture. Depends on base-body-collapse-rollback.

**Pain context:** Inconsistent naming between base body files (qa-reviewer, e2e-validator vs. the expected short role names) creates confusion about what is a base body vs. a composed specialist and breaks the canonical lookup convention established by the one-base-per-role model.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- qa-reviewer.md is renamed to qa.md in the plugin's agent files
- e2e-validator.md is renamed to e2e.md in the plugin's agent files
- All references to qa-reviewer.md and e2e-validator.md in skills, workflows, and architecture docs are updated to the new names
- The canonical lookup table resolves qa → qa.md and e2e → e2e.md correctly
- No broken references remain after the rename

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
