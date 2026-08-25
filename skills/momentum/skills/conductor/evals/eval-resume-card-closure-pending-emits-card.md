# Eval: A refused sprint closure emits a closure-pending resume card

**Surface under test:** The tier-2 SPRINT CLOSURE GATE's refusal-handling RESUME-CARD REFRESH
action (workflow.md), per `references/resume-card.md`.

**Invariant guarded (AC 13):** When sprint closure is refused or left pending awaiting recorded
verdicts, the card is emitted or refreshed with its one question being the closure question —
naming which goal conditions still await a verdict and how to record one.

## Scenario

**Given:** A sprint whose tier-1 merge already succeeded (`merge-gate-outcome: "merged"`, and the
resume card already resolved with `resolution: "approved"` from that step), and whose
`momentum-tools sprint complete` call refuses closure because one or more `goal_conditions` lack a
recorded verdict.

**When:** The Conductor reaches the closure-refused branch of the SPRINT CLOSURE GATE.

**Then:**

1. `resume-card.json` is written/refreshed with `status: "pending"`, `phase: "closure"`.
2. `question.text` is the closure-verdict question, `question.gates` names the tier-2 closure gate,
   and `question.options` name the specific unverified/failing condition slugs (or the generic
   verify/close-manually/close-failed paths when no named conditions are present).
3. This is a NEW question relative to the already-resolved approve question — `waited_since` is
   bound fresh on first refusal, not carried forward from the resolved merge-gate card.
4. A repeat refusal on a later pass, for the same still-unresolved closure question, carries the
   existing `waited_since` forward unchanged rather than resetting it again.
5. Impetus's existing all-sprints pending scan (no read-side change required for this AC) surfaces
   this card at the next session start with no additional wiring.

## Pass Criteria

The card transitions from resolved (approve) to a freshly-pending closure question on first
refusal, and stays pending with a stable `waited_since` across repeated refusals of the same
outstanding conditions.

## Fail Criteria

No card is written on closure refusal; the closure question is missing `gates` or `options`;
`waited_since` resets on every repeat refusal instead of staying stable; the card is left
`resolved` (from the approve step) while a closure decision is genuinely still pending.

## Verification Method

Inspection of the SPRINT CLOSURE GATE refusal branch in `workflow.md` for the RESUME-CARD REFRESH
action and its fresh-vs-carried-forward `waited_since` logic, cross-checked with a subagent
walkthrough using a fixture sprint with one unverified `goal_conditions` entry.
