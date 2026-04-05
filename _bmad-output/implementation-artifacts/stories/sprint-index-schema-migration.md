---
title: Sprint Index Schema Migration — Add Status and Retro Fields
story_key: sprint-index-schema-migration
status: backlog
epic_slug: greeting-redesign
depends_on: []
touches:
  - _bmad-output/implementation-artifacts/sprints/index.json
change_type: config-structure
---

# Sprint Index Schema Migration — Add Status and Retro Fields

## Description

Architecture Decision 36 defines a sprint lifecycle state machine (planning →
ready → active → done → completed). The current `sprints/index.json` is missing
several fields that the state machine expects: active and planning sprint entries
lack explicit `status` fields, the planning entry lacks a `slug`, and the
completed entry lacks a `retro_run_at` timestamp.

This story migrates the existing data by adding these fields. The change is
purely additive — no existing fields are changed or removed.

## Acceptance Criteria

1. The active sprint object in `sprints/index.json` has a `"status": "active"`
   field.
2. The planning sprint object in `sprints/index.json` has a
   `"status": "planning"` field.
3. The planning sprint object has a `"slug"` field following the same naming
   convention as active and completed sprints (derived from the sprint date).
4. The completed sprint entry has a `"retro_run_at": "2026-04-04"` field
   alongside its existing `"completed"` field.
5. No existing fields are modified or removed — the migration is strictly
   additive.
6. After migration, the `sprints/index.json` file is valid JSON.

## Dev Notes

### Target file

`_bmad-output/implementation-artifacts/sprints/index.json`

### Fields to add

| Sprint entry | Field to add | Value |
|---|---|---|
| Active sprint object | `"status"` | `"active"` |
| Planning sprint object | `"status"` | `"planning"` |
| Planning sprint object | `"slug"` | Derive from sprint date using existing convention |
| Completed sprint entry | `"retro_run_at"` | `"2026-04-04"` |

### What NOT to change

- No existing field values should be modified
- No fields should be removed
- No structural changes to the JSON shape beyond adding the new keys
- Other index files (stories/index.json, etc.) are not touched

### Validation

After editing, confirm the file parses as valid JSON and all four additions are
present. A quick `python3 -m json.tool` or `jq .` check is sufficient.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
