---
title: Persist scope boundaries across sessions
story_key: persist-scope-boundaries-across-sessions
status: backlog
epic_slug: momentum-impetus-session-orientation
story_type: feature
priority: medium
depends_on: []
---

# Persist scope boundaries across sessions

## Story
Scope boundaries the developer asserts must be written into handoff state and honored by later sessions, so the developer stops re-asserting them.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): the developer re-asserted "planning is out of scope" at least 3× across 3 days (Msgs [27], [52], [23]); no scope guardrail survived handoffs. Pairs with the "Specification Fatigue" pattern.

## What's needed
- Explicit scope boundaries are written into handoff state at session end.
- Session start loads and honors recorded scope boundaries.
- An agent proposing out-of-scope work against a recorded boundary self-corrects before surfacing it.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related: `plain-anchor-and-durable-handoff-on-returning-turns` (the durable-handoff artifact this writes into), `session-handoff-prompt-as-artifact`
