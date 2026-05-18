---
title: "Add CREED behavioral anchors to ux, analyst, and researcher base bodies"
story_key: creed-blocks-for-new-base-bodies
status: backlog
epic_slug: agent-team-model
feature_slug: ""
story_type: maintenance
depends_on: []
touches:
  - skills/momentum/agents/ux.md
  - skills/momentum/agents/analyst.md
  - skills/momentum/agents/researcher.md
---

# Add CREED behavioral anchors to ux, analyst, and researcher base bodies

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the ux, analyst, and researcher base body agents to include CREED blocks,
so that each agent has explicit "I [verb] because [reason]" behavioral anchors that communicate its core commitments.

## Description

All three base body agents created in sprint-2026-05-16 (ux.md, analyst.md, researcher.md) are missing CREED blocks — statements of the form "I [verb] because [reason]" that anchor the agent's behavioral commitments. These are a standard structural pattern in Momentum agent definitions per the agent-skill-development-guide.md.

This was flagged during sprint-2026-05-16 Phase 6 structural verification. It was not in any story AC (hence low priority) but represents a consistency gap with the dev base body which does have CREED-style anchors.

**Pain context:** Agents without CREED blocks are harder for spawning prompts to align to — the "I do X because Y" statements give orchestrators a fast-path to anchor the agent's behavior in context.

## Acceptance Criteria

<!-- DRAFT -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- `skills/momentum/agents/ux.md` contains a CREED block with at least 3 "I [verb] because [reason]" statements reflecting its core constraints (scope to UX artifacts, surface unknowns, no implementation decisions)
- `skills/momentum/agents/analyst.md` contains a CREED block with at least 3 statements (inform not decide, source all claims, write only to analysis/decisions dirs)
- `skills/momentum/agents/researcher.md` contains a CREED block with at least 3 statements (cite all sources, distinguish evidence from inference, surface gaps rather than invent)
- CREED blocks are positioned consistently with existing agent convention (check dev.md for placement reference)
- Total file line counts remain within the 200-400 line guideline after addition

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- `skills/momentum/agents/dev.md` — reference for CREED block placement and format
- `skills/momentum/references/agent-skill-development-guide.md` — CREED block conventions
- Sprint-2026-05-16 Phase 6 structural verification finding

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
