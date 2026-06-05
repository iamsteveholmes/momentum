---
title: Wire the AVFL/merge consumer that discharges covered-by-composition deferrals
story_key: conduct-coverage-disposition-discharge-consumer
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Wire the AVFL/merge consumer that discharges covered-by-composition deferrals

## Story
Follow-up from the conduct core-build slice (`sprint-2026-06-02-conduct-core`). Wire the AVFL/merge consumer that discharges covered-by-composition deferrals.

## Why this exists
conduct records a covered-by-composition deferral (skip build-time QA, discharge later via a named integration scenario) but the consumer that actually runs the named scenario at AVFL/merge and verifies its outcome is not wired.

## What's needed
- At AVFL/merge (Phase 3), consume the coverage-disposition-deferred records: run each named integration scenario and verify the deferred story's contract is discharged.
- Surface any undischarged deferral as a leftover at the end-gate.

## References
- Conduct spec §5 / §7 (coverage plan): _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- conductor/workflow.md step 2.C / step 3 (DOWNSTREAM DISCHARGE note)
