---
title: Register the conductor skill: confirm user-invocable frontmatter and force a plugin/marketplace refresh so it surfaces
story_key: conduct-register-skill-and-refresh-cache
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: high
depends_on: []
---

# Register the conductor skill: confirm user-invocable frontmatter and force a plugin/marketplace refresh so it surfaces

## Classification
Blocking level: **blocks-invocation** · found by discovery lenses: entry-point, agent-deps, e2e-runnability, spec-audit


## What
conductor/SKILL.md frontmatter has only name/description/model/effort — no explicit user-invocable flag (structurally matching other user-invocable skills that rely on the default). More importantly, the conductor is NOT in the live available-skills registry the session sees (assessment/decision/retro/triage/sprint-dev are; conductor is absent), indicating the active plugin/marketplace cache predates the merge. A version bump in plugin.json + /plugin marketplace update momentum + session restart is required for the skill to become discoverable at all. If conduct is intended to be directly user-invocable (pending Q6), the frontmatter should also declare that explicitly per the dev guide.

## Why it's needed (what breaks without it)
The skill exists on disk (v0.25.0 source) but is not in the registry the session can reach, so neither /momentum:conductor nor the Skill tool can invoke it without a marketplace refresh. Even a correct command file won't dispatch until the skill registers.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
