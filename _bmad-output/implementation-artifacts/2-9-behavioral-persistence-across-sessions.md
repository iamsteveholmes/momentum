# Story 2.9: Behavioral Persistence Across Sessions for Offers and Expertise

Status: ready-for-dev

## Story

As a developer using Momentum,
I want proactive offer declinations and invocation history to persist across sessions,
so that Impetus does not re-surface offers I already declined and delivers appropriately abbreviated orientation on repeat encounters.

## Acceptance Criteria

1. **Given** the developer explicitly declines a proactive offer (e.g., dormant thread closure), **When** the declination occurs, **Then** a journal entry is appended recording: what was offered, that it was declined, and the context at time of decline
2. **Given** a previously declined offer exists in the journal, **When** Impetus runs hygiene checks on the next session, **Then** the same offer is not re-surfaced unless context has materially changed (spec updated, story changed, new workflow aspect)
3. **Given** the developer has invoked `/momentum` in a prior session, **When** Impetus starts, **Then** a persistent counter of prior `/momentum` completions is available (in `installed.json` or journal metadata)
4. **Given** the expertise counter shows ≥1 prior completion, **When** Impetus delivers session orientation, **Then** orientation is abbreviated per UX-DR20 — current state and decision points, skipping explanatory walkthrough

## Tasks / Subtasks

### Task 1: Extend journal schema with `declined_offers` field (AC: #1, #2) — config-structure

- [ ] 1.1: Add a `declined_offers` field to the journal schema reference (`skills/momentum/references/journal-schema.md`). Define it as an optional array of offer objects on thread entries. Each offer object contains:
  - `offer_type` (string, required) — category of proactive offer (e.g., `dormant-closure`, `dependency-resolution`, `config-gap`, `unwieldy-triage`)
  - `description` (string, required) — what was offered, in natural language (e.g., "Close dormant thread: Story 4.2 implementation")
  - `declined_at` (string, required) — ISO 8601 timestamp of declination
  - `context_hash` (string, required) — a lightweight context fingerprint that enables "material change" detection. Compose from: `thread_id` + `story_ref` + `phase` + `git hash-object` output of the referenced story spec file (if available, empty string otherwise). Format: concatenated string, not a cryptographic hash — just enough to compare equality across sessions.
- [ ] 1.2: Add a "Declined Offers" section to the journal schema reference documenting write semantics: when a developer explicitly declines a proactive offer, append a new journal entry for the affected thread with the existing thread state fields plus the `declined_offers` array containing the new declination. Previous `declined_offers` from the thread's last entry carry forward (append-only accumulation).
- [ ] 1.3: Add read semantics for declined offers: at hygiene check time, read the current thread state (last entry per `thread_id`), check `declined_offers` array. For each pending hygiene offer, compare `offer_type` + `context_hash` against declined entries. If a match exists, suppress the offer. If `context_hash` differs (context has materially changed), the offer is eligible to resurface.
- [ ] 1.4: Document the "material change" heuristic in the schema reference: context is considered materially changed when any of these differ from the declined entry's `context_hash`: `story_ref` changed, `phase` advanced, or the story spec file's `git hash-object` differs from time of decline. The context_hash comparison is the mechanism — the heuristic defines what goes into the hash.
- [ ] 1.5: Add an example JSONL entry showing a thread with `declined_offers`:
  ```jsonl
  {"thread_id":"T-002","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Declined dormant closure","context_summary":"Story 4.2 implementation — developer declined dormant closure, keeping thread open","last_active":"2026-03-24T10:00:00Z","status":"open","depends_on_thread":null,"declined_offers":[{"offer_type":"dormant-closure","description":"Close dormant thread: Story 4.2 implementation","declined_at":"2026-03-24T10:00:00Z","context_hash":"T-002|4.2|mid-review|2026-03-23"}]}
  ```

### Task 2: Add invocation counter to installed.json schema (AC: #3) — config-structure

- [ ] 2.1: Extend the project-level `installed.json` schema (architecture Decision 5c, File 3) by adding a `session_stats` top-level object. Define it in the journal schema reference (since that file is the schema authority for session-related state) with a cross-reference to `installed.json`. The `session_stats` object contains:
  - `momentum_completions` (integer) — count of `/momentum` sessions that reached the session menu (Step 7). Incremented by Impetus at session start, not session end, since the completion signal matters for expertise detection, not farewell.
  - `first_invocation` (string) — ISO 8601 timestamp of the very first `/momentum` invocation in this project
  - `last_invocation` (string) — ISO 8601 timestamp of the most recent `/momentum` invocation
- [ ] 2.2: Document the write semantics in the schema reference: Impetus reads `installed.json` at session start (already happens in Step 1). After the expertise-adaptive check in Step 7 completes (and before the menu/journal display), Impetus increments `momentum_completions`, updates `last_invocation`, and writes `installed.json`. If `session_stats` is absent, initialize with `momentum_completions: 1`, `first_invocation: <now>`, `last_invocation: <now>`.
- [ ] 2.3: Add the `session_stats` example to the journal schema reference:
  ```json
  {
    "installed_at": "2026-03-22T14:30:00Z",
    "components": {
      "hooks": { "version": "1.0.0" }
    },
    "session_stats": {
      "momentum_completions": 5,
      "first_invocation": "2026-03-22T14:30:00Z",
      "last_invocation": "2026-03-24T10:00:00Z"
    }
  }
  ```

### Task 3: Update No-Re-Offer behavioral pattern in workflow.md (AC: #1, #2) — skill-instruction

- [ ] 3.1: Update the "No-Re-Offer After Decline" behavioral pattern (workflow.md, lines 53-58) to add persistence instructions:
  - After bullet 1 ("Record the declination in journal thread state"), add specific write instructions: "Append a new journal entry for the affected thread. Copy all current thread state fields. Add or extend the `declined_offers` array with a new offer object per the journal schema."
  - After bullet 2 ("Do not re-surface"), add the read instruction: "At hygiene check time, before surfacing any proactive offer, check the thread's `declined_offers` array. If an entry matches the current offer's `offer_type` and `context_hash`, suppress the offer."
  - Add bullet 4: "When context has materially changed (context_hash differs), the declination no longer applies. Re-offer is permitted."
- [ ] 3.2: Update the hygiene checks in the merged step (Step 12 currently, will be Step 11 after Story 2.6 merges Steps 11+12). For each hygiene check (dormant closure at line 413, unwieldy triage at line 432), add a guard clause:
  - Before surfacing the offer: `<check if="no declined_offers entry matches this offer_type + context_hash for this thread">`
  - This ensures declined offers are filtered before rendering, not after

### Task 4: Update Expertise-Adaptive pattern in workflow.md (AC: #3, #4) — skill-instruction

- [ ] 4.1: Update the "Expertise-Adaptive Orientation (UX-DR20)" behavioral pattern (workflow.md, lines 60-66) to use the concrete `session_stats.momentum_completions` counter instead of the vague "Check journal thread history for prior completions":
  - Replace bullet 1: "Read `session_stats.momentum_completions` from `.claude/momentum/installed.json`. If absent or zero, treat as first encounter."
  - Bullet 2 (first encounter) remains: `momentum_completions == 0` → full walkthrough
  - Bullet 3 (repeat encounter) becomes: `momentum_completions >= 1` → abbreviated orientation
- [ ] 4.2: Update Step 7 (session orientation, workflow.md line 339) to use the concrete counter:
  - Replace `<action>Check journal thread history for prior completions of /momentum by this developer</action>` with `<action>Read session_stats.momentum_completions from installed.json (already loaded in Step 1). If absent, treat as 0.</action>`
  - Replace `<check if="first encounter (zero prior completions)">` with `<check if="session_stats.momentum_completions == 0">`
  - Replace `<check if="repeat encounter (one or more prior completions)">` with `<check if="session_stats.momentum_completions >= 1">`
- [ ] 4.3: Add the counter increment to Step 7, after the expertise-adaptive check and before the menu/journal display:
  - `<action>Increment session_stats.momentum_completions in installed.json. Update last_invocation. If session_stats absent, initialize with momentum_completions: 1, first_invocation: now, last_invocation: now. Write installed.json.</action>`

## Dev Notes

### Root Cause Analysis

Two separate persistence gaps:

**F10 (No-Re-Offer):** The "No-Re-Offer After Decline" behavioral pattern (workflow.md lines 53-58) instructs Impetus to "Record the declination in journal thread state" but the journal schema (`skills/momentum/references/journal-schema.md`) has no field for declination tracking. The instruction is aspirational — it describes intent without a concrete data structure. The journal only tracks thread lifecycle state (`open`/`closed`), not offer history. Without a schema-level field, the LLM has nowhere to write the declination, so it exists only in ephemeral conversation context and is lost when the session ends.

**F11 (Expertise-Adaptive):** The "Expertise-Adaptive Orientation (UX-DR20)" pattern (workflow.md lines 60-66) says "Check journal thread history for prior completions of this workflow type" but the journal tracks thread state, not invocation counts. A completed thread closure is not the same as a `/momentum` session completion. The LLM has no reliable cross-session signal to distinguish first-time from repeat users. The instruction gives the LLM a behavior to exhibit but no concrete data to drive it.

Both findings share the same root pattern: behavioral instructions that reference data that does not exist in the schema.

**Design note — field naming:** The refinement proposal names the new field `offers`. This story uses `declined_offers` instead — the more precise name reflects that we only persist declinations (not all offers), which is the actionable state for the no-re-offer rule. Accepted offers need no tracking.

### Architecture Compliance

**Session Journal (Architecture Decision 1b):**
- Location: `.claude/momentum/journal.jsonl` (append-only JSONL)
- Current state = last entry per `thread_id`
- The `declined_offers` extension follows append-only semantics — each new entry carries forward previous declinations plus any new one
- No schema-breaking change: `declined_offers` is optional, absent on existing entries, backward-compatible

**Installed State (Architecture Decision 1d, Decision 5c File 3):**
- Location: `.claude/momentum/installed.json`
- Written by Impetus on first install; updated on each upgrade
- Current schema: `{ installed_at, components: { group: { version } } }`
- `session_stats` is a new top-level key — does not interfere with `installed_at` or `components`
- Written as part of normal `installed.json` update flow (already read at Step 1)

**Proactive Offer Pattern (UX-DR8 equivalent, workflow.md lines 45-51):**
- The no-re-offer rule is a sub-pattern that extends proactive offers with memory
- Declined offers feed back into the offer pattern's decision logic

**Expertise-Adaptive (UX-DR20, UX spec line 216):**
- First encounter: full walkthrough with context
- Subsequent encounters: abbreviated — decision points and what's changed
- The `momentum_completions` counter provides the concrete signal the pattern currently lacks

### File Structure Requirements

**Two files modified:**

1. `skills/momentum/references/journal-schema.md` — Add `declined_offers` field definition, write/read semantics for declinations, example entry. Add `session_stats` documentation with cross-reference to `installed.json`.
2. `skills/momentum/workflow.md` — Update No-Re-Offer pattern (lines 53-58), update Expertise-Adaptive pattern (lines 60-66), update Step 7 expertise check (lines 338-346), add declined-offer guard to hygiene step (lines 401-438, or post-2.6 merged step).

### Testing Requirements

This is a mixed-type story:
- **Tasks 1-2 (config-structure):** Verified by inspection — schema fields are correctly defined, examples are valid JSONL/JSON, write/read semantics are unambiguous
- **Tasks 3-4 (skill-instruction):** Verified by EDD (Eval-Driven Development) — behavioral evals confirm the LLM follows the updated instructions

### Previous Story Intelligence

**From Story 2.6 (direct dependency):**
- Story 2.6 merges Steps 11+12 into a single step, renumbers Step 13 → 12. The hygiene checks this story adds guard clauses to will be in the NEW merged Step 11 after 2.6 completes.
- Pattern: tasks reference current line numbers but note post-2.6 locations. The dev agent must verify actual line numbers at implementation time.
- Story 2.6 established the pattern of adding behavioral rules to workflow steps via `<check>` guards and `<note>` elements.

**From Story 2.5:**
- Expertise-adaptive pattern was added to workflow.md but with no concrete persistence mechanism — this story supplies that mechanism.
- Configuration gap detection pattern provides the model for how Impetus reads state at session start and acts on it.

**From Dogfood Findings:**
- F10 and F11 are both medium-severity behavioral gaps caught in live testing. Both share the same root pattern: behavioral instructions without backing data structures.
- The journal schema extension follows the pattern established by the journal itself: append-only, last-entry-wins, optional fields for backward compatibility.

### Git Intelligence

Story 2.6 (`2-6-session-thread-display-fires-hygiene-checks.md`) is `ready-for-dev` and will modify `skills/momentum/workflow.md` Steps 11-13. This story has a hard dependency on 2.6 — the hygiene step guard clauses (Task 3.2) must target the post-2.6 merged step. The dev agent should verify the step structure after 2.6 is merged before implementing Task 3.2.

`skills/momentum/references/journal-schema.md` has not been modified since its creation (Story 1.9). No conflicting changes expected.

### References

- [Source: skills/momentum/references/journal-schema.md, lines 1-71] — Current journal schema (no declination tracking, no invocation counter)
- [Source: skills/momentum/workflow.md#No-Re-Offer After Decline, lines 53-58] — Current no-re-offer pattern (aspirational, no persistence)
- [Source: skills/momentum/workflow.md#Expertise-Adaptive Orientation, lines 60-66] — Current expertise-adaptive pattern (no concrete counter)
- [Source: skills/momentum/workflow.md#Step 7, lines 334-381] — Session orientation step with expertise check
- [Source: skills/momentum/workflow.md#Step 12, lines 401-448] — Hygiene checks (pre-2.6; will be merged into Step 11 by Story 2.6)
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1b, line 224] — Session journal JSONL architecture
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1d, line 246] — Installed state JSON architecture
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 5c, line 474] — Installation & upgrade manifest (installed.json schema)
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX-DR20, line 216] — Expertise-adaptive orientation design rule
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Proactive Intervention Threshold, line 1047] — Proactive offer floor rules
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F10, lines 157-167] — No-re-offer not persisted finding
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F11, lines 171-181] — Expertise-adaptive not differentiated finding
- [Source: _bmad-output/implementation-artifacts/epic-2-refinement-proposal.md#Story 2.9, lines 148-167] — Story proposal with ACs and verification plan
- [Source: _bmad-output/implementation-artifacts/2-6-session-thread-display-fires-hygiene-checks.md] — Dependency story (step merge pattern)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → config-structure (inspection)
- Tasks 3, 4 → skill-instruction (EDD)

---

### config-structure Tasks: Inspection-Based Verification

**Tasks 1 and 2 modify schema reference files**, not executable code. Verification is by inspection:

1. **Schema validity:** Each new field has a type, required/optional designation, and description
2. **Example validity:** Example JSONL/JSON entries parse correctly and include the new fields
3. **Write semantics clarity:** Instructions for when and how to write the new fields are unambiguous — an LLM reading the schema should know exactly what to write and when
4. **Read semantics clarity:** Instructions for how to read and interpret the new fields at session start are unambiguous
5. **Backward compatibility:** Existing journal entries without `declined_offers` continue to work (field is optional). Existing `installed.json` without `session_stats` continues to work (field is optional with default behavior documented)

**DoD for config-structure tasks:**
- [ ] New fields defined with type, required/optional, description
- [ ] Example entries included and valid
- [ ] Write and read semantics documented
- [ ] Backward compatibility confirmed (optional fields, no breaking changes)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-declined-offer-not-resurfaced.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Suggested evals:**
- `eval-declined-offer-not-resurfaced.md` — Given a journal with a thread whose `declined_offers` contains a dormant-closure entry with matching `context_hash`, when Impetus runs hygiene checks and the thread is still dormant, Impetus should NOT offer dormant closure for that thread.
- `eval-declined-offer-resurfaced-on-context-change.md` — Given a journal with a declined dormant-closure entry where the `context_hash` no longer matches current context (phase has advanced), when Impetus runs hygiene checks and the thread is still dormant, Impetus SHOULD re-offer dormant closure.
- `eval-repeat-invocation-abbreviated-orientation.md` — Given an `installed.json` with `session_stats.momentum_completions >= 1`, when Impetus reaches Step 7, Impetus should deliver abbreviated orientation (current state and decision points) without the full explanatory walkthrough.

**Then implement:**
2. Write/modify the workflow.md behavioral patterns and step instructions (Tasks 3, 4)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance note:** This story modifies `workflow.md` and `journal-schema.md`, not SKILL.md. Verify the existing SKILL.md remains compliant after changes if the overall line count of the skill package shifts.

**Additional DoD items for this story (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically)

---

### Verification (post-AVFL)

Adversarial subagent verification via cmux (Workspace D — isolated from other story verifications).

**Setup:**
1. `cmux new-workspace` → create isolated verification workspace
2. `cmux send --surface <X> "cd ~/projects/nornspun && npx skills update"` → pull latest momentum
3. Set up journal.jsonl with a dormant thread (>3d) to trigger a proactive offer
4. `cmux send --surface <X> "claude"` → launch Claude Code

**Test sequence (multi-session):**
1. Session 1: `cmux send` → `/momentum`
2. `cmux read-screen` → confirm proactive offer appears (dormant thread closure)
3. `cmux send` → decline the offer ("N")
4. `cmux send` → exit Claude Code (`/exit` or Ctrl+C)
5. Verify: `cat ~/projects/nornspun/.claude/momentum/journal.jsonl` — **Assert:** `declined_offers` entry present
6. Verify: `cat ~/projects/nornspun/.claude/momentum/installed.json` — **Assert:** `session_stats.momentum_completions` ≥ 1
7. Session 2: `cmux send --surface <X> "claude"` → relaunch Claude Code
8. `cmux send` → `/momentum`
9. `cmux read-screen` → **Assert:** declined offer NOT re-surfaced (same context)
10. `cmux read-screen` → **Assert:** orientation is abbreviated (repeat user — decision points, not full walkthrough)
11. **Edge case:** Advance story phase in journal, re-run `/momentum`, verify offer CAN re-surface (context changed)
12. **Adversarial:** Try to trigger re-offer with same context, try to get full walkthrough on repeat session — both should fail

## Dev Agent Record

### Agent Model Used

### Completion Notes List

### File List
