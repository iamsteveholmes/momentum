---
title: "Live E2E: compose + register + resolve a Gen-2 agent against a real manifest + KB"
story_key: live-e2e-compose-register-resolve-gen-2-agent
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: exploration
depends_on: [manifesto-format-normative-file-pattern-ownership-field]
touches: []
---

# Live E2E: compose + register + resolve a Gen-2 agent against a real manifest + KB

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a live executable E2E that runs the full agent-composition pipeline against a real fixture project,
so that I have running-app proof — not just an instruction trace — that build-guidelines composes, registers (with non-empty patterns), and resolves a specialist agent end-to-end.

## Description

E2E for sprint-2026-06-18 was integration-TRACE (walking the skill instructions), not live execution — there is no running-app proof that build-guidelines actually composes, registers (with non-empty patterns), and resolves a specialist agent end-to-end against a real project manifest + KB.

Fix: build a live executable E2E that runs the full agent-composition pipeline against a real fixture (e.g., the nornspun project) and asserts `agent resolve --touches` returns the composed slug, the composed file has the diagnostic table + base body, etc.

Best sequenced AFTER the manifesto patterns field (story `manifesto-format-normative-file-pattern-ownership-field`) lands, so it tests the deterministic path.

This is a real backlog item, NOT a quick-fix.

**Pain context:** Surfaced at the sprint-2026-06-18 conduct end-gate as a "still hollow" gap. Important for real confidence in the cohort, and the natural validation once the manifesto patterns field makes resolution deterministic. Priority: MEDIUM. Depends on `manifesto-format-normative-file-pattern-ownership-field`.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- A live, executable E2E runs the full agent-composition pipeline against a real fixture project (e.g., nornspun) with a real manifest + KB.
- The E2E asserts `momentum-tools agent resolve --touches` returns the composed agent slug (non-empty patterns registered).
- The E2E asserts the composed agent file contains the diagnostic table + base body.
- It is sequenced AFTER the manifesto patterns field lands, so it exercises the deterministic resolution path.

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
