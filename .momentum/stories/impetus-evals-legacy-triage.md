---
title: "Impetus evals — triage legacy markdown evals against new memory agent"
story_key: impetus-evals-legacy-triage
status: backlog
epic_slug: impetus-core
feature_slug: 
story_type: maintenance
depends_on: []
touches:
  - skills/momentum/skills/impetus/evals/
---

# Impetus evals — triage legacy markdown evals against new memory agent

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to audit and triage the 70+ legacy markdown eval files in `skills/momentum/skills/impetus/evals/`
against the rebuilt Impetus memory agent,
so that obsolete evals are deleted, surviving behaviors are identified, and the path is clear for authoring proper micro-eval YAML fixtures for the new Impetus.

## Description

The Impetus skill was rebuilt from a 793-line XML-step workflow into a lean memory agent with three capabilities: Orient, Dispatch, and Partner. The old evals/ folder contains 70+ markdown eval files that test behaviors from the removed workflow — journal thread hygiene, progress bars, install/upgrade routing, hash drift warnings, session menu voice, spec contextualization steps, XML step narration guards, etc.

Before any micro-eval YAML fixtures can be authored for the new Impetus, this triage must happen first. Without it, new fixture work has no baseline — we don't know which behaviors survived, which are gone, and which concepts are worth carrying forward in the new format.

**Three-pass approach:**
1. **Classify** each eval as one of: `obsolete` (tests a removed behavior — delete), `salvageable` (the concept survives in the new memory agent but needs rewriting as a micro-eval YAML fixture), or `keep` (tests a behavior that still applies as-is — unlikely given the full rewrite)
2. **Delete** all obsolete evals
3. **Stub** salvageable ones — for each salvageable behavior, create an intake stub identifying what micro-eval fixture it would become

Behaviors guaranteed obsolete: journal threads, progress bars, install/upgrade routing, hash drift, session menu voice, spec contextualization steps, XML step narration guards, thread hygiene checks, declined-offer tracking, version detection, upgrade execution.

Behaviors that may survive in new form: silent preflight (now the Orient capability), no-narration rule (now a CREED boundary), dispatch confirmation before summoning (Dispatch capability).

**Dependency impact:** The existing micro-eval fixture backlog stories should be updated to `depends_on` this story:
- `momentum-micro-eval-runner-skill`
- `micro-eval-fixture-yaml-schema-schemamd`
- `micro-eval-workflow-fidelity-meta-fixture`
- Any fixture stories written specifically for Impetus behaviors

**Pain context:** Without this triage, 70+ stale evals sit in the evals folder testing behaviors that don't exist, polluting the eval suite and giving a false signal about what the new Impetus actually does. Downstream micro-eval fixture work for Impetus blocks on knowing what's worth keeping.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Every eval in `skills/momentum/skills/impetus/evals/` is classified: obsolete, salvageable, or keep
- Classification rationale documented (one line per eval is sufficient)
- All obsolete evals deleted from the evals/ directory
- For each salvageable eval: an intake stub exists describing the corresponding micro-eval YAML fixture to author
- The following existing backlog stories are updated to `depends_on: [impetus-evals-legacy-triage]`: `momentum-micro-eval-runner-skill`, `micro-eval-fixture-yaml-schema-schemamd`, `micro-eval-workflow-fidelity-meta-fixture`
- The evals/ directory after triage contains only files that correspond to behaviors that actually exist in the rebuilt Impetus

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance
_DRAFT_

### Testing Requirements
_DRAFT_

### Implementation Guide
_DRAFT_

### Project Structure Notes
_DRAFT_

### References
_DRAFT_

## Dev Agent Record

_DRAFT — populated by dev agent after create-story enrichment._

### Agent Model Used
### Debug Log References
### Completion Notes List
### File List
