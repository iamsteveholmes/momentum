# Story 2a.2: Epic Progress Bar at Session Open

Status: in-progress

## Story

As a developer,
I want to see my sprint state at a glance when I open a session,
so that I always know where I am and what's worth doing next without having to ask.

## Acceptance Criteria

1. **Given** sprint-status.yaml exists and has epic entries **When** `/momentum` runs **Then** Impetus reads sprint-status.yaml at session start **And** renders a progress bar showing: last done epic(s) with `✓` prefix, current in-progress epic(s) with `→` prefix and story count, next backlog epic with `◦` prefix **And** the bar appears as the first visible output

2. **Given** multiple in-progress epics exist simultaneously **When** the bar renders **Then** each in-progress epic gets its own `→` line

3. **Given** the developer has `momentum_completions >= 3` **When** the bar renders **Then** it compresses to a single line (done collapsed, current summary, next collapsed) **And** no logo or preamble text appears

4. **Given** sprint-status.yaml does not exist or is unreadable **When** the bar would render **Then** it is silently omitted (graceful degradation — zero output, no error message)

## Tasks / Subtasks

### Task 1: Add epic progress bar rendering logic to Step 7 (AC: #1, #2, #4) — skill-instruction

- [ ] 1.1: In `skills/momentum/workflow.md` Step 7, before the expertise-adaptive orientation check, add a new action block: "Read `_bmad-output/implementation-artifacts/sprint-status.yaml` (project-relative path). If the file does not exist or cannot be read, skip all rendering — silent degradation, no output."
- [ ] 1.2: Add parsing logic: from the `development_status` section, extract all epic entries (keys matching `epic-*` or `epic-N*` pattern). For each epic entry, capture: epic key, status (`done` / `in-progress` / `backlog`). Also for in-progress epics, count how many story entries (keys matching `N-N-*` pattern for that epic number) have status `in-progress` or `ready-for-dev`.
- [ ] 1.3: Add rendering logic for the verbose bar (used when `momentum_completions < 3`):
  - For each `done` epic (most recent first): `  ✓  {{epic-label}}`
  - For each `in-progress` epic: `  →  {{epic-label}}   {{N}} stories active`
  - For the first `backlog` epic: `  ◦  {{epic-label}}`
  - Epic label = epic key with dashes replaced by spaces, title-cased (e.g., `epic-2a` → `Epic 2a`)
  - Render all done epics, all in-progress epics, and one backlog epic. No ellipsis or counts.
- [ ] 1.4: Add a blank line after the bar, before the rest of Step 7 output (journal display or menu).
- [ ] 1.5: Verify no narration precedes the bar — it must be the first visible output. No "Reading sprint status…" or "Here's your progress:" preamble.

### Task 2: Add compressed bar variant for experienced users (AC: #3) — skill-instruction

- [ ] 2.1: Add a `<check if="session_stats.momentum_completions >= 3">` block wrapping the bar rendering. When true, render the compressed single-line variant:
  - `  ✓ {{done_count}} done  ·  → {{in-progress_epic_labels}}  ·  ◦ next: {{first_backlog_epic_label}}`
  - Example: `  ✓ 2 done  ·  → Epic 2a, Epic 3  ·  ◦ next: Epic 4`
  - No logo, no preamble, no blank line before it
- [ ] 2.2: When false (first-time / early user, `momentum_completions < 3`), use the verbose multi-line bar from Task 1.
- [ ] 2.3: In both cases, after the bar, continue to the existing Step 7 logic (expertise-adaptive orientation, journal read, menu display). The bar is purely additive — it does not replace existing Step 7 logic.

### Task 3: Handle `done-incomplete` epics in bar rendering (AC: #1) — skill-instruction

- [ ] 3.1: Epic status `done-incomplete` (force-closed epics) should render the same as `done` in the bar — `✓` prefix. These epics are complete from an accounting perspective even if not all stories finished.
- [ ] 3.2: Epic status entries that are not one of `done`, `done-incomplete`, `in-progress`, or `backlog` should be treated as `backlog` for rendering purposes (forward-compatible default).

## Dev Notes

### Root Cause / Design Context

The current session-open experience (Step 7 of `skills/momentum/workflow.md`) jumps directly to the expertise-adaptive orientation check and then either shows open threads or the 6-item menu. There is no visual signal of sprint progress — the developer cannot tell at a glance what epic they're in, what's done, or what's next.

Epic 2a corrects this: the progress bar replaces the implicit context assumption with an explicit, scannable orientation surface. The bar reads from `sprint-status.yaml` (the live source of truth for sprint state) rather than from the journal (which tracks workflow threads, not sprint progress). This is the correct data source separation: sprint state in sprint-status.yaml, session thread state in journal.jsonl.

This story implements only the bar rendering and graceful degradation. The 2-item menu redesign is Story 2a.3. The silent pre-flight voice rules (no narration of step transitions) are Story 2a.1. These stories are independent — 2a.2 can be implemented without 2a.1 being complete, since it only adds new output rather than removing existing narration.

### Architecture Compliance

**Session orientation contract (Architecture Decision 4b, updated 2026-03-26):**
> "At session start, Impetus reads `sprint-status.yaml` and renders an epic progress bar (done/current/next) before presenting the primary menu. The primary menu is reduced to 2 items: `/create` (story/epic) and `/develop` (story/epic). Session-stats write is deferred until after the menu is displayed — startup rendering does not block on writes."

This story implements the progress bar portion. The primary menu reduction is Story 2a.3.

**Sprint status file location:**
- Path: `_bmad-output/implementation-artifacts/sprint-status.yaml` (project-relative — relative to the project root where `/momentum` is invoked, not `${CLAUDE_SKILL_DIR}`)
- This file is the BMAD sprint tracking file, already read by momentum-create-story and momentum-dev skills
- Epic entry format in `development_status`: `epic-N: <status>` and `epic-Xa: <status>` (e.g., `epic-2a: in-progress`)

**Visual progress symbol vocabulary (Architecture Decision 4a, UX spec):**
- `✓` = completed/done
- `→` = current/in-progress
- `◦` = upcoming/next

These are the canonical Impetus symbols. The bar must use exactly these symbols — no ASCII alternatives.

**Expertise-adaptive threshold (Story 2.9 established):**
- `momentum_completions` counter lives in `.claude/momentum/installed.json` under `session_stats`
- Already read in Step 7 (line 344 current workflow.md)
- Use the already-loaded value — do not read `installed.json` a second time

**Silent pre-flight (Epic 2a intent):**
- The bar must appear without any narration of its own generation
- Wrong: `"Reading your sprint status..."` then bar
- Right: bar immediately, no preamble

**Graceful degradation:**
- sprint-status.yaml may not exist (first-time project, before sprint planning)
- Must produce zero output and no error — the bar is additive, never required
- Impetus voice rule: never surface backstage machinery; a missing file is not surfaced to the developer

### File Structure Requirements

**Single file modified:** `skills/momentum/workflow.md`

**Insertion point:** Step 7, immediately BEFORE the expertise-adaptive orientation check (currently line 343 in the current file, the `<!-- Expertise-adaptive orientation -->` comment). The bar rendering block goes first in Step 7, before all existing logic.

**Current Step 7 structure (lines 339–391):**
```
Step 7
  action: Load practice-overview.md
  action: Read journal.jsonl
  [NEW] epic progress bar block here ← insertion point
  check: momentum_completions == 0 → full orientation
  check: momentum_completions >= 1 → abbreviated
  action: Increment session_stats
  action: Configuration gap detection
  check: no open threads → show menu
  check: open threads → GOTO Step 11
```

**The bar block does not replace any existing logic.** It adds new output before the orientation check. Step 7's existing flow (orientation, counter increment, gap detection, journal/menu dispatch) is unchanged.

**workflow.md token budget:**
- Current: 764 lines
- This story adds ~15–25 lines of workflow XML
- NFR3 budget: SKILL.md under 500 lines; workflow.md is referenced by SKILL.md and itself should stay reasonably sized. 764 + 25 = ~790 lines — within acceptable range. If the file is approaching 800+ lines, alert the implementer to consider extracting the bar rendering logic to a `references/epic-progress-bar.md` helper file.

### Testing Requirements

This is a `skill-instruction` story. Use EDD (Eval-Driven Development):

**Suggested evals (write before implementing):**

- `eval-progress-bar-basic.md` — Given sprint-status.yaml with Epic 1 (done), Epic 2 (in-progress, 3 stories ready-for-dev), Epic 3 (backlog), and `momentum_completions: 1`, when `/momentum` runs, Impetus should render the verbose multi-line bar as first output, showing `✓ Epic 1`, `→ Epic 2`, `◦ Epic 3` before any journal display or menu.

- `eval-progress-bar-compressed.md` — Given the same sprint-status.yaml and `momentum_completions: 5`, when `/momentum` runs, Impetus should render the single-line compressed bar (done count · in-progress labels · next epic label) instead of the verbose bar, with no logo or preamble.

- `eval-progress-bar-graceful-degradation.md` — Given sprint-status.yaml does not exist in the project, when `/momentum` runs, Impetus should produce zero output related to the progress bar — the session menu or journal display appears as if the bar feature does not exist.

**EDD cycle:**
1. Write evals in `skills/momentum/evals/` (create directory if it doesn't exist)
2. Implement workflow.md changes
3. Run each eval by spawning a subagent with the eval scenario + workflow.md + sprint-status.yaml context
4. All 3 evals pass → Task complete
5. Any eval fails → diagnose gap in instructions, revise, re-run (max 3 cycles)

**NFR compliance check (mandatory):**
- SKILL.md description ≤150 characters: verify after implementation (description is on SKILL.md, not workflow.md — check it hasn't changed)
- `model:` and `effort:` frontmatter present on SKILL.md: verify unchanged
- workflow.md line count: report final count in Dev Agent Record

### Previous Story Intelligence

**From Story 2.9 (most recent done story touching workflow.md):**
- Story 2.9 established the pattern for adding behavioral blocks to Step 7: use XML `<action>` and `<check>` elements consistent with existing step structure
- The `session_stats.momentum_completions` counter is now a concrete data signal (not aspirational) — the bar can rely on it
- Pattern: always add new blocks before existing checks, not interleaved — placement matters for reading comprehension of the workflow XML

**From Story 2.8 (voice/personality — also done):**
- "Everything's in place — let's build something." is the current zero-thread menu opener (Step 7, line 371)
- The bar must appear BEFORE this line — the bar is the first visible output, the menu text comes after
- Story 2a.3 will redesign the menu text. This story must not modify that text — even if it seems natural to update it here.

**From Story 2.6 (step merge pattern):**
- Story 2.6 merged what were formerly Steps 11+12. Verify current step numbering before referencing any line numbers — the workflow.md structure may differ from what earlier stories reference.

**From Story 2.10 (background agent coordination — done):**
- No cmux dependency for this story — no terminal multiplexer needed
- The progress bar is rendered synchronously in the main Impetus workflow, not via a background agent

### Git Intelligence

Recent commits touching `skills/momentum/workflow.md`:
- `feat(skills): add behavioral persistence for declined offers and expertise counter (Story 2.9)` — last modification
- `feat(skills): add Impetus personality, identity, and voice to greeting templates (Story 2.8)` — before that

The workflow.md file was last modified in Story 2.9. No conflicts expected with in-progress stories (Stories 2.2–2.5 are in `review` status — their branches are separate and workflow.md edits within those branches are not active conflicts).

Before implementing, read the actual current state of workflow.md Step 7 (line 339 onward) to confirm the exact insertion point — do not rely on line numbers from this story file, as merges may have shifted them.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 2a.2, lines 1033–1059] — Story ACs (primary spec)
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 2a, lines 998–1004] — Epic context and FR/UX-DR mapping
- [Source: _bmad-output/planning-artifacts/epics.md#FR Coverage Map, line 311] — FR54: Session-open epic progress bar
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4b] — Session orientation contract (updated 2026-03-26 with progress bar)
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4a] — Visual progress symbol vocabulary
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1d] — Installed state JSON (session_stats location)
- [Source: skills/momentum/workflow.md#Step 7, lines 339–391] — Insertion target (read current file before editing)
- [Source: skills/momentum/workflow.md#Expertise-Adaptive Orientation, lines 61–67] — The `momentum_completions` threshold pattern
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml] — Data source for bar (epic statuses, story counts)
- [Source: _bmad-output/implementation-artifacts/2-9-behavioral-persistence-across-sessions.md#Dev Notes] — session_stats counter schema and Step 7 insertion pattern
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Progress Indicator, line 810] — UX component pattern (✓/→/◦ symbol usage)
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Emotional Design Principles, line 193] — "Orient before the user asks"

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Workflow instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the workflow:**
1. Write 3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - `eval-progress-bar-basic.md`
   - `eval-progress-bar-compressed.md`
   - `eval-progress-bar-graceful-degradation.md`
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and output shape, not exact text

**Then implement:**
2. Modify `skills/momentum/workflow.md` Step 7 per Tasks 1–3 above

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — verify it hasn't changed after modifying workflow.md
- `model:` and `effort:` frontmatter fields must be present on SKILL.md — verify after edit
- workflow.md body: report line count in Dev Agent Record; if >800 lines, extract bar rendering to `references/epic-progress-bar.md`
- Skill name `momentum` already compliant (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct on SKILL.md
- [ ] workflow.md final line count documented in Dev Agent Record
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
