# Eval: Clean Run Pauses at Exactly Three Designed Gates

## Setup

A `momentum:sprint-planning` session runs end to end on a clean input:
- The backlog has 3 candidate stories, all with dependencies already satisfied (each
  `depends_on` entry is either empty or status `done`).
- All 3 stories get selected, flesh out cleanly (no revisions needed), and are approved
  on the first A/R/J prompt.
- Contract authoring, the adversarial guard, Gherkin generation, and spec-impact analysis
  all complete clean (guard reports `GUARD_CLEAN` on the first pass; no missing artifacts).
- Team composition resolves every specialist domain to an existing guidelines file, and
  every required role (Dev, QA Reviewer, E2E Validator, Architect Guard) has an existing
  agent file — Step 5.5's validation finds no gaps.
- AVFL (Step 6) returns `CLEAN` on the first run.
- The developer approves the plan gate on first presentation with zero genuine forks
  (or all forks signed off in one pass).

## Expected Behavior

The workflow proceeds continuously from invocation to `momentum-tools sprint activate`
and blocks for developer input at exactly three points:

1. **Story selection** (Step 2) — the `<ask>Select 2-8 stories...` prompt.
2. **Per-story A/R/J approval** (Step 3) — the `<ask>Your decision [A/R/J]:</ask>` prompt,
   once per story.
3. **Plan-gate sign-off** (Step 7) — the `<ask>Your decision [A/M/R]:</ask>` prompt.

No other step emits a blocking `<ask>` on this clean-run path. Specifically:
- The dependency-warning check in Step 2 does not fire (no warnings exist on this input),
  and even if it did, it must surface as a notice and continue rather than ask.
- The Guidelines Verification Gate (Step 5) and Team Composition Validation gate (Step 5.5)
  do not present a choice prompt, because their trigger conditions (missing guidelines,
  composition gaps) are false on this clean input.
- The AVFL checkpoint (Step 6) reports `CLEAN`, so neither the `CHECKPOINT_WARNING` notice
  nor the `GATE_FAILED` HALT branch fires.
- The adversarial guard (Step 3.5 Phase C) reports `GUARD_CLEAN` on the first pass, so the
  contaminated-contracts halt/ask branch never triggers.
- The cross-story seam coherence check (Step 3.6) finds no seam mismatches
  (`{{coherence_failures}}` empty on this clean input), so it emits only a non-blocking `✓`
  notice and continues — it never asks. Its clean result also carries downstream: the Step 7
  gate raises no mandatory coherence fork, and the Step 8 activation coherence gate finds zero
  open failures and imposes no activation hold or override prompt.

The run reaches `## ✓ Sprint {{sprint_slug}} Activated` without the orchestrator inserting
any of its own additional confirmation pauses between steps.

## Verification

- Count the blocking `<ask>` resolutions actually presented to the developer during the
  run: exactly 3 (selection, A/R/J once per approved story batch counts as one gate type,
  plan-gate sign-off).
- No "proceed or revise?" / "address now or proceed?" style prompt appears anywhere else
  in the transcript.
- The workflow's own `<critical>` continuous-execution directive (top of workflow.md) is
  honored: the session does not stop to ask "should I continue to the next step?" between
  Steps 1, 3.5, 3.6, 4, 4.5, 5, 6, or 8.
