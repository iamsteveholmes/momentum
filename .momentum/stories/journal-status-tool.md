---
title: Journal Status Tool — Deterministic Open Thread Detection
story_key: journal-status-tool
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - sprint-lifecycle-tools
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
change_type: code
---

# Journal Status Tool — Deterministic Open Thread Detection

## Description

The Impetus greeting needs to know whether there are open journal threads
from prior sessions. Currently this would require reading and parsing the
full journal.jsonl in the workflow — which is error-prone and wastes
context budget on raw JSONL parsing.

This story adds a `session journal-status` subcommand to momentum-tools.py
that deterministically scans `.claude/momentum/journal.jsonl` and returns
structured data about open threads, last activity, and whether the journal
exists at all. This follows the established pattern of moving deterministic
logic to tools (Decision from Phase 2).

## Acceptance Criteria (Plain English)

1. A new `session journal-status` command exists in momentum-tools.py that
   reads `.claude/momentum/journal.jsonl` and returns structured JSON about
   journal state.

2. When the journal file does not exist, the command returns:
   `{"exists": false, "open_threads": 0, "last_entry": null}`.

3. When the journal file exists, the command scans all entries and reports:
   - `exists: true`
   - `open_threads: N` — count of threads where the most recent event is
     not a closing event (thread_close, session_end, or similar terminal)
   - `last_entry: ISO_TIMESTAMP` — timestamp of the most recent entry
   - `total_entries: N` — total line count
   - `thread_summary: [{thread_id, status, last_event, last_timestamp}]`
     — one entry per unique thread_id found in the journal

4. The command handles malformed JSONL lines gracefully — skips lines that
   don't parse as JSON without crashing, reports `parse_errors: N` in
   the output.

5. The command completes in under 2 seconds even for journals with 1000+
   entries (linear scan, no indexing needed at this scale).

6. All new code has passing unit tests in test-momentum-tools.py following
   the existing subprocess-based pattern.

## Dev Notes

### journal.jsonl format

The journal is an append-only JSONL file. Each line is a JSON object with
at minimum: `timestamp`, `event`, and optionally `thread_id`, `detail`.

Thread detection logic:
- Group entries by `thread_id`
- For each thread, check the most recent event type
- If the most recent event is `thread_close`, `session_end`, or `done` →
  thread is closed
- Otherwise → thread is open

### Dependencies

Depends on `sprint-lifecycle-tools` (already done — the `session` command group
exists in momentum-tools.py). This story adds a new subcommand under that group.

### CLI integration

Add under the existing `session` command group:

```python
# session journal-status
sjs = session_sub.add_parser("journal-status", help="Scan journal for open threads")
sjs.set_defaults(func=cmd_session_journal_status)
```

### Return format

```json
{
  "exists": true,
  "open_threads": 2,
  "last_entry": "2026-04-05T19:30:00",
  "total_entries": 47,
  "parse_errors": 0,
  "thread_summary": [
    {"thread_id": "sprint-dev-001", "status": "open", "last_event": "decision", "last_timestamp": "2026-04-05T19:30:00"},
    {"thread_id": "triage-002", "status": "closed", "last_event": "thread_close", "last_timestamp": "2026-04-05T18:00:00"}
  ]
}
```

### Required unit tests

| Test Name | What It Verifies |
|---|---|
| test_journal_status_no_file | Returns `exists: false` when journal.jsonl absent |
| test_journal_status_empty_file | Returns `exists: true, open_threads: 0` for empty file |
| test_journal_status_open_threads | Correctly counts open threads |
| test_journal_status_closed_threads | Threads with terminal events are closed |
| test_journal_status_malformed_lines | Skips bad lines, reports parse_errors |
| test_journal_status_thread_summary | Returns correct per-thread summary |

### Files

- `skills/momentum/scripts/momentum-tools.py` — add `session journal-status` command
- `skills/momentum/scripts/test-momentum-tools.py` — add unit tests
