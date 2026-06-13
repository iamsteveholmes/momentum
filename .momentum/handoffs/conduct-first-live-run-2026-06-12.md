# Handoff: First Live Conduct Run — sprint-2026-06-10 (Conductor Seam Fixes)

**Date:** 2026-06-12
**From:** Sprint-planning session (sprint-2026-06-10 planned, validated, activated)
**To:** Next session — run `/momentum:conduct`
**Commit anchor:** `23dacbf` on `sprint/sprint-2026-06-10` (pushed through `a5540e4`; `23dacbf` itself is local-only)

## Mission

Run the **first live `/momentum:conduct` build** for the active sprint `sprint-2026-06-10` —
five conductor seam-fix stories, single wave, no inter-story dependencies. The developer
accepted the chicken-and-egg risk: the Conductor fixes its own seams on its maiden run.
Invoke `/momentum:conduct` (or say "run the sprint build" — Impetus dispatches there).

## Pre-flight

1. No plugin update needed: installed marketplace copy and repo `skills/` are identical at
   v0.28.0 (verified at planning time; nothing under `skills/` changed since).
2. Fresh session per standing practice — this handoff is written for it.
3. The repo is already checked out on `sprint/sprint-2026-06-10` (pushed, upstream set).
   Conduct's H5 guard expects exactly this.

## Sprint State (all persisted in `.momentum/sprints/index.json`)

- **Active sprint:** `sprint-2026-06-10`, started 2026-06-11. Five stories, all approved
  (SHA-recorded), all `ready-for-dev`, all Wave 1.
- **Stories:** `conduct-build-state-persistence-and-resume` (critical),
  `conduct-worktree-and-branch-creation` (high),
  `conduct-dev-commit-authority-reconciliation`,
  `conduct-qa-reviewer-normalization-adapter`,
  `conduct-coverage-deferral-preserve-code-review`.
- **Contracts:** one frozen `.eval.yaml` per story in
  `.momentum/sprints/sprint-2026-06-10/specs/` — all `skill-invoke`, SHA-256s frozen in
  `planning.team.story_assignments`, GUARD_CLEAN. Dev agents read Part-A headers only.
- **Coverage:** all five `dedicated-run`, zero covered-by-composition (deliberate — see
  `coverage-plan.md`; the composition path carries the very defect story 5 fixes).
- **Team:** dev-skills specialist on every story (guidelines `.claude/rules/dev-skills.md`);
  QA Reviewer + E2E Validator + Architect Guard at review.
- **can_merge_independently:** true for persistence/worktree/commit-authority; false for
  qa-adapter and coverage-deferral (external depends_on, all `done`).

## CRITICAL — the engine still carries the defects it is fixing

The installed Conductor (v0.28.0) has all five seam defects DURING this run. Compensate by hand exactly as the rehearsal sprints did:

1. **No worktree/branch creation step (story 2's defect).** The workflow passes
   `worktree_path: .worktrees/story-{slug}` but never creates it. At each story launch the
   Conductor must explicitly run: `git branch story/{slug} sprint/sprint-2026-06-10` then
   `git worktree add .worktrees/story-{slug} story/{slug}` — base = sprint tip, NEVER main.
   Stale leftovers: `git worktree remove --force` + `git branch -D`, then recreate.
2. **No persistence (story 1's defect).** Hand-maintain an append-only ledger at
   `.momentum/sprints/sprint-2026-06-10/build-ledger.jsonl` — one JSON row per
   state-bearing event (launch, stage transitions, each finding disposition, terminal
   outcomes, escalations), `story_slug` + `event` fields, enums per
   `skills/momentum/references/finding-schema.md` v1.1. This is the recovery net; stalls
   are the proven failure mode.
3. **Dev artifacts still instruct devs to commit (story 3's defect).** The spawn
   constraint ("Do not mutate git") conflicts with dev.md. If a dev returns with a CLEAN
   worktree and a new commit in `git log`, the write-scope guard was neutralized — treat
   as a seam mismatch: verify the committed diff against `writable_files` manually before
   merging; do not let `git add -u` staging nothing pass silently.
4. **qa-reviewer output is NOT canonical (story 4's defect).** Normalize manually before
   merging stage-2 findings, per the mapping table in the qa-adapter story's Dev Notes:
   BLOCKED→critical, MISSING→major, PARTIAL→minor (verdict only, never stakes);
   `type: security` iff stakes_class==security-auth-isolation else `spec-compliance`;
   `legitimate: true`, `source: "qa-reviewer"`, `suggested_fix: null`, `story_slug` from
   pipeline.
5. **Coverage-deferral skip defect (story 5) — moot this run:** every story is
   dedicated-run, so the broken skip path is never exercised. Do not mark anything
   covered-by-composition mid-run.

## Operational Warnings (carried from prior handoff + planning session)

- **Background-validator orphaning is real** (headless validators died with 0-byte output
  when the spawning turn ended). The Conductor has no watchdog. Recovery: run the lens
  inline, or SendMessage the stalled agent with a precise diagnosis.
- **Merge adjacency:** 4 of 5 stories touch `skills/momentum/skills/conductor/workflow.md`;
  2 touch `skills/dev/workflow.md`. Per-story rebase-then-ff + AVFL-on-merge is the
  mitigation; expect a cross-story drift reconciliation pass (precedent: `351b36c`, 9 drifts).
- **Sole-writer discipline:** `stories/index.json` mutations only via momentum-tools
  (sprint-manager authority). Status transitions only via `sprint status-transition`.
- **Single end-gate (DEC-035):** one developer ask at the end of the build. No mid-build
  prompts on the routine path; mid-flight escalation only per DEC-036 stakes/timing.
- **Known tooling defects (backlogged, do NOT fix mid-run):**
  `compute-verification-method` crashes on list-valued `change_type`, and empty
  `change_type` silently routes to document-review (stubs:
  `compute-verification-method-accepts-list-change-type`,
  `fail-loud-on-empty-or-unrecognized-change-type`). Route via verification-standard.md §1
  manually if needed.
- **Git:** commits autonomous (`type(scope):` format; skill markdown is code → `fix`/`feat`,
  not `docs`); NEVER push without explicit approval; `23dacbf` (intake stubs) is unpushed.
  Two campaign-init docs commits (`488d871`, `dbde69e`) on this branch are expected history.
- **On sprint completion/merge to main:** bump `skills/momentum/.claude-plugin/plugin.json`
  per the version-on-release rule (these are behavioral changes → minor bump to 0.29.0),
  then offer the push (approval required).

## Success Criteria

All five stories merged to `sprint/sprint-2026-06-10` with QA PASS + freeze MATCH, every
finding dispositioned and recorded, one end-gate report assembled and approved by the
developer, sprint completed via momentum-tools. The build ledger you hand-wrote becomes
the precedent input for verifying story 1's implementation.
