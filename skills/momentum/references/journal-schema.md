# Journal Schema Reference

The session journal lives at `.claude/momentum/journal.jsonl`. It tracks open threads across sessions and tabs, enabling session orientation and workflow resumability.

## Format

JSONL (JSON Lines) — one JSON object per line, append-only. Never overwrite or modify existing lines.

## Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `thread_id` | string | yes | Unique identifier, format `T-NNN` (auto-incrementing) |
| `workflow_type` | string | yes | Type of workflow (e.g., `story-cycle`, `ux-design`, `architecture-research`) |
| `story_ref` | string | no | Story identifier if applicable (e.g., `4.2`) |
| `current_step` | string | yes | Current workflow step name |
| `phase` | string | yes | Human-readable phase label (e.g., `mid-review`, `early-design`) |
| `last_action` | string | yes | Last completed action description |
| `context_summary` | string | yes | One sentence with enough context to re-orient a developer in a fresh session without re-reading the story file |
| `last_active` | string | yes | ISO 8601 timestamp of last activity |
| `status` | string | yes | `open` or `closed` |
| `depends_on_thread` | string | no | Thread ID this thread is waiting on (e.g., `T-001`), or `null` |

## Example Entry

```jsonl
{"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Code reviewer dispatched","context_summary":"Story 4.2 implementation — reviewer is analyzing the null-check pattern","last_active":"2026-03-21T14:30:00Z","status":"open","depends_on_thread":null}
```

## Write Semantics

Every state change appends a new line:
- **Thread created:** First entry with a new `thread_id`, `status: "open"`
- **Step advanced:** New entry with same `thread_id`, updated `current_step`, `phase`, `last_action`, `context_summary`, `last_active`
- **Thread closed:** New entry with same `thread_id`, `status: "closed"`

Never modify or delete existing lines. The journal is an append-only log.

## Read Semantics

1. Read all lines from `journal.jsonl`
2. Group entries by `thread_id`
3. For each `thread_id`, take the **last** entry — this is the current state
4. Filter by `status: "open"` for active threads
5. Sort by `last_active` descending (most recent first)

## Thread ID Assignment

When creating a new thread:
1. Read all existing entries
2. Find the highest `T-NNN` number
3. Assign `T-{NNN+1}` (zero-padded to 3 digits)
4. If no entries exist, start at `T-001`

## Context Summary Guidelines

The `context_summary` field must contain enough information for re-orientation without re-reading source files.

- **Good:** "Story 4.2 — the null-check pattern was flagged by the reviewer; 3 findings remain to address."
- **Bad:** "Working on story." (too vague to re-orient)

One sentence, specific, actionable.

## Journal View Auto-Generation

After every append to `journal.jsonl`, regenerate `.claude/momentum/journal-view.md` as a human-readable markdown table of all entries (open and recently closed within last 7 days). This file is read-only for developers — Impetus only reads/writes the JSONL source.

## Concurrency

JSONL append is concurrency-safe for lines under POSIX pipe buffer size (typically 4096 bytes). No file locking is needed for writes. Multiple tabs can safely append simultaneously.
