---
title: "momentum:intake — remove worktree isolation, story-add is safe to run concurrently"
story_key: momentumintake-remove-worktree-isolation-story-add-is-safe
status: backlog
epic_slug: ad-hoc
feature_slug: ""
story_type: maintenance
depends_on: []
touches: []
---

# momentum:intake — remove worktree isolation, story-add is safe to run concurrently

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want intake agents to write stubs directly to main without worktree isolation,
so that stubs land immediately in .momentum/stories/ and are registered in the index without manual recovery steps.

## Description

Remove the EnterWorktree / worktree isolation step from the momentum:intake skill workflow. The index.json mutation performed by intake is a `sprint story-add` call that writes a brand-new unique slug key — it is non-colliding even under parallel execution. Worktree isolation adds overhead, delays story registration, and orphans stub files in branches rather than landing them directly in main. Fix: audit intake/workflow.md (and any SKILL.md) for EnterWorktree/ExitWorktree invocations and remove them. Verify that 8 parallel intake spawns (as in the DEC-033/034 cascade triage) all produce stubs directly in .momentum/stories/ with index entries written to main. Change type: skill-instruction.

**Pain context:** Intake agents spawn worktrees to protect against concurrent index.json collision, but each story-add writes a unique new slug key — there is no actual collision risk. Worktrees cause stubs to be orphaned in branches instead of landing in main, requiring manual copy+re-register. Observed during cascade triage: 4 of 8 intake agents created worktrees; triage had to copy stubs out and re-run story-add manually.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- No EnterWorktree or ExitWorktree calls exist in intake/workflow.md or intake/SKILL.md
- 8 parallel intake spawns all produce stub files directly in .momentum/stories/ (no branch artifacts)
- 8 parallel intake spawns all produce index entries in stories/index.json on main with no conflicts
- No manual copy/re-register steps required after parallel intake run

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
