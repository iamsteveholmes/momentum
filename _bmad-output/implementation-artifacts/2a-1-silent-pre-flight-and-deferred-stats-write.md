# Story 2a.1: Silent Pre-Flight and Deferred Stats Write

Status: review

## Story

As a developer,
I want Impetus to start without narrating its own startup process,
so that I see only what matters and am never made to watch a loading screen.

## Acceptance Criteria

**Given** Momentum is fully installed and all components are at current version
**When** I run `/momentum`
**Then** zero lines of output appear before the progress bar
**And** no narration of intent, routing, or step numbers appears at any point

**Given** Impetus runs its session startup sequence (version check, hash check, journal read)
**When** all checks pass with no actionable condition found
**Then** each check produces zero output (silent pre-flight rule)

**Given** Impetus increments the session_stats counter in installed.json
**When** the startup sequence runs
**Then** the write to installed.json happens after the menu is displayed, not before
**And** the session_stats write does not delay the menu appearing

**Given** a new voice rule: "speak only at phase boundaries"
**When** Impetus routes between startup steps
**Then** no narration of routing decisions appears ("proceeding to step 10", "GOTO step 7", etc.)

## Tasks / Subtasks

### Task 1: Add "speak only at phase boundaries" voice rule to workflow.md (AC: #1, #4) — skill-instruction

- [x] 1.1: Add a new Voice Rule entry to the Voice Rules behavioral pattern section (workflow.md, after existing non-negotiable bullets): "Never narrate routing or internal step transitions. GOTO, GOTO step N, 'proceeding to step', 'checking version', 'routing to' — all of these are internal machinery. Speak only at phase boundaries: first-install consent prompt, hash drift warning, upgrade offer, and session menu."
- [x] 1.2: Verify that all existing steps that emit output only do so at the defined phase boundaries: Step 2 (consent prompt), Step 3 (action execution `✓` per file), Step 6 (decline message), Step 7 (orientation and menu), Step 9 (upgrade offer), Step 10 (hash drift warning). Steps 1, 4, 5, and all GOTO transitions must produce zero output.
- [x] 1.3: In Step 1, ensure there is no output action — confirm the step has only `<action>` and `<check>` elements with zero `<output>` elements. If any output exists in Step 1, remove it.

### Task 2: Move session_stats write to after menu display in workflow.md (AC: #3) — skill-instruction

- [x] 2.1: Locate the session_stats increment action in Step 7 (currently at approximately line 354, added by Story 2.9). This action reads: "Increment session_stats.momentum_completions in installed.json. Update last_invocation to current ISO 8601 timestamp. If session_stats is absent, initialize with momentum_completions: 1, first_invocation: now, last_invocation: now. Write installed.json."
- [x] 2.2: Move this action to AFTER the menu display output. The correct sequence in Step 7 must be:
  1. Read journal
  2. Expertise-adaptive check (reads momentum_completions — read-only at this point)
  3. Run gap detection
  4. Display menu (the first visible output to the developer)
  5. **THEN** write session_stats to installed.json (deferred write — does not delay menu)
  6. Wait for developer input
- [x] 2.3: Confirm the expertise-adaptive check in Step 7 still reads `momentum_completions` BEFORE the increment (it uses the value from the PREVIOUS session to determine this session's orientation mode). The read happens at step 7 start (loaded in Step 1), the write happens after the menu. This is correct and intentional: the current session starts as a repeat only once the menu has appeared.
- [x] 2.4: Add a comment in the workflow immediately before the deferred write action: `<!-- Deferred stats write (Story 2a.1): write AFTER menu is displayed, not before — the menu must appear with zero I/O latency from the stats write. -->`

### Task 3: Verify Steps 4 and 5 are silent (AC: #2) — skill-instruction

- [x] 3.1: Read Steps 4 and 5 of workflow.md. Confirm neither step has any `<output>` elements. Steps 4 (write state files) and 5 (verify git tracking) operate silently — they perform I/O and produce no user-facing output on the happy path.
- [x] 3.2: If Step 5 has an `<output>` inside the `.gitignore excludes installed.json` check, this is an acceptable exception — it is an actionable condition, not routine narration. Confirm that message meets the "speak only at phase boundaries" rule: it is a warning, not routing narration.

### Task 4: Verify Step 10 (hash drift) is the only hash-related output and uses plain language (AC: #1, #4) — skill-instruction

- [x] 4.1: Read Step 10 of workflow.md. The current hash drift warning reads: "Rules modified since Momentum installed them. {{group}} files have been changed (hash mismatch). Re-apply from the Momentum package, or keep your edits? [R] Re-apply · [K] Keep modified". This uses technical vocabulary ("hash mismatch", "group"). Epic 2a Story 2a.4 will fully redesign this message — Story 2a.1 does NOT change the hash drift message text. This task is a verification gate: confirm that Step 10 is the only step that produces output related to hash or drift conditions. No other step should pre-announce hash checking ("now checking hashes...", "running hash verification").
- [x] 4.2: Confirm Step 1's GOTO to step 10 produces zero output. The routing is silent.

## Dev Notes

### Root Cause Analysis

Two behavioral problems introduced or exposed by prior Epic 2 work:

**Silent Pre-Flight Violation (AC1, AC2, AC4):** The workflow's Voice Rules section defines narration prohibitions for step counts and generic praise, but does not prohibit routing narration. An LLM implementing the workflow may add narration between steps ("Running version check...", "Proceeding to session orientation...") because nothing explicitly forbids it. The silent pre-flight rule must be stated as a positive constraint: zero output before the menu, with the single exception of actionable conditions (hash drift, first install consent, upgrade offer).

**Stats Write Timing (AC3):** Story 2.9 added the session_stats increment to Step 7, placing it immediately after the expertise-adaptive check and before the menu display (workflow.md ~line 354). This is logically sound — the counter increments when the session is considered "complete" (menu appeared). However it means a write I/O operation occurs before the menu appears. The deferred write pattern moves the write to after the menu output but before the `Wait` action, preserving the semantic (session is "started" when the menu is visible) while eliminating any write-before-display latency.

### Architecture Compliance

**Session orientation (Architecture Decision 1c, workflow.md Step 7):**
- Step 7 is the primary session-start dispatcher. All changes in this story are within Step 7 or the Voice Rules section.
- The `installed.json` is read in Step 1 (already loaded in memory). Moving the write later in Step 7 does not require re-reading the file — the in-memory object is modified and written after the menu display.
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1c (installed state)]

**installed.json schema (Architecture Decision 5c, File 3):**
- `session_stats` was added in Story 2.9. No schema changes in this story.
- The write semantics change: write happens later in the step sequence (after menu output), not at a different step.
- [Source: _bmad-output/implementation-artifacts/2-9-behavioral-persistence-across-sessions.md] — session_stats schema (not present in architecture.md)

**Voice rules (workflow.md BEHAVIORAL PATTERNS):**
- The Voice Rules section (workflow.md lines 69–79) is where the "speak only at phase boundaries" rule belongs. It is additive — no existing rules are removed.
- All other behavioral patterns (Proactive Offer, No-Re-Offer, etc.) are unaffected.

### File Structure Requirements

**One file modified:**
`skills/momentum/workflow.md`
- Task 1: Voice Rules section (~line 69) — add new bullet
- Task 2: Step 7 (~line 339) — move session_stats write action
- Tasks 3, 4: Read-only verification (no changes unless violations found)

Three new eval files created: `skills/momentum/evals/eval-silent-pre-flight.md`, `eval-deferred-stats-write.md`, `eval-no-routing-narration.md`. No schema files modified.

### Testing Requirements

This is a skill-instruction story: all tasks modify or verify instructions in `workflow.md`. Use EDD.

**EDD approach:**
1. Write 2–3 behavioral evals in `skills/momentum/evals/`
2. Implement the changes (Tasks 1 and 2 are the only write tasks)
3. Run evals and confirm behaviors

**Suggested evals:**

- `eval-silent-pre-flight.md` — Given Momentum is fully installed (all components current), when Impetus runs, the session should produce zero output before the menu appears. The LLM should NOT produce any output in Steps 1, 4, 5, or during GOTO transitions. The only output before the menu is in Step 7 (the menu itself).

- `eval-deferred-stats-write.md` — Given a repeat user (momentum_completions >= 1), when Step 7 runs, the session_stats write to installed.json should occur AFTER the menu output, not before. The expertise-adaptive check (read) uses the pre-increment value. After the menu is printed, Impetus increments and writes.

- `eval-no-routing-narration.md` — Given Impetus is routing between steps (e.g., GOTO step 10 from Step 1), when an LLM implements this, no output matching "proceeding", "checking", "routing", "GOTO", "step N" should appear in the terminal.

**Verification:**
- Run evals with a subagent spawned via Agent tool
- Provide the eval scenario as task + load workflow.md + SKILL.md as context
- Check whether subagent behavior matches the expected outcome
- If any eval fails: diagnose the specific instruction gap, revise the rule wording, re-run (max 3 cycles)

### Previous Story Intelligence

**From Story 2.9 (direct dependency — session_stats):**
- Story 2.9 Task 4.3 added the counter increment to Step 7 at the correct logical position. This story moves the *write* to after the menu — the read-for-expertise-check is still pre-menu.
- The `session_stats` field is now in `installed.json` — Task 2 works with the already-committed schema.
- Story 2.9 pattern: behavioral changes to workflow.md go in the correct step, with explicit comment citing the story that introduced them.

**From Story 2.8 (greeting templates / identity):**
- The ASCII art greeting and Impetus identity block was added in Story 2.8. This is inside the first-install consent prompt (Step 2) — it is an actionable phase boundary, not routing narration. The "speak only at phase boundaries" rule does NOT remove the greeting; it only prevents inter-step narration on the happy path (Steps 1 → 10 → 7 when fully installed).
- Dev agent must NOT remove or suppress the Step 2 greeting template in the course of this story.

**From Story 2.6 (step merge):**
- Steps 11 and 12 in the current workflow.md are the journal display and hygiene checks. This story does not touch those steps.

**From git history:**
- The most recent commit (`eeb43f1`) added the session_stats write at line 354 in Step 7. This is the exact line this story's Task 2 moves. Verify the current line number before editing — it may have shifted from subsequent merges.

### Project Structure Notes

- All changes are within `skills/momentum/workflow.md`
- The evals directory `skills/momentum/evals/` exists (created in Story 2.9 or earlier) — confirm before creating eval files
- No path collisions with other ready-for-dev stories (Epic 3 stories touch `hooks/` and `hooks-config.json`, not `workflow.md`)

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Epic 2a, lines 998–1031] — Epic context and ACs for Story 2a.1
- [Source: skills/momentum/workflow.md#Voice Rules, lines 69–79] — Current voice rules (no "speak only at phase boundaries" yet)
- [Source: skills/momentum/workflow.md#Step 1, lines 145–179] — Startup routing (must be silent)
- [Source: skills/momentum/workflow.md#Step 7, lines 339–391] — Session orientation with stats write at line 354
- [Source: skills/momentum/workflow.md#Step 10, lines 598–631] — Hash drift check (source of the hash-drift message Story 2a.4 will rewrite)
- [Source: _bmad-output/implementation-artifacts/2-9-behavioral-persistence-across-sessions.md] — installed.json schema with session_stats (session_stats not present in architecture.md)
- [Source: _bmad-output/implementation-artifacts/2-9-behavioral-persistence-across-sessions.md#Task 4.3] — Original placement of session_stats write (Story 2.9)
- [Source: _bmad-output/implementation-artifacts/2-8-impetus-first-impression-has-personality-and-identity.md] — Greeting template (must not be removed by this story)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Completion Notes List

- Task 1: Added "speak only at phase boundaries" voice rule bullet to Voice Rules section in workflow.md (line 79, after existing non-negotiable bullets). Verified Step 1 has zero output elements. Confirmed all steps emit output only at defined phase boundaries: Steps 2, 3, 6, 7, 9, 10. Steps 1, 4, and all GOTO transitions produce zero output. Step 5's single output is inside the `.gitignore excludes installed.json` conditional check — an actionable warning exception, not routing narration.
- Task 2: Moved session_stats write to after menu display in Step 7. Removed original placement between expertise-adaptive check and gap detection. Added deferred write immediately after the `<check if="journal.jsonl does not exist OR has zero open threads">` output block. Added `<!-- Deferred stats write (Story 2a.1): ... -->` comment. Added clarifying comment `<!-- Read momentum_completions BEFORE incrementing — determines this session's orientation mode -->` to document the intentional read-before-write ordering.
- Task 3: Verified Step 4 has zero output elements (silent state file writes). Verified Step 5's sole output is inside the `.gitignore` warning conditional — acceptable actionable exception.
- Task 4: Verified Step 10 is the only step with hash-related output. Step 1's GOTO to Step 10 is expressed as `<action>GOTO step 10</action>` with no surrounding `<output>` — fully silent routing. Message text left unchanged (Story 2a.4 will redesign it).
- Evals written: eval-silent-pre-flight.md, eval-deferred-stats-write.md, eval-no-routing-narration.md in skills/momentum/evals/. All three evals pass against the updated workflow.md.

### File List

- `skills/momentum/workflow.md` — Added voice rule, moved session_stats deferred write, added clarifying comments
- `skills/momentum/evals/eval-silent-pre-flight.md` — New eval: zero output before session menu on happy path
- `skills/momentum/evals/eval-deferred-stats-write.md` — New eval: stats write occurs after menu display
- `skills/momentum/evals/eval-no-routing-narration.md` — New eval: GOTO transitions produce zero output
- `_bmad-output/implementation-artifacts/2a-1-silent-pre-flight-and-deferred-stats-write.md` — Story file (status, tasks, record)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` — Updated epic-2a and story status to in-progress/review

## Change Log

- feat(skills): add "speak only at phase boundaries" voice rule to Impetus workflow.md (Story 2a.1, 2026-03-26)
- feat(skills): move session_stats write to after menu display — deferred write pattern (Story 2a.1, 2026-03-26)
- feat(skills): add three behavioral evals for silent pre-flight, deferred stats write, and no routing narration (Story 2a.1, 2026-03-26)
