---
title: Build AVFL-on-merge as a Workflow over the 3-dot merged diff (replace the interim prose pass)
story_key: avfl-merge-review-as-workflow
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Build AVFL-on-merge as a Workflow over the 3-dot merged diff (replace the interim prose pass)

## Story
Follow-up from the conduct core-build slice (`sprint-2026-06-02-conduct-core`). Build AVFL-on-merge as a Workflow over the 3-dot merged diff (replace the interim prose pass).

## Why this exists
conduct's Phase 3 currently runs an interim prose approximation over a touches-union diff. The spec calls for a dynamic Workflow (avfl-merge-review) over the precise 3-dot merge-base diff, with the retained lens taxonomy + declining-skepticism auto-fix loop.

## What's needed
- Implement avfl-merge-review as a Workflow under the avfl skill, fed the merge-base 3-dot diff + the --no-ff merge-commit list.
- Return the typed CLEAN | NON_CONVERGENT result the Conductor consumes; route integration code findings to the directed fixer (dev fix-mode).
- Replace the interim touches-union prose pass in conductor/workflow.md step 3.

## References
- Conduct spec §5 (AVFL — reviewer of the merge): _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- conductor/workflow.md step 3 (INTERIM NOTE)
