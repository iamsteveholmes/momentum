---
title: "Impetus orientation — active-sprint detection and cross-repo git state"
story_key: impetus-orientation-active-sprint-and-cross-repo-git-state
status: backlog
epic_slug: stay-oriented-impetus
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# Impetus orientation — active-sprint detection and cross-repo git state

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Impetus to check for an active sprint before suggesting sprint planning, and to scan all related repos for uncommitted/unpushed state at session start,
so that I am never misled by stale orientation and can trust Impetus's session summary reflects true project state across all repos.

## Description

momentum:impetus must make two orientation improvements:

(a) **Active-sprint detection:** Before proposing "plan a sprint," Impetus must check `sprints/index.json` for an active sprint. If one exists, it should orient the developer to the active sprint instead of suggesting planning.

(b) **Cross-repo git state:** At session start, Impetus must scan all related repos — configured via the project's CLAUDE.md or a sibling-repo list — for uncommitted or unpushed changes, and surface any dirty state as part of the session orientation summary.

**Touches:** `skills/momentum/skills/impetus/workflow.md`

**Pain context:** Auditor-human H1 ('Why are you saying plan the sprint?' when an active sprint already existed), H23 ('Is everything committed and pushed in ALL nornspun repos?') from nornspun sprint-2026-04-12 retro. Signal type: Workflow.

**Source:** triage — nornspun sprint-2026-04-12 retro handoff

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- When an active sprint exists in `sprints/index.json`, Impetus does NOT suggest "plan a sprint" — it orients to the active sprint instead
- When no active sprint exists, Impetus may suggest planning as before
- At session start, Impetus scans all related repos (from CLAUDE.md config or sibling-repo list) for uncommitted and unpushed changes
- If dirty state is found in any repo, Impetus surfaces it prominently in the session orientation summary
- If no related repos are configured, Impetus scans only the current repo

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

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
