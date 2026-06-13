# Eval: Ledger append at state-bearing events

## Scenario

Given a conduct build is running for sprint `sprint-2026-06-10` with three stories (`story-a`, `story-b`, `story-c`), and the Conductor processes each story through the full pipeline (dev spawn, stage-2 review, stage-3 fix loop with two findings per story, merge), the skill should append a JSONL row to `.momentum/sprints/sprint-2026-06-10/build-ledger.jsonl` at every state-bearing event — not batched at phase end.

## Expected behavior

1. Each story launch (pipeline spawn at step 2.1) produces an immediate ledger append with an event field identifying it as a launch event and a `story_slug` field naming the story.
2. Each stage transition (stage-1 → stage-2 and stage-2 → stage-3 boundaries) produces an immediate ledger append with the event type and story slug. There are exactly two stage-transition boundaries per story pipeline; story-terminal covers the stage-3 completion event and does not produce a separate stage-transition append.
3. Each individual finding disposition (fixed, dismissed, escalated, triaged-out, blocked, scope-reverted) within step 2.S3 produces its own ledger append at the moment the disposition is recorded — not deferred to the story's terminal signal.
4. Each story terminal signal (merged or blocked/quarantined) produces a ledger append.
5. Escalation events (mid-flight and end-gate-expanded), coverage deferrals, coverage discharges, contract-integrity stops, and end-gate change-request events each produce their own ledger append.
6. The append mechanism is a single-line Bash printf to the ledger file — no new script or tool is introduced.
7. A simulated crash after story-b's merge but before story-c starts would leave the ledger containing all events for story-a and story-b but none for story-c — demonstrating event-time writes rather than phase-end batches.
