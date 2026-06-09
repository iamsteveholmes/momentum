---
title: Exercise the conduct escalation machinery end-to-end before trusting it
story_key: exercise-conduct-escalation-machinery-end-to-end
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Exercise the conduct escalation machinery end-to-end before trusting it

## Story
Drive the stakes-and-timing escalation machinery through its branches with real findings/evals, since it has never actually fired on a per-story mid-flight finding.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): the stakes-and-timing engine fired exactly once (post-merge AVFL only); of 105 findings, 104 were routine and 1 was high-blast-radius-architecture, with `timing_tier` 100% end-gate-expanded. The per-story mid-flight branch was never triggered by a real finding, and the stage-3 fix-loop verification was inspection-only. The machinery is largely untested in practice.

## What's needed
- A runtime/eval test drives a real stakes-class finding through the mid-flight loop.
- The end-gate-expanded vs mid-flight branch is exercised with both timing tiers.
- The bound-exhausted (BLOCKED) and escalated dispositions are each driven through the loop at least once.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related: `conduct-stakes-timing-escalation-mechanism` (done), `stakes-classification-rubric` (done), `stage3-fix-loop-via-directed-dev` (done)
