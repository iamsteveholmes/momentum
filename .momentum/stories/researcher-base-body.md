---
title: researcher-base-body
story_key: researcher-base-body
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
depends_on: []
touches: []
---

# researcher-base-body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a researcher base body agent file (`agents/researcher.md`) shipped in the Momentum plugin,
so that the researcher role is universally available for project-specific composition via the agent-composition-pipeline.

## Description

Create `agents/researcher.md` as one of the nine universal base bodies defined in DEC-020. This file defines the unconditioned researcher role — it owns research artifacts, synthesis briefings, and knowledge investigation outputs. The base body carries no project-specific context; that layer is added by the agent-composition-pipeline at install time.

BMAD role alignment: matches the researcher role. Document ownership: research docs, synthesis briefings, investigation reports.

**Pain context:** DEC-020 established the full agent taxonomy and nine universal base bodies. The researcher base body is one of the core nine that must be shipped in the plugin. Without it, any project relying on Momentum for research orchestration lacks a standardized researcher role definition, forcing ad-hoc workarounds per project.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- `agents/researcher.md` exists in the Momentum plugin module
- File defines the unconditioned researcher role (no project-specific context)
- Document ownership section covers: research docs, synthesis briefings, investigation reports
- BMAD role alignment is documented (matches researcher role)
- Base body is composable — agent-composition-pipeline can inject project-specific context on top of it
- File follows the same structure/schema as other base body agent files in the plugin

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

- Source: triage — handoff agent-architecture-triage-2026-05-16.md (DEC-020)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6 (dev-skills specialist)

### Debug Log References

None — straightforward agent definition creation.

### Completion Notes List

- Created `skills/momentum/agents/researcher.md` as universal base body per DEC-020
- File defines unconditioned researcher role — no project-specific context
- Document ownership declared: research docs, synthesis briefings, investigation reports
- BMAD role alignment documented (researcher persona)
- Standard Large File Handling section included per agent-skill-development-guide.md convention
- Output structure section provides a canonical template for research artifact format
- SendMessage pattern documented for team context spawning

### File List

- `skills/momentum/agents/researcher.md` (created)
