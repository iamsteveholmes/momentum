---
title: Momentum knowledge base buildout
story_key: momentum-knowledge-base-buildout
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Momentum knowledge base buildout

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to stand up Momentum's own knowledge base (KB) — separate from any other project's KB — that Momentum agents query via `wiki-query`,
so that a Momentum agent's diagnostic-table manifesto resolves its symptom→`wiki-query` lookups against Momentum-domain knowledge instead of an unrelated project's KB.

## Description

Momentum needs its OWN Obsidian-style cold KB, distinct from nornspun's, because agents are
project-scoped (DEC-038 D2): a Momentum agent resolves its manifesto's symptom→`wiki-query`
lookups against Momentum-domain knowledge (skills, workflows, agent architecture, conduct,
practice model, …), not nornspun's. This story stands up the "cold KB" half that the
diagnostic-table manifesto (DEC-038 D1) queries.

Scope to define during create-story: which concept pages the Momentum KB needs (its own
domain), the vault location/config, ingest path, and the `wiki-query` wiring against it.
Also carries the **multi-KB requirement** from DEC-038 D2 — the `build-agents` pipeline and
the `wiki-query` interface must support more than one project KB (extends DEC-018).

Source: DEC-038 (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture,
2026-06-16). Background: `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`.

**Pain context:** Without a Momentum KB there is nothing for a Momentum agent's diagnostic-table
manifesto to query — the recovered prototype's KB (`nornspun-agentic-kb`) is nornspun's, not
Momentum's. The cohort pipeline can compose agents but their `wiki-query` routing would resolve
against the wrong (or no) knowledge base until this exists.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- A Momentum-owned KB vault exists (location/config defined) and is distinct from nornspun's.
- An initial set of Momentum-domain concept pages is identified/seeded (skills, workflows, agent architecture, conduct, practice model).
- `wiki-query` resolves against the Momentum KB for Momentum agents.
- The `build-agents` pipeline and `wiki-query` interface support multiple, per-project KBs (DEC-038 D2; extends DEC-018).
- Manifesto symptom→query entries for Momentum agents map to real Momentum KB pages (no dangling queries — ties to the DEC-038 D1 completeness criterion).

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
Source: DEC-038; `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
