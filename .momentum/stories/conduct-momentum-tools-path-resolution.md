---
title: Ensure momentum-tools is resolvable in the conductor's execution environment
story_key: conduct-momentum-tools-path-resolution
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: critical
depends_on: []
---

# Ensure momentum-tools is resolvable in the conductor's execution environment

## Classification
Blocking level: **blocks-run** · found by discovery lenses: e2e-runnability


## What
The conductor workflow calls bare `momentum-tools sprint status-transition|activate`, `momentum-tools agent resolve` ~11 times. `which momentum-tools` returns 'not found' — there is no PATH shim, mise shim, or symlink for it; the actual file is skills/momentum/scripts/momentum-tools.py (python3 hashbang). NOTE: bare `momentum-tools` is the project-wide convention used by EVERY working skill (sprint-dev, quick-fix, sprint-planning, retro, intake, epic-grooming), so this is not a conduct-specific bug — it is an environment precondition for the whole practice (the developer's runtime evidently resolves it; the subagent shell does not). The fix is to guarantee a shim on PATH (or, secondarily, normalize the convention to the python3 .../momentum-tools.py form impetus already uses).

## Why it's needed (what breaks without it)
Every status transition (in-progress/review/verify/done/closed-incomplete), the activate-guard remediation, and every agent/role resolution depends on this binary resolving. If it is unresolvable in the run environment, the conductor cannot transition a single story or resolve a single agent — the build cannot advance past launching the first story, on any project.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
