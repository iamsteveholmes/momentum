# Eval: Triage Never Delegates to momentum:distill

## Purpose

Verify that `momentum:triage` never spawns `momentum:distill`, regardless of the nature
of the observations being classified.

## Scenario

A developer invokes `/momentum:triage` with observations that are clearly practice
improvements — the type that formerly would have been classified as DISTILL:

1. "The impetus dispatch.md has a stale row for momentum:distill — remove it"
2. "Add a rule to retro skill that says Phase 5 routes all findings to stubs"
3. "The partner.md quality concern entry mentions momentum:distill — needs cleaning"

All three are small, targeted improvements to practice files — exactly the kind of item
previously routed to DISTILL.

## Expected Behaviors

### B1: All Items Classified as ARTIFACT

Each observation is classified as ARTIFACT (a backlog story to implement), not DISTILL.
Practice improvements are now sprint stories or quick-fix tasks — they route through intake,
not direct distillation.

### B2: No DISTILL Invocation in Step 5

When Step 5 (Execute approved actions) runs, it processes ARTIFACT items by spawning
`momentum:intake` per item. It does not invoke `momentum:distill` at any point.

### B3: No DISTILL Spawn Code in Workflow

The workflow's Step 5 execution block does not contain:
- "spawn momentum:distill"
- "DISTILL items — spawn momentum:distill per item"
- `{{distill_results}}` or `{{distill_count}}` variables

### B4: Triage Summary Shows Only intake/decision/queue Delegations

The final triage summary shows:
- Stubbed to backlog (N): items sent to momentum:intake
- Decisions recorded (N): items sent to momentum:decision
- Parked to practice-ledger.jsonl: shaping/deferred/rejected counts
- No "Distilled (N)" section in the summary

---

## Pass Criteria

- [ ] All three observations classified as ARTIFACT
- [ ] Step 5 executes only intake, decision, and queue-append delegations
- [ ] `momentum:distill` not invoked at any point
- [ ] `{{distill_results}}` and `{{distill_count}}` not referenced
- [ ] Triage summary contains no "Distilled" section

## Failure Criteria

- Any observation classified as DISTILL
- `momentum:distill` spawned in Step 5
- `{{distill_count}}` appears in triage summary output
- Triage workflow references DISTILL class in its routing logic
