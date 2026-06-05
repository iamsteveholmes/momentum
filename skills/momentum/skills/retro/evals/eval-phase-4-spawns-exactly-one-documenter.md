# Eval: Phase 4 Synthesizes via Exactly One Agent

## Scenario

A retro run reaches Phase 4 with prepared audit-extracts at
`.momentum/sprints/{slug}/audit-extracts/`. Phase 4 invokes the dynamic audit Workflow
(`skills/momentum/skills/retro/audit-workflow.js`) via the Workflow tool, passing the args
contract `{ sprint_slug, sprint_started, sprint_completed, sprint_stories, audit_dir, transcript_query_path }`.

## Expected Behavior

The audit Workflow's `Synthesize` phase spawns **exactly one** agent — the synthesizer — and it is
the only agent that writes `retro-transcript-audit.md`. The synthesizer `agent()` call is **not**
inside a loop, `parallel()`, or a multi-item `pipeline()` stage. The `Discover` and `Verify` phases
may spawn many agents (lens auditors, per-story analysts, refute panels) — the synthesizer is never
multiplexed.

## Verification

1. Inspect `audit-workflow.js`: the `Synthesize` phase (`phase('Synthesize')`) contains a single
   `agent(...)` call that is not wrapped in a loop / `parallel()` / multi-item `pipeline()` stage.
2. After a run, exactly one agent wrote `retro-transcript-audit.md`.

## Pass Condition

Exactly one synthesize-stage agent writes the findings document. There is **no** assertion on total
Phase-4 agent count — it scales with the lens count plus the sprint's story count.

## Fail Condition

More than one agent writes the document, or the synthesizer `agent()` call sits inside a loop /
`parallel()` / multi-item `pipeline()` stage that could multiplex it (the historical 8–10-documenter
replication defect observed on sprint-2026-04-08 and sprint-2026-04-10).

## Rationale

Migrated from the TeamCreate/"documenter" era to the dynamic-Workflow design. The singleton is now a
**structural** property of the script — one `agent()` call in the `Synthesize` phase — which is
strictly stronger than the old runtime team-cardinality tally.
