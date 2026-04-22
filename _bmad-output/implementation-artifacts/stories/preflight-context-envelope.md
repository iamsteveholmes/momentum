---
title: Preflight returns a context envelope of ingested project state, not just rendered greeting strings
story_key: preflight-context-envelope
status: backlog
epic_slug: impetus-ux-redesign
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Preflight returns a context envelope of ingested project state, not just rendered greeting strings

<!-- INTAKE STUB -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready._

## Story

As a developer,
I want Impetus's startup preflight to return a context envelope of ingested project state (feature names, active sprint story slugs and statuses, last 3 journal threads with `context_summary_short`),
so that Impetus can reason substantively about my work during the session — naming features, referring to stories, recalling recent threads — instead of only reciting a pre-rendered greeting.

## Description

The current `momentum-tools session startup-preflight` script aggressively
pre-renders the greeting narrative / menu / closer in Python and returns
summary-shaped fields. `feature_status.summary` is a count string (e.g., "21
features: 2 working, 7 planned…") with no feature names. Journal state is
collapsed to a boolean `has_open_threads`. Active sprint stories and the
in-flight wave are not in the payload. The LLM has zero substantive knowledge
after the greeting — it can recite the rendered text but has no material to
reason over for follow-ups.

This is the mechanical root of the developer's "he doesn't refer to features,
doesn't seem to know anything" complaint. Quality analysis called this the
**scope failure of the preflight contract**, not a delivery failure.

This story extends the preflight return with a "context envelope" alongside the
existing rendering payload:
- Active sprint's story slugs + statuses (bounded list — e.g., in_progress + next 3 ready-for-dev)
- Top 5–8 features by activity (by `stories_in_progress`, else by recent commit activity)
- Last 3 journal threads (open or closed) with their `context_summary_short`
- Current sprint state + sprint slug
- Anchor timestamps (last retro, last sprint activation) for temporal orientation

SKILL.md happy path documents the envelope and instructs the agent to reason
over it during conversation. The persona file is loaded on the happy path (see
sibling story `load-impetus-persona-on-happy-path-so-voice-is-in-context`) so
the envelope is interpreted in voice.

**Pain context:** "Feels uninformed" is the single most persistent symptom in a month of use. Quality analysis (bmad-agent-builder, 2026-04-19, finding H3) rated this HIGH. Token cost estimate from the analysis: ~400–600 tokens per startup — negligible against the quality improvement.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `momentum-tools session startup-preflight` returns a `context` object alongside the existing `greeting` payload
- `context.features` includes feature slugs + names + states for top 5–8 features by activity
- `context.sprint_stories` includes the active sprint's story slugs + titles + statuses for the in-progress plus next 3 ready-for-dev
- `context.recent_threads` includes the last 3 journal threads (open or closed) with `context_summary_short` and `phase`
- `context.anchors` includes last retro timestamp, last sprint activation, current sprint slug
- SKILL.md happy path documents how to reason over the envelope (e.g., "use feature names when referencing what the developer worked on; reference story slugs by their human name from the envelope")
- Token budget: envelope adds < 800 tokens to preflight return on a realistic repo
- Existing greeting rendering is unchanged — envelope is additive
- New evals assert: Impetus names at least one specific feature when relevant; Impetus refers to an active story by its human-facing title after the greeting; Impetus can answer "what was I working on last time?" from the envelope

> Note: Rough starting points — create-story will validate.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT._

### Testing Requirements

_DRAFT._

### Implementation Guide

_DRAFT._

### Project Structure Notes

_DRAFT._

### References

Origin: bmad-agent-builder quality analysis report, `_bmad-output/reports/impetus/quality-analysis/2026-04-19-141047/quality-report.md`, opportunity H3 "Preflight returns rendered output, not ingested context — root of 'feels uninformed'."

## Dev Agent Record

_DRAFT._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
