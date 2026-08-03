# Coverage Plan — sprint-2026-08-03

> **Anti-redundancy principle:** Never validate in isolation what an integrated scenario
> already exercises.

## Integration Scenarios

None declared. Three composition candidates were examined and each stays dedicated:

1. **Verdict-recorded-then-closure-honors-it** (`momentum-tools-feature-verify-human-verdict-recorder-and` × `sprint-closure-refusal-recorded-human-verdicts-per-goal`) — the closure contract deliberately hand-builds producer-shaped registry fixtures instead of invoking `feature verify`, so each contract exercises its own boundary in isolation while the seam is frozen by matching field-shape scenarios on both sides (producer pins the written shape; consumer pins the read shape and names mismatches as cross-side field-shape incompatibilities). Folding either into a composed scenario would discharge only the happy path and silently drop the rejection-path coverage that is most of both contracts.
2. **Declared-conditions-then-closure-keys-on-them** (`sprint-planning-goal-conditions-declaration-plan-gate-leads` × `sprint-closure-refusal-recorded-human-verdicts-per-goal`) — same structure: the closure contract fabricates sprint records carrying `goal`/`goal_conditions` in the exact producer shape; the producer contract independently proves `sprint plan` writes that shape and `sprint activate` carries it. Both sides pin the same record shape; neither scenario set is redundant with the other.
3. **Session-start with both a pending card and a populated registry** (`conduct-resume-card-impetus-pending-gate-agenda-session` × `impetus-session-greeting-leads-with-n-of-m-feature`) — the two contracts share the session-start surface but assert complementary, non-overlapping content (card-leads ordering vs N-of-M headline); the greeting contract's scenarios explicitly fix "no pending card" as a given to isolate the headline behavior. The agreed ordering rule (card leads; N-of-M follows) is stated identically in both story specs and is exercised from the card side by the resume-card contract's greeting-leads scenarios.

## Dedicated-Run Stories

Every approved story is a standalone verification target:

| Story | Contract |
|---|---|
| momentum-tools-feature-verify-human-verdict-recorder-and | specs/momentum-tools-feature-verify-human-verdict-recorder-and.smoke.sh |
| sprint-planning-goal-conditions-declaration-plan-gate-leads | specs/sprint-planning-goal-conditions-declaration-plan-gate-leads.smoke.sh |
| conduct-merge-gate-completes-by-executing-merge-push-story | specs/conduct-merge-gate-completes-by-executing-merge-push-story.eval.yaml |
| sprint-closure-refusal-recorded-human-verdicts-per-goal | specs/sprint-closure-refusal-recorded-human-verdicts-per-goal.smoke.sh |
| conduct-resume-card-impetus-pending-gate-agenda-session | specs/conduct-resume-card-impetus-pending-gate-agenda-session.eval.yaml |
| daily-tasting-reminder-expected-vs-reality-brief-generator | specs/daily-tasting-reminder-expected-vs-reality-brief-generator.smoke.sh |
| verification-routing-re-key-to-assembled-surface-dod | specs/verification-routing-re-key-to-assembled-surface-dod.smoke.sh |
| impetus-session-greeting-leads-with-n-of-m-feature | specs/impetus-session-greeting-leads-with-n-of-m-feature.eval.yaml |

**Validation:** 8 approved stories, each appearing exactly once, all dedicated-run; zero
integration scenarios, therefore no story is covered-by-composition and no scenario lacks a
discharged story.
