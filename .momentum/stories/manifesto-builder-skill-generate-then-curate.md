---
title: manifesto-builder skill (generate-then-curate)
story_key: manifesto-builder-skill-generate-then-curate
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# manifesto-builder skill (generate-then-curate)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a skill that produces an agent's manifesto — its per-role×domain diagnostic table (observable symptom → exact `wiki-query`) — by auto-drafting entries from the project KB and then requiring human curation of the symptom phrasing,
so that building an agent means authoring its diagnostic identity, reusing the KB-generation method while preserving the human-curated symptom quality the prototype proved is the valuable part.

## Description

Per DEC-038 D1, the manifesto IS the agent's diagnostic table (observable symptom → exact
`wiki-query`). This story builds the producer for it. Design stance to resolve at DEC-038
**Gate G2 (authored vs. generated)**: auto-DRAFT entries from the project KB per role×domain
(reuse `constitution-builder`'s `wiki-query`-per-concept loop), then require human CURATION of
the symptom phrasing — because the recovered `cmp-dev` prototype showed the quality of symptom
phrasing (specific, observable, diagnostic) is the expensive, valuable part.

Open question to settle in create-story: is this a **standalone** `manifesto-builder` skill, or a
generation step **folded into** `agent-builder` / `build-agents`? Reference exemplar for the output
format: `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (~35 worked symptom→`wiki-query`
entries across 9 technology areas).

Source: DEC-038 (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture,
2026-06-16). Background: `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`.

**Pain context:** DEC-038 D1 names the manifesto the agent's diagnostic table, but nothing in the
current pipeline generates it — `agent-builder` *composes* a manifesto that is handed in, it does
not author one. Without this, every composed agent needs a hand-written table from scratch, and the
prototype's hard-won authoring method (generate from KB, then curate) is lost.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Produces a manifesto = per-role×domain diagnostic table in the exemplar format (observable symptom → exact `wiki-query` terms), grouped by technology area.
- Auto-drafts entries from the project KB (reusing the `constitution-builder` wiki-query-per-concept method), then routes to a human curation step for symptom phrasing.
- The authored-vs-generated design (DEC-038 G2) and standalone-vs-folded-into-agent-builder question are resolved and recorded.
- Output validates against the cmp-dev exemplar shape (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`); 15–40 entries, per role×domain, no "consult KB if needed" placeholders.
- Enforces the DEC-038 D1 completeness criterion (no situation the role will face is left unrouted).

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
Source: DEC-038; cmp-dev exemplar `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`; prototype origin `constitution-builder`.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
