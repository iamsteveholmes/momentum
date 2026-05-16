---
title: audit-skill-descriptions-routing-distinctiveness
story_key: audit-skill-descriptions-routing-distinctiveness
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-impetus-session-orientation
story_type: maintenance
depends_on: []
touches: []
---

# audit-skill-descriptions-routing-distinctiveness

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want skill descriptions for all Momentum plugin skills to have clearly distinct, non-overlapping trigger surfaces,
so that Impetus routes requests to the correct skill without developer intervention.

## Description

Full audit of Momentum plugin skill descriptions for overlapping trigger phrases that could cause Impetus routing misfires. In sprint-2026-05-03, the developer had to redirect an agent to the correct skill because a grooming task was routed to the wrong skill. This story delivers: (1) a list of all skill descriptions with overlapping trigger surfaces, (2) proposed disambiguation fixes, (3) application of approved fixes. Focus is on pairs where one skill could plausibly match requests intended for another — e.g., feature-grooming vs epic-grooming vs refine vs triage.

**Pain context:** Developer had to manually redirect routing in sprint-2026-05-03 due to a grooming task landing in the wrong skill. Misrouting causes friction, wastes agent tokens, and can silently produce the wrong output if unnoticed. The risk compounds as the plugin skill count grows.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- [ ] All Momentum skill descriptions are audited and a report of overlapping trigger surfaces is produced
- [ ] Skill pairs with ambiguous routing (e.g., feature-grooming / epic-grooming / refine / triage) are explicitly identified
- [ ] Disambiguation fixes are proposed for each overlapping pair
- [ ] Developer reviews and approves proposed fixes before application
- [ ] Approved fixes are applied to the relevant SKILL.md description blocks
- [ ] No skill description change broadens an existing trigger surface — only narrows or sharpens

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
