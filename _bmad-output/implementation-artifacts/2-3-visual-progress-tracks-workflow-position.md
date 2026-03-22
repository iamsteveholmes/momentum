# Story 2.3: Visual Progress Tracks Workflow Position

Status: ready-for-dev

## Story

As a developer,
I want Impetus to show me exactly where I am in any workflow with a consistent 3-line indicator,
So that I'm never lost and always know what's completed and what's next.

## Acceptance Criteria

1. **Given** a developer enters any Momentum workflow via Impetus
   **When** a workflow is entered or a phase transitions (UX-DR2)
   **Then** Impetus displays the Progress Indicator using ✓/→/◦ symbols
   **And** completed steps collapse to a single ✓ line with a value summary phrase
   **And** the current step stands alone with a one-phrase description
   **And** upcoming steps collapse to a single ◦ line

2. **Given** a developer is at the very first step of a workflow (no completed steps yet)
   **When** the Progress Indicator is displayed
   **Then** the ✓ completed line is absent — the indicator is 2 lines at workflow start (→ current, ◦ upcoming only)

3. **Given** a developer is at the very last step of a workflow (no upcoming steps)
   **When** the Progress Indicator is displayed
   **Then** the ◦ upcoming line is absent — the indicator is 2 lines at workflow end (✓ completed, → current only)

4. **Given** any symbol appears in any Impetus, hook, or subagent response
   **When** rendered in any terminal or text context (UX-DR9)
   **Then** each symbol is paired with text — meaning is recoverable without symbol rendering
   **And** the symbol vocabulary is consistent across all Momentum components: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision

5. **Given** a developer is at a Workflow Step
   **When** Impetus renders it (UX-DR4)
   **Then** the step contains: narrative orientation line, substantive content, transition signal, explicit user control [A/P/C or equivalent]
   **And** the orientation line is narrative — never contains a step count in "Step N/M" format
   **And** user control is always the final element

6. **Given** a workflow is interrupted mid-step
   **When** the developer re-invokes `/momentum` in a new session (UX-DR17)
   **Then** Impetus identifies the interrupted workflow from the ledger
   **And** presents the Progress Indicator showing which steps are complete
   **And** asks: "continue from here, or restart this step?"
   **And** sufficient context is in the ledger entry to re-orient without developer re-explanation

7. **Given** a developer asks for their current position in any workflow (FR7)
   **When** Impetus responds
   **Then** a visual ASCII status graphic shows completed / current / upcoming phases
   **And** the representation uses only characters available in any terminal

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

- [ ] Task 4: Define ledger integration for workflow resumption (AC: 6)
  - [ ] 4.1 Specify what fields the progress indicator reads from `ledger.json` thread entries to reconstruct state: `current_step`, `phase`, workflow step list
  - [ ] 4.2 Specify the resume behavior: read ledger → build indicator showing completed/current/upcoming → present with "continue from here, or restart this step?"
  - [ ] 4.3 Specify the sufficiency criteria for `context_summary` in ledger entries — must include enough detail for indicator reconstruction without re-reading the workflow definition. Note: Story 2.2 owns ledger writes; this task only specifies format and sufficiency requirements that 2.2's phase-transition logic must satisfy

- [ ] Task 5: Create behavioral evals (EDD) (AC: 1–7)
  - [ ] 5.1 `eval-progress-mid-workflow.md` — Verify 3-line indicator at a middle step shows ✓/→/◦ with narrative content
  - [ ] 5.2 `eval-progress-first-step.md` — Verify 2-line indicator at first step (→/◦ only, no ✓)
  - [ ] 5.3 `eval-progress-last-step.md` — Verify 2-line indicator at last step (✓/→ only, no ◦)
  - [ ] 5.4 `eval-progress-resume-from-ledger.md` — Verify interrupted workflow resumes with correct indicator state and offers continue/restart
  - [ ] 5.5 `eval-symbol-text-pairing.md` — Verify every symbol in a response has adjacent text carrying the same meaning

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

Example at mid-workflow:
```
  ✓  Brief · Research · PRD          vision through requirements done
  →  UX Design                       building interaction patterns
  ◦  Architecture · Epics · Stories  3 phases to implementation
```

Example at first step:
```
  →  Brief                           capturing the core product idea
  ◦  Research · PRD · UX · Arch      5 phases ahead
```

Example at last step:
```
  ✓  Brief · Research · PRD · UX     foundation through interaction patterns
  →  Architecture                    making implementation decisions
```

### Symbol Vocabulary (Single Source of Truth)

| Symbol | Meaning | Paired text example |
|--------|---------|---------------------|
| ✓ | completed / confirmed / passing | "✓ Built: vision through requirements done" |
| → | current / active / in progress | "→ Now: building interaction patterns" |
| ◦ | upcoming / pending / next | "◦ Next: 3 phases to implementation" |
| ! | warning / attention needed | "! This thread appears active in another tab" |
| ✗ | failed / blocked | "✗ lint check failed — missing semicolon at auth.ts:42" |
| ? | question / decision required | "? Which authentication provider should we use?" |

This vocabulary is used by Impetus, all hooks, and all subagent output synthesis. Consistency is mandatory.

### Relationship to Stories 2.1 and 2.2

This story builds on:
- **Story 2.1** (Impetus skill creation): Establishes the menu, voice rules, input interpretation, Response Architecture Pattern (UX-DR15). The progress indicator is rendered *within* this pattern.
- **Story 2.2** (Session orientation / thread management): Establishes the session ledger (`ledger.json`), thread lifecycle, and resume behavior. The progress indicator *reads* ledger state to reconstruct workflow position after interruption.

**Dependency note:** Stories 2.1 and 2.2 are both `ready-for-dev` — they may or may not be implemented before this story. The progress indicator logic should be self-contained in `references/` so it works regardless of implementation order.

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
| `skills/momentum/references/progress-indicator.md` | Create | Canonical format, collapse rules, boundary rules, symbol vocabulary |
| `skills/momentum/evals/eval-progress-mid-workflow.md` | Create | Eval: 3-line indicator at mid-workflow |
| `skills/momentum/evals/eval-progress-first-step.md` | Create | Eval: 2-line indicator at first step |
| `skills/momentum/evals/eval-progress-last-step.md` | Create | Eval: 2-line indicator at last step |
| `skills/momentum/evals/eval-progress-resume-from-ledger.md` | Create | Eval: resume interrupted workflow with indicator |
| `skills/momentum/evals/eval-symbol-text-pairing.md` | Create | Eval: symbol accessibility |

**Constraint:** `workflow.md` must stay ≤500 lines total (including content from Stories 1.3, 1.4, 2.1, 2.2). Heavy reference content goes in `references/progress-indicator.md`.

### Testing Strategy (Eval-Driven Development)

Each eval simulates a scenario and verifies Impetus renders the correct indicator format. Evals are behavioral — they test what Impetus *outputs*, not executable code.

**Eval structure pattern** (established in Story 2.1):
- Input: simulated workflow state (step position, completed steps, upcoming steps)
- Expected: specific indicator format with narrative content
- Fail criteria: numeric step counts, missing symbols, missing text pairing, wrong line count

### NFR Compliance

- **NFR1**: Progress indicator reference doc does not increase SKILL.md description (stays ≤150 chars)
- **NFR3**: Overflow content in `references/progress-indicator.md`, loaded on demand
- **UX-DR2**: Every phase transition displays the indicator
- **UX-DR4**: Response Architecture Pattern followed (orientation → content → transition → control)
- **UX-DR9**: Symbols paired with text for accessibility
- **UX-DR15**: Response Architecture Pattern structure enforced
- **UX-DR17**: Workflow resumability with indicator reconstruction from ledger

### Project Structure Notes

- All files under `skills/momentum/` per the canonical repository structure [Source: architecture.md, Repository Structure section]
- Evals directory at `skills/momentum/evals/` per pattern established in Story 2.1
- Reference documents at `skills/momentum/references/` per the micro-file architecture pattern
- `.claude/momentum/ledger.json` read (not written) by this story for indicator reconstruction

### References

- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 4a: Visual Progress Format]
- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 1b: Session Ledger JSON]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Symbol Vocabulary, 3-Line Standard]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Response Architecture Pattern]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md — Session Orientation Moments]
- [Source: _bmad-output/planning-artifacts/prd.md — FR7: Visual status graphics]
- [Source: _bmad-output/planning-artifacts/prd.md — FR42: Visual progress through story cycle]
- [Source: _bmad-output/planning-artifacts/epics.md — Epic 2, Story 2.3 acceptance criteria]
- [Source: _bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md — EDD eval pattern, voice rules]
- [Source: _bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md — Ledger schema, resume behavior]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
