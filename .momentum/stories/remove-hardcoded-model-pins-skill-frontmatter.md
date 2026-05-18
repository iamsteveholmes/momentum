---
title: remove hardcoded model pins from 23+ skill frontmatter files
story_key: remove-hardcoded-model-pins-skill-frontmatter
status: backlog
epic_slug: automatic-quality-enforcement
feature_slug: momentum-model-routing-strategy
story_type: defect
depends_on: []
touches: []
---

# remove hardcoded model pins from 23+ skill frontmatter files

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to remove the hardcoded model: claude-sonnet-4-6 pins from all skill frontmatter files and replace with proper capability-tier declarations,
so that skill subagents respect the session's model selection and don't trigger billing gates via forced model mismatches.

## Description

Defect: 23+ skill frontmatter files hardcode `model: claude-sonnet-4-6`, overriding the session's model selection. This caused the developer to hit the 1M billing gate in two separate sprint sessions. Fix: remove specific model ID pins from all skill frontmatter — model routing must be delegated to session-level config or declared via capability tier, not string pin. Audit all skill files, remove or replace the hardcoded model pins with capability-tier declarations. Source: sprint-2026-05-16 retro handoff iq-20260518043618.

**Pain context:** Billing gate hit twice in sprint-2026-05-16 directly caused by skill frontmatter hardcoding claude-sonnet-4-6. Every subagent spawn triggers the billing gate. Blocks productive sprint work.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- (1) all skill frontmatter files audited for hardcoded model IDs
- (2) model: claude-sonnet-4-6 and similar specific model ID pins removed
- (3) where needed, replaced with effort: or model tier declarations per model-routing.md
- (4) sprint workflow runs without hitting billing gates from model pin conflicts
- (5) model-routing.md updated to clarify the policy (no specific model ID pins in frontmatter)

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
