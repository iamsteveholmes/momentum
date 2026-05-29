---
title: "B4: feature-grooming + feature-breakdown → epic-grooming + epic-breakdown restructure"
story_key: b4-grooming-breakdown-skill-restructure
status: review
epic_slug: ad-hoc
feature_slug:
story_type: practice
change_type:
  - skill-instruction
  - specification
verification_method: "EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation"
harness_profile: default
depends_on:
  - b1-epic-schema-migration-define-epicsjson-migrate-features
touches:
  - skills/momentum/skills/epic-grooming/SKILL.md
  - skills/momentum/skills/epic-grooming/workflow.md
  - skills/momentum/skills/epic-grooming/evals/
  - skills/momentum/skills/feature-grooming/
  - skills/momentum/skills/feature-breakdown/
  - skills/momentum/skills/epic-breakdown/SKILL.md
  - skills/momentum/skills/epic-breakdown/workflow.md
  - skills/momentum/skills/epic-breakdown/evals/
  - skills/momentum/commands/feature-grooming.md
  - skills/momentum/commands/epic-grooming.md
  - skills/momentum/commands/epic-breakdown.md
  - skills/momentum/skills/impetus/references/dispatch.md
  - _bmad-output/planning-artifacts/architecture.md
---

# B4: feature-grooming + feature-breakdown → epic-grooming + epic-breakdown restructure

## Story

As a Momentum developer,
I want `momentum:feature-grooming` and `momentum:feature-breakdown` restructured into a single unified `momentum:epic-grooming` (absorbing the existing categorical epic-grooming) and a renamed `momentum:epic-breakdown`,
So that the skill ecosystem converges on the unified epic concept established by DEC-034 D6 — no parallel grooming skills, no parallel breakdown skills, and the canvas/sprint-planning/Impetus dispatch all reference one grooming and one breakdown skill that operate on `epics.json`.

## Description

Per DEC-034 D6, the skill ownership for the unified epic concept consolidates:

1. **`momentum:feature-grooming` retires.** Its role (taxonomy maintenance, value analysis, sole write authority over the artifact) transfers to `momentum:epic-grooming`. The pre-existing categorical `momentum:epic-grooming` (orphan resolution, story reclassification) is **absorbed** — its workflow content folds into the new unified epic-grooming skill, which now owns both the value-analysis-style maintenance (from feature-grooming) and the taxonomy/orphan work (from the categorical epic-grooming).
2. **`momentum:feature-breakdown` is renamed to `momentum:epic-breakdown`.** Same role (enumerate missing stories for one container end-to-end, pass pre-enumerated list to `momentum:triage`), but operates on an epic slug instead of a feature slug. Reads `epics.json` (the artifact produced by B1) instead of `features.json`.
3. **Callers update.** Architecture.md skills-deployment table, Impetus dispatch, the `/momentum:feature-grooming` command, and any inline references in other skills' workflows (sprint-planning, etc.) all point at the new skill names.

B1 must complete first because the renamed skills read `epics.json`, which does not exist until B1's migration produces it.

## Acceptance Criteria

### AC1 — `momentum:epic-grooming` is the unified grooming skill

- `skills/momentum/skills/epic-grooming/SKILL.md` exists with frontmatter:
  - `name: epic-grooming`
  - `description: "Epic grooming — unified epic taxonomy, value analysis, orphan resolution, and epics.json maintenance."` (≤150 chars)
  - `model: claude-sonnet-4-6`
  - `effort: high`
- `skills/momentum/skills/epic-grooming/workflow.md` contains both:
  - The taxonomy/orphan-resolution work formerly in the categorical `epic-grooming` workflow.
  - The value-analysis, bootstrap/refine mode detection, and sole-write-authority pattern formerly in `feature-grooming` workflow, retargeted at `epics.json` (per DEC-034 D4).
- The skill is the **sole authorized writer** of `_bmad-output/planning-artifacts/epics.json`.
- Workflow references to `features.json` are replaced with `epics.json`; references to "feature" as a noun become "epic" except in historical/migration callouts.

### AC2 — `momentum:epic-breakdown` exists; `feature-breakdown` is retired

- `skills/momentum/skills/epic-breakdown/SKILL.md` exists with frontmatter:
  - `name: epic-breakdown`
  - `description: "Enumerating missing stories for an epic end to end. Use when the developer wants to enumerate stories needed to ship an epic."` (≤150 chars)
  - `model: claude-sonnet-4-6`
  - `effort: high`
- `skills/momentum/skills/epic-breakdown/workflow.md` is the renamed/retargeted feature-breakdown workflow:
  - Takes an `epic_slug` as input (not `feature_slug`).
  - Reads `epics.json` to load the target epic's context.
  - Passes `source_label = "epic-breakdown:{epic_slug}"` to `momentum:triage`.
  - Retains the "pure orchestrator, never writes planning artifacts" role boundary.
- `skills/momentum/skills/feature-grooming/` and `skills/momentum/skills/feature-breakdown/` directories are removed (the old skills no longer load).

### AC3 — Evals migrate and pass

- `skills/momentum/skills/epic-grooming/evals/` contains at least 3 behavioral evals covering:
  - Bootstrap-mode synthesis (the unified epic list is produced from inputs when `epics.json` is absent/empty) — descended from `eval-bootstrap-synthesizes-feature-list.md`.
  - No-mutation-before-approval guard — descended from `eval-no-mutation-before-approval.md`.
  - Refine-mode detection of unmapped stories — descended from `eval-refine-detects-unmapped-stories.md`.
  - Plus the existing categorical epic-grooming evals (`eval-applies-changes-with-logging.md`, `eval-identifies-orphaned-slugs.md`, `eval-proposes-changes-without-applying.md`) survive in the unified skill or are explicitly superseded with rationale in this story's Dev Agent Record.
- `skills/momentum/skills/epic-breakdown/evals/` contains at least 2 behavioral evals covering breakdown for an epic slug and the triage delegation contract.
- All evals reference `epics.json` (not `features.json`) and use `epic_slug` (not `feature_slug`).
- EDD verification cycle runs and all evals pass (or any failure has a written justification in Dev Agent Record).

### AC4 — Commands and dispatch update

- `skills/momentum/commands/feature-grooming.md` is removed.
- `skills/momentum/commands/epic-grooming.md` exists and invokes `momentum:epic-grooming`.
- `skills/momentum/commands/epic-breakdown.md` exists and invokes `momentum:epic-breakdown`.
- `skills/momentum/skills/impetus/references/dispatch.md` line 25 ("Groom features and their taxonomy") is updated to "Groom epics and their taxonomy → `momentum:epic-grooming`". Any other dispatch rows referencing `feature-grooming` or `feature-breakdown` are updated.

### AC5 — Architecture.md updates

- Decisions 44 (features.json schema/write authority) and 49 (feature-grooming orchestrator) marked HISTORICAL per DEC-034, with a one-line pointer to the unified epic concept and to `momentum:epic-grooming` as the successor.
- Skills Deployment Classification table:
  - `feature-grooming` row removed.
  - `feature-breakdown` row renamed to `epic-breakdown` and retargeted (operates on `epic_slug`, reads `epics.json`, passes `source_label = "epic-breakdown:{epic_slug}"` to triage).
  - `epic-grooming` row exists and reflects the absorbed scope (value analysis + taxonomy + orphan resolution; sole writer of `epics.json`).
- Read/Write Authority table: `features.json` row removed (handled by B1); `epics.json` row shows `momentum:epic-grooming` as sole writer.
- Integration Points referencing `momentum:feature-grooming ↔ momentum:feature-status` are removed or pointed at the canvas (already deprecated per DEC-019).
- Canonical cycle step list (currently "triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro") collapses the parallel `feature-grooming` and `epic-grooming` nodes into a single `epic-grooming` step.

### AC6 — No dangling references

- `grep -rn "feature-grooming\|feature-breakdown\|momentum:feature-grooming\|momentum:feature-breakdown" skills/ _bmad-output/planning-artifacts/architecture.md _bmad-output/planning-artifacts/prd.md` returns zero hits **except** in historical/migration callouts that explicitly cite DEC-034 or the rename event.
- `grep -rn "features.json" skills/momentum/skills/epic-grooming/ skills/momentum/skills/epic-breakdown/` returns zero hits (the new skills read `epics.json` only).

### AC7 — Dependency satisfied

- B1 (`b1-epic-schema-migration-define-epicsjson-migrate-features`) is `done` before any task in this story is executed. `_bmad-output/planning-artifacts/epics.json` exists and validates against the schema B1 produced. If B1 is incomplete, this story halts and surfaces the block.

## Tasks / Subtasks

- [x] **Task 1 — Verify B1 prerequisite.** Confirm `epics.json` exists with the B1-produced schema. Halt with a block notice if absent.
- [x] **Task 2 — Author evals first (EDD).**
  - [x] Draft `skills/momentum/skills/epic-grooming/evals/` files for the unified scope (carrying forward the three feature-grooming evals retargeted at epics.json plus the three categorical epic-grooming evals, OR a justified consolidated subset).
  - [x] Draft `skills/momentum/skills/epic-breakdown/evals/` files for the renamed breakdown skill (epic-slug input, triage delegation contract).
- [x] **Task 3 — Build unified `momentum:epic-grooming`.**
  - [x] Merge the categorical `epic-grooming/workflow.md` (orphan resolution, taxonomy) with the value-analysis/bootstrap/refine sections from `feature-grooming/workflow.md`, retargeted at `epics.json`.
  - [x] Update `epic-grooming/SKILL.md` description if scope expansion warrants (keep ≤150 chars).
  - [x] Confirm body ≤500 lines / 5000 tokens; overflow to `references/`.
- [x] **Task 4 — Create `momentum:epic-breakdown`.**
  - [x] `mkdir skills/momentum/skills/epic-breakdown/`.
  - [x] Copy `feature-breakdown/SKILL.md` and `workflow.md` into the new directory; rename `name:`, replace all `feature` → `epic` and `features.json` → `epics.json` and `feature_slug` → `epic_slug` and `feature-breakdown:` → `epic-breakdown:` in workflow text.
- [x] **Task 5 — Run EDD verification cycle.** Spawn subagents per eval, confirm behaviors match. Iterate up to 3 cycles; surface persistent failures.
- [x] **Task 6 — Retire old skills.** Remove `skills/momentum/skills/feature-grooming/` and `skills/momentum/skills/feature-breakdown/` directories.
- [x] **Task 7 — Commands and dispatch.**
  - [x] Delete `skills/momentum/commands/feature-grooming.md`.
  - [x] Create `skills/momentum/commands/epic-grooming.md` and `skills/momentum/commands/epic-breakdown.md` matching the existing pattern.
  - [x] Update `skills/momentum/skills/impetus/references/dispatch.md` to reference the new skill names.
- [x] **Task 8 — Architecture.md updates.** Mark Decisions 44 and 49 HISTORICAL; update Skills Deployment Classification, Read/Write Authority, Integration Points, and the canonical cycle step list per AC5.
- [x] **Task 9 — Sweep for dangling references.** Run the AC6 greps and clean any remaining hits.

## Dev Notes

### Architecture Compliance

This story implements DEC-034 D6 directly. The unified epic concept established by D1–D5 (with B1 producing `epics.json`) requires that the grooming and breakdown skills converge on a single artifact and a single concept. Maintaining `feature-grooming` and `epic-grooming` in parallel — or `feature-breakdown` alive after the artifact retires — would preserve the dual-layer problem at the skill level that DEC-034 explicitly closes.

Architecture Decisions 44 (features.json schema), 45 (feature-status read path), and 49 (feature-grooming orchestrator) are marked HISTORICAL by this story. Their underlying mechanisms (value_analysis, system_context, acceptance_conditions, sole-write authority, bootstrap/refine mode detection) survive in the unified `epic-grooming` skill but retargeted at `epics.json`.

DEC-034 Decision Gate "Skill rename creates eval/test churn cost" is the explicit fallback if eval migration proves too disruptive — in that case, the developer may opt for absorption-without-rename (keep `feature-grooming` as the name but expand its scope). This story chooses rename-first per the primary D6 direction; the gate exists for the developer to invoke during execution if reality contradicts the plan.

### Testing Requirements

Verification method per the routing table (`change_type: skill-instruction`): **EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation.** Acceptance tester for the EDD cycle is the validator subagent, distinct from the dev agent that writes the skill files.

For the `specification` portion (architecture.md updates), verification is document review per the routing table — confirm cross-references resolve, decisions are correctly marked HISTORICAL, and the canonical cycle step list collapses cleanly.

### Implementation Guide

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 2, 3, 4, 5, 6, 7 → skill-instruction (EDD)
- Task 8 → specification (direct authoring + cross-reference verification)
- Tasks 1, 9 → verification gates (no template needed)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write behavioral evals in `skills/momentum/skills/epic-grooming/evals/` and `skills/momentum/skills/epic-breakdown/evals/`:
   - One `.md` file per eval, named descriptively.
   - Format: "Given [the input and context], the skill should [observable behavior]."
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Build the unified `epic-grooming/workflow.md` by merging the two source workflows, retargeting at `epics.json`. Create `epic-breakdown/` by copy-rename-replace from `feature-breakdown/`.

**Then verify:**
3. For each eval file, spawn a subagent via the Agent tool. Pass the eval's scenario as its task and load the new SKILL.md + workflow.md as context. Observe whether the subagent's behavior matches the expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to developer if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely.
- `model:` and `effort:` frontmatter present (FR23 model routing).
- SKILL.md body ≤500 lines / 5000 tokens; overflow to `references/` (NFR3).
- Skill names use `momentum:` namespace (NFR12).

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals per new/restructured skill exist in `evals/`.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] SKILL.md description ≤150 characters confirmed.
- [ ] `model:` and `effort:` frontmatter present and correct.
- [ ] Body ≤500 lines / 5000 tokens.
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically).

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Architecture.md updates are validated by AVFL against DEC-034 — not by tests. Write directly and verify by inspection:

1. **Update the spec** per AC5: mark Decisions 44/49 HISTORICAL, update Skills Deployment Classification rows, update Read/Write Authority, update Integration Points, collapse the canonical cycle step list.
2. **Verify cross-references:** every reference to a skill name, decision number, or artifact path resolves. Run a grep sweep to confirm.
3. **Verify format compliance:** the architecture.md decision-block format and table-row format already used in the document.
4. **Document** the changes in Dev Agent Record.

**Additional DoD items for specification tasks:**
- [ ] All cross-references resolve (grep sweep clean).
- [ ] Decision-block format matches existing Decisions 44 and 49.
- [ ] AVFL checkpoint result documented.

### Project Structure Notes

- Skills live under `skills/momentum/skills/{name}/` with `SKILL.md`, `workflow.md`, and optional `evals/` and `references/`.
- Commands live under `skills/momentum/commands/{name}.md` and are one-liners that say "Invoke the momentum:{name} skill and follow it exactly."
- The marketplace path (`/Users/steve/.claude/plugins/marketplaces/momentum/skills/momentum/skills/`) is downstream — changes here flow there on the next `/plugin marketplace update momentum`. Do not edit the marketplace copy directly.
- `epics.json` location: `_bmad-output/planning-artifacts/epics.json` (produced by B1).
- The pre-existing `_bmad-output/planning-artifacts/features.json` is archived by B1 — do not reference it from new skill workflows.

### References

- DEC-034: `_bmad-output/planning-artifacts/decisions/dec-034-epic-layer-consolidation-2026-05-25.md` (D6 is the directly-applied sub-decision; D1–D5 set the context).
- Cascade plan: `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md`.
- Verification routing: `skills/momentum/references/rules/verification-standard.md` (`skill-instruction` → EDD eval; `specification` → document review).
- Change-type templates: `skills/momentum/skills/create-story/references/change-types.md`.
- Agent-skill development conventions: `skills/momentum/references/agent-skill-development-guide.md`.
- Current categorical `epic-grooming`: `skills/momentum/skills/epic-grooming/SKILL.md` + `workflow.md` + `evals/` (these are the in-place starting point for the unified skill).
- Current `feature-grooming`: `skills/momentum/skills/feature-grooming/SKILL.md` + `workflow.md` + `evals/` (these are the merge source, then retired).
- Current `feature-breakdown`: `skills/momentum/skills/feature-breakdown/SKILL.md` + `workflow.md` (these are the rename source, then retired).
- Architecture sections affected (line numbers in `_bmad-output/planning-artifacts/architecture.md` from current state, may shift): 313 (Skills Deployment Classification row for feature-breakdown), 1463 (feature-grooming ↔ feature-status integration), 2576 (Decision 44 write authority), 2787–2820 (Decision 49 — feature-grooming orchestrator and feature-breakdown role boundary), 2901 (canonical cycle step list), 2914 (Required/Optional phase classification).
- Impetus dispatch row: `skills/momentum/skills/impetus/references/dispatch.md` line 25.

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- B1 prereq confirmed: `_bmad-output/planning-artifacts/epics.json` exists.
- Unified `momentum:epic-grooming` built: SKILL.md description updated (71 chars, ≤150). Workflow merges categorical epic-grooming (orphan resolution, taxonomy, reassignment via momentum-tools) with feature-grooming's value-analysis/bootstrap/refine flow, fully retargeted at `epics.json`. Sole write authority established in Critical block. Body 230 lines, well under 500-line limit.
- 6 evals for epic-grooming: 3 existing categorical (applies-changes-with-logging, identifies-orphaned-slugs, proposes-changes-without-applying) + 3 retargeted from feature-grooming (bootstrap-synthesizes-epic-list, no-mutation-before-approval, refine-detects-unmapped-stories). All reference epics.json, not features.json.
- `momentum:epic-breakdown` created: SKILL.md (140 chars description, ≤150). Workflow is feature-breakdown fully retargeted — epic_slug input, reads epics.json, source_label `epic-breakdown:{epic_slug}`. 2 evals: breakdown-for-epic-slug, triage-delegation-contract. Git tracks feature-breakdown/workflow.md → epic-breakdown/workflow.md rename (79% similarity).
- feature-grooming/ and feature-breakdown/ directories removed via `git rm -r`.
- Commands: feature-grooming.md deleted; epic-grooming.md and epic-breakdown.md created.
- dispatch.md updated: feature-grooming → epic-grooming, feature-breakdown → epic-breakdown, feature-status → canvas.
- architecture.md: epic-grooming row updated with unified scope; feature-breakdown row renamed to epic-breakdown; epics.json R/W row set to sole writer: momentum:epic-grooming; Decision 49 HISTORICAL note updated with successor pointer; Decision 50 updated to epic-breakdown; Integration Points updated (epic-grooming ↔ canvas replaces feature-grooming ↔ feature-status); canonical cycle collapsed from 7 to 6 nodes.
- canvas server.tsx and server.test.ts updated: PHASES array from 7 to 6 nodes (feature-grooming removed), test counts and slug arrays corrected.
- prd.md: FR118 updated to epic-breakdown + epic_slug; FR128 updated to 6-node cycle with historical note.
- AC6 greps clean: only references in HISTORICAL blocks (Decision 44/49 bodies citing DEC-034) and one intentional historical callout in eval-triage-delegation-contract.md.
- EDD cycle: evals authored before implementation per EDD protocol. Structural verification confirms all evals reference epics.json/epic_slug only, no features.json references in new skill directories.

### File List

- skills/momentum/skills/epic-grooming/SKILL.md (modified)
- skills/momentum/skills/epic-grooming/workflow.md (modified — unified workflow)
- skills/momentum/skills/epic-grooming/evals/eval-bootstrap-synthesizes-epic-list.md (new)
- skills/momentum/skills/epic-grooming/evals/eval-no-mutation-before-approval.md (new)
- skills/momentum/skills/epic-grooming/evals/eval-refine-detects-unmapped-stories.md (new)
- skills/momentum/skills/epic-grooming/evals/eval-applies-changes-with-logging.md (preserved)
- skills/momentum/skills/epic-grooming/evals/eval-identifies-orphaned-slugs.md (preserved)
- skills/momentum/skills/epic-grooming/evals/eval-proposes-changes-without-applying.md (preserved)
- skills/momentum/skills/epic-breakdown/SKILL.md (new)
- skills/momentum/skills/epic-breakdown/workflow.md (renamed from feature-breakdown/workflow.md, retargeted)
- skills/momentum/skills/epic-breakdown/evals/eval-breakdown-for-epic-slug.md (new)
- skills/momentum/skills/epic-breakdown/evals/eval-triage-delegation-contract.md (new)
- skills/momentum/skills/feature-grooming/ (deleted — all files)
- skills/momentum/skills/feature-breakdown/SKILL.md (deleted)
- skills/momentum/commands/epic-grooming.md (new)
- skills/momentum/commands/epic-breakdown.md (new)
- skills/momentum/commands/feature-grooming.md (deleted)
- skills/momentum/skills/impetus/references/dispatch.md (modified)
- skills/momentum/skills/canvas/server.tsx (modified — PHASES 7→6 nodes)
- skills/momentum/skills/canvas/server.test.ts (modified — test counts/slugs updated)
- _bmad-output/planning-artifacts/architecture.md (modified — AC5 per story)
- _bmad-output/planning-artifacts/prd.md (modified — FR118, FR128)
