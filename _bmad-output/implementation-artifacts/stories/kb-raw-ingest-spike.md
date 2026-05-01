---
title: Spike — KB Raw Source Ingestion: Obsidian, Document Trees, llms.txt, Research
story_key: kb-raw-ingest-spike
status: backlog
epic_slug: agent-team-model
depends_on:
  - kb-init
touches:
  - _bmad-output/research/kb-raw-ingest-spike/
change_type: research
---

# Spike — KB Raw Source Ingestion

## What This Is

A spike to determine how documents get into the cold KB vault's `raw/` folder. Before
`momentum:kb-ingest` can synthesize wiki pages, raw source material must exist. This
spike researches the ingestion patterns and produces a committed findings report that
directly informs the `kb-ingest` story implementation.

As a spike, this story is complete when the research artifact is committed — not when
code ships. See feedback: spikes must commit research artifacts, not informal experiments.

## Questions to Answer

### 1. Obsidian as a collection surface

Obsidian has a rich plugin ecosystem for pulling external content into a vault.
Investigate which plugins are relevant for KB raw feed:

- Which Obsidian plugins support importing web pages, documentation sites, RSS feeds,
  or GitHub release notes into a local vault?
- Can an Obsidian vault serve as the `raw/` directory directly (or feed into it)?
- What format does Obsidian-collected content arrive in — are cleanup passes needed
  before ingest synthesis?
- Is Obsidian viable as the "collection UI" with the KB vault as the backend, or does
  it add complexity without enough value?

### 2. Large published document sets without llms.txt

Many important library docs exist as large site trees (Jetpack Compose, Ktor, Django,
FastAPI, etc.) with no `llms.txt` consolidation. Pulling the entire tree is too much;
ignoring it loses accuracy.

Investigate:
- What chunking/selection strategies work for large doc sites? (sitemap crawl + filter,
  targeted page selection, API reference extraction only?)
- Are there existing tools that handle this — crawl4ai, Firecrawl, llmstxt.site, or
  similar scrapers designed for LLM ingestion?
- What's the right granularity for a `raw/` entry — one file per page, one file per
  section, one file per library?
- How does the cold KB avoid becoming a mirror of the internet? What's the selection
  criteria for what goes into `raw/`?

### 3. llms.txt — when it exists and when it doesn't

Some projects publish `llms.txt` (Anthropic, Kotlin, Next.js, Stripe). Others don't.

- For sites with `llms.txt`: what's the ingest path? Direct pull? Size limits?
- For sites without `llms.txt`: what's the fallback? Does `llmstxt.site` auto-generate
  them for common sites? Can we generate one ourselves from a sitemap?
- Is `llms.txt` even the right abstraction for tech-stack guidelines — or is it better
  suited to API reference than patterns/conventions?

### 4. Research output ingestion

Momentum produces structured research reports (`_bmad-output/research/**/*.md`). These
are already pre-synthesized — they should feed the cold KB directly.

- What's the ingest path for a finished research report? (direct copy? synthesis pass?)
- How do research findings get cross-referenced against existing wiki pages to avoid
  duplication?
- Should raw research go into `raw/` (immutable source) or directly into `wiki/` (already
  synthesized)?
- What about planning artifacts — decisions, assessments, architecture.md sections? Do
  those go into the KB?

### 5. Maintenance and staleness

The cold KB is only valuable if it stays current.

- How does the vault know when a raw source has been updated upstream?
- What's the staleness signal — `lastVerified` date? Version pins? Webhook?
- How does re-ingesting a source update the wiki page derived from it without blowing
  away manual edits?

## Deliverable

A committed research report at:
`_bmad-output/research/kb-raw-ingest-spike/findings.md`

The report must answer all five question sets above and include:
- Recommended ingestion strategy per source type (table)
- Recommended tooling (Obsidian plugin names, scrapers, etc.)
- The selection criteria for `raw/` inclusion
- A proposed ingest flow diagram
- Open questions that need user input before `kb-ingest` implementation begins

## Research Method

Use the standard Momentum research pattern: spawn parallel discovery agents per
question set, cross-validate with AVFL checkpoint. Web search is required — this
investigation has a large external component.

## Context References

- Decision document: `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`
- Vault structure: `kb-init` story — `raw/` is the immutable source layer
- Downstream: `kb-ingest` story — depends on this spike's findings to define source types
- Example existing raw material: `_bmad-output/research/agent-guidelines-architecture-2026-04-09/`
- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
