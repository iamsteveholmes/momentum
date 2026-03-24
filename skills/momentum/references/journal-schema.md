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
| `declined_offers` | array | no | Array of offer objects recording proactive offers the developer explicitly declined. See [Declined Offers](#declined-offers) section below. |

### Declined Offer Object Fields

Each object in the `declined_offers` array contains:

| Field | Type | Required | Description |
|---|---|---|---|
| `offer_type` | string | yes | Category of proactive offer (e.g., `dormant-closure`, `dependency-resolution`, `config-gap`, `unwieldy-triage`) |
| `description` | string | yes | What was offered, in natural language (e.g., "Close dormant thread: Story 4.2 implementation") |
| `declined_at` | string | yes | ISO 8601 timestamp of declination |
| `context_hash` | string | yes | Lightweight context fingerprint for material-change detection. Format: `thread_id\|story_ref\|phase\|git_hash` where `git_hash` is the output of `git hash-object` on the referenced story spec file (empty string if unavailable). This is a concatenated equality-check string, not a cryptographic hash. |

## Example Entry

```jsonl
{"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Code reviewer dispatched","context_summary":"Story 4.2 implementation — reviewer is analyzing the null-check pattern","last_active":"2026-03-21T14:30:00Z","status":"open","depends_on_thread":null}
```

### Example Entry with Declined Offers

```jsonl
{"thread_id":"T-002","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Declined dormant closure","context_summary":"Story 4.2 implementation — developer declined dormant closure, keeping thread open","last_active":"2026-03-24T10:00:00Z","status":"open","depends_on_thread":null,"declined_offers":[{"offer_type":"dormant-closure","description":"Close dormant thread: Story 4.2 implementation","declined_at":"2026-03-24T10:00:00Z","context_hash":"T-002|4.2|mid-review|2026-03-23"}]}
```

## Write Semantics

Every state change appends a new line:
- **Thread created:** First entry with a new `thread_id`, `status: "open"`
- **Step advanced:** New entry with same `thread_id`, updated `current_step`, `phase`, `last_action`, `context_summary`, `last_active`
- **Thread closed:** New entry with same `thread_id`, `status: "closed"`

Never modify or delete existing lines. The journal is an append-only log.

### Declined Offers Write Semantics

When a developer explicitly declines a proactive offer (responds "No", "Skip", or "Continue as planned"):
1. Append a new journal entry for the affected thread
2. Copy all current thread state fields from the thread's last entry
3. Update `last_action` to describe the declination (e.g., "Declined dormant closure")
4. Add or extend the `declined_offers` array: carry forward all existing `declined_offers` from the thread's previous entry (append-only accumulation), then append a new offer object for the just-declined offer
5. Compute `context_hash` as: `thread_id|story_ref|phase|git_hash` where `git_hash` is the output of `git hash-object` on the story spec file referenced by `story_ref` (empty string if no spec file exists or `story_ref` is absent)

"Ignore" (no response) is NOT a declination — only explicit decline triggers persistence.

## Read Semantics

1. Read all lines from `journal.jsonl`
2. Group entries by `thread_id`
3. For each `thread_id`, take the **last** entry — this is the current state
4. Filter by `status: "open"` for active threads
5. Sort by `last_active` descending (most recent first)

### Declined Offers Read Semantics

At hygiene check time (Step 11), before surfacing any proactive offer for a thread:
1. Read the thread's current state (last entry per `thread_id`)
2. Check the `declined_offers` array (if present)
3. For each pending proactive offer, compute the current `context_hash` using the same formula: `thread_id|story_ref|phase|git_hash`
4. Compare the offer's `offer_type` + current `context_hash` against each entry in `declined_offers`
5. **Match found** (same `offer_type` AND same `context_hash`): suppress the offer — do not surface it
6. **No match** (either `offer_type` differs or `context_hash` differs): offer is eligible — surface it normally

### Material Change Heuristic

Context is considered materially changed when the current `context_hash` differs from the declined entry's `context_hash`. This happens when any of:
- `story_ref` changed (different story)
- `phase` advanced (e.g., `mid-review` → `late-review`)
- The story spec file content changed (different `git hash-object` output)

When context has materially changed, the prior declination no longer applies and the offer may be re-surfaced.

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

## Session Stats (installed.json)

The project-level `.claude/momentum/installed.json` file carries a `session_stats` object that tracks invocation history across sessions. This section documents the schema; the data lives in `installed.json` (not the journal JSONL).

### Fields

| Field | Type | Description |
|---|---|---|
| `session_stats.momentum_completions` | integer | Count of `/momentum` sessions that reached the session menu (Step 7). Incremented at session start (Step 7), not session end. |
| `session_stats.first_invocation` | string | ISO 8601 timestamp of the very first `/momentum` invocation in this project |
| `session_stats.last_invocation` | string | ISO 8601 timestamp of the most recent `/momentum` invocation |

### Write Semantics

Impetus reads `installed.json` at session start (Step 1 — already happens). After the expertise-adaptive check in Step 7 completes (and before the menu/journal display):
1. Read `session_stats` from `installed.json` (already loaded)
2. If `session_stats` is absent, initialize: `{ "momentum_completions": 1, "first_invocation": "<now>", "last_invocation": "<now>" }`
3. If `session_stats` exists, increment `momentum_completions` by 1 and update `last_invocation` to current ISO 8601 timestamp
4. Write the updated `installed.json`

### Read Semantics

At Step 7, read `session_stats.momentum_completions` from `installed.json`:
- If absent or `0`: treat as first encounter (full walkthrough)
- If `>= 1`: treat as repeat encounter (abbreviated orientation)

### Example installed.json with session_stats

```json
{
  "installed_at": "2026-03-22T14:30:00Z",
  "components": {
    "hooks": { "version": "1.0.0" }
  },
  "session_stats": {
    "momentum_completions": 5,
    "first_invocation": "2026-03-22T14:30:00Z",
    "last_invocation": "2026-03-24T10:00:00Z"
  }
}
```

## Concurrency

JSONL append is concurrency-safe for lines under POSIX pipe buffer size (typically 4096 bytes). No file locking is needed for writes. Multiple tabs can safely append simultaneously.
