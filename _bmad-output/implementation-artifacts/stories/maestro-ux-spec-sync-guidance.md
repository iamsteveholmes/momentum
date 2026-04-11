---
title: Maestro UX Spec Sync Guidance — Scan Test Fixtures After UX Story Completions
story_key: maestro-ux-spec-sync-guidance
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Maestro UX Spec Sync Guidance — Scan Test Fixtures After UX Story Completions

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As an E2E validator,
I want a pre-validation spec-sync check that scans Maestro test fixtures for stale references after UX story completions,
so that tests fail because behavior broke — not because UI copy changed and the fixture wasn't updated.

## Description

When UX stories modify or remove UI copy, downstream Maestro test fixtures can silently contain stale references. These produce misleading test failures: the test fails on the old copy, not on a behavioral regression. The stale fixture isn't caught by any automated check — it surfaces as a confusing failure when the test suite runs.

E2E skill should include a spec-sync check in its pre-validation step:
1. Check for UX story completions since the last E2E run
2. For each completed UX story: scan Maestro test files for references to modified or removed UI copy
3. Flag stale references before running (not after — stale tests produce misleading failures)

This is a guidance gap Momentum should encode as a pattern, even though the specific fixtures are project-owned. The pattern is universal: any project using Maestro with UX stories needs this check.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 11, Low). A Maestro test referenced "The Nornspun Experience" — UI copy removed in a prior UX story. User had to manually identify and flag the stale reference at message 93: "That was removed in one of our UX stories. It should be removed from that maestro test." Not caught by any automated check during the sprint.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- E2E skill includes a pre-validation spec-sync step
- Step checks for UX story completions since last E2E run
- Step scans Maestro test files for references to UI copy from completed UX stories
- Stale references are flagged before test execution, not discovered as failures after
- Check is framed as a pattern/guidance, not a hard-coded project-specific fixture list

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
