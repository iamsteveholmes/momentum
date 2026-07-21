# Eval: AVFL Checkpoint Invokes the Namespaced Skill

## Setup

A `momentum:create-story` session reaches Step 8 (Run AVFL checkpoint on the story file)
with a fully-written story file ready for validation.

## Expected Behavior

1. The workflow invokes the skill named `momentum:avfl` — not the bare name `avfl` — to
   run the checkpoint validation.
2. The invocation succeeds and returns a valid AVFL result (`CLEAN`, `CHECKPOINT_WARNING`,
   or `GATE_FAILED`) rather than a tool-use error.
3. No `Unknown skill: avfl` error appears anywhere in the run's tool-use trace.

## Verification

```bash
grep -n "Invoke the \`avfl\`" skills/momentum/skills/create-story/workflow.md
# must produce no matches (exit code 1) — the bare form must not exist

grep -n "momentum:avfl" skills/momentum/skills/create-story/workflow.md
# must match the Step 8 invocation line
```

A create-story run that reaches the Step 8 AVFL checkpoint produces zero
`Unknown skill: avfl` errors in `.momentum` error logs.
