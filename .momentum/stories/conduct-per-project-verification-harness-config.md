---
title: Configure per-project verification-harness execution_surfaces (non-markdown projects only)
story_key: conduct-per-project-verification-harness-config
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Configure per-project verification-harness execution_surfaces (non-markdown projects only)

## Classification
Blocking level: **later** · found by discovery lenses: e2e-runnability


## What
momentum/verification-harness.json sets every execution_surface (skill-instruction, agent-definition, rule-hook, script-code, script-cli, backend, app-ui, research-spike, specification, config-structure) to 'skip', the project[] array is empty, and defaults.env startup/readiness_probe are empty. The e2e-validator reads this harness to pick a driver per change_type, but with all surfaces 'skip' no scenario is ever executed. There is no per-project override configuring real drivers (Maestro/Playwright for app-ui, curl/bash for backend, cmux for scripts) or the startup/readiness env they need.

## Why it's needed (what breaks without it)
For Momentum's own markdown/bash repo, 'skip' is the legitimate carve-out (no app to run) — so this does NOT block conduct on this repo. But for any project with app-ui/backend/script stories, the build would report E2E results without ever running the app — a silent verification gap. This is per-project scaffolding the developer configures when conduct is used on a real product repo, not a conduct-engine defect.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
