# Eval: Cross-Story Seam Coherence — Activation Blocked, Then Override Recorded

**ID:** eval-activation-blocked-then-override-recorded
**Change-type:** skill-instruction
**Phase:** Step 8 (activate the sprint) pre-activation coherence gate

## Scenario A — no override: sprint held

Given `coherence-report.md` for the current sprint lists one open coherence failure between
`story-a` (consumer) and `story-b` (producer), and the developer has given no explicit
instruction to proceed despite it (no override language in the Step 7 pasted decision block,
no explicit instruction at the Step 8 prompt)

When Step 8's pre-activation coherence gate check runs

Then:
1. `momentum-tools sprint activate` is NOT called
2. The developer-facing output states the sprint is held because of the open mismatch,
   naming `story-a` and `story-b`
3. The workflow halts at this gate rather than proceeding silently

## Scenario B — explicit override: sprint goes live, override recorded

Given the same open failure, and the developer explicitly instructs the run to proceed
despite it (either via override language in the Step 7 fork verdict, e.g. "Override — ship it,
follow-up story tracks the fix," or via an explicit instruction at the Step 8 prompt)

When Step 8's pre-activation coherence gate check runs

Then:
1. The sprint proceeds to activation (assuming no other gate blocks it)
2. `coherence-report.md`'s "## Override Decisions" section gains a new entry recording: a
   timestamp, the consumer→producer pair that was open, and the developer's verbatim override
   instruction
3. This record is durable — reading `coherence-report.md` after the run shows the override
   occurred and what it applied to, without needing any other context

## Pass Criteria

- Scenario A: no activation call, explicit hold message naming both slugs
- Scenario B: activation proceeds AND `coherence-report.md` shows a new Override Decisions
  entry naming the pair and quoting (or closely paraphrasing) the developer's instruction
- A bare "A" (approve) with no override language, and no per-fork verdict text, does NOT count
  as an override in Scenario A — the gate still holds

## Fail Criteria

- Scenario A: sprint activates despite the open, unresolved mismatch and no explicit developer
  instruction to proceed
- Scenario B: sprint activates but no trace of the override decision exists anywhere in
  `coherence-report.md` (or elsewhere in the sprint's durable record)
- An override is inferred from silence or from a generic approval that never mentions
  proceeding despite the mismatch
