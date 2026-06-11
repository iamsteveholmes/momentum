# Coverage Plan — sprint-2026-06-10

**Anti-redundancy principle:** Never validate in isolation what an integrated scenario already exercises.

## Integration Scenarios

None planned this sprint — deliberately.

All five stories modify the conduct build machinery itself, and this sprint is the
first live conduct run. The one integration scenario that could plausibly discharge
them — "run a conduct build end-to-end and observe ledger/worktree/commit/review
behavior" — is exactly the artifact under repair, executed by the engine that still
carries the defects being fixed. Using it as a composition-discharge venue would be
circular: a defect in any fix would corrupt the discharge scenario itself. Worse,
the engine's covered-by-composition routing currently carries the precise defect
`conduct-coverage-deferral-preserve-code-review` exists to fix (the wholesale
skip of build-time review), so any story marked covered-by-composition in this
sprint would be routed through the known-broken path during this very build.

Every story therefore runs dedicated verification. Composition coverage becomes a
sound option again for future sprints once this sprint's fixes are merged.

## Dedicated-Run Stories

- `conduct-build-state-persistence-and-resume` — dedicated-run. Ledger append/resume/append-only behavior must be verified directly; it is the recovery net for this very build.
- `conduct-worktree-and-branch-creation` — dedicated-run. The unexecutable first step of the per-story pipeline; verified directly via git-observable state at story launch.
- `conduct-dev-commit-authority-reconciliation` — dedicated-run. The commit-authority seam must be verified on both sides directly; its silent-failure mode (guard staging nothing) is invisible to composition-level observation.
- `conduct-qa-reviewer-normalization-adapter` — dedicated-run. Field-shape totality of the producer→consumer mapping requires record-level inspection, not behavioral composition.
- `conduct-coverage-deferral-preserve-code-review` — dedicated-run. This story repairs the covered-by-composition path itself; it cannot be verified by the path it fixes.

## Validation

Five approved stories; each appears exactly once above; all five are dedicated-run;
zero stories covered-by-composition; zero integration scenarios (none needed — no
story is discharged by composition).
