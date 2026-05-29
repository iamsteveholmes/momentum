# Eval: Intake Skill Runs on Main Working Tree Without Worktree Isolation

## Purpose

Verify that the `momentum:intake` skill never invokes worktree-isolation tooling
during execution — and that the captured stub file lands on the main working tree
immediately, with no merge or recovery step required.

## Scenario

A developer is mid-conversation reviewing sprint triage findings. They say:

> "While we're here — we should track a story for improving the sprint-dev retry
> logic when a story AVFL check fails. Orbiters have been running the full AVFL
> pass twice on failures because the retry path doesn't record the first result.
> Medium priority, put it in the sprint-execution epic."

The developer then invokes `/momentum:intake`.

## Expected Behaviors

### B1: No Worktree Isolation

During the entire intake run, the skill's tool-call sequence must contain **zero**
invocations of:

- `EnterWorktree`
- `ExitWorktree`
- Any Bash command containing `git worktree add`, `git worktree remove`, or
  `git worktree prune`

The skill runs exclusively in the current (main) working tree from the moment it is
invoked to the moment it completes. A reviewer scanning the tool-call sequence must
find no worktree-entry or worktree-exit calls anywhere in the run.

### B2: Stub Lands on Main Working Tree

After the run completes, the stub file at `.momentum/stories/<slug>.md` is:

- Present in the main working tree checkout (i.e., visible without checking out any
  branch or navigating into any `.worktrees/` subdirectory)
- Written via the standard `Write` tool targeting the `.momentum/stories/` path
  directly — not written to a branch-scoped path first and then merged

A reviewer can confirm this by checking that the write target path did not start
with `.worktrees/` and that the file exists in the working directory immediately
after the run, not "pending a merge".

### B3: story-add Is the Sole Index Mutation

The `.momentum/stories/index.json` file is mutated exactly once during the run, via:

```
python3 skills/momentum/scripts/momentum-tools.py sprint story-add ...
```

No direct edits to `stories/index.json` occur. No other tool call modifies
`stories/index.json`. The `story-add` call is the only write to the index.

### B4: Zero Manual Recovery Steps Required

After the run completes:

- The stub file is present on main — no copy, cherry-pick, or re-registration required
- The index entry is present — no separate `story-add` invocation is needed after the run
- The developer can immediately run `momentum-tools sprint list` (or equivalent) and
  see the new story in the backlog without any follow-up action

The run is self-contained: one invocation → stub written → index updated → done.

## What Should NOT Happen

- `EnterWorktree` call at any point during the run
- `ExitWorktree` call at any point during the run
- Any Bash command containing `git worktree`
- The stub file written to a path under `.worktrees/`
- A post-run instruction to the developer to "merge the stub" or "copy the stub file"
- Multiple mutations to `stories/index.json` (e.g., a branch-local write followed by
  a merge-time re-application)

## Pass Criteria

All of B1–B4 must be satisfied. A failure on any behavioral expectation is a failing
eval. Specifically:

- **B1 fail:** Any `EnterWorktree`, `ExitWorktree`, or `git worktree` call appears
  in the tool sequence.
- **B2 fail:** The stub file path starts with `.worktrees/` or the file requires a
  merge or branch checkout to become visible on main.
- **B3 fail:** `stories/index.json` is written by any tool other than the `story-add`
  CLI call, or is written more than once.
- **B4 fail:** The run's output instructs the developer to perform a manual recovery
  step (copy, re-register, cherry-pick, etc.) to make the stub visible or indexed.
