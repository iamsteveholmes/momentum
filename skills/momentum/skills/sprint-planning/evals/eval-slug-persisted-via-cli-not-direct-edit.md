# Eval: Sprint Slug Persisted via momentum-tools CLI, Not a Direct Index Edit

## Setup

A `momentum:sprint-planning` session reaches Step 2 (Story selection). The developer has
selected 2 stories, and the workflow has just generated `{{sprint_slug}}` (e.g.
`sprint-2026-07-20`).

## Expected Behavior

1. Immediately after generating `{{sprint_slug}}`, the workflow registers the selected
   stories AND persists the slug in the same `momentum-tools` call:
   `momentum-tools sprint plan --operation add --stories <slugs> --slug {{sprint_slug}}`
2. Reading `.momentum/sprints/index.json` right after this step shows
   `planning.slug == "sprint-2026-07-20"` — a real value, never absent and never the
   literal string `"unknown"`.
3. At no point later in the run (including Step 8's "edit directly" block at sprint
   activation) does the workflow write or overwrite `planning.slug` via a direct
   Write/Edit of `sprints/index.json`. The Step 8.B block updates `team`, `waves`, and
   `planned` directly, but does not touch `slug` — a comment in that block notes the slug
   was already persisted durably in Step 2.
4. If the session's context were reset immediately after Step 2 (e.g. a `/model` switch),
   re-reading `sprints/index.json` still recovers `{{sprint_slug}}`, because it was written
   through `momentum-tools` at the moment it was first known, not held only as an
   in-memory workflow variable.

## Verification

- `grep -n "slug: {{sprint_slug}}"` (or any direct-edit line naming the slug) against
  `sprint-planning/workflow.md` returns no matches anywhere in the file.
- The only place `{{sprint_slug}}` is written into `sprints/index.json` is via the
  `momentum-tools sprint plan --slug` call in Step 2.
- `sprints/index.json`'s `planning.slug` field is populated before Step 3 begins, not just
  before Step 8.
