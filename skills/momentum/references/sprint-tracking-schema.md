# Sprint Tracking Schema Reference

> Source of truth: `_bmad-output/planning-artifacts/architecture.md` — Sprint Tracking Schema section.

## stories/index.json

Flat lookup index. One entry per story, keyed by slug.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | yes | Current story status (see Valid Story Statuses) |
| `title` | string | yes | Human-readable story title |
| `epic_slug` | string | yes | Epic this story belongs to |
| `story_file` | boolean | yes | Whether a fleshed-out story file exists |
| `depends_on` | string[] | yes | Story slugs that must be `done` before this story can start |
| `touches` | string[] | yes | Paths this story modifies (merge conflict risk indicator) |
| `priority` | string | no | Story priority: `critical`, `high`, `medium`, `low` (default: `low`) |
| `change_type` | string | no | Present on fleshed-out stories: `code`, `skill-instruction`, `config-structure`, `rule-hook`, `specification` (or combinations with ` + `) |

### Valid Story Statuses

| Status | Meaning |
|--------|---------|
| `backlog` | Stub entry — no story file yet |
| `ready-for-dev` | Story file created with ACs; awaiting sprint selection |
| `in-progress` | Dev agent actively working on implementation |
| `review` | Merged to sprint branch — awaiting AVFL quality gate |
| `verify` | AVFL passed — behavioral verification running |
| `done` | Story completed and verified |
| `dropped` | Story cancelled — obsolete or duplicate |
| `closed-incomplete` | Sprint force-closed before story completion |

### Story Priority

| Priority | When |
|----------|------|
| `critical` | Blocks other work or has a deadline |
| `high` | Important for current goals, should be in next sprint |
| `medium` | Valuable, no urgency |
| `low` | Default — nice to have, refine when relevant |

### Example Entry

```json
{
  "posttooluse-lint-and-format-hook-active": {
    "status": "done",
    "title": "PostToolUse Lint and Format Hook Active",
    "epic_slug": "quality-enforcement",
    "story_file": true,
    "depends_on": [],
    "touches": [
      "skills/momentum/hooks/hooks.json",
      "skills/momentum/scripts/momentum-lint.sh"
    ],
    "change_type": "rule-hook + code"
  }
}
```

## sprints/index.json

Sprint lifecycle index. Tracks active, planning, and completed sprints.

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `active` | object or null | Active sprint record (null if none) |
| `planning` | object or null | Planning sprint record (null if none) |
| `completed` | object[] | Array of completed sprint records |

### Sprint Record Fields

| Field | Type | Description |
|-------|------|-------------|
| `slug` | string | Sprint identifier (e.g., `sprint-2026-04-05-2`) |
| `locked` | boolean | Whether the sprint is locked (immutable once activated) |
| `status` | string | `planning`, `active`, `done` |
| `stories` | string[] | Story slugs in this sprint |
| `waves` | object[] | Execution wave plan (see below) |
| `team_composition` | object | Per-story role assignments (see below) |
| `started` | string | ISO date sprint started |
| `completed` | string or null | ISO date sprint completed |
| `retro_run_at` | string or null | ISO date retrospective was run |

### Wave Object

```json
{
  "wave": 1,
  "stories": ["story-a", "story-b"]
}
```

Stories in the same wave can execute in parallel. Wave N stories depend on all Wave 1..N-1 stories completing.

### Team Composition Object

Per-story entry keyed by story slug:

| Field | Type | Description |
|-------|------|-------------|
| `roles` | string[] | Agent roles assigned: `dev`, `qa`, `e2e-validator`, `architect-guard` |
| `change_type` | string | Story's change type classification |
| `guidelines` | object | Per-role guideline strings |
| `test_approach` | string | Testing methodology (TDD, EDD, behavioral, inspection) |
| `wave` | number | Execution wave number |
| `dependencies` | string[] | Story slugs this story depends on within the sprint |
| `specialist` | string | Dev specialist type: `dev-skills`, `dev-build`, `dev-frontend`, or `dev` (base) |
| `guidelines_status` | string | `present`, `missing`, `skipped`, or `n/a` |

### Example (no active sprint)

```json
{
  "active": null,
  "planning": null,
  "completed": [
    {
      "locked": true,
      "status": "done",
      "slug": "sprint-2026-04-05-2",
      "stories": ["retro-skill", "journal-status-tool"],
      "waves": [{"wave": 1, "stories": ["retro-skill", "journal-status-tool"]}],
      "team_composition": { ... },
      "started": "2026-04-05",
      "completed": "2026-04-06",
      "retro_run_at": "2026-04-06"
    }
  ]
}
```

## Write Authority

`momentum-tools.py sprint` CLI is the sole writer of:
- `sprints/index.json` (sprint lifecycle transitions)
- `status` fields in `stories/index.json` (story status transitions)

`momentum:create-story` writes:
- Story files in `stories/`
- New entries to `stories/index.json` (status, title, epic_slug, depends_on, touches)

No other agent or script writes to these files directly.

## Story Stub Files (stories/{slug}.md)

Minimal markdown files created at backlog stage:

```markdown
# {title}

Status: {status}
Epic: {epic_slug}
```

Fleshed out with full ACs, dev notes, and tasks during sprint planning via `momentum:create-story`.

## Epic Membership

Epic membership is tracked in `stories/index.json` via the `epic_slug` field — not in `epics.md`. The `epics.md` file contains only epic names, slugs, and descriptions.
