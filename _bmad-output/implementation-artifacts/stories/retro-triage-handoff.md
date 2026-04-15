---
title: Retro → Triage Handoff — Retro Findings Feed Planning via Unified Intake Queue
story_key: retro-triage-handoff
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on:
  - triage-skill
touches:
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - _bmad-output/planning-artifacts/architecture.md
priority: medium
story_type: practice
feature_slug: momentum-retro-and-flywheel
---

# Retro → Triage Handoff — Retro Findings Feed Planning via Unified Intake Queue

## Story

As a developer closing a sprint,
I want the retro's un-actioned findings — including feature-state transitions and diagnosed failures — to flow automatically into the next sprint's planning as `handoff` events in the unified `intake-queue.jsonl`,
so that retro-surfaced gaps, user-stated complaints, regressed feature states, and named failures are visible as planning candidates without my having to re-inject them by hand.

## Description

The sprint-2026-04-10 planning session started cold against the sprint-2026-04-08 retro. The developer manually injected the three largest known gaps — Material 3 inconsistency, API stub status, iOS coverage — before planning could proceed. The retro and sprint-planning skills share no automated state today: planning's backlog-synthesis reads `stories/index.json` and accepts developer prompts, but does not read prior retro findings, feature-state regressions, or user-stated complaints.

This story closes that loop — but reframed per **DEC-005** (2026-04-14) and channeled through the artifact defined by **DEC-007** (2026-04-14).

### DEC-005 reframing

The pre-DEC-005 framing of this story treated handoff as a narrow "priority action items → planning candidates" pipeline with three explicit buckets (prior-retro findings, cross-platform coverage gaps, user-stated complaints). DEC-005 reshapes it:

- **D8 — Retro as feature-state hygienist.** Retro is responsible for transitioning features through Done / Shelved / Abandoned / Rejected (D6). Handoff items now carry feature-state transition context — e.g., "feature X was asserted Done but retro observed Y behavior regressing it to Partial."
- **D7 — Failure as legitimate diagnostic category.** Retro must name failures specifically — what was attempted, what didn't work, what was learned — alongside successes. Handoff items carry failure-diagnosed framing so planning can decide whether to retry, shelve, or rethink.
- **D1 / D5 — Feature-first, story-type-tagged.** Handoff items that imply new stories carry suggested `feature_slug` (D1) and suggested `story_type` (D5 — feature / maintenance / defect / exploration / practice).
- **D10 — No gap-check at handoff.** Handoff does not itself perform value-floor analysis. It carries context so downstream consumers (triage at session start, sprint-planning at backlog synthesis) can evaluate.

### DEC-007 alignment

Retro writes handoff items as JSONL events to the unified `_bmad-output/implementation-artifacts/intake-queue.jsonl` with `source: "retro"` and `kind: "handoff"`. This replaces:

- The previously-proposed `retro-summary.json` handoff artifact (never built — superseded before build).
- The `triage-inbox.md` contract in `architecture.md` lines ~1671–1698 (never built — retired by DEC-007 before build).

One artifact, one schema, one reader path. Sprint-planning Step 1 Phase A.5 already loads the previous sprint summary; this story adds an adjacent read of open handoff entries. Triage already reads the queue on session start (per Story A — `triage-skill`); this story adds the retro producer side.

### Pain context

HF-01 (2026-04-11T05:31) and HF-03 (2026-04-11T05:36) captured the developer manually injecting retro-surfaced gaps into sprint-2026-04-10 planning because the automated path did not exist. The sprint-2026-04-06 retro surfaced M3 inconsistency as a major user-visible regression; sprint-2026-04-08 retro ran 2026-04-10; sprint-2026-04-10 planning ran the same day; findings did not carry across. This story closes the gap at the artifact and workflow level — not sprint-by-sprint.

### Dependency relationship to Story A (`triage-skill`)

Story A delivers:
- `_bmad-output/implementation-artifacts/intake-queue.jsonl` schema (per DEC-007).
- `momentum-tools` CLI write path for queue events (SHAPING / DEFER / REJECT from triage).
- Triage read path that surfaces open queue entries at session start.

This story (Story B) extends Story A with the **retro producer side**:
- Retro Phase 5 writes `kind: "handoff"` events using Story A's schema and CLI.
- Sprint-planning Phase A.5 extends to read `kind: "handoff"` entries filtered to `status: "open"`.
- Triage's existing queue read path already re-surfaces handoff items — no additional triage work here.

This ordering is hard: without Story A's schema and CLI in place, there is nothing for retro to write through. Do not start this story until `triage-skill` is merged.

## Acceptance Criteria

1. **Retro emits handoff events.** When `momentum:retro` completes Phase 5 (action-item triage), any action item the developer does not immediately distill or stub is recorded as a JSONL event appended to `_bmad-output/implementation-artifacts/intake-queue.jsonl` with `source: "retro"`, `kind: "handoff"`, and `status: "open"`.

2. **Handoff event schema.** Core discriminators per DEC-007: `source`, `kind`. Remaining fields defined by this story. Each retro handoff event carries, at minimum:
   - `id` — unique event id (ULID or timestamped slug, per Story A's schema convention).
   - `source: "retro"` and `kind: "handoff"`.
   - `sprint_slug` — the sprint this handoff originated from (provenance).
   - `title` — short human-readable title.
   - `description` — one-to-three-sentence summary of the finding.
   - `status` — one of `open` | `consumed` | `rejected` (initial write is always `open`).
   - `created_at` — ISO-8601 UTC timestamp.
   - Optional fields (present when applicable):
     - `feature_state_transition` — a record of the form `{ "feature_slug": "...", "prior_state": "...", "observed_state": "...", "evidence": "..." }` when the finding reflects a DEC-005 D8 feature-state change.
     - `failure_diagnosis` — a record of the form `{ "attempted": "...", "didn_t_work": "...", "learned": "..." }` when the finding reflects a DEC-005 D7 diagnosed failure.
     - `suggested_feature_slug` — when the finding implies new feature-bearing work (DEC-005 D1).
     - `suggested_story_type` — one of `feature` | `maintenance` | `defect` | `exploration` | `practice` (DEC-005 D5) when the finding implies new work.
     - `evidence_refs` — array of pointers back to the findings document (e.g., section anchor or line range of `retro-transcript-audit.md`).

3. **Retro does not gate or value-check at handoff.** Per DEC-005 D10, retro performs no value-floor analysis when emitting handoff events. It records context; downstream consumers (triage, sprint-planning) decide.

4. **No manual injection required on the golden path.** When the developer opens a new sprint-planning session after a retro that produced handoff events, planning Phase A.5 surfaces those events as candidate context for backlog synthesis without the developer typing them into the prompt.

5. **Sprint-planning reads handoff events.** `momentum:sprint-planning` Step 1 Phase A.5 gains a read of `intake-queue.jsonl` filtered to `source: "retro"`, `kind: "handoff"`, `status: "open"`. Open handoff entries are included in the "what matters most right now" synthesis context alongside the previous sprint summary.

6. **Planning surfaces handoff items in the recommendation output.** Where Phase C currently lists recommendations and a stale-candidates block, the output gains an additional labeled section — e.g., "Open handoff items from recent retros" — that lists each open handoff entry by title, source sprint, and (if present) its feature-state transition or failure-diagnosis framing. Developer can reference these when selecting stories.

7. **Triage re-surfaces handoff items unchanged.** Triage's existing queue read (delivered by Story A) already surfaces any `status: "open"` entry regardless of `source` or `kind`. This story does not change triage behavior.
   - (a) Testable assertion: when the developer starts a triage session after a retro that produced handoff events, entries with `kind: "handoff"` appear in triage's classification list alongside other open entries — visibly tagged with their age and `kind` — using the same classify / promote / continue-watching / reject flow Story A defines for `kind: "shape"` and `kind: "watch"` entries.
   - (b) Out of scope: any gaps discovered during the Task 4 verification run are addressed in a follow-up story against `triage-skill`, not within this AC. This story does not patch triage workflow behavior.

8. **Consumption updates the entry.** When a handoff item is acted on — promoted to a story via intake, distilled, decided via decision, or explicitly rejected — the corresponding queue entry is updated to `status: "consumed"` (or `"rejected"`) with an outcome reference (e.g., story slug, SDR id). This must use the same CLI update path Story A provides for queue mutation — no direct file edits.

9. **Legacy `triage-inbox.md` contract is retired in architecture.md.** The section at `_bmad-output/planning-artifacts/architecture.md` lines ~1671–1698 is updated to (a) mark the format as superseded, (b) cross-reference DEC-007 and this story, and (c) point to `intake-queue.jsonl` as the replacement artifact. The section is retained as historical context; it is not deleted.

10. **Retro workflow documents the handoff step.** `skills/momentum/skills/retro/workflow.md` Phase 5 is updated so the Tier 1 / Tier 2 routing path explicitly includes a third disposition — "carry forward as handoff event" — with instructions for when to choose it (unaddressed, non-Tier-1, non-stubbed findings that matter to future planning). The update does not delete the existing distill and stub dispositions — it adds the handoff disposition alongside them.

11. **Developer-approval preserved for handoff writes.** Retro does not silently emit handoff events. Phase 5 prompts the developer to confirm which un-actioned findings carry forward as handoff events, same Y/N approval pattern used for stub creation.

## Tasks / Subtasks

- [ ] **Task 1 — Retro Phase 5 extension.** Update `skills/momentum/skills/retro/workflow.md` Phase 5 to add the third routing disposition ("carry forward as handoff event") alongside the existing Tier 1 distill path and Tier 2 stub path. Include the developer-approval prompt for handoff carry-forward. Document the handoff event schema inline in Phase 5 so the retro instructions are self-contained. Call the Story A-provided CLI to write each approved handoff event. Covers ACs 1, 2, 3, 10, 11.

- [ ] **Task 2 — Sprint-planning Phase A.5 extension.** Update `skills/momentum/skills/sprint-planning/workflow.md` Step 1 Phase A.5 to add a read of `_bmad-output/implementation-artifacts/intake-queue.jsonl` filtered to `source: "retro"`, `kind: "handoff"`, `status: "open"` immediately after the previous sprint summary load. Fold open handoff items into the synthesis context that feeds Phase C. Covers AC 5.

- [ ] **Task 3 — Sprint-planning output surfaces handoff section.** Extend Phase C of Step 1 in `skills/momentum/skills/sprint-planning/workflow.md` so that the recommendation display gains a labeled "Open handoff items from recent retros" section listing each open handoff entry with title, source sprint, and (when present) feature-state transition or failure-diagnosis framing. Covers AC 6.

- [ ] **Task 4 — Triage handoff-kind verification.** With Story A merged, run an end-to-end verification that triage's session-start queue read handles `kind: "handoff"` entries correctly. Document what works, document any triage-side gaps discovered, and — only if gaps exist — note them as follow-up work (separate story if non-trivial). This task produces no skill file changes unless a bug is discovered; then the fix is a task 4b. Covers AC 7.

- [ ] **Task 5 — Architecture.md cross-reference update for retired triage-inbox contract.** Update `_bmad-output/planning-artifacts/architecture.md` lines ~1671–1698 ("Retro → Triage Handoff Format"). Add a clearly-marked superseded banner at the top of the section that (a) names DEC-007 and this story as the replacement, (b) points to `intake-queue.jsonl` with `source: "retro"`, `kind: "handoff"` as the new contract, and (c) retains the existing YAML entry format below the banner for historical context. Do not delete the old section. Covers AC 9.

- [ ] **Task 6 — Consumption-update cross-check.** Verify that the existing Story A queue-mutation CLI supports updating status to `consumed` or `rejected` with an outcome reference for entries of any `kind` (not just `shape` / `watch`). If it does, this task is documentation-only — add a short note in retro workflow Phase 5 pointing to the CLI syntax. If it does not, open a follow-up story against `triage-skill` (or a new queue-mutation-cli story) rather than implementing the CLI change here — this story's scope is retro + planning, not queue CLI. Covers AC 8.

## Dev Notes

### Architecture Compliance

- **DEC-005 (2026-04-14) — Cycle redesign.** This story implements Phase 5 of DEC-005's phased plan (Retro restructure). Specifically: D7 (failure-as-diagnostic framing in handoff events), D8 (feature-state transition framing in handoff events), D10 (retro does not gap-check when emitting handoff), D1/D5 (handoff items carry `suggested_feature_slug` and `suggested_story_type` when they imply new work). Sprint-planning Phase A.5 is a Phase 3 touchpoint (sprint-planning restructure) that piggy-backs on the existing summary-load infrastructure.
- **DEC-007 (2026-04-14) — Unified intake-queue.jsonl.** This story is explicitly called out as the Phase 3 and Phase 4 deliverable in DEC-007's phased plan: "Wire `momentum:retro` to write `handoff` entries in the same artifact" and "Update `momentum:sprint-planning` to optionally read `handoff` entries when synthesizing next sprint backlog." The `triage-inbox.md` contract retirement (AC 9) is explicit in DEC-007's architecture_decisions_affected list.
- **Decision 27 (Transcript Audit Retro) — superseded-partial per DEC-005.** Retro's findings document (`retro-transcript-audit.md`) remains the primary retro output. This story adds a secondary output — queue events — that flow downstream into planning. The findings document is the human audit trail; the queue event is the machine-readable carry-forward.
- **Decision 30 (Gherkin Separation).** Story markdown files carry plain English ACs only. Gherkin specs for this story, if authored during sprint planning, live in `sprints/{sprint-slug}/specs/` and are accessible only to verifier agents — dev agents never read them. All ACs above are plain English.
- **Decision 34 (Retro Owns Sprint Closure).** Retro's ownership of sprint closure is preserved; this story extends Phase 5, not Phase 6 (closure). Handoff event writes must happen inside Phase 5 so sprint closure in Phase 6 can run against a fully-recorded handoff state.
- **Orchestrator purity.** `momentum:retro` remains an orchestrator — queue-event writes go through the Story A CLI, not through retro writing JSONL directly. This matches the same pattern `momentum:triage` uses for its SHAPING/DEFER/REJECT writes per DEC-007.

### Testing Requirements

- **EDD for skill-instruction changes (Tasks 1, 2, 3).** Retro workflow.md and sprint-planning workflow.md are LLM prompts. Write behavioral evals, not unit tests:
  - At minimum, one eval per modified skill covering the golden path (retro: developer approves a handoff carry-forward at Phase 5, event is written through the CLI; sprint-planning: Phase A.5 reads a seeded queue with one open handoff entry, Phase C recommendation output includes the "Open handoff items" section).
  - At least one eval per skill covering a boundary case (retro: developer declines all handoff carry-forwards — no events written; sprint-planning: empty queue — output contains no handoff section or explicitly says "no open handoff items").
  - Store evals in `skills/momentum/skills/retro/evals/` and `skills/momentum/skills/sprint-planning/evals/`.
- **Functional verification for Task 4 (triage handoff-kind).** Seed the queue with a test handoff entry, invoke triage, confirm the handoff entry surfaces in triage's classification list with the same UX as SHAPING/DEFER entries. This is a manual verification run — document the result in the Dev Agent Record.
- **Specification verification for Task 5 (architecture.md update).** After editing architecture.md, confirm cross-references resolve (DEC-007 link works, "this story" link points to `retro-triage-handoff.md`, `intake-queue.jsonl` path is correct).
- **Golden-path end-to-end acceptance.** After all tasks merge, run a full retro → handoff-write → sprint-planning cycle against a real recent sprint. Confirm AC 4 holds — no manual injection needed. Document the run in the Dev Agent Record.
- **No-regression check.** Run a retro that emits zero handoff events (all findings are either Tier 1 distilled or Tier 2 stubbed). Confirm sprint-planning Phase A.5 handles the empty-queue case without error and the recommendation output's handoff section is either absent or cleanly labeled "No open handoff items."

### Implementation Guide

#### Task-by-Task Approach

**Task 1 (Retro Phase 5 extension) — skill-instruction / EDD.**
- Before writing: draft 2–3 evals in `skills/momentum/skills/retro/evals/` describing the expected Phase 5 behavior. Example eval topics: "Given three findings where one is Tier 1, one is Tier 2, one is neither, Phase 5 prompts for handoff carry-forward on the third"; "Given all findings declined, Phase 5 writes zero handoff events and records disposition as `skipped`."
- Implementation: add the third disposition arm to Phase 5's routing block. Keep the existing Tier 1 distill and Tier 2 stub arms unchanged. The new arm prompts the developer ("Carry this forward as a handoff event for next sprint? Y/N") and on Y calls the Story A CLI with the handoff schema fields.
- Include the full handoff event schema inline in Phase 5 (field list, types, optional-field rules) so the retro instructions are self-contained and the dev agent implementing this does not need to open DEC-007 to check.
- Verify: run each eval by spawning a subagent with the updated workflow.md as context; confirm behavior matches.

**Task 2 (Sprint-planning Phase A.5 extension) — skill-instruction / EDD.**
- Evals: "Given a queue with two open retro handoffs, Phase A.5 includes both in the synthesis context"; "Given an empty queue, Phase A.5 proceeds with only the previous sprint summary."
- Implementation: insert the queue read immediately after the existing `sprint-summary.md` load. Use a small JSONL scan (Python or `jq`-style filter) to pull `source == "retro" AND kind == "handoff" AND status == "open"` entries. Store as `{{handoff_items}}` for downstream reference in Phase C.
- Keep the read defensive: if `intake-queue.jsonl` does not exist (e.g., first-ever sprint after Story A merges), treat as empty and continue silently.

**Task 3 (Sprint-planning Phase C handoff section) — skill-instruction / EDD.**
- Eval: "Given three open handoff items with mixed framing (one feature-state transition, one failure diagnosis, one plain), Phase C output labels the section, lists each item with its source sprint, and renders the optional framing when present."
- Implementation: add an "Open handoff items from recent retros" block to the Phase C output template. Render per-item: title, source sprint, and — if `feature_state_transition` present — a one-liner "feature X: prior Done → observed Partial — evidence: ..."; if `failure_diagnosis` present — a one-liner "attempted: ... / didn't work: ... / learned: ...".

**Task 4 (Triage verification) — specification / functional verification.**
- Run triage against a seeded queue containing a single handoff entry. Observe whether triage surfaces the entry in its classification list.
- If it works: Dev Agent Record notes "verified — no changes needed." Story does not edit triage workflow.md.
- If a gap is found: write a short findings note describing the gap, and — only if the fix is small and scoped to this story — patch it here. Non-trivial gaps get a follow-up story against `triage-skill`, not a scope creep in this story.

**Task 5 (Architecture.md update) — specification / direct authoring with cross-reference verification.**
- Edit `_bmad-output/planning-artifacts/architecture.md` lines ~1671–1698 (the "Retro → Triage Handoff Format" section).
- Add at the top of the section, immediately under the heading:
  > **> Superseded 2026-04-14 by DEC-007 and story `retro-triage-handoff`.** The `triage-inbox.md` contract below was never built and has been replaced by `intake-queue.jsonl` (one artifact, JSONL event log, `source` and `kind` discriminators). See `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md`. Retained below as historical context.
- Preserve the existing YAML entry format and body below the banner.
- Verify: grep architecture.md for any other references to `triage-inbox.md` and update them similarly, or cross-reference the superseded section.

**Task 6 (Consumption-update cross-check) — specification / investigation.**
- Read Story A's CLI implementation for queue-event mutation.
- If it supports `kind`-agnostic status updates with an outcome reference: add a one-line reference in retro Phase 5 pointing to the CLI syntax. Done.
- If it does not: flag as out-of-scope; open a triage-skill follow-up story. Do not patch queue CLI in this story.

#### Gherkin Reminder (Decision 30)

Gherkin specs for this story, if authored during sprint planning, are at `sprints/{sprint-slug}/specs/retro-triage-handoff.feature` and are accessible only to verifier agents. The dev agent implements against the plain English ACs above and never reads the `.feature` file. Do not write Gherkin into this story file under any circumstances.

### Project Structure Notes

**Files that will be modified by this story:**

- `skills/momentum/skills/retro/workflow.md` — Phase 5 extended with handoff disposition (Task 1).
- `skills/momentum/skills/sprint-planning/workflow.md` — Step 1 Phase A.5 extended with queue read (Task 2); Phase C output extended with handoff section (Task 3).
- `_bmad-output/planning-artifacts/architecture.md` — lines ~1671–1698 get superseded banner (Task 5).

**Files that must exist (prerequisite — delivered by Story A `triage-skill`, not this story):**

- `_bmad-output/implementation-artifacts/intake-queue.jsonl` — the queue file itself (created on first write by Story A's CLI).
- `momentum-tools` CLI: `queue write` (or equivalent) for appending events; `queue update` (or equivalent) for mutating status on existing entries.
- Triage workflow.md already reads the queue at session start — no change required here.

**Files this story creates:**

- `skills/momentum/skills/retro/evals/*.md` — 2–3 behavioral evals for Phase 5 handoff disposition.
- `skills/momentum/skills/sprint-planning/evals/*.md` — 2–3 behavioral evals for Phase A.5 queue read and Phase C handoff section.

**Structural alignment with existing patterns:**

- Retro already has a Phase 5 routing block that branches between Tier 1 distill and Tier 2 stub; adding a third arm for handoff matches the existing pattern.
- Sprint-planning Phase A.5 already performs a conditional file read (sprint-summary.md) and tolerates missing files; the queue read follows the same pattern.
- Architecture.md already has a "superseded 2026-04-08" pattern used on the Agent Logging Infrastructure section — this story uses the same banner convention.
- All queue writes flow through CLI — no JSONL is written directly by any skill. This matches the orchestrator-purity pattern enforced by DEC-007 across retro, triage, and future producers.

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → skill-instruction (EDD)
- Task 4 → specification (functional verification — investigation task, no file edits expected on success)
- Task 5 → specification (direct authoring with cross-reference verification)
- Task 6 → specification (investigation; conditional documentation update)

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/retro/evals/` and `skills/momentum/skills/sprint-planning/evals/` (create `evals/` if they don't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-retro-phase-5-writes-handoff-on-approve.md`, `eval-sprint-planning-surfaces-open-handoffs.md`).
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Modify `skills/momentum/skills/retro/workflow.md` (Task 1) and `skills/momentum/skills/sprint-planning/workflow.md` (Tasks 2, 3).

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's scenario as its task, plus the modified workflow.md contents as context. Observe whether the subagent's behavior matches the expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the workflow instructions, revise, re-run (max 3 cycles; surface to user if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md changes (if any): `description` field must be ≤150 characters (NFR1) — count precisely. This story primarily edits workflow.md; if SKILL.md touches happen, the 150-char rule applies.
- `model:` and `effort:` frontmatter fields must be present and unchanged.
- Workflow.md body changes must not push the file past any existing size budget documented in the skill's references. If retro's workflow.md grows substantially, consider extracting the handoff event schema into `skills/momentum/skills/retro/references/handoff-event-schema.md` with a clear load instruction from the workflow.
- Skill names use `momentum:` namespace prefix (NFR12) — no changes here since neither skill name changes.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/retro/evals/`
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] No SKILL.md `description` field regressions (≤150 characters still satisfied if touched)
- [ ] `model:` and `effort:` frontmatter unchanged on both skills
- [ ] Workflow.md body sizes documented before/after; if grown meaningfully, overflow extracted to `references/`
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

---

#### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, DEC, parent spec) — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria.
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly.
   - Task 4: If documentation is updated, confirm cross-references to Story A (`triage-skill`) and the `intake-queue.jsonl` path resolve.
   - Task 5: Confirm the DEC-007 cross-reference path is correct (`_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md`); confirm "this story" link points to this story file; confirm `intake-queue.jsonl` path is correct.
   - Task 6: If the CLI-syntax note is added to retro Phase 5, confirm the CLI command syntax matches Story A's actual implementation.
3. **Verify format compliance:** architecture.md uses a specific "superseded [date] by [ref]" banner convention already present in the file (see the "Updated 2026-04-08" block around the Agent Logging Infrastructure section). Match that convention.
4. **Document** what was written or updated in the Dev Agent Record.

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum:dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] All cross-references to other documents, files, or sections resolve correctly
- [ ] Architecture.md banner matches the existing "Updated [date]" / superseded convention in the file
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

---

#### Gherkin Separation Reminder (Decision 30)

Gherkin specs for this sprint exist at `sprints/{sprint-slug}/specs/retro-triage-handoff.feature` and are off-limits to the dev agent. The dev agent implements against the plain English ACs in this story file only, never against `.feature` files. This story file contains zero Gherkin by design — if any `Given/When/Then` structure appears here, that is a defect.

### References

- **Plans:** `/Users/steve/.claude/plans/curious-crunching-crystal.md` — the approved plan that produced this story stub rewrite (Story B).
- **Decisions:**
  - `_bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md` — D1 (feature-first), D5 (story types), D6 (terminal states), D7 (failure as diagnostic), D8 (retro as feature-state hygienist), D10 (no gap-check at handoff). This story is in DEC-005 `stories_affected`.
  - `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md` — unified `intake-queue.jsonl`; this story is in DEC-007 `stories_affected`; DEC-007 Phase 3 and Phase 4 are this story's scope.
- **Architecture:**
  - `_bmad-output/planning-artifacts/architecture.md` lines ~1671–1698 — the `triage-inbox.md` contract this story retires (Task 5 edits here).
  - `_bmad-output/planning-artifacts/architecture.md` — Decision 27 (Transcript Audit Retro, superseded-partial), Decision 30 (Gherkin separation), Decision 34 (Retro owns sprint closure).
- **Depends on:** `triage-skill` (Story A). Story A delivers the `intake-queue.jsonl` schema, write CLI, read path, and triage-side classification flow. This story is Story B in the approved plan.
- **Skills touched:**
  - `skills/momentum/skills/retro/workflow.md` — Phase 5 is the extension point (Task 1).
  - `skills/momentum/skills/sprint-planning/workflow.md` — Step 1 Phase A.5 is the queue-read extension point (Task 2); Phase C is the output-surface extension point (Task 3).
- **Features:**
  - `_bmad-output/planning-artifacts/features.json` — this story is already listed under `momentum-retro-and-flywheel.stories`. No features.json edit needed.
- **Superseded artifacts (explicitly retired by this story and its prerequisite):**
  - `triage-inbox.md` contract in architecture.md lines ~1671–1698 — superseded by DEC-007.
  - `retro-summary.json` proposed handoff artifact (never built — never referenced in architecture.md after DEC-007).
- **Pain evidence:** HF-01 (2026-04-11T05:31), HF-03 (2026-04-11T05:36) — the handoff-manual-injection moments from sprint-2026-04-10 planning.
- **Epic membership:** `impetus-epic-orchestrator` (Epic 2b — Impetus as Sprint Orchestrator). FRs covered: FR49 (triage workflow), FR52 (epic lifecycle including retro → triage → planning).

## Dev Agent Record

<!-- This section is populated only during and after development. -->

_Populated by the dev agent during implementation._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
