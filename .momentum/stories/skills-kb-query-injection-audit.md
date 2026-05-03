---
title: "Skills KB Query Injection Audit — Enumerate Injection Points Across All Momentum Skills"
story_key: skills-kb-query-injection-audit
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: exploration
depends_on: [kb-init]
touches: []
---

# Skills KB Query Injection Audit — Enumerate Injection Points Across All Momentum Skills

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to audit every Momentum skill workflow for steps that make domain decisions, select technical patterns, or produce recommendations — and identify where an explicit `wiki-query [question]` call should be added as a required step,
so that every skill that makes a domain recommendation invokes wiki-query with a specific question instead of relying on LLM training data, surfacing project-specific conventions that training data will never know.

## Description

Commission a full audit of all Momentum skill workflows (sprint-dev, sprint-planning, create-story, retro, triage, intake, distill, decision, quick-fix, research, and all others) to enumerate wiki-query injection points. For each skill, identify steps where a `wiki-query [question]` call should be added as an explicit required step — any step that classifies a domain, selects a pattern, or produces a technical recommendation is a candidate. 

**Audit output format:** For each injection point, propose the specific `wiki-query` invocation: the skill name, the workflow step number, the current step text, and the exact question string to pass to wiki-query (e.g., `wiki-query "what patterns does this project use for error handling?"`). Output written as a structured artifact (markdown table or annotated list). This drives subsequent per-skill wiki-query injection implementation stories.

Depends on KB being real (kb-init + kb-ingest shipped) before injection steps are meaningful to implement — but the audit itself can be done against the skill definitions now.

**Pain context:** LLMs always prefer training data over external lookup. Passive instructions like "consult the KB if needed" are effectively ignored. The only reliable delivery mechanism is an explicit required workflow step. Without an audit, injection points will be added ad-hoc and inconsistently. Originally decided in DEC-015 D4 (2026-05-02); injection mechanism updated by DEC-018 D2 (2026-05-03) — the mechanism is now `wiki-query`, superseding the original DEC-015 D2 description of "grep index.md, read targeted page."

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Every Momentum skill workflow.md reviewed for injection candidates
- Each identified injection point documented: skill name, step number, current step text, and the specific `wiki-query [question]` call to add (including the exact question string)
- Output written as a structured artifact (markdown table or annotated list)
- Injection points categorized by type: domain classification, pattern selection, technical recommendation
- Audit notes which skills already have explicit wiki-query steps vs. none
- Output serves as the direct input for per-skill wiki-query injection implementation stories
- Proposed wiki-query questions are concrete and answerable (not vague — e.g., `wiki-query "what naming conventions does this project use for skill workflow steps?"` not `wiki-query "conventions"`)

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
