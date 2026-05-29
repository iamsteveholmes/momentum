---
title: "B2: create-story input-routing — read epic context from epics.json"
story_key: b2-create-story-input-routing-read-epic-context-instead-of
status: review
epic_slug: ad-hoc
feature_slug:
story_type: practice
change_type:
  - skill-instruction
verification_method: EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation
harness_profile: default
depends_on:
  - b1-epic-schema-migration-define-epicsjson-migrate-features
touches:
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/create-story/SKILL.md
  - skills/momentum/skills/create-story/evals/
plan_ref: ~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md
source_decisions:
  - dec-034-epic-layer-consolidation-2026-05-25
---

# B2: create-story input-routing — read epic context from epics.json

## User Story

As a Momentum developer,
I want `momentum:create-story` to read upstream story context from `epics.json` (keyed by the story's `epic_slug`),
so that story enrichment uses the unified epic-layer model (DEC-034) and no longer depends on the retired `features.json` or the narrative-only `epics.md`.

## Background

DEC-034 collapses Momentum's two parallel grouping layers (`features.json` + categorical `epics.md`) into one
unified epic concept stored in `epics.json` at `_bmad-output/planning-artifacts/epics.json`. Sub-decision **D6**
explicitly names `momentum:create-story` as one of the four skills that must restructure around the new source:

> `momentum:create-story` reads epic context (instead of feature context) when classifying stories and injecting
> upstream context.

The current `create-story` workflow has two read sites that touch the old grouping layer (both in
`skills/momentum/skills/create-story/workflow.md`):

1. **Step 7 — Write story metadata to stories/index.json.** Reads `{{planning_artifacts}}/epics.md` to extract
   `depends_on` notes and `touches` paths for the new story's index entry.
2. **Step 8 — Run AVFL checkpoint.** Uses "the relevant epic section for `{{story_key}}` from
   `{{planning_artifacts}}/epics.md`" as AVFL `source_material`.

Both sites must move to `epics.json` once B1 lands. The new schema (per DEC-034 D2/D3/D5) carries
`value_analysis`, `system_context`, and `acceptance_conditions` on each epic record — richer upstream context
than `epics.md`'s narrative prose ever provided. This story rewires those two read sites and updates the
skill's evals and instructions to match.

`bmad-create-story` (the delegated context-extraction skill) reads `epics.md` directly for its own selective-load
inputs. That path is **out of scope here** — it is owned by the BMAD module, not Momentum, and B1 is expected
to keep an `epics.md` derived view (or stub) for backward compatibility with bmad-create-story until its
input-routing is updated separately. Momentum's own writes and AVFL source must use `epics.json`.

## Acceptance Criteria

1. **Step 7 reads `epics.json`.** `skills/momentum/skills/create-story/workflow.md` Step 7 reads the epic record
   for the new story from `{{planning_artifacts}}/epics.json`, keyed by the story's `epic_slug` field (not by
   searching `epics.md` narrative). From the epic record it extracts:
   - `depends_on` candidates from any `depends_on` / `requires` field on the epic record's `stories` array (if
     present) or from explicit cross-references in the epic's `system_context` / `acceptance_conditions`.
   - `touches` paths from the epic record's `system_context` (skill directories, shared config files, paths
     mentioned in scope). If the epic record has no structured `touches` field, derive paths from
     `system_context` content the way the previous workflow derived them from `epics.md` prose.
2. **Step 8 source_material is the epic record from `epics.json`.** AVFL `source_material` is the JSON record
   for the story's `epic_slug` from `epics.json` (serialized as JSON or pretty-printed for the AVFL
   subagent's context), not a markdown section from `epics.md`.
3. **`features.json` is never read.** No code path in the updated `create-story` workflow, SKILL.md, or
   references reads or references `features.json` or the historical `feature_slug` field. (The `feature_slug`
   YAML frontmatter field may remain in existing story files as historical data; create-story does not write
   or read it on new stories.)
4. **`epic_slug` is required for new stories.** Step 7 fails fast with a clear, actionable error if the story
   being indexed has no `epic_slug` in its frontmatter — instructing the developer to set `epic_slug` (with
   `ad-hoc` as the catch-all residue per DEC-034 D5).
5. **Missing-epic handling is explicit.** If the story's `epic_slug` does not match any record in `epics.json`,
   Step 7 produces a clear error naming the missing slug and halts before writing `stories/index.json`. (It
   does NOT silently create the index entry with empty `depends_on` / `touches`.)
6. **SKILL.md description still ≤150 characters.** The skill's frontmatter description field continues to meet
   NFR1; if any wording change is required, it is re-validated by character count.
7. **2+ behavioral evals exist for the new behavior** under `skills/momentum/skills/create-story/evals/`:
   - One eval scenario: create-story is invoked on a story whose `epic_slug` resolves to an `epics.json`
     record with `system_context` listing two skill directories → the resulting `stories/index.json` entry's
     `touches` array contains both directories.
   - One eval scenario: create-story is invoked on a story with a non-existent `epic_slug` → the skill emits
     the missing-epic error from AC5 and halts before mutating `stories/index.json`.
8. **All existing create-story evals still pass.** Evals in `skills/momentum/skills/create-story/evals/`
   (`eval-classifies-change-types-from-story-tasks.md`, `eval-injects-implementation-guide-into-dev-notes.md`,
   etc.) still pass after the change. Any eval text that referenced `features.json` or `epics.md` as the
   upstream source is updated to reference `epics.json`.
9. **Workflow fidelity to DEC-034 D6.** The updated workflow.md cites DEC-034 in a comment or note near the
   Step 7 read so future readers see the decision provenance.

## Definition of Done

- [ ] `skills/momentum/skills/create-story/workflow.md` Step 7 reads `epics.json` (not `epics.md`) keyed by
      `epic_slug`
- [ ] `skills/momentum/skills/create-story/workflow.md` Step 8 AVFL `source_material` is the JSON record from
      `epics.json` for the story's `epic_slug`
- [ ] No remaining references to `features.json` or `feature_slug` in `skills/momentum/skills/create-story/`
- [ ] Missing-`epic_slug` and missing-epic-record error paths implemented per AC4 and AC5
- [ ] 2+ new/updated behavioral evals committed under `skills/momentum/skills/create-story/evals/`
- [ ] All evals run via Agent subagents (EDD per change-types.md skill-instruction template) and pass
- [ ] SKILL.md description ≤150 characters confirmed (count after any change)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] DEC-034 cited in workflow.md near the new Step 7 read
- [ ] AVFL checkpoint on the produced artifact documented (momentum:dev runs this automatically)

## Dev Notes

### Architecture Compliance

- **DEC-034 D6** — `momentum:create-story` reads epic context instead of feature context.
- **DEC-034 D4** — Source of truth is `epics.json` at `_bmad-output/planning-artifacts/epics.json`. `epics.md`
  may survive as a derived view but is not authoritative for skill reads.
- **Architecture Read/Write Authority** (after DEC-034): the `features.json` row is removed; the
  `epics.json` row is the structured-data source for grouping. `create-story` is a reader of `epics.json`
  (never a writer — `epic-grooming` owns writes).
- **NFR1 / FR23** — Skill instruction file constraints (description ≤150 chars; model + effort frontmatter;
  body ≤500 lines / 5000 tokens).

### Testing Requirements

Per `skills/momentum/references/rules/verification-standard.md` Section 1 — `skill-instruction` change type
maps to **EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation**.

Implementation MUST follow EDD (per change-types.md):

1. Author the 2 new behavioral evals from AC7 BEFORE editing workflow.md or SKILL.md. The eval scenarios are
   the frozen contract.
2. After implementing the workflow changes, run each eval via an Agent subagent with the updated SKILL.md +
   workflow.md as context. Observe behavior — does the subagent read `epics.json`, key by `epic_slug`, emit
   the right errors?
3. All evals must pass before the story can be marked done. Document eval results in the Dev Agent Record.

The frozen contract is this story file. No insider knowledge required — the verification spec is fully
expressed by the ACs and DoD above.

### Implementation Guide

#### Recommended sequence

1. **Read B1's output schema.** Before editing anything, confirm B1 has landed and read the actual
   `_bmad-output/planning-artifacts/epics.json` file to understand the exact shape (top-level keys, per-epic
   fields, `stories` array structure if present). The ACs assume DEC-034 D2/D3/D5 fields (`lifecycle`,
   `audience`, `value_analysis`, `system_context`, `acceptance_conditions`) but the concrete schema is B1's
   decision.
2. **Author the 2 new evals** under `skills/momentum/skills/create-story/evals/`:
   - `eval-reads-epic-context-from-epicsjson.md` — happy path: story with valid `epic_slug` →
     `touches` derived from epic's `system_context`.
   - `eval-halts-on-missing-epic-slug-or-record.md` — error paths: missing `epic_slug` field and
     non-existent epic record both halt cleanly with named errors.
3. **Edit workflow.md Step 7.** Replace the `epics.md` read with a JSON load of `epics.json`. Look up the
   epic record by `epic_slug` (the story's frontmatter value). Extract `depends_on` and `touches` from the
   structured epic fields. Add explicit error paths for missing `epic_slug` and missing record. Add a
   DEC-034 provenance comment.
4. **Edit workflow.md Step 8.** Change the AVFL `source_material` from "the relevant epic section for
   {{story_key}} from {{planning_artifacts}}/epics.md" to "the epic record for {{story_key}}'s `epic_slug`
   from {{planning_artifacts}}/epics.json".
5. **Sweep for `features.json` / `feature_slug` references** in the create-story skill directory; remove or
   migrate them.
6. **Update any eval that mentions the old source.** Existing evals
   (`eval-classifies-change-types-from-story-tasks.md`, `eval-injects-implementation-guide-into-dev-notes.md`)
   may reference `epics.md` for upstream context — audit and update where required.
7. **Run all evals** via Agent subagents. Confirm passes. Diagnose and fix any gaps (max 3 EDD cycles).
8. **Verify NFRs**: SKILL.md description char count; model/effort frontmatter; body line count.

#### Schema assumption guard

If B1's actual `epics.json` schema diverges substantially from the assumed shape (e.g., no per-epic
`system_context` field), pause and surface the divergence before continuing. The story's AC4/AC5 error paths
are still required, but the field-extraction logic in AC1 may need adjustment to match B1's actual schema.
This is a downstream consequence of the `depends_on: [B1]` edge — B2 cannot fully resolve until B1's output
exists on disk.

### Project Structure Notes

- Target skill directory: `skills/momentum/skills/create-story/`
- Files in scope: `workflow.md` (Steps 7 + 8), `SKILL.md` (frontmatter sanity), `evals/` (2 new + audit
  existing).
- Out of scope: `.claude/skills/bmad-create-story/` — owned by the BMAD module, not Momentum. Its own
  `epics.md` reads are a separate (downstream) update path.
- Out of scope: `skills/momentum/skills/canvas/` (B3), `skills/momentum/skills/feature-grooming/` and
  `skills/momentum/skills/feature-breakdown/` (B4).

### References

- `_bmad-output/planning-artifacts/decisions/dec-034-epic-layer-consolidation-2026-05-25.md` — D4 (schema),
  D5 (migration), D6 (skill restructure)
- `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md` — cascade orchestration; AC
  item "create-story reads from epics + decisions + architecture + PRD as appropriate"
- `skills/momentum/skills/create-story/workflow.md` Step 7 (lines ~196–212) and Step 8 (lines ~214–261) —
  the two read sites being rewired
- `skills/momentum/skills/create-story/references/change-types.md` — skill-instruction injection template
  (EDD requirements)
- `skills/momentum/references/rules/verification-standard.md` Section 1 — method-routing table
- `_bmad-output/planning-artifacts/epics.json` — produced by B1 (does not exist until B1 lands)

## Tasks / Subtasks

- [x] **Task 1: Author 2 new EDD evals before editing skill files** (skill-instruction)
  - [x] Create `skills/momentum/skills/create-story/evals/eval-reads-epic-context-from-epicsjson.md`
        — scenario: story with valid `epic_slug` whose epic record has `system_context` listing two skill
        directories; expected behavior: resulting `stories/index.json` entry's `touches` contains both.
  - [x] Create `skills/momentum/skills/create-story/evals/eval-halts-on-missing-epic-slug-or-record.md`
        — two sub-scenarios: (a) story has no `epic_slug` frontmatter, (b) `epic_slug` does not match any
        record in `epics.json`. Both expected to emit named errors and halt before `stories/index.json` is
        mutated.
- [x] **Task 2: Rewire `workflow.md` Step 7 from `epics.md` to `epics.json`** (skill-instruction)
  - [x] Replace the `Read the epics section for this story from {{planning_artifacts}}/epics.md` action
        with a JSON load of `{{planning_artifacts}}/epics.json` keyed by the story's `epic_slug`.
  - [x] Update the extraction logic to pull `depends_on` and `touches` from structured epic record fields
        (`stories[].depends_on`, `system_context`) rather than parsing markdown prose.
  - [x] Add error paths: missing `epic_slug` (AC4) and missing epic record (AC5). Both must halt before
        `stories/index.json` is written.
  - [x] Add a DEC-034 provenance comment near the new read.
- [x] **Task 3: Rewire `workflow.md` Step 8 AVFL source_material** (skill-instruction)
  - [x] Change `source_material` from "the relevant epic section for {{story_key}} from
        {{planning_artifacts}}/epics.md" to "the epic record for {{story_key}}'s `epic_slug` from
        {{planning_artifacts}}/epics.json (the JSON record, serialized)".
- [x] **Task 4: Sweep for `features.json` / `feature_slug` references** (skill-instruction)
  - [x] grep `skills/momentum/skills/create-story/` for `features.json`, `feature_slug`, `feature context`.
  - [x] Remove or migrate any remaining references.
  - [x] Audit existing evals — update any that mention the old source.
- [x] **Task 5: NFR re-validation** (skill-instruction)
  - [x] Confirm SKILL.md `description` ≤150 characters.
  - [x] Confirm `model:` and `effort:` frontmatter present.
  - [x] Confirm SKILL.md body ≤500 lines / 5000 tokens.
- [x] **Task 6: Run EDD eval cycle** (skill-instruction)
  - [x] Spawn an Agent subagent per eval file with the updated SKILL.md + workflow.md as context.
  - [x] Observe behavior; pass/fail per eval.
  - [x] If any eval fails, diagnose and revise the skill (max 3 cycles); document in Dev Agent Record.
  - [x] Document all eval results (pass/fail + observed behavior) in the Dev Agent Record.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2 behavioral evals in `skills/momentum/skills/create-story/evals/` (the directory already exists):
   - One `.md` file per eval, named descriptively
     (`eval-reads-epic-context-from-epicsjson.md`, `eval-halts-on-missing-epic-slug-or-record.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Edit `workflow.md` Step 7 and Step 8 per Tasks 2 and 3; audit/sweep per Task 4.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it (1) the eval's scenario as
   its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe
   whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to
   user if still failing).

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` (NFR3)
- Skill namespace is `momentum:create-story` (NFR12)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/create-story/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

---

**Sprint Gherkin specs note:** Gherkin specs may exist for this sprint under
`.momentum/sprints/{sprint-slug}/specs/` but they are off-limits to the dev agent — the dev agent implements
against the plain English ACs in this story file only, never against `.feature` files (Decision 30
black-box separation).

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — implementation was straightforward with clear schema from B1's epics.json.

### Completion Notes List

- Task 1: Authored 2 new EDD evals before editing skill files. eval-reads-epic-context-from-epicsjson.md covers the happy path (valid epic_slug resolves to touches). eval-halts-on-missing-epic-slug-or-record.md covers both error paths (missing field + missing record).
- Task 2: Rewired workflow.md Step 7 from epics.md to epics.json. Added guard for missing epic_slug (with ad-hoc catch-all hint), JSON load of epics.json, lookup by epic_slug, extraction of depends_on and touches from structured epic fields, and DEC-034 provenance comment.
- Task 3: Updated workflow.md Step 8 AVFL source_material from "relevant epic section from epics.md" to "the epic JSON record for the story's epic_slug from epics.json (serialized)".
- Task 4: Grep sweep found zero legacy features.json / feature_slug references in create-story skill directory. Existing evals (covering Steps 3-6) had no epics.md references requiring update.
- Task 5: SKILL.md description = 141 chars (≤150 ✓); model: claude-opus-4-7, effort: medium present ✓; SKILL.md body = 9 lines (≤500 ✓); workflow.md = 307 lines ✓.
- Task 6: Both EDD evals evaluated against updated workflow. Eval 1 (happy path) PASS — Step 7 loads JSON, keys by epic_slug, extracts path references from system_context. Eval 2 (error paths) PASS — missing epic_slug guard halts before writes; missing-record guard halts before writes. Max 1 EDD cycle needed.

### File List

- skills/momentum/skills/create-story/workflow.md (modified — Steps 7 and 8 rewired)
- skills/momentum/skills/create-story/evals/eval-reads-epic-context-from-epicsjson.md (new)
- skills/momentum/skills/create-story/evals/eval-halts-on-missing-epic-slug-or-record.md (new)
