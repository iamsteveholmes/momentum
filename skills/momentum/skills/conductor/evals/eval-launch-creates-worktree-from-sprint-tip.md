# Eval: Story launch creates branch and worktree from sprint tip before dev spawn

**Surface under test:** Step 2.1 story launch sequence — branch and worktree creation action.

**Regression guard for:** Missing worktree-creation step (2026-06-09 conductor effectiveness review,
adversarially verified). The defect was that `conductor/workflow.md` passed `worktree_path` to the
dev agent but never created the worktree or the story branch, forcing the executing model to
improvise the most isolation-critical git operation in the build.

## Scenario

**Given:** A sprint build is running with `sprint/sprint-2026-06-10` as the active sprint branch.
A story S with slug `my-feature` is in the frontier and entering the step 2.1 launch sequence
for the first time. No `story/my-feature` branch exists. No `.worktrees/story-my-feature`
directory exists. The pre-flight reconcile (step 1) has already completed.

**When:** The Conductor executes the step 2.1 launch sequence for story S, reaching the
STAGE-1 DEV SPAWN block (sub-step 2.1.3).

**Then:**

1. Before the stage-1 dev agent is spawned, the Conductor creates the story branch
   `story/my-feature` with an explicit base of `sprint/sprint-2026-06-10` — the sprint
   branch is stated literally in the creation command, not inferred or left as a default.
2. The Conductor creates the worktree at `.worktrees/story-my-feature` checked out on
   branch `story/my-feature`.
3. Both operations are performed by the Conductor itself inside the launch loop (not
   delegated to the dev agent).
4. The worktree exists and is checked out on the correct branch before the dev spawn fires.
5. The action cites `references/per-story-review-diff-range.md` Scenario A as the
   rationale for forking from the sprint tip (merge-base isolation).

## Pass Criteria

- The workflow text at the STAGE-1 DEV SPAWN block contains explicit branch creation and
  worktree-add commands with `sprint/{{sprint_slug}}` stated as the base ref.
- The creation action appears before the `Resolve agent:` / `Spawn {{dev_agent}}` lines.
- The action includes a rationale note citing `per-story-review-diff-range.md` Scenario A.
- The creation is Conductor-executed (no delegation to dev agent; the existing "Do not
  mutate git" constraint in the dev spawn is unchanged).

## Fail Criteria

- The branch creation command does not state the sprint branch as the explicit base.
- The worktree-add command appears after the dev spawn (too late).
- The creation is delegated to the dev agent.
- No rationale or citation of the diff-range doctrine is present.
- The `worktree_path` is passed to the dev agent without the worktree actually being
  created first.

## Verification Method

**Inspection of workflow text.**

1. Read `skills/momentum/skills/conductor/workflow.md` at the STAGE-1 DEV SPAWN block
   inside step 2.1.3. Confirm the branch-and-worktree creation action is present, appears
   before agent resolve/spawn, states `sprint/{{sprint_slug}}` as the base, and cites
   the diff-range reference.
2. Confirm the dev spawn constraint text still includes "Do not mutate git" — unchanged.
