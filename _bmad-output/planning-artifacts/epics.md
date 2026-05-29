---
title: Epics — Derived Index
status: derived
authoritative_source: _bmad-output/planning-artifacts/epics.json
archived_narrative: _bmad-output/planning-artifacts/archive/epics-pre-2026-05.md
last_updated: '2026-05-28'
decision: DEC-034
---

# Epics — Derived Index

> **This file is a derived index only.** The authoritative source is [`epics.json`](epics.json).
>
> Per DEC-034 (Epic-Layer Consolidation, 2026-05-25), the dual `features.json` + categorical-epics
> architecture is unified into a single `epics.json` with `lifecycle` and `audience` properties.
>
> - **For LLM and programmatic access:** Read `_bmad-output/planning-artifacts/epics.json`
> - **For human-readable view:** Run `/momentum:canvas` — Epics lens (port 3456)
> - **For the pre-migration narrative:** See `_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md`

## Epic Summary

As of the B1 migration (sprint-2026-05-26), the unified epic layer contains:

- **23 finite-lived epics** — migrated from `features.json` (lifecycle: finite-lived, audience: user)
- **1 long-lived epic** — `ad-hoc` (canonical residue catcher, lifecycle: long-lived, audience: internal)
- **18 categorical epics dissolved** — stories re-homed to appropriate finite-lived epics

All 419 stories have been assigned to a valid epic. Zero orphans. The bidirectional invariant
(stories/index.json ↔ epics.json) is enforced by the migration script and will be maintained by
momentum:epic-grooming after B4 ships.

## Epics (brief index)

See `epics.json` for full entries with `lifecycle`, `audience`, `value_analysis`, `system_context`,
`acceptance_conditions`, `stories[]`, `stories_done`, `stories_remaining`, and `notes`.

| epic_slug | name | lifecycle | audience |
|---|---|---|---|
| momentum-agent-composition-pipeline | Agent Composition Pipeline | finite-lived | user |
| momentum-agent-role-contracts | Agent Role Contracts | finite-lived | user |
| momentum-agent-spawn-orchestration | Agent Spawn Orchestration | finite-lived | user |
| momentum-assessment-decision-pipeline | Assessment to Decision to Story Traceability Pipeline | finite-lived | user |
| momentum-backlog-refinement | Backlog Refinement and Epic Taxonomy | finite-lived | user |
| momentum-canvas | Momentum Cycle — Three-Lens Live Dashboard | finite-lived | user |
| momentum-deep-research-pipeline | Deep Research Pipeline | finite-lived | user |
| momentum-feature-taxonomy-maintenance | Feature Taxonomy Maintenance (pending B4 rename to epic-grooming) | finite-lived | user |
| momentum-gherkin-separation | Black-Box Behavioral Specification via Gherkin | finite-lived | user |
| momentum-impetus-experience | Impetus: Session Host and Practice Companion | finite-lived | user |
| momentum-impetus-session-orientation | Impetus Session Orientation | finite-lived | user |
| momentum-model-routing-strategy | Model and Effort Routing Defaults | finite-lived | user |
| momentum-practice-distillation | Lightweight Practice Artifact Distillation | finite-lived | user |
| momentum-practice-flywheel | Practice Improvement Flywheel | finite-lived | user |
| momentum-practice-knowledge-base | Practice Knowledge Base | finite-lived | user |
| momentum-protocol-based-integration | Swappable Protocol Implementations | finite-lived | user |
| momentum-provenance-chain | Artifact Provenance and Staleness Detection | finite-lived | user |
| momentum-quality-gates-enforced | Quality Gates — AVFL, Code Review, and Retro | finite-lived | user |
| momentum-quick-fix-workflow | Single-Story Tactical Workflow | finite-lived | user |
| momentum-sprint-orchestration | Sprint Execution — Concurrent Agents + Quality Gates | finite-lived | user |
| momentum-sprint-planning-to-ready | Sprint Planning — Backlog to Ready Sprint | finite-lived | user |
| momentum-sprint-retro | Sprint Retrospective — Transcript Audit and Sprint Closure | finite-lived | user |
| momentum-startup-performance | Sub-2s Session Startup (NFR20) | finite-lived | user |
| ad-hoc | Ad-Hoc Work | long-lived | internal |

## Migration Log

The `_migration` key in `epics.json` contains the full provenance log including:
- Dissolved categorical epics and their target re-home epic
- Long-lived epics and their justification
- Story re-homing count

## Prior Narrative

This file's prior narrative content (18 categorical epic definitions, Requirements Inventory,
FR Coverage Map, full story breakdowns per sprint-2026-03-20 through sprint-2026-05-14) is archived at:
`_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md`

Choice documentation per AC7: retire-and-stub was chosen (not restructured narrative view) because
the canvas provides the human reading surface and `epics.json` is the authoritative store.
Documented in `epics.json` `_migration.notes`.
