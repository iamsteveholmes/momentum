# Eval: Phase 0 prefilter invocation before classification

## Scenario

Given a triage session with 3 incoming items and a populated stories index (`.momentum/stories/index.json` contains 10+ non-terminal stories), the skill is invoked and reaches the classification phase.

## Expected behavior

Before producing any classification output, the orchestrator runs:

```
python3 skills/momentum/scripts/momentum-tools.py triage prefilter \
  --items-json '...' \
  --stories-index .momentum/stories/index.json
```

The output (shortlists and similarity matrix) is captured and stored as `{{prefilter_output}}` before Phase 1 clustering begins.

The orchestrator does NOT skip Phase 0 even when the batch is small (≤5 items). Phase 0 always runs.
