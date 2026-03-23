# Story 2.2: Session Orientation and Thread Management

Status: ready-for-dev

## Story

As a developer,
I want Impetus to tell me where I am at every session start and track open threads across sessions and tabs,
so that I can pick up any thread without hunting for context.

## Acceptance Criteria

**AC1 — Session orientation:**
Given a developer invokes `/momentum`,
When Impetus starts (UX-DR11),
Then within two exchanges, Impetus surfaces: active story/task, current phase, last completed action, and suggested next action
And Impetus speaks first — the developer is never required to ask "where were we?"

**AC2 — Journal display (threads exist):**
Given the journal at `.claude/momentum/journal.jsonl` contains one or more open thread entries,
When Impetus starts (UX-DR1),
Then Impetus displays the Session Journal: numbered list of open threads, each showing workflow phase and elapsed time
And threads are ordered by most-recently-active
And each thread is directly selectable by its number

**AC3 — Empty journal (no threads):**
Given no journal exists or the journal is empty,
When Impetus starts,
Then the Session Journal display is absent
And Impetus transitions directly to new-session orientation (menu from Story 2.1)

**AC4 — Multi-tab concurrent work detection:**
Given a developer is running a workflow in Tab A,
When they open Tab B and invoke `/momentum` (UX-DR13),
Then Impetus in Tab B reads the shared journal and surfaces Tab A's active thread
And if the entry was timestamped within the last 30 minutes, Impetus flags it as likely intentional concurrent work
And asks the developer to confirm before starting a competing thread on the same story

**AC5 — Dormant thread hygiene:**
Given a journal entry has had no activity beyond the configured dormancy threshold (default: 3 days),
When Impetus starts (UX-DR14),
Then Impetus surfaces the dormant thread with brief context and offers one-action closure
And closure requires exactly one developer confirmation
And if confirmed, the thread is marked closed in the journal

**AC6 — Dependency-satisfied thread notification:**
Given a story or workflow that another journal thread depended on has just completed,
When Impetus detects the dependency is satisfied (UX-DR14),
Then Impetus surfaces the waiting thread at session start with "The work this thread was waiting on is complete — ready to continue?"
And the developer decides whether to activate the waiting thread

**AC7 — Unwieldy journal triage:**
Given the session journal has grown to more than 5 open threads,
When Impetus starts (UX-DR14),
Then Impetus flags the journal size and offers a triage pass before starting new work
And triage surfaces each thread's status and age with a single-action close option

**AC8 — Workflow resumability:**
Given the developer starts Impetus in a fresh context after an interruption,
When Impetus reads the journal entry for the interrupted workflow (UX-DR17),
Then Impetus re-orients using saved journal context — no developer re-explanation required
And offers: "continue from here, or restart this step?" before proceeding

## Tasks / Subtasks

- [ ] Task 1: Define and implement journal.jsonl schema (AC: 1–8)
  - [ ] 1.1: Create `skills/momentum/references/journal-schema.md` documenting the JSONL schema for `.claude/momentum/journal.jsonl` — each line is one JSON object with fields: thread_id, workflow_type, story_ref, current_step, phase, last_action, context_summary, last_active (ISO 8601), status (open|closed), depends_on_thread. Current state of a thread = last entry with that thread_id.
  - [ ] 1.2: Implement journal read/write helpers in workflow.md — read all lines, reconstruct current state per thread_id (last entry wins), append new entries (never overwrite)

- [ ] Task 2: Implement session orientation logic in workflow.md (AC: 1, 3)
  - [ ] 2.1: At startup (after install/upgrade routing from Stories 1.3/1.4), read journal.jsonl
  - [ ] 2.2: If journal is empty or absent → skip display, go to menu (Story 2.1 normal session)
  - [ ] 2.3: If threads exist → display Session Journal (Task 3), then orient with active story, phase, last action, suggested next

- [ ] Task 3: Implement Session Journal Display component (AC: 2)
  - [ ] 3.1: Format: numbered list of open threads, each showing workflow phase + elapsed time since last activity
  - [ ] 3.2: Order by most-recently-active first
  - [ ] 3.3: Each thread selectable by number (integrates with input interpretation from Story 2.1)
  - [ ] 3.4: End with "Continue (1/2/3) or tell me what you need?"

- [ ] Task 4: Implement multi-tab concurrent work detection (AC: 4)
  - [ ] 4.1: When reading journal, check each open entry's `last_active` timestamp
  - [ ] 4.2: If any entry was active within 30 minutes → flag as concurrent: "This thread appears active in another tab (N minutes ago)."
  - [ ] 4.3: Ask developer to confirm before starting a competing thread on the same story

- [ ] Task 5: Implement dormant thread hygiene (AC: 5, 7)
  - [ ] 5.1: At session start, scan for entries with `last_active` > 3 days ago → surface each with context and one-action close offer
  - [ ] 5.2: If >5 open threads, offer triage pass with per-thread status + age + close option
  - [ ] 5.3: Closure = set status to "closed" in journal, one confirmation required

- [ ] Task 6: Implement dependency-satisfied notification (AC: 6)
  - [ ] 6.1: When reading journal, check `depends_on_thread` field for each entry
  - [ ] 6.2: If the depended-on thread is now "closed" → surface: "The work this thread was waiting on is complete — ready to continue?"

- [ ] Task 7: Implement workflow resumability (AC: 8)
  - [ ] 7.1: When a thread is selected (by number or "continue"), read its `current_step`, `last_action`, and `context_summary`
  - [ ] 7.2: Display re-orientation: "[context_summary]. Continue from here, or restart this step?"
  - [ ] 7.3: On continue → resume at `current_step`; on restart → reset `current_step` to start of that phase

- [ ] Task 8: Implement auto-generated journal-view.md (AC: 1)
  - [ ] 8.1: After any journal.jsonl write, regenerate `.claude/momentum/journal-view.md` as a human-readable markdown view of all entries (open and recently closed)

## Dev Notes

### Prerequisite: Stories 1.3, 1.4, 2.1

This story extends the Impetus workflow.md created in Stories 1.3/1.4 and the menu/persona from Story 2.1. The startup routing order becomes:

```
/momentum invoked
  → installed.json absent? → Journey 0 (Story 1.3)
  → version mismatch? → Journey 4 (Story 1.4)
  → versions match → READ JOURNAL (this story, Story 2.2)
    → journal empty? → menu (Story 2.1)
    → threads exist? → Session Journal Display → orient → user selects
```

### Journal Schema

Per architecture Decision 1b (updated by Story 1.9), the journal lives at `.claude/momentum/journal.jsonl` using JSONL append-only format. Each line is one JSON object:

```jsonl
{"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Code reviewer dispatched","context_summary":"Story 4.2 implementation — reviewer is analyzing the null-check pattern","last_active":"2026-03-21T14:30:00Z","status":"open","depends_on_thread":null}
```

**Write semantics:** Every state change (thread created, step advanced, thread closed) appends a new line. Never overwrite or modify existing lines.

**Read semantics:** Read all lines, group by `thread_id`, take the last entry per thread. This gives current state. Filter by `status: open` for active threads.

**Thread ID format:** `T-NNN` (auto-incrementing). New thread created when a workflow starts; closed when the workflow completes or developer explicitly closes.

**`context_summary`:** Must contain enough information to re-orient the developer in a fresh session WITHOUT re-reading the story file. One sentence, specific. Bad: "Working on story." Good: "Story 4.2 — the null-check pattern was flagged by the reviewer; 3 findings remain to address."

[Source: architecture.md#Decision 1b; epics.md Story 2.2 AC8 — "re-orients using saved journal context"]

### Session Journal Display Format (UX Component 1)

```
3 threads in progress:

  1.  Story 4.2 implementation      mid-review          2h ago
  2.  UX design specification       visual foundation   yesterday
  3.  Architecture research         awaiting your input  5d ago

Continue (1/2/3) or tell me what you need?
```

The `5d ago` entry would trigger dormant thread hygiene (3-day threshold). Impetus would surface it separately after the display.

[Source: ux-design-specification.md#Component 1 Session Journal Display]

### Multi-Tab Detection (UX-DR13)

The journal is a shared JSONL file — all Claude Code tabs (each an independent Impetus instance) append to it. JSONL append is concurrency-safe (POSIX atomic append for lines under pipe buffer size), so no file locking is needed for writes. The 30-minute timestamp check is a heuristic for detecting *intentional* concurrent work, not a concurrency control mechanism.

**Warning format:**
```
  !  This thread appears active in another tab (4 minutes ago).
     Opening here may cause conflicts. Proceed anyway?
```

Warn, never block — the developer decides.

[Source: ux-design-specification.md#Conflicting Thread Warning]

### Dormant Thread and Triage (UX-DR14)

Three triggers for thread hygiene:
1. **Time-based:** Entry with `last_active` > 3 days → surface for closure
2. **Contextual:** Dependency satisfied (depended-on thread closed) → surface for continuation
3. **Unwieldy:** >5 open threads → offer triage pass

All hygiene actions are low-friction: one confirmation to close, one confirmation to continue. Never two questions to resolve a single thread.

### Workflow Resumability (UX-DR17)

Every workflow must be resumable from any step. The `current_step` + `context_summary` fields in the journal provide the re-orientation data. When a developer selects a thread:

```
  You were mid-way through code review on Story 4.2.
  Three reviewer findings remain — the null-check pattern and two import issues.

  Continue from here, or restart the review step?
```

The developer never needs to re-explain what they were doing. Impetus has all context in the journal entry.

[Source: ux-design-specification.md#Step Re-entry After Interruption]

### Journal-View.md Auto-Generation

Per architecture Decision 1b: "Auto-generated `.claude/momentum/journal-view.md` for human readability." After every journal.jsonl append, regenerate this file. It's a read-only markdown view — developers can inspect it but Impetus only reads/writes the JSONL.

### Spec Fatigue Patterns

Session orientation is a brief, single-exchange interaction — not a review checkpoint where spec fatigue patterns (UX-DR19–22) primarily apply. The ledger display (AC2) and thread triage (AC7) already implement attention-management principles by design: the ledger is a compact summary, and triage surfaces only actionable threads. The full spec fatigue patterns (tiered review depth, expertise-adaptive orientation, motivated disclosure, confidence-directed review) are exercised downstream in Stories 2.4, 2.5, and Epic 4 where developers review substantive generated content.

### References

- [Source: epics.md#Story 2.2 — All Acceptance Criteria]
- [Source: architecture.md#Decision 1b — Session Journal: JSONL with Markdown View]
- [Source: architecture.md#Decision 4b — Session Orientation Contract]
- [Source: ux-design-specification.md#Component 1 Session Journal Display]
- [Source: ux-design-specification.md UX-DR1 — Session Journal Display]
- [Source: ux-design-specification.md UX-DR11 — Session Orientation Contract]
- [Source: ux-design-specification.md UX-DR13 — Multi-Thread Journal Awareness]
- [Source: ux-design-specification.md UX-DR14 — Thread Hygiene]
- [Source: ux-design-specification.md UX-DR17 — Workflow Resumability]
- [Source: ux-design-specification.md#Step Re-entry After Interruption]
- [Source: ux-design-specification.md#Conflicting Thread Warning]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–7 → skill-instruction (EDD) — extending workflow.md with journal logic
- Task 8 → config-structure (direct) — journal-view.md auto-generation
- Task 1.1 → config-structure (direct) — journal-schema.md reference file

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Write evals first** in `skills/momentum/evals/`:
- `eval-session-orientation-with-threads.md` — Given 2 open threads in journal.jsonl, Impetus should display numbered list ordered by most-recent, with phase and elapsed time, then orient to the most recent thread's active story/phase/last action
- `eval-empty-journal-skip.md` — Given no journal.jsonl exists, Impetus should skip journal display entirely and show the menu (Story 2.1 normal session path)
- `eval-dormant-thread-closure.md` — Given a journal entry with last_active > 3 days ago, Impetus should surface it with context and offer one-action closure; after developer confirms, entry status changes to "closed"
- `eval-concurrent-tab-warning.md` — Given a journal entry with last_active 5 minutes ago, Impetus should warn about concurrent work and ask to confirm before starting a competing thread

**Then implement.** Max 3 fix cycles per eval.

**NFR compliance:**
- workflow.md total ≤500 lines (significant content being added — use references/ for overflow, especially journal-schema.md)
- Journal operations (read/write/parse) are behavioral instructions, not executable code — describe WHAT Impetus should do, not HOW in a programming sense

**Additional DoD items:**
- [ ] 4 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all 4 eval behaviors confirmed
- [ ] `references/journal-schema.md` created with full JSONL schema
- [ ] Journal read/write described in workflow.md
- [ ] journal-view.md auto-generation described
- [ ] AVFL checkpoint documented

---

### config-structure Tasks: Direct Implementation

For `journal-schema.md` and journal-view.md generation logic:
- Validate the schema example parses as valid JSON
- Verify all required fields are documented with types
- Document in Dev Agent Record

---

## Acceptance Test Plan

**Story type:** skill-instruction
**Verification method:** EDD — adversarial eval authoring by an independent acceptance tester
**Test artifacts location:** `skills/momentum/evals/`
**Acceptance tester:** unassigned

### Test Scenarios

1. **Eval: session-orientation-with-threads** — Given a journal.json with 2 open threads (one active 2 hours ago, one active yesterday), invoke `/momentum`. Impetus must display a numbered list ordered by most-recently-active, with workflow phase and elapsed time for each. Within two exchanges, Impetus must surface active story, current phase, last completed action, and suggested next action. Fail if: threads appear out of order, elapsed time is missing, or developer must ask "where were we?"

2. **Eval: empty-journal-skip** — Given no journal.json exists at `.claude/momentum/journal.json`, invoke `/momentum`. Impetus must skip the journal display entirely and transition directly to the menu (Story 2.1 normal session). Fail if: journal section appears, error message appears, or user is asked to create a journal.

3. **Eval: dormant-thread-closure** — Given a journal entry with `last_active` timestamp >3 days ago, invoke `/momentum`. Impetus must surface the dormant thread with brief context and offer one-action closure. After developer confirms with a single response, the thread status must change to "closed". Fail if: requires more than one confirmation, thread not marked closed after confirmation, or dormant thread is not surfaced.

4. **Eval: concurrent-tab-warning** — Given a journal entry with `last_active` timestamp 5 minutes ago (simulating an active tab), invoke `/momentum`. Impetus must flag the entry as likely concurrent work and ask to confirm before starting a competing thread on the same story. Fail if: no warning shown, or warning is blocking (must warn, not block).

### Acceptance Gate

This story passes acceptance when:
- AC1: Within two exchanges, Impetus surfaces active story, phase, last completed action, and next action — without developer prompting
- AC2: Journal with threads displays ordered numbered list with phase and elapsed time
- AC3: Empty journal skips directly to menu with no display artifact
- AC4: Entry active within 30 minutes triggers concurrent work warning (non-blocking)
- AC5: Entry >3 days old triggers one-action closure offer; confirmation closes thread
- AC8: Selecting a thread re-orients using journal context with "continue from here, or restart this step?"

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
