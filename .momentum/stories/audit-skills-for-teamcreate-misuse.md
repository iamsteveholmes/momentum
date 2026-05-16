---
title: audit-skills-for-teamcreate-misuse
story_key: audit-skills-for-teamcreate-misuse
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-spawn-orchestration
story_type: maintenance
depends_on: []
touches: []
---

# audit-skills-for-teamcreate-misuse

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a full audit of all Momentum skills that use TeamCreate verified against the fan-out vs TeamCreate decision rule,
so that spawning-pattern misuses are identified and corrected across the entire skill corpus.

## Description

Full audit of Momentum skill corpus against spawning-patterns.md fan-out vs TeamCreate decision rule. TeamCreate was misused in the retro skill (since fixed via hookify). Other skills may have the same violation.

The fan-out vs TeamCreate decision rule: use TeamCreate only when agents need to talk to each other during execution via SendMessage; use fan-out (individual Agent spawns) when agents work independently.

Deliverable: (1) list all skills using TeamCreate, (2) verify each against the decision rule, (3) flag misuses, (4) apply approved fixes.

**Pain context:** A known misuse was found and fixed reactively in the retro skill via hookify. The corpus has not been proactively audited — other skills may contain the same violation. The rule exists in spawning-patterns.md but compliance has not been systematically verified. Source: triage — queue handoff sprint-2026-05-03.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- All Momentum skills using TeamCreate are identified and listed
- Each TeamCreate usage is verified against the decision rule (needs inter-agent SendMessage communication = TeamCreate OK; agents work independently = fan-out violation)
- Misuses are flagged with a clear rationale referencing the decision rule
- Approved fixes are applied — misuses converted to fan-out (individual Agent spawns)
- No regressions: fixed skills retain correct behavior post-conversion

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

- `~/.claude/rules/spawning-patterns.md` — the fan-out vs TeamCreate decision rule being audited

_DRAFT — additional references will be added by create-story._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
