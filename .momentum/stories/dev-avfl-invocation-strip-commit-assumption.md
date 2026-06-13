---
title: Strip the residual dev-commits assumption from avfl-invocation.md
story_key: dev-avfl-invocation-strip-commit-assumption
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
priority: low
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/dev/references/avfl-invocation.md
---

# Strip the residual dev-commits assumption from avfl-invocation.md

## Story

As the maintainer of the dev-side artifacts,
I want `skills/momentum/skills/dev/references/avfl-invocation.md` reconciled with the no-commit dev contract,
so that the last dev-side reference asserting the dev/bmad-dev-story produces commits no longer contradicts DEC-035.

## Why this exists (triaged-out finding ca-01 from sprint-2026-06-10)

The dev-commit-authority story swept commit instructions out of the dev artifacts, but `avfl-invocation.md` was outside that story's writable set and was left untouched. It still: asserts "regardless of how many intermediate commits bmad-dev-story made" (assumes dev-side commits exist), prescribes a committed-only diff capture (`git diff target...story`) that returns **empty** under the no-commit regime, references a nonexistent "Step 7", and says "the workflow exits the worktree" (contradicting the no-worktree-management rule). The dev-commit-authority sweep eval enumerates only six files and omits this one, so the eval passes while the residual survives.

## Acceptance Criteria

1. `avfl-invocation.md` no longer assumes the dev or bmad-dev-story produces commits: committed-only diff capture is replaced with working-tree capture (`git status --porcelain` + `git diff`), the bmad-dev-story-commits phrasing is removed, the nonexistent Step-7 pointer is dropped, and the worktree-exit line is corrected or removed. (Alternatively, if the file is genuinely orphaned — dev no longer invokes AVFL — delete it and remove its references.)
2. The dev-commit-authority sweep eval's grep scope is widened to the full `skills/momentum/skills/dev/` tree so a future residual of this class is caught.

## Dev Notes
- Decide keep-and-reconcile vs delete based on whether dev still invokes AVFL at all; record the decision.

## Dev Agent Record
