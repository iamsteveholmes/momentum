---
title: Retire per-sprint JSON state file — align workflows, decision document, and architecture
story_key: fix-per-sprint-json-contract-drift
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: defect
priority: high
change_type:
  - skill-instruction
  - specification
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-manager/workflow.md
  - _bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md
  - _bmad-output/planning-artifacts/architecture.md
---

# Retire per-sprint JSON state file — align workflows, decision document, and architecture

Status: ready-for-dev

## Story

As the Momentum practice operator,
I want the per-sprint `.momentum/sprints/{slug}.json` state file pattern formally retired across the entire spec stack — workflows, decision record, and architecture — so that one canonical sprint-state source (`sprints/index.json` with its `active`, `planning`, `completed[]`, `quickfixes[]` sections) governs all readers and writers, sprint-dev can initialize against the active sprint without halting on a missing file, sprint-manager actions match what `momentum-tools.py` actually writes, the architecture document reflects the implementation rather than a never-built design, and a new decision document (DEC-012) records the reconciliation so future contributors find the decision trail.

## Description

**Defect class.** Two-source-of-truth contract drift between the spec stack and the implementation. The implementation has always written one holistic file (`sprints/index.json`); the spec stack — across two skill workflows and three sections of `architecture.md` — has continued to describe a never-built per-sprint file (`sprints/{slug}.json`). DEC-011 D3 ("State Source Paths Under `.momentum/`") narrowed what the **canvas** reads to the holistic index, but it never explicitly retired the per-sprint file pattern at the architecture level. This story closes that gap with a formal decision record and aligns all four artifacts to one canonical state source.

**Observed behavior.** The per-sprint file pattern appears in five places across the spec stack despite never having been written by the implementation:

- `skills/momentum/skills/sprint-dev/workflow.md` — Phase 1 instructs "Read the per-sprint record: `sprints/{{sprint_slug}}.json`" (line 141) and derives `{{sprint_dependencies}}` from a `dependencies` field on that record (line 151). Neither the file nor the field exist. Sprint-dev cannot proceed past Phase 1 against the active `sprint-2026-04-27`.
- `skills/momentum/skills/sprint-manager/workflow.md` — three procedure steps (`sprint_activate` step 8 ~line 75, `sprint_complete` step 6 ~line 95, `sprint_plan` step 7 ~line 137) instruct writing to `sprints/{slug}.json`. The actual writer (`momentum-tools.py` `cmd_sprint_activate` lines 133–152, plus parallel paths) only ever writes `sprints/index.json`.
- `_bmad-output/planning-artifacts/architecture.md` — three sections still describe the per-sprint file as canonical: the Read/Write Authority table at line 1320 lists `momentum-tools sprint` as the sole writer of `.momentum/sprints/{slug}.json`; the Protection Boundaries list at line 1347 includes the per-sprint file path; the Sprint Tracking Schema at line 1526 describes the `.momentum/sprints/` folder as "one file per sprint" containing the per-sprint state contents.

**Diagnostic signal.** The on-disk evidence is unambiguous: `ls _bmad-output/implementation-artifacts/sprints/*.json` returns only `index.json` — no per-sprint file exists for `sprint-2026-04-27` or any prior sprint, and none has ever been written. The `active` block of `sprints/index.json` already contains every field sprint-dev needs (`slug`, `status`, `locked`, `stories`, `waves`, `team.story_assignments`, `planned`). It does not contain a `dependencies` field — and should not — because ordering is expressed by `waves` (story in wave N runs after wave N-1) and per-story `depends_on` lives in `stories/index.json`.

**Root cause.** Both workflow files and the three architecture sections were authored against an earlier design that envisioned a per-sprint record file alongside an index. That design was abandoned in favor of single-holistic-state, and the implementation in `momentum-tools.py` matches the holistic-state design. DEC-011 D3 partially documented this for the canvas but stopped short of formally retiring the per-sprint file pattern at the state-model level. The two skill workflow specs and three architecture sections were never updated to match.

**Why expanded scope (vs. original two-file fix).** The original story scope (workflow.md edits only) was based on a reading of DEC-011 D3 as having retired the per-sprint file. Architecture review surfaced that DEC-011 D3 only specifies what the **canvas** reads, not the underlying state model — leaving the per-sprint file design alive in three architecture.md sections. Fixing only the workflows would re-create drift the next time someone reads architecture.md and re-introduces the per-sprint file pattern into a workflow. The clean fix is to formally retire the pattern: author DEC-012 as the explicit retirement record, update architecture.md to match, then update the two workflows. All four edits are one coherent reconciliation.

**Fix shape.** Four scope-isolated artifact updates that together reconcile the spec stack to the implementation:

1. New decision document **DEC-012** at `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` formally retires the per-sprint file pattern. The holistic `sprints/index.json` is the canonical sprint state source. Per-sprint **subdirectories** (`{slug}/specs/`, `{slug}/sprint-summary.md`, `{slug}/retro-transcript-audit.md`, `{slug}/audit-extracts/`) remain — only the per-slug **JSON file** is retired.
2. `architecture.md` is updated in three sections to reflect the new authority model and reference DEC-012; a new `meta.cycles` (editHistory) entry captures the change.
3. `skills/momentum/skills/sprint-dev/workflow.md` reads from `sprints/index.json` `active` block; derives ordering from `active.waves` and per-story `depends_on` in `stories/index.json`; references DEC-012 inline so future contributors find the decision.
4. `skills/momentum/skills/sprint-manager/workflow.md` deletes the three obsolete per-sprint-write steps; references DEC-012 inline at the top of the file.

After the fix, sprint-dev can resume Wave 1 of `sprint-2026-04-27` on the sprint branch without Phase 1 halting; sprint-manager's specified procedures exactly match what `momentum-tools.py` already does; architecture.md describes the implementation rather than an unbuilt design; DEC-012 stands as the durable record of the reconciliation.

**Source pain.** Discovered while attempting to run sprint-dev against the active `sprint-2026-04-27`: Phase 1 step "Read the per-sprint record: `sprints/{{sprint_slug}}.json`" failed because the file does not exist. Investigation against `momentum-tools.py` confirmed the file has never been written. Subsequent architecture review surfaced that the per-sprint file pattern is still alive in three architecture.md sections — meaning the original two-file fix would have left the spec stack internally inconsistent. Expanded scope addresses the full reconciliation.

**Out of scope.** The 21 files referencing legacy `_bmad-output/implementation-artifacts/...` paths for sprint state are addressed by Wave 1 of `sprint-2026-04-27` (story `impetus-momentum-state-migration`, Task 5). Those are path-prefix updates, not contract drift, and intentionally land separately. This story changes contract semantics (which file, which fields) — not the path prefix. Per-sprint **subdirectories** (`{slug}/specs/`, `{slug}/sprint-summary.md`, retro artifacts) are explicitly preserved and out of scope for retirement.

**Why permanent.** DEC-012 makes the holistic-state direction explicit and durable at the architecture level, not implicit at the canvas-read level. With the decision recorded, the architecture matched, and the workflows aligned, the next contributor cannot re-introduce the per-sprint file pattern without either contradicting an ADOPTED decision or re-editing all three artifacts. The Wave 1 path migration (`sprints/index.json` → `.momentum/sprints/index.json`) preserves the `active` block shape and the `index.json` filename, so this fix survives the migration intact.

## Acceptance Criteria

1. **sprint-dev Phase 1 initialization succeeds against `sprints/index.json` alone, on the sprint branch.** When `momentum:sprint-dev` is invoked against the currently active sprint (`sprint-2026-04-27`), Phase 1 (Initialization) — running on the `sprint/{sprint_slug}` branch (per the existing `git checkout sprint/{{sprint_slug}}` step in workflow.md line 138, which this story preserves) — reaches the end of the step without halting on a missing file. The workflow reads `sprints/index.json`, binds `{{sprint_record}}` to its `active` block, verifies `active.slug == {{sprint_slug}}`, verifies `active.locked == true` (or equivalent activation check), and proceeds to dependency-graph construction. No reference to or read of `sprints/{slug}.json` occurs.

2. **sprint-dev derives wave ordering and per-story dependencies from the correct sources.** The workflow's dependency-graph step constructs the execution order from two sources, in this order of precedence:
   - Primary ordering: `active.waves` from `sprints/index.json` (a story in wave N is blocked until every story in wave N-1 has status `done`).
   - Secondary detail: per-story `depends_on` arrays from `stories/index.json` (used to detect cross-wave or intra-wave dependencies the wave grouping does not already imply).
   The workflow does not reference a `dependencies` object on the sprint record, because no such object exists on the holistic state by design. Wave 1 of the active sprint (containing the single story `impetus-momentum-state-migration`) is correctly identified as unblocked at start; wave-2 stories are correctly identified as blocked until wave-1 completes.

3. **sprint-dev's `<critical>` contract block reflects the new sources.** The first `<critical>` directive at the top of `skills/momentum/skills/sprint-dev/workflow.md` is rewritten to instruct that sprint-dev reads from `sprints/index.json` `active` block (for team, waves, and story_assignments) and from `stories/index.json` (for per-story `depends_on`). No mention of `sprints/{slug}.json` remains in the file. The directive carries a brief inline reference to DEC-012 so future contributors can locate the decision record.

4. **sprint-dev's HALT message is correct after the change.** Any HALT or error-output prose in Phase 1 that mentioned the per-sprint file is rewritten to reference the actual source (`sprints/index.json` `active` block) and the actual failure modes (missing `active`, `active.slug` mismatch, `active.locked == false`, etc.). The diagnostic remains actionable and points to the real file the user can inspect.

5. **sprint-manager workflow.md no longer instructs writes to the per-sprint file in any procedure.** All three procedure steps that currently instruct writing to `sprints/{slug}.json` are removed:
   - `sprint_activate` step 8 ("If a sprint file exists at `sprints/{slug}.json`, update it...") — deleted.
   - `sprint_complete` step 6 ("Update the sprint file at `sprints/{slug}.json` with the `completed` date") — deleted.
   - `sprint_plan` step 7 ("Update or create the sprint file at `sprints/{slug}.json` to match") — deleted.
   The remaining steps in each procedure still produce a complete, in-order procedure that ends with the JSON return contract. Step renumbering is consistent. Each procedure's behavior, after the deletions, exactly matches what `momentum-tools.py` already does. A brief inline reference to DEC-012 appears near the top of the file so future contributors find the decision record.

6. **No new file references to `sprints/{slug}.json` are introduced anywhere in the two touched workflow files.** A grep for `sprints/{slug}.json` and `sprints/{{sprint_slug}}.json` (and any close variant such as `sprints/<slug>.json`) across `skills/momentum/skills/sprint-dev/workflow.md` and `skills/momentum/skills/sprint-manager/workflow.md` returns zero matches after the fix.

7. **DEC-012 exists as a well-formed decision document and records the retirement.** `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` exists and follows the same structural conventions as existing decision documents in `decisions/` (frontmatter with `id`, `title`, `date`, `status`, `source_research`, `prior_decisions_reviewed`, `stories_affected`; body sections covering Summary, Decision(s) with embedded Rationale, Status with Supersedes line, Consequences, Cross-references, Implementation Impact — section names may vary as long as the substantive content below is present). It contains the following substantive content:
   - **Decision:** Retire the `.momentum/sprints/{slug}.json` per-sprint state file pattern. The holistic `sprints/index.json` (with `active`, `planning`, `completed[]`, `quickfixes[]` sections) is the canonical sprint state source. Per-sprint subdirectories (`{slug}/specs/`, `{slug}/sprint-summary.md`, retro artifacts) remain — only the per-slug JSON file is retired.
   - **Rationale:** The implementation (`momentum-tools.py` `cmd_sprint_activate` lines 133–152 and parallel paths) has never written this file. The holistic record already carries everything the per-sprint file was designed to hold (team composition, waves, story_assignments, dates, per-story approvals). Two sources of truth would invite drift; one source eliminates it.
   - **Status:** ADOPTED (developer Steve Holmes, 2026-04-30).
   - **Supersedes:** none — clarifies a state-model question DEC-011 D3 left ambiguous.
   - **Cross-references:** DEC-011 D3 (canvas reads from holistic index, not per-sprint file).
   - **Implementation impact:** lists the four touches in this story (two workflows, architecture.md, this decision document) so the decision points back at its enacting story.

8. **Architecture.md is updated to reflect the new authority model in three sections, and references DEC-012 in each.**
   - **Read/Write Authority table (line 1320):** the `momentum-tools sprint` row's "Writes" column no longer lists `.momentum/sprints/{slug}.json`. The remaining write authority covers `.momentum/stories/index.json` (status fields) and `.momentum/sprints/index.json`. A short inline note (or footnote-style reference) cites DEC-012 as the source for the change.
   - **Protection Boundaries list (line 1347):** the entry for sole-writer protection on `.momentum/sprints/{slug}.json` is removed. The remaining entry preserves protection on `.momentum/stories/index.json` and `.momentum/sprints/index.json` with `momentum-tools.py sprint` as the sole writer. A short inline note cites DEC-012.
   - **Sprint Tracking Schema (line 1526):** the `.momentum/sprints/` folder description is rewritten to remove "one file per sprint (`.momentum/sprints/{slug}.json`)" language. The new prose clarifies that `.momentum/sprints/` contains one canonical state file (`index.json`) with `active`, `planning`, `completed[]`, `quickfixes[]` sections, and one per-sprint **subdirectory** (`.momentum/sprints/{slug}/`) per sprint for `specs/`, `sprint-summary.md`, retro-transcript-audit.md, and `audit-extracts/`. The subdirectory structure tree (lines 1528+) is preserved unchanged. A short inline note cites DEC-012.

9. **Architecture.md `editHistory` (meta.cycles) carries a new entry capturing the change.** A new entry dated 2026-04-30 is prepended to the `editHistory:` list in the frontmatter. The entry describes the per-sprint file retirement, references DEC-012, and lists the three sections updated. Format matches existing entries in the list (date + free-form changes string).

10. **DEC-012 is referenced from all enacting artifacts.** A grep for `dec-012` (case-insensitive) across the four touched files returns at least one match in each: the new decision document itself, `architecture.md` (in each of the three updated sections plus the new editHistory entry), `sprint-dev/workflow.md` (in or near the rewritten `<critical>` directive), and `sprint-manager/workflow.md` (in the file-level header or near the procedure changes). This ensures the decision trail is discoverable from any of the enacting artifacts.

11. **Behavioral evals confirm the workflow-level fix.** Two `.md` evals in `skills/momentum/skills/sprint-dev/evals/` (created if the directory does not exist) confirm:
    - `eval-sprint-dev-reads-active-block-only.md`: Given a workspace where `sprints/index.json` has a populated `active` block and no per-sprint file exists on disk, the sprint-dev workflow's Phase 1 binds the sprint record to `active`, verifies its slug, and proceeds without halting. Satisfied if a subagent loaded with the updated `workflow.md` describes Phase 1 reading only `sprints/index.json` and never attempting to read `sprints/{slug}.json`.
    - `eval-sprint-dev-derives-ordering-from-waves.md`: Given a sprint record with two waves (wave 1: 1 story; wave 2: 7 stories), the workflow identifies the wave-1 story as initially unblocked and the wave-2 stories as blocked on wave-1 completion. The subagent's described dependency graph reflects this without referencing any `dependencies` field on the sprint record.
    Both evals follow the EDD protocol described in the Momentum Implementation Guide section below; they test described behavior, not exact prose.

12. **Format and NFR compliance preserved across all four files.**
    - Each touched workflow.md remains a valid Momentum workflow file: `<workflow>` / `<critical>` / `<step>` XML structure preserved and well-formed; SKILL.md siblings unmodified; body length within Momentum's skill-instruction conventions; internal cross-references resolve.
    - `architecture.md` remains valid markdown with intact frontmatter (parses as YAML); the editHistory list remains chronological at the top (newest first, matching existing convention); table formatting in the Read/Write Authority section remains valid markdown.
    - DEC-012 file follows the structural conventions of existing decisions in `_bmad-output/planning-artifacts/decisions/` (frontmatter present, sectioning consistent with siblings, filename pattern `dec-NNN-{slug}-{YYYY-MM-DD}.md`).

13. **AVFL checkpoint passes (or known issues documented).** The post-implementation AVFL checkpoint on each touched file produces either CLEAN or a CHECKPOINT_WARNING with each finding either resolved or documented in the Dev Agent Record with a specific reason it is acceptable to defer. No GATE_FAILED result is left unaddressed.

## Tasks / Subtasks

- [ ] **Task 1 — Re-read source-of-truth artifacts and confirm the contract** (AC: 1, 2, 3, 4, 5, 7, 8) — `skill-instruction` + `specification`
  - [ ] Subtask 1.1: Read `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` Decision D3. Confirm its scope is canvas-reads, not state-model retirement, and note this in the Dev Agent Record `Debug Log References` as the rationale for authoring DEC-012.
  - [ ] Subtask 1.2: Read `skills/momentum/scripts/momentum-tools.py` lines 133–200 (covering `cmd_sprint_activate`, `cmd_sprint_complete`, and any planning-related sprint mutations). Confirm — and note in Dev Agent Record — that the implementation only ever reads/writes `sprints/index.json` and never `sprints/{slug}.json`. Identify the exact sprint-manager procedure steps whose deletion is justified by this implementation behavior.
  - [ ] Subtask 1.3: Read `_bmad-output/implementation-artifacts/sprints/index.json` and confirm the live `active` block shape: `slug`, `status`, `locked`, `stories`, `waves`, `team.story_assignments`, `planned`. Confirm there is no `dependencies` field. Use this confirmed shape as the basis for the rewritten sprint-dev step.
  - [ ] Subtask 1.4: List `_bmad-output/planning-artifacts/decisions/` to confirm the highest current decision number is 011 and DEC-012 is the correct next number. Confirm the date 2026-04-30 for the filename.
  - [ ] Subtask 1.5: Read `_bmad-output/planning-artifacts/architecture.md` lines 1310–1360, 1480–1545 (and surrounding context) to confirm the three sections that must be updated still match the line ranges in this story (line numbers may have shifted slightly between story authoring and dev start; confirm by content match, not line number). Note the current `editHistory:` entry format for the new entry to match.

- [ ] **Task 2 — Author DEC-012 decision document** (AC: 7, 10, 12) — `specification`
  - [ ] Subtask 2.1: Create `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md`. Use sibling decisions (especially `dec-011-project-canvas-implementation-foundations-2026-04-24.md`) as the structural template — match frontmatter shape, section headings, and prose tone.
  - [ ] Subtask 2.2: Write the Decision section — explicit retirement of `.momentum/sprints/{slug}.json` per-sprint state file pattern; canonical state in `sprints/index.json` (`active`, `planning`, `completed[]`, `quickfixes[]`); per-sprint **subdirectories** (`{slug}/specs/`, `{slug}/sprint-summary.md`, retro artifacts) preserved.
  - [ ] Subtask 2.3: Write the Rationale section — implementation never wrote the file; holistic record carries every field the per-sprint file was designed to hold; one source eliminates drift.
  - [ ] Subtask 2.4: Write Status (ADOPTED, Steve Holmes, 2026-04-30), Supersedes (none — clarifies DEC-011 D3 ambiguity), Cross-references (DEC-011 D3).
  - [ ] Subtask 2.5: Write an Implementation Impact section listing the four enacting touches in this story so the decision is discoverable from its implementation artifacts.

- [ ] **Task 3 — Update architecture.md (three sections + editHistory)** (AC: 8, 9, 10, 12) — `specification`
  - [ ] Subtask 3.1: Update the Read/Write Authority table row for `momentum-tools sprint` (currently around line 1320) — remove `.momentum/sprints/{slug}.json` from the Writes column; preserve the rest of the row; add a short inline DEC-012 reference (e.g., a parenthetical or footnote-style note).
  - [ ] Subtask 3.2: Update the Protection Boundaries list (currently around line 1347) — remove the per-sprint file path entry; preserve the entry covering `stories/index.json` and `sprints/index.json`; add a short inline DEC-012 reference.
  - [ ] Subtask 3.3: Rewrite the Sprint Tracking Schema `.momentum/sprints/` folder description (currently around line 1526) — remove "one file per sprint (`.momentum/sprints/{slug}.json`)" language; describe one canonical state file (`index.json`) with sectioned blocks; describe per-sprint **subdirectories** for specs/sprint-summary/retro/audit-extracts; preserve the per-sprint folder structure tree below it unchanged; add a short inline DEC-012 reference.
  - [ ] Subtask 3.4: Prepend a new `editHistory:` entry dated 2026-04-30 to the frontmatter list, describing the per-sprint file retirement, citing DEC-012, and listing the three updated sections. Match existing entry format (date + free-form changes string).
  - [ ] Subtask 3.5: Verify by inspection — grep for `sprints/{slug}.json` across architecture.md after edits. Document the remaining matches (if any are intentional — e.g., in historical editHistory entries — note why).

- [ ] **Task 4 — Fix `skills/momentum/skills/sprint-dev/workflow.md`** (AC: 1, 2, 3, 4, 6, 10, 12) — `skill-instruction`
  - [ ] Subtask 4.1: Update the first `<critical>` directive (currently around line 12) so it instructs sprint-dev to read from `sprints/index.json` `active` block (team, waves, story_assignments) and from `stories/index.json` (per-story `depends_on`). Remove the phrase "the per-sprint record from `sprints/{slug}.json`" entirely. Add a brief inline DEC-012 reference.
  - [ ] Subtask 4.2: Replace the Phase 1 step (currently around line 141) that says `Read the per-sprint record: sprints/{{sprint_slug}}.json` with: read `sprints/index.json` and bind `{{sprint_record}}` to its `active` block. Add an explicit verification step that `active.slug == {{sprint_slug}}` before proceeding (HALT with a specific message if not). Preserve the existing `git checkout sprint/{{sprint_slug}}` step (line 138) — Phase 1 runs on the sprint branch.
  - [ ] Subtask 4.3: Replace the line (currently around line 151) that sets `{{sprint_dependencies}} = dependencies object from the sprint record`. There is no `dependencies` field by design. Replace with two derivation steps: derive primary ordering from `active.waves` (a story in wave N is blocked until every wave-(N-1) story is `done`); load per-story `depends_on` from `stories/index.json` for cross-wave detail. Both sources combine into the existing dependency-graph variable used downstream.
  - [ ] Subtask 4.4: Update the dependency-graph construction step (currently around line 175) so its prose references the new derivation source (waves + stories/index.json `depends_on`), not `{{sprint_dependencies}}` from a per-sprint record.
  - [ ] Subtask 4.5: Update any HALT or error message in Phase 1 that still mentions the per-sprint file. Rewrite it to reflect realistic failure modes against the new sources (missing `active`, slug mismatch, `active.locked == false`, etc.).
  - [ ] Subtask 4.6: Verify by inspection: grep for `sprints/{slug}.json` and `sprints/{{sprint_slug}}.json` in the file. The grep must return zero matches.

- [ ] **Task 5 — Fix `skills/momentum/skills/sprint-manager/workflow.md`** (AC: 5, 6, 10, 12) — `skill-instruction`
  - [ ] Subtask 5.1: In the `sprint_activate` procedure (currently around line 75), delete step 8 ("If a sprint file exists at `sprints/{slug}.json`, update it..."). Renumber subsequent steps if any; ensure the procedure still ends with the JSON return contract.
  - [ ] Subtask 5.2: In the `sprint_complete` procedure (currently around line 95), delete step 6 ("Update the sprint file at `sprints/{slug}.json` with the `completed` date"). Renumber subsequent steps if any; preserve the JSON return contract.
  - [ ] Subtask 5.3: In the `sprint_plan` procedure (currently around line 137), delete step 7 ("Update or create the sprint file at `sprints/{slug}.json` to match"). Renumber subsequent steps if any; preserve the JSON return contract.
  - [ ] Subtask 5.4: Add a brief inline DEC-012 reference near the top of the file (e.g., in the file-level summary or in a new note line above the first procedure) so future contributors find the decision trail.
  - [ ] Subtask 5.5: Verify by inspection: grep for `sprints/{slug}.json` in the file. The grep must return zero matches.
  - [ ] Subtask 5.6: Re-read each updated procedure end-to-end to confirm the remaining steps form a complete, in-order procedure that exactly matches what `momentum-tools.py` already does for that command.

- [ ] **Task 6 — Behavioral evals for sprint-dev** (AC: 11) — `skill-instruction`
  - [ ] Subtask 6.1: Create `skills/momentum/skills/sprint-dev/evals/` if it does not exist.
  - [ ] Subtask 6.2: Add `eval-sprint-dev-reads-active-block-only.md`: "Given a workspace where `sprints/index.json` contains a populated `active` block and no `sprints/{slug}.json` exists on disk, the sprint-dev workflow's Phase 1 should bind the sprint record to `active`, verify `active.slug == sprint_slug`, and proceed to dependency-graph construction — without ever reading or referencing `sprints/{slug}.json`."
  - [ ] Subtask 6.3: Add `eval-sprint-dev-derives-ordering-from-waves.md`: "Given a sprint record whose `active.waves` is `[{wave: 1, stories: [s1]}, {wave: 2, stories: [s2, s3, s4]}]`, the workflow should identify s1 as initially unblocked and s2/s3/s4 as blocked on wave-1 completion. The dependency derivation should describe `active.waves` as the primary ordering source and `stories/index.json` `depends_on` as the cross-wave detail source — never a `dependencies` field on the sprint record."
  - [ ] Subtask 6.4: Run both evals per the EDD protocol below. Document results in the Dev Agent Record.

- [ ] **Task 7 — Cross-reference and close-out** (AC: all) — `skill-instruction` + `specification`
  - [ ] Subtask 7.1: In the Dev Agent Record `Completion Notes`, cite Decision D3 of `dec-011-project-canvas-implementation-foundations-2026-04-24.md`, the new DEC-012 decision document, and the actual writer behavior in `momentum-tools.py` (`cmd_sprint_activate`, `cmd_sprint_complete`, planning paths) as the source-of-truth chain this story aligns the spec stack to.
  - [ ] Subtask 7.2: Note the relationship to Wave 1 of `sprint-2026-04-27` (story `impetus-momentum-state-migration`, Task 5): the 21 files referencing legacy `_bmad-output/implementation-artifacts/...` paths are out of scope for this story. This story changes contract semantics across four artifacts; the migration story changes path prefixes elsewhere. The two are independent and survive together because the `active` block shape and the `index.json` filename are preserved by the migration.
  - [ ] Subtask 7.3: Run a final grep across the four touched files for `sprints/{slug}.json`, `sprints/{{sprint_slug}}.json`, and `sprints/<slug>.json`. Document the result. Document the per-file `dec-012` grep results required by AC10.

## Dev Notes

### Why expanded scope (architecture-discovery finding)

The original story scope (workflow.md edits only) was based on a reading of DEC-011 D3 as having retired the per-sprint file pattern. Architecture review during Phase 1 of `momentum:quick-fix` surfaced that DEC-011 D3 is narrower than that — it specifies what the **canvas** reads, not the underlying state model. The per-sprint file design remained alive in three sections of `architecture.md`:

- Read/Write Authority table (line 1320) — listed `momentum-tools sprint` as sole writer of `.momentum/sprints/{slug}.json`.
- Protection Boundaries (line 1347) — included the per-sprint file path as a hook-protected sole-writer target.
- Sprint Tracking Schema (line 1526) — described the `.momentum/sprints/` folder as containing "one file per sprint" holding the per-sprint state contents.

Meanwhile the actual implementation in `momentum-tools.py` (`cmd_sprint_activate` lines 133–152) has never written a per-sprint file — only `sprints/index.json`. The per-sprint design has lived only in the spec stack, never in code.

The original two-file workflow.md fix would have left `architecture.md` describing a state model the workflows no longer follow — recreating drift the next time someone reads architecture.md and re-introduces the per-sprint pattern into a workflow. The expanded scope formally retires the pattern via a new decision document (DEC-012), updates architecture.md to match, then aligns the two workflows. All four edits are one coherent reconciliation of the spec stack to the implementation.

### Architecture Compliance

- **Decision D3 of dec-011-project-canvas-implementation-foundations-2026-04-24** — Sprint state lives in a single holistic file (`sprints/index.json`, relocating to `.momentum/sprints/index.json` post Wave 1). This story builds on D3 by formally retiring the per-sprint file at the state-model level (DEC-012), not just at the canvas-read level.
  - Source: `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` Decision D3.
- **DEC-012 (new, this story)** — Formal retirement of `.momentum/sprints/{slug}.json`. The holistic `sprints/index.json` is the canonical sprint state source. Per-sprint subdirectories preserved.
  - Source: `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` (created by Task 2).
- **Implementation parity (`momentum-tools.py`)** — `cmd_sprint_activate` (lines 133–152) only reads/writes `sprints/index.json`. Parallel `cmd_sprint_complete` and planning paths follow the same convention. The sprint-manager spec must match the implementation exactly because sprint-manager is the spec for the executor wrapping these commands.
  - Source: `skills/momentum/scripts/momentum-tools.py` lines 133–200.
- **Wave 1 state migration relationship** — `impetus-momentum-state-migration` (Wave 1 of `sprint-2026-04-27`, Task 5) relocates path prefixes from `_bmad-output/implementation-artifacts/...` to `.momentum/...`. That story does not change contract semantics; this story does not change path prefixes. The two are orthogonal and survive together because the `active` block shape and the `index.json` filename are preserved by the migration.
  - Source: `_bmad-output/implementation-artifacts/stories/impetus-momentum-state-migration.md` Task 5.
- **Decision 30 (Black-box separation)** — N/A in mechanics. This story does not touch `sprints/{slug}/specs/` directories or any Gherkin feature files. The dev agent does not read or write `.feature` files for this story.

### Files Being Modified (state and constraints)

- `skills/momentum/skills/sprint-dev/workflow.md` — currently 200+ lines; this story modifies the first `<critical>` directive, the Phase 1 read step (~line 141), the dependency-source step (~line 151), the dependency-graph build step (~line 175), and any HALT message in Phase 1 that mentions the per-sprint file. Phases 2–7 and the `<team-composition>` block are not modified.
- `skills/momentum/skills/sprint-manager/workflow.md` — currently 149 lines; this story deletes one step from each of three procedures and adds one brief DEC-012 reference near the top. Remaining sections (Input Format, Output Format, `status_transition`, `epic_membership`, Critical Rules) are not modified. JSON return contracts must be preserved.
- `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` — new file; structurally matches `dec-011-...` and other siblings; ~50–120 lines expected.
- `_bmad-output/planning-artifacts/architecture.md` — currently 2819 lines; this story modifies one row in the Read/Write Authority table (~line 1320), one entry in the Protection Boundaries list (~line 1347), one paragraph in the Sprint Tracking Schema (~line 1526), and prepends one new `editHistory:` entry at the top. Surrounding context (table headers, other rows, other boundaries, the per-sprint folder structure tree at lines 1528+) is preserved unchanged.

What must be preserved end-to-end:
- sprint-dev's Phase 2–7 logic (dev wave, progress tracking, AVFL, code review, fix queue, team review, completion) — out of scope.
- sprint-manager's `status_transition` and `epic_membership` actions and the Critical Rules section — out of scope.
- Architecture.md sections outside the three named here — out of scope.
- The `momentum-tools.py` script — not modified by this story. The implementation is already correct; the spec is what changes.

### Testing Requirements

EDD (Eval-Driven Development) applies to the two workflow.md updates because they are SKILL workflow files. No unit tests apply; behavioral evals replace them. See the Momentum Implementation Guide section below for the full EDD protocol and DoD.

The DEC-012 authoring and architecture.md updates are `specification` change-type — no evals required; AVFL checkpoint and AC verification (especially AC7, AC8, AC9, AC10) cover quality.

- 2 behavioral evals in `skills/momentum/skills/sprint-dev/evals/`:
  1. `eval-sprint-dev-reads-active-block-only.md` — verifies Phase 1 binds to `active` and never reads `sprints/{slug}.json`.
  2. `eval-sprint-dev-derives-ordering-from-waves.md` — verifies wave-based ordering derivation with `stories/index.json` `depends_on` as cross-wave detail.
- No evals for `sprint-manager/workflow.md` (purely deletion + one-line reference; AC5/AC6/AC10 grep + AC12 structural-integrity check are sufficient).
- No evals for the decision document or architecture.md (specification artifacts; AC verification + AVFL checkpoint cover quality).

### Project Context Reference

- `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` (Decision D3) — clarifies what the canvas reads; this story explicitly retires the per-sprint file pattern that D3 left ambiguous.
- `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` (created by this story, Task 2) — the formal retirement record.
- `_bmad-output/planning-artifacts/architecture.md` — three sections updated by this story:
  - Read/Write Authority table at ~line 1320 (`momentum-tools sprint` row).
  - Protection Boundaries list at ~line 1347 (per-sprint file entry).
  - Sprint Tracking Schema at ~line 1526 (`.momentum/sprints/` folder description).
  - `editHistory:` (frontmatter, top of file) — new entry prepended.
- `skills/momentum/scripts/momentum-tools.py` (lines 133–200) — authoritative source for what the implementation actually writes.
- `_bmad-output/implementation-artifacts/sprints/index.json` (the `active` block) — authoritative source for the live shape this fix targets.
- `_bmad-output/implementation-artifacts/stories/impetus-momentum-state-migration.md` (Task 5) — out-of-scope reference for the legacy-path-prefix migration that lands separately in Wave 1.

## Dev Agent Record

### Context Reference

- `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md`
- `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` (created by Task 2)
- `_bmad-output/planning-artifacts/architecture.md` (lines ~1320, ~1347, ~1526 + frontmatter editHistory)
- `skills/momentum/scripts/momentum-tools.py`
- `_bmad-output/implementation-artifacts/sprints/index.json`
- `_bmad-output/implementation-artifacts/stories/impetus-momentum-state-migration.md`

### Agent Model Used

_To be filled by dev agent._

### Debug Log References

_To be filled by dev agent. Required: note that DEC-011 D3 is canvas-read scope only (justifying DEC-012 authoring); confirm momentum-tools.py never writes per-sprint file._

### Completion Notes

_To be filled by dev agent. Required: cite DEC-011 D3, cite DEC-012 (created), cite `momentum-tools.py` implementation, document grep zero-match result on workflow files, document `dec-012` reference present in all four touched files, document EDD eval results, note relationship with `impetus-momentum-state-migration` Task 5._

### File List

_To be filled by dev agent. Expected: two files modified (`skills/momentum/skills/sprint-dev/workflow.md`, `skills/momentum/skills/sprint-manager/workflow.md`); one file modified (`_bmad-output/planning-artifacts/architecture.md`); one file created (`_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md`); two files created (`skills/momentum/skills/sprint-dev/evals/eval-sprint-dev-reads-active-block-only.md`, `skills/momentum/skills/sprint-dev/evals/eval-sprint-dev-derives-ordering-from-waves.md`)._

### Change Log

_To be filled by dev agent._

---

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 4, 5, 6 → skill-instruction (EDD applies to the two workflow.md updates and the evals)
- Tasks 1, 2, 3 → specification (DEC-012 authoring + architecture.md updates; AVFL checkpoint covers quality)
- Task 7 → cross-cutting close-out (touches both classifications)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-dev/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-sprint-dev-reads-active-block-only.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) [N/A for this story — no SKILL.md files are modified, only workflow.md]
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23) [N/A — no SKILL.md changes]
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3) [N/A]
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills) [N/A — no new skills]

**Note on this story specifically:** Both touched workflow files are `workflow.md` (not SKILL.md). The NFR items above apply to SKILL.md files; preserve existing SKILL.md frontmatter unchanged. Workflow.md files have no character or token caps but should follow the existing XML-style structure (`<workflow>`, `<critical>`, `<step>`).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2 behavioral evals written in `skills/momentum/skills/sprint-dev/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

---

### specification Tasks: Spec-Quality Verification

**No EDD or TDD applies to specification artifacts (decision documents, architecture.md sections).** Quality is verified by:

1. **AC verification** — each AC for the spec change (AC7, AC8, AC9, AC10 in this story) is satisfied by inspection.
2. **Structural conformance** — DEC-012 follows sibling decision-doc structure; architecture.md edits preserve table validity, frontmatter validity (parses as YAML), and editHistory chronological order.
3. **Cross-reference integrity** — DEC-012 is discoverable from each enacting artifact (AC10 grep). DEC-011 D3 is cited from DEC-012 as supersedes/clarifies linkage.
4. **AVFL checkpoint** — post-implementation AVFL on the modified architecture.md and the new DEC-012 file produces CLEAN or addressed CHECKPOINT_WARNING.

**DoD items for specification tasks:**
- [ ] DEC-012 file created and structurally matches sibling decisions
- [ ] All three architecture.md sections updated and reference DEC-012
- [ ] New `editHistory:` entry prepended (date 2026-04-30, cites DEC-012, lists three updated sections)
- [ ] `dec-012` grep returns at least one match in each of the four touched files
- [ ] AVFL checkpoint documented for architecture.md and DEC-012

---

### Gherkin Specs Reminder (Decision 30 — Black-Box Separation)

If Gherkin specs exist for this sprint at `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/specs/`, they are **off-limits to the dev agent**. The dev agent implements against the plain-English Acceptance Criteria in this story file only — never against `.feature` files. This black-box separation prevents the dev agent from "teaching to the test" and preserves independent verification by the QA reviewer in Phase 5 of sprint-dev.
