---
title: Wire the end-gate 'request changes' path to spawn fixers (the change-workflow from the gate)
story_key: conduct-endgate-request-changes-redispatch
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Wire the end-gate 'request changes' path to spawn fixers (the change-workflow from the gate)

## Story
Follow-up from the conduct core-build slice (`sprint-2026-06-02-conduct-core`). Wire the end-gate 'request changes' path to spawn fixers (the change-workflow from the gate).

## Why this exists
The end-gate can acknowledge a change request but cannot yet act on it. The change-workflow (the same machinery as the per-story fix loop) needs a gate-side entry point.

## What's needed
- From the end-gate, parse the developer's change request into discrete fixer items and run one change-workflow over them (bounded), then re-render the report.
- Reuse the directed-fixer machinery; no developer prompt inside the loop.

## References
- Conduct spec §8 (the change-workflow): _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- conductor/workflow.md step 5 (out-of-scope note)
