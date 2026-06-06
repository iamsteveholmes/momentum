---
title: Tighten dev/fixer write-scope to stop out-of-scope story-spec edit-then-revert
story_key: tighten-dev-fixer-write-scope-stop-story-spec-edits
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: defect
priority: high
depends_on: []
---

# Tighten dev/fixer write-scope to stop out-of-scope story-spec edit-then-revert

## Story
Dev/fixer agents must be confined to an explicit writable file set so they stop editing the story `.md` or sibling workflow files, forcing Conductor reverts.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): **5 of 21 stories (24%)** required a Conductor revert of an out-of-scope edit to the story file or a hot sibling workflow — `dev-read-contract-part-a-header`, `conduct-coverage-disposition-branch`, `code-review-adapter-retire-stub`, `stakes-classification-rubric`, `conduct-preflight-halts`. The edit-then-revert pattern also caused the scorecard-divergence defect (a reverted "fix" still reported as fixed).

## What's needed
- The dev/fixer spawn prompt enumerates the exact writable file set and forbids editing the story `.md` and sibling stories' files.
- A cross-artifact finding routes to a reconciliation note for the owning story rather than an in-worktree edit.
- Out-of-scope revert rate falls below 10% of stories.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related: `reconcile-fix-disposition-with-conductor-scope-reverts` (the downstream scorecard symptom), `dev-fixer-agent-definition`, `dev-strip-merge-cleanup-authority`
