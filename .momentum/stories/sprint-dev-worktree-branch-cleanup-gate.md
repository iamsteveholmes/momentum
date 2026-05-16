---
title: Sprint-Dev Phase 7 Mandatory Worktree+Branch Cleanup (macOS-Portable)
story_key: sprint-dev-worktree-branch-cleanup-gate
status: backlog
epic_slug: sprint-dev-workflow
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
priority: medium
source: "retro sprint-2026-04-14 action item #7"
---

# Sprint-Dev Phase 7 Mandatory Worktree+Branch Cleanup (macOS-Portable)

<!-- INTAKE STUB: This story was captured by momentum:intake and enriched via momentum:distill.
     It is a conversational stub, NOT a dev-ready story. All sections below marked DRAFT require
     full rewrite by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer completing a sprint,
I want Phase 7 of sprint-dev to detect leftover worktrees and branches from the completed sprint and offer to clean them up,
so that stale worktrees do not accumulate across sprints and I retain control over when cleanup occurs.

## Description

Currently, Phase 7 (sprint-close) removes `worktree-agent-*` branches automatically, but does not detect or offer to remove story worktrees (`.worktrees/story-{slug}`) or story branches (`story/{slug}`) from the completed sprint. These can accumulate silently across sprints, consuming disk space and creating confusion during subsequent sprint planning.

The fix requires Phase 7 to scan for leftover worktrees and branches belonging to the completed sprint after the merge to main, present them to the developer with a removal prompt (not automatic), and log any cleanup actions taken.

This was identified during sprint-2026-04-27 retrospective as a practice gap: worktrees from completed sprints may accumulate without cleanup and the sprint-close gate has no detection or remediation step.

**Pain context:** Worktrees from completed sprints persist silently. The developer may not notice until `git worktree list` reveals multiple stale entries from past sprints. The cleanup should be offered, not forced — the developer may want to inspect a worktree before removing it.

## Acceptance Criteria

<!-- AC enrichment applied via momentum:distill from sprint-2026-04-27 retro finding.
     These ACs are distill-sourced, not yet through create-story full validation. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following acceptance criteria were captured from the retro finding and distill enrichment:

- Sprint-close (Phase 7) detects leftover worktrees and branches from the completed sprint (`.worktrees/story-{slug}` and `story/{slug}` for each story in the completed sprint)
- Offers the developer the option to remove them (not automatic — developer must confirm)
- Logs cleanup actions taken (which worktrees/branches were removed and which were kept)
- If no leftover worktrees or branches are found, Phase 7 proceeds without prompting the developer (happy path unchanged)
- Cleanup commands must be macOS-portable (no Linux-only flags or tools)

> Note: The ACs above were enriched from a retro finding via momentum:distill. They are starting
> points only. Create-story will replace them with validated, testable acceptance criteria.

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

Key implementation pointers (pre-create-story):
- Phase 7 action should run AFTER the merge to main and `worktree-agent-*` branch cleanup
- Detection: `git worktree list --porcelain` to find `.worktrees/story-{slug}` entries; `git branch -l 'story/*'` to find leftover story branches
- Removal: `git worktree remove --force .worktrees/story-{slug}` + `git branch -D story/{slug}`
- macOS-portable: avoid `git branch -l | xargs` patterns — use explicit loops

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Primary touch point: `skills/momentum/skills/sprint-dev/workflow.md` — Phase 7 step (n="7").

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Source: sprint-2026-04-27 retrospective — triage queue handoff
- Related: `sprint-dev-phase-7-gate.md` — companion Phase 7 story for MANUAL scenario sign-off

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
