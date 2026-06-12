# Eval: Resume rehydrates from ledger

## Scenario

Given a conduct build for sprint `sprint-2026-06-10` was interrupted after completing stories `story-a` and `story-b` (both merged), with `story-b` having produced two finding-disposition records (one fixed, one escalated to end-gate-expanded) and one mid-flight escalation on `story-a`, and the build ledger at `.momentum/sprints/sprint-2026-06-10/build-ledger.jsonl` contains all event rows from the prior session, and a fresh session re-invokes the Conductor for the same sprint, the skill should rehydrate all Conductor-scoped accumulators from the ledger before computing the frontier.

## Expected behavior

1. Step 2.0 detects the existing build ledger at `{{ledger_path}}` and replays its rows before the existing `{{merged}}` status-seed and in-progress reconcile run.
2. After rehydration, `{{build_log}}` contains all event records from the prior session (story launches, stage transitions, finding dispositions, terminal signals, escalations).
3. After rehydration, `{{end_gate_escalations}}` contains the end-gate-expanded finding from story-b's fix loop.
4. After rehydration, `{{escalations}}` contains the mid-flight escalation record from story-a.
5. After rehydration, `{{finding_dispositions}}` records from the prior session are recoverable from the ledger (the phantom store is closed — dispositions are sourced from durable ledger rows, not from the per-story transient variable that resets each story).
6. The existing status-based `{{merged}}` seeding still runs and is cross-checked against the ledger — the ledger provides the richer record (findings, dispositions, escalations) while story statuses provide the authoritative membership check.
7. Events already present in the ledger are not re-appended when their stories are not re-run (duplicate prevention).
8. The frontier computation proceeds normally with only `story-c` (and any other incomplete stories) in the frontier.
