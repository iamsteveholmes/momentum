---
title: KB Ingest — Ingest Documents into Project Knowledge Vault
story_key: kb-ingest
status: backlog
epic_slug: agent-team-model
depends_on:
  - kb-init
touches:
  - skills/momentum/skills/kb-ingest/SKILL.md
  - skills/momentum/skills/kb-ingest/workflow.md
---

# KB Ingest — Ingest Documents into Project Knowledge Vault

## What This Is

A skill (`/momentum:kb-ingest`) that ingests source material into a project's cold
knowledge base vault. Accepts documents from multiple sources — web URLs, local files,
research outputs, changelogs — and processes them into the pre-synthesized wiki format
the vault uses.

## Why It Matters

The cold KB is only useful if it's populated with accurate, current domain knowledge.
The vault's wiki pages are the upstream source that `momentum:build-guidelines` distills
into hot constitutions and composed agent files. Without tooling to maintain the vault,
it goes stale and loses its core value: pre-compiled "use X not Y" decisions that agents
never have to re-derive at runtime.

**The Karpathy argument (April 9, 2026 session):** "RAG doesn't accumulate. Every query
re-derives knowledge from scratch. The alternative is a persistent wiki where knowledge
compounds over time." Ingest is how the wiki compounds.

## Design (from April 9, 2026 session)

The ingest pipeline follows Karpathy's compile-time / query-time split:

**At ingest time (expensive, done once):**
1. Accept source (URL, file, research report, changelog)
2. Fetch and parse content
3. Synthesize into wiki format: extract "use X not Y" decisions, version pins, patterns
4. Place in appropriate wiki subdirectory (`concepts/`, `entities/`, `sources/`, `maps/`)
5. Update `index.md` registry entry
6. Append to `log.md`

**At query time (free):** Agents grep `index.md` for relevant page, read the targeted
page, apply pre-compiled decisions. No re-derivation, no embedding search.

## Source Types

| Source | Example | Processing |
|---|---|---|
| Web URL | `kotlinlang.org/llms.txt` | Fetch, extract relevant sections, synthesize |
| Research report | `_bmad-output/research/**/*.md` | Extract key findings, convert to wiki format |
| Local file | `docs/api-reference.md` | Parse and synthesize |
| Changelog | Library GitHub releases | Extract breaking changes, version pins |
| Raw dump | Any unstructured text | LLM-assisted synthesis into wiki format |

## Rough Scope

- Accept one or more source inputs (interactive or CLI args)
- For each source: fetch → parse → synthesize → classify (concepts/entities/sources/maps)
- Synthesize LLM pass: extract prohibitions, version pins, patterns, cross-references
- Write wiki page to appropriate subdirectory with frontmatter (lastVerified, sources)
- Update `index.md` with new registry entry
- Append ingest event to `log.md`
- Output: summary of pages created/updated, staleness count for existing pages

## Context References

- Decision document: `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`
- Depends on: `kb-init` (vault must exist)
- Enables: `momentum:build-guidelines` (distills vault into hot constitution + agent files)
