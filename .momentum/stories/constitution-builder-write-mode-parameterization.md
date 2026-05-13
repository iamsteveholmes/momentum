---
title: Constitution-Builder Write-Mode Parameterization — In-Place SKILL vs Composed Agent File vs Standalone Constitution
story_key: constitution-builder-write-mode-parameterization
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches:
  - skills/momentum/skills/constitution-builder/SKILL.md
  - skills/momentum/skills/constitution-builder/workflow.md
---

# Constitution-Builder Write-Mode Parameterization

<!-- INTAKE STUB: Captured during feature-grooming pass 2026-05-12. Run
     momentum:create-story to enrich before development. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want `momentum:constitution-builder` to accept a `write_mode` parameter that selects between writing the constitution block into an existing SKILL.md, writing it as a standalone composed agent file at a target path, or writing the universal Tier 1 constitution,
so that the same KB-synthesis logic powers both direct-invoke skills (frontend-dev style) and sprint-dev subagents (composed agent file style) without duplicating implementation.

## Description

`momentum:constitution-builder` today writes its output (`## Permissions` + `## Standing Rules` + `## Quick Routing`) **into** an existing SKILL.md at a target path. That is one of three write contexts the system needs:

1. **`in_place_skill`** (current behavior) — write the constitution sections into an existing `SKILL.md`. Used when the agent IS a skill invoked by name (e.g., the project-local `frontend-dev` SKILL.md we hand-rolled).
2. **`composed_agent_file`** (new) — write a standalone agent file at `.claude/guidelines/agents/{role}-{domain}.md` whose body = the constitution sections + an imported base body from `skills/momentum/agents/{role}.md`. Used when the agent is spawned as a subagent by sprint-dev / retro / AVFL.
3. **`standalone_constitution`** (new) — write the universal Tier 1 constitution at `.claude/guidelines/constitution.md` — universal trigger tables, wiki-query interface block, critical rules. Loaded as hot context for every spawned agent.

The workflow phases (Elicit → Permission Scoping → Standing Rules → KB Audit → Routing Generation → Review → Write) stay the same. Only the **write target and the final assembly step** differ. The synthesis work is shared across all three modes.

**Pain context:** Without this parameterization, `build-guidelines-skill` would have to re-implement the KB-synthesis logic that already lives in `constitution-builder`. That's textbook duplication. Parameterization is the cheap fix.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Rough draft ACs captured from grooming conversation:

- `constitution-builder` accepts a `write_mode` argument with values: `in_place_skill`, `composed_agent_file`, `standalone_constitution`
- `in_place_skill` mode preserves the current behavior — no regression
- `composed_agent_file` mode produces a file at the specified path whose body includes:
  - A `## Project Guidelines — {Stack} ({Date})` block with critical rules and reference-doc pointers
  - The full unchanged base body content from `skills/momentum/agents/{role}.md`
  - Proper frontmatter (`name`, `model`, `effort`, `tools`)
- `standalone_constitution` mode produces a universal Tier 1 constitution including the wiki-query interface block (per `wiki-query-interface-block-for-hot-constitution` story)
- The write target path is provided as an argument; the skill does not infer the path from the mode
- The Elicit phase asks "where should this constitution be written?" only when the developer hasn't supplied the path
- Workflow phases that are identical across all three modes (KB audit, routing generation) are not duplicated in the workflow.md

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- `momentum:constitution-builder` SKILL.md and workflow.md (current behavior)
- `build-guidelines-skill` story (the primary consumer of new modes)
- `wiki-query-interface-block-for-hot-constitution` (defines what `standalone_constitution` mode must include)
- DEC-018 — wiki-query as Tier 3 cold KB interface
- DEC-013 — universal agent model
- DEC-001 — three-tier agent guidelines architecture

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._
