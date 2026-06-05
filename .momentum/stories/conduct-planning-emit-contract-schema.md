---
title: Build the planning→build producer suite: sprint-planning + sprint-manager must emit the story_assignments[].contract{} schema
story_key: conduct-planning-emit-contract-schema
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: critical
depends_on: []
---

# Build the planning→build producer suite: sprint-planning + sprint-manager must emit the story_assignments[].contract{} schema

## Classification
Blocking level: **blocks-run** · found by discovery lenses: planning-handoff, engine-hollows, spec-audit, e2e-runnability


## What
The entire build phase depends on decision-10 artifacts that NO skill produces — in the conduct-core sprint they were hand-crafted into sprints/index.json. This is one coherent producer work item spanning two skills (it should be sequenced as a small sprint, not a single story): (1) sprint-planning must COMPUTE the closed-enum verification_method (skill-invoke | behavioral-trigger | bash | smoke-ui | curl | document-review) from change_type precedence as the single routing signal; (2) write the Part-A '# === VERIFICATION HEADER' (story_slug, verification_method, harness_profile, contract_path, how_dev_self_checks, coverage_disposition, covered_by_scenario, acceptance_criteria_ref, platforms) into every frozen contract — dev/workflow.md Step 2.5 and agents/dev.md already CONSUME this and silently skip the self-check when it is absent; (3) denormalize each story's coverage_disposition + covered_by_scenario from the prose coverage-plan.md into per-story machine-readable fields; (4) compute frozen_sha256 over each contract file at activation; (5) set can_merge_independently from depends_on (true for no-hard-dependency stories); (6) sprint-manager (sole writer of sprints/index.json) must accept and PERSIST the formalized story_assignments[] including the full contract{path, harness_profile, coverage_disposition, covered_by_scenario, frozen_sha256} + verification_method + can_merge_independently (today its sprint_plan action writes only slugs/wave; sprint-planning Step 8 writes only role/specialist/guidelines). The Conductor consumers (step 2.V freeze-check reads contract.frozen_sha256; step 2.C reads coverage_disposition/covered_by_scenario; dev reads Part-A) all already exist and read these exact keys.

## Why it's needed (what breaks without it)
This is the single largest functional gap on the producer side. Without it, every freshly-planned sprint produces assignment records with no contract block: step 2.V compares a live hash against undefined → contract-integrity-stop on every story → no story gets verified and the end-gate surfaces every story as a follow-up; step 2.C reads null coverage → conservative dedicated-run default everywhere; dev's Step 2.5 hits its no-Part-A branch and degrades to plain-English ACs on every story. The consumer engine was shipped against a producer that does not exist.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
