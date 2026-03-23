# Story 1.9: journal.json JSONL Migration Evaluation

Status: ready-for-dev

## Story

As an architect,
I want a documented evaluation of whether the session journal should use JSONL instead of JSON,
so that the concurrency and data integrity implications are understood before Story 2.2 implements the journal.

## Acceptance Criteria

1. **Given** the session journal is specified as `.claude/momentum/journal.json` using read-modify-write JSON
   **When** an architect evaluates the concurrency implications
   **Then** the evaluation documents the failure modes of concurrent multi-tab access to a read-modify-write JSON file
   **And** the evaluation compares JSON (read-modify-write) with JSONL (append-only) for the session journal use case
   **And** the evaluation references the existing architecture decision (Decision 1c) that chose JSONL for the findings ledger for the same concurrency reason

2. **Given** the evaluation is complete
   **When** an architect reviews the recommendation
   **Then** a clear recommendation is documented: migrate to JSONL, keep JSON, or alternative approach
   **And** the rationale addresses concurrency safety, query patterns, human readability, and implementation complexity

3. **Given** Steve has approved the recommendation
   **When** the decision is JSONL migration
   **Then** the architecture document is updated to reflect the new storage format for the session journal
   **And** Story 2.2 acceptance criteria are updated to use JSONL semantics instead of JSON read-modify-write

4. **Given** Steve has approved the recommendation
   **When** the decision is to keep JSON
   **Then** the architecture document records the decision with rationale
   **And** Story 2.2 remains unchanged

## Tasks / Subtasks

- [ ] Task 1: Document concurrency failure modes for read-modify-write JSON (AC: #1)
  - [ ] 1.1 Enumerate failure scenarios: concurrent read-modify-write from multiple Claude Code tabs (lost writes, partial overwrites, corrupted JSON)
  - [ ] 1.2 Reference POSIX file semantics — JSON read-modify-write requires file locking or is fundamentally racy
  - [ ] 1.3 Reference architecture Decision 1c (findings ledger chose JSONL for this exact reason)

- [ ] Task 2: Compare JSON vs JSONL for session journal use case (AC: #1, #2)
  - [ ] 2.1 Document JSONL advantages: atomic append (POSIX guarantee for lines under pipe buffer), no file locking needed, concurrent-safe
  - [ ] 2.2 Document JSONL disadvantages: no random-access update, requires reconstruction for current-state queries, slightly larger file over time
  - [ ] 2.3 Document JSON advantages: random-access read/update, single-file state snapshot, human-readable as-is
  - [ ] 2.4 Document JSON disadvantages: read-modify-write race, requires file locking for safety, corrupt-on-crash risk
  - [ ] 2.5 Analyze session journal query patterns (Impetus reads active story, current phase, open threads) — evaluate which format serves these better

- [ ] Task 3: Write recommendation with rationale (AC: #2)
  - [ ] 3.1 State clear recommendation: JSONL, JSON, or alternative
  - [ ] 3.2 Address all four evaluation dimensions: concurrency safety, query patterns, human readability, implementation complexity
  - [ ] 3.3 Document the evaluation as an architecture decision record in `_bmad-output/planning-artifacts/architecture.md`

- [ ] Task 4: Apply decision outcome (AC: #3 or #4, conditional on Steve's approval)
  - [ ] 4.1 If JSONL: update architecture Decision 1b to reflect new format
  - [ ] 4.2 If JSONL: update Story 2.2 acceptance criteria to use JSONL semantics
  - [ ] 4.3 If JSON: record the keep-JSON rationale in architecture as a formal decision
  - [ ] 4.4 If JSON: confirm Story 2.2 requires no changes

## Dev Notes

### Architecture Context

This story addresses Epic 1 retrospective Action Item #5, which identified that the session journal uses the same read-modify-write pattern the team already rejected for the findings ledger.

**Current state:**
- Architecture Decision 1b specifies `journal.json` at `.claude/momentum/journal.json` with read-modify-write JSON
- Architecture Decision 1c specifies `findings-ledger.jsonl` at `~/.claude/momentum/findings-ledger.jsonl` with JSONL append-only — chosen explicitly because "JSONL enables concurrent append from multiple Claude Code sessions without file locking (POSIX atomic append for lines under pipe buffer size)"
- The session journal and findings ledger face the same concurrency scenario: multiple Claude Code tabs (via CMUX or manual) writing simultaneously

**Key architecture references:**
- Decision 1b (Session Journal: JSON with Markdown View): `.claude/momentum/journal.json`, auto-generated `.claude/momentum/journal-view.md` [Source: architecture.md#Decision 1b]
- Decision 1c (Findings Ledger: JSONL Global): JSONL append-only, POSIX atomic append [Source: architecture.md#Decision 1c]
- Read/Write Authority table: Impetus reads/writes `journal.json`; upstream-fix reads session journal [Source: architecture.md#Read/Write Authority]
- File tree: `.claude/momentum/journal.json`, `.claude/momentum/journal-view.md`, `.claude/momentum/installed.json` [Source: architecture.md#File Tree]

**Session journal query patterns (from Epic 2 stories):**
- Impetus reads at session start: active story, current phase, last completed action, open threads (Decision 4b)
- Thread management: numbered list of open threads, ordered by most-recently-active (Story 2.2 ACs)
- `active_stories` array for concurrent session support (architecture extension)

**Downstream impact — Story 2.2 (Session Orientation and Thread Management):**
- Story 2.2 implements the journal and currently assumes JSON semantics
- If the decision is JSONL migration, Story 2.2 ACs must be updated before development begins
- `journal-view.md` auto-generation remains relevant regardless of format (human readability layer)

**Implementation note:** This is a documentation/evaluation story, not a code story. The output is an architecture decision record and (conditionally) spec updates. No code is written.

### Project Structure Notes

- Architecture decisions live in `_bmad-output/planning-artifacts/architecture.md`
- Story 2.2 file: `_bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md`
- Epic 1 retrospective: `_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md` (Action Item #5)

### References

- [Source: architecture.md#Decision 1b — Session Journal: JSON with Markdown View]
- [Source: architecture.md#Decision 1c — Findings Ledger: JSONL (Global)]
- [Source: architecture.md#Decision 4b — Session Orientation Contract]
- [Source: architecture.md#Read/Write Authority]
- [Source: architecture.md#File Tree]
- [Source: epics.md#Story 1.9 — journal.json JSONL Migration Evaluation]
- [Source: epics.md#Story 2.2 — Session Orientation and Thread Management]
- [Source: epic-1-retro-2026-03-22.md#Action Item #5]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → unclassified (documentation/evaluation)

All tasks in this story are documentation and architectural evaluation tasks. No Momentum-specific guidance applies — standard bmad-dev-story DoD covers the work. The output is an architecture decision record and (conditionally) spec updates to architecture.md and Story 2.2.

**DoD note:** The standard bmad-dev-story DoD applies. No EDD, TDD, or functional verification is required — this story produces evaluation documentation and architecture decisions, not executable artifacts.

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
