---
title: Replace static Impetus menu with state-aware action surface that names the next move and active features
story_key: impetus-state-aware-action-surface
status: backlog
epic_slug: impetus-ux-redesign
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Replace static Impetus menu with state-aware action surface that names the next move and active features

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Impetus session menu to name the actual next story, wave, or blocker as the primary action and surface the top features by activity,
so that orientation feels intelligent and Impetus-aware of what I'm working on, not like a generic static menu that could belong to any agent.

## Description

The current Impetus session menu uses a static state→menu lookup (see Menu Table in
`skills/momentum/references/session-greeting.md`) that maps 9 sprint states to
hard-coded 3–4 item menus. Across all states, the dispatch table routes to only 6
of the 24 sibling Momentum skills. The entire feature taxonomy
(`feature-grooming`, `feature-status`, `feature-breakdown`), strategic capture
(`decision`, `assessment`), backlog hygiene (`distill`, `research`,
`epic-grooming`), and the quality flywheel (`avfl`, `upstream-fix`,
`agent-guidelines`, `quick-fix`) are unreachable from the session menu.

Beyond the invisibility, the menu never names what the developer is actually
working on. "Continue the sprint" is identical whether the next move is a
two-minute fix-up merge or a blocked epic-spanning story.

This story replaces the static table with a sprint-state-aware action surface
that:
- Names the actual next story / wave / blocker as the primary action
- Surfaces the top 3 features by activity (or by `stories_remaining` at sprint boundaries) as a first-class orientation axis
- Adds an in-context "Look around" affordance for read-only browsing of decisions / retros / features / recent stories
- Routes to the full set of capabilities a "practice orchestrator" should expose

**Pain context:** Developer reports over a month of feeling Impetus "doesn't refer to features" and "doesn't seem to know anything." Quality analysis (bmad-agent-builder, 2026-04-19, finding H2) rated this HIGH — capability blindness is a structural symptom that cannot be repaired with prompt-level edits. The menu needs a redesign.

Dependencies: This story assumes `preflight-context-envelope` has shipped (the action surface needs feature/story/journal context to render against). If sprint-planned before that, scope must include a minimal inline context fetch or block on the envelope story.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The session menu's first item names a concrete next action: a specific story slug, an in-progress wave, a blocked work item, or an explicit "plan a sprint" when no sprint is active
- The menu surfaces the top 3 features by activity (or by `stories_remaining` at sprint boundaries) with each feature's current state visible
- A "Look around" menu item routes to a read-only browse of decisions / retros / features / recent stories
- Dispatch routes cover the full practice-orchestrator surface — at minimum: sprint-dev, sprint-planning, refine, triage, retro, feature-grooming, feature-status, feature-breakdown, decision, assessment, intake, distill, research, epic-grooming, avfl, upstream-fix, agent-guidelines, quick-fix
- The menu is sprint-state-aware — distinct shapes for active-in-progress vs active-blocked vs done-retro-needed are preserved but each with state-aware primary action
- Existing menu-behavior evals are updated in lockstep (estimate: 40+ evals in `skills/momentum/skills/impetus/evals/` touching menu rendering)
- New evals added asserting: primary action names a concrete thing; feature list is present; "Look around" works; all 18+ sibling skills are reachable from at least one state

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

Origin: bmad-agent-builder quality analysis report, `_bmad-output/reports/impetus/quality-analysis/2026-04-19-141047/quality-report.md`, opportunity H2 "Capability blindness — 18 of 24 sibling skills invisible from every menu."

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
