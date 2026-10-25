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
| `status` | string | `planning`, `active`, `done`, `failed` (DEC-040 D3 — `failed` is an honest terminal state, not an error; see Sprint Closure Gate below) |
| `stories` | string[] | Story slugs in this sprint |
| `waves` | object[] | Execution wave plan (see below) |
| `team_composition` | object | Per-story role assignments (see below) |
| `goal` | string | Plain-language sprint purpose, declared at planning (`sprint plan --goal`). For a maintenance sprint (no `goal_conditions`), this string also carries the verified-fix list as `- ` bullet lines following a `Verified fixes:` lead-in line — there is no separate structured fix-list field. |
| `goal_conditions` | string[] | Feature slugs (keys into `.momentum/features.json`; each must already be registered via `momentum-tools feature register` — today a developer act done before planning; wiring register into planning is a follow-up) whose acceptance conditions this sprint intends to flip to passing, declared at planning (`sprint plan --goal-conditions`). `[]` (or the key absent) means a maintenance sprint — its equivalent gate is the verified-fix list inside `goal` instead. Missing key and `null` are both treated as `[]` everywhere this field is read. |
| `started` | string | ISO date sprint started |
| `completed` | string or null | ISO date sprint completed |
| `retro_run_at` | string or null | ISO date retrospective was run |
| `closure` | object | Present only on a closed sprint record (in `completed[]`); written once by the sprint closure gate. See Sprint Closure Gate below. |

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
| `roles` | string[] | Agent roles assigned: `dev`, `qa-reviewer`, `e2e-validator`, `architect-guard` |
| `change_type` | string | Story's change type classification |
| `guidelines` | object | Per-role guideline strings |
| `test_approach` | string | Testing methodology (TDD, EDD, behavioral, inspection) |
| `wave` | number | Execution wave number |
| `dependencies` | string[] | Story slugs this story depends on within the sprint |
| `specialist` | string | Resolved agent slug from `momentum-tools agent resolve` against `agents.json`: `dev` (base body) or a composed project slug (e.g., `dev-kotlin-compose`) |
| `guidelines_status` | string | `present`, `missing`, `skipped`, or `n/a` |

### Sprint Closure Gate (DEC-040 D2/D3, tier 2)

`momentum-tools sprint complete` is a **gate**, not an unconditional closer. It refuses (non-zero
exit, `active` left untouched, nothing appended to `completed[]`) unless every entry in the
sprint's `goal_conditions` carries a recorded human verdict in `.momentum/features.json` (written only by `momentum-tools feature verify`; `feature register` creates entries at status `absent` and never writes a verdict) — or, for
a maintenance sprint declaring no conditions, its verified-fix list (parsed from `goal`) is
confirmed via repeatable `--fix-confirmed` plus `--build`. This is tier 2 of the two-tier gate;
tier 1 (`conduct-merge-gate-completes-by-executing-merge-push-story`) is the separate question of
whether the code is safe to keep on trunk, and completes independently via merge + push + story
status transitions — a successful merge never implies the sprint is closed.

**Registry write authority (split).** `.momentum/features.json` has exactly two write paths, both
in `momentum-tools feature`: `register` is the sole creator of registry entries (it writes the
entry with status `absent`, `last_verified` null; it never writes `status` or `last_verified` of an
existing entry, and refuses — file byte-identical — on a duplicate slug, non-kebab-case slug, empty
name/acceptance condition, or an invalid/non-object registry), and `verify` remains the sole
writer of `status` and `last_verified`. No skill, agent, or hand edit writes the registry except by invoking one of these two subcommands. Every
other consumer (sprint planning, sprint closure, Impetus N-of-M, tasting) reads it only.

`--verdict {done,failed}` (default `done`) selects the terminal state. `failed` requires a
non-empty `--reason` and bypasses the verdict requirement above — an honest FAILED closure records
which conditions were unverified rather than pretending the goal was met. Both `done` and `failed`
require `--punt-decision <ref>` (a document under `_bmad-output/planning-artifacts/decisions/`)
whenever the sprint closes with a story at `closed-incomplete`/`dropped` while a declared condition
is not verified-pass.

Every successful closure — `done` or `failed` — writes a `closure` block onto the record appended
to `completed[]`:

```json
{
  "closure": {
    "verdict": "done",
    "conditions": [
      {
        "slug": "demo-feature",
        "state": "verified-pass",
        "reason": null,
        "status": "passing",
        "verdict": "pass",
        "backend_sha": "aaaa111",
        "client_sha": "bbbb222",
        "summary": "pass — build aaaa111:bbbb222"
      }
    ],
    "fix_confirmations": [],
    "reason": null,
    "punt_decision": null
  }
}
```

`conditions[].state` is one of `verified-pass`, `recorded-fail`, or `unverified` (with `reason`
one of the closed set `missing-entry` | `no-verdict` | `no-build-shas`). `fix_confirmations` is
populated only for a maintenance closure (one entry per confirmed verified-fix line, with the
`--build` pair). `reason` carries the FAILED reason text when `verdict == "failed"`, else `null`.
`punt_decision` carries the `--punt-decision` ref when supplied, else `null`.

`retro_run_at: null` is set identically for `done` and `failed` closures — `momentum:retro` Step 1
discovers a FAILED sprint exactly as readily as a `done` one.

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
