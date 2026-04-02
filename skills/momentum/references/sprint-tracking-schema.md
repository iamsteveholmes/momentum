# Sprint Tracking Schema Reference

> Source of truth: `_bmad-output/planning-artifacts/architecture.md` — Sprint Tracking Schema section.

## stories/index.json

Flat lookup index. One entry per story, keyed by slug.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Current story status |
| `title` | string | Human-readable story title |
| `epic_slug` | string | Epic this story belongs to |
| `story_file` | boolean | Whether a fleshed-out story file exists |
| `depends_on` | string[] | Story slugs that must be `done` before this story can start |
| `touches` | string[] | Paths this story modifies (merge conflict risk indicator) |

### Valid Story Statuses

| Status | Meaning |
|--------|---------|
| `backlog` | Story only exists in epic file (no story file yet) |
| `ready-for-dev` | Story file created; awaiting development |
| `in-progress` | Developer actively working on implementation |
| `review` | Ready for code review |
| `verify` | Verification in progress |
| `done` | Story completed and merged |
| `dropped` | Story cancelled before development began |
| `closed-incomplete` | Story abandoned mid-execution |

### Example Entry

```json
{
  "posttooluse-lint-hook": {
    "status": "in-progress",
    "title": "PostToolUse Lint and Format Hook Active",
    "epic_slug": "quality-enforcement",
    "story_file": true,
    "depends_on": [],
    "touches": ["skills/momentum/references/hooks/"]
  }
}
```

## sprints/index.json

Sprint lifecycle index. Tracks which sprint is active, which is in planning, and which are completed.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `active` | string or null | Slug of the active sprint (null if none) |
| `planning` | object or null | Planning sprint state |
| `planning.locked` | boolean | Whether the planning sprint is locked |
| `completed` | string[] | Slugs of completed sprints |

### Example (no active sprint)

```json
{
  "active": null,
  "planning": {
    "locked": false
  },
  "completed": []
}
```

### Example (active sprint)

```json
{
  "active": "quality-hooks-sprint",
  "planning": {
    "name": "Impetus UX Sprint",
    "slug": "impetus-ux-sprint",
    "stories": ["impetus-identity-redesign"],
    "locked": false
  },
  "completed": ["foundation-sprint"]
}
```

## Sprint File (sprints/{slug}.json)

When an active sprint exists, its detail lives in a separate file.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable sprint name |
| `slug` | string | Sprint slug |
| `stories` | string[] | Story slugs in this sprint |
| `locked` | boolean | Whether the sprint is locked (no story adds/removes) |
| `started` | string | ISO date sprint started |
| `completed` | string or null | ISO date sprint completed (null if in progress) |
| `waves` | object[] | Wave plan for parallel execution |

## Write Authority

`momentum-sprint-manager` is the sole writer of:
- `sprints/index.json` and all files in `sprints/`
- `status` fields in `stories/index.json`

`momentum-create-story` writes:
- Story stub files in `stories/`
- New entries to `stories/index.json` (status, title, epic_slug, depends_on, touches)

No other agent or script writes to these files directly.

## Story Stub Files (stories/{slug}.md)

Minimal markdown files created at backlog stage:

```markdown
# {title}

Status: {status}
Epic: {epic_slug}
```

Fleshed out with full ACs, dev notes, and tasks during sprint planning via `momentum-create-story`.

## Epic Membership

Epic membership is tracked in `stories/index.json` via the `epic_slug` field — not in `epics.md`. The `epics.md` file contains only epic names, slugs, and descriptions.
