---
title: "DEC-029 Phase 2 design note — context bundles scoped per agent role, assembled independently"
story_key: dec-029-phase-2-design-note-context-bundles-scoped-per-agent
status: backlog
epic_slug: sprint-dev-workflow
feature_slug: momentum-sprint-planning-to-ready
story_type: practice
depends_on: []
touches: []
---

# DEC-029 Phase 2 design note — context bundles scoped per agent role, assembled independently

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Phase 2 sprint-dev rewrite to scope each agent's context bundle to its role,
so that agents reason only from relevant material, parallel spawning requires no coordination, and hallucination risk from irrelevant noise is minimised.

## Description

Design constraint for the Phase 2 sprint-dev rewrite: each agent in the per-story review step and fix loops receives a context bundle scoped to its role — not a shared dump of everything.

**Specific scoping:**
- **code-reviewer:** architecture docs + diff (what was changed + how it should be built)
- **QA agent:** PRD + story file (ACs, spec) — what was promised
- **AVFL fixer:** failing check + architecture rules relevant to that check + diff that caused the failure
- **E2E fixer:** failing scenario + story ACs + harness driver that ran it + observable output

These bundles are completely disjoint — code-reviewer and QA agent share no reference material. This drives two things:
1. They can be constructed independently and spawned in parallel with zero coordination overhead (pure fan-out, not TeamCreate).
2. Each agent reasons only from relevant context, reducing hallucination risk from irrelevant noise.

This principle extends across all three loop tiers (per-story review, AVFL, E2E): **context bundle = scoped to the failure type, not the story type.**

**Pain context:** Emerged from design discussion after sprint-2026-05-17 completion. If Phase 2 is built without this constraint, a natural shortcut is to pass all available context to every agent — which wastes tokens, slows spawning, and degrades reasoning quality by burying the relevant signal in noise.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- The Phase 2 sprint-dev per-story review step constructs separate context bundles for code-reviewer and QA agent before spawning
- code-reviewer bundle contains architecture docs + diff; does NOT contain PRD or story ACs
- QA agent bundle contains PRD + story file; does NOT contain architecture docs
- AVFL fix routing attaches the failing check + relevant architecture rules to the fixer agent prompt
- E2E fix routing attaches the failing scenario + story ACs + harness driver output to the fixer agent prompt
- code-reviewer and QA agent are spawned concurrently (fan-out), not sequentially

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- DEC-029 D10 — unified validate-fix loop primitive
- DEC-029 D9 — four-step sprint-dev flow
- `momentum/agents.json` — fixer routing table
- `momentum/verification-harness.json` — execution surface + driver bindings
- Sprint-2026-05-17 post-sprint design discussion (session 2026-05-19)

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
