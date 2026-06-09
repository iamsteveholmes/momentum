---
title: Exercise the conduct escalation machinery end-to-end before trusting it
story_key: exercise-conduct-escalation-machinery-end-to-end
status: review
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Exercise the conduct escalation machinery end-to-end before trusting it

## Story
Drive the stakes-and-timing escalation machinery through its branches with real findings/evals, since it has never actually fired on a per-story mid-flight finding.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): the stakes-and-timing engine fired exactly once (post-merge AVFL only); of 105 findings, 104 were routine and 1 was high-blast-radius-architecture, with `timing_tier` 100% end-gate-expanded. The per-story mid-flight branch was never triggered by a real finding, and the stage-3 fix-loop verification was inspection-only. The machinery is largely untested in practice.

## What's needed
- A runtime/eval test drives a real stakes-class finding through the mid-flight loop.
- The end-gate-expanded vs mid-flight branch is exercised with both timing tiers.
- The bound-exhausted (BLOCKED) and escalated dispositions are each driven through the loop at least once.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related: `conduct-stakes-timing-escalation-mechanism` (done), `stakes-classification-rubric` (done), `stage3-fix-loop-via-directed-dev` (done)

## Dev Agent Record

### Completion Notes

Delivered `skills/momentum/skills/conductor/evals/eval-escalation-machinery-end-to-end.md` — an
execution-primary eval that seeds four concrete fixture findings and drives each of the four
escalation outcomes the conduct-core retro found never exercised:

1. **Mid-flight path (Fixture A):** `irreversible-destructive` + `timing_tier=mid-flight` → step 2.F
   fires, pause-ask surfaces mid-build, resolution `fix-applied` recorded in `{{escalations}}`.

2. **End-gate-expanded path (Fixture B):** `high-blast-radius-architecture` +
   `timing_tier=end-gate-expanded` → no pause-ask, routed to `{{end_gate_escalations}}`, surfaces as
   decision card at Phase 5.

3. **BLOCKED disposition (Fixture C):** `routine` finding that fails to converge in 3 fix/re-check
   iterations → `disposition: blocked` in `{{finding_dispositions}}`, story left unmerged, triage stub
   spun via `momentum:triage`.

4. **Escalated disposition (Fixtures A + B):** both paths produce `disposition: escalated` records
   observable in `{{build_log}}`, `{{escalations}}`, and `{{end_gate_escalations}}`.

Each scenario specifies Given/When/Then, pass criteria, and fail criteria aligned to the frozen
contract scenarios in
`.momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/exercise-conduct-escalation-machinery-end-to-end.eval.yaml`.

The eval includes a verification method section and an inspection-vs-execution note explaining
why static inspection of workflow.md is insufficient — the four outcomes depend on runtime
accumulator state (`{{build_log}}`, `{{escalations}}`, etc.) that can only be confirmed by
driving real findings through the loop.

### File List

- `skills/momentum/skills/conductor/evals/eval-escalation-machinery-end-to-end.md` (new)
