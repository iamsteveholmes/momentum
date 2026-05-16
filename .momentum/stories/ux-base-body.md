---
title: ux-base-body
story_key: ux-base-body
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
depends_on: []
touches: []
---

# ux-base-body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a `agents/ux.md` base body file that defines the UX agent role contract,
so that orchestrators like sprint-dev and retro can spawn a consistent, unconditioned UX agent that the agent-composition-pipeline can layer project context onto.

## Description

Create `agents/ux.md` as one of the nine universal base bodies that ship in the Momentum plugin per DEC-020. The ux base body defines the role contract for a UX agent spawned by orchestrators like sprint-dev and retro. It owns UX-related document types and provides the unconditioned role definition that the agent-composition-pipeline layers project context onto. BMAD role alignment: matches the ux-designer role. Document ownership: ux specs, wireframes, design docs, UX requirements.

**Pain context:** DEC-020 established the full agent taxonomy and build pipeline. The nine universal base bodies must all ship with the plugin. Without `agents/ux.md`, the agent-composition-pipeline cannot assemble a UX agent for any project, blocking orchestrator-driven UX work across the practice.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `agents/ux.md` exists in the Momentum plugin under the canonical base-body path
- The file defines the UX agent role aligned with the BMAD ux-designer role
- Document ownership is declared: ux specs, wireframes, design docs, UX requirements
- The role definition is unconditioned (no project-specific context baked in)
- The file is recognized by the agent-composition-pipeline as a valid base body
- Orchestrators (sprint-dev, retro) can reference this base body when spawning a UX agent

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

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
