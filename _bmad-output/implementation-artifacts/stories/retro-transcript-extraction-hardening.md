---
title: Retro Transcript Extraction Hardening — Worktree Path Resolution and UTC Boundary Fix
story_key: retro-transcript-extraction-hardening
story_type: practice
priority: critical
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/scripts/transcript-query.py
  - skills/momentum/scripts/test-transcript-query.py
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - _bmad-output/planning-artifacts/architecture.md
---

# Retro Transcript Extraction Hardening — Worktree Path Resolution and UTC Boundary Fix

Status: ready-for-dev

## Story

As the retro orchestrator,
I want the transcript extraction pipeline to resolve worktree paths, attribute sessions correctly across UTC boundaries, serialize JSON-valued columns with `json.dumps`, discover its tooling at the canonical dynamic path, scope sessions to the sprint window via story slugs (not just dates), and protect long-lived agents from large-file read failures,
so that retro analysis sees the full sprint corpus and produces audit findings grounded in complete, correctly attributed evidence.

## Description

The retro transcript extraction pipeline (Decision 27) is the sole evidence source for retrospectives. Six independent defects discovered across two consecutive retros (sprint-2026-04-08 and nornspun-2026-04-10) leave large portions of sprint activity invisible or miscounted. This story hardens the pipeline along all six dimensions in one coherent change set so the next retro runs against a complete corpus.

**Pain context:**
- *sprint-2026-04-08 retro:* Worktree sessions invisible to extraction (entire sprint stories missing from corpus). UTC boundary issue caused 1–3 sessions/sprint to be miscounted. DuckDB `repr` corrupted JSON-valued columns silently.
- *nornspun sprint-04-10 retro (2026-04-12):* Phase 2 extraction step referenced a non-existent relative script path; developer had to manually direct discovery. Same-day sprints had session windows that captured the previous sprint's execution but missed the current sprint's substantive dev events. 106 of 238 (44%) tool errors in that retro were file-too-large variants on `agent-summaries.jsonl`, `errors.jsonl`, `prd.md`, `architecture.md`, and `stories/index.json` — wasting 12+ turns per agent on recovery.

## Acceptance Criteria

1. **Worktree session discovery.** When the developer runs the retro from a checkout that may include git worktrees, `transcript-query.py` discovers Claude Code session JSONL files for every worktree path that maps to the same project, not just the path returned by `_project_base()` for the current working directory. Sessions from worktree directories appear in the consolidated session list with stable, deduplicated paths.

2. **UTC day-boundary attribution.** Sessions whose mtime crosses UTC midnight are attributed to the sprint whose `[started, completed]` range contains them according to UTC date semantics. The `--after YYYY-MM-DD` flag includes sessions with `mtime >= start-of-day-UTC(after)`; the `--before YYYY-MM-DD` flag includes sessions with `mtime <= end-of-day-UTC(before)` (inclusive of the full final UTC day, not just `00:00:00Z`). A session that closed at `23:55Z` on the sprint's last day and a session that opened at `00:05Z` on the day after sprint completion are both correctly classified.

3. **DuckDB JSON serialization correctness.** All JSONL extracts produced by `transcript-query.py` (`user-messages.jsonl`, `agent-summaries.jsonl`, `errors.jsonl`, `team-messages.jsonl`) emit JSON-valued columns using `json.dumps` (or DuckDB's native JSON output), not Python `repr`. Each emitted line round-trips through `json.loads` without raising. No lines contain Python-style single-quoted strings, `None`, `True`, or `False` literals where JSON booleans/null are expected.

4. **Canonical dynamic script path.** The retro workflow (`skills/momentum/skills/retro/workflow.md` Phase 2) and any caller that needs `transcript-query.py` resolves the script path dynamically via glob over `~/.claude/plugins/cache/momentum/momentum/*/scripts/transcript-query.py`, picking the highest semver version directory present. The relative reference `skills/momentum/scripts/transcript-query.py` is retained only as a development-mode fallback for work inside the Momentum repo itself. The chosen path is logged once at the start of Phase 2.

5. **Sprint-window alignment via story slugs.** Same-day sprints (e.g., started and completed on `2026-04-11`) are scoped by story slug membership in addition to the date range. The extraction pipeline filters sessions to those that mention any slug in `{{sprint_stories}}` at least once in user messages, agent prompts, or tool inputs (the date range remains the outer bound). For multi-day sprints with non-overlapping date ranges, slug-based filtering is a no-op (date range alone is sufficient and correct). The pipeline reports the per-sprint session count both before and after slug filtering.

6. **Peek-first convention for long-lived agents.** Inline system prompts for `auditor-human`, `auditor-execution`, `auditor-review`, and `documenter` in `skills/momentum/skills/retro/workflow.md` instruct the agent to (a) run `wc -l` on any audit-extracts file before reading, (b) read in 500-line chunks via `Read offset/limit` or `python3` line-by-line streaming for files over 200 lines, and (c) never attempt a full `Read` on `agent-summaries.jsonl`, `errors.jsonl`, `prd.md`, `architecture.md`, or `stories/index.json`. The `spec-impact-discovery` agents in `skills/momentum/skills/sprint-planning/workflow.md` Step 4.5 receive the same convention for `architecture.md`, `prd.md`, and `stories/index.json`.

7. **Regression protection.** Existing pre-built queries (`user-messages`, `agent-summary`, `errors`, `team-messages`, `tool-usage`, `sql`) continue to produce the same row schema and ordering as before this change for inputs that were previously handled correctly. The `--after`/`--before` flags continue to accept `YYYY-MM-DD`. Existing tests in `skills/momentum/scripts/test-momentum-tools.py` (or a new sibling test file for `transcript-query.py`) cover: worktree discovery resolution, UTC boundary inclusivity, JSON round-trip, dynamic script path resolution, slug-based filtering on a fixture, and graceful handling when no worktree paths exist.

8. **Observability.** Phase 2 of the retro workflow logs a one-line summary per extract showing pre-filter and post-filter counts, the resolved script path, and the resolved session base directories (one per worktree path included). When `{{sprint_stories}}` slug filtering reduces the session count, the reduction is shown.

## Tasks / Subtasks

- [ ] **Task 1 — Worktree discovery in `transcript-query.py`** (AC: #1, #7, #8) — *change-type: script-code*
  - [ ] 1.1 Inspect current `_project_base()` (lines 73–89) and `discover_sessions()` (lines 92–120). Document existing behavior in dev notes.
  - [ ] 1.2 Add a `_worktree_bases(cwd)` helper: shells out `git worktree list --porcelain` (when inside a git repo); for each worktree path, computes the Claude Code project encoding (`path.replace('/', '-')`); returns the list of `~/.claude/projects/<encoded>/` directories that exist on disk. Fall back to `[]` when not in a git repo.
  - [ ] 1.3 Update `discover_sessions(base, ...)` signature to accept either a single base or a list of bases. When called from `main()`, pass `[primary_base, *_worktree_bases(cwd)]`, deduplicated. Sort the merged session list by mtime then path for stable ordering.
  - [ ] 1.4 Update `discover_subagent_files()` to walk subagent directories under each base session-id directory it finds.
  - [ ] 1.5 Echo all resolved bases to stderr at startup (`Found N session(s) across M base(s): ...`).

- [ ] **Task 2 — UTC day-boundary semantics** (AC: #2, #7) — *change-type: script-code*
  - [ ] 2.1 In `discover_sessions()`, change `before_dt` resolution from `datetime.fromisoformat(before).replace(tzinfo=timezone.utc)` (which evaluates to `00:00:00Z`) to `datetime.fromisoformat(before).replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)` so the comparison `mtime <= before_dt` includes the full final UTC day.
  - [ ] 2.2 Confirm `after_dt` already evaluates to `00:00:00Z` of the after day (it does — keep behavior). Add a docstring note clarifying inclusivity at both ends.
  - [ ] 2.3 Add a unit test fixture: two synthetic JSONL files with mtimes set via `os.utime` to `23:55:00Z` on day N and `00:05:00Z` on day N+1, asserting both are included when `--after N --before N` (boundary inclusivity for the closing day).

- [ ] **Task 3 — JSON serialization audit** (AC: #3, #7) — *change-type: script-code*
  - [ ] 3.1 Search `transcript-query.py` for any `repr(`, `str(`, or f-string interpolation that emits Python data into JSONL lines. The current `emit_result()` already uses `json.dumps()` for `--format json` (line 460); confirm no path emits raw `str()` of a dict/list to a file or stdout when format is `json`.
  - [ ] 3.2 Inspect `query_agent_summary()` lines 321–328: `output_text = "\n".join(json.dumps(r) for r in results)` is correct. Confirm. Add an assertion in tests that every emitted line `json.loads()` cleanly.
  - [ ] 3.3 If any emit path uses `str()` or `repr()` for a JSON-shaped value, replace with `json.dumps(value, default=str)` (the `default=str` falls back to string for non-JSON-native types like `datetime`).
  - [ ] 3.4 Add a regression test that runs each pre-built query against a fixture JSONL file, captures stdout/output file, and asserts every output line round-trips through `json.loads`.

- [ ] **Task 4 — Canonical dynamic script path resolution in retro workflow** (AC: #4, #8) — *change-type: skill-instruction*
  - [ ] 4.1 In `skills/momentum/skills/retro/workflow.md` Phase 2 (`<step n="2">`), replace each occurrence of the bare relative path `skills/momentum/scripts/transcript-query.py` (lines 115, 124, 133, 142, plus the prose at line 104 and any other reference) with a resolved variable `{{transcript_query_path}}`.
  - [ ] 4.2 Add a sub-step at the start of Phase 2 that resolves `{{transcript_query_path}}` via shell:
    ```
    TRANSCRIPT_QUERY=$(ls -d ~/.claude/plugins/cache/momentum/momentum/*/scripts/transcript-query.py 2>/dev/null \
      | sort -V | tail -n1)
    [ -z "$TRANSCRIPT_QUERY" ] && [ -f skills/momentum/scripts/transcript-query.py ] \
      && TRANSCRIPT_QUERY=skills/momentum/scripts/transcript-query.py
    ```
    Echo the resolved path to the orchestrator output before running extractions.
  - [ ] 4.3 Confirm: when running inside `/Users/steve/projects/momentum/` itself, the dev-mode fallback kicks in and the in-repo script is used; in any downstream project, the highest-versioned plugin-cache copy is used.
  - [ ] 4.4 Update the `<note>` block at the top of Phase 2 (lines 104–106) to reflect the dynamic path convention.

- [ ] **Task 5 — Sprint-window alignment via story slugs** (AC: #5, #7, #8) — *change-type: script-code* + *skill-instruction*
  - [ ] 5.1 Add a new `transcript-query.py` flag: `--story-slugs <comma-separated>` accepted by every pre-built query. When present, the per-query SQL adds a filter to drop sessions/subagent files whose union of `message.content::VARCHAR` does not contain any of the supplied slugs. (DuckDB SQL: `EXISTS (SELECT 1 FROM ... WHERE message.content::VARCHAR LIKE '%slug-1%' OR ...)` evaluated per session file.)
  - [ ] 5.2 Implementation pattern: pre-filter session paths in `main()` before passing to query functions — for each session path, run a small DuckDB probe query (`SELECT 1 FROM read_json('{path}', {READ_JSON_OPTS}) WHERE message.content::VARCHAR LIKE '%slug%' LIMIT 1`); keep paths whose probe returns at least one row when `--story-slugs` is supplied. Log pre/post counts.
  - [ ] 5.3 Update `skills/momentum/skills/retro/workflow.md` Phase 2 extraction commands (lines 113–144) to pass `--story-slugs "{{sprint_stories | join(',')}}"` to all four pre-built query invocations. The variable `{{sprint_stories}}` is already populated in Phase 1 line 89.
  - [ ] 5.4 Behavior: when slug list is empty (`{{sprint_stories | length}} == 0`), `--story-slugs` is omitted; when non-empty, slug filtering applies and pre/post counts are logged.

- [ ] **Task 6 — Peek-first convention in inline auditor/documenter prompts** (AC: #6) — *change-type: skill-instruction*
  - [ ] 6.1 In `skills/momentum/skills/retro/workflow.md` Phase 4 inline system prompts (lines 238–414), strengthen the existing large-file note from "use offset/limit on Read to stream in chunks, or python3 to process JSONL line-by-line. Do not attempt to Read a whole file at once" to a numbered protocol matching the convention in `skills/momentum/agents/dev.md` lines 106–122. Add an explicit "known-large files" list: `agent-summaries.jsonl`, `errors.jsonl`, `prd.md`, `architecture.md`, `stories/index.json`.
  - [ ] 6.2 Apply the same protocol to the spec-impact-discovery agents in `skills/momentum/skills/sprint-planning/workflow.md` Step 4.5 (lines 395–412) — they read `architecture.md` and `prd.md` and were also affected per the nornspun retro.
  - [ ] 6.3 Wording standard: "Before reading any file in this list, run `wc -l` first. For files >200 lines, read in 500-line chunks via `Read offset/limit`, or stream JSONL line-by-line via `python3`. Never attempt a full `Read` on these files."

- [ ] **Task 7 — Tests** (AC: #7) — *change-type: script-code*
  - [ ] 7.1 Add `skills/momentum/scripts/test-transcript-query.py` (new file) — pytest-style or stdlib `unittest`; runnable as `python3 skills/momentum/scripts/test-transcript-query.py` without external test runners. Mirror the structure of `test-momentum-tools.py`.
  - [ ] 7.2 Test cases:
    - `test_worktree_bases_resolves_extra_paths`: stub `git worktree list --porcelain` output via monkeypatch; assert merged base list.
    - `test_utc_boundary_inclusive`: synthesize JSONL files at `23:55Z` day-N and `00:05Z` day-N+1; assert `--after N --before N` includes both.
    - `test_emit_json_roundtrips`: run each pre-built query against a 3-line fixture JSONL; assert every emitted line `json.loads()` succeeds.
    - `test_slug_filter_drops_unrelated_sessions`: two fixture sessions, one mentioning `story-foo`, one not; `--story-slugs story-foo` keeps only the first.
    - `test_no_worktrees_falls_back_to_primary_base`: outside a git repo, `_worktree_bases()` returns `[]` and discovery proceeds with only the primary base.
  - [ ] 7.3 Wire test invocation into the developer's manual run note in the story dev notes — there is no CI test runner in this repo, but tests should exit non-zero on failure.

- [ ] **Task 8 — Documentation alignment** (AC: #4, #8) — *change-type: specification*
  - [ ] 8.1 Update Decision 27 in `_bmad-output/planning-artifacts/architecture.md` (line 1909+) to mention dynamic path resolution and slug-based session filtering as part of the "Wave 1: DuckDB Preprocessing" subsection. Keep the change concise — one paragraph addition.
  - [ ] 8.2 Add a row to the Read/Write Authority table for `transcript-query.py` if not already present (it's tooling, not an artifact writer; likely no change needed — verify).

## Dev Notes

### Story-Specific Context

This is a **diagnose-and-harden** story addressing six independent regressions in a single tightly-coupled pipeline. All six issues live in the retro evidence chain (Decision 27): five touch `transcript-query.py` and `retro/workflow.md` directly; the sixth (peek-first convention) crosses into `sprint-planning/workflow.md` because the same pattern bit `spec-impact-discovery` agents.

**The pipeline being modified:**
```
retro/workflow.md Phase 2
  ↓ shells out to
transcript-query.py
  ↓ uses DuckDB to read
~/.claude/projects/<encoded-cwd>/*.jsonl  ←— problem 1: worktree paths missing
  ↓ filtered by --after/--before          ←— problem 2: UTC boundary off-by-one
  ↓ + (new) --story-slugs                  ←— problem 5: same-day sprint scoping
  ↓ emits via json.dumps                   ←— problem 3: confirm correct
  ↓ to audit-extracts/*.jsonl
  ↓ read by
auditor-{human,execution,review} + documenter (TeamCreate inline prompts)
                                            ←— problem 6: peek-first protocol
```

**Problem 4 (canonical script path)** is purely orchestrator-side: the retro workflow currently hard-codes `skills/momentum/scripts/transcript-query.py`, which only exists when the developer runs retro from inside the Momentum repo. In every downstream project, the script lives at `~/.claude/plugins/cache/momentum/momentum/<version>/scripts/transcript-query.py`. The fix is glob + `sort -V | tail -1` resolution with in-repo fallback.

### Architecture Compliance

- **Decision 27 (Transcript Audit Retro)** is the governing decision — see `architecture.md` lines 1909–1947. This story preserves all of Decision 27's contracts: same four extract files (`user-messages.jsonl`, `agent-summaries.jsonl`, `errors.jsonl`, `team-messages.jsonl`), same audit-extracts directory layout, same auditor team composition. The change-set hardens the pipeline's edges without altering its shape.
- **Decision 41 (Workflow Team Composition Declarations)** is preserved — the `<team-composition>` block in `retro/workflow.md` is not changed.
- **Decision 35 (Agent Definition Files vs SKILL.md Boundary)** is honored — auditor and documenter system prompts remain inline in `retro/workflow.md` (they are pure spawned workers tied to retro-specific phases, not user-invocable; per Decision 35 they could be either inline or in `agents/`, and the existing inline placement is appropriate).
- **NFR3 (Reliability)** — this story is itself an NFR3 hardening story: it removes silent failure modes from the retro evidence chain.
- **Read/Write Authority (architecture.md line 1179)** — `momentum:retro` reads session JSONL transcripts and writes `audit-extracts/`. No authority changes.

### Project Structure Notes

Files this story will modify:
- `skills/momentum/scripts/transcript-query.py` — primary code change (Tasks 1, 2, 3, 5)
- `skills/momentum/skills/retro/workflow.md` — orchestrator changes (Tasks 4, 5, 6)
- `skills/momentum/skills/sprint-planning/workflow.md` — peek-first convention only, Step 4.5 inline prompts (Task 6)
- `_bmad-output/planning-artifacts/architecture.md` — small Decision 27 addendum (Task 8)

Files this story will create:
- `skills/momentum/scripts/test-transcript-query.py` — new test file (Task 7)

No new directories. No changes to plugin manifest or skill registration.

### Implementation Guide

**Change-type classification per task:**

| Task | Change Type | Notes |
|---|---|---|
| 1 (worktree discovery) | script-code | Python in `transcript-query.py` |
| 2 (UTC boundary) | script-code | Python in `transcript-query.py` |
| 3 (JSON serialization audit) | script-code | Python in `transcript-query.py` + tests |
| 4 (canonical script path) | skill-instruction | Markdown in `retro/workflow.md` |
| 5 (slug filtering) | script-code + skill-instruction | Both — Python flag + workflow wiring |
| 6 (peek-first convention) | skill-instruction | Markdown in two workflow.md files |
| 7 (tests) | script-code | New `test-transcript-query.py` |
| 8 (docs) | specification | architecture.md addendum |

**For script-code tasks (1, 2, 3, 5, 7):** Implementation is direct Python. Read each function fully before editing. Preserve existing query SQL — additions are pre-filtering and an optional flag, not query rewrites. Use `python3 skills/momentum/scripts/test-transcript-query.py` to run tests; failures must exit non-zero.

**For skill-instruction tasks (4, 5, 6):** This skill (`skills/momentum/skills/retro/`) is the implementing artifact. Apply EDD (executable-diff discipline): read the section being modified, write the change, re-read after to confirm the prose still scans cleanly. NFR compliance: workflow.md changes must keep the `<workflow>`/`<step>`/`<action>` XML structure valid (no new tags, no malformed nesting).

**For the specification task (8):** Direct authoring with cross-reference verification — open architecture.md at line 1909, add one paragraph that does NOT contradict the rest of Decision 27, save. No new section headers; no decision number changes.

**DoD additions specific to this story's change types:**
- Run `python3 skills/momentum/scripts/test-transcript-query.py` and confirm zero failures.
- Manually invoke `python3 skills/momentum/scripts/transcript-query.py user-messages --after 2026-04-08 --before 2026-04-08 --story-slugs <some-slug> --format json --output /tmp/test.jsonl` and verify (a) it runs without error, (b) the resolved base count is logged, (c) the output file is valid JSONL.
- For workflow.md changes: smoke-test by reading the Phase 2 step end-to-end and confirming all `{{transcript_query_path}}` substitutions are consistent and the `<step>` tag structure is intact.

**Gherkin reminder:** Gherkin specs for this sprint will live in `sprints/sprint-2026-04-27/specs/` but are off-limits to the dev agent. The dev agent implements against the plain English ACs in this story file only — never against `.feature` files (Decision 30 black-box separation).

### Testing Requirements

- **Unit:** New `skills/momentum/scripts/test-transcript-query.py` covering AC #1, #2, #3, #5 (see Task 7.2 for the test list).
- **Integration:** Manual smoke run as described in DoD above. Optionally run a dry retro on the most recent completed sprint to confirm extractions populate correctly with the new flags — but this is not a gating test.
- **Regression:** Re-run any pre-existing tests in `skills/momentum/scripts/test-momentum-tools.py` to confirm no collateral damage.
- **No CI runner exists** for this repo — tests are invoked manually by the dev agent and confirmed in the dev agent record.

### References

- Architecture Decision 27 (Transcript Audit Retro, Revised 2026-04-06): `_bmad-output/planning-artifacts/architecture.md` lines 1909–1947
- Architecture Decision 41 (Workflow Team Composition Declarations): referenced in `retro/workflow.md` line 7
- NFR3 (Reliability): listed in Epic 10 frontmatter — `_bmad-output/planning-artifacts/epics.md` line 654
- `transcript-query.py` source: `skills/momentum/scripts/transcript-query.py` (full inspection in Tasks 1, 2, 3, 5)
- Retro workflow Phase 2 (extraction): `skills/momentum/skills/retro/workflow.md` lines 101–179
- Retro workflow Phase 4 (auditor team inline prompts): `skills/momentum/skills/retro/workflow.md` lines 227–435
- Sprint-planning Step 4.5 (spec-impact-discovery agents): `skills/momentum/skills/sprint-planning/workflow.md` lines 393–432
- Large-file convention pattern: `skills/momentum/agents/dev.md` lines 106–122
- Pain-context source — sprint-2026-04-08 retro findings document (worktree, UTC, repr issues)
- Pain-context source — nornspun sprint-04-10 retro (2026-04-12), `docs/intake/nornspun-2026-04-12-1-retro.md` (path discovery, slug-window, peek-first)

## Momentum Implementation Guide

### Change-Type Classification (per Task)

- Task 1 — script-code
- Task 2 — script-code
- Task 3 — script-code
- Task 4 — skill-instruction
- Task 5 — script-code + skill-instruction
- Task 6 — skill-instruction
- Task 7 — script-code
- Task 8 — specification

### Implementation Approach

- **script-code tasks (1, 2, 3, 5 Python parts, 7):** TDD delegation — write or extend the test in `test-transcript-query.py` first, watch it fail with the current `transcript-query.py`, then implement until green. Keep existing query SQL untouched where possible; pre-filter at the Python layer (`main()` and `discover_sessions()`) instead of rewriting queries.
- **skill-instruction tasks (4, 5 workflow parts, 6):** EDD — read the workflow.md section, make the diff, re-read to confirm XML structure is intact and prose still scans. Verify all `{{transcript_query_path}}` references resolve to the same variable.
- **specification task (8):** Direct authoring with cross-reference verification — confirm the new paragraph in Decision 27 does not contradict any later Decision (28, 29, 41, 47).

### NFR Compliance

For Task 4 and Task 6 (skill-instruction tasks): the modified `workflow.md` files must remain valid XML-flavored markdown (every `<step>` closes, every `<action>` closes, every `<check>` block is well-formed). The retro Phase 2 commands and Phase 4 inline system prompts are end-user-facing — clarity over cleverness; preserve the existing voice.

For Task 1 (script-code): worktree discovery is shell-shellable; favor a small, well-named helper (`_worktree_bases`) over a bigger refactor of `_project_base`. Existing call sites of `discover_sessions` and `discover_subagent_files` should not break — accept either single-base or list-of-bases via duck-typed input or a thin wrapper.

### DoD Additions

- All ACs (1–8) demonstrably met.
- New tests added (`test-transcript-query.py`) and passing locally via `python3 skills/momentum/scripts/test-transcript-query.py`.
- Manual smoke run of `transcript-query.py user-messages` on a real sprint date range completes without error and logs resolved base directories.
- Phase 2 of `retro/workflow.md` reads end-to-end with no broken variable references and resolves `{{transcript_query_path}}` correctly in both in-repo and downstream contexts.
- No regression in `test-momentum-tools.py`.
- Decision 27 paragraph addition committed in the same change-set.

### Gherkin / Spec Separation Reminder

Gherkin specs for sprint-2026-04-27 (when generated) will live in `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/` and are off-limits to the dev agent (Decision 30). The dev agent implements against the plain English ACs in this story only.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
