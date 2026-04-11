---
slug: retro-session-analytics-phase-0
story_key: retro-session-analytics-phase-0
title: "Retro Phase 0 — Session Analytics and Regression Detection"
epic_slug: ad-hoc
status: backlog
story_file: true
change_type: skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/references/findings-ledger-schema.md
  - skills/momentum/skills/retro/references/session-analytics-queries.md
derives_from:
  - _bmad-output/planning-artifacts/architecture.md#Decision43
  - _bmad-output/research/momentum-vs-fowler-feedback-flywheel-2026-04-10/final/momentum-vs-fowler-feedback-flywheel-final-2026-04-10.md
---

# Retro Phase 0 — Session Analytics and Regression Detection

## User Story

As a Momentum developer running a retrospective, I see a quantitative session analytics brief
before the qualitative audit begins, so that auditors know where to focus and practice
regressions are detected automatically rather than noticed by feel.

## Background / Context

Momentum captures failure signals (retro findings, gate failures, distill events) but has no
mechanism for detecting whether a practice change made things measurably worse. A developer
who changes the research skill workflow has no way to know if Gemini integration errors spiked
until someone notices in conversation.

All the data exists: every Claude Code session is logged to JSONL at
`~/.claude/projects/<project>/*.jsonl`. A DuckDB query over these files for the sprint window
can compute error rates, gate failures, skill usage, and performance signals — and compare
them to the prior sprint window.

Decision 43 establishes Phase 0 as a pre-qualitative analytics pass. It runs before Phase 1
(qualitative audit) so auditors receive a structured brief telling them where to look.

**DuckDB query note:** Session files must be read with `read_csv_auto` using
`columns={'content': 'VARCHAR'}` — not `read_ndjson_auto`. The `queue-operation` entry type
has a bare string in its `content` field which breaks DuckDB type inference. All JSON
extraction then uses `json_extract_string()` / `json_extract()` inline.

## Acceptance Criteria

### AC1 — Phase 0 added to retro workflow before Phase 1
- `skills/momentum/skills/retro/workflow.md` has a new Phase 0 step that runs before the
  existing Phase 1 (qualitative audit)
- Phase 0 is labelled "Session Analytics" and produces a brief before proceeding
- Phase 0 receives the sprint window dates as input (from the sprint index or user-provided)

### AC2 — Session files queried for sprint window
- Phase 0 identifies all session JSONL files in the project's Claude session directory whose
  timestamps fall within the current sprint window
- Identifies the prior sprint window for comparison (preceding sprint dates from sprint index)
- Uses `read_csv_auto` with `VARCHAR` columns — not `read_ndjson_auto`

### AC3 — Core metric set computed for current and prior sprint
Phase 0 computes all of the following for both the current sprint window and the prior sprint
window:
- **Tool error rate per skill:** count of `is_error: true` tool results, grouped by the most
  recent skill invocation preceding each error
- **Hook prevention events:** count of `system.stop_hook_summary` entries where
  `preventedContinuation = true`
- **Compaction frequency:** count of `system.compact_boundary` entries per session
- **Skill invocation counts:** count of `Skill` tool calls by `input.skill` value
- **Turn duration vs. context depth:** `durationMs / messageCount` from
  `system.turn_duration` entries (performance degradation signal)
- **Cache hit rate:** `cache_read_input_tokens / (cache_read + cache_creation_input_tokens)`
  from `assistant.message.usage`
- **Git commit type distribution:** regex on `Bash` tool inputs containing `git commit`,
  extract conventional commit type (`feat`, `fix`, `docs`, `chore`, etc.)

### AC4 — Regressions flagged in the brief
- Phase 0 compares current sprint metrics to prior sprint metrics
- Any metric that worsened by more than a threshold is flagged as a regression:
  - Tool error rate: increase of more than 3 percentage points
  - Hook prevention events: any increase from 0
  - Compaction frequency per session: increase of more than 1
  - `fix` commit ratio: increase of more than 10 percentage points
- Flagged regressions are listed at the top of the brief with the delta and the skill or
  context associated with the regression

### AC5 — Findings-ledger entries include `momentum_version`
- All findings-ledger writes include a `momentum_version` field populated from the installed
  plugin version at write time
- This applies to all ledger writers: `momentum:distill` (Phase 6), `momentum:retro`
  (Phase 0 brief entry + Phase 5 stubs), and any future writers
- The `momentum_version` value is read from the plugin's installed version record at write
  time (not hardcoded)
- Existing ledger entries without `momentum_version` are not backfilled — Option B
  (git timestamp join) provides retrospective version attribution when needed

### AC6 — Structured brief output
- Phase 0 writes a brief to the retro working directory (e.g.,
  `.claude/momentum/sprint-logs/<sprint>/session-analytics-brief.md`)
- Brief contains:
  - Sprint window dates and session count
  - Metric table: metric name, prior sprint value, current sprint value, delta, flagged/clean
  - Flagged regressions section (empty = "No regressions detected")
  - `momentum_version` range active during the sprint (from ledger entries or git log)
- Brief is displayed to the developer before Phase 1 begins

### AC7 — Session analytics query reference doc created
- `skills/momentum/skills/retro/references/session-analytics-queries.md` is created with
  the canonical DuckDB queries for each metric in AC3
- Queries use the `read_csv_auto` pattern with `VARCHAR` columns
- Queries are parameterised for sprint window dates
- This doc is the reference for Phase 0 implementation and future query additions

### AC8 — Option B version validation available
- The brief includes a note when `momentum_version` ledger entries are sparse or absent for
  the sprint window
- In that case, Phase 0 uses git log to identify version bump commit dates within the sprint
  window and lists them as the version context (Option B fallback)
- Option B output is clearly labelled as "estimated from git history" not ledger data

## Tasks / Subtasks

- [ ] Task 1 — Add `momentum_version` to findings-ledger schema (AC5)
  - [ ] Update `skills/momentum/references/findings-ledger-schema.md` with `momentum_version`
        field definition
  - [ ] Update `momentum:distill` Phase 6 ledger write to include `momentum_version`
  - [ ] Update `momentum:retro` Phase 5 ledger write to include `momentum_version`

- [ ] Task 2 — Create session analytics query reference doc (AC7)
  - [ ] Create `skills/momentum/skills/retro/references/session-analytics-queries.md`
  - [ ] Include parameterised DuckDB queries for all 7 metrics in AC3
  - [ ] Document the `read_csv_auto` pattern and why `read_ndjson_auto` fails
  - [ ] Include example output for each query

- [ ] Task 3 — Implement Phase 0 in retro workflow (AC1–AC4, AC6, AC8)
  - [ ] Add Phase 0 before Phase 1 in `skills/momentum/skills/retro/workflow.md`
  - [ ] Phase 0 reads sprint window from sprint index (current + prior sprint dates)
  - [ ] Phase 0 runs DuckDB queries from the reference doc against session files
  - [ ] Phase 0 computes deltas and applies regression thresholds (AC4)
  - [ ] Phase 0 writes structured brief to sprint log directory (AC6)
  - [ ] Phase 0 falls back to Option B git timestamp attribution when ledger data is sparse
  - [ ] Phase 0 output is displayed before Phase 1 qualitative audit begins

## Dev Notes

### DuckDB `read_csv_auto` pattern

The session files cannot be read with `read_ndjson_auto()` — the `queue-operation` entry
type has a bare string in its `content` field which breaks DuckDB type inference. Use this
pattern for all queries:

```sql
SELECT json_extract_string(c, '$.type') AS type,
       json_extract_string(c, '$.timestamp') AS ts,
       ...
FROM (
  SELECT content AS c
  FROM read_csv_auto('/path/to/session.jsonl',
       columns={'content': 'VARCHAR'}, header=false)
)
WHERE json_extract_string(c, '$.type') = 'assistant'
```

### Sprint window identification

The session directory for a project is:
`~/.claude/projects/<url-encoded-project-path>/`

For this project: `~/.claude/projects/-Users-steve-projects-momentum/`

Sprint start and end dates come from the sprint index JSON. Filter session files by
`MIN(timestamp)` falling within the sprint window.

### Regression threshold rationale

Thresholds are conservative to avoid false positives on small-sample sprints. A sprint with
3 sessions and 1 tool error has a 33% error rate but zero signal value. Phase 0 should note
session count and suppress regression flags when N < 3 sessions in the window.

### findings-ledger-schema.md

If this file does not exist, create it at `skills/momentum/references/findings-ledger-schema.md`
with the full schema documenting all current fields (`timestamp`, `origin`, `artifact`,
`learning`, `tier`, `path`) plus the new `momentum_version` field.

## Definition of Done

- [ ] `momentum_version` field in findings-ledger schema and all ledger writers
- [ ] Session analytics query reference doc exists with all 7 metric queries
- [ ] Phase 0 implemented in retro workflow, runs before Phase 1
- [ ] Brief written to sprint log directory with metric table and regression flags
- [ ] Option B fallback documented and functional when ledger data is sparse
- [ ] Story status transitioned to done
