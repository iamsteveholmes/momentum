---
title: Write an interim pending resume card during the end-gate request-changes fix pass
story_key: write-interim-pending-resume-card-during-end-gate-fix-pass
status: backlog
epic_slug: ad-hoc
feature_slug: 
story_type: defect
depends_on: []
touches: [skills/momentum/skills/conductor/workflow.md]
---

# Write an interim pending resume card during the end-gate request-changes fix pass

<!-- INTAKE STUB: captured by momentum:intake. NOT dev-ready. -->

_Backlog stub. Run `momentum:create-story` on it when ready to make it dev-ready._

## Story

As a developer,
I want the conductor to leave a pending resume card on disk for the whole request-changes fix pass,
so that an interrupted session still shows the unresolved end-gate in Impetus's next greeting.

## Description

Finding DOM-A-4-001 (major, stakes_class routine, AVFL residual) from the sprint-2026-08-03 build, story conduct-resume-card-impetus-pending-gate-agenda-session.

RESUME-CARD RESOLVE fires the instant the developer picks "request changes" at the end-gate, but the next resume-card write does not happen until the entire 5.RC.1-3 autonomous fix pass completes (multi-agent, retry-bound, interruption-prone). The next RESUME-CARD REFRESH comes only at re-render. If the session dies mid-pass, the on-disk card stays status resolved / changes-requested, so Impetus's next session greeting shows no pending gate even though the gate was never re-presented. This is the silent-gate failure the resume card exists to prevent.

Evidence: skills/momentum/skills/conductor/workflow.md, RESUME-CARD RESOLVE in the request-changes branch. A grep for RESUME-CARD shows no card-write actions between it and the post-pass REFRESH; the 5.RC.1-3 parse/dispatch/fix-budget steps in between contain only ledger appends.

Suggested fix: write an interim pending card (phase "end-gate-fix-pass", an informational no-action question such as "a requested change pass was interrupted - resume the conduct run to finish it and re-present the gate") immediately after RESOLVE fires, refreshed per fix-pass iteration, replaced by the normal pending card at re-render.

**Pain context:** Silent loss of a pending gate across a session death; the developer is never told the gate is outstanding. Shape of the card must still satisfy the resume-card.md seam contract (Anti-Expiry Invariant, Impetus shared-write fields).

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- After RESUME-CARD RESOLVE in the request-changes branch, an interim card with status pending and phase "end-gate-fix-pass" is written before 5.RC.1 begins.
- The interim card is refreshed on each fix-pass iteration.
- The normal pending card replaces it at re-render.
- A session killed mid-pass leaves a pending card that Impetus surfaces on the next start.

> Note: The ACs above are rough captures from conversation. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation
