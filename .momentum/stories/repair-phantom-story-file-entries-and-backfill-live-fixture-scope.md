---
title: "Repair phantom story_file entries + sprint-manager invariant; verify live-fixture backfill on conduct-live-run-against-fixture-sprint"
story_key: repair-phantom-story-file-entries-and-backfill-live-fixture-scope
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: defect
priority: high
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/sprint-manager/workflow.md
  - .momentum/stories/index.json
  - .momentum/stories/build-guidelines-invocation-surface-in-sprint-planning.md
  - .momentum/stories/canvas-gate-review-surface-epic.md
  - .momentum/stories/dag-dispatch-blast-radius-discovery.md
  - .momentum/stories/endgate-format-spec-section00-alignment.md
  - .momentum/stories/re-emit-frozen-app-ui-contracts-via-producer.md
  - .momentum/stories/verification-method-two-column-smoke-ui-model.md
change_type:
  - script-code
  - skill-instruction
  - specification
verification_method_advisory: bash
---

# Repair phantom story_file entries + sprint-manager invariant; verify live-fixture backfill on conduct-live-run-against-fixture-sprint

## Story

As the practice maintainer,
I want every `story_file: true` index entry to have a backing `.md` on disk — enforced by a code invariant that forbids setting the flag when the file is absent, plus a one-time repair of the entries already broken —
so that sprint-planning never crashes on phantom entries and `stories/index.json` stays a truthful map of what actually exists.

## Description

`stories/index.json` has carried entries that claim `story_file: true` for slugs whose `.momentum/stories/{slug}.md` never existed. The 2026-07-06 retro audit of sprint-2026-06-28 found 8 such phantoms; dedup verifiers independently re-confirmed them. A full-index scan on 2026-07-13 shows **6 phantoms remain** — a subset of the original 8. Two of the original eight are now truthful and must be left alone: `conduct-live-run-against-fixture-sprint` (seeded by sprint-planning on 2026-07-13) and `retro-audit-workflow-process-findings-return` (backfilled during the 2026-07-06 retro).

The durable fix and the cleanup are separate concerns:

1. **Code invariant (durable fix).** The sole programmatic index writer — `cmd_story_add` in `momentum-tools.py` — hardcodes `"story_file": True` for every new entry (≈ line 2197), regardless of whether the backing file exists. That is the phantom-creation site. The flag must instead reflect on-disk reality: `story_file: true` is written only when `.momentum/stories/{slug}.md` exists. The `sprint-manager/workflow.md` sole-writer doctrine documents the invariant alongside the code.

2. **Mechanical repair (one-time cleanup).** Backfill a **stub** `.md` for each of the 6 remaining phantoms, with frontmatter mirroring its index entry. These are enrichment-ready stubs (like `momentum:intake` stubs), NOT full authoring — each of the 6 keeps its own substantive scope and its own epic (dedup-confirmed distinct: e.g. `dag-dispatch-blast-radius-discovery` stays a distinct exploration story). After repair the index carries zero phantoms.

3. **Live-fixture backfill — verify, do not re-author (rescoped leg).** The original retro scope asked this story to backfill `conduct-live-run-against-fixture-sprint.md` with live-fixture scope. Sprint-planning already seeded that file on 2026-07-13 with the nornspun-fixture scope. This story therefore only **verifies** the backfill landed (file exists, index truthful, fixture scope documented). Building the fixture and running the driver are `conduct-live-run-against-fixture-sprint`'s own scope — that story declares `depends_on` on this one.

**Pain context:** the missing live fixture was sprint-2026-06-28's dominant root cause — 9/9 ACs BLOCKED on `companion-surface-pre-sprint-plan-gate`, 16/27 E2E scenarios BLOCKED, one 51-turn E2E agent with zero net-new yield; the same root cause was independently rediscovered 3+ times. Phantom entries crash the next sprint-planning pass that selects them. This story removes both hazards: the invariant prevents recurrence, the backfill clears the existing damage.

## Acceptance Criteria

1. **Six backing files exist.** Each of the 6 remaining phantom slugs has a backing `.momentum/stories/{slug}.md`: `build-guidelines-invocation-surface-in-sprint-planning`, `canvas-gate-review-surface-epic`, `dag-dispatch-blast-radius-discovery`, `endgate-format-spec-section00-alignment`, `re-emit-frozen-app-ui-contracts-via-producer`, `verification-method-two-column-smoke-ui-model`. Observable: `for s in <the 6>; do test -f .momentum/stories/$s.md || echo MISSING $s; done` prints nothing.

2. **Stub frontmatter mirrors the index entry.** Each backfilled stub's frontmatter `title`, `epic_slug`, `story_type`, and `priority` equal that slug's `stories/index.json` entry. The 6 span four distinct epics (`momentum-agent-composition-pipeline`, `momentum-feature-taxonomy-maintenance`, `momentum-sprint-orchestration`, `momentum-impetus-experience`) — each stub keeps its own epic; none is reassigned to this story's epic. Observable: a field-by-field frontmatter-vs-index comparison reports 0 mismatches.

3. **Stubs are enrichment-ready, not scope-absorbing.** Each backfilled stub carries `status: backlog` and a "backlog stub — run `momentum:create-story` to enrich" disclaimer, and reproduces only its own slug's scope. No stub absorbs or duplicates another story's substantive work. Observable: each file contains the stub-disclaimer marker; the 6 remain distinct stories in the index.

4. **Index truthfulness after repair — zero phantoms.** A full scan of `stories/index.json` finds zero entries where `story_file: true` and the backing file is absent. Observable: a phantom-scan script (`story_file is True and not os.path.isfile(...)`) prints `PHANTOMS: 0`.

5. **Code invariant — `story_file` reflects disk truth.** `momentum-tools.py` never records `story_file: true` for a slug whose `.momentum/stories/{slug}.md` does not exist. `cmd_story_add` sets `story_file` from on-disk reality (or rejects with a clear error) rather than hardcoding `True`. Observable (bash): adding a brand-new slug with no backing file yields an entry with `story_file: false` (or a non-zero exit + explanatory error); adding one whose backing file exists yields `story_file: true`.

6. **Invariant regression test.** `test-momentum-tools.py` gains a test covering both branches (backing file absent → not-true / rejected; backing file present → `true`). The absent-branch assertion fails against the current hardcoded-`True` behavior and passes after the guard lands. Observable: `python3 skills/momentum/scripts/test-momentum-tools.py` runs green with the new test present; no regressions in the existing suite.

7. **Invariant documented in the sole-writer doctrine.** `sprint-manager/workflow.md` Critical Rules states the invariant: `story_file: true` is written only when the backing `.md` exists on disk; the flag mirrors disk truth. Observable: grep the Critical Rules section for the invariant statement.

8. **Live-fixture backfill verified (verify-only — do not re-author or build the fixture).** `conduct-live-run-against-fixture-sprint.md` exists, its index entry is truthful (`story_file: true` + file present), and the file documents the live-fixture scope (committed nornspun fixture: `momentum/agents.json` project entries, `.claude/manifests/`, composed agents / completed-sprint sample) that the fixture-blocked story family consumes. This story does not build the fixture or run the driver. Observable: file exists + index truthful + grep confirms the fixture scope is documented.

## Tasks / Subtasks

- [ ] **Task 1 — Add the `story_file` truthfulness invariant to the index writer** (script-code; AC5, AC6)
  - [ ] 1.1 Red: add a test to `test-momentum-tools.py` asserting `story-add` for a slug with no backing `.md` produces `story_file: false` (or a clear error); confirm it fails against current behavior.
  - [ ] 1.2 Green: modify `cmd_story_add` in `momentum-tools.py` so `story_file` derives from `(.momentum/stories/{slug}.md).exists()` instead of the hardcoded `True` (≈ line 2197); keep the file-present branch yielding `true`.
  - [ ] 1.3 Add the file-present-branch test (backing file exists → `story_file: true`); run the full suite green.
- [ ] **Task 2 — Document the invariant in the sole-writer doctrine** (skill-instruction; AC7)
  - [ ] 2.1 Add a Critical Rule to `sprint-manager/workflow.md`: `story_file: true` is written only when `.momentum/stories/{slug}.md` exists; the flag mirrors disk truth.
- [ ] **Task 3 — Backfill the 6 phantom stub files** (specification; AC1, AC2, AC3)
  - [ ] 3.1 For each of the 6 slugs, create `.momentum/stories/{slug}.md` with frontmatter (`title`, `epic_slug`, `story_type`, `priority`, `status: backlog`) mirroring its index entry — each keeps its own epic.
  - [ ] 3.2 Give each stub the "backlog stub — run `momentum:create-story` to enrich" disclaimer and a one-line statement of that slug's own scope; do not absorb or duplicate any other story's work.
- [ ] **Task 4 — Confirm index truthfulness** (script-code/verify; AC4)
  - [ ] 4.1 Run the full-index phantom scan; confirm `PHANTOMS: 0`.
- [ ] **Task 5 — Verify the live-fixture backfill landed** (specification/verify; AC8)
  - [ ] 5.1 Confirm `conduct-live-run-against-fixture-sprint.md` exists, its index entry is truthful, and the file documents the nornspun-fixture scope. Do NOT re-author it or build the fixture.

## Dev Notes

### Decision Authority

- **Epic: `momentum-conductor-core`** — index-authoritative (DEC-034 D6: the index `epic_slug` governs). The story-file frontmatter was self-healed from the stale `momentum-sprint-orchestration` to match the index during enrichment.
- **This story is a hard blocker for `conduct-live-run-against-fixture-sprint`**, which declares `depends_on: [..., repair-phantom-story-file-entries-and-backfill-live-fixture-scope]`. The live-fixture family cannot verify PASS/FAIL until the phantom-and-fixture-spec substrate this story repairs is truthful. The downstream "3 fixture-blocked stories report PASS/FAIL instead of BLOCKED" payoff belongs to that consumer story, not here.
- **Source:** 2026-07-06 retro transcript audit of sprint-2026-06-28 (`audit-return.json` priority items 1 + 3, merged at the Phase 5 dedup), dedup-verified in the 2026-07-06 corpus-dedup workflow.

### Current State of Affected Files

- `skills/momentum/scripts/momentum-tools.py` — `cmd_story_add` (≈ line 2168) is the sole programmatic writer of `stories/index.json`; line ≈ 2197 hardcodes `"story_file": True` for every new entry regardless of disk state. This is the phantom-creation site.
- `skills/momentum/scripts/test-momentum-tools.py` — CLI-driven test harness (`python3 test-momentum-tools.py`, self-contained, no pytest); currently has no `story-add` / `story_file`-truthfulness test.
- `skills/momentum/skills/sprint-manager/workflow.md` — the sole-writer doctrine doc (Critical Rules section, ≈ lines 188–195); does not yet state the `story_file` truthfulness invariant.
- `.momentum/stories/index.json` — 523 entries; full scan (2026-07-13) shows exactly 6 phantoms remaining (the AC1 list), all a subset of the retro's original 8. `conduct-live-run-against-fixture-sprint` and `retro-audit-workflow-process-findings-return` are already truthful — do NOT re-create them.

### Architecture Compliance

- The invariant belongs at the single write site, not scattered across callers — `momentum-tools.py` is the DEC-designated sole writer of `stories/index.json`. Deriving the flag from disk truth there is the durable fix; the 6-file backfill is one-time cleanup of pre-existing damage.
- `story_file` semantics: `true` MUST mean "a backing `.md` exists." The guard turns the field into a derived truth rather than an unconditional assertion.
- The 6 stubs follow the established backlog-stub pattern (frontmatter + stub disclaimer + `status: backlog`), so a later `momentum:create-story` enrich pass can flesh each out without conflict.

### Testing Requirements

- **Verification method (advisory): `bash`.** The story's primary deliverable is the code invariant (`script-code` → `bash` per `verification-standard.md` §1). Exercise `sprint story-add` against a temp index with and without a backing file and observe the resulting `story_file` value.
- Regression coverage lives in `test-momentum-tools.py`; run `python3 skills/momentum/scripts/test-momentum-tools.py` — full suite green, new test covers both branches (absent → not-true; present → true).
- The stub-backfill (specification) and doctrine (skill-instruction) tasks are verified by inspection/grep, subsumed under the story's `bash` primary method — no separate driver.
- **Harness profile:** declare the harness-profile reference from the frozen contract before verification (`verification-standard.md` §3); the `bash` driver binding applies.

### Project Context Reference

- A frozen verification contract for this sprint lives at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly named by `how_dev_self_checks`.

### References

- Retro audit return: `.momentum/sprints/sprint-2026-06-28/audit-return.json` (priority items 1 + 3, merged at the Phase 5 dedup)
- Dedup verification record: session 2026-07-06 corpus-dedup workflow `wf_7b949d2b-a8e`
- Downstream consumer: `.momentum/stories/conduct-live-run-against-fixture-sprint.md` (declares `depends_on` on this story; owns the fixture build + live driver run)
- Invariant site: `skills/momentum/scripts/momentum-tools.py` `cmd_story_add` (≈ line 2197)
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 4 → `script-code` (TDD; the invariant guard + truthfulness scan)
- Task 2 → `skill-instruction` (EDD/doctrine; sole-writer Critical Rule)
- Tasks 3, 5 → `specification` (direct authoring / cross-reference verification; stub backfill + backfill verification)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively:

1. **Red:** Write the failing test for the invariant first (Task 1.1 — new slug, no backing file, assert `story_file` is not `true`). Confirm it fails against the current hardcoded-`True` behavior before implementing.
2. **Green:** Implement the minimum change in `cmd_story_add` so `story_file` derives from `(.momentum/stories/{slug}.md).exists()`. Run tests to confirm.
3. **Refactor:** Keep the file-present branch (`true`) intact; ensure no regression in the existing suite.

**Note:** Momentum scripts live under `skills/momentum/scripts/`. Follow the existing structure of `momentum-tools.py` / `test-momentum-tools.py` (self-contained, subprocess-driven CLI tests — no pytest).

**DoD items for script-code tasks:**
- Tests written and passing (both branches of the invariant)
- No regressions in existing `test-momentum-tools.py`
- `PHANTOMS: 0` confirmed by the full-index scan after backfill

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

The doctrine change to `sprint-manager/workflow.md` is a documentation-of-behavior change, not a new skill capability, so a full EDD eval cycle is not warranted for a single Critical-Rule addition. Verify functionally instead: the added rule must be internally consistent with the enforced code invariant (Task 1) and must state the disk-truth semantics precisely.

**NFR compliance (skill-instruction):** the edit is confined to `workflow.md` Critical Rules; do not alter the `sprint-manager` SKILL.md frontmatter (`model`/`effort`) or exceed the 500-line body limit.

**Additional DoD items:**
- [ ] Critical Rule added to `sprint-manager/workflow.md` stating the `story_file` disk-truth invariant
- [ ] Rule wording matches the enforced code behavior in `cmd_story_add` (no divergence between doctrine and code)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

The 6 stub files and the backfill verification are specification tasks — validated by inspection and cross-reference, not tests:

1. **Write each stub** with frontmatter mirroring its index entry (`title`, `epic_slug`, `story_type`, `priority`, `status: backlog`) and a stub disclaimer. Each keeps its own epic — do not reassign.
2. **Verify cross-references:** each stub's frontmatter fields resolve against `stories/index.json`; the conduct-live-run backfill verification confirms the file exists, the index entry is truthful, and the fixture scope is documented.
3. **Verify format compliance:** stubs follow the backlog-stub frontmatter schema used by `momentum:intake` / retro stubs.
4. **Document** the backfill and verification results in the Dev Agent Record.

**No tests or evals required** for the stub/verify tasks. AVFL checkpoint (run by `momentum:dev`) validates against acceptance criteria.

**Additional DoD items:**
- [ ] All 6 stub frontmatters resolve field-for-field against their index entries
- [ ] Each stub carries the backlog-stub disclaimer and does not absorb another story's scope
- [ ] conduct-live-run backfill confirmed present + truthful + fixture-scope documented (verify-only)

## Dev Agent Record

_Populated by the dev agent during implementation._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
