# Eval: Stale collision at story launch triggers deterministic remove-and-recreate

**Surface under test:** Step 2.1 story launch sequence — idempotent collision handling for
leftover story branches and worktrees.

**Regression guard for:** Missing collision handling at launch (2026-06-09 conductor
effectiveness review). Without explicit handling, a leftover `story/{slug}` branch or
`.worktrees/story-{slug}` directory from a prior interrupted session (not caught by
reconcile because the story was not in `in-progress` state) would cause `git worktree add`
to fail, forcing improvisation.

## Scenario

**Given:** A sprint build is running with `sprint/sprint-2026-06-10` as the active sprint
branch. A story S with slug `my-feature` is entering the step 2.1 launch sequence. A stale
branch `story/my-feature` already exists (leftover from a prior session). A stale worktree
directory `.worktrees/story-my-feature` also exists.

**When:** The Conductor executes the branch-and-worktree creation action for story S in the
STAGE-1 DEV SPAWN block (step 2.1.3).

**Then:**

1. The Conductor removes the existing worktree first:
   `git worktree remove --force --force .worktrees/story-my-feature`
2. The Conductor deletes the existing branch:
   `git branch -D story/my-feature`
3. The Conductor then creates the fresh branch from the sprint tip and adds the worktree
   (same commands as the fresh-launch path).
4. No developer prompt is presented. The collision is handled deterministically.
5. The removal semantics mirror the RECONCILE ON START action in Phase 1:
   same ordering (worktree first, then branch), forced worktree removal,
   same `-D` on branch delete.

## Pass Criteria

- The workflow text at the creation action includes a pre-removal check: if the worktree
  path exists, remove it with `git worktree remove --force --force`; if the branch exists,
  delete it with `git branch -D`.
- The removal mirrors the RECONCILE ON START action in Phase 1: same ordering (worktree
  first, then branch), forced worktree removal, same `-D` on branch delete.
- After removal, the fresh creation proceeds (branch from sprint tip, worktree add).
- No developer prompt or interactive choice is introduced — the handling is fully automatic.
- The collision handling runs before the dev spawn, as part of the Conductor-executed
  creation action.

## Fail Criteria

- No collision handling exists — the creation assumes a clean state and would fail on
  existing branch/worktree.
- The collision triggers a developer prompt or presents a choice.
- The removal is not forced (e.g., missing `--force`) or uses `-d` instead of `-D`.
- The collision handling is delegated to the dev agent.

## Verification Method

**Inspection of workflow text (static leg):**

1. Read `skills/momentum/skills/conductor/workflow.md` at the STAGE-1 DEV SPAWN block.
   Confirm the creation action includes pre-removal checks with
   `git worktree remove --force --force` and `git branch -D`, mirroring the reconcile's
   forced removal semantics.
2. Confirm no `<ask>` or developer-prompt element is introduced in the collision path.
3. Cross-reference with the RECONCILE ON START action in Phase 1 to confirm the removal
   commands use the same ordering (worktree first, then branch) and forced-removal
   semantics.

**Behavioral leg (scratch-repo git exercise):**

4. In a scratch git repository, create a branch `sprint/test-sprint`, a stale branch
   `story/my-feature`, and a stale worktree at `.worktrees/story-my-feature`.
5. Simulate the collision-handling instructions from the workflow:
   - `git worktree prune`
   - `git worktree remove --force --force .worktrees/story-my-feature`
   - `git branch -D story/my-feature`
   - `git branch story/my-feature sprint/test-sprint`
   - `git worktree add .worktrees/story-my-feature story/my-feature`
6. Confirm the sequence completes without error and the resulting worktree is on a fresh
   `story/my-feature` branch rooted at `sprint/test-sprint`.
7. Confirm the collision path produces no interactive prompt — the sequence runs to
   completion deterministically.
