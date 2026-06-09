---
title: Clean up dead agent routing entries and add existence validation to agent resolve
story_key: conduct-cleanup-dead-agent-paths-and-validate-resolve
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: low
depends_on: []
---

# Clean up dead agent routing entries and add existence validation to agent resolve

## Classification
Blocking level: **cleanup** · found by discovery lenses: engine-hollows, agent-deps, e2e-runnability


## What
momentum/agents.json defaults map architect, pm, sm to agent body files that do NOT exist (verified 2026-06-06: `skills/momentum/agents/` contains dev.md, dev-build.md, dev-frontend.md, dev-skills.md, qa-reviewer.md, e2e-validator.md, analyst.md, researcher.md, ux.md — so ONLY architect/pm/sm are dead; ux/analyst/researcher DO exist and must NOT be deleted or recreated). cmd_agent_resolve reads agents.json and returns the mapped path with NO Path.exists() check, so `agent resolve --role architect` returns success:true pointing at a missing file. Spec §10/§12 call this P2 cleanup: create the bodies or delete the dead entries, and ideally add existence validation so a broken path fails fast instead of silently mis-spawning.

## Why it's needed (what breaks without it)
NOT a conduct-run blocker — conduct resolves only dev (via --touches, which falls back to dev), qa-reviewer, and e2e-validator, all of which exist and resolve cleanly. But the dead entries are a latent trap: any future routing-table change or --touches pattern mapping to these roles would silently spawn a missing agent body with no early signal. Defense-in-depth + spec-tracked cleanup.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
