---
title: e2e-validator agent body rewrite — de-Gherkin, harness-driven
story_key: e2e-validator-agent-body-rewrite-de-gherkin-harness-driven
status: review
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: practice
change_type: agent-definition
verification_method: trigger
depends_on: []
touches: []
---

# e2e-validator agent body rewrite — de-Gherkin, harness-driven

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an e2e-validator agent body that reads method-polymorphic contracts and a harness profile instead of assuming Gherkin and a fixed stack,
so that the validator works across projects/stacks without prompt edits and stays consistent with the method-routed pipeline.

## Description

Rewrite the e2e-validator agent body to: consume method-polymorphic contracts (not only .feature/Gherkin files); remove the hardcoded finch / PostgreSQL / FastAPI tooling leak from the prompt; and drive entirely from momentum/verification-harness.json. (DEC-029 D1/D3; affects DEC-020.)

**Pain context:** Source: DEC-029 (_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md), decisions D1/D3; affects DEC-020. Depends on the momentum/verification-harness.json schema stub (consumes it). Phase 1 gated on routing-table-schema-and-implementation landing momentum/agents.json (DEC-029 Gate 1).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Consumes method-polymorphic contract not only .feature
- No hardcoded finch/PostgreSQL/FastAPI references
- Reads momentum/verification-harness.json for env/drivers/targets
- Behavior consistent with DEC-029 D1/D3
- Reconciles with DEC-020 agent taxonomy

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [x] Rewrite e2e-validator.md agent body — remove Gherkin-only language, add harness-driven routing
- [x] Add verification routing table (change_type → method → driver) driven by harness.json
- [x] Remove hardcoded finch/PostgreSQL/FastAPI references from Environment Prerequisites
- [x] Add harness.json Environment Setup section (reads startup, readiness_probes, execution_surfaces, driver_bindings)
- [x] Update description to reflect method-polymorphic, harness-driven behavior
- [x] Add evals: harness-driven driver selection, BLOCKED when harness absent, document review for research-spike

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

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — implementation was direct rewrite with clear source (harness.json schema + verification-standard.md routing table).

### Completion Notes List

- Rewrote e2e-validator.md agent body from scratch per DEC-029 D1/D3
- Removed all Gherkin-specific language: description, input section, process steps, output format
- Removed hardcoded finch/PostgreSQL/FastAPI environment prerequisites
- Added "Environment Setup" section: reads momentum/verification-harness.json for startup, readiness_probes, execution_surfaces, driver_bindings, human_review_carveouts
- Added "Verification Routing" section: change_type → method → driver table aligned with verification-standard.md
- Added method-specific sections: skill-invoke, behavioral-trigger, bash/curl, document-review
- Updated description frontmatter: now describes method-polymorphic, harness-driven behavior
- Output format updated: per-story results include change_type, method, driver fields
- Verdict rule for BLOCKED now explicitly covers harness.json absent case
- Added 3 evals covering: harness-driven driver selection, BLOCKED when harness absent, document review routing for research-spike

### File List

- skills/momentum/agents/e2e-validator.md
- skills/momentum/agents/evals/eval-e2e-validator-reads-harness-for-driver.md
- skills/momentum/agents/evals/eval-e2e-validator-blocked-when-harness-absent.md
- skills/momentum/agents/evals/eval-e2e-validator-document-review-for-research-spike.md
