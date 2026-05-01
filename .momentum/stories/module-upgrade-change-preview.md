---
title: Module Upgrade Change Preview — Diff Before Apply
story_key: module-upgrade-change-preview
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Module Upgrade Change Preview — Diff Before Apply

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer triggering a module setup or upgrade,
I want a preview of all file changes before they are applied,
so that I am never surprised by unexpected git state after an upgrade completes.

## Description

Module setup/upgrade skills apply file changes without a preview step. The developer has no opportunity to review what will be modified before the skill executes. For upgrades that touch directory structure or file locations, this creates surprise git state with no clear explanation.

Any module setup or upgrade skill must include a preview step before applying changes:
- List files that will be created, modified, or deleted
- Highlight directory structure changes explicitly
- Show file moves or renames as `old path → new path`
- Present to developer: "The upgrade will make these changes. Proceed?"
- Apply changes only after explicit developer approval

The preview should be diff-style so the developer can assess risk without reading full file contents.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 7, Medium). A BMad builder upgrade from 1.0.0 to 1.5.0 modified files without communicating what would change. User: "What the heck just happened to my git?" and "Did it change the bmad output location?" — discovered unexpected state after the fact. Earlier: "wait are you manually updating the skill files? Shouldn't you have copied those from the bmb github repo?" — indicating the upgrade process was unclear throughout.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Module setup/upgrade skills include a preview step before applying any changes
- Preview lists files to be created, modified, deleted, and moved/renamed
- Developer must explicitly approve before changes are applied
- Preview is diff-style (not full file contents)
- Directory structure changes are highlighted separately from content changes

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
