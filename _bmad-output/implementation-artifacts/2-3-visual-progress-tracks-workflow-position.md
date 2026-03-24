# Story 2.3: Visual Progress Tracks Workflow Position

Status: ready-for-dev

## Story

As a developer,
I want Impetus to show me exactly where I am in any workflow with a consistent 3-line indicator,
so that I'm never lost and always know what's completed and what's next.

## Acceptance Criteria

**AC1 — Progress indicator at phase transition:**
**Given** a developer enters any Momentum workflow via Impetus
**When** a workflow is entered or a phase transitions (UX-DR2)
**Then** Impetus displays the Progress Indicator using ✓/→/◦ symbols
**And** completed steps collapse to a single ✓ line with a value summary phrase
**And** the current step stands alone with a one-phrase description
**And** upcoming steps collapse to a single ◦ line

**AC2 — Two-line indicator at workflow start:**
**Given** a developer is at the very first step of a workflow (no completed steps yet)
**When** the Progress Indicator is displayed
**Then** the ✓ completed line is absent — the indicator is 2 lines at workflow start (→ current, ◦ upcoming only)

**AC3 — Two-line indicator at workflow end:**
**Given** a developer is at the very last step of a workflow (no upcoming steps)
**When** the Progress Indicator is displayed
**Then** the ◦ upcoming line is absent — the indicator is 2 lines at workflow end (✓ completed, → current only)

**AC4 — Symbol vocabulary and text pairing:**
**Given** any symbol appears in any Impetus, hook, or subagent response
**When** rendered in any terminal or text context (UX-DR9)
**Then** each symbol is paired with text — meaning is recoverable without symbol rendering
**And** the symbol vocabulary is consistent across all Momentum components: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision

**AC5 — Response Architecture Pattern integration:**
**Given** a developer is at a Workflow Step
**When** Impetus renders it (UX-DR4)
**Then** the step contains: narrative orientation line, substantive content, transition signal, explicit user control [A/P/C or equivalent]
**And** the orientation line is narrative — never contains a step count in "Step N/M" format
**And** user control is always the final element

**AC6 — Interrupted workflow resumption:**
**Given** a workflow is interrupted mid-step
**When** the developer re-invokes `/momentum` in a new session (UX-DR17)
**Then** Impetus identifies the interrupted workflow from the journal
**And** presents the Progress Indicator showing which steps are complete
**And** asks: "continue from here, or restart this step?"
**And** sufficient context is in the journal entry to re-orient without developer re-explanation

**AC7 — On-demand position query:**
**Given** a developer asks for their current position in any workflow (FR7)
**When** Impetus responds
**Then** a visual status graphic shows completed / current / upcoming phases
**And** the representation uses only terminal-safe characters available in any terminal

## Tasks / Subtasks

- [ ] Task 1: Define progress indicator rendering logic in workflow.md (AC: 1, 2, 3, 7)
  - [ ] 1.1 Define the canonical 3-line format as a reusable instruction block in `skills/momentum/references/`
  - [ ] 1.2 Specify collapse rules: all completed → single ✓ line with value summary; all upcoming → single ◦ line
  - [ ] 1.3 Specify boundary rules: 2 lines at workflow start (no ✓), 2 lines at workflow end (no ◦)
  - [ ] 1.4 Specify the "on-demand position query" behavior — developer asks "where am I?" and gets the same indicator

- [ ] Task 2: Define symbol vocabulary and accessibility rules (AC: 4)
  - [ ] 2.1 Document the symbol vocabulary table in `skills/momentum/references/` as a single source of truth
  - [ ] 2.2 Specify the text-pairing rule: every symbol must have adjacent text conveying the same meaning
  - [ ] 2.3 Define the 80-char terminal width constraint — progress indicator must render cleanly without horizontal scrolling

- [ ] Task 3: Define the Response Architecture Pattern integration (AC: 5)
  - [ ] 3.1 Specify how the progress indicator fits within the Response Architecture Pattern: orientation line (which includes indicator) → substantive content → transition signal → user control
  - [ ] 3.2 Specify that orientation lines are always narrative ("We've established the project structure, now building interaction patterns") — never "Step 3/8"
  - [ ] 3.3 Specify that user control is always the final visible element (A/P/C or contextual equivalent)

- [ ] Task 4: Define journal integration for workflow resumption (AC: 6)
  - [ ] 4.1 Specify what fields the progress indicator reads from `journal.jsonl` thread entries to reconstruct state: `current_step`, `phase`, workflow step list
  - [ ] 4.2 Specify the resume behavior: read journal → build indicator showing completed/current/upcoming → present with "continue from here, or restart this step?"
  - [ ] 4.3 Specify the sufficiency criteria for `context_summary` in journal entries — must include enough detail for indicator reconstruction without re-reading the workflow definition. Note: Story 2.2 owns journal writes; this task only specifies format and sufficiency requirements that 2.2's phase-transition logic must satisfy. Output: `skills/momentum/references/progress-indicator.md` (context_summary requirements section)

- [ ] Task 5: Create behavioral evals (EDD) (AC: 1–7)
  - [ ] 5.1 `eval-progress-mid-workflow.md` — Verify 3-line indicator at a middle step shows ✓/→/◦ with narrative content
  - [ ] 5.2 `eval-progress-first-step.md` — Verify 2-line indicator at first step (→/◦ only, no ✓)
  - [ ] 5.3 `eval-progress-last-step.md` — Verify 2-line indicator at last step (✓/→ only, no ◦)
  - [ ] 5.4 `eval-progress-resume-from-ledger.md` — Verify interrupted workflow resumes with correct indicator state and offers continue/restart
  - [ ] 5.5 `eval-symbol-text-pairing.md` — Verify every symbol in a response has adjacent text carrying the same meaning
  - [ ] 5.6 `eval-response-architecture-pattern.md` — Verify a rendered workflow step contains all four elements: narrative orientation line, substantive content, transition signal, explicit user control; verify orientation line is never "Step N/M"
  - [ ] 5.7 `eval-on-demand-position-query.md` — Verify that when a developer asks "where am I?", Impetus responds with the correct 3-line (or 2-line at boundary) indicator using terminal-safe characters with text pairing

## Dev Notes

### Implementation Type

This is a **skill-instruction (EDD) + config-structure** story — same pattern as Stories 2.1 and 2.2. The deliverables are behavioral instructions in `workflow.md` and reference documents, validated through eval-driven development. No executable code is produced; the "code" is the skill instruction set that Impetus follows.

### Canonical Progress Indicator Format

Architecture Decision 4a (non-negotiable):

```
✓ Built: [what exists now — value accumulated, not tasks completed]
→ Now:   [this step and why it matters to the work]
◦ Next:  [what follows after this step]
```

Example at mid-workflow (4 completed, 1 current, 2 upcoming):
```
  ✓  Brief · Research · PRD · UX      vision through interaction patterns done
  →  Architecture                     making implementation decisions
  ◦  Epics · Stories                  2 phases to implementation
```

Example at first step (0 completed, 1 current, 6 upcoming):
```
  →  Brief                                         capturing the core product idea
  ◦  Research · PRD · UX · Arch · Epics · Stories  6 phases ahead
```

Example at last step (6 completed, 1 current, 0 upcoming):
```
  ✓  Brief · Research · PRD · UX · Arch · Epics  foundation through planned work
  →  Stories                                      breaking the work into deliverables
```

The workflow phases are (in order): Brief, Research, PRD, UX, Architecture, Epics, Stories — 7 phases total.

### Symbol Vocabulary (Single Source of Truth)

| Symbol | Meaning | Paired text example |
|--------|---------|---------------------|
| ✓ | completed / confirmed / passing | "✓ Built: vision through requirements done" |
| → | current / active / in progress | "→ Now: building interaction patterns" |
| ◦ | upcoming / pending / next | "◦ Next: 3 phases to implementation" |
| ! | warning / attention needed | "! This thread appears active in another tab" |
| ✗ | failed / blocked | "✗ lint check failed — missing semicolon at auth.ts:42" |
| ? | question / decision required | "? Which authentication provider should we use?" |
| · | item / detail / minor finding | "· src/ledger.ts — LedgerEntry type + CRUD operations" |

This vocabulary is used by Impetus, all hooks, and all subagent output synthesis. Consistency is mandatory.

### Relationship to Stories 2.1 and 2.2

This story builds on:
- **Story 2.1** (Impetus skill creation): Establishes the menu, voice rules, input interpretation, Response Architecture Pattern (UX-DR15). The progress indicator is rendered *within* this pattern.
- **Story 2.2** (Session orientation / thread management): Establishes the session journal (`journal.json`), thread lifecycle, and resume behavior. The progress indicator *reads* journal state to reconstruct workflow position after interruption.

**Dependency note:** Stories 2.1 and 2.2 are both `ready-for-dev` — they may or may not be implemented before this story. The progress indicator logic should be self-contained in `references/` so it works regardless of implementation order.

### Cross-Story Coordination

**Story 2.2 dependency (Task 4.3):** Task 4.3 defines the sufficiency criteria for `context_summary` in journal entries. Story 2.2 owns all ledger write operations. Before closing this story, confirm with Story 2.2's implementation that the `context_summary` field in every phase-transition write satisfies the criteria specified in `skills/momentum/references/progress-indicator.md`. If Story 2.2 is already implemented, the dev agent must review its `context_summary` write logic against this story's criteria and file a finding if the format is insufficient.

### Key Design Constraints

1. **Terminal-first**: All output must render cleanly in any terminal. No color dependency. Tested at 80-char and 120-char width.
2. **Never numeric**: "Step 3/8" is explicitly banned. All orientation is narrative.
3. **Text-paired symbols**: Every ✓/→/◦ must have adjacent text so meaning survives if Unicode doesn't render.
4. **Collapse, don't enumerate**: Completed steps collapse to ONE line summarizing accumulated value. Upcoming steps collapse to ONE line. The indicator never grows with workflow length.
5. **Anti-patterns to avoid**: "Continuing...", "Moving on to...", "Great work!", ellipsis counts, special syntax.

### File Structure

Files this story creates or modifies:

| File | Action | Purpose |
|------|--------|---------|
| `skills/momentum/workflow.md` | Modify | Add progress indicator rendering instructions at phase transitions |
| `skills/momentum/references/progress-indicator.md` | Create | Canonical format, collapse rules, boundary rules, symbol vocabulary, context_summary sufficiency criteria |
| `skills/momentum/evals/eval-progress-mid-workflow.md` | Create | Eval: 3-line indicator at mid-workflow |
| `skills/momentum/evals/eval-progress-first-step.md` | Create | Eval: 2-line indicator at first step |
| `skills/momentum/evals/eval-progress-last-step.md` | Create | Eval: 2-line indicator at last step |
| `skills/momentum/evals/eval-progress-resume-from-ledger.md` | Create | Eval: resume interrupted workflow with indicator |
| `skills/momentum/evals/eval-symbol-text-pairing.md` | Create | Eval: symbol accessibility |
| `skills/momentum/evals/eval-response-architecture-pattern.md` | Create | Eval: Response Architecture Pattern structure (AC5) |
| `skills/momentum/evals/eval-on-demand-position-query.md` | Create | Eval: on-demand position query response (AC7) |

**Constraint:** `workflow.md` must stay ≤500 lines total (including content from Stories 1.3, 1.4, 2.1, 2.2). Heavy reference content goes in `references/progress-indicator.md`.

### Testing Strategy (Eval-Driven Development)

Each eval simulates a scenario and verifies Impetus renders the correct indicator format. Evals are behavioral — they test what Impetus *outputs*, not executable code.

**Eval structure pattern** (established in Story 2.1):
- Input: simulated workflow state (step position, completed steps, upcoming steps)
- Expected: specific indicator format with narrative content
- Fail criteria: numeric step counts, missing symbols, missing text pairing, wrong line count

### NFR Compliance

- **NFR3**: Overflow content in `references/progress-indicator.md`, loaded on demand
- **UX-DR2**: Every phase transition displays the indicator
- **UX-DR4**: Response Architecture Pattern followed (orientation → content → transition → control)
- **UX-DR9**: Symbols paired with text for accessibility
- **UX-DR15**: Response Architecture Pattern structure enforced
- **UX-DR17**: Workflow resumability with indicator reconstruction from journal

### Project Structure Notes

- All files under `skills/momentum/` per the canonical repository structure [Source: architecture.md, Repository Structure section]
- Evals directory at `skills/momentum/evals/` per pattern established in Story 2.1
- Reference documents at `skills/momentum/references/` per the micro-file architecture pattern
- `.claude/momentum/journal.jsonl` read (not written) by this story for indicator reconstruction

### References

- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 4a: Visual Progress Format]
- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 1b: Session Journal JSON]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Symbol Vocabulary]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Progress Indicator Standard]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Response Architecture Pattern]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Step Re-entry After Interruption]
- [Source: _bmad-output/planning-artifacts/prd.md — FR7: Visual status graphics]
- [Source: _bmad-output/planning-artifacts/prd.md — FR42: Visual progress through story cycle]
- [Source: _bmad-output/planning-artifacts/epics.md — Epic 2, Story 2.3 acceptance criteria]
- [Source: _bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md — EDD eval pattern, voice rules]
- [Source: _bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md — Journal schema, resume behavior]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD) — extending workflow.md with progress indicator logic and reference documents
- Task 1.1 → config-structure (direct) — creating `references/progress-indicator.md` (reference file, not executable skill instruction)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md.** Use EDD:

**Write evals first** in `skills/momentum/evals/`:
- `eval-progress-mid-workflow.md` — Given Impetus is at a middle workflow step with 3 completed phases and 3 upcoming, it should display all 3 indicator lines (✓/→/◦) with narrative content; no "Step N/M"; each symbol has adjacent text
- `eval-progress-first-step.md` — Given Impetus is at the first step of a workflow (no completed phases), it should display 2 lines only (→/◦); the ✓ line must be absent
- `eval-progress-last-step.md` — Given Impetus is at the last step of a workflow (no upcoming phases), it should display 2 lines only (✓/→); the ◦ line must be absent
- `eval-progress-resume-from-ledger.md` — Given a journal entry with `current_step` and `context_summary` for an interrupted workflow, Impetus should reconstruct and display the correct indicator state and offer "continue from here, or restart this step?"
- `eval-symbol-text-pairing.md` — Given any Impetus response containing ✓/→/◦/!/✗/? symbols, every symbol must have adjacent text conveying the same meaning; verify no symbol appears without paired text
- `eval-response-architecture-pattern.md` — Given Impetus renders a workflow step, the response must contain all four elements in order: narrative orientation line (with progress indicator), substantive content, transition signal, explicit user control; orientation line must never contain "Step N/M"
- `eval-on-demand-position-query.md` — Given a developer types "where am I?" or "what's my current position?", Impetus should respond with the correct progress indicator (3-line or 2-line at boundary) using only terminal-safe characters, with all symbols text-paired

**Then implement:** extend workflow.md, create references/progress-indicator.md

**Then verify:** spawn subagent per eval, observe behavior. Max 3 fix cycles per eval.

**NFR compliance:**
- workflow.md body ≤500 lines (check combined length with Stories 1.3/1.4/2.1/2.2 content; if over, extract reference content)
- Progress indicator reference content in `references/progress-indicator.md`

**Additional DoD items:**
- [ ] 7 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all 7 eval behaviors confirmed
- [ ] `references/progress-indicator.md` created with canonical format, collapse rules, boundary rules, symbol vocabulary, and context_summary sufficiency criteria
- [ ] workflow.md ≤500 lines confirmed (or overflow in references/)
- [ ] Cross-story coordination with Story 2.2 verified: context_summary write logic reviewed against sufficiency criteria
- [ ] AVFL checkpoint documented

---

### config-structure Tasks: Direct Implementation

For `references/progress-indicator.md`:
- Write the canonical 3-line format block as a reusable instruction
- Include all collapse rules, boundary rules, the symbol vocabulary table, and context_summary sufficiency criteria
- This is a markdown reference file — verify it is well-formed markdown
- No special validation needed beyond visual inspection

---

## Acceptance Test Plan

**Story type:** skill-instruction
**Verification method:** EDD — adversarial eval authoring by an independent acceptance tester
**Test artifacts location:** `skills/momentum/evals/`
**Acceptance tester:** unassigned

### Test Scenarios

1. **Eval: progress-mid-workflow** — Given Impetus is at a middle workflow step (3 completed phases, 1 current, 3 upcoming), trigger a phase transition. All 3 indicator lines must appear (✓/→/◦) with narrative content. Fail if: "Step N/M" appears anywhere, a symbol appears without adjacent text, or line count is not exactly 3.

2. **Eval: progress-first-step** — Given Impetus is at the very first step of a workflow (no completed phases), display the indicator. Only 2 lines must appear (→ current, ◦ upcoming). Fail if: ✓ completed line appears, or 3 lines shown.

3. **Eval: progress-last-step** — Given Impetus is at the very last step (no upcoming phases), display the indicator. Only 2 lines must appear (✓ completed, → current). Fail if: ◦ upcoming line appears, or 3 lines shown.

4. **Eval: progress-resume-from-journal** — Given a journal entry with `current_step` and `context_summary` for an interrupted workflow, invoke `/momentum` in a fresh session. Impetus must reconstruct and display the correct indicator state and offer "continue from here, or restart this step?" — without the developer re-explaining context. Fail if: developer must re-explain their state, or indicator shows wrong position.

5. **Eval: symbol-text-pairing** — Given any Impetus response containing ✓/→/◦/!/✗/? symbols, every symbol must have adjacent text conveying the same meaning. Fail if: any symbol appears in isolation without accompanying text.

6. **Eval: response-architecture-pattern** — Given Impetus renders a workflow step, the response must contain all four elements in order: narrative orientation line (with progress indicator), substantive content, transition signal, explicit user control. Fail if: orientation line contains "Step N/M", user control is not the final element, or any element is absent.

7. **Eval: on-demand-position-query** — Given a developer types "where am I?", Impetus must respond with the correct progress indicator (3-line or 2-line at boundary) using only terminal-safe characters, with all symbols text-paired. Fail if: response requires color rendering, contains numeric step count, or symbols lack text pairing.

### Acceptance Gate

This story passes acceptance when:
- AC1: Phase transition displays 3-line ✓/→/◦ indicator with narrative content, no "Step N/M"
- AC2: First step displays 2 lines (→/◦ only, ✓ absent)
- AC3: Last step displays 2 lines (✓/→ only, ◦ absent)
- AC4: Every symbol in every response has adjacent text pairing
- AC5: Every rendered workflow step contains all four Response Architecture Pattern elements
- AC6: Interrupted workflow resumes with correct indicator state using journal context
- AC7: On-demand query returns correct indicator with terminal-safe characters

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
