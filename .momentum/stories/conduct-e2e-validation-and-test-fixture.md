---
title: Add a producer→consumer smoke/eval proving a planned sprint yields a conduct-runnable record, and create an activated test-fixture sprint
story_key: conduct-e2e-validation-and-test-fixture
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: high
depends_on: []
---

# Add a producer→consumer smoke/eval proving a planned sprint yields a conduct-runnable record, and create an activated test-fixture sprint

## Classification
Blocking level: **blocks-run** · found by discovery lenses: entry-point, planning-handoff, e2e-runnability


## What
Two coupled integration-test gaps. (1) There is no verification artifact (eval scenario or smoke contract) asserting that a fresh sprint-planning → sprint-manager run produces a sprints/index.json whose story_assignments[] satisfy the Conductor's reads: contract.path resolvable, frozen_sha256 matches the on-disk file, coverage_disposition in the recognized set, verification_method a valid driver_bindings key, Part-A header present in each contract. The conduct-core sprint validated the consumer against hand-crafted inputs only. (2) On the current repo .momentum/sprints/index.json has no active sprint (active.slug = null) and the active block would lack the contract schema even if one were activated — there is no end-to-end fixture (an activated sprint with frozen contracts) to exercise a real conduct run. Capstone: NO end-to-end conduct build has EVER been run (DEC-035 D8 / Gate 4) — pre-flight → per-story pipelines → AVFL-on-merge → E2E → end-gate → approve/push has never been exercised together against a live sprint.

## Why it's needed (what breaks without it)
The success condition — a developer can run /momentum:conduct and execute a sprint end-to-end — has never been demonstrated. Integration seams (the documented HOLLOW dead-ends) only surface in a real run. A producer/consumer contract test is the only thing that proves the planning→build handoff actually closes; a fixture sprint is the precondition that lets the run be exercised at all. This is the acceptance gate for the whole capability and should be the final step of the critical path.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
