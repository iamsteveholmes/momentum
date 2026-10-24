---
title: Give the story surface field a sanctioned write path (create-story elicitation, --surface flag, schema row)
story_key: give-story-surface-field-a-sanctioned-write-path
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Give the story surface field a sanctioned write path (create-story elicitation, --surface flag, schema row)

<!-- INTAKE STUB: captured by momentum:intake. Not dev-ready; run momentum:create-story. -->

## Story

As a developer,
I want the story surface field to have a sanctioned write path,
so that surface-keyed verification routing (DEC-040 D7) stops falling through to change_type inference.

## Description

From sprint-2026-08-03 end-gate (Option A). Consumers prefer a declared surface, but create-story Step 5 only reads frontmatter (no elicitation), story-add has no --surface flag, and sprint-tracking-schema.md omits surface. Every story falls through to change_type inference, the routing that caused the backend-to-curl misroute. An interim hand-declaration note exists in verification-standard.md.

**Pain context:** Every story silently uses change_type inference.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- create-story asks for surface when inference is ambiguous or overridden
- --surface flag on story-add (or story-set-surface) keeping sprint-manager sole writer of index.json
- Schema-doc row for surface in skills/momentum/references/sprint-tracking-schema.md

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
