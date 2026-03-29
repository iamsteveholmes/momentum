# Story 2a.3: Session-Open Menu Redesign

Status: done

## Story

As a developer,
I want the session menu to show only the actions I'd actually initiate,
so that I'm not presented with diagnostic tools or auto-triggered workflows as if they were my choices.

## Acceptance Criteria

1. **Given** a returning user (`momentum_completions >= 1`) with no open threads, **When** the session menu renders, **Then** it contains exactly 2 items: `/create` (write a story) and `/develop` (build the next story), and validate, plan review, spec provenance, and session threads do not appear as primary menu items
2. **Given** the primary menu is displayed, **When** the developer types `/create` or `1`, **Then** Impetus dispatches to the create-story workflow; **When** the developer types `/develop` or `2`, **Then** Impetus dispatches to the develop-story workflow; **And** both slash command and number inputs work equivalently
3. **Given** open journal threads exist, **When** the session opens, **Then** journal threads are displayed before the menu (existing Story 2.2 behavior), and they are not duplicated as a menu item

## Tasks / Subtasks

### Task 1: Replace 6-item menu with 2-item menu in Step 7 (AC: #1, #2, #3) — skill-instruction

- [ ] 1.1: In `skills/momentum/workflow.md`, locate the Step 7 `<check if="journal.jsonl does not exist OR has zero open threads">` block (currently lines 366–384). Replace the 6-item `<output>` block with the 2-item menu:
  ```
  Everything's in place — let's build something.

    /create   Write a story
    /develop  Build the next story

  What would you like to work on?
  ```
  The new `<output>` block must render the menu with `/create` and `/develop` as the primary affordances. Number aliases (`1` for `/create`, `2` for `/develop`) must work equivalently — add a `<note>` immediately after the output: "Number aliases: 1 = /create, 2 = /develop. Both forms dispatch identically."

- [ ] 1.2: Remove the existing items 3–6 (Review a plan, Run quality validation, Audit spec provenance, Show session threads) entirely from the Step 7 menu block. These workflows are not removed from the system — they remain accessible via natural language input, which the Input Interpretation gate handles. The primary menu no longer advertises them.

- [ ] 1.3: Verify the `<note>` for the natural language gate (currently line 386) remains intact and unchanged after the output block: "Natural language gate: If developer input is natural language (not a menu number), apply the Input Interpretation structural gate — confirm extracted intent before dispatching to any workflow. Do not skip confirmation even if the intent seems obvious." This gate is the fallback for items 3–6 and any other requests.

- [ ] 1.4: Verify the `<check if="one or more open threads exist">` block (currently line 388–390) remains intact immediately after the natural language gate note. Thread display (GOTO step 11) is unchanged.

### Task 2: Add dispatch actions for `/create` and `/develop` in Step 7 (AC: #2) — skill-instruction

- [ ] 2.1: After the 2-item menu `<output>` block in Step 7 (after the natural language gate note and before the thread check), add two `<check>` blocks for explicit dispatch:
  ```xml
  <check if="developer selects /create or 1">
    <action>Dispatch to momentum-create-story workflow</action>
  </check>
  <check if="developer selects /develop or 2">
    <action>Dispatch to momentum-dev workflow</action>
  </check>
  ```
  These dispatch checks mirror the pattern used in Step 11 thread selection (lines 477+). The natural language gate note must appear before these checks (it already does from Task 1.3).

- [ ] 2.2: Confirm that the existing dispatch pattern for thread selection in Step 11 is unchanged — the new menu dispatch checks in Step 7 are additive and do not touch Step 11 logic.

## Dev Notes

### Root Cause Analysis

The current Step 7 menu (workflow.md lines 370–384) presents 6 items to the developer. Items 3–6 (Review a plan, Run quality validation, Audit spec provenance, Show session threads) are not developer-initiated workflows — they are diagnostic tools and auto-triggered housekeeping that the developer never needs to consciously choose. Presenting them as peer choices to the two real actions creates cognitive noise at the most important moment: the session open.

Architecture Decision 4b (architecture.md line 434) mandates: "The primary menu is reduced to 2 items: `/create` (story/epic) and `/develop` (story/epic)." This story implements that mandate.

### Architecture Compliance

**Session open sequence (architecture.md line 434):**
> "The primary menu is reduced to 2 items: `/create` (story/epic) and `/develop` (story/epic). Session-stats write is deferred until after the menu is displayed — startup rendering does not block on writes."

This story implements the menu reduction. Story 2a.1 implements the deferred stats write. Story 2a.2 implements the epic progress bar. All three are independent changes to Step 7 — the dev agent must apply this story's changes without disturbing the Step 7 changes from 2a.1 and 2a.2 if those are already merged.

**UX-DR1 (UX spec):** "Primary surface shows only the two developer-initiated actions." This story satisfies UX-DR1 for the menu surface.

**UX-DR2 (UX spec):** "Diagnostic tools (validate, plan review, spec provenance) are not presented as peer choices to create and develop." This story removes them from the primary menu. They remain accessible via natural language — the Input Interpretation gate (workflow.md lines 80–89) handles this as-is.

**FR54 (epics.md):** Epic 2a's FR coverage — session-open epic progress bar and 2-item primary menu. The 2-item menu portion is this story's deliverable.

**Input Interpretation gate (workflow.md lines 80–89):** The existing natural language gate already handles arbitrary requests ("run quality validation", "review a plan", "audit spec provenance") without any additional changes. Removing items 3–6 from the menu does not break their accessibility — it only removes the primary-menu advertisement.

**Thread display (Story 2.2, Step 11):** AC3 requires threads to display before the menu. This is already implemented in Step 7 via `<check if="one or more open threads exist"> GOTO step 11`. This story does not change this logic. The dev agent must confirm the thread GOTO check is untouched after applying menu changes.

### File Structure Requirements

**One file modified:**

`skills/momentum/workflow.md` — Step 7 menu output block (lines 366–390). Specifically:
- The `<output>` block inside `<check if="journal.jsonl does not exist OR has zero open threads">` (lines 370–383)
- The `<note>` for natural language gate (line 386) — must remain unchanged
- The `<check if="one or more open threads exist">` block (lines 388–390) — must remain unchanged

No other files modified. The 6-item to 2-item change is localized to the Step 7 output block.

### Testing Requirements

This is a `skill-instruction` story. The implementation is a workflow.md instruction change — use EDD (Eval-Driven Development):

**Before writing any changes, write evals:**

1. **Returning user, no threads — primary menu eval:**
   - Input: `momentum_completions = 3`, `journal.jsonl` absent
   - Expected: Menu displays exactly `/create` and `/develop`. No items 3–6. Both `1` and `/create` dispatch to create-story. Both `2` and `/develop` dispatch to develop-story.
   - Failure mode: Items 3–6 still appear; or `/create` alias not recognized; or dispatch fires wrong workflow.

2. **Returning user, open threads — journal before menu eval:**
   - Input: `momentum_completions = 2`, one open thread in `journal.jsonl`
   - Expected: Step 11 (thread display) fires before menu. Menu appears after thread selection or new-work decision. Menu still shows only 2 items.
   - Failure mode: Thread display duplicated as a menu item; or menu appears before threads.

3. **First-time user — no menu change eval:**
   - Input: `momentum_completions = 0`
   - Expected: Full orientation walkthrough fires (existing Expertise-Adaptive behavior). The 2-item menu may not appear during first walkthrough — this is acceptable. The eval verifies that the first-encounter path is not broken by the menu change.
   - Failure mode: First-time user sees the 2-item menu with no context; or walkthrough is suppressed.

4. **Natural language fallback eval:**
   - Input: returning user types "I want to run quality validation"
   - Expected: Input Interpretation gate fires ("Running quality validation — correct?"). On yes, validation workflow dispatches. The primary menu change does not break natural language access to removed items.
   - Failure mode: Natural language input for item 3–6 workflows fails silently or errors.

**After writing changes, run evals:** Confirm each of the 4 scenarios above before marking done.

**DoD for skill-instruction tasks:**
- [ ] Evals written before implementation begins
- [ ] 2-item menu renders correctly for returning users (no threads)
- [ ] Number aliases (`1`, `2`) and slash commands (`/create`, `/develop`) both dispatch correctly
- [ ] Thread display (Step 11 GOTO) is unchanged — threads still appear before menu
- [ ] Natural language gate note is intact
- [ ] No items 3–6 in the primary menu
- [ ] First-encounter path (momentum_completions == 0) is not broken
- [ ] Evals pass before marking done

### Previous Story Intelligence

No Epic 2a stories have been implemented yet — 2a-1 and 2a-2 are also in `backlog`. This story modifies Step 7 of `skills/momentum/workflow.md`, as do 2a-1 (silent pre-flight) and 2a-2 (epic progress bar). If any of those stories merge before this one, the dev agent must resolve conflicts by applying this story's menu change to the already-updated Step 7, not to the original baseline.

**Safe merge order for Epic 2a:**
- 2a-1, 2a-2, and 2a-3 all touch Step 7. Any merge order is valid — changes are non-overlapping (2a-1 removes narration, 2a-2 adds progress bar before menu, 2a-3 replaces menu items). The dev agent must read the current Step 7 state at implementation time and apply the delta precisely.

**From Stories 2.6/2.9 (Step 7 context):**
- Story 2.9 added the `session_stats.momentum_completions` counter increment to Step 7 (line 354). This counter is the signal this story's 2-item menu condition depends on (`momentum_completions >= 1`). This is already implemented and available.
- Story 2.9 also updated the expertise-adaptive check blocks (lines 345–351). These blocks are above the menu output block and are unchanged by this story.

### Git Intelligence

Recent commits (2026-03-26):
- `bf136b8 docs(epics): add Epic 2a (UX Redesign) and Epic 2b (Epic Orchestrator)` — epics.md now has full 2a spec
- `eeb43f1 feat(skills): add behavioral persistence for declined offers and expertise counter (Story 2.9)` — `momentum_completions` counter is live in workflow.md Step 7

`skills/momentum/workflow.md` Step 7 (lines 339–391) was last modified by Story 2.9. The menu block (lines 366–384) has not changed since Story 2.1 created it. No conflicting in-flight changes expected beyond other Epic 2a stories (2a-1, 2a-2) which may also be in-progress.

### References

- [Source: skills/momentum/workflow.md#Step 7, lines 366–390] — Current 6-item menu block and thread GOTO check (the exact diff target for Task 1 and Task 2)
- [Source: skills/momentum/workflow.md#Input Interpretation, lines 80–89] — Natural language gate (unchanged by this story; handles removed items 3–6)
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4b, line 434] — "Primary menu is reduced to 2 items: /create and /develop" — authoritative design decision
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 2a, line 998] — Epic context and UX-DR coverage
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2a.3, lines 1062–1087] — ACs and user story (ground truth for this story)
- [Source: _bmad-output/implementation-artifacts/2-9-behavioral-persistence-across-sessions.md] — Pattern reference for skill-instruction task structure (EDD approach, DoD format)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write behavioral evals (test inputs → expected outputs) for each AC
2. Run evals against current skill to establish baseline failure (confirm the current 6-item menu fails the 2-item menu eval)
3. Write the implementation
4. Run evals again — all must pass before marking DoD complete

**EDD workflow for this story:**
- Eval 1: Returning user, no threads → 2-item menu renders, number aliases work, correct dispatch
- Eval 2: Returning user, open threads → journal display before menu, no thread duplication in menu
- Eval 3: First-time user (momentum_completions == 0) → orientation path not broken
- Eval 4: Natural language fallback for removed items (validate, plan review, etc.) → Input Interpretation gate fires correctly

**NFR compliance:**
- Voice rules (workflow.md lines 69–78): No generic praise, no step counts, no internal name surfacing. The new menu text ("Everything's in place — let's build something. /create Write a story / /develop Build the next story") follows Impetus's direct, concise voice.
- Terminal width: Menu items must fit within 80-char width (satisfied by 2-item format).
- Symbol vocabulary (workflow.md line 78): No symbols needed in the 2-item menu — `/create` and `/develop` are the affordances. Keep it clean.

**DoD additions for this story's change types:**
- [ ] Evals written before implementation begins (EDD gate)
- [ ] 2-item menu renders correctly for returning users with no threads
- [ ] Number aliases 1 and 2 dispatch identically to /create and /develop
- [ ] Thread display path (Step 11 GOTO) unchanged — threads still precede menu
- [ ] Natural language gate note intact in Step 7
- [ ] Items 3–6 absent from primary menu
- [ ] First-encounter orientation path unaffected
- [ ] All 4 evals pass

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation with no errors.

### Completion Notes List

- EDD applied: 4 evals written before implementation (eval-2item-menu-returning-user-no-threads.md, eval-2item-menu-returning-user-open-threads.md, eval-2item-menu-first-time-user-orientation-unaffected.md, eval-2item-menu-natural-language-fallback.md)
- Baseline confirmed failing: current 6-item menu fails the 2-item menu eval
- Implementation: replaced `<output>` block lines 369-382 in skills/momentum/workflow.md Step 7 with 2-item /create /develop menu
- Added `<note>` for number aliases (1=/create, 2=/develop) immediately after output block
- Natural language gate note (line 382) verified intact and unchanged
- Thread GOTO check (`<check if="one or more open threads exist">`) verified intact and unchanged
- Added two explicit dispatch `<check>` blocks for `/create or 1` and `/develop or 2` after the NL gate note
- Step 11 thread selection dispatch (line 482) verified unchanged
- All 4 evals pass post-implementation
- AVFL: DEFERRED — parallel session orchestrator will run AVFL after all Epic 2a stories merge

### File List

- `skills/momentum/workflow.md` — Modified: Step 7 menu output block replaced (6-item → 2-item), dispatch checks added
- `skills/momentum/evals/eval-2item-menu-returning-user-no-threads.md` — Created: EDD eval 1
- `skills/momentum/evals/eval-2item-menu-returning-user-open-threads.md` — Created: EDD eval 2
- `skills/momentum/evals/eval-2item-menu-first-time-user-orientation-unaffected.md` — Created: EDD eval 3
- `skills/momentum/evals/eval-2item-menu-natural-language-fallback.md` — Created: EDD eval 4
