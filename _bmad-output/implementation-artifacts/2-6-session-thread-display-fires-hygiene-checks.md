# Story 2.6: Session Thread Display Fires Hygiene Checks Before Developer Input

Status: ready-for-dev

## Story

As a developer using Momentum,
I want the session journal display to render hygiene checks (concurrent detection, dormant closure, dependency notification, unwieldy triage) in the same response as the thread list,
so that I see all warnings and offers before being asked for thread selection, and internal identifiers like T-NNN are never visible.

## Acceptance Criteria

1. **Given** open threads exist in journal.jsonl, **When** Impetus displays the session journal, **Then** thread list, hygiene warnings (concurrent/dormant/dependency/unwieldy), and selection prompt all appear in ONE response before developer input
2. **Given** any thread was active within the last 30 minutes, **When** Impetus displays the session journal, **Then** concurrent-work warning appears inline before selection prompt (Story 2.2 AC4)
3. **Given** any thread exceeds the 3-day dormancy threshold, **When** Impetus displays the session journal, **Then** dormant-thread closure offer appears inline before selection prompt (Story 2.2 AC5)
4. **Given** any thread is displayed in output, **Then** identified by `context_summary` or `story_ref` — never by `thread_id` (T-NNN). Internal identifiers do not appear in any user-facing output.

## Tasks / Subtasks

- [ ] Task 1: Merge Steps 11 and 12 into a single step (AC: #1)
  - [ ] 1.1: Remove the interactive output and `<ask>` from current Step 11 that causes the LLM to wait for input before hygiene
  - [ ] 1.2: Move all hygiene checks (concurrent [Story 2.2 AC4], dormant [Story 2.2 AC5], dependency [Story 2.2 AC6], unwieldy [Story 2.2 AC7]) into the merged step, positioned AFTER thread list display but BEFORE the selection prompt
  - [ ] 1.3: Place the selection prompt ("Continue (1/2/...) or tell me what you need?") as the FINAL element of the merged step, after all hygiene warnings have been rendered
  - [ ] 1.4: Ensure the merged step renders threads + conditional hygiene warnings + selection prompt within a single LLM response turn (one merged step, no interactive pause between display and hygiene). Preserve the individual `<check if="..."><output>` blocks for each hygiene condition — they remain conditional.
  - [ ] 1.5: Renumber subsequent steps (Step 13 → Step 12, etc.) and update all GOTO references throughout workflow.md
- [ ] Task 2: Enforce voice rule prohibiting thread_id in user-facing output (AC: #4)
  - [ ] 2.1: Add an explicit behavioral rule in the merged step (or reinforce in Voice Rules section): "When referencing any thread in output, use the thread's `context_summary` or `story_ref` value — never the `thread_id` key or its T-NNN value. This is a non-negotiable voice rule."
  - [ ] 2.2: Search all `<output>` blocks in Steps 11-13 (and the merged result) for any direct `thread_id` references — expect to find none in templates (the dogfood F6 issue was behavioral, not template-driven), but verify for completeness
  - [ ] 2.3: In the merged step's thread list output template, confirm threads are displayed using `context_summary_short` (already the case — verify, don't rewrite)
  - [ ] 2.4: In Step 13 (workflow resumability, now renumbered), confirm output uses `context_summary` / `story_ref` (already the case — verify, don't rewrite)
  - [ ] 2.5: Verify the voice rule addition is placed where the LLM will encounter it before rendering the thread display — either in the step's `<note>` or in the BEHAVIORAL PATTERNS section
- [ ] Task 3: Verify GOTO chain integrity after renumbering (AC: #1)
  - [ ] 3.1: Audit all `GOTO step N` references in workflow.md for correct targets after renumbering
  - [ ] 3.2: Verify no step references point to the old Step 12 number

## Dev Notes

### Root Cause Analysis

The critical defect is in the step split architecture:
- **Step 11** (line 385, `skills/momentum/workflow.md`): Displays threads, outputs an interactive question "Continue (1/2/...) or tell me what you need?", then has `<action>GOTO step 12 (thread hygiene checks)</action>`
- **Step 12** (line 401): Contains ALL hygiene checks — concurrent detection, dormant closure, dependency notification, unwieldy triage
- **Problem**: The LLM renders Step 11's output with the interactive question and naturally waits for developer input. The GOTO to Step 12 never executes because the conversation pauses at the question. This is a fundamental architectural issue with XML workflow execution in LLM context — any step that contains both an interactive output AND a GOTO will have the GOTO ignored.

### Architecture Compliance

**Session Journal (Architecture Decision 1b):**
- Location: `.claude/momentum/journal.jsonl` (append-only JSONL)
- Current state = last entry per `thread_id`
- View file: `.claude/momentum/journal-view.md` (regenerated after every append)
- Concurrency: POSIX atomic append, safe for multi-tab

**Thread Hygiene Thresholds (implemented in workflow.md Step 12, lines 403-438; design intent in UX spec lines 453-462):**
- Concurrent detection: `last_active` within 30 minutes (workflow.md line 403)
- Dormant threshold: 3 days inactive (workflow.md line 413)
- Unwieldy triage: >5 open threads (workflow.md line 432)
- Closure pattern: one confirmation, not ceremony (UX spec line 781)

**Voice Rules (workflow.md, lines 68-77):**
- Never surface internal names: model names, agent names, tool names, or backstage machinery
- Thread display must use `context_summary` or `story_ref`, never `thread_id` (T-NNN)
- Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? question — always paired with text

**Response Architecture Pattern (UX-DR15):**
- Orientation line → Substantive content → Transition signal → User control (always final element)
- The merged step must follow this pattern: orientation (journal state) → threads + warnings → transition → selection prompt

### File Structure Requirements

**Single file modified:** `skills/momentum/workflow.md`

The changes are confined to Steps 11, 12, and 13 (lines 385-470). After the merge:
- Old Step 11 + Old Step 12 → New Step 11 (merged)
- Old Step 13 (workflow resumability) → New Step 12
- All subsequent steps renumber accordingly
- All GOTO references updated

### Testing Requirements

This is a `skill-instruction` change — use EDD (Eval-Driven Development), not TDD. See Momentum Implementation Guide below.

### Previous Story Intelligence

**From Story 2.5 (most recent in Epic 2):**
- Pattern: Evals go in `skills/momentum/evals/` (established by Story 2.3)
- Journal integration: Story 2.2 established journal read at session start; gap detection (2.5) integrates in same orientation phase — no duplication
- Anti-pattern: "Step N/M regression" — never use step counts in orientation, always narrative
- Voice rules: All output must synthesize in Impetus voice, never raw JSON or internal identifiers

**From Dogfood Findings:**
- F7 (dormant hygiene) and F8 (concurrent detection) are both symptoms of F9 (step split). Fixing the merge fixes all three.
- F6 (thread ID visible) is a behavioral issue — the LLM used journal `thread_id` field values directly instead of `context_summary`. The output templates already use `context_summary_short`, but the LLM needs an explicit voice rule reinforcement to prevent substituting internal IDs. Fix by adding a behavioral rule in the merged step.

### Git Intelligence

Recent commits show dogfood validation work (ee40034 through 8b9dc49) documenting the exact failures. The workflow.md hasn't been modified since the Epic 2 story merges (commit 2c40cc7). No conflicting changes expected.

### References

- [Source: skills/momentum/workflow.md#Step 11, lines 385-399] — Current broken step (thread display with premature interactive output)
- [Source: skills/momentum/workflow.md#Step 12, lines 401-448] — Hygiene checks that never execute
- [Source: skills/momentum/workflow.md#Step 13, lines 450-470] — Workflow resumability (to be renumbered)
- [Source: skills/momentum/workflow.md#Voice Rules, lines 68-77] — No visible machinery
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1b] — Session journal JSONL architecture
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Multi-Thread Work Model, lines 427-464] — Thread hygiene design
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Response Architecture Pattern, lines 341-346] — Response structure
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F9, lines 143-152] — Root cause analysis
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F6, lines 107-115] — Thread ID machinery finding
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F7, lines 119-127] — Dormant hygiene finding
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F8, lines 131-139] — Concurrent detection finding

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-hygiene-fires-before-selection.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md steps (merge Steps 11+12, add voice rule for thread_id prohibition, fix GOTO chain)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance note:** This story modifies only `workflow.md`, not SKILL.md. The standard SKILL.md NFR checks (description ≤150 chars, model/effort frontmatter, body ≤500 lines) do not apply. Verify the existing SKILL.md remains compliant after workflow changes if the overall line count of the skill package shifts.

**Additional DoD items for this story (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically)

---

### Verification (post-AVFL)

Adversarial subagent verification via cmux (Workspace A — isolated from other story verifications).

**Setup:**
1. `cmux new-workspace` → create isolated verification workspace
2. Write test journal.jsonl in `~/projects/nornspun/.claude/momentum/` with:
   - Thread 1: `last_active` = 30 seconds ago (triggers concurrent detection)
   - Thread 2: `last_active` = 5 days ago (triggers dormant closure)
   - Thread 3: normal active thread
3. `cmux send --surface <X> "cd ~/projects/nornspun && npx skills update"` → pull latest momentum
4. `cmux send --surface <X> "claude"` → launch Claude Code

**Test sequence:**
1. `cmux send` → `/momentum`
2. `cmux read-screen --lines 80` → capture session journal display
3. **Assert:** All hygiene warnings (concurrent, dormant) appear BEFORE "Continue (1/2/...) or tell me what you need?"
4. **Assert:** No T-NNN identifiers visible — threads shown by `context_summary`
5. **Adversarial:** Verify the old failure mode (Step 11 pause before hygiene) is gone — all warnings render without user input needed

## Dev Agent Record

### Agent Model Used

### Completion Notes List

### File List
