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

Per **DEC-026 D4**, `momentum:constitution-builder` is reworked to generate **domain knowledge only**: project-specific embedded facts (stack, conventions, architectural patterns) and KB-sourced context (wiki lookups via DEC-018 wiki-query interface). It no longer generates Permissions, Standing Rules, or Quick Routing — those responsibilities move to `agent-builder-skill` (see story `agent-builder-skill`).

The constitution's output is scoped to:
- **Embedded facts** — stack identity, key conventions, architectural constraints that every agent in this project needs
- **KB-sourced context** — wiki-query lookups that surface project-specific knowledge at agent spawn time
- **Wiki-query interface block** (DEC-018) — shared infrastructure available to all agents; stays in constitution as a cross-cutting concern

**What moves out of constitution-builder:**
- `## Quick Routing` — moves to `agent-builder-skill` (agent-specific routing per role × domain)
- Agent-specific `## Permissions` — moves to `agent-builder-skill`
- Agent-specific `## Standing Rules` — moves to `agent-builder-skill`

Cross-cutting permissions and standing rules that apply to every agent (e.g., "never commit secrets", "always use conventional commits") remain in the constitution.

The `write_mode` parameter still governs where the output is written (`in_place_skill`, `composed_agent_file`, `standalone_constitution`), but the content written is now domain knowledge only rather than the full agent configuration.

**Pain context:** Per DEC-026 D5, the canonical pipeline is constitution-builder (Tier 1, once) → agent-builder × N (Tier 2, per role × domain). Constitution-builder must be narrowed to domain knowledge so it stays stable and slow-changing; per-agent routing is fast-changing and belongs in agent-builder.

> **Scope note:** Routing generation moves to `agent-builder-skill` (story: `agent-builder-skill`). That story must be activated before or alongside this one.

## DEC-038 Alignment

**DEC-038** ratifies that an agent's per-role×domain routing is its **manifesto** — a *stable diagnostic table* mapping observable developer symptoms to the exact `wiki-query` lookup for each. That table is owned **per agent**, at the manifesto/`agent-builder` layer. This sharpens the constitution-vs-routing split this story already encodes:

- **The shared constitution must NOT own per-agent routing.** A project-shared `## Quick Routing` table is meaningless for a `pm` or `architect` — a shared Compose/Kotest routing table only makes sense for a frontend specialist. Per-agent routing (the diagnostic table) belongs in the per-agent manifesto / composed-agent layer, not in any write mode that emits shared, project-wide content.
- **Write modes must respect the split.** Whatever a write mode emits for the shared constitution carries only project-wide, agent-agnostic content (embedded facts, KB-sourced context, the shared wiki-query interface). The per-agent diagnostic table is layered on by the manifesto/`agent-builder` step, not by constitution-builder.
- **`## Quick Routing` ownership is reconciled here**, consistent with the sibling story `constitutionmd-generation-acceptance-criteria`: shared content stays project-wide; per-agent routing is per-agent (the manifesto). Per DEC-038, `wiki-query` (DEC-018) is also extended to address multiple per-project KBs, and agents are project-scoped — so the KB-sourced context a constitution emits is scoped to *this* project's KB(s).

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready. ACs below reflect DEC-026 D4 scope (domain knowledge only); prior ACs assuming Permissions + Standing Rules + Quick Routing generation have been superseded._

Rough draft ACs (updated per DEC-026 D4, source: triage handoff 2026-05-16):

**write_mode parameter**
- `constitution-builder` accepts a `write_mode` argument with values: `in_place_skill`, `composed_agent_file`, `standalone_constitution`
- The write target path is provided as an argument; the skill does not infer the path from the mode
- The Elicit phase asks "where should this constitution be written?" only when the developer has not supplied the path

**Domain knowledge output (all modes)**
- The constitution output contains an embedded facts section covering stack identity, key conventions, and architectural constraints for the project
- The constitution output contains a KB-sourced context section populated via wiki-query lookups (DEC-018 interface) at generation time
- The constitution output includes the wiki-query interface block (DEC-018) as shared infrastructure for all agents
- The constitution output does NOT contain `## Quick Routing` — routing is not generated by constitution-builder
- Per DEC-038, `## Quick Routing` ownership is reconciled: any per-role×domain routing (the agent's diagnostic table — observable symptom → exact `wiki-query`) is owned per-agent at the manifesto/`agent-builder` layer and is NOT emitted into shared, project-wide constitution content by any write mode (consistent with sibling story `constitutionmd-generation-acceptance-criteria`)
- The constitution output does NOT contain agent-specific `## Permissions` sections — agent-specific permissions are not generated by constitution-builder
- The constitution output does NOT contain agent-specific `## Standing Rules` — agent-specific standing rules are not generated by constitution-builder
- Cross-cutting permissions and standing rules that apply to every agent in the project MAY appear in the constitution
- KB-sourced context is scoped to this project's KB(s): per DEC-038 (multi-KB, project-scoped agents), wiki-query lookups address the project's own knowledge base(s), not another project's

**write_mode behavior**
- `in_place_skill` mode writes the domain knowledge sections into an existing `SKILL.md` at the specified path
- `composed_agent_file` mode writes the domain knowledge sections into a standalone agent file at the specified path (agent-specific configuration is supplied by `agent-builder-skill`, not constitution-builder)
- `standalone_constitution` mode writes the universal Tier 1 constitution at `.claude/guidelines/constitution.md`

**Routing delegation**
- The workflow contains no phase that generates routing tables or agent-specific routing entries — these have been removed
- A note or comment in the workflow.md explicitly states that routing generation is handled by `agent-builder-skill`

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- `momentum:constitution-builder` SKILL.md and workflow.md (current behavior to be narrowed)
- `agent-builder-skill` story (receives routing + agent-specific permissions; must coordinate with this story)
- `build-guidelines-skill` story (primary consumer of new write modes)
- `constitutionmd-generation-acceptance-criteria` story (sibling — shares the `## Quick Routing` ownership reconciliation per DEC-038)
- `wiki-query-interface-block-for-hot-constitution` (defines what `standalone_constitution` mode must include)
- DEC-038 — manifesto = per-agent diagnostic table; per-agent routing owned at the manifesto/agent-builder layer, NOT the shared constitution; per-project multi-KB, project-scoped agents (reconciles `## Quick Routing` ownership for this story)
- DEC-026 D4 — constitution-builder rework, domain knowledge only (authoritative scope source)
- DEC-026 D5 — three-skill pipeline: constitution-builder → agent-builder × N → routing table
- DEC-018 — wiki-query as Tier 3 cold KB interface (extended by DEC-038 to multiple per-project KBs)
- DEC-013 — universal agent model
- DEC-001 — three-tier agent guidelines architecture

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._
