---
title: "build-guidelines: orchestrated/headless bypass for the role×domain confirmation ask"
story_key: build-guidelines-orchestrated-headless-bypass-for-role-domain-ask
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# build-guidelines: orchestrated/headless bypass for the role×domain confirmation ask

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer running build-guidelines in a fully-automated / CI context,
I want an orchestrated/headless bypass for the Consult-phase role×domain confirmation `<ask>`,
so that an automated invocation can proceed without blocking on a human prompt.

## Description

`build-guidelines/workflow.md` has a Consult-phase `<ask>` ("confirm the role×domain matrix is current") with no orchestrated-mode bypass, so a fully-automated / CI invocation would block. The developer-driven path (a human confirms the matrix before a sprint) works fine — this is the natural human checkpoint.

Fix: add an orchestrated/headless bypass (mirroring the bypasses added to constitution-builder this sprint) gated on inputs being supplied, so automated invocation can proceed.

This is a real backlog item, NOT a quick-fix.

**Pain context:** Surfaced at the sprint-2026-06-18 conduct end-gate as a "still hollow" gap. The developer-driven path already works and the human checkpoint is arguably desirable; this only matters for future full automation. Priority: LOW.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `build-guidelines/workflow.md` Consult-phase role×domain confirmation `<ask>` has an orchestrated/headless bypass.
- The bypass is gated on required inputs being supplied (mirroring the constitution-builder bypass pattern added this sprint).
- The developer-driven (human-confirmed) path remains unchanged and continues to work.

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
