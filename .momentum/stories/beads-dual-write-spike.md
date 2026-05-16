---
title: Spike — Beads Dual-Write Proof of Concept
story_key: beads-dual-write-spike
status: ready-for-dev
epic_slug: sprint-dev-workflow
story_type: spike
change_type: [skill-instruction, config-structure, rule-hook]
depends_on: []
touches:
  - skills/momentum/skills/sprint-manager/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/intake/workflow.md
  - .claude/settings.json
  - .momentum/beads-id-map.json
---

# Spike: Beads Dual-Write Proof of Concept

Status: ready-for-dev

## Story

As a Momentum developer running a sprint,
I want beads (`bd`) running as a dual-write shadow alongside the existing JSON-backed state layer,
so that we can empirically validate whether `bd ready`, `discovered-from`, and `bd prime` deliver
the dependency scheduling, intake, and memory benefits described in DEC-028 before committing to
a full migration.

## Context / Decision Reference

**Source decision:** DEC-028 — Beads as Tracker/Dependency/Memory Substrate — Adoption Under Momentum via Dual-Write Spike
**Decision document:** `momentum/decisions/dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md`

This is a time-boxed spike (one sprint). The deliverable is a committed research artifact that
evaluates all four gate criteria from DEC-028 and records the go/no-go recommendation. `index.json`
remains authoritative throughout — beads is a shadow, not a replacement.

**Gate criteria to evaluate (from DEC-028):**
- Gate 1: Did `bd ready` + `--claim` measurably simplify sprint-dev Phases 1–3 and remove hand-maintained graph logic?
- Gate 2: Did `discovered-from` eliminate intake-queue triage toil without losing items?
- Gate 3: Was Dolt sync manageable alongside the git-discipline rules?
- Gate 4: Did `--spec-id` linkage hold without in-tree metadata loss?

## Acceptance Criteria

1. Beads is installed (`bd` CLI available) and initialized (`bd init --quiet`) in the project root.
2. `.beads/` directory is gitignored; `bd` CLI invocations are confirmed to operate without error.
3. `sprint-manager/workflow.md` is modified to dual-write: every story/sprint creation and `status_transition` call mirrors to beads via `bd create`, `bd update`, and `bd dep add`. Epic memberships write as `--parent` relationships; features write as `relates-to` edges on epic-type beads.
4. `sprint-dev/workflow.md` Phase 1 dependency graph construction uses `bd ready --json --claim` as the primary ready-queue source, supplemented by `sprint_waves`/`story_depends_on_map` as a fallback when beads returns empty or errors. The `--claim` flag enables atomic acquisition of the unblocked story so concurrent agents cannot race on the same story. The handoff point (where the old graph-building logic was) is clearly marked.
5. For one sprint: discovered work is captured via `bd create --deps discovered-from:<origin-bead-id>` instead of appending to `intake-queue.jsonl`. The `intake/workflow.md` is modified to route `discovered-from` items through `bd create` when the beads layer is active.
6. `bd prime` is wired via a SessionStart hook in `.claude/settings.json`. A `.beads/PRIME.md` file exists carrying Momentum's protocol (git-discipline rules summary, sprint state reminder, sole-writer enforcement note). `no-git-ops` / `--stealth` mode is set so `bd prime` never injects `bd dolt push` autonomously.
7. Story spec files remain exclusively in `.momentum/stories/{slug}.md`. Each bead created for a Momentum story includes `--spec-id` linking to the corresponding `.md` path. No spec prose is stored in Dolt.
8. A research artifact is written at `docs/research/beads-dual-write-spike-findings-{date}.md` with:
   - One section per gate criterion (Gate 1–4) with factual observations from the spike sprint
   - A go/no-go recommendation: proceed to authoritative migration (3+ gates positive) OR keep JSON model
   - Any operational friction observed (Dolt sync, `--stealth` compliance, edge cases)
9. The research artifact is committed to the git tree before the spike story is marked done.
10. No regressions in sprint-manager or sprint-dev behavior — the JSON-backed path remains fully functional as a fallback.
11. `bd ready --json --claim` is verified to return a semantically distinct `discovered-from` edge type (not a generic blocker dependency) by running `bd show <bead-id>` and inspecting the deps field type during Task 5 validation.

## Tasks / Subtasks

- [ ] Task 1: Install and initialize beads (AC: 1, 2)
  - [ ] Install `bd` CLI via `mise use github:gastownhall/beads@latest` (or Homebrew if mise backend unavailable — `brew install beads`)
  - [ ] Run `bd init --quiet` in project root
  - [ ] Verify `.beads/` is in `.gitignore` (add if absent)
  - [ ] Smoke-test: `bd list --json` returns empty array without error
  - [ ] Commit: `chore(beads): initialize beads substrate for dual-write spike`

- [ ] Task 2: Dual-write in sprint-manager workflow (AC: 3)
  - [ ] Read `skills/momentum/skills/sprint-manager/workflow.md` fully before modifying
  - [ ] Add beads mirroring calls to `status_transition` action: after writing `index.json`, call `bd update <bead-id> --status <mapped-status>` — map Momentum statuses to beads status categories (backlog→backlog, ready-for-dev→active, in-progress→wip, review/verify→wip, done→done, dropped/closed-incomplete→frozen)
  - [ ] Add beads creation call to `sprint_plan` action: for each story in the sprint plan, call `bd create "<title>" --type task --deps blocks:<sprint-bead-id>` and store the resulting bead ID in a sidecar `.momentum/beads-id-map.json` (slug → bead ID) — this map is the canonical link between Momentum slugs and beads hash IDs
  - [ ] Add epic mirroring: create epic-type beads with `bd create "<epic-title>" --type epic` and use `--parent <epic-bead-id>` on story beads
  - [ ] Add feature mirroring: create feature epic-type beads with `bd create "<feature-title>" --type epic` and add `relates-to` edges from story beads to feature beads
  - [ ] Verify dual-write doesn't break existing sprint-manager behavior — `index.json` remains authoritative and is always written first; beads write is best-effort (log failure, don't abort)
  - [ ] Commit: `feat(skills): sprint-manager dual-write to beads shadow layer`

- [ ] Task 3: Drive sprint-dev dependency from `bd ready --json --claim` (AC: 4)
  - [ ] Read `skills/momentum/skills/sprint-dev/workflow.md` Phase 1 (Initialization step) fully
  - [ ] After building `{{story_depends_on_map}}` from `index.json`, call `bd ready --json --claim` and store as `{{bd_ready_result}}`
  - [ ] Compare `{{bd_ready_result}}` against the existing wave/depends_on graph: log discrepancies (stories in one but not the other)
  - [ ] Use `bd ready --json --claim` as primary source for unblocked stories in Phase 2; fall back to wave/depends_on graph if `bd ready` errors or returns empty
  - [ ] Mark the fallback clearly in workflow.md with a comment: `<!-- SPIKE: falls back to wave/depends_on if bd ready --claim unavailable -->`
  - [ ] Verify that `--claim` produces an atomic acquisition — run two concurrent `bd ready --claim` calls on a sprint with one unblocked story; confirm only one caller receives the story
  - [ ] Commit: `feat(skills): sprint-dev Phase 1 uses bd ready --json --claim for dependency resolution`

- [ ] Task 4: Wire `bd prime` via SessionStart hook (AC: 6)
  - [ ] Create `.beads/PRIME.md` with Momentum protocol content:
    - Git-discipline rules summary (no autonomous push; conventional commits; push needs approval)
    - Sprint state reminder (sole writer: sprint-manager; never write stories/index.json or sprints/index.json directly)
    - Beads discipline: use `bd create/update/dep add` via sprint-manager, not directly; `bd dolt push` is NEVER called autonomously — Momentum owns sync
  - [ ] Add SessionStart hook entry to `.claude/settings.json` (merge, don't append) calling `bd prime --no-git-ops`
  - [ ] Verify: session startup shows `bd prime` output (Momentum PRIME.md protocol) without triggering `bd dolt push`
  - [ ] Commit: `feat(rules): wire bd prime via SessionStart hook with no-git-ops constraint`

- [ ] Task 5: Route discovered work via `discovered-from` (AC: 5)
  - [ ] Read `skills/momentum/skills/intake/workflow.md` fully
  - [ ] Add a beads dual-write path: when a new story is captured via intake, also call `bd create "<title>" --deps discovered-from:<origin-bead-id>` — origin bead ID is resolved from `.momentum/beads-id-map.json` using the source story slug (if available); otherwise use a sentinel `bd-discovery-root` bead
  - [ ] Write the new bead ID back to `beads-id-map.json`
  - [ ] This path is additive — the existing `intake-queue.jsonl` append is NOT removed during the spike
  - [ ] Commit: `feat(skills): intake dual-writes discovered work to beads with discovered-from dep`

- [ ] Task 6: Add `--spec-id` to every story bead (AC: 7)
  - [ ] Update sprint-manager Task 2 changes to include `--spec-id .momentum/stories/{slug}.md` on every `bd create` call for story beads
  - [ ] Verify: `bd show <bead-id>` displays `spec_id` pointing to the correct `.md` path
  - [ ] No story content is written to Dolt bead body beyond title and spec-id link
  - [ ] Commit: `feat(skills): add --spec-id linkage to all story bead creates in sprint-manager`

- [ ] Task 8: Regression validation — JSON-backed path (AC: 10)
  - [ ] After all dual-write modifications are in place, run sprint-manager with a test story and verify `stories/index.json` is correctly written before any beads call
  - [ ] Simulate a beads failure (e.g., kill the bd process or use an invalid bead ID) and confirm sprint-manager completes the JSON write and logs the failure without halting
  - [ ] Run sprint-dev Phase 1 with beads unavailable (set `bd ready` to return an error) and confirm fallback to wave/depends_on graph executes correctly
  - [ ] Document regression verification results in Dev Agent Record
  - [ ] Commit: `test(skills): verify JSON-backed path regression-free after beads dual-write`

- [ ] Task 7: Write spike research artifact (AC: 8, 9)
  - [ ] After running one real sprint with the dual-write layer active, write `docs/research/beads-dual-write-spike-findings-{date}.md`
  - [ ] Document factual observations for each of the 4 gate criteria (not just assertions — cite specific examples, discrepancies found, operational friction encountered)
  - [ ] Record the go/no-go recommendation with evidence
  - [ ] Commit: `docs(research): beads dual-write spike findings and gate evaluation`
  - [ ] Update DEC-028 `status` from `decided` to `decided` (unchanged) but add a `spike_completed` note if go, or `deferred` if no-go

## Dev Notes

This is a Momentum-internal spike. All modifications are to `skills/momentum/skills/` skill files — no user-facing functionality changes in the spike phase.

### Critical: `index.json` stays authoritative

The entire spike is predicated on `index.json` never being displaced as the authoritative store. The dual-write is additive. If beads is unavailable, misconfigured, or returns errors, sprint-manager and sprint-dev must continue to function exactly as before. Beads write failures MUST be logged (to `.momentum/handoffs/beads-errors-{date}.md` or similar) but MUST NOT abort the primary JSON write or raise exceptions that halt the skill.

### beads ID mapping

Momentum uses human-readable slugs (`beads-dual-write-spike`). Beads uses hash IDs (`bd-a3f8...`). The bridge is `.momentum/beads-id-map.json` — a flat JSON object mapping `slug → bead_hash_id`. Sprint-manager owns this file as an additional write target during the spike. It is NOT tracked in `stories/index.json` or `sprints/index.json`.

**`beads-id-map.json` is git-tracked during the spike** — it must NOT be gitignored. This file is Momentum's own translation layer, not Dolt data. Keeping it in git ensures the slug↔hash bridge is reviewable alongside the research artifact (AC 8, 9) and can substantiate Gate 4 auditability. Once the spike succeeds and beads becomes authoritative, the map can be retired. Only the `.beads/` directory (the actual Dolt DB) is gitignored.

### `bd ready --json` output format

The `bd ready --json` command returns an array of beads that are unblocked (all blockers done). Each entry includes the bead ID and title. Sprint-dev must map bead IDs back to story slugs using `beads-id-map.json` before scheduling.

### Hook format for `bd prime`

The `.claude/settings.json` SessionStart hook entry follows the established hook format in this project. The command is `bd prime --no-git-ops`. `--no-git-ops` prevents beads from injecting `bd dolt push` into the `bd prime` protocol output.

### What doesn't change

- `.momentum/stories/*.md` files: never touched by beads; they remain the spec of record
- AVFL, code-reviewer, qa-reviewer, e2e-validator, architecture-guard: untouched — the quality practice layer is unaffected
- `intake-queue.jsonl`: still written as before (dual-write, not replacement)
- Approval-SHA gates, workflow-fidelity rules: unchanged

### Architecture compliance

All modifications stay within the established sole-writer model:
- Sprint-manager remains the sole writer of `stories/index.json` and `sprints/index.json`
- Intake remains the sole writer of `stories/{slug}.md` for new stories
- Beads writes (`bd create/update/dep add`) are performed by the same sole-writer skill that owns the corresponding JSON write — never by a separate agent

### Beads version

Evaluated against beads v1.0.4 (Dolt-powered). Older JSONL-backed versions of beads are different software — do not confuse with earlier public information about beads. The `bd` CLI uses Dolt under `.beads/` (gitignored). Dolt sync (`bd dolt push`) is explicitly prohibited during the spike per the `--no-git-ops` constraint.

### References

- [Source: momentum/decisions/dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md]
- [Source: docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md]
- [Source: skills/momentum/skills/sprint-manager/workflow.md — Actions: status_transition, sprint_plan]
- [Source: skills/momentum/skills/sprint-dev/workflow.md — Phase 1: Initialization (dependency graph construction)]
- [Source: skills/momentum/skills/intake/workflow.md]
- [Source: architecture.md — Read/Write Authority table, Sole Writer model]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1 → config-structure (direct implementation)
- Tasks 2, 3, 5 → skill-instruction (EDD)
- Task 4 → rule-hook (functional verification)
- Tasks 6 → skill-instruction (EDD)
- Task 7 → specification (direct authoring)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

Tasks 2, 3, 5, 6 modify existing skill workflow.md files. **Do NOT use TDD for workflow.md files.** Use EDD:

**Before modifying any workflow.md:**
1. Write 2–3 behavioral evals in the skill's `evals/` directory (create if absent):
   - `eval-sprint-manager-mirrors-story-to-beads.md` (`skills/momentum/skills/sprint-manager/evals/`): Given sprint-manager activates a story, the beads shadow should have a corresponding bead with the correct status and spec-id.
   - `eval-sprint-manager-spec-id-links-to-story-md.md` (`skills/momentum/skills/sprint-manager/evals/`): Given sprint-manager creates a bead for a story slug, `bd show <bead-id>` must return `spec_id` equal to `.momentum/stories/{slug}.md`. This eval specifically validates the `--spec-id` linkage path.
   - `eval-sprint-dev-uses-bd-ready-claim-for-unblocked-stories.md` (`skills/momentum/skills/sprint-dev/evals/`): Given a sprint with dependencies, sprint-dev Phase 1 calls `bd ready --json --claim` and selects unblocked stories from that result (falling back to wave graph if empty). Verify `--claim` produces atomic acquisition (second concurrent call on same story receives empty or different story).
   - `eval-intake-routes-discovered-work-with-discovered-from.md` (`skills/momentum/skills/intake/evals/`): Given a new story captured via intake when beads is active, a bead is created with `discovered-from` edge to the origin bead (not a generic `blocks` edge — verify the edge type semantically).
2. Implement the workflow.md changes.
3. Verify evals by spawning Agent subagents with the eval scenario + modified skill context.

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters — this spike does NOT create new SKILL.md files, but if any are edited, verify
- `model:` and `effort:` frontmatter fields must remain present
- workflow.md files must stay under 500 lines / 5000 tokens (overflow to `references/`)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written per modified skill
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] Dual-write path confirmed to not abort primary JSON write on beads failure

---

### config-structure Tasks: Direct Implementation

Task 1 (beads initialization) needs no tests or evals. Implement directly:
1. Install `bd` via mise or Homebrew
2. Run `bd init --quiet`
3. Verify `.beads/` in `.gitignore`
4. Validate `bd list --json` returns `[]` without error

**DoD items:**
- [ ] `bd list --json` returns valid JSON without error
- [ ] `.beads/` present in `.gitignore`

---

### rule-hook Tasks: Functional Verification

Task 4 (SessionStart hook for `bd prime`):
1. Write the hook entry and `.beads/PRIME.md`
2. State the expected behavior: "On SessionStart, `bd prime --no-git-ops` runs and outputs Momentum protocol content. No `bd dolt push` command is injected."
3. Verify: trigger a new session and confirm `bd prime` fires without autonomous push

**Format requirements:**
- Hook entry in `.claude/settings.json` follows established hook schema (merge, don't append)
- `.beads/PRIME.md` follows markdown format — no YAML frontmatter needed

**Additional DoD items:**
- [ ] Expected behavior stated as testable condition in Dev Agent Record
- [ ] Functional verification performed: session started, `bd prime` fired, no autonomous push

---

### specification Tasks: Direct Authoring

Task 7 (research artifact) is a specification task. Write directly:
1. Run one real sprint with the dual-write layer active
2. Document factual observations per gate criterion — not assertions
3. Record go/no-go recommendation with evidence
4. Verify: cross-references to DEC-028 gate criteria resolve correctly

**Additional DoD items:**
- [ ] All four gate criteria addressed with factual evidence
- [ ] Go/no-go recommendation stated with supporting evidence
- [ ] Path to DEC-028 resolves correctly in cross-references

---

**Gherkin spec reminder:** Gherkin specs for this sprint live in `sprints/{sprint-slug}/specs/` — off-limits to the dev agent. Implement against the plain English ACs above only (Decision 30 black-box separation).

## Dev Agent Record

### Agent Model Used

_to be filled by dev agent_

### Debug Log References

### Completion Notes List

### File List
