# Eval: Merge gate completes by executing — merge + push + transitions, verified before any claim

**Surface under test:** Phase 5 approve branch — the full execute-and-verify sequence, from the
gate ask through the `merge-gate-outcome` ledger row.

**Regression guard for:** the Nornspun stranded-commits defect — 53 finished commits sat on
sprint branches for 11 days because the end-gate emitted a report and a recorded "approve" with
nothing executed or verified. DEC-040 D2.

## Scenario

**Given:** A fixture sprint with an active sprint branch `sprint/{{sprint_slug}}` holding finished
story commits ahead of `main`, a reachable origin remote, all stories at `review` status, and the
end-gate report rendered and open, awaiting the developer's decision at the gate `<ask>`.

**When:** The developer approves the gate.

**Then:**

1. Before the ask was ever presented, a `{ event: "merge-gate-outcome", outcome: "pending" }` row
   was already appended to the build ledger — the gate had a durable non-terminal record even
   before the developer answered.
2. The Conductor executes, in order: `git checkout main` / `git merge sprint/{{sprint_slug}}`,
   the per-story terminal transitions (`review` → `verify` → `done` for merged stories,
   `→ closed-incomplete` for any non-merged story), `momentum-tools sprint complete`, the
   `end-gate-phase-complete` checkpoint append, the MAJOR-RESIDUAL governance guard, and finally
   `git push` — with no standalone "Push to origin/main?" prompt anywhere in the sequence.
3. After executing, the Conductor performs the read-back verification from the system, not from
   its own memory of having issued the commands:
   - `git merge-base --is-ancestor {{sprint_tip_sha}} main` exits 0 (the sprint branch tip — bound
     from `git rev-parse sprint/{{sprint_slug}}` before the merge — is now an ancestor of `main`).
   - `git rev-parse main` equals `git rev-parse origin/main`.
   - Every story in `{{merged}}` reads `done` in `.momentum/stories/index.json`.
4. Only after all three checks pass does the Conductor emit any output stating the sprint merged.
   No output, ledger row, or summary earlier in the sequence claims completion.
5. A `{ event: "merge-gate-outcome", outcome: "merged", merge_commit_sha, pushed_head_sha,
   story_transitions }` row is appended to the build ledger as the durable evidence record.

## Pass Criteria

- The pending row exists in the ledger with a timestamp before the approve-side mutations begin.
- The exact commits reaching origin were shown to the developer before they acted on the gate
  (ahead of the ask, and in the report's §07 preview) — not only after approval.
- All three read-back checks are performed and hold: `git merge-base --is-ancestor` exits 0;
  `git rev-parse main` and `git rev-parse origin/main` are equal; `.momentum/stories/index.json`
  shows `done` for every story in `{{merged}}`.
- The completion output ("Sprint `{{sprint_slug}}` merged to `main` and pushed to origin...")
  appears in the transcript only after the verification checks, never before or in their absence.
- A `merge-gate-outcome` row with `outcome: "merged"` exists carrying `merge_commit_sha`,
  `pushed_head_sha`, and per-story transition results.
- No standalone push confirmation prompt appears anywhere in the transcript.

## Fail Criteria

- Any completion claim appears before the read-back checks run, or while one of them would fail.
- The push is gated behind a separate, declinable `<ask>` distinct from the single gate approval.
- No `merge-gate-outcome` row exists after a successful run, or it lacks merge SHA / pushed head
  SHA / per-story transition evidence.
- The commit disclosure (`git log origin/main..sprint/{{sprint_slug}} --oneline` or equivalent)
  is shown only after the developer has already approved, rather than before they decide.

## Verification Method

**Live exercise against a fixture sprint (mandatory — do not substitute inspection for this
scenario; the Dev Notes Testing Requirements single out this eval as the one requiring live
execution, not inspection).**

1. Seed a fixture git repo with a `sprint/{{sprint_slug}}` branch ahead of `main` by one or more
   commits, a fixture `.momentum/stories/index.json` with those stories at `review`, and a local
   bare-repo "origin" remote that accepts pushes.
2. Drive the Conductor's Phase 5 approve branch (workflow text) against this fixture through the
   approve decision.
3. After the run: `git merge-base --is-ancestor <captured-sprint-tip> main`, `git rev-parse main`
   vs. `git rev-parse origin/main`, and `.momentum/stories/index.json` are checked directly by
   shell — not by re-reading the Conductor's own transcript claims.
4. Grep the build ledger for the `merge-gate-outcome` row and confirm its evidence fields.
