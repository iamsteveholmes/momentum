---
title: Resolve spec §13 Q6 — Conductor as a separate skill vs. sprint-dev's top-level session (who legitimately runs git push)
story_key: conduct-resolve-invocation-model-q6
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: exploration
priority: critical
depends_on: []
---

# Resolve spec §13 Q6 — Conductor as a separate skill vs. sprint-dev's top-level session (who legitimately runs git push)

## Classification
Blocking level: **blocks-invocation** · found by discovery lenses: entry-point, engine-hollows, spec-audit, e2e-runnability
**This is a DECISION to resolve (run via momentum:decision), not a build story — it gates the invocation wiring.**

## What
Spec §13 open question 6 is unresolved and is THE architectural fork that determines how conduct is invoked. The Conductor must own git mutation (commits, merges, the approve-time git push), spawn subagents, and hold a long live end-gate conversation — those are top-level-session authorities, and orchestrator-purity rules forbid non-top-level skills from writing files / running git directly. It must be decided whether: (a) the Conductor IS the top-level session that sprint-dev's workflow becomes (sprint-dev/workflow.md rewritten per §12 to embody the Conductor build phase), or (b) conduct is a separately-invoked top-level skill with its own command. The built artifact is a standalone `conductor` skill that no caller invokes, while spec §10/§12 say the redesign REPLACES the build phase inside sprint-dev/workflow.md — the artifact and the spec's stated integration point disagree.

## Why it's needed (what breaks without it)
Every downstream invocation decision hangs off this: whether the command file points at a new skill or sprint-dev is repointed/retired; whether the standalone skill's pre-flight + end-gate are duplicative; and whether the Conductor can legitimately run git push without violating orchestrator-purity. Building the command wrapper before resolving this risks wiring the wrong entry point and leaving sprint-dev/workflow.md as an orphaned parallel implementation of the superseded wave model.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
