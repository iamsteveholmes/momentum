# Eval: Resume after approve skips re-merge and re-transition

## Scenario A — full approve-side completion (Phase 5 checkpoint)

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

## Scenario B — crash mid-sequence, inside a single story's two-step transition

Given the same Phase 5 approve pass as Scenario A, but the session died narrower: the sprint→main
merge and branch delete completed, and story `story-x` (in `{{merged}}`) had its Step 1 transition
applied (`momentum-tools sprint status-transition --story story-x --target verify`, moving it from
`review` to `verify`) — but the session was killed before Step 2 (`--target done`) ran, and before
the `end-gate-phase-complete` row was appended. `story-x`'s status is therefore `verify`, not
`review` and not `done`, when the session dies.

**When** the developer re-invokes `/momentum:conduct` on the same sprint,

**Then:**
1. No `end-gate-phase-complete` row exists yet, so the resumed session re-enters the
   first-time-approve branch (not the RESUME PAST APPROVAL branch).
2. For `story-x`, the transition logic reads its CURRENT status fresh (`verify`, not the stale
   `review` that {{story_map}} may hold from earlier in the build) and runs ONLY Step 2:
   `momentum-tools sprint status-transition --story story-x --target done`.
3. Step 1 (`--target verify`) is NOT re-attempted for `story-x` — re-running it from `verify`
   would be a non-adjacent `verify` → `verify` transition, which the state machine rejects as
   invalid (per `validate_transition`'s adjacency check).
4. `story-x` ends the resumed pass at `done`, matching what an uninterrupted single run would
   have produced. Every other story in `{{merged}}` still at `review` runs both steps normally.
5. The `end-gate-phase-complete` checkpoint is appended once all stories reach their terminal
   status, exactly as in an uninterrupted run.

## Expected outcome

- **PASS**: In Scenario A, no merge/branch-delete/transition mutation is re-attempted, no error
  occurs, and the final "Sprint `sprint-2026-07-13` complete" output and push flow are still
  presented. In Scenario B, `story-x` resumes from its true current status (`verify`) and reaches
  `done` via a single valid transition, with no invalid `verify` → `verify` attempt.
- **FAIL**: The resumed session attempts `git merge sprint/sprint-2026-07-13` or a per-story
  terminal transition that either errors, or silently mutates state a second time in a way that
  diverges from a single uninterrupted run — including Scenario B's `story-x` case, where blindly
  re-running Step 1 from `verify` produces an invalid transition error.
