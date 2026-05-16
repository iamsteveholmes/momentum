---
title: Build Nornspun Agent Constitution (Tier 1 Hot Context)
story_key: nornspun-agent-constitution
status: backlog
epic_slug: agent-team-model
feature_slug: ""
story_type: feature
depends_on: []
touches: []
---

# Build Nornspun Agent Constitution (Tier 1 Hot Context)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a tight Tier 1 constitution file for nornspun agents,
so that every agent — whether spawned by sprint planning or invoked ad-hoc — operates with the right project-specific context, routing, and KB access without requiring developer guidance each time.

## Description

The three-tier Codified Context architecture (DEC-008) defines: Tier 1 hot constitution (always loaded), Tier 2 composed specialist files (loaded at spawn), Tier 3 cold KB (on-demand retrieval). The nornspun-agentic-kb vault was built as the Tier 3 cold layer. This story builds the Tier 1 constitution.

The constitution for nornspun is intentionally narrow — ~100-150 lines, not the 660-line reference implementation — because Momentum's sprint planning already handles structured routing. The constitution covers only what planning cannot: ad-hoc invocations and project-specific invariants every agent must honor.

**Key design decisions from conversation:**
- Sprint planning drives routing for structured work; the constitution handles ad-hoc only
- The routing table maps file patterns / task types to specialist agents as a fallback
- CMUX layout is now hardcoded globally (see `~/.claude/rules/cmux.md`) — the constitution should reference it, not re-define it
- The cold KB lives at `~/projects/nornspun-agentic-kb`; agents need JIT retrieval instructions, not the index pre-loaded

**Pain context:** Without the constitution, ad-hoc agent invocations on nornspun lack context about the project's invariants (async-first, repository pattern, SSE contract, cost caps). Agents reinvent decisions already captured in architecture docs and the KB. The KB exists but agents aren't wired to query it.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation, narrowed per DEC-026 D4:

**Scope: project domain knowledge only (embedded facts + KB lookups). The constitution is
project-wide shared knowledge — identical for every agent. It does NOT contain agent-specific
routing entries; those belong in each agent's manifesto (agent-builder's concern).**

- Constitution file exists at `nornspun/.claude/guidelines/constitution.md` (or equivalent agreed path)
- File is ≤150 lines
- Project invariants section covers: async-first (no blocking calls in async routes), all DB access via repository layer, SSE contract (message.delta/message.complete per Decision 20), snake_case wire format, per-session cost cap enforcement
- Cold KB pointer section: vault path, when to query (unfamiliar API, pattern uncertainty, library version questions), wiki-query interface block (how to invoke wiki-query skill or grep vault) — this block stays in the constitution as shared infrastructure
- Constitution is validated against nornspun architecture docs for accuracy before merge
- Tier 2 specialist files (Python backend dev, Kotlin/Compose dev, QA) are out of scope for this story — tracked separately

> **Not in scope (moved per DEC-026 D4):** File-pattern → agent-role routing entries
> (e.g., `*.kts` → dev-build, `*.kt` in `composeApp/` → dev-frontend) are agent-specific
> and belong in the agent manifesto. Generating those entries is agent-builder's concern,
> not the constitution's.

> Note: The ACs above are rough captures from conversation, narrowed by DEC-026 D4 scope
> decision. They are starting points only. Create-story will replace them with validated,
> testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- DEC-008: Composable Specialist Agents Architecture (`_bmad-output/planning-artifacts/decisions/dec-008-composable-agents-architecture-2026-04-22.md`)
- Lens B2: Context Engineering Ecosystem (`_bmad-output/research/agent-guidelines-discovery-2026-04-09/raw/lens-b2-context-engineering-ecosystem.md`)
- Cold KB vault: `~/projects/nornspun-agentic-kb`
- CMUX layout rule: `~/.claude/rules/cmux.md`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
