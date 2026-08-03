---
title: Daily tasting reminder + expected-vs-reality brief generator
story_key: daily-tasting-reminder-expected-vs-reality-brief-generator
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: [momentum-tools-feature-verify-human-verdict-recorder-and]
touches: []
---

# Daily tasting reminder + expected-vs-reality brief generator

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a scheduled daily reminder for my ≥10-minute tasting session, paired with a generated brief that lays out what should work today, what changed, and 2–3 specific probes,
so that the model's expectations about the product's behavior get tested against reality instead of going unverified.

## Description

Scheduled daily reminder for the developer's ≥10-minute tasting session, plus a generated
brief from `.momentum/features.json` and merges since the last walkthrough: what should
work today, what changed, and 2–3 specific probes — the model's expectations tested against
reality. Findings from the walkthrough route to intake under the owner-priority rule
(DEC-040 D6).

**Implementation note:** Check whether `preflight-context-envelope`'s project-state
ingestion can be reused for the brief's data gathering, rather than re-deriving equivalent
logic from scratch.

**Source:** DEC-040 D4 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`.

**Pain context:** Steve, verbatim: "no less than 10 min daily, and that means I need Claude
Code to remind me AND prepare a document for what we would expect today. Let's see if the
model's expectations stand up to reality." Discovery: human walkthroughs found a top-tier
defect within minutes on every occasion (~5-6 in 4 months); the dev database held zero real
user data.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- A daily reminder fires reliably, prompting the developer to run a ≥10-minute tasting
  session (mechanism — session-start nudge, scheduled agent, or other — to be determined
  by create-story analysis).
- A brief is generated from `.momentum/features.json` and merges since the last walkthrough,
  covering: (a) what should work today, (b) what changed, (c) 2–3 specific probes that test
  the model's stated expectations against observed reality.
- Findings surfaced during the walkthrough route to intake under the owner-priority rule
  (DEC-040 D6).
- The brief's data-gathering step reuses `preflight-context-envelope`'s project-state
  ingestion where applicable, rather than re-deriving equivalent logic — to be confirmed
  during create-story's architecture analysis.

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
