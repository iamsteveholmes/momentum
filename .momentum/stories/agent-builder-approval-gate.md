---
title: "agent-builder: Add developer approval gate before routing entry write"
story_key: agent-builder-approval-gate
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches:
  - skills/momentum/skills/agent-builder/workflow.md
---

# agent-builder: Add developer approval gate before routing entry write

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want agent-builder to show me the composed file and evaluation summary before writing to the agents registry,
so that I can approve, request a revision, or abort without any side effects occurring.

## Description

The agent-builder workflow currently writes to `momentum/agents.json` unconditionally after skill-creator validation (Step 3 → Step 4 with no gate). The agent-builder-skill story spec (Scenarios 3, 4, 5) requires an explicit approve/revise/abort gate shown to the developer before any routing entry is written. This gap was surfaced during sprint-2026-05-16 Phase 6 verification.

The gate must:
- Surface the composed file content and skill-creator eval summary to the developer
- Offer three options: approve, revise (with feedback), abort
- Write nothing to agents.json until the developer approves
- On revise: run one improvement pass and re-present
- On abort: clean up the .draft file and exit with no side effects

**Pain context:** Without the approval gate, agent-builder writes routing entries autonomously after validation. If skill-creator passes a suboptimal file, the developer has no checkpoint before the entry lands in agents.json. The story spec explicitly requires this gate (Scenarios 3–5 of agent-builder-skill.feature).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- After skill-creator validation completes, the developer is shown the composed file content and eval summary before any write to agents.json
- Developer is offered three explicit options: approve, request revision (with feedback text), or abort
- No routing entry is written to agents.json until the developer selects approve
- On abort: the .draft file is removed, no agents.json entry is written, skill exits cleanly
- On revise: agent-builder applies the developer's feedback, runs one improvement pass, and re-presents the gate
- On re-present: developer is again offered approve/revise/abort
- On approval: the routing entry is written to agents.json and the final file is committed as before

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Sprint-2026-05-16 Phase 6 verification: agent-builder-skill Scenarios 3, 4, 5 (approve/revise/abort gate)
- `skills/momentum/skills/agent-builder/workflow.md` — Step 3 (skill-creator) → Step 4 (write) gap
- `skills/momentum/skills/agent-builder/SKILL.md`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
