---
title: Fail loud on empty/unrecognized change_type and reconcile index from story frontmatter — stop silent document-review mis-routes
story_key: fail-loud-on-empty-or-unrecognized-change-type
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: defect
depends_on: []
touches: []
---

# Fail loud on empty/unrecognized change_type and reconcile index from story frontmatter — stop silent document-review mis-routes

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer running sprint planning,
I want an empty or unrecognized `change_type` to produce a loud error (and stale index entries to be reconciled from story-file frontmatter),
so that a story is never silently routed to the wrong verification method by missing data.

## Description

Two defects in one seam, found during sprint-2026-06-10 planning:

1. **Silent wrong default.** `conduct-worktree-and-branch-creation` has `change_type: ""`
   (empty) in `.momentum/stories/index.json`. `momentum-tools sprint
   compute-verification-method` silently routed the empty value to `document-review` —
   wrong; the correct routing is `skill-invoke`. An empty/unrecognized `change_type`
   should error or escalate, never default silently (this mirrors FR133's rule that
   unclassified stories escalate rather than default).

2. **Index writer drift.** The story FILE frontmatter correctly declares
   `change_type: skill-instruction`; the index entry is stale/empty. sprint-manager is
   the sole index writer — the index should be reconciled from story frontmatter (or
   the write path that dropped the value fixed).

**Pain context:** A silent mis-route at planning time corrupts contract routing for the
whole sprint — the contract would have been authored as a `.review.md` document-review
artifact for a story that needs behavioral skill-invoke verification. Caught only
because the planner cross-checked the story file by hand.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `compute-verification-method` on an empty or unrecognized `change_type` exits non-zero with a diagnostic naming the story and the bad value — it never silently emits `document-review` (or any other method) as a fallback
- The stale index entry for `conduct-worktree-and-branch-creation` is reconciled to match its story-file frontmatter (`skill-instruction`), via the sprint-manager-owned write path
- The write path that produced the empty index value is identified and fixed (or a reconcile check is added) so story-file frontmatter and index `change_type` cannot drift silently

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
