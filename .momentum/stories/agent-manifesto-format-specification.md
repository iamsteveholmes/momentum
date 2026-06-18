---
title: Agent manifesto format specification
story_key: agent-manifesto-format-specification
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Agent manifesto format specification

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a defined schema, location, and content model for the agent manifesto — the agent's diagnostic table — that build-guidelines consumes,
so that build-guidelines can generate composed Tier 2 specialist agent files without ambiguity.

## Description

Define schema, location, and content model of the agent manifesto that build-guidelines consumes to produce composed specialist files.

Per DEC-038, the manifesto **is** the agent's **diagnostic table**: a **stable**, per-role×domain table that maps each *observable developer symptom → the exact `wiki-query` KB lookup* that resolves it, plus the **stack facts** that scope those lookups. The table is the *same* across every sprint and every story — it is the agent's standing "how everything is implemented here" guidance, not a per-sprint or per-story context overlay (that earlier reading is rejected). Without this format, build-guidelines cannot generate Tier 2 composed agents.

**Pain context:** build-guidelines currently has no defined input format. Without a manifesto spec, the skill cannot know which role × domain diagnostic table to compose, what stack facts to include, or which project KB the symptom→`wiki-query` entries resolve against. This blocks all downstream composed-specialist work.

The manifesto is **project-scoped**: its diagnostic table targets one project's knowledge base, and `wiki-query` (DEC-018, extended) resolves against that project's KB. Momentum agents draw on the Momentum KB; nornspun agents draw on the nornspun KB; the format must carry which KB it scopes to. The recovered nornspun `cmp-dev` prototype (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`) is the reference shape the format must capture — it is a **format exemplar only**, never a Momentum agent.

## DEC-038 Alignment

This is the canonical format story for the manifesto; DEC-038 fixes the definition it must encode. The earlier framings ("role × domain matrix plus stack facts" here; "agent-specific routing" in DEC-026 D4; "project/sprint context overlay" in PRD FR136) are superseded by one definition:

- **The manifesto IS the agent's diagnostic table** — stable, per-role×domain, mapping observable developer symptom → exact `wiki-query` KB lookup, plus the stack facts that scope it. Same across every sprint and story; the per-sprint/per-story overlay reading is **rejected**.
- **Completeness is an acceptance criterion on this story:** an agent hitting territory the diagnostic table does not guide means the manifesto is incomplete, and the format must make that gap detectable.
- **Project-scoped, multi-KB:** the format scopes to one project's KB; multiple per-project KBs are supported, with `wiki-query` (DEC-018) extended accordingly.
- **Reference exemplar:** `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (verbatim nornspun `cmp-dev.md`; ~35 worked symptom→`wiki-query` entries across 9 technology areas) is the shape the format must capture — format-only, never a Momentum agent.

See `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` (Phase 0).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation, reconciled with the DEC-038 diagnostic-table canon:
- A manifesto schema is defined (format and location TBD) that models a **stable, per-role×domain diagnostic table**: each entry pairs an *observable developer symptom* with the *exact `wiki-query` KB lookup* that resolves it.
- The schema captures the **stack facts** (language, frameworks, test tools, etc.) that scope the diagnostic table's lookups.
- The schema is **project-scoped**: the manifesto records which project KB its `wiki-query` entries resolve against, supporting multiple per-project KBs (DEC-018 extended).
- **Completeness criterion:** the format makes manifesto completeness verifiable — if an agent hits a situation the manifesto's diagnostic table does not guide (a symptom with no entry, or an entry whose `wiki-query` returns nothing usable), the manifesto is **incomplete**. The format must expose this gap rather than hide it.
- The format is validated against the reference exemplar shape (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`, ~35 worked symptom→`wiki-query` entries across 9 technology areas) — the format must be able to express every entry in that exemplar.
- The schema is documented in a reference location accessible to build-guidelines.
- build-guidelines can parse the manifesto and use its diagnostic table to determine which composed files to generate.
- The manifesto location/naming convention is documented in architecture.md.

> Note: The ACs above are reconciled to the DEC-038 canon but remain rough captures.
> Create-story will replace them with validated, testable acceptance criteria.

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

<!-- DRAFT: References below are reconciliation anchors from DEC-038. Create-story will
     add further source citations from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` — canonical manifesto = diagnostic-table definition, completeness criterion, per-project multi-KB scope (D1, D2; Phase 0).
- `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — format reference exemplar (verbatim nornspun `cmp-dev.md`; ~35 symptom→`wiki-query` entries across 9 tech areas). Format-only; never a Momentum agent.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
