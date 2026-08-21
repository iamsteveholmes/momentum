This is a use-then-discard build bridge for the next `/momentum:conduct` session. Delete this
file once the build session has consumed it — handoffs are ephemeral, not preserved as history.

# Build Handoff — sprint-2026-08-03

## Sprint Goal

A sprint can no longer claim done without a human seeing it work.
Verified fixes:
- Sprint closure refuses done while any declared condition lacks a recorded human verdict, and closes FAILED honestly with a reason
- The merge gate completes by executing merge, push, and story transitions verified by read-back, never a report
- An interrupted or gated build leaves a resume card and the next session opens with its one pending question
- momentum-tools feature verify records a human pass/fail verdict with paired build SHAs into .momentum/features.json
- The session greeting leads with N of M feature conditions passing, honest when no registry exists
- momentum-tools tasting produces the daily expected-vs-reality brief and a due signal with rising tiers
- A backend-only story with a declared chat-ui surface routes to smoke verification, never curl

## Stories by Wave

### Wave 1
- `momentum-tools-feature-verify-human-verdict-recorder-and`
- `sprint-planning-goal-conditions-declaration-plan-gate-leads`
- `conduct-merge-gate-completes-by-executing-merge-push-story`

### Wave 2
- `sprint-closure-refusal-recorded-human-verdicts-per-goal`
- `impetus-session-greeting-leads-with-n-of-m-feature`

### Wave 3
- `conduct-resume-card-impetus-pending-gate-agenda-session`
- `verification-routing-re-key-to-assembled-surface-dod`

### Wave 4
- `daily-tasting-reminder-expected-vs-reality-brief-generator`

## Contract / Spec Locations

- `momentum-tools-feature-verify-human-verdict-recorder-and`: `.momentum/sprints/sprint-2026-08-03/specs/momentum-tools-feature-verify-human-verdict-recorder-and.smoke.sh`
- `sprint-planning-goal-conditions-declaration-plan-gate-leads`: `.momentum/sprints/sprint-2026-08-03/specs/sprint-planning-goal-conditions-declaration-plan-gate-leads.smoke.sh`
- `conduct-merge-gate-completes-by-executing-merge-push-story`: `.momentum/sprints/sprint-2026-08-03/specs/conduct-merge-gate-completes-by-executing-merge-push-story.eval.yaml`
- `sprint-closure-refusal-recorded-human-verdicts-per-goal`: `.momentum/sprints/sprint-2026-08-03/specs/sprint-closure-refusal-recorded-human-verdicts-per-goal.smoke.sh`
- `conduct-resume-card-impetus-pending-gate-agenda-session`: `.momentum/sprints/sprint-2026-08-03/specs/conduct-resume-card-impetus-pending-gate-agenda-session.eval.yaml`
- `daily-tasting-reminder-expected-vs-reality-brief-generator`: `.momentum/sprints/sprint-2026-08-03/specs/daily-tasting-reminder-expected-vs-reality-brief-generator.smoke.sh`
- `verification-routing-re-key-to-assembled-surface-dod`: `.momentum/sprints/sprint-2026-08-03/specs/verification-routing-re-key-to-assembled-surface-dod.smoke.sh`
- `impetus-session-greeting-leads-with-n-of-m-feature`: `.momentum/sprints/sprint-2026-08-03/specs/impetus-session-greeting-leads-with-n-of-m-feature.eval.yaml`
- Coverage plan: `.momentum/sprints/sprint-2026-08-03/coverage-plan.md`

## Planning-Time Cautions

- Plan-gate fork verdicts (developer instructed adoption of all recommended defaults): Fork 1 — capability statement + the verified-fix list above signed as the sprint goal (goal_conditions is [] because no feature registry exists yet; closure gates on the fix list); Fork 2 — four amended stories re-approved; Fork 3 — the `evidence` sub-field extension to the registry schema is CONFIRMED (persist it; consumers treat it present-but-not-asserted); Fork 4 — feature-verify reassigned to epic momentum-quality-gates-enforced; Fork 5 — resume-card story extended with the closure-pending emit (AC 13 / Task 8), re-approved.
- Sprint closure for THIS sprint keys on the verified-fix list in `goal` — once the closure-refusal story lands, `sprint complete` will require per-fix confirmation (`--fix-confirmed`) against a real build. Plan the end-of-sprint tasting session accordingly.
- Same-wave shared-file overlap accepted with rationale (recorded in coherence-report.md): feature-verify and goal-conditions both edit `skills/momentum/scripts/momentum-tools.py` in Wave 1 — edit regions ~2,700 lines apart, no shared hunks; merge one story at a time.
- Five stories touch `momentum-tools.py` across waves and three touch `.claude/rules/impetus.md` (greeting W2, resume-card W3, tasting W4) — waves serialize them; do not parallelize across waves.
- AVFL checkpoint closed at CHECKPOINT_WARNING: 4 of 7 findings fixed in-pass; the remaining 3 were resolved as plan-gate forks (goal seeding = Fork 1, approval re-stamps = Fork 2, closure-pending card = Fork 5). Nothing else outstanding.
- The `.momentum/features.json` registry starts absent by design — registry content arrives via DEC-040 Phase 3 design reconciliation (project-side, out of this sprint). Consumers (greeting, tasting, closure) must degrade honestly per their contracts; an absent registry is correct behavior at build time, not a defect.
