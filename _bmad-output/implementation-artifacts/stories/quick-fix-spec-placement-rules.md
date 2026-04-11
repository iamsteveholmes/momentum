---
title: Quick-Fix Spec Placement Rules — Gherkin in Separate Files, Not Inline
story_key: quick-fix-spec-placement-rules
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Quick-Fix Spec Placement Rules — Gherkin in Separate Files, Not Inline

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a quick-fix workflow,
I want create Gherkin specs in separate .feature files (not inline in story files) and enforce this in the quick-fix workflow,
so that Gherkin is protected from accidental read by dev agents — the protected-paths rule applies correctly and tests aren't compromised.

## Description

Quick-fix stories sometimes embed Gherkin inline in the story file. The protected-paths rule protects .feature files but not inline Gherkin in story files. Dev agents can read the inline Gherkin and write to its expectations (AC-by-AC translation anti-pattern). Spec placement rules mandate a separate .feature file for all Gherkin.

**Pain context:** Nornspun upstream #7 (Medium). Inline Gherkin was observed in quick-fix stories. The test integrity guardrail depends on file separation — inline Gherkin breaks it silently.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Quick-fix workflow creates a separate .feature file for Gherkin specs
- Story file references the .feature file path but does not embed Gherkin inline
- Create-story workflow enforces the same rule for enriched stories
- Protected-paths.json already protects .feature — this aligns spec placement with that protection

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
