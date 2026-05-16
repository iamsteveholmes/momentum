---
title: routing-table-schema-and-implementation
story_key: routing-table-schema-and-implementation
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
story_type: feature
depends_on: [agent-builder-skill]
touches: []
---

# routing-table-schema-and-implementation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a machine-readable routing table (`momentum/agents.json`) that maps file patterns to agent slug, agent path, and write_permissions,
so that every Momentum skill can dynamically resolve the correct agent(s) for any given file rather than hardcoding agent names.

## Description

Define and implement `momentum/agents.json` — the routing table schema for the agent composition pipeline. The routing table is machine-readable and maps file patterns to an agent slug, agent path, and write_permissions. It contains two sections:

- **defaults block**: plugin base entries that ship with the Momentum plugin and define core agent routing.
- **project entries**: added dynamically by agent-builder when a project-specific agent is registered.

Every skill in Momentum resolves 1..N agents from this table based on relevant files, using pattern matching — not hardcoded agent names.

Resolution algorithm: pattern match against file paths → return `{slug, agent_path, write_permissions}`.

Per DEC-023 (agent routing table decision). This story is foundational and unblocks:
- `specialist-classify-multi-result`
- `change-type-routing-in-sprint-dev`

Source: triage handoff `agent-architecture-triage-2026-05-16.md` (DEC-023).

**Pain context:** Skills currently hardcode agent names, which means adding or changing agents requires editing every skill. The routing table centralizes agent resolution so skills are decoupled from specific agent identities. Without this, the agent composition pipeline cannot function — it is the load-bearing schema layer.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `momentum/agents.json` exists with a defined JSON schema documenting all required fields
- Schema includes a `defaults` block with plugin-shipped base agent entries
- Schema includes a `project` block for project-specific entries added by agent-builder
- Each entry maps: file pattern → `{slug, agent_path, write_permissions}`
- A resolution function/utility accepts a list of file paths and returns matching `{slug, agent_path, write_permissions}` entries
- Pattern matching supports glob-style file patterns
- Skills can call the resolver without hardcoding agent names
- Defaults block is included in the plugin distribution
- agent-builder can write project entries to the `project` block without touching `defaults`

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

- DEC-023 — agent routing table decision
- `agent-architecture-triage-2026-05-16.md` — triage handoff source

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
