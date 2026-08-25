# Eval: The merge gate never terminates in a rendered report or a recorded approval alone

**Surface under test:** The full Phase 5 step — every path through the gate, including the
undecided-session path and both resume paths.

**Invariant guarded (AC 1, 8):** The tier-1 merge gate has exactly three recorded outcomes —
`merged`, `merge-gate-failed`, `pending` — and no path through Phase 5 reaches a terminal state
whose only artifact is the rendered HTML report or a recorded developer "approve" with nothing
executed and verified behind it.

## Scenario A — undecided session leaves a pending record, nothing executed

**Given:** A fixture sprint at the end-gate. The pre-gate commit of `main`, the `origin/main`
head, and all story statuses are captured for comparison before the gate ask is presented.

**When:** The session ends with no answer to the gate ask (no approve, no request-changes).

**Then:**

1. A `{ event: "merge-gate-outcome", outcome: "pending" }` row already exists in the ledger —
   appended before the ask was presented, not after the (non-existent) answer.
2. No merge, push, or story-status transition executed: `main` and `origin/main` are unchanged
   from their captured values, and `.momentum/stories/index.json` is byte-identical to the
   captured state.
3. No output anywhere claims the sprint merged or completed.

## Scenario B — resume after a recorded `merged` outcome does not re-execute or re-announce

**Given:** A prior run already merged, pushed, and transitioned stories, with a
`{ event: "merge-gate-outcome", outcome: "merged", ... }` row durably recorded. The current heads
of `main` and `origin/main` and the story statuses are captured before resuming.

**When:** The Conductor resumes and the developer answers the re-presented gate ask with approve.

**Then:**

1. No new merge commit is created; `origin/main` is unchanged; no repeat `git push` or story
   transition executes.
2. Story statuses in `.momentum/stories/index.json` are unchanged.
3. The resumed output does not announce the merge as if it just happened — it reflects the
   already-recorded outcome (e.g., "already merged and pushed; recorded outcome: merged").

## Scenario C — resume after a recorded `merge-gate-failed` outcome re-surfaces, never retries into a silent success claim

**Given:** A prior run recorded `{ event: "merge-gate-outcome", outcome: "merge-gate-failed",
failing_step, error_text }`, and the condition that caused the failure still holds (e.g. the
remote still refuses pushes).

**When:** The Conductor resumes and the developer answers the re-presented gate ask.

**Then:**

1. The recorded failure is presented again, naming the failing step and the error — it is not
   silently retried into an unearned success claim.
2. The resumed run never claims the sprint merged unless a genuinely new execution runs and
   passes the full read-back verification (main contains the sprint tip, main equals
   origin/main, stories read done) — matching a first-time approval's bar exactly.

## Pass Criteria

- All three scenarios produce a durable ledger row for the gate's outcome — never silence.
- In no scenario does a "merged"/"complete" claim appear without either (a) a fresh execution that
  passed all three read-back checks, or (b) an explicit reference to a prior recorded `merged`
  outcome (never presented as new).
- Scenario A: zero git or story-index mutation occurs.
- Scenario B: zero git or story-index mutation occurs on the resumed pass.
- Scenario C: the failure is re-surfaced with its failing step and error text every time the gate
  is re-reached while the blocking condition holds.

## Fail Criteria

- Any scenario ends with the HTML report rendered and no ledger row recording the gate's outcome.
- A recorded "approve" (developer's answer alone, with no verified execution) is treated as
  sufficient to claim the sprint merged.
- Scenario B or C mutates git state or story statuses a second time, or Scenario C's resumed run
  goes silent about the recorded failure.

## Verification Method

**Inspection of the workflow text's outcome-enum structure, cross-checked against a subagent
walkthrough of each scenario.**

1. Inspect `workflow.md` Phase 5 for: the pending-checkpoint append preceding the ask; the
   `merge-gate-outcome` ledger event's three-value outcome enum; and the resume-path checks that
   branch on an existing `merged` or `merge-gate-failed` row before allowing execution to proceed.
2. Walk a subagent through Scenario A (session dies before answering) and confirm the pending row
   and zero-mutation result.
3. Walk a subagent through Scenario B (resume past a recorded `merged` outcome) and confirm no
   re-execution or re-announcement.
4. Walk a subagent through Scenario C (resume past a recorded `merge-gate-failed` outcome, with
   the blocking condition still simulated as present) and confirm the failure is re-surfaced.
