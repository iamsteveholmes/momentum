# Eval: Namespace and Stale-Subcommand Regression Guard

## Setup

Static/grep-based check against `skills/momentum/skills/sprint-planning/workflow.md` and
`skills/momentum/scripts/momentum-tools.py`. No live session required.

## Expected Behavior

1. Every skill invocation line in `sprint-planning/workflow.md` (matched by patterns like
   `Invoke the \`...\` skill`, `` Spawn `...` ``, `` Re-spawn `...` ``, or `invoke \`...\`` )
   names a skill prefixed with `momentum:` (e.g. `momentum:avfl`, `momentum:create-story`,
   `momentum:agent-guidelines`, `momentum:build-guidelines`, `momentum:architecture-guard`).
   Zero bare (un-namespaced) skill names remain.
2. Every `momentum-tools sprint <subcommand>` reference in the same file names a
   subcommand actually registered via `sprint_sub.add_parser(...)` in `momentum-tools.py`:
   `activate`, `plan`, `ready`, `story-add`, `story-approve`, `story-set-contract`,
   `compute-verification-method` (the full set referenced by this workflow).
3. Neither `sprint-current` nor `sprint-stories` (the historical stale subcommand names)
   appears anywhere in the workflow file.

## Verification

Run these checks against the worktree:

```bash
# 1. No bare skill invocations (every hit below must show a momentum: prefix)
grep -n "Invoke the \`\|Spawn \`\|Re-spawn \`" skills/momentum/skills/sprint-planning/workflow.md

# 2. Every referenced subcommand resolves
grep -oE "momentum-tools sprint [a-z-]+" skills/momentum/skills/sprint-planning/workflow.md | sort -u
# cross-check each against:
grep -n 'sprint_sub.add_parser' -A0 skills/momentum/scripts/momentum-tools.py

# 3. Stale subcommand names are absent
grep -n "sprint-current\|sprint-stories" skills/momentum/skills/sprint-planning/workflow.md
# must produce no matches (exit code 1)
```

All three checks must pass with zero disqualifying matches.
