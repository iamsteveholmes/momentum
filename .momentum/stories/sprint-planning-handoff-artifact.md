---
title: Add mandatory handoff artifact to sprint-planning workflow terminal step
story_key: sprint-planning-handoff-artifact
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: practice
priority: high
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
---

# Add mandatory handoff artifact to sprint-planning workflow terminal step

<!-- PLANNING STUB: Seeded by sprint-planning 2026-07-13 (index entry existed with no
     story file). All sections below marked DRAFT require full rewrite by create-story
     before development. -->

_This story is a planning-seeded stub. Run `momentum:create-story` on it to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-planning's terminal step to emit a mandatory handoff artifact into
`.momentum/handoffs/` summarizing the activated sprint — goal, stories, waves, contract
locations, and where sprint state lives,
so that the build session (a fresh `/momentum:conduct` session, per the
fresh-session-before-major-workflows practice) starts from a durable bridge instead of
re-deriving planning context or losing it to session boundaries.

## Description

Sprint-planning currently ends at activation with no durable handoff; the practice's
handoff-conventions rule (`.claude/rules/handoff-conventions.md`) names retro, assessment,
decision, and sprint-dev as handoff writers but planning emits nothing. Major workflows are
run in fresh sessions, so planning context (sprint goal per DEC-039, wave rationale,
ride-along cautions) evaporates unless carried by an artifact. The 2026-06-28 retro corpus
flagged this as a terminal-step gap (related, unselected story:
`sprint-planning-activation-gate` — the two were noted as likely one terminal-step story;
this story takes the handoff-artifact scope only).

Handoffs are use-then-discard bridging docs — the artifact must follow the
`<topic>-<YYYY-MM-DD>.md` naming convention and is deleted after consumption.

## Acceptance Criteria

<!-- DRAFT: rough criteria captured at planning. This section MUST be fully rewritten by
     create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

1. sprint-planning's terminal step (activation) writes a handoff artifact to
   `.momentum/handoffs/` before declaring the sprint live.
2. The artifact carries: sprint goal (DEC-039), story list with waves, contract/spec
   locations, and any planning-time cautions the build must honor.
3. The workflow treats the artifact as mandatory — activation output names the artifact path.

## References

- Rule: .claude/rules/handoff-conventions.md
- DEC-039 D1 (sprint goal stored in sprint record, carried to build)
- Handoff: refine-complete-2026-07-10 (developer-directed sprint-planning fixes)
