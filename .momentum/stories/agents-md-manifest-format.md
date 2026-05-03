---
title: Agents.md Manifest Format — Per-Skill Agent Role Configuration Spec
story_key: agents-md-manifest-format
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Agents.md Manifest Format — Per-Skill Agent Role Configuration Spec

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a documented agents.md manifest format spec,
so that each Momentum skill can declare its agent role slots, defaults, tier classification, cardinality, and override instructions in a consistent machine-readable format.

## Description

Define and document the `agents.md` format for use inside each Momentum skill directory. Following DEC-013 (universal agent model) and DEC-016 (two-tier agent taxonomy), each skill needs a manifest that declares: (1) every agent role the skill spawns, (2) the default plugin file for each role, (3) the tier (Tier A: project-conditioned; Tier B: stable default), (4) cardinality (1 or N), and (5) how a project overrides the default. The format enables sprint-planning to discover new agent types at runtime (seed list concept from DEC-013 D3) and enables the `missing-base-bodies-audit` story to systematically verify coverage. After the format is defined, populate agents.md files for sprint-dev, retro, avfl, and distill as the highest-priority skills.

**Pain context:** Currently no agents.md format exists. Sprint-planning cannot discover role gaps automatically. The missing-base-bodies-audit cannot run systematically without a machine-parseable role manifest. DEC-013 referenced the agents.md seed list concept but left the format unspecified. DEC-016 adds tier and cardinality dimensions that also need representation in the format.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- A documented agents.md format spec exists (referenced in DEC-016 and/or a skill reference doc)
- The spec defines: role slot name, default file path, tier (A/B), cardinality (1/N), override instructions
- At minimum sprint-dev, retro, avfl, and distill skills have populated agents.md files conforming to the spec
- sprint-planning can parse agents.md to identify roles not yet in the project's composed agent pool
- The format correctly captures the multi-fixer cardinality=N case for dev-fixer in sprint-dev

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
