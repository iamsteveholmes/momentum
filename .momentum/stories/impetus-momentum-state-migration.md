---
title: Migrate Impetus State Reads to .momentum/
story_key: impetus-momentum-state-migration
status: ready-for-dev
epic_slug: impetus-core
feature_slug: 
story_type: maintenance
priority: high
depends_on: []
touches:
  - .momentum/sprints/index.json
  - .momentum/stories/index.json
  - .momentum/sprints/
  - .momentum/signals/
  - .momentum/intake-queue.jsonl
  - skills/momentum/skills/impetus/references/orient.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/references/protected-paths.json
  - skills/momentum/references/hooks/file-protection.sh
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/dev/workflow.md
  - skills/momentum/skills/epic-grooming/workflow.md
  - skills/momentum/skills/feature-breakdown/workflow.md
  - skills/momentum/skills/feature-grooming/workflow.md
  - skills/momentum/skills/feature-status/workflow.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/plan-audit/workflow.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/refine/workflow.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-manager/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/triage/workflow.md
  - _bmad-output/planning-artifacts/architecture.md
---

# Story: Migrate Impetus State Reads to .momentum/

Status: ready-for-dev

## Story

As the developer running Momentum,
I want Impetus and every Momentum skill to read sprint and story state from a unified `.momentum/` directory (and a new `.momentum/signals/` ledger),
so that the project canvas and all downstream tooling have a single, stable state source — clearing **DEC-011 Gate G1** for the canvas redesign.

## Context

Per **DEC-011 (Project Canvas Implementation Foundations, 2026-04-24)** Decision D3, all canvas reads are pinned to `.momentum/sprints/index.json`, `.momentum/stories/index.json`, and `.momentum/signals/`. Phase 1 of the canvas (`canvas-vite-scaffold`) is gated on this relocation per **Gate G1**: "Is the Impetus state relocation complete enough to wire against? — `.momentum/sprints/index.json`, `.momentum/stories/index.json`, `.momentum/signals/` directory all exist with stable schemas."

Investigation (performed during story creation) found:

- The `.momentum/` directory does **not** yet exist on disk.
- No separate state-relocation prerequisite story exists in `stories/index.json`. DEC-011's phased plan lists "Phase 0: Impetus state relocation under `.momentum/` (parallel work) — Already in flight" but no concrete story has been created.
- Therefore **this story bundles the full state relocation**: physically relocate state, update every writer (`momentum-tools.py`, hook protection lists), update every reader (Impetus + 14 skill workflows), and define the `.momentum/signals/` schema. Single atomic delivery for Gate G1.
- Existing read paths in `skills/momentum/skills/impetus/references/orient.md` (lines 17–18) hard-code `_bmad-output/implementation-artifacts/sprints/index.json` and `_bmad-output/implementation-artifacts/stories/index.json`. These move to `.momentum/sprints/index.json` and `.momentum/stories/index.json`.
- `momentum-tools.py` is the sole writer; its `stories_path()` and `sprints_path()` helpers (lines 79–84) plus two inline path constructions (lines 1261 and 1346) define every write target and must move together. Adjacent constructions on lines 1260 and 1345 are features.json carve-outs that remain under `_bmad-output/planning-artifacts/` and are intentionally left unchanged.
- 14 skill workflows reference the old paths and must be updated synchronously to maintain the single-state-source invariant (no fallback, no dual reads).
- Architecture.md documents the read/write authority table at lines ~1166–1184 and must be updated to reflect the new canonical paths and the new `signals/` location.

## Acceptance Criteria

1. **Canonical state paths under `.momentum/`.** After this story, `.momentum/sprints/index.json` and `.momentum/stories/index.json` are the canonical state files. The legacy paths `_bmad-output/implementation-artifacts/sprints/index.json` and `_bmad-output/implementation-artifacts/stories/index.json` no longer exist (or are deleted as part of the relocation), and no Momentum code or workflow reads or writes them.

2. **`.momentum/signals/` directory established with schema.** `.momentum/signals/` exists. A schema is documented (in architecture.md and as a `.momentum/signals/README.md` or equivalent) defining: filename pattern, JSON shape, required fields (at minimum: `signal_type`, `origin`, `created`, `payload`), the optional `cleared` field, and the initial set of recognized `signal_type` values: `triage-uncleared`, `avfl-finding-pending-upstream-fix`. Empty directory is a valid state.

3. **Impetus reads from `.momentum/` only.** `skills/momentum/skills/impetus/references/orient.md` references only `.momentum/sprints/index.json`, `.momentum/stories/index.json`, and `.momentum/signals/`. All three reads happen silently at session open — no narration, no user-visible diff. There is no fallback path to `_bmad-output/implementation-artifacts/`. If any of the three sources is missing, Impetus reports state honestly (e.g., "no sprints recorded") rather than silently substituting old paths.

4. **`.momentum/signals/` graceful degradation.** When `.momentum/signals/` is empty or absent, Impetus orientation runs without error and produces a clean situational report (no signals surfaced is a valid case — neither a warning nor a crash).

5. **`momentum-tools.py` writes to `.momentum/`.** `stories_path()`, `sprints_path()`, and the two inline path constructions in `momentum-tools.py` (lines 1261 and 1346 pre-change) all resolve to `.momentum/stories/index.json` and `.momentum/sprints/index.json`. Adjacent lines 1260 and 1345 are features.json carve-outs that stay under `_bmad-output/planning-artifacts/` and are intentionally left unchanged. `python3 skills/momentum/scripts/test-momentum-tools.py` passes against the new paths.

6. **All 15 skill workflows updated synchronously.** Every skill workflow that previously read the old index paths (create-story, dev, epic-grooming, feature-breakdown, feature-grooming, feature-status, intake, plan-audit, quick-fix, refine, retro, sprint-dev, sprint-manager, sprint-planning, triage) reads `.momentum/sprints/index.json` and/or `.momentum/stories/index.json`. No workflow contains a stale `_bmad-output/implementation-artifacts/sprints/index.json` or `_bmad-output/implementation-artifacts/stories/index.json` reference (verifiable via `grep -r`).

7. **Hook protection updated.** `skills/momentum/references/protected-paths.json`, `skills/momentum/references/hooks/file-protection.sh`, `.claude/momentum/protected-paths.json`, and `.claude/momentum/hooks/file-protection.sh` all reference `.momentum/stories/index.json` and `.momentum/sprints/index.json` as the protected paths. The old paths are removed from protection lists (or the lists are cleared entirely if the legacy directory is deleted).

8. **Existing data relocated, not lost.** The current contents of `_bmad-output/implementation-artifacts/sprints/index.json`, `_bmad-output/implementation-artifacts/stories/index.json`, and the per-sprint subdirectories under `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/` (specs, sprint-summary.md, retro artifacts, quickfix records) are present at the new `.momentum/` locations after the migration — `.momentum/sprints/index.json`, `.momentum/stories/index.json`, and `.momentum/sprints/{sprint-slug}/`. Spot-check: every story slug present pre-migration is present post-migration with identical status; the active/planning sprint state is preserved; per-sprint subdirectories present pre-migration are present at `.momentum/sprints/{sprint-slug}/` post-migration with identical contents.

9. **Architecture.md reflects the relocation.** `_bmad-output/planning-artifacts/architecture.md` is updated so the Read/Write Authority table (around lines 1166–1184), the `stories/index.json` and `sprints/index.json` reference sections (around lines 1337, 1389, 1396, 1456), and the Session-open sequence note (around line 572) all use `.momentum/` paths. A new section documents `.momentum/signals/` schema and authority (which skills write signals; default authority: `momentum:retro`, `momentum:triage`, `momentum:avfl`).

10. **End-to-end smoke verification.** After the relocation, running `cmux send`-equivalent `momentum-tools sprint show` (or the sprint-manager `/momentum:sprint-manager status` command), a plan-audit invocation, and Impetus session-open all succeed against the new `.momentum/` paths with no errors. Concretely: `momentum-tools.py` returns the same active/planning sprint as it did pre-migration; Impetus's situational report matches the pre-migration state for the same input.

11. **Single source of truth — no dual writes.** During the migration, the legacy directory is deleted (or moved to a clearly-named archive location outside the read path) so no future write can accidentally split state across two locations. There is no symlink, mirror, or fallback retained.

## Tasks / Subtasks

- [ ] **Task 1 — Define `.momentum/signals/` schema and document it (AC: 2, 9)**
  - [ ] 1.1 Author `.momentum/signals/README.md` (or an equivalent embedded section in architecture.md) defining: filename pattern (`{signal_type}-{slug-or-timestamp}.json`), required JSON fields (`signal_type`, `origin`, `created`, `payload`, optional `cleared`), and initial recognized `signal_type` values (`triage-uncleared`, `avfl-finding-pending-upstream-fix`). Confirm shape is forward-compatible (room for future `signal_type` values without schema change).
  - [ ] 1.2 Add a "`.momentum/` State Sources" subsection to `_bmad-output/planning-artifacts/architecture.md` describing the directory layout (`sprints/`, `stories/`, `signals/`), the relocation from `_bmad-output/implementation-artifacts/`, and which skills write signals (`momentum:retro`, `momentum:triage`, `momentum:avfl` are the expected initial signal-writers; this story does not implement those writers — it only defines the read contract).

- [ ] **Task 2 — Relocate physical state files (AC: 1, 8, 11)**
  - [ ] 2.1 Create `.momentum/sprints/` and `.momentum/stories/` directories.
  - [ ] 2.2 Copy `_bmad-output/implementation-artifacts/sprints/index.json` → `.momentum/sprints/index.json` (preserve byte-for-byte).
  - [ ] 2.3 Copy `_bmad-output/implementation-artifacts/stories/index.json` → `.momentum/stories/index.json` (preserve byte-for-byte).
  - [ ] 2.4 Copy every per-sprint subdirectory under `_bmad-output/implementation-artifacts/sprints/` (e.g., `sprint-2026-04-XX/`, `quickfix-*/`, `phase-3-sprint-execution/`) to `.momentum/sprints/{same-slug}/`, preserving full subtree (specs, sprint-summary.md, retro artifacts, etc.). Verify against `sprints/index.json` entries — every sprint slug referenced in the index should have a corresponding subdirectory copied; flag any orphan subdirectories (present on disk but absent from index) for the developer to decide whether to relocate or leave behind.
  - [ ] 2.5 Copy `_bmad-output/implementation-artifacts/intake-queue.jsonl` → `.momentum/intake-queue.jsonl` if it exists. (If the file is absent, skip — `momentum-tools.py` will create it at the new location on first write.)
  - [ ] 2.6 Verify spot-check: count of story keys in old vs. new `stories/index.json` is identical; `active`, `planning`, `completed`, `quickfixes` arrays in `sprints/index.json` match exactly; per-sprint subdirectories present pre-migration are present post-migration; intake-queue.jsonl line count matches.
  - [ ] 2.7 Create empty `.momentum/signals/` directory with the README from Task 1.
  - [ ] 2.8 After all writers and readers are updated (Tasks 3–5) and tests pass, **delete** `_bmad-output/implementation-artifacts/sprints/`, `_bmad-output/implementation-artifacts/stories/`, and `_bmad-output/implementation-artifacts/intake-queue.jsonl` to enforce single-source-of-truth (AC #11). This deletion is the last step of this task — sequenced after Tasks 3, 4, 5, and 6.

- [ ] **Task 3 — Update `momentum-tools.py` write paths (AC: 5)**
  - [ ] 3.1 Edit `skills/momentum/scripts/momentum-tools.py`:
    - Lines 79–80: `stories_path()` → return `project_dir / ".momentum" / "stories" / "index.json"`.
    - Lines 83–84: `sprints_path()` → return `project_dir / ".momentum" / "sprints" / "index.json"`.
    - Line 1261 (`stories_path_val` in features command): update to `.momentum/stories/index.json`. (Line 1260 is an adjacent features.json carve-out — intentionally left unchanged.)
    - Line 1346 (hash-input section): update to `.momentum/stories/index.json`. (Line 1345 is an adjacent features.json carve-out — intentionally left unchanged.)
    - Line ~1557 (`intake_queue_path()` helper returning `_bmad-output/implementation-artifacts/intake-queue.jsonl`): relocate to `.momentum/intake-queue.jsonl`. The intake queue is implementation-artifacts state (not planning), so it follows the relocation. Migrate the existing file in Task 2 if it exists. This keeps the single-state-source invariant and avoids splitting state between `.momentum/` and the legacy directory. (If the file does not exist on disk, no migration step is needed — the helper just resolves to the new location.)
    - Audit the entire file with `grep -n "_bmad-output\|implementation-artifacts"` and update any other in-script paths that target sprint/story/intake state. **Carve-outs (do not relocate):** `_bmad-output/planning-artifacts/features.json` is planning state, not implementation state — leave it under `_bmad-output/`. Anything else under `_bmad-output/planning-artifacts/` likewise stays put.
  - [ ] 3.2 Run `python3 skills/momentum/scripts/test-momentum-tools.py` and confirm it passes against the new paths. Update test fixtures or path constants in the test file if it hard-codes old paths.

- [ ] **Task 4 — Update Impetus reads (AC: 3, 4)**
  - [ ] 4.1 Edit `skills/momentum/skills/impetus/references/orient.md`:
    - Replace line 17 path with `{project-root}/.momentum/sprints/index.json`.
    - Replace line 18 path with `{project-root}/.momentum/stories/index.json`.
    - Add a third bullet: `{project-root}/.momentum/signals/` — pending work flags (retro-derived). Iterate the directory; if empty, no narration. For each `*.json` signal file, read `signal_type`, `origin`, `payload` and surface as part of orientation context.
    - Add a brief Situational States row for "Pending signals present" → signal "Surface the outstanding signals alongside sprint/story state" — this gives Impetus a recognized state for the new ledger.
  - [ ] 4.2 If `skills/momentum/skills/impetus/SKILL.md` references the old paths, update it. (Current inspection shows it delegates to `references/orient.md`, so no change is expected — verify with `grep`.)
  - [ ] 4.3 Confirm Impetus session-open behavior: silent reads, no fallback to `_bmad-output/implementation-artifacts/`, graceful degradation on empty `.momentum/signals/`.

- [ ] **Task 5 — Update all other skill workflows (AC: 6)**
  - [ ] 5.1 Update each of the following workflow files. Replace every reference to `_bmad-output/implementation-artifacts/sprints/index.json` with `.momentum/sprints/index.json` and every reference to `_bmad-output/implementation-artifacts/stories/index.json` with `.momentum/stories/index.json`. Also replace `{implementation_artifacts}/stories/index.json` and `{implementation_artifacts}/sprints/index.json` with the explicit `.momentum/...` paths (the new path is no longer derived from the `implementation_artifacts` config var):
    - `skills/momentum/skills/create-story/workflow.md` (line 85)
    - `skills/momentum/skills/dev/workflow.md` (lines 29, 35, 120, 121)
    - `skills/momentum/skills/epic-grooming/workflow.md` (lines 28, 132, 133)
    - `skills/momentum/skills/feature-breakdown/workflow.md` (line 129)
    - `skills/momentum/skills/feature-grooming/workflow.md` (lines 16, 50, 190, 228)
    - `skills/momentum/skills/feature-status/workflow.md` (line 14: `stories_path` constant)
    - `skills/momentum/skills/intake/workflow.md` (line 79)
    - `skills/momentum/skills/plan-audit/workflow.md` (lines 67, 81)
    - `skills/momentum/skills/quick-fix/workflow.md` (line 460 — comment block referencing path; update for accuracy)
    - `skills/momentum/skills/refine/workflow.md` (lines 40, 76, 87, 156, 226, 319, 492)
    - `skills/momentum/skills/retro/workflow.md` (lines 58, 188, 531)
    - `skills/momentum/skills/sprint-dev/workflow.md` (lines 125, 153)
    - `skills/momentum/skills/sprint-manager/workflow.md` (uses bare `stories/index.json` / `sprints/index.json` — update inline references and any documentation comments to point at `.momentum/...`; but note that sprint-manager delegates physical writes to `momentum-tools.py` which is already updated in Task 3, so the change here is documentary)
    - `skills/momentum/skills/sprint-planning/workflow.md` (lines 48, 96, 748)
    - `skills/momentum/skills/triage/workflow.md` (verify with `grep`; update any references)
  - [ ] 5.2 Final-pass verification: `grep -rn "_bmad-output/implementation-artifacts/\(sprints\|stories\)/index\.json\|implementation_artifacts.*\(sprints\|stories\)/index\.json" skills/momentum/ .claude/` returns zero matches in workflow.md and SKILL.md files. (Eval files, sprint-logs, and protected-paths protection lists are addressed in Tasks 6 and 7 respectively.)

- [ ] **Task 6 — Update hook protection lists (AC: 7)**
  - [ ] 6.1 Update `skills/momentum/references/protected-paths.json` lines 25 and 30: change patterns to `.momentum/stories/index.json` and `.momentum/sprints/index.json` respectively.
  - [ ] 6.2 Update `skills/momentum/references/hooks/file-protection.sh`:
    - Comment block lines 12–13: update path comments.
    - Array entries lines 99–100: update paths.
    - Conditional matchers lines 195–196 and 200–201: update path string-match conditions.
  - [ ] 6.3 Mirror the same updates to `.claude/momentum/protected-paths.json` and `.claude/momentum/hooks/file-protection.sh` (these are deployed copies of the references files — keeping them in sync is required for the protection hook to actually fire on the correct paths).
  - [ ] 6.4 Verify with `grep -rn "_bmad-output/implementation-artifacts/\(sprints\|stories\)/index\.json" skills/momentum/references/ .claude/momentum/` returns zero matches.

- [ ] **Task 7 — Update architecture.md to reflect the relocation (AC: 9)**
  - [ ] 7.1 Update the Read/Write Authority table (around line 1166–1184): every row that currently lists `stories/index.json` or `sprints/index.json` as a read or write target should clarify the canonical location is `.momentum/stories/index.json` / `.momentum/sprints/index.json`.
  - [ ] 7.2 Update the `stories/index.json` and `sprints/index.json` description sections (around lines 1337, 1389, 1396, 1452, 1456) and the Session-open sequence note (around line 572) to use `.momentum/` paths.
  - [ ] 7.3 Add a new "`.momentum/` State Layout" subsection (companion to the existing state-source documentation) describing: `sprints/`, `stories/`, `signals/`, and the rationale (DEC-011 D3, Gate G1). Reference DEC-011 by ID.
  - [ ] 7.4 Add a `meta.cycles` changelog entry capturing this relocation, following the existing changelog convention at the top of the file.

- [ ] **Task 8 — End-to-end smoke verification and rollback safety (AC: 10, 11)**
  - [ ] 8.1 With all changes applied, run:
    - `python3 skills/momentum/scripts/test-momentum-tools.py` — passes.
    - `python3 skills/momentum/scripts/momentum-tools.py sprint show` (or equivalent CLI surface) — returns the expected active/planning sprint that matches pre-migration state.
    - Open a fresh Claude session in this project and observe Impetus session-open. Confirm orientation reflects current sprint/story state with no errors and no narration of file reads.
  - [ ] 8.2 Verify the legacy paths `_bmad-output/implementation-artifacts/sprints/`, `_bmad-output/implementation-artifacts/stories/`, and `_bmad-output/implementation-artifacts/intake-queue.jsonl` are deleted (Task 2.8) and that `grep -rn "implementation-artifacts/sprints/index\|implementation-artifacts/stories/index\|implementation-artifacts/intake-queue" .` returns zero matches outside of `.git/`, `.claude/momentum/sprint-logs/` (historical observability data — leave as-is), and any frozen retro/transcript artifacts that quote the old paths historically.
  - [ ] 8.3 Confirm no symlinks or shim files exist that re-expose the old paths (AC #11). The migration is one-way; rollback in this session would require `git checkout`, not a fallback path.

## Dev Notes

### Architecture Compliance

This story implements **DEC-011 Decision D3** (State Source Paths Under `.momentum/`) and clears **Gate G1** for the canvas redesign. Architecture.md's existing Read/Write Authority table (around lines 1166–1184) and the `stories/index.json` / `sprints/index.json` description sections (around lines 1337–1396) require synchronized updates as part of Task 7. The single-state-source invariant (architecture.md "Write authority" note at ~line 1456 — `momentum-tools.py sprint` is the sole writer of `sprints/` and the `status` fields in `stories/index.json`) is preserved: this story only relocates the files, not the write authority.

The new `.momentum/signals/` directory establishes a **read-only ledger pattern** for retro-derived pending work flags. This story defines the contract; the writers (likely `momentum:retro`, `momentum:triage`, `momentum:avfl`) are out of scope and will be implemented in follow-up stories. Architecture.md's new `.momentum/` State Layout subsection (added in Task 7.3) documents this contract so future writers conform.

### Testing Requirements

- `python3 skills/momentum/scripts/test-momentum-tools.py` — must pass after Task 3. Update test fixtures if they hard-code old paths.
- Manual smoke: `momentum-tools sprint show` returns identical output pre- and post-migration (active/planning sprint, completed list, quickfixes list).
- Manual smoke: Open a fresh Claude session, invoke `/momentum`, and confirm Impetus orientation runs silently and reports state correctly.
- Negative test: temporarily move `.momentum/sprints/index.json` aside and confirm Impetus reports state-source-missing honestly (no fallback to old path, no crash).
- Negative test: with `.momentum/signals/` empty, confirm Impetus orientation completes without error or warning.
- `grep -rn` audit confirms zero residual references to `_bmad-output/implementation-artifacts/sprints/index.json` or `_bmad-output/implementation-artifacts/stories/index.json` in `skills/momentum/` and `.claude/` (excluding historical sprint logs and frozen retro artifacts).

### Implementation Guide

Sequence matters because writers and readers must flip together to preserve the single-source-of-truth invariant:

1. **Define schema first** (Task 1) — readers and writers need to know the contract.
2. **Stage data at new location** (Tasks 2.1–2.7) — copy, do not move yet; old paths still readable.
3. **Update writers** (Task 3) — `momentum-tools.py` now writes only to `.momentum/`. From this point forward, the old files become stale.
4. **Update readers** (Tasks 4 and 5) — Impetus and all 15 skill workflows now read only from `.momentum/`.
5. **Update protection hooks** (Task 6) — protect the new paths.
6. **Update architecture documentation** (Task 7) — the spec catches up.
7. **Delete legacy paths and verify** (Tasks 2.8 and 8) — enforce single-source-of-truth.

**Failure mode to avoid:** Do not leave a fallback/dual-read path in any skill workflow. The whole point of Gate G1 is that the canvas can pin against `.momentum/` with stable schemas — a silent fallback re-introduces drift between writers and readers that this story is designed to eliminate.

**Sequencing during the work session:** All writes can be batched into one commit per task; the story is not safely interruptible between Task 3 (writers updated) and Task 5 (readers updated) — during that window, readers are looking at the wrong location. Recommend running Tasks 3, 4, 5 in a single contiguous editing pass before committing.

### Project Structure Notes

- New top-level directory `.momentum/` becomes a first-class state location alongside `_bmad-output/`, `.claude/`, `_bmad/`, `skills/`. Hidden-prefix is intentional — it is operational state, not source.
- `.momentum/signals/` filename pattern: `{signal_type}-{slug-or-timestamp}.json`. Example signal payloads (illustrative, not normative for this story):
  - `triage-uncleared-2026-04-26.json` → `{"signal_type":"triage-uncleared","origin":"momentum:retro","created":"2026-04-26T...","payload":{"items":["..."]}}`
  - `avfl-finding-pending-upstream-fix-canvas-vite-scaffold.json` → `{"signal_type":"avfl-finding-pending-upstream-fix","origin":"momentum:avfl","created":"2026-04-26T...","payload":{"finding_id":"...","story_slug":"canvas-vite-scaffold"}}`
- `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/` per-sprint subdirectories (specs, sprint-summary.md, retro artifacts) currently coexist alongside the index. **Decision:** these sprint-scoped subdirectories move to `.momentum/sprints/{sprint-slug}/` together with the index — relocation is whole-tree, not just the index file. Update sprint-planning, sprint-dev, and retro workflows that write to these per-sprint subdirectories accordingly. (See Task 5 — sprint-planning, sprint-dev, retro all touch these per-sprint paths.)

### References

- **DEC-011** — `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` — Decision D3 (state paths) and Gate G1 (timing).
- **Epic 10: Impetus Core Infrastructure** — `_bmad-output/planning-artifacts/epics.md` lines 642–660. This story falls under "cross-cutting quality work that enables the practice but doesn't belong to a specific capability epic."
- **Architecture: Impetus session-open sequence** — `_bmad-output/planning-artifacts/architecture.md` line ~572.
- **Architecture: Read/Write Authority table** — `_bmad-output/planning-artifacts/architecture.md` lines ~1166–1184.
- **Architecture: stories/index.json schema** — `_bmad-output/planning-artifacts/architecture.md` line ~1337.
- **Architecture: sprints/index.json schema** — `_bmad-output/planning-artifacts/architecture.md` line ~1389.
- **Architecture: write authority** — `_bmad-output/planning-artifacts/architecture.md` line ~1456.
- **Impetus orient reference** — `skills/momentum/skills/impetus/references/orient.md` lines 17–18 (current state-source paths to be replaced).
- **momentum-tools writers** — `skills/momentum/scripts/momentum-tools.py` lines 79–84 (`stories_path()`, `sprints_path()`), 1261, 1346 (lines 1260 and 1345 are adjacent features.json carve-outs — intentionally left unchanged).
- **Hook protection** — `skills/momentum/references/protected-paths.json`, `skills/momentum/references/hooks/file-protection.sh` (and their deployed mirrors under `.claude/momentum/`).
- **Canvas Phase 1 dependency** — `_bmad-output/implementation-artifacts/stories/canvas-vite-scaffold.md` declares `depends_on: [impetus-momentum-state-migration]` and references Gate G1.
- **Downstream canvas consumers** — `canvas-sprints-lens.md` and `canvas-flywheel-lens.md` declare further dependencies on `.momentum/sprints/` lifecycle states and `.momentum/signals/` ledger format being final.

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → specification + config-structure (schema doc + directory)
- Task 2 → config-structure (file relocation, directory creation, deletion)
- Task 3 → script-code (TDD — `momentum-tools.py` and its test file)
- Task 4 → skill-instruction (Impetus `orient.md` reference file)
- Task 5 → skill-instruction (15 skill workflow.md files)
- Task 6 → rule-hook (protected-paths.json + file-protection.sh hook protection)
- Task 7 → specification (architecture.md updates)
- Task 8 → config-structure (verification by inspection)

A reminder for the dev agent: Gherkin specs for this sprint live in `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/` (or the post-migration `.momentum/sprints/sprint-2026-04-27/specs/` location). They are off-limits to the dev agent — implement against the plain English Acceptance Criteria above, never against `.feature` files (Decision 30 black-box separation).

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

This story modifies existing skill files (Impetus `references/orient.md` in Task 4; 15 skill workflow.md files in Task 5). For changes of this kind — pure path-substitution updates that preserve all existing behavior except the file location read — full EDD ceremony is overkill. Apply this lightweight EDD adaptation:

**Before changing any skill file:**
1. Write 1–2 behavioral evals in `skills/momentum/skills/impetus/evals/` (Impetus is the primary affected skill). Examples:
   - `eval-impetus-reads-momentum-state.md` — "Given `.momentum/sprints/index.json` and `.momentum/stories/index.json` exist with valid contents and the legacy `_bmad-output/implementation-artifacts/sprints/index.json` does not exist, Impetus session-open should orient against `.momentum/` data without error and without narrating the read."
   - `eval-impetus-handles-empty-signals.md` — "Given `.momentum/signals/` is empty, Impetus orientation should complete without error and without surfacing any signal-related warnings."

**Then implement:**
2. Update the path strings in the affected skill files per Tasks 4 and 5.

**Then verify:**
3. Run evals: spawn a subagent per eval, give it the eval scenario plus the updated SKILL.md / workflow.md / orient.md as context, and observe whether behavior matches expectation.
4. If all evals match → tasks complete.
5. If any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface to user if still failing).

For Task 5 (15 workflow.md files), the change is mechanical path replacement — no per-skill eval is required for each. Treat the Impetus evals as the EDD coverage for the read-path migration as a whole.

**NFR compliance — applies to any skill file touched:**
- SKILL.md `description` field must remain ≤150 characters (NFR1) — verify if any frontmatter is touched.
- `model:` and `effort:` frontmatter fields must remain present (model routing per FR23).
- SKILL.md / workflow.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3).
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills).

**Additional DoD items for skill-instruction tasks:**
- [ ] At least 2 behavioral evals written in `skills/momentum/skills/impetus/evals/` covering the new `.momentum/` read paths and empty-signals graceful degradation.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation).
- [ ] No SKILL.md frontmatter regressions (description ≤150 chars; model/effort present).
- [ ] No SKILL.md / workflow.md / orient.md exceeds 500 lines after changes.
- [ ] AVFL checkpoint on the produced changes documented (momentum:dev runs this automatically — validates implementation against story ACs).

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). `momentum-tools.py` already has a companion test file at `skills/momentum/scripts/test-momentum-tools.py` — use it as the home for new tests.

1. **Red:** Before changing `stories_path()` and `sprints_path()`, add or update tests in `test-momentum-tools.py` that assert the resolved paths are `.momentum/stories/index.json` and `.momentum/sprints/index.json`. Confirm tests fail against the unmodified script.
2. **Green:** Update `momentum-tools.py` per Task 3.1 — `stories_path()`, `sprints_path()`, line 1261, line 1346 (leave lines 1260 and 1345 unchanged — features.json carve-outs), plus any other internal references found via grep. Run tests; confirm they pass.
3. **Refactor:** If any path is repeated more than twice, consider hoisting to a module-level constant (`_MOMENTUM_DIR = Path(".momentum")`). Keep tests green throughout.

**Note:** Scripts in Momentum live under `skills/momentum/scripts/` for top-level CLI tools and `skills/momentum/skills/[name]/scripts/` for skill-local tools. `momentum-tools.py` is a top-level CLI — no relocation of the script itself, only the data paths it touches.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies):**
- [ ] Tests written and passing for the new `.momentum/`-resolved paths.
- [ ] No regressions in existing test suite.
- [ ] `python3 skills/momentum/scripts/test-momentum-tools.py` passes end-to-end after Task 3.

---

### rule-hook Tasks: Functional Verification

Rules and hook configurations are declarative — they don't have unit tests. Use functional verification:

1. **Update the protection entries** in `skills/momentum/references/protected-paths.json`, `skills/momentum/references/hooks/file-protection.sh`, `.claude/momentum/protected-paths.json`, and `.claude/momentum/hooks/file-protection.sh` per Task 6.
2. **State the expected behavior:** "Given a Write or Edit tool call targeting `.momentum/sprints/index.json` or `.momentum/stories/index.json` from any agent other than `momentum-tools.py` / `momentum:sprint-manager`, the file-protection hook should block the call. Given a tool call targeting the legacy `_bmad-output/implementation-artifacts/sprints/index.json` or `_bmad-output/implementation-artifacts/stories/index.json` (which no longer exist), the hook should not match those paths (since the legacy directory is deleted in Task 2.7)."
3. **Verify functionally:**
   - Read the four updated files and confirm the path strings match `.momentum/sprints/index.json` and `.momentum/stories/index.json` exactly.
   - Run the file-protection.sh script in a dry-run / test mode if available, or simulate by passing a JSON event with a Write tool call targeting `.momentum/stories/index.json` from a non-allowlisted agent.
   - Confirm the conditional matchers (file-protection.sh lines 195–196 and 200–201 pre-change) updated correctly — these are bash string-equality conditions on `$NORM_PATH`.
4. **Document** the verification result in the Dev Agent Record.

**Format requirements:**
- `protected-paths.json` is JSON — must parse without error after edit (validate with `jq` or `python3 -m json.tool`).
- `file-protection.sh` is bash — must pass `bash -n file-protection.sh` (syntax check) after edit.
- The four files (`skills/momentum/references/{protected-paths.json,hooks/file-protection.sh}` and their `.claude/momentum/` mirrors) must stay in sync — if you edit one mirror only, the protection diverges between source-of-truth and deployed copy.

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as a testable condition (in Dev Agent Record).
- [ ] Functional verification performed and result documented.
- [ ] All four protection files (source + mirror, JSON + shell) updated consistently.
- [ ] `protected-paths.json` parses cleanly post-edit.
- [ ] `file-protection.sh` passes `bash -n` post-edit.

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection. Tasks 1.1, 2, and 8 are config-structure work:

1. **Create the directory structure and relocate files** per Tasks 2.1–2.6.
2. **Verify by inspection:**
   - `.momentum/sprints/index.json` and `.momentum/stories/index.json` parse without error (`python3 -m json.tool < .momentum/stories/index.json` returns no error; same for sprints).
   - Story-key count and sprint-state counts match pre-migration (spot-check per AC #8).
   - `.momentum/signals/` exists and is either empty or contains only valid JSON files conforming to the schema.
   - `.momentum/signals/README.md` (or equivalent) is present and readable.
3. **Delete legacy paths** per Task 2.8 only after Tasks 3, 4, 5, 6 are complete and Task 8.1 smoke verification passes.
4. **Document** what was created/moved/deleted in the Dev Agent Record File List.

**No tests required** for pure config/structure changes — JSON parse + spot-check + smoke is sufficient.

**DoD items for config-structure tasks:**
- [ ] `.momentum/sprints/index.json` and `.momentum/stories/index.json` parse cleanly post-relocation.
- [ ] Story-key count and sprint-state arrays preserved byte-for-byte.
- [ ] `.momentum/signals/` directory exists; README documents schema.
- [ ] Legacy `_bmad-output/implementation-artifacts/sprints/` and `_bmad-output/implementation-artifacts/stories/` deleted (single-source-of-truth invariant — AC #11).
- [ ] All paths and structural changes documented in Dev Agent Record File List.

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, or parent spec) — not by tests or evals. Tasks 1.1 (signals schema doc), 1.2 (architecture subsection for `.momentum/`), and 7 (full architecture.md update for the relocation) are specification work.

1. **Write or update the spec** per Tasks 1.1, 1.2, and 7.
2. **Verify cross-references:**
   - All references to DEC-011 and Gate G1 resolve correctly (DEC-011 lives at `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md`).
   - All path references in architecture.md (Read/Write Authority table, schema sections, session-open sequence) match the actual filesystem layout post-Task-2.
   - The new `.momentum/` State Layout subsection in architecture.md cross-references the `.momentum/signals/README.md` (or wherever the signals schema lives) without broken links.
3. **Verify format compliance:**
   - Architecture.md `meta.cycles` changelog follows the existing convention at the top of the file.
   - Any new section heading depth matches surrounding sections (no jumping from `##` to `####`).
4. **Document** what was written or updated in the Dev Agent Record File List.

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum:dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] All cross-references to DEC-011, Epic 10, and other documents resolve correctly.
- [ ] Architecture.md follows existing changelog and section-heading conventions.
- [ ] `.momentum/signals/` schema is documented in exactly one canonical location (avoid drift).
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically).

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
