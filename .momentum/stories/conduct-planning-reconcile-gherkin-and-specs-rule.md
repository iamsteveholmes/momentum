---
title: Reconcile sprint-planning Step 4 (Gherkin generation) and remove the stale 'dev never accesses specs/' rule
story_key: conduct-planning-reconcile-gherkin-and-specs-rule
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: maintenance
priority: medium
depends_on: []
---

# Reconcile sprint-planning Step 4 (Gherkin generation) and remove the stale 'dev never accesses specs/' rule

## Classification
Blocking level: **refinement** · found by discovery lenses: planning-handoff


## What
Two coupled sprint-planning corrections needed once the new contract model lands. (1) Step 4 still generates standalone .feature files for non-app-ui stories keyed on the legacy frontmatter verification_method, in parallel with Step 3.5's single frozen Part-A+Part-B contract. The build flow resolves EXACTLY ONE contract per story (dev/workflow.md globs specs/{story}.* expecting 0 or 1; the Conductor assumes one contract.path). If Step 4 emits a .feature alongside Step 3.5's .eval.yaml/.smoke.sh/.review.md for the same slug, the glob fallback and single-path assumption break — the two steps must be reconciled to exactly one contract of record per story. (2) sprint-planning/workflow.md line 12 (echoed at Step 4 line 590 and inherited by create-story's injected Implementation Guide) carries <critical>...dev agents never access that path</critical> — but the redesign hinges on dev reading the contract's Part-A header in specs/. The rule directly contradicts dev/workflow.md Step 2.5 + agents/dev.md and must be removed per §7.

## Why it's needed (what breaks without it)
A divergent second spec file per story breaks contract resolution; the stale prohibition creates a spec-vs-skill contradiction (planning forbids exactly what the rebuilt dev agent is required to do) and would block any access logic. Both are cleanup-of-contradiction that the new model makes mandatory but that do not by themselves stop a dedicated-run sprint from completing.

## Source
Identified by the conduct-runnability discovery (2026-06-04) cross-referencing the merged conduct core-build against the design spec (§7/§8/§9/§10/§12/§13). Follow-up to `sprint-2026-06-02-conduct-core`.

## References
- Conduct design spec: _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
- End-gate Format & Voice spec: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md
- DEC-035, DEC-036
