---
title: Impetus Journal Hygiene Script — Move Deterministic Thread Computations to momentum-tools
story_key: impetus-journal-hygiene-script
status: review
epic_slug: impetus-core
depends_on:
  - journal-status-tool
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/impetus/workflow.md
change_type: code + skill-instruction
---

# Impetus Journal Hygiene Script — Move Deterministic Thread Computations to momentum-tools

## User Story

As a developer using Impetus, I want the session-open thread display and hygiene
checks to load instantly instead of burning 800-1200 tokens on in-context JSONL
parsing and timestamp arithmetic, so the open-threads path is as fast as the
happy-path greeting.

## Description

Workflow Step 11 (Session Journal Display) currently instructs the LLM to perform
six categories of deterministic computation in-context:

1. **Thread sorting** — sort open threads by `last_active` descending
2. **Elapsed-time computation** — compute human-readable elapsed labels ("2h ago",
   "yesterday", "5d ago") for each thread's `last_active` timestamp
3. **Concurrent-tab detection** — flag threads with `last_active` within 30 minutes
4. **Dormant-thread flagging** — flag threads with `last_active` more than 3 days ago
5. **Dependency-satisfaction checks** — for threads with `depends_on_thread`, check
   whether the depended-on thread has `status: "closed"`
6. **No-Re-Offer suppression** — compute `context_hash` values and match against each
   thread's `declined_offers` array to suppress previously-declined proactive offers

Additionally, Step 13 (Journal Write) instructs the LLM to construct JSON lines and
append them via inline Bash, with no corruption resilience or concurrent-session safety.

Every one of these operations is deterministic — they involve timestamp arithmetic,
string comparison, and JSON traversal. The LLM currently reads the journal schema
reference file, parses raw JSONL, and evaluates multiple conditional branches. This
costs 800-1200 tokens per session on the open-threads path and adds measurable
startup latency.

The `session journal-status` command (from `journal-status-tool`, now done) already
handles basic thread detection and counting. This story extends that foundation with
two new commands:

- **`session journal-hygiene`** — returns the full structured display data: sorted
  threads with elapsed labels, all warnings (concurrent, dormant, dependency-satisfied,
  unwieldy), No-Re-Offer suppression results, and pre-composed prompts
- **`session journal-append`** — safe JSONL append with atomic writes, malformed-line
  resilience, and journal-view.md regeneration

After implementation, workflow Step 11 becomes a thin presenter that calls one tool
and formats the structured JSON output. The LLM performs zero computation — only
voice-appropriate rendering.

**Performance target (NFR20 extension):** The open-threads path should complete in
under 15 seconds wall-clock and under 10 tool calls total from `/momentum` invocation
to menu display. Currently the happy-path greeting achieves this via
`startup-preflight`; the open-threads path should match it.

## Acceptance Criteria (Plain English)

1. A new `session journal-hygiene` command exists in momentum-tools.py that reads
   `.claude/momentum/journal.jsonl` and returns a single structured JSON object
   containing everything Step 11 needs to render the thread display and hygiene
   checks — no further file reads or computation required by the workflow.

2. The returned JSON includes a `threads` array sorted by `last_active` descending.
   Each thread entry contains: `context_summary_short`, `context_summary`, `phase`,
   `story_ref`, `last_active` (ISO timestamp), `elapsed_label` (human-readable
   string like "2h ago", "yesterday", "5d ago"), and `status`.

3. The returned JSON includes a `warnings` object with four arrays:
   - `concurrent`: threads with `last_active` within the last 30 minutes, each
     including a `minutes_ago` field
   - `dormant`: threads with `last_active` more than 3 days ago, each including
     a `days_inactive` field
   - `dependency_satisfied`: threads whose `depends_on_thread` target is now
     closed, each including the depended-on thread's `context_summary_short`
   - `unwieldy`: present (with `open_count`) only when more than 5 open threads
     exist

4. The returned JSON includes a `suppressed_offers` array listing any proactive
   offers that were suppressed by No-Re-Offer matching. For each dormant thread,
   the command computes `context_hash` (format:
   `thread_id|story_ref|phase|git_hash`) and checks the thread's `declined_offers`
   array. If a match is found for `offer_type` + `context_hash`, the thread is
   excluded from the `dormant` warnings array and listed in `suppressed_offers`
   instead.

5. The returned JSON includes a `suggested_prompts` object with pre-composed
   prompt strings for each warning type — the workflow renders these directly
   without constructing prompt text.

6. A new `session journal-append` command exists that accepts `--entry` (JSON
   string) and performs an atomic append to `.claude/momentum/journal.jsonl`:
   writes to a temp file first, then appends to the journal, ensuring no
   corruption on partial writes.

7. The `journal-append` command also regenerates `.claude/momentum/journal-view.md`
   after every successful append: reads all journal entries, reconstructs current
   state per `thread_id` (last entry wins), and renders a markdown table with
   columns Thread, Story, Phase, Last Action, Last Active, Status. Includes all
   open threads and threads closed within the last 7 days.

8. Workflow Step 11 is rewritten to call `momentum-tools session journal-hygiene`
   once, then render the structured output using Impetus voice rules. The step
   contains no JSONL parsing, no timestamp arithmetic, no conditional branching
   for hygiene checks — only template rendering from the tool's JSON output.

9. Workflow Step 13 (Journal Write) is rewritten to call `momentum-tools session
   journal-append --entry '{{json}}'` instead of raw `echo >> journal.jsonl`.
   The view regeneration action is removed from Step 13 since `journal-append`
   handles it.

10. The open-threads startup path (preflight through thread display) completes
    in under 15 seconds wall-clock and uses fewer than 10 tool calls from
    `/momentum` invocation to the thread selection prompt.

11. All new and modified commands have passing unit tests in
    test-momentum-tools.py following the existing subprocess-based pattern.

## Tasks

### Task 1: Implement `session journal-hygiene` command [x]

Add `cmd_session_journal_hygiene` to momentum-tools.py under the `session`
command group. This command:

- Reads `.claude/momentum/journal.jsonl`
- Groups entries by `thread_id`, takes last entry per thread for current state
- Filters to open threads (status != closed, last event not in terminal set)
- Sorts by `last_active` descending
- Computes elapsed-time labels using `datetime.now() - last_active`:
  - < 1 hour: "{N}m ago"
  - < 24 hours: "{N}h ago"
  - < 2 days: "yesterday"
  - otherwise: "{N}d ago"
- Builds warnings:
  - concurrent: `last_active` within 30 minutes of now
  - dormant: `last_active` more than 3 days ago
  - dependency_satisfied: `depends_on_thread` target has status "closed"
  - unwieldy: open thread count > 5
- Applies No-Re-Offer suppression:
  - For each dormant thread, compute `context_hash` = `f"{thread_id}|{story_ref}|{phase}|{git_hash}"`
  - `git_hash` = output of `git rev-parse --short HEAD` (cached once per invocation)
  - Check `declined_offers` array for matching `offer_type` + `context_hash`
  - Suppress matching threads from dormant warnings; add to `suppressed_offers`
- Composes `suggested_prompts` for each warning type
- Returns single JSON object

#### Subtask 1a: Core thread sorting and elapsed labels [x]

Implement the thread scanning, sorting, and elapsed-time computation. Wire up
the parser and CLI registration.

#### Subtask 1b: Warning computation [x]

Add concurrent, dormant, dependency-satisfied, and unwieldy detection.

#### Subtask 1c: No-Re-Offer suppression [x]

Add context_hash computation and declined_offers matching. Integrate with
dormant warning logic.

#### Subtask 1d: Suggested prompts [x]

Add pre-composed prompt strings keyed by warning type.

### Task 2: Implement `session journal-append` command [x]

Add `cmd_session_journal_append` to momentum-tools.py under the `session`
command group. This command:

- Accepts `--entry` argument containing a JSON string
- Validates the JSON parses correctly (fail with error if not valid JSON)
- Appends the line to `.claude/momentum/journal.jsonl` using atomic write:
  write to a temp file in the same directory, then append contents to the
  journal file (avoids corruption from partial writes)
- After successful append, regenerates `.claude/momentum/journal-view.md`:
  reads all entries, groups by thread_id (last entry wins), renders markdown
  table with Thread, Story, Phase, Last Action, Last Active, Status columns,
  includes open threads and threads closed within 7 days

#### Subtask 2a: Atomic append implementation [x]

Write the temp-file-then-append logic with proper error handling.

#### Subtask 2b: Journal-view regeneration [x]

Port the view regeneration logic from workflow Step 13's natural language
description into deterministic Python code.

### Task 3: Rewrite workflow Step 11 [x]

Replace the current Step 11 content with a thin presenter:

- Single action: `Run momentum-tools session journal-hygiene via Bash.
  Store as {{hygiene}}.`
- Render thread list from `{{hygiene.threads}}` array
- Render warnings from `{{hygiene.warnings}}` using suggested prompts
- Keep the selection prompt and deferred stats-update
- Remove all JSONL parsing, timestamp arithmetic, conditional hygiene branches

### Task 4: Rewrite workflow Step 13 [x]

Replace the current Step 13 content:

- Single action: `Run momentum-tools session journal-append --entry '{{json_line}}'
  via Bash`
- Remove the journal-view.md regeneration action (handled by the tool)
- Keep the step's role as a shared procedure invoked by other steps

### Task 5: Unit tests [x]

Add tests following the existing subprocess-based pattern in
test-momentum-tools.py.

| Test Name | What It Verifies |
|---|---|
| test_journal_hygiene_no_file | Returns empty threads and no warnings when journal absent |
| test_journal_hygiene_no_open_threads | Returns empty threads when all closed |
| test_journal_hygiene_sort_order | Threads sorted by last_active descending |
| test_journal_hygiene_elapsed_labels | Correct human-readable labels (minutes, hours, yesterday, days) |
| test_journal_hygiene_concurrent_warning | Flags threads active within 30 minutes |
| test_journal_hygiene_dormant_warning | Flags threads inactive > 3 days |
| test_journal_hygiene_dependency_satisfied | Detects when depends_on_thread target is closed |
| test_journal_hygiene_unwieldy | Warning present when > 5 open threads |
| test_journal_hygiene_no_reoff_suppression | Suppresses dormant offer when declined_offers matches |
| test_journal_hygiene_no_reoff_context_change | Re-offers when context_hash differs from declined entry |
| test_journal_hygiene_suggested_prompts | Returns pre-composed prompts for each active warning type |
| test_journal_append_creates_file | Creates journal.jsonl if absent |
| test_journal_append_appends_line | Appends valid JSON line to existing file |
| test_journal_append_invalid_json | Fails with error for non-JSON input |
| test_journal_append_regenerates_view | journal-view.md is regenerated after append |
| test_journal_append_view_includes_recent_closed | View includes threads closed within 7 days |

## Dev Notes

### Return format for `session journal-hygiene`

```json
{
  "threads": [
    {
      "thread_id": "T-001",
      "context_summary_short": "Sprint dev — story-a",
      "context_summary": "Developing story-a in sprint-2026-04-06",
      "phase": "implementation",
      "story_ref": "story-a",
      "last_active": "2026-04-07T10:30:00",
      "elapsed_label": "2h ago",
      "status": "open"
    }
  ],
  "warnings": {
    "concurrent": [
      {"thread_id": "T-001", "context_summary_short": "Sprint dev — story-a", "minutes_ago": 15}
    ],
    "dormant": [
      {"thread_id": "T-003", "context_summary_short": "Triage — issue-7", "days_inactive": 5}
    ],
    "dependency_satisfied": [
      {"thread_id": "T-002", "context_summary_short": "Dev — story-b",
       "depends_on_summary": "Dev — story-a"}
    ],
    "unwieldy": null
  },
  "suppressed_offers": [
    {"thread_id": "T-004", "offer_type": "dormant-closure", "reason": "declined, context unchanged"}
  ],
  "suggested_prompts": {
    "concurrent": "!  \"{summary}\" appears active in another tab ({minutes} minutes ago). Opening here may cause conflicts. Proceed anyway?",
    "dormant": "{summary} — {days} days inactive. Close this thread? [Y] Yes · [N] Keep open",
    "dependency_satisfied": "The work \"{dep_summary}\" that \"{summary}\" was waiting on is complete — ready to continue?",
    "unwieldy": "!  {count} open threads — consider a quick triage before starting new work. Close any that are stale?"
  },
  "open_count": 3,
  "total_count": 7
}
```

### Existing code to build on

- `cmd_session_journal_status` (line ~510) already has thread scanning, terminal
  event detection, and thread summary construction. The hygiene command extends
  this with sorting, elapsed labels, and warning computation.
- `cmd_session_startup_preflight` (line ~576) already reads journal.jsonl and
  checks `has_open_threads` as a boolean. The hygiene command replaces the need
  for the LLM to re-read and re-parse the journal after preflight routes to
  the open-threads path.

### Workflow Step 11 rewrite target

The current Step 11 (lines ~389-479 in workflow.md) contains approximately 90
lines of XML with inline JSONL parsing, timestamp arithmetic, four hygiene check
branches, and No-Re-Offer guard logic. After this story, Step 11 should be
approximately 30 lines: one tool call, one thread list render, one warning render,
and one selection prompt.

### Journal-append atomicity

The raw `echo >> journal.jsonl` pattern in Step 13 has no corruption resilience.
The `journal-append` command should:
1. Validate the input JSON parses correctly
2. Write to a temp file in the same directory (`journal.jsonl.tmp`)
3. Read the temp file back to confirm it's valid
4. Append the contents to journal.jsonl
5. Remove the temp file
6. Trigger journal-view.md regeneration

This eliminates the class of bugs where a partial write (interrupted process,
disk full) leaves malformed JSONL that breaks subsequent reads.

### context_hash computation for No-Re-Offer

The context_hash format is: `{thread_id}|{story_ref}|{phase}|{git_hash}`

- `thread_id`, `story_ref`, `phase` come from the thread's last journal entry
- `git_hash` is the short HEAD hash (`git rev-parse --short HEAD`), cached once
  per journal-hygiene invocation
- A material context change (different story_ref, different phase, or different
  git hash) produces a different context_hash, which means previously declined
  offers are no longer suppressed

### Performance budget

The open-threads path tool-call sequence should be:
1. `startup-preflight` (already runs — detects `has_open_threads: true`)
2. `journal-hygiene` (new — returns everything Step 11 needs)
3. [LLM renders thread display and prompts — zero tool calls]
4. [User selects thread]
5. `stats-update` (deferred, post-selection)
6. `journal-append` (if any hygiene action taken)

Total: 3-4 tool calls for the display phase, well within the 10-call budget.

### Files

- `skills/momentum/scripts/momentum-tools.py` — add `session journal-hygiene` and
  `session journal-append` commands
- `skills/momentum/scripts/test-momentum-tools.py` — add unit tests for both commands
- `skills/momentum/skills/impetus/workflow.md` — rewrite Steps 11 and 13

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- Implemented `cmd_session_journal_hygiene` in momentum-tools.py: reads journal.jsonl, resolves open threads (last-entry-wins per thread_id), sorts by last_active descending, computes elapsed labels, builds all four warning categories (concurrent/dormant/dependency_satisfied/unwieldy), applies No-Re-Offer suppression via context_hash matching, returns pre-composed suggested_prompts. CLI registered as `session journal-hygiene`.
- Implemented `_regenerate_journal_view` helper: reads journal, groups by thread_id (last entry wins), renders markdown table with open threads + threads closed within 7 days, open threads sorted most-recent-first.
- Implemented `cmd_session_journal_append` in momentum-tools.py: validates JSON, atomic append via temp file (write → verify → append → cleanup), triggers view regeneration. CLI registered as `session journal-append --entry <json>`.
- Rewrote workflow Step 11 to single tool call (`momentum-tools session journal-hygiene`), template rendering only — zero in-context JSONL parsing, timestamp arithmetic, or conditional hygiene branching.
- Rewrote workflow Step 13 to single tool call (`momentum-tools session journal-append --entry '{{json_line}}'`), removing manual view regeneration (now handled by the tool).
- Updated Step 12 references to remove redundant "Regenerate journal-view.md" actions.
- Added 16 unit tests covering all AC behaviors; all 346 tests pass.

### File List

- `skills/momentum/scripts/momentum-tools.py`
- `skills/momentum/scripts/test-momentum-tools.py`
- `skills/momentum/skills/impetus/workflow.md`
