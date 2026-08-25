# Eval: A Bare Capability Approval Is Rejected — Written Reasoning Required

**ID:** eval-plan-gate-capability-bare-approval-rejected
**Change-type:** skill-instruction
**Phase:** Developer review (Step 7) — sign-off validation

## Scenario A: Developer pastes a decision block with a blank or single-character Fork 1 verdict

Given a plan gate rendered with the capability card as Fork 1 (per
`eval-plan-gate-capability-card-renders-first`), and the developer types "A" to approve

When the workflow asks the developer to paste the signed decision block, and the pasted block's
"Fork 1:" line is blank, or contains only a single character (e.g. "Fork 1: y")

Then:

1. The workflow rejects the paste and explains specifically that the capability verdict needs
   written reasoning naming the capability being accepted or amended — not just that "a fork line
   is missing text" generically.
2. The workflow does not proceed to Step 8 (activation).
3. The workflow re-asks for the pasted block.

## Scenario B: Developer pastes "Fork 1: approve all"

Given the same setup, and the pasted block's "Fork 1:" line reads exactly "approve all" (a
blanket approval with no reasoning naming the specific capability)

When the workflow validates the paste

Then:

1. The workflow rejects it — non-empty text alone does not satisfy the requirement; the text must
   name the capability being accepted or amended.
2. The workflow explains why the blanket phrase does not count and re-asks.

## Scenario C: Developer pastes a written, substantive verdict

Given the pasted block's "Fork 1:" line reads something like "approve — session-capture and
campaign-identity are the right pair to ship this sprint, matches what we scoped"

When the workflow validates the paste

Then:

1. The workflow accepts it as satisfying the capability verdict requirement.
2. If all other genuine forks (if any) also carry non-empty written verdicts, the workflow
   proceeds to Step 8.

## Pass Criteria

- Blank, single-character, and "approve all"-style bare verdicts on the capability fork are all
  rejected with an explanation.
- A written verdict naming the capability is accepted.
- Rejection never silently proceeds to Step 8.

## Fail Criteria

- A blank or single-character Fork 1 verdict is accepted because the pasted block is
  "non-empty overall".
- "approve all" or equivalent blanket phrasing passes validation for the capability fork.
- The workflow proceeds to Step 8 without a valid capability verdict recorded.
