---
title: Create the /momentum:conduct entry-point command file (and resolve the conduct-vs-conductor name)
story_key: conduct-entry-point-command
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: critical
depends_on: []
---

# Create the /momentum:conduct entry-point command file (and resolve the conduct-vs-conductor name)

## Classification
Blocking level: **blocks-invocation** · found by discovery lenses: entry-point, engine-hollows, agent-deps, e2e-runnability, spec-audit, planning-handoff


## What
There is no command file exposing the Conductor as a slash command. skills/momentum/commands/ has thin one-line wrappers for every other skill (sprint-dev.md = 'Invoke the momentum:sprint-dev skill and follow it exactly.') but no conduct.md or conductor.md. The skill directory is `conductor` (natural Skill name momentum:conductor) yet the goal and DEC-035 call the capability `conduct` — so /momentum:conduct binds to nothing. A command file must be created AND the canonical command name resolved (the literal command name is never specified anywhere in the spec). This is downstream of Q6: if sprint-dev embodies the Conductor, the 'command' may be a repoint of sprint-dev rather than a new file.

## Why it's needed (what breaks without it)
The literal task goal — a developer typing /momentum:conduct — is impossible with no command file. Even if a developer guesses, the conduct/conductor name mismatch means /momentum:conduct does not resolve. This is the first concrete artifact between today and an invocable conductor.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
