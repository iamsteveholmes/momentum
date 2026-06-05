---
title: Wire a caller and a discovery route into the Conductor (sprint-dev rewrite and/or Impetus dispatch)
story_key: conduct-wire-caller-and-discovery
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: high
depends_on: []
---

# Wire a caller and a discovery route into the Conductor (sprint-dev rewrite and/or Impetus dispatch)

## Classification
Blocking level: **blocks-invocation** · found by discovery lenses: entry-point, engine-hollows, e2e-runnability, agent-deps


## What
The Conductor is built in complete isolation with zero callers and zero discovery path. (a) sprint-dev/workflow.md still contains the OLD wave-loop architecture (sprint_waves primary ordering, 'Phase 2 — Dev Wave', per-wave done barriers, global Phase 4 AVFL stop-gate) — it was only edited to repoint code-review calls to the bmad-code-review adapter, never rewritten to embody or invoke the Conductor (grep 'conductor' in sprint-dev/workflow.md returns nothing). (b) Impetus (impetus/SKILL.md + the .claude/rules/impetus.md always-on persona) has no dispatch entry routing 'run the sprint build' to the Conductor — its 'where state lives' table and dispatch behavior point only at the legacy sprint-dev path. So a developer running /momentum:sprint-dev or asking Impetus to 'continue the sprint' gets the stale wave loop, not the Conductor. Resolution depends on Q6 (rewrite sprint-dev to be the Conductor, OR add an Impetus/command route to a separate conduct skill).

## Why it's needed (what breaks without it)
The new DEC-035/036 build engine is dead code with no path leading into it. Even with a command file, the build phase the Conductor owns is still served by the stale sprint-dev wave loop, and the practice's front door (Impetus) never surfaces conduct. Both reachability and discoverability are part of 'a developer can run it.'

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
