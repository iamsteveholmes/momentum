---
title: change-type-routing-in-sprint-dev
story_key: change-type-routing-in-sprint-dev
status: backlog
epic_slug: sprint-dev-workflow
feature_slug: momentum-sprint-orchestration
story_type: feature
depends_on: [routing-table-schema-and-implementation]
touches: []
---

# change-type-routing-in-sprint-dev

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-dev Phase 2 to read `change_type` from story frontmatter and route to the appropriate subagent or execution path,
so that skill/agent, rule/hook, docs, and feature/bug stories each follow the correct build pipeline without manual intervention.

## Description

Sprint-dev Phase 2 reads `change_type` from story frontmatter and routes accordingly:

- **skill/agent stories** → skill-building subagent (skill-creator in autonomous mode + explicit approval gate before merge)
- **rule/hook stories** → direct edit + commit (no dev agent spawn)
- **docs stories** → writer agent
- **feature/bug stories** → normal dev path (unchanged)

Per DEC-027 D3. This requires `routing-table-schema-and-implementation` to be in place for agent path resolution. The skill-building subagent path uses the existing skill-creator skill in autonomous mode with an explicit approval gate before the worktree is merged.

**Pain context:** Without change-type routing, all stories — regardless of whether they produce code, skills, rules, or docs — go through the generic dev agent path. Skill and rule changes need fundamentally different pipelines (skill-creator for skills, direct edits for rules), and conflating them leads to incorrect build artifacts and missed quality gates. DEC-027 D3 mandates this routing as part of the agent architecture redesign. Source: triage — handoff agent-architecture-triage-2026-05-16.md.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Sprint-dev Phase 2 reads `change_type` field from story frontmatter before dispatching
- Stories with `change_type: skill` or `change_type: agent` are routed to skill-creator in autonomous mode
- Skill-creator path includes an explicit developer approval gate before the worktree is merged
- Stories with `change_type: rule` or `change_type: hook` are handled via direct file edit + commit — no dev agent spawn
- Stories with `change_type: docs` are routed to a writer agent
- Stories with `change_type: feature` or `change_type: bug` (or no change_type) continue through the existing dev path unchanged
- Routing uses the routing table from `routing-table-schema-and-implementation` for agent path resolution
- If `change_type` is absent or unrecognized, falls back to the default feature/bug path with a warning

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

- DEC-027 D3 — agent architecture redesign routing table decision
- Source triage: handoff agent-architecture-triage-2026-05-16.md
- Depends on: routing-table-schema-and-implementation

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
