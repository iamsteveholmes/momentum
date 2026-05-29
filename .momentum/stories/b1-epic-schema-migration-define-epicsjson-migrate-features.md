---
title: "B1: Epic schema migration — define epics.json, migrate features and categorical epics, re-home unhomed stories"
story_key: b1-epic-schema-migration-define-epicsjson-migrate-features
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: practice
change_type:
  - config-structure
  - specification
  - script-code
verification_method: document review
harness_profile: default
depends_on: []
touches:
  - _bmad-output/planning-artifacts/epics.json
  - _bmad-output/planning-artifacts/features.json
  - _bmad-output/planning-artifacts/archive/features-pre-2026-05.json
  - _bmad-output/planning-artifacts/epics.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/prd.md
  - .momentum/stories/index.json
  - skills/momentum/scripts/migrate-features-to-epics.py
priority: high
source_decisions:
  - DEC-034 (Epic-Layer Consolidation — D1–D5)
plan_ref: ~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md
---

# B1: Epic schema migration — define epics.json, migrate features and categorical epics, re-home unhomed stories

## Story

As a Momentum developer,
I want a unified `epics.json` schema with all 23 features migrated, the 18 categorical epics evaluated case-by-case, and the 269 unhomed stories best-effort re-homed,
So that the epic layer becomes the single source of truth for work organization per DEC-034, B2/B3/B4 can proceed against a stable schema, and the dual feature/epic layer is retired.

## Description

Implements DEC-034 D1–D5. This is the foundation story for Cascade B and blocks B2 (create-story input-routing), B3 (canvas update), and B4 (feature-grooming/feature-breakdown restructure).

**Scope:**

1. **Define `epics.json` schema** at `_bmad-output/planning-artifacts/epics.json` with the unified epic shape:
   - `epic_slug` — string, identifier (snake-case)
   - `name` — string, human-readable
   - `description` — string, prose summary
   - `lifecycle` — enum `finite-lived | long-lived` (DEC-034 D2)
   - `audience` — enum `user | internal` (DEC-034 D3)
   - `value_analysis` — string (multi-paragraph; carried from features.json — current value, full vision, known gaps)
   - `system_context` — string (carried from features.json — product fit)
   - `acceptance_conditions` — array of strings (renamed from `acceptance_condition`; carried from features.json with semantics widened to support long-lived epics where ACs may be absent)
   - `stories` — array of story_keys (carried from features.json; for categorical epics, derived from current stories/index.json `epic_slug` membership)
   - `stories_done` — integer (count cached)
   - `stories_remaining` — integer (count cached)
   - `last_verified` — ISO date string
   - `notes` — string (free-form provenance / migration notes)
   - `depends_on` — array of `epic_slug` (optional; carried from features.json Decision 44 amendment)
   - `type` — optional string `flow | connection | quality` (DEC-034 D3 rationale: flow/connection/quality taxonomy may survive as sub-typing for user-facing finite-lived epics; preserve where present, omit otherwise)

2. **Migrate the 23 features** from `features.json` into `epics.json`:
   - Default `lifecycle: finite-lived`, `audience: user` per DEC-034 D5.
   - Carry `value_analysis`, `system_context`, `acceptance_condition → acceptance_conditions[]`, `stories[]`, `stories_done`, `stories_remaining`, `last_verified`, `notes`, `type`.
   - Drop legacy fields no longer in the unified schema (`prd_section`, `status` — superseded by lifecycle + counts; `feature_slug` becomes `epic_slug`).
   - The feature-slug → epic-slug rename is direct (no string mutation needed: `momentum-agent-composition-pipeline` carries forward as the epic_slug).

3. **Evaluate the 18 categorical epics** one by one with the developer (interactive review during dev, not at story-definition time):
   - For each current `epic_slug` referenced in `stories/index.json` that is NOT one of the 23 migrated features, decide:
     - **Dissolve** — re-home each story to a finite-lived epic; the categorical epic disappears.
     - **Convert to long-lived** — write the epic into `epics.json` with `lifecycle: long-lived`. Reserved for genuinely ongoing concerns (e.g., `ad-hoc`).
   - Default disposition is **dissolve**; `long-lived` requires explicit justification per epic recorded in the `notes` field.

4. **Re-home the 269 unhomed stories** referenced in `stories/index.json` that do not appear in any feature's `stories[]` array:
   - Best-effort assignment to an appropriate epic_slug.
   - `ad-hoc` accepts residue per DEC-034 D5.
   - Update each affected entry in `stories/index.json` to reflect the new epic membership AND add to the target epic's `stories[]` array in `epics.json`.
   - Stories already homed in a feature carry their feature_slug forward as the new epic_slug — no action needed.

5. **Freeze `features.json`** as `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json` and remove the original file. Document the archive path in the migration script output and the epics.json provenance `notes`.

6. **Update `architecture.md`:**
   - Mark Decisions 44–49 (Feature Artifact Layer, feature-status, feature-status cache, sprint summary feature-status spawn, practice project detection, feature-grooming) as **HISTORICAL** with a forward reference to DEC-034 and epics.json.
   - Update the Read/Write Authority table: remove the `features.json` row; add an `epics.json` row (writers TBD by B4 — note as such); update the canvas server row to read `epics.json` instead of `features.json`.
   - Update Skills Deployment Classification: note `momentum:feature-grooming` and `momentum:feature-breakdown` as pending rename (B4); update canvas row to read epics.json.
   - Update `.momentum/` State Layout and Repository Structure trees: replace `features.json` with `epics.json` references.

7. **Update `prd.md`:**
   - Mark FR102–FR113 (feature artifact layer + feature-status + feature-breakdown FRs introduced sprint-2026-04-11) as **SUPERSEDED** with a forward reference to DEC-034.
   - Annotate Epic 13 (Feature Orientation) as **HISTORICAL** — the epic concept absorbs the feature layer per DEC-034.
   - Do NOT delete the FRs — annotate in place, preserving the historical record.

8. **Restructure `epics.md`:**
   - Per DEC-034 D4, `epics.md` may retire entirely (canvas becomes the human view) OR survive as a derived narrative view.
   - Implementation choice for this story: retire as the primary store; convert to a derived index page that points readers to `epics.json` (authoritative) and the canvas (human view). Preserve current narrative content as historical archive (e.g., `_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md`).

**Pain context:** Foundation story for Cascade B. Blocks B2/B3/B4. Heaviest single lift in cascade (269-story re-homing pass). DEC-034 D5 explicitly accepts `ad-hoc` as residue to keep the work shippable.

**Source:** triage handoff `practice-ledger-and-epic-cascade-stories-2026-05-25`; DEC-034.

## Acceptance Criteria

### AC1 — epics.json schema and instance

- `_bmad-output/planning-artifacts/epics.json` exists and parses as valid JSON.
- The top-level structure is `{ "<epic_slug>": { ...epic-fields... }, ... }` (object keyed by epic_slug — matches features.json shape for migration legibility).
- Every entry has at minimum: `epic_slug`, `name`, `description`, `lifecycle`, `audience`, `stories[]`, `stories_done`, `stories_remaining`, `last_verified`, `notes`.
- `lifecycle` ∈ {`finite-lived`, `long-lived`} for every entry; no other values.
- `audience` ∈ {`user`, `internal`} for every entry; no other values.
- A JSON-schema validation pass (jq or python script) confirms the above for every entry.

### AC2 — features.json migration

- All 23 features in the pre-migration `features.json` appear as entries in `epics.json`.
- Each migrated entry has `lifecycle: finite-lived` and `audience: user` unless `notes` records explicit reclassification with rationale.
- `value_analysis`, `system_context`, `stories[]`, `stories_done`, `stories_remaining`, `last_verified`, and `type` (where present) carry forward unchanged.
- Each migrated entry's `acceptance_conditions[]` contains the prior `acceptance_condition` string as its first element.
- The original `features.json` is gone from `_bmad-output/planning-artifacts/`; an archive copy exists at `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json` byte-identical to the pre-migration file (sha256 check).

### AC3 — categorical epic evaluation

- Every `epic_slug` value currently appearing in `.momentum/stories/index.json` is accounted for in `epics.json` OR has been dissolved (its stories re-homed to a different epic_slug that DOES appear in `epics.json`).
- `ad-hoc` exists in `epics.json` with `lifecycle: long-lived`.
- Every `lifecycle: long-lived` epic has a non-empty `notes` field containing the developer's rationale for that classification.
- Dissolved categorical epics are documented in a single migration log section at the end of `epics.json` (in a `_migration` reserved key, or in the migration script output committed alongside the story).

### AC4 — story re-homing

- Every story in `.momentum/stories/index.json` has an `epic_slug` field that matches a key in `epics.json`. Zero orphans.
- For every epic in `epics.json`, its `stories[]` array is consistent with the set of stories in `stories/index.json` whose `epic_slug` matches. Stated as a bidirectional invariant: `stories/index.json` → `epics.json` and `epics.json` → `stories/index.json` agree.
- `stories_done` and `stories_remaining` counts in `epics.json` match the corresponding `status` distribution in `stories/index.json` (done counts as `stories_done`; backlog/ready-for-dev/in-progress count as `stories_remaining`; dropped is excluded).

### AC5 — architecture.md updates

- Decisions 44, 45, 46, 47, 48, 49 in `architecture.md` are explicitly annotated `HISTORICAL` with a forward reference to DEC-034 and `epics.json`. Annotation pattern matches existing historical-decision annotations in the file.
- The Read/Write Authority table no longer contains a `features.json` row; it contains an `epics.json` row (writer designation may say "TBD by B4 — currently the migration script in this story; future writes via epic-grooming once B4 ships").
- The canvas server row in the Read/Write Authority table reads `epics.json` (not `features.json`).
- All other inline references to `features.json` are either updated to `epics.json` OR explicitly annotated as historical.

### AC6 — prd.md updates

- FR102 through FR113 are annotated `SUPERSEDED by DEC-034` in place (not deleted).
- Epic 13 (Feature Orientation) is annotated `HISTORICAL — absorbed into the unified epic concept per DEC-034`.

### AC7 — epics.md restructure

- `_bmad-output/planning-artifacts/epics.md` is either:
  - **Retired** — moved to `_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md` and a short successor stub at the original path points readers to `epics.json` and the canvas; OR
  - **Restructured** — rewritten as a derived narrative view with explicit annotation that `epics.json` is authoritative.
- The choice is documented in `epics.json` `_migration` notes.

### AC8 — migration script committed

- A migration script exists at `skills/momentum/scripts/migrate-features-to-epics.py` (or `.sh`, developer's choice) that performs the deterministic portions of the migration (features → epics.json shape transform, story re-homing index sync, archive copy).
- The script is idempotent: running it twice on the same input produces the same output, and running it against an already-migrated state is a no-op (or errors clearly).
- The script has a corresponding test file (`test-migrate-features-to-epics.py` or equivalent) covering at minimum: schema-shape transform, story-list sync, archive-path creation.
- The script does NOT perform the interactive categorical-epic evaluation (that is developer judgment); it accepts the developer's per-epic disposition as input (e.g., a YAML or JSON config file committed with the story).

### AC9 — end-to-end consistency

- After the migration is complete, `bd ready --json` (or the equivalent CLI dependency-readiness check) reports B2, B3, B4 as ready-to-start (their `depends_on: [b1-epic-schema-migration-define-epicsjson-migrate-features]` constraint is satisfied).
- A document-review pass (manual + AVFL) confirms: epics.json parses, all ACs above hold, no broken cross-references in architecture.md / prd.md / epics.md.

## Tasks / Subtasks

- [x] **Task 1 (config-structure):** Define `epics.json` schema and write a JSON-schema validator (informal — jq query or Python validator script). Schema lives inline in the migration script or as a sibling file.
- [x] **Task 2 (script-code):** Implement `skills/momentum/scripts/migrate-features-to-epics.py` with TDD:
  - Red: write failing tests for the features → epics shape transform (one feature in → one epic out, all carried fields preserved).
  - Red: write failing tests for the stories/index.json round-trip (every story has a valid epic_slug after migration; epics.json `stories[]` arrays match).
  - Red: write failing tests for archive-path creation (features.json → archive/features-pre-2026-05.json, byte-identical, original removed).
  - Green: implement the script to make tests pass.
  - Refactor as needed.
- [x] **Task 3 (config-structure + developer-interactive):** Evaluate the 18 categorical epics with the developer. Record per-epic disposition (dissolve | long-lived) in a config file (`skills/momentum/scripts/categorical-epic-dispositions.yaml` or similar) committed with the story. The migration script reads this config.
- [x] **Task 4 (config-structure):** Run the migration script. Verify epics.json parses, AC1–AC4 invariants hold by automated check (jq or Python). Commit the generated `epics.json`, the archived `features-pre-2026-05.json`, and the updated `.momentum/stories/index.json`.
- [x] **Task 5 (specification):** Update `architecture.md` — annotate Decisions 44–49 HISTORICAL; update Read/Write Authority table (remove features.json, add epics.json, update canvas row); update Skills Deployment Classification (note feature-grooming/feature-breakdown pending B4 rename); update Repository Structure trees and `.momentum/` State Layout references.
- [x] **Task 6 (specification):** Update `prd.md` — annotate FR102–FR113 SUPERSEDED-by-DEC-034 in place; annotate Epic 13 HISTORICAL.
- [x] **Task 7 (specification):** Restructure `epics.md` per AC7 (retire-and-stub chosen as the default disposition; archive original to `archive/epics-pre-2026-05.md`).
- [x] **Task 8 (specification):** Cross-reference verification — run a grep/check pass for `features.json` references across the repo (docs, skills, scripts). Update or annotate each occurrence. Surface any that cannot be safely changed in this story (will be fixed in B2/B3/B4 as those touch their own surfaces).
- [x] **Task 9 (verification):** Document-review pass on the migration script output + all updated specs. AVFL pass on the schema + migrated data (corpus mode across epics.json, architecture.md, prd.md, epics.md).

## Dev Notes

### Architecture Compliance

- DEC-034 D1–D5 are the authoritative source. Read `_bmad-output/planning-artifacts/decisions/dec-034-epic-layer-consolidation-2026-05-25.md` before starting.
- This story DOES touch protected paths under `_bmad-output/planning-artifacts/`. The architecture's Protection Boundaries allow such writes when authorized by a decision document; DEC-034 is the authorization.
- B4 (feature-grooming → epic-grooming + feature-breakdown → epic-breakdown rename) handles the skill-side ownership transfer. This story does NOT modify those skills' workflow.md files — it only annotates the architecture table that they are pending rename.
- The Read/Write Authority row for `epics.json` writer should temporarily say "TBD — migration script in story B1; future writes via momentum:epic-grooming (B4)". B4 will harden that row.

### Testing Requirements

- **Migration script (Task 2):** TDD via bmad-dev-story standard. Tests live alongside the script (`test-migrate-features-to-epics.py` or equivalent). Red-green-refactor.
- **JSON schema validation (Task 1):** A jq query or Python validator runs as part of the script's test suite. Confirms every epic entry has the required fields with the right types.
- **Cross-reference verification (Task 8):** Grep-based — no test framework needed. Document findings in the Dev Agent Record.
- **End-to-end verification (Task 9):** Document review per the verification-standard.md routing for `specification` change_type. AVFL corpus mode across epics.json + the three spec files.

### Implementation Guide

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1, 3, 4 → config-structure (direct implementation + validation)
- Task 2 → script-code (TDD)
- Task 5, 6, 7, 8 → specification (document review)
- Task 9 → verification (document review + AVFL)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria.
2. **Verify by inspection:**
   - JSON files: must parse without error (validate with `jq` or `python -m json.tool`).
   - Required fields: each required field must be present with the correct type. Use the jq validator script from Task 1.
   - Paths: all referenced paths must exist after creation.
   - Cross-document consistency: stories/index.json ↔ epics.json bidirectional invariant (AC4) must hold by automated check.
3. **Document** what was created in the Dev Agent Record.

**DoD items for config-structure tasks:**
- [ ] `epics.json` parses without error (validated with jq).
- [ ] All required fields present with correct types.
- [ ] `archive/features-pre-2026-05.json` exists, byte-identical to pre-migration features.json (sha256 check recorded in Dev Agent Record).
- [ ] `stories/index.json` ↔ `epics.json` bidirectional invariant verified by automated script.
- [ ] Categorical-epic disposition config (`categorical-epic-dispositions.yaml`) committed.

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively:

1. **Red:** Write failing tests for the migration script's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/scripts/`. Follow the existing pattern from `momentum-tools.py` for language choice (Python preferred), structure (subcommand pattern), and test conventions.

**DoD items for script-code tasks:**
- [ ] Tests written and passing for: features→epics shape transform, stories/index.json round-trip, archive-path creation, idempotency check.
- [ ] No regressions in existing test suite (`test-momentum-tools.py` and siblings still pass).
- [ ] Script is idempotent — verified by running twice and diffing output.

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (DEC-034 + the migrated epics.json) — not by tests or evals.

1. **Write or update the spec** per the story's acceptance criteria.
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly. Run a grep pass for `features.json` and `feature-grooming` / `feature-breakdown` to find every touchpoint.
3. **Verify format compliance:** architecture.md uses inline `HISTORICAL — superseded by ...` annotations for historical decisions — follow the existing pattern. prd.md uses inline `SUPERSEDED` annotations for FRs — follow the existing pattern.
4. **Document** what was written or updated in the Dev Agent Record.

**DoD items for specification tasks:**
- [ ] Decisions 44–49 in architecture.md annotated HISTORICAL with DEC-034 cross-reference.
- [ ] Read/Write Authority table in architecture.md updated (features.json removed; epics.json added; canvas row updated).
- [ ] FR102–FR113 in prd.md annotated SUPERSEDED in place.
- [ ] Epic 13 in epics.md / prd.md annotated HISTORICAL.
- [ ] epics.md restructured per AC7 (retire-and-stub default disposition).
- [ ] Grep pass for `features.json` references across repo completed; findings documented in Dev Agent Record with disposition for each (updated | annotated | deferred to B2/B3/B4).
- [ ] AVFL checkpoint result documented.

### Project Structure Notes

- New file: `_bmad-output/planning-artifacts/epics.json` (sole writer for B1: the migration script; subsequent writer: momentum:epic-grooming after B4 ships).
- New file: `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json` (frozen archive — never written again).
- New file (optional): `_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md` (frozen archive of the narrative).
- New file: `skills/momentum/scripts/migrate-features-to-epics.py` and test sibling.
- New file: `skills/momentum/scripts/categorical-epic-dispositions.yaml` (developer-authored config consumed by the migration script).
- Modified: `_bmad-output/planning-artifacts/architecture.md`, `prd.md`, `epics.md` (in place).
- Modified: `.momentum/stories/index.json` (epic_slug normalization across the 269 unhomed stories).
- Removed: `_bmad-output/planning-artifacts/features.json` (archived first, then removed).

### Concurrency Notes

- This story touches `architecture.md` and `prd.md`. Per the cascade plan's concurrency matrix (max 1 quick-fix touching architecture.md at a time), this story must NOT run in parallel with another architecture.md-touching story. Within cascade B, this is the only architecture.md-touching story in the foundation slot.
- This story does NOT touch `momentum-tools.py` (that is A1's domain). Cascade A and Cascade B are independent.

### References

- DEC-034 (Epic-Layer Consolidation) — D1–D5 — `_bmad-output/planning-artifacts/decisions/dec-034-epic-layer-consolidation-2026-05-25.md`
- AES-003 (Practice-Ledger Defects + Epic-Layer Consolidation) — `_bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md`
- Cascade plan — `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md`
- Handoff — `.momentum/handoffs/practice-ledger-and-epic-cascade-stories-2026-05-25.md`
- Verification standard — `skills/momentum/references/rules/verification-standard.md`
- Change-type templates — `skills/momentum/skills/create-story/references/change-types.md`
- features.json (pre-migration) — `_bmad-output/planning-artifacts/features.json`
- epics.md (pre-migration) — `_bmad-output/planning-artifacts/epics.md`

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6 (sprint-2026-05-26 dev agent)

### Debug Log References

- Idempotency test fixed: second-run rehomed_count differed from first run because dissolved-epic re-homing was being recounted on already-homed stories. Fixed by only incrementing rehomed_count when epic_slug actually changes.
- Smoke test _migration key: schema validator in smoke script iterated all keys including `_migration`. Fixed by adding `if slug == '_migration': continue` guard.
- Smoke test stories loop: original used `s.get('story_key')` on values (not valid — key is dict key, not field). Fixed to iterate `idx.items()`.

### Completion Notes List

- Migration script (`migrate_features_to_epics.py`) implemented with TDD: 39 tests written (red first, then green), all passing.
- Schema validator is inline in the script (`validate_epic_schema()`).
- 23 features migrated from `features.json` to `epics.json` with `lifecycle: finite-lived`, `audience: user` per DEC-034 D5.
- 18 categorical epics evaluated in `categorical-epic-dispositions.yaml`: 17 dissolved, 1 long-lived (`ad-hoc`).
- 401 stories re-homed to valid epic_slugs. Zero orphans. Bidirectional invariant holds.
- Archive SHA256: `4fe78e31e28a9aad53d700d50a047caefc9957aaf832b7d61c3cef0022634ad5` (byte-identical to pre-migration `features.json`).
- `epics.md` retired-and-stubbed; narrative archived to `archive/epics-pre-2026-05.md`.
- architecture.md: Decisions 44–49 annotated HISTORICAL with DEC-034 forward reference. Read/Write Authority table updated. Skills Deployment Classification updated. Repository Structure tree updated. `.momentum/` State Layout carve-out updated.
- prd.md: FR102–FR113 annotated SUPERSEDED by DEC-034 in place. Epic 13 (Feature Orientation) annotated HISTORICAL.
- Cross-reference grep: `features.json` refs in skills/feature-grooming, skills/feature-breakdown, skills/triage, skills/feature-status explicitly deferred to B4 (those are the skill-side rename stories). Research/doc archives left as historical records.
- Smoke test passes: `bash .momentum/sprints/sprint-2026-05-26/specs/b1-epic-schema-migration-define-epicsjson-migrate-features.smoke.sh` → PASS.
- No regressions: `test-momentum-tools.py` 553 passed, 0 failed.

### File List

- `_bmad-output/planning-artifacts/epics.json` — CREATED (unified epic layer, 24 entries + _migration)
- `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json` — CREATED (byte-identical archive)
- `_bmad-output/planning-artifacts/archive/epics-pre-2026-05.md` — CREATED (archived narrative)
- `_bmad-output/planning-artifacts/features.json` — DELETED (migrated to epics.json)
- `_bmad-output/planning-artifacts/epics.md` — MODIFIED (retired-and-stubbed; points to epics.json and canvas)
- `_bmad-output/planning-artifacts/architecture.md` — MODIFIED (Decisions 44–49 HISTORICAL; table updates)
- `_bmad-output/planning-artifacts/prd.md` — MODIFIED (FR102–FR113 SUPERSEDED; Epic 13 HISTORICAL)
- `.momentum/stories/index.json` — MODIFIED (401 stories re-homed to valid epic_slugs)
- `.momentum/stories/b1-epic-schema-migration-define-epicsjson-migrate-features.md` — MODIFIED (task checkboxes, Dev Agent Record)
- `skills/momentum/scripts/migrate_features_to_epics.py` — CREATED (migration script)
- `skills/momentum/scripts/migrate-features-to-epics.py` — CREATED (symlink to migrate_features_to_epics.py)
- `skills/momentum/scripts/test-migrate-features-to-epics.py` — CREATED (39 tests)
- `skills/momentum/scripts/categorical-epic-dispositions.yaml` — CREATED (18 categorical epic dispositions)
- `.momentum/sprints/sprint-2026-05-26/specs/b1-epic-schema-migration-define-epicsjson-migrate-features.smoke.sh` — MODIFIED (fixed _migration key guard and story loop)
