# Eval: Impetus Dispatch Routes Practice Fixes via Two-Lane Model

## Purpose

Verify that `momentum:impetus` (Partner mode) routes developer intent to apply a practice
fix via the two-lane model — urgent fixes go to `momentum:quick-fix`, non-urgent fixes
become sprint stories via `momentum:create-story`. No routing to `momentum:distill` exists.

## Scenario

### Scenario A — Urgent Practice Fix

A developer says to Impetus:
> "I just noticed the retro skill still references Tier 1 routing in Phase 5 — that's
> stale and wrong. I want to fix it now."

This is an urgent, single-story fix to a practice skill.

### Scenario B — Non-Urgent Practice Improvement

A developer says to Impetus:
> "After this sprint, we should add a rule that AVFL evals must be written before
> skill files are modified. Not urgent — just a future improvement."

This is a non-urgent practice improvement suitable for the backlog.

### Scenario C — Quality Concern

A developer says to Impetus:
> "Something feels off about the output from the last retro — the findings don't match
> what I saw in the transcript."

This is a quality concern about retro output.

## Expected Behaviors

### B1: Scenario A Routes to momentum:quick-fix

Impetus suggests `momentum:quick-fix` for the urgent retro fix. The dispatch table row
for "apply a retro finding / urgent practice fix" points to `momentum:quick-fix`.
No mention of `momentum:distill` appears.

### B2: Scenario B Routes to Sprint Story Creation

Impetus suggests creating a sprint story via `momentum:create-story` for the non-urgent
improvement. The suggestion includes framing it as a backlog item for the next sprint,
not immediate application.

### B3: Scenario C Routes to AVFL or upstream-fix

For the quality concern (Scenario C), Impetus suggests `momentum:avfl` or
`momentum:upstream-fix` depending on what's known. `momentum:distill` is not suggested.

### B4: No momentum:distill in Dispatch Table

The dispatch table (dispatch.md) does not contain a row mapping any intent to
`momentum:distill`. The row "Apply a retro finding to rules, skills, or refs → momentum:distill"
has been replaced with two-lane guidance.

### B5: Dispatch Precision

Impetus confirms intent with one sentence before dispatching. It does not dispatch
without a yes from the developer.

---

## Pass Criteria

- [ ] Scenario A: Impetus suggests `momentum:quick-fix`, not `momentum:distill`
- [ ] Scenario B: Impetus suggests `momentum:create-story` for backlog, not `momentum:distill`
- [ ] Scenario C: Impetus suggests `momentum:avfl` or `momentum:upstream-fix`, not `momentum:distill`
- [ ] Dispatch table contains no row pointing to `momentum:distill`
- [ ] No mention of `momentum:distill` in any Impetus routing response

## Failure Criteria

- Impetus suggests `momentum:distill` for any scenario
- Dispatch table still contains a `momentum:distill` row
- Partner mode lists `momentum:distill` as an option for quality concerns
