---
title: "micro-eval: workflow-fidelity meta-fixture"
story_key: micro-eval-workflow-fidelity-meta-fixture
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quality-gates-enforced
story_type: practice
depends_on: []
touches: []
---

# micro-eval: workflow-fidelity meta-fixture

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a meta-fixture that, given a momentum skill with N delegated steps in its workflow.md, verifies all N delegations actually fired during a real invocation,
so that the workflow-fidelity rule is protected from silent erosion via skill self-implementation.

## Description

Build the meta-fixture that, given a momentum skill with N delegated steps in its workflow.md, verifies all N delegations actually fired during a real invocation (no silent self-implementation). Catches the workflow-fidelity rule-violation failure mode that no public benchmark covers — directly protects the `.claude/rules/workflow-fidelity.md` rule from silent erosion.

**Pain context:** The workflow-fidelity rule keeps surfacing as user feedback (`feedback_follow_workflow_exactly`) because skills under load tend to shortcut delegations and do work directly. No public benchmark catches this failure mode — it's specific to Momentum's orchestration discipline. Without a meta-fixture, every skill is one model upgrade away from silently regressing on workflow fidelity.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Meta-fixture parses a target skill's workflow.md and counts delegated steps (spawn/invoke/run X)
- Meta-fixture invokes the target skill against a representative prompt
- Meta-fixture asserts each delegated step actually fired (subagent spawn or skill invoke observed)
- Meta-fixture flags silent self-implementation (workflow says spawn, but skill did it inline)
- Meta-fixture references `.claude/rules/workflow-fidelity.md` as the governing rule
- Meta-fixture conforms to the canonical SCHEMA.md (depends on M2)
- Meta-fixture is parameterizable across multiple skills (not hardcoded to one skill)

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
