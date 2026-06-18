---
title: Constitution.md generation acceptance criteria
story_key: constitutionmd-generation-acceptance-criteria
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Constitution.md generation acceptance criteria

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want concrete acceptance criteria defined for build-guidelines' constitution.md (Tier 1) output,
so that the generated constitution is verifiable, appropriately sized, and properly cites its sources.

## Description

Author concrete acceptance criteria for build-guidelines' constitution.md (Tier 1) output: format, line-count budget (target ~660 lines per decision document), content rules (critical rules only, pointers to refs/), citation integrity (every rule traceable to a KB source or project decision).

**Pain context:** Without defined acceptance criteria for constitution.md, build-guidelines has no quality bar to produce against, and the output cannot be verified as correct. The ~660 line budget and citation integrity requirements are derived from the decision document model but have not been formalized as testable ACs for the skill.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Acceptance criteria for constitution.md format are documented (file format, section structure) — scoped to shared project content (identity, values, constraints, glossary); see DEC-038 Alignment below for why per-agent routing is excluded from the shared constitution
- Line-count budget target (~660 lines) is specified and enforced by build-guidelines
- Content rules are defined: critical rules only, pointers to refs/ for detail
- Citation integrity rule is defined: every rule must be traceable to a KB source or project decision
- ACs are integrated into build-guidelines' verification logic or post-generation check
- **DEC-015 D3 fold-in:** KB trigger language in the constitution must be prescriptive, not permissive. Do not use "if you need domain knowledge, check the KB." Instead enumerate specific named scenarios that require a KB query (e.g., "when classifying a story's domain", "when selecting a test pattern for a new library", "when choosing between library approaches on this stack"). Each trigger must name the exact context — no judgment call left to the agent. Rationale: LLMs always prefer training data; vague permission is effectively no instruction.
- **DEC-038 D1 fold-in:** The shared constitution.md carries project identity, values, constraints, and glossary — content that is meaningfully shared across every agent on the project. It must NOT own or duplicate per-agent routing (the diagnostic table of observable symptom → exact `wiki-query` lookup). Per-agent routing is owned at the manifesto/agent-builder layer because a project-shared routing block (e.g., a Compose/Kotest table) is meaningless for a `pm` or `architect` agent. Acceptance criteria for constitution.md generation must therefore assert that the generated shared constitution contains no per-agent routing content, and that any `## Quick Routing` material is reconciled against the per-agent model — see sibling story `constitution-builder-write-mode-parameterization`.

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## DEC-038 Alignment

Per [DEC-038](../../_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md) (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB), the acceptance criteria for constitution.md generation must respect the ownership boundary between the shared constitution and the per-agent manifesto:

- **Shared constitution scope.** constitution.md (Tier 1) carries project-level identity, values, constraints, and glossary — content that is genuinely shared across every agent on the project. The "format / section structure" AC above must reflect this scope and must not prescribe a per-agent routing section as part of the shared constitution.
- **Routing is per-agent, not shared.** Per-agent routing — the *diagnostic table* mapping observable developer symptoms to the exact `wiki-query` KB lookup — is a stable, per-role×domain artifact owned at the **manifesto/agent-builder** layer, not the shared constitution. A project-shared `## Quick Routing` block (e.g., a Compose/Kotest routing table) is meaningless for a `pm` or `architect` agent, so the shared constitution must not bake it in.
- **AC consequence.** Constitution generation does not own or duplicate per-agent routing. Acceptance criteria must include a check that the generated shared constitution contains no per-agent diagnostic-table / routing content, and that any `## Quick Routing` content is reconciled against the per-agent model.
- **Cross-reference.** This reconciliation is coordinated with the sibling story `constitution-builder-write-mode-parameterization` (DEC-038 Phase 1), which owns reconciling `constitution-builder`'s current project-*shared* `## Quick Routing` ownership against the per-agent routing model. Keep the two stories consistent.

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

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
