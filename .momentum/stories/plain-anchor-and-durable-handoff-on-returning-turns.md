---
title: Lead returning/jargon-bearing turns with a plain-language anchor and a durable session handoff
story_key: plain-anchor-and-durable-handoff-on-returning-turns
status: backlog
epic_slug: momentum-impetus-session-orientation
story_type: feature
priority: high
depends_on: []
---

# Lead returning/jargon-bearing turns with a plain-language anchor and a durable session handoff

## Story
On a returning session or any turn that surfaces internal counts/jargon, lead with a plain-language anchor before any number; and write a durable session-handoff artifact the next session reads, replacing hand-pasted prompts.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): four distinct orientation failures over five days — "remind me what we were working on?" (Msg 15); "totally lost... What is the 52 stories?" (Msg 45); "no idea what you're talking about... the existing 18 stories" (Msg 70); "I don't understand the stubs or why we're talking about beads" (Msg 86). The developer named it "Specification Fatigue" (Msg 60) and acted as the manual message bus across 4 cross-session handoffs, carrying state (the 18 stories, DEC-036 amendments, the sprint plan) by hand-pasted prompts rather than a durable artifact.

This story consolidates several existing slices into one coherent behavioral rule.

## What's needed
- On a returning session or any turn surfacing internal counts/jargon, the agent leads with a plain-language anchor before any number.
- A durable session-handoff artifact is written that the next session reads, replacing hand-pasted prompts.
- The handoff carries the live story set, active decisions, and the sprint plan.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Consolidates (dedup — collapse these slices into this coherent intent): `session-handoff-prompt-as-artifact` (durable handoff half), `add-proactive-handoff-offer-to-long-running-workflow-skills` (when to fire), `distill-jargon-definition-fix` + `hash-drift-plain-language-message` (done — plain-language slices), `impetus-lifecycle-and-handoff-fix` (adjacent — lifecycle state)
