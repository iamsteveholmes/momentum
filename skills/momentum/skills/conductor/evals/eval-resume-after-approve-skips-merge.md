# Eval: Resume after approve skips re-merge and re-transition

## Scenario

Given a conduct build for `sprint-2026-07-13` reached Phase 5, the developer approved the
end-gate, the Conductor completed the sprint→main merge, deleted the `sprint/sprint-2026-07-13`
branch, transitioned all stories to their terminal statuses (`done` or `closed-incomplete`),
and appended an `end-gate-phase-complete` row to the build ledger — and the session was then
killed (or context-compacted) before the developer saw the final completion output,

**When** the developer re-invokes `/momentum:conduct` on the same sprint,

**Then:**
1. Step 2.0 rehydration recognizes the `end-gate-phase-complete` row is present in the ledger
   (PHASE CHECKPOINT RULE).
2. The resumed session reaches Phase 5 and, inside the `developer approves` branch, detects
   the existing `end-gate-phase-complete` row and does NOT re-attempt: `git checkout main` /
   `git merge sprint/sprint-2026-07-13` (the branch no longer exists — this would error),
   `git branch -d sprint/sprint-2026-07-13`, or any per-story `verify`→`done` /
   `closed-incomplete` transition (the stories are already at a terminal status — the state
   machine rejects re-transitioning from a terminal state without `--force`, per the
   terminal-to-terminal transition guard).
3. No error is raised about re-merging a missing branch or re-transitioning an already-done
   story.
4. The MAJOR-RESIDUAL GOVERNANCE GUARD still runs (it is independently idempotent via
   momentum:triage's own dedup gate) and the push summary / push-confirmation / completion
   output are still presented — the resumed build's final output is content-equivalent to
   what the interrupted session would have shown had it not died.
5. The end-gate report reopened in this session was re-rendered fresh from the ledger (not
   from stale in-context state) and matches the report an uninterrupted run would have
   produced for the same sprint.

## Expected outcome

- **PASS**: No merge/branch-delete/transition mutation is re-attempted; no error occurs; the
  final "Sprint `sprint-2026-07-13` complete" output and push flow are still presented.
- **FAIL**: The resumed session attempts `git merge sprint/sprint-2026-07-13` or a per-story
  terminal transition and either errors, or silently mutates state a second time in a way
  that diverges from a single uninterrupted run.
