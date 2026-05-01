---
title: "dev-skills fixture: SKILL.md frontmatter conformance"
story_key: dev-skills-fixture-skill-md-frontmatter-conformance
status: backlog
epic_slug: epic-3-automatic-quality-enforcement
feature_slug: momentum-quality-gates-enforced
story_type: practice
depends_on: []
touches: []
---

# dev-skills fixture: SKILL.md frontmatter conformance

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies SKILL.md files created or edited by momentum:dev-skills conform to the schema in the agent-skill-development-guide.md,
so that silent structural drift across skills is caught automatically.

## Description

Build a behavioral micro-eval fixture that verifies SKILL.md files created or edited by momentum:dev-skills conform to the schema in skills/momentum/references/agent-skill-development-guide.md (per the project rule .claude/rules/dev-skills.md). Catches silent structural drift across skills.

**Pain context:** SKILL.md frontmatter drift is a silent quality failure — skills that don't conform to the schema may be misrouted, mis-described, or fail to trigger correctly. Without an executable fixture, structural drift accumulates undetected across the skill library.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Given a SKILL.md file produced by momentum:dev-skills, the fixture verifies all required frontmatter fields per agent-skill-development-guide.md schema are present and correctly typed
- Fixture detects and fails when required frontmatter fields are missing, malformed, or use incorrect types
- Fixture passes when frontmatter is fully conformant with the schema
- Fixture follows ForgeCode-style YAML schema with probabilistic assertion, pinned temperature, and model-at-time-of-failure fields
- Fixture is placed in the appropriate evals/ directory under the dev-skills skill
- Schema source is skills/momentum/references/agent-skill-development-guide.md per .claude/rules/dev-skills.md

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
