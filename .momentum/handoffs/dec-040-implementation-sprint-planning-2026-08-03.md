# Handoff — DEC-040 Implementation Sprint Planning

**Date:** 2026-08-03
**For:** The next Momentum session (sprint-planning dispatch)
**From:** Prior session that ratified and documented DEC-040

## Purpose

Run a sprint-planning pass over the nine DEC-040 implementation stories already in the
backlog. Everything upstream is complete — the decision is ratified, `architecture.md` and
`README.md` carry the spec impact, and all nine story stubs are captured with epics and
priorities. Planning is the only step between here and build.

## Recommended sprint goal

> **"A sprint can no longer claim done without a human seeing it work."**

This is the loop-closure condition from DEC-040: merge gates that execute instead of report,
sprint closure that refuses until per-goal-condition human verdicts are recorded, and a
feature verification registry those verdicts land in.

## The nine stories

### Spine (deliver the sprint goal — recommend these lead)

| Story slug | Epic | Priority |
|---|---|---|
| `momentum-tools-feature-verify-human-verdict-recorder-and` | momentum-feature-taxonomy-maintenance | high |
| `sprint-planning-goal-conditions-declaration-plan-gate-leads` | momentum-sprint-planning-to-ready | high |
| `conduct-merge-gate-completes-by-executing-merge-push-story` | momentum-conductor-core | high |
| `sprint-closure-refusal-recorded-human-verdicts-per-goal` | momentum-sprint-orchestration | high |

These four form a dependency chain: the `feature verify` CLI (sole writer of
`.momentum/features.json`) must exist before closure refusal can record verdicts;
`goal_conditions` declared at planning are what closure verdicts key against; the merge gate
(tier 1) must be separated from closure (tier 2) for either to mean anything.

### Ergonomics wave (valuable, none block the spine — second wave or second sprint)

| Story slug | Epic | Priority |
|---|---|---|
| `conduct-resume-card-impetus-pending-gate-agenda-session` | momentum-conductor-core | high |
| `daily-tasting-reminder-expected-vs-reality-brief-generator` | momentum-impetus-experience | high |
| `verification-routing-re-key-to-assembled-surface-dod` | momentum-quality-gates-enforced | high |
| `impetus-session-greeting-leads-with-n-of-m-feature` | momentum-impetus-session-orientation | medium |
| `intake-owner-priority-validator-owner-sourced-app` | momentum-backlog-refinement | medium |

## Source of truth — read before drafting stories

- **Decision:** `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`
  — directives D1–D9 are the practice-side scope for this sprint. D10 is project-side
  execution, already handled; it is **out of scope** here.
- **D1 is the schema authority for `features.json`.** The registry design (failing-by-default
  statuses `absent|failing|passing`, human-only verdicts with paired-build SHAs, exactly
  three integration seams: planning `goal_conditions`, closure verdict, Impetus N-passing
  report). The story for the `feature verify` CLI must implement D1 as written — this design
  has churned before (DEC-034 amendment); do not re-derive it, implement it.
- **Architecture spec impact:** `architecture.md` editHistory entry 2026-08-02 — State Layout
  note for `.momentum/features.json`, Sprint Tracking `goal_conditions` field, the two-tier
  gate rewrite of Decision 59, and the Read/Write Authority row naming
  `momentum-tools feature verify` sole writer.
- **Prior decisions amended by DEC-040** (planning should respect the amendments, not the
  originals): DEC-029 (verification routing re-keyed by D7), DEC-034 (outcome layer amended
  by D1), DEC-036 (resume-card contract added by D5), DEC-039 (completed + amended).

## Notes for planning

- This sprint is **all skill/CLI/rules work in this repo** — no external project involvement.
  Verification methods will mostly be CLI-executable and fixture-based.
- Sprint-planning itself should declare `goal_conditions` for this sprint **manually in the
  plan gate** if the D-declaring story isn't built yet — practice what the sprint builds.
- The pre-sprint plan gate renders as a companion decision surface (visual HTML) per the
  decision-grade presentation standard; the developer works nights and weekends — resume
  cards and short surfaces are the spirit of this entire sprint. Plan accordingly.
