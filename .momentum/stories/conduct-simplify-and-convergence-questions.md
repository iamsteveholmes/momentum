---
title: Wire /simplify Phase C invocation and resolve the §13 convergence open questions
story_key: conduct-simplify-and-convergence-questions
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: low
depends_on: []
---

# Wire /simplify Phase C invocation and resolve the §13 convergence open questions

## Classification
Blocking level: **refinement** · found by discovery lenses: engine-hollows, e2e-runnability, spec-audit


## What
Two small loose-end items. (1) Step 2.S3 Phase C describes /simplify as an optional post-fixer cleanup pass but contains NO actual <action> that invokes it, captures output, or feeds it back — it is inert prose while Phase B (mid-flight dispatch) and Phase D (re-check) are concrete actions. (2) Several §13 open questions remain unresolved and make a clean run under-defined: Q1 /simplify placement (every story / diff threshold / on-demand); Q2 retry bounds are inconsistent across the workflow (dev/pipeline retry=2, merge attempts=3, fix-loop=3 in one place, MAX_FIX_ITERATIONS unspecified elsewhere) with no single canonical source; Q5 review_depth:deep authority+heuristic is unassigned (no story sets it); Q9 dropped vs closed-incomplete is unresolved (approve only ever emits closed-incomplete, leaving 'dropped' an unreachable terminal state). NOTE: §13 Q3 (bmad config) is RESOLVED — _bmad/bmm/config.yaml EXISTS, so the bmad-code-review HALT is a non-issue; Q7 (code-fixer location) is also resolved.

## Why it's needed (what breaks without it)
Phase C as written never runs, so no story gets a cleanup pass; inconsistent retry bounds make bounded-retry non-deterministic; unowned review_depth means the high-risk deep-review opt-in can't be set; the dropped-vs-closed-incomplete ambiguity leaves a terminal state with no defined transition. These are convergence/polish items — the routine fix path completes without them — but the loop and state machine are incomplete vs spec until decided.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
