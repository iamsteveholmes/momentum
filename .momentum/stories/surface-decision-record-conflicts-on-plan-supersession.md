---
title: Surface decision-record conflicts when a new plan supersedes prior commitments
story_key: surface-decision-record-conflicts-on-plan-supersession
status: backlog
epic_slug: momentum-assessment-decision-pipeline
story_type: feature
priority: medium
depends_on: []
---

# Surface decision-record conflicts when a new plan supersedes prior commitments

## Story
When a new plan touches an area governed by a prior decision (DEC), the agent must surface the conflict and propose a supersession before proceeding, and record the supersession as a decision amendment.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): Msgs 19–27, the developer interrupted the agent mid-action ("[Request interrupted by user for tool use]") to force reconciliation between the new conduct plan and prior committed decisions (DEC-028 beads, DEC-032 Gas City) before letting it proceed — "we had plans to integrate beads and gascity. I think this plan is a bit of a replacement." The agent was building forward without reconciling against the standing decision record; the human had to catch it.

## What's needed
- When a new plan touches an area covered by a prior DEC, the agent surfaces the conflict and proposed supersession before proceeding.
- The supersession is recorded as a decision amendment.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related (dedup, adjacent): `plan-audit` Spec Impact gate (covers PRD/arch/UX impact, not DEC conflicts), `decision-skill` (done)
