---
title: Wire conduct stages 1–2: per-story dev spawn + concurrent QA/code-review fan-out
story_key: conduct-per-story-build-review-dispatch
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: critical
depends_on: []
---

# Wire conduct stages 1–2: per-story dev spawn + concurrent QA/code-review fan-out

## Story
Follow-up from the conduct core-build slice (`sprint-2026-06-02-conduct-core`). Wire conduct stages 1–2: per-story dev spawn + concurrent QA/code-review fan-out.

## Why this exists
THE blocker to conduct being runnable. The core-build slice (sprint-2026-06-02-conduct-core) left the per-story build (stage 1: dev spawn) and review (stage 2: concurrent QA + code-review fan-out) dispatch as a labelled HOLLOW in conductor/workflow.md step 2.1.3. The fix loop (stage 3) downstream is live but has nothing to consume. Until this lands, conduct cannot build-and-review a story on its own.

## What's needed
- Fill the stage-1 dev spawn (individual-agent, scoped to the story worktree, no git mutation by the agent).
- Fill the stage-2 concurrent fan-out: qa-reviewer (per-story contract) + the bmad-code-review adapter, read-only, returning normalized findings.
- Feed their findings into the live stage-3 fix loop. Preserve per-story isolation and the Conductor-owns-git invariant.
- After this, run a real end-to-end conduct build to validate (DEC-035 D8 / Gate 4).

## References
- Conduct spec §3 (per-story pipeline) and §4 (QA + code review + fix): _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- conductor/workflow.md step 2.1.3 (the HOLLOW marker)
- DEC-035, DEC-036
