This is a use-then-discard session bridge. Delete after the next session has consumed it.

# Handoff — sprint-2026-08-03 post-planning, pre-build

**Date:** 2026-08-24
**For:** the next Momentum session
**From:** the sprint-planning session (planned 2026-08-03, gate signed + activated 2026-08-21)

## Where things stand

Sprint planning is COMPLETE. The sprint is ACTIVE and UNBUILT — all 8 stories sit at
`ready-for-dev`; `/momentum:conduct` has never run (no build-ledger exists in
`.momentum/sprints/sprint-2026-08-03/`).

**Sprint goal:** "A sprint can no longer claim done without a human seeing it work."
(DEC-040 implementation — closure refusal, executing merge gate, resume cards, feature
registry, tasting brief, N-of-M greeting, surface-keyed verification routing.)

## The one next action

Run the sprint build: dispatch `/momentum:conduct`. It should read
`.momentum/handoffs/sprint-2026-08-03-build-handoff-2026-08-21.md` (goal, 4 waves, contract
paths, cautions) and delete it once consumed. Everything conduct needs is in that file plus
the frozen contracts in `.momentum/sprints/sprint-2026-08-03/specs/`.

## Decisions already made — do not re-litigate

The plan gate closed with five fork verdicts (developer instructed adoption of all
recommended defaults; recorded in coherence-report.md → Override Decisions):

1. Goal + 7-entry verified-fix list seeded on the sprint record; `goal_conditions: []`
   (no feature registry exists yet — closure gates on the fix list).
2. All post-approval story amendments re-approved; `verify-approvals --scope planning`
   returns clean.
3. The `evidence` sub-field on `last_verified` is a CONFIRMED extension to DEC-040 D1
   (recorded in the feature-verify story + architecture.md State Layout note).
4. `momentum-tools-feature-verify-human-verdict-recorder-and` reassigned to epic
   `momentum-quality-gates-enforced`.
5. Resume-card story extended with the closure-pending emit (AC 13 / Task 8).

## Watch-outs for the build session

- **Branch state:** work happens on `sprint/sprint-2026-08-03` (already checked out; never
  pushed — no upstream). A non-sprint commit rides on it: `dcbbb24` "gas-city HITL research
  checkpoint" from another session. It will merge to main with the sprint; flag it at the
  end-gate rather than untangling mid-build.
- **Hot files:** five stories touch `skills/momentum/scripts/momentum-tools.py`; three touch
  `.claude/rules/impetus.md`. Waves serialize them — build waves in order, merge one story
  at a time. The only same-wave overlap (feature-verify ∩ goal-conditions, W1) is accepted
  with rationale: edit regions ~2,700 lines apart.
- **Absent registry is correct:** `.momentum/features.json` does not exist and no story
  creates its content (that is DEC-040 Phase 3, project-side). Greeting/tasting/closure
  contracts all require honest degradation on an absent registry — QA must not flag that
  as a defect.
- **This sprint's own closure** will require per-fix human confirmation once the closure
  story lands (`sprint complete` gains the gate mid-sprint). Expect to schedule a tasting
  session before closing; the sprint deliberately eats its own cooking.
- **Plugin cache:** repo skill tree and installed plugin were verified identical at v0.32.0
  when planning started (2026-08-03). If skills changed since, run
  `/plugin marketplace update momentum` + fresh session before conducting.

## Parked (not blocking the build)

- Three old sprints completed without retros: `sprint-2026-05-26`,
  `sprint-2026-06-05-conduct-runnable`, `sprint-2026-06-10` — historical gap, close when idle.
- `epics.json` story rosters lag the DEC-040 batch — reconciles at next epic-grooming.
- ~60 open retro-handoff items in the practice ledger predate this sprint; next
  sprint-planning run will surface them.
- The plan gate HTML (`.momentum/handoffs/sprint-2026-08-03-plan-gate.html`) is now record
  only — safe to delete with this file.
