# Eval: stage-2 silent-downgrade guard rejects a diff-only VERIFIED report and re-runs/escalates

## Scenario

Given a dedicated-run story S whose frozen contract Part-A header declares an executable
`verification_method` (e.g. `verification_method: smoke`), and REVIEWER A (qa-reviewer) returns a
QA Review Report for S that:

- States `**Verification Method:** smoke | **Driver:** Maestro` in its header (matching the
  contract), AND
- Marks every AC `VERIFIED`, but every AC's Evidence field cites only a diff line / file:line
  reference (e.g. `src/ui/SettingsScreen.kt:42`) with no build result, launch confirmation, or
  driven-scenario output anywhere in the report.

A second, separately submitted report for a different dedicated-run story T (same
`verification_method: smoke`) returns overall Verdict `BLOCKED`, naming a genuinely unavailable
prerequisite (e.g. "no Android emulator reachable").

## Expected Behavior

The Conductor's stage-2 REVIEWER A RETURN VALIDATION / silent-downgrade guard should:

1. For story S: detect the silent downgrade (contract's `verification_method` is executable, and
   VERIFIED ACs cite diff/source evidence only) and NOT bind `{{qa_findings}}` from that report.
2. Re-dispatch REVIEWER A once for S with a note that the prior report was rejected for
   VERIFIED-without-execution-evidence and must execute the routed method this time.
3. If the re-run for S is still a silent downgrade: treat it as a REVIEWER A failure — invoke the
   same pipeline-retry path already used for an unparseable REVIEWER A return (re-launch S's
   pipeline; on retry exhaustion, S is marked blocked and its terminal transition is deferred to
   Phase 5 approve). S does NOT advance to stage-3/merge on the rejected report.
4. For story T: accept the BLOCKED report as a legitimate outcome — normalize it per the existing
   NORMALIZE REVIEWER A action (BLOCKED → `severity: critical`) and proceed to stage-3 normally.
   T's BLOCKED verdict is never treated as the same failure class as S's silent downgrade.

## Invariants (must hold)

- Story S never reaches stage-3/merge on the basis of the rejected (diff-only VERIFIED) report.
- The guard fires only on the dedicated-run path (REVIEWER A actually executes) — it does not
  apply to, or alter, the covered-by-composition branch where REVIEWER A is never dispatched.
- Story T's genuine BLOCKED-with-named-prerequisite report is accepted without triggering the
  silent-downgrade guard, and BLOCKED continues to normalize to `severity: critical` unchanged.
- The existing NORMALIZE REVIEWER A action (base-field mapping, severity-from-verdict, `type`
  routing by `stakes_class`) and the covered-by-composition deferral branch are unaffected by the
  guard's presence — this is a regression check (AC7).

## How to Run This Eval

Spawn a subagent with the edited `skills/momentum/skills/conductor/workflow.md` stage-2 section as
its context (the REVIEWER A dispatch, RETURN VALIDATION, and silent-downgrade guard), the two
crafted QA Review Report strings above as REVIEWER A's simulated returns for S and T, and ask it
to trace through the stage-2 logic and report what it would do for each story. Observe its actual
reasoning and outcome — do not just re-read the workflow text and assume compliance.
