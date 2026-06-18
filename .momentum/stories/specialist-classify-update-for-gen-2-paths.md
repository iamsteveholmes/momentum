---
title: Specialist-classify update for gen-2 paths
story_key: specialist-classify-update-for-gen-2-paths
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
depends_on: []
touches: []
---

# Specialist-classify update for gen-2 paths

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want momentum-tools specialist-classify to resolve composed-file paths in .claude/guidelines/agents/ rather than the plugin agents directory,
so that the deterministic lookup targets the project's composed output and not Momentum's shipped specialists.

## Description

Update momentum-tools specialist-classify to resolve composed-file paths in .claude/guidelines/agents/ rather than the plugin agents directory. The deterministic lookup must target the project's composed output, not Momentum's shipped specialists.

**Pain context:** specialist-classify is the programmatic lookup that maps a role+domain to a concrete file path. If it still points at the plugin directory after gen-2 is shipped, every consumer of specialist-classify (sprint-planning assignment, sprint-dev spawning, any tooling) will get wrong paths and load stale gen-1 agents even when composed gen-2 files exist.

## DEC-038 Alignment

Per **DEC-038** (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture), the
gen-2 composed files this lookup resolves to are **project-scoped composed agents**, each produced by
the build-guidelines / agent-builder pipeline as **base body + constitution (Tier 1) + per-agent
manifesto (Tier 2)**. The manifesto is the agent's **stable diagnostic table** — a per-role×domain map
of observable developer symptoms to the exact `wiki-query` KB lookup, plus the stack facts that scope
it (it is NOT a per-sprint/per-story context overlay). This shapes specialist-classify's resolution in
two ways:

- **Project scope is part of the key.** Agents are project-scoped (a nornspun agent is not a Momentum
  agent), and the composed output lives under the *project's* `.claude/guidelines/agents/`. Resolution
  must therefore target the composed agents of the project it runs in, never Momentum's shipped (gen-1)
  specialists — which is the core of this story.
- **What resolution returns is a composed agent, not a bare body.** A returned gen-2 path points at a
  fully composed file whose manifest is the per-agent diagnostic table scoped to that project's KB(s)
  (DEC-018 wiki-query extended to multiple per-project KBs). specialist-classify itself is the
  deterministic path lookup — it does not read or interpret the manifesto — but its contract must stay
  consistent with this composition model so consumers always load the project's composed gen-2 agent.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- specialist-classify resolves .claude/guidelines/agents/{role}-{domain}.md as the primary lookup path
- When a composed file exists at the gen-2 path, specialist-classify returns that path
- When a composed file is absent, the fallback behavior is defined and documented
- The plugin agents directory is NOT returned as a primary path by specialist-classify after this change
- All consumers of specialist-classify receive correct gen-2 paths
- Resolution is project-scoped: the gen-2 path returned points at the running project's composed agent
  (under that project's .claude/guidelines/agents/), never another project's or Momentum's shipped
  specialists — consistent with DEC-038's project-scoped agents
- The path returned is a DEC-038 composed agent (base body + constitution + per-agent diagnostic-table
  manifesto, scoped to the project's KB); specialist-classify's resolution contract stays consistent
  with this composition model even though the lookup itself does not read or interpret the manifesto

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- DEC-038 — Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture
  (`_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`).
  This story is listed under `stories_affected` and is Phase 2 ("Pipeline consumes manifesto + multi-KB").
  Defines the gen-2 composition model (base body + constitution + per-agent diagnostic-table manifesto)
  and project-scoped, multi-KB agents that the gen-2 paths resolved here point at.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
