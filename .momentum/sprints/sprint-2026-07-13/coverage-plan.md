# Coverage Plan — sprint-2026-07-13

> **Anti-redundancy principle:** Never validate in isolation what an integrated scenario
> already exercises.

## Integration Scenario: Conducted fixture build — interrupted, resumed, approved

**Description:** One conducted build over a crafted fixture sprint drives the build engine
end-to-end and is observed from five angles at once. The fixture sprint is constructed to
contain: a story whose deliverable is a brand-new file; story/finding prose full of
shell-hazard characters (quotes, apostrophes, dollar signs, embedded newlines); one
smoke-routed story; and an adjacent out-of-scope file the build must not sweep in. The build
is interrupted and resumed at defined points (mid-story; after findings exist; once with a
truncated final state line; once after approval), driven to its end-gate in a session with an
existing viewer pane (and once without), approved, and a retrospective is then invoked.
Auxiliary probes in the same run: an approval pass when nothing is left to complete, and one
fixture story whose verification contract omits a required declaration.

**Discharges** (each story covered-by-composition, with rationale):

| Story | What the run observes for it |
|---|---|
| `conductor-endgate-viewer-hijack-and-silent-gate` | End-gate render steals no focus; viewer reused/created correctly; approval ask lands in the same turn. (Its 3 `[Document check]` scenarios are static inspections — verified by the per-story QA leg, which composition does not defer.) |
| `conduct-adoption-retire-sprint-dev` | Approval completes the sprint with no manual step; retrospective finds the completed sprint; re-approval is non-fatal. |
| `conduct-resume-and-rehydration-idempotency-hardening` | Each resume continues without redoing stories or double-counting findings; final summary matches an uninterrupted run. |
| `conduct-conductor-staging-and-ledger-append-safety` | The green-field file survives to the merged result; ledger lines stay valid JSON under hostile prose; the out-of-scope file is excluded; the truncated-line interrupt resumes with a warning, not an abort. |
| `conduct-qa-execute-verification-method` | The smoke-routed story gets a real build+launch+drive (or BLOCKED with the named prerequisite); a verdict without execution evidence is rejected; the missing-declaration fixture produces BLOCKED naming the field. |

**Files/spans exercised:** the conductor build pipeline end-to-end (story launch → dev →
QA/code-review → merge → AVFL-on-merge → E2E → end-gate → completion), the build state
record, the sprint record, and the merged tree.

## Dedicated-run (10 stories)

- `momentum-knowledge-base-buildout` — KB vault + per-project resolver behavior lives outside the conducted-build boundary.
- `manifesto-builder-skill-generate-then-curate` — the interactive generate-then-curate flow needs its own invocation; its producer/consumer seam with composition discovery is *additionally* exercised by the cohort driver run, but the skill flow itself is not.
- `base-body-collapse-rollback` — CLI/resolve/file-set assertions independent of any build run.
- `rename-base-body-files-to-canonical-naming` — naming-conformance checks + decision-doc annotation inspection.
- `architecture-decision-26-update-for-base-body-collapse` — document review of the architecture text.
- `repair-phantom-story-file-entries-and-backfill-live-fixture-scope` — index/file truth scan + registration-guard sandbox probe.
- `conduct-live-run-against-fixture-sprint` — THE cohort proof; its contract *is* the observed driver run (dedicated by design; discharges the sprint-2026-06-28 escalated residual).
- `sprint-planning-cross-story-coherence-gate` — planning-run eval over crafted incoherent/coherent story pairs.
- `sprint-planning-continuous-execution-and-cli-fixes` — CLI smoke assertions + plain-language workflow observation.
- `sprint-planning-handoff-artifact` — planning-to-activation artifact observations.

## Coverage notes (verified elsewhere — not E2E material)

- `manifesto-builder` AC8 (skill prose states its design stances and cites its authorities) is not black-box verifiable — the per-story QA/code-review leg owns it.
- `conductor-endgate` ACs 2/5/7 (`[Document check]` scenarios) are static instruction-text checks — per-story QA leg owns them.
- The KB contract's unregistered-project_kb mismatch scenario is seam-rule-derived (no explicit AC clause); it encodes the story's stated project-scoping intent (DEC-038 D2).
- `sprint-planning-continuous-execution-and-cli-fixes` froze the AC-stated `--slug`-flag invocation shape; if the implementer ships the alternate dedicated-subcommand shape, the contract must be updated via a loud escalation, never silently.

## Validation

Every approved story appears exactly once: **5 covered-by-composition + 10 dedicated-run = 15 ✓.**
The single integration scenario discharges 5 stories ✓.
