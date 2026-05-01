---
title: "momentum:dev — Previous Story Context Injection for depends_on Stories"
story_key: dev-previous-story-continuity
status: backlog
epic_slug: story-cycles
depends_on: []
touches:
  - skills/momentum/skills/dev/workflow.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Provenance as Infrastructure"
---

# momentum:dev — Previous Story Context Injection for depends_on Stories

## Story

As a Momentum dev agent executing a story with dependencies,
I want the completed spec of my predecessor story injected as context before implementation begins,
so that I build correctly on what was actually delivered, not on what was planned.

## Description

When a story's `depends_on` list is non-empty, the dev agent today reads only its own story file. It has no visibility into what the prior story actually produced — the completed spec, the files it touched, the patterns it established. This causes unnecessary re-discovery and occasional pattern drift between related stories.

The fix: in `momentum:dev` Step 6 (before invoking bmad-dev-story), load the completed story file(s) from `depends_on` and extract their Completion Notes and File List sections. Append as "Prior Story Context" to the bmad-dev-story briefing.

This is the "previous story continuity" pattern from BMad 6.3.0's quick-dev changes, applied to Momentum's dependency-aware execution model.

Identified in the 2026-04-10 BMad 6.3.0 impact analysis session.

## Acceptance Criteria

### AC1: depends_on stories are loaded before bmad-dev-story invocation
- In momentum:dev Step 6, before bmad-dev-story is invoked, the workflow checks if the current story's `depends_on` list is non-empty
- For each story slug in `depends_on`, locate the corresponding story file in `implementation_artifacts/stories/`
- If the story file exists and its status is `done` or `review`, load it

### AC2: Completion Notes and File List are extracted and injected
- From each loaded prior story file, extract: Completion Notes List and File List sections (from Dev Agent Record)
- Append these as a "Prior Story Context" block in the dev agent's briefing prompt
- If a depends_on story file does not exist or has no Completion Notes, skip it silently (no error)

### AC3: Prior story context does not override current story spec
- The current story's ACs and tasks remain authoritative
- Prior story context is labeled clearly as reference material, not instructions
- The dev agent reads both but implements against the current story's ACs only

### AC4: No change to stories without depends_on
- When `depends_on` is empty (`[]`), Step 6 is unchanged — no file reads, no context injection
- Zero overhead on the common case

## Tasks / Subtasks

- [ ] Task 1 — Add depends_on context loading to dev/workflow.md Step 6 (AC: 1)
  - [ ] Before bmad-dev-story invocation: check if depends_on is non-empty
  - [ ] For each slug: resolve path as `{{implementation_artifacts}}/stories/{{slug}}.md`
  - [ ] Load file if it exists and status is done or review
- [ ] Task 2 — Extract and format prior story context (AC: 2)
  - [ ] Extract Completion Notes List and File List from Dev Agent Record section
  - [ ] Format as labeled "Prior Story Context: {{slug}}" block
  - [ ] Append to bmad-dev-story prompt after current story content
- [ ] Task 3 — Verify current story spec priority (AC: 3)
  - [ ] Prior context block is labeled as "reference" — wording in workflow step makes this explicit
- [ ] Task 4 — Verify no-op for empty depends_on (AC: 4)
  - [ ] Add eval or manual test confirming Step 6 is unchanged when depends_on is []

## Dev Notes

### Implementation scope
Single file: `skills/momentum/skills/dev/workflow.md`. One conditional block added to Step 6 before bmad-dev-story invocation. No changes to bmad-dev-story, stories/index.json, or story template.

### What "completed spec" means here
The Completion Notes List and File List in the Dev Agent Record section. These capture what was actually built — not what was planned. This is the authoritative record of prior story output.

### Key decision
Scope is limited to done/review stories. In-progress stories (where the prior dev agent is still running) are excluded — their completion notes are not yet final.

### References
- [Source: session 2026-04-10] — bmad-quick-dev 6.3.0 pattern analysis (previous story continuity)
- [Source: README.md#Provenance as Infrastructure] — derives_from chains as navigable infrastructure

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
