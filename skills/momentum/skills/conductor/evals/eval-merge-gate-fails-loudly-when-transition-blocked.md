# Eval: Merge gate fails loudly when a transition cannot complete — never a success claim

**Surface under test:** Phase 5 approve branch — the bounded-failure routing added around merge
conflicts, story-status transitions, and push.

**Regression guard for:** the exact stranded-commits shape DEC-040 D2 names — an approval that
prints "complete" while origin has nothing, because the standalone push prompt was declined or
the push silently failed.

## Scenario A — push cannot land

**Given:** A fixture sprint identical to the success-path fixture, except its configured origin
remote is guaranteed to refuse the push (unreachable, unauthenticated, or read-only). The merge to
local `main` and the per-story terminal transitions can both complete normally — only the push
fails.

**When:** The developer approves the gate.

**Then:**

1. The merge, per-story transitions, `sprint complete`, and the `end-gate-phase-complete`
   checkpoint all execute and succeed (they do not depend on network access).
2. `git push` is attempted and fails.
3. The read-back verification detects `git rev-parse main` != `git rev-parse origin/main` (even
   if the push command's own exit code were somehow ambiguous, this check independently catches
   the failure — verification never trusts the issued command's apparent success).
4. The gate outcome is recorded as `merge-gate-failed` naming the failing step (`push`) and the
   actual captured error text from the failed `git push`.
5. The developer is told, in plain language, that the gate failed, which step failed, and what is
   now stranded and where — specifically that `main` locally (and the story statuses) already
   reflect the merge, but `origin/main` does not yet have it, so the work is stranded on the local
   checkout until the push can be retried.
6. No output anywhere in the run — not the push summary, not any intermediate note, not a final
   summary — contains a claim that the sprint "merged" or "completed."
7. If `momentum-tools sprint complete` succeeded before the push failure was detected, that
   success does NOT mask or replace the merge-gate-failed surfacing — the developer sees the
   merge-gate failure regardless of sprint-closure's own success.

## Scenario B — merge conflict exhausts the bounded retry budget

**Given:** A fixture sprint whose branch produces a merge conflict against `main` that cannot be
resolved by the autonomous conflict-resolution attempts within `{{MAX_FIX_ATTEMPTS}}` tries (e.g.
a fixture designed to always re-conflict).

**When:** The developer approves the gate.

**Then:**

1. The Conductor attempts autonomous conflict resolution and retries the merge, up to
   `{{MAX_FIX_ATTEMPTS}}` times — it does not retry unboundedly and does not HALT waiting for
   developer resolution mid-attempt.
2. After the bound is exhausted, the gate outcome is recorded as `merge-gate-failed` naming the
   failing step (`merge`) and the conflict detail (conflicting files / git error text).
3. No per-story transitions, sprint-complete call, or push are attempted — nothing merged, so
   nothing downstream proceeds.
4. No output claims the sprint merged or completed.

## Pass Criteria

- Scenario A: a `merge-gate-failed` record exists naming step `push` with real error text; the
  developer-facing message names the stranded state (local main / done stories vs. origin
  lacking the push) in plain language; a full-transcript grep finds no "merged to main" or
  "sprint ... complete" claim; a successful sprint-closure message (if present) does not stand in
  for surfacing the merge-gate failure.
- Scenario B: the retry bound is `{{MAX_FIX_ATTEMPTS}}`, not unbounded; a `merge-gate-failed`
  record exists naming step `merge` with the conflict detail; no transitions, sprint-complete, or
  push occurred after the bound was exhausted.

## Fail Criteria

- Any "merged"/"complete" claim appears in either scenario.
- The failure is recorded without naming the specific failing step, or without the underlying
  error/conflict text.
- Scenario B retries beyond `{{MAX_FIX_ATTEMPTS}}`, or falls through to per-story transitions and
  push despite the merge never completing.
- A successful `momentum-tools sprint complete` call is allowed to stand in the output as if it
  resolved or masked the merge-gate failure.

## Verification Method

**Inspection + targeted dry-run walkthrough (per Dev Notes Testing Requirements — failure paths
are hard to trigger live; a fixture with a rejected push or an engineered unresolvable conflict
may be simulated with a subagent walkthrough rather than a fully live push rejection).**

1. Inspect the workflow text for the bounded conflict-retry structure (a counter compared against
   `{{MAX_FIX_ATTEMPTS}}`, with a defined `merge-gate-failed` terminal branch when exhausted) and
   for the push failure / read-back-verification routing into the same `merge-gate-failed` path.
2. Walk a subagent through Scenario A using a simulated push rejection (e.g. a fixture remote
   configured to reject) and confirm the output and ledger row match the Then clauses above.
3. Walk a subagent through Scenario B using a simulated always-conflicting merge and confirm the
   bound is honored and no downstream steps execute.
