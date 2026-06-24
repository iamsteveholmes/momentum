---
title: "Manifesto format: normative file-pattern / ownership field for deterministic agent resolution"
story_key: manifesto-format-normative-file-pattern-ownership-field
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Manifesto format: normative file-pattern / ownership field for deterministic agent resolution

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the manifesto format to declare a normative, machine-readable file-pattern / ownership field that build-guidelines reads deterministically,
so that each composed agent's `agents.json` `patterns` resolve reliably and the agent is always reachable instead of silently falling back to the generic `dev` agent.

## Description

build-guidelines (shipped in sprint-2026-06-18) derives each composed agent's `agents.json` `patterns` (the file globs the `momentum-tools agent resolve --touches` resolver matches on) by best-effort LLM inference from the manifesto's `## Project Stack` PROSE — because the manifesto format (`skills/momentum/references/manifesto-format.md`) declares no normative machine-readable file-pattern/ownership field. A vague Project Stack can yield patterns that don't resolve, leaving the composed agent unreachable (silent fallback to the generic `dev` agent). This is the single G1-determinism residual that stands between "agent cohort works in practice" and "works deterministically."

Fix: add a normative file-pattern/ownership field to the manifesto format and have build-guidelines read it deterministically (no LLM inference for the resolver-critical globs).

This is a real backlog item, NOT a quick-fix.

**Pain context:** Surfaced at the sprint-2026-06-18 conduct end-gate as a "still hollow" gap. It gates the reliability of the sprint's flagship capability (agent composition) — the cohort is not production-trustworthy until resolution is deterministic. Priority: HIGH.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The manifesto format (`skills/momentum/references/manifesto-format.md`) declares a normative, machine-readable file-pattern / ownership field.
- build-guidelines reads that field deterministically to populate `agents.json` `patterns` — no best-effort LLM inference from `## Project Stack` prose for resolver-critical globs.
- A composed agent with a populated ownership field resolves via `momentum-tools agent resolve --touches` (no silent fallback to the generic `dev` agent).

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
