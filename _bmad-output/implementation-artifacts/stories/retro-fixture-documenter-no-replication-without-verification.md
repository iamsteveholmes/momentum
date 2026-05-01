---
title: "retro fixture: documenter no-replication-without-verification"
story_key: retro-fixture-documenter-no-replication-without-verification
status: backlog
epic_slug: epic-4-complete-story-cycles
feature_slug: momentum-retro-and-flywheel
story_type: defect
depends_on:
  - fix-retro-documenter-replication-defect
touches: []
---

# retro fixture: documenter no-replication-without-verification

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies the retro documenter never replicates auditor-team output verbatim without independent verification,
so that the documenter-replication defect cannot regress and the documenter retains its independent-verification role.

## Description

Build a behavioral micro-eval fixture that verifies the retro documenter never replicates auditor-team output verbatim without independent verification. Depends on the existing story `fix-retro-documenter-replication-defect`.

**Pain context:** When the documenter replicates auditor output verbatim without independent verification, the retro loses its check-and-balance value — auditor errors propagate unchallenged. The fix story addresses the immediate defect; this fixture pins the no-replication contract so the verification step cannot be silently dropped again.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture provides a synthetic auditor-team output with verifiable claims
- Fixture invokes the retro documenter against the auditor output
- Fixture asserts the documenter's output does not contain verbatim duplication of auditor extracts beyond a defined similarity threshold
- Fixture asserts the documenter's output shows evidence of independent verification (e.g., direct source citations, restated findings, or explicit confirmation steps)
- Fixture fails loudly when verbatim replication is detected without verification
- Fixture is wired into the practice micro-eval suite
- Fixture is gated to run only after `fix-retro-documenter-replication-defect` is merged

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
