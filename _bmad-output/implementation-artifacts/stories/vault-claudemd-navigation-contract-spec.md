---
title: Vault CLAUDE.md navigation contract spec
story_key: vault-claudemd-navigation-contract-spec
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-practice-knowledge-base
story_type: feature
depends_on: []
touches: []
---

# Vault CLAUDE.md navigation contract spec

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a precise specification for the CLAUDE.md that kb-init writes into each scaffolded vault,
so that LLM agents running build-guidelines and other consumers can reliably navigate the vault at runtime.

## Description

Specify the exact contents of the CLAUDE.md kb-init writes into each scaffolded vault: index-first navigation rule, grep-keyword workflow, never-load-all-pages rule, query patterns, ambiguity resolution. The CLAUDE.md is a precise instruction set for LLM agents and determines whether build-guidelines and other consumers can reliably find relevant KB passages at runtime.

**Pain context:** The CLAUDE.md in a scaffolded vault is the primary navigation contract for any LLM agent reading from it. Without a spec, kb-init may produce a CLAUDE.md that is vague, incomplete, or inconsistent across vaults — meaning agents like build-guidelines will navigate differently per vault and may fail to locate relevant content. The spec must be authored before kb-init can be correctly implemented.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- The CLAUDE.md navigation contract is documented specifying: index-first navigation rule, grep-keyword workflow, never-load-all-pages rule, query patterns, and ambiguity resolution strategy
- The spec is precise enough for kb-init to generate a conforming CLAUDE.md without further interpretation
- The spec covers how agents should identify and load relevant KB passages given a query
- build-guidelines and other consumer skills can rely on the CLAUDE.md contract at runtime

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

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
