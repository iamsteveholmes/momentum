---
title: KB Init — Scaffold Cold Knowledge Base Repo for a Project
story_key: kb-init
status: backlog
epic_slug: agent-team-model
depends_on: []
touches:
  - skills/momentum/skills/kb-init/SKILL.md
  - skills/momentum/skills/kb-init/workflow.md
---

# KB Init — Scaffold Cold Knowledge Base Repo for a Project

## What This Is

A skill (`/momentum:kb-init`) that scaffolds a new cold knowledge base (KB) repo for a
project. The cold KB is Tier 3 in the three-tier agent guidelines architecture — the
pre-synthesized, LLM-maintained vault of domain knowledge that feeds Tier 1 (hot
constitution) and Tier 2 (composed specialist agent files).

## Why It Matters

The three-tier agent guidelines architecture (decided April 9, 2026 — see
`_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`)
requires a per-project KB repo. Currently no tooling exists to scaffold one. Without
it, the hot constitution and composed agent files have no upstream source of truth —
guidelines would have to be authored from scratch each time rather than distilled from
a maintained wiki.

**Reference example:** `~/projects/momentum_vault` — the cold KB for the Momentum
project itself. Steve built this manually to validate the concept. This skill automates
that setup.

## Design (from April 9, 2026 session)

The cold KB repo follows the Karpathy wiki structure — pre-synthesized knowledge that
compounds over time, fed by `momentum:kb-ingest`:

```
{project}_vault/
├── raw/              ← Immutable source material (docs, research, changelogs)
├── wiki/             ← Pre-synthesized pages (LLM-maintained)
│   ├── concepts/     ← Concepts and patterns
│   ├── entities/     ← Named entities (libraries, tools, APIs)
│   ├── sources/      ← Source summaries with citations
│   └── maps/         ← Cross-reference maps
├── index.md          ← Registry of all wiki pages
├── log.md            ← Ingest history and change log
└── CLAUDE.md         ← Vault schema: how agents navigate it
```

`CLAUDE.md` in the vault teaches agents: index-first navigation, never load all pages,
grep by keyword for relevant pages, read the targeted page only.

## Rough Scope

- Interactive: ask developer for project name and target directory (default: `../{project}_vault`)
- Scaffold the full directory structure with stub files
- Write `CLAUDE.md` with vault navigation instructions
- Write `index.md` with empty registry table
- Write `log.md` with creation entry
- Git init the new repo and make first commit
- Output: path to new vault repo, instructions for next step (`momentum:kb-ingest`)

## Context References

- Decision document: `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`
- Example vault: `~/projects/momentum_vault`
- Depends on: nothing (this is the entry point)
- Enables: `momentum:kb-ingest`, `momentum:build-guidelines`
