# sprint-2026-05-26 — Verification Coverage Plan

> Never validate in isolation what an integrated scenario already exercises.

Each approved story in this sprint is covered exactly once — either by an
integration scenario that exercises multiple stories' contracts together,
or by a dedicated run of its own frozen contract. Composition is preferred
when an end-to-end scenario can naturally discharge multiple stories'
observable obligations; only stories whose contracts cannot be subsumed by
an integration run get a dedicated run.

---

## Integration scenarios

### Scenario 1 — Cascade-A end-to-end: Impetus session-start after the ledger redesign + hygiene + workflow sweep land

**Behavioral description.** Open a fresh Claude Code session at the project
root after Cascade A (A1 + A2 + A3 + A4) has merged. Observe the first
response. Then run a representative producer skill (one retro Phase 5.5
handoff capture, one triage SHAPING capture). Then re-query the practice
ledger CLI for the resulting state. A single end-to-end session-trace
collects every observation needed to discharge all four Cascade-A stories'
frozen contracts:

- **A1 contract** is exercised by every `momentum-tools practice-ledger`
  invocation in the trace — the new schema, the new subcommands, the
  archive/new-ledger split, and the close-stale safety net all fire during
  session-start. The A1 smoke contract's individual assertions are still
  re-run at sprint-dev time as a focused regression, but at sprint-review
  time this integration scenario subsumes them.
- **A2 contract** is exercised by querying `practice-ledger open` after
  Cascade A merges and observing the 12 enumerated entities absent from
  open and present (with terminal events + outcome_ref payloads) in
  `history --entity <id>`. The A2 hygiene pass leaves its observable trace
  in the post-Cascade-A ledger state.
- **A3 contract** is exercised by the session-start response itself: the
  Impetus-voice situational report with the `N open entries (X this week,
  Y older than 30 days, Z near auto-close)` shape, the absence of "last 5"
  enumeration, the close-stale safety net firing idempotently across two
  fresh-session opens within 24h.
- **A4 contract** is exercised by the retro Phase 5.5 + triage SHAPING
  captures that follow the session-start observation. The captures' visible
  CLI invocations and the resulting `practice-ledger by-source <skill>`
  queries discharge the producer-side sweep's behavioral assertions.

**Discharges:**
- a1-practice-ledger-schema-cli-redesign-true-append-only
- a2-practice-ledger-hygiene-cleanup-close-12-stale-entries
- a3-impetus-rule-update-honest-counts-new-ledger-retired
- a4-skill-workflow-updates-point-retro-triage-sprint

---

### Scenario 2 — Cascade-B end-to-end: create-story + canvas + epic-grooming exercised against the migrated epics.json

**Behavioral description.** With Cascade B (B1 + B2 + B3 + B4) merged, run
a single end-to-end pass that:

1. Inspects the migrated `epics.json` artifact (schema validation, the 23
   features migrated, every story's `epic_slug` resolving to a record).
2. Invokes `momentum:create-story` on a draft pointing at one of the
   migrated epic records — observing the new index entry and the
   missing-epic error path on a second draft pointing at a nonexistent
   epic_slug.
3. Starts the canvas server (`bun --hot skills/momentum/skills/canvas/server.tsx`)
   and exercises `/lenses/epics` and `/epics/<known-slug>` via `curl`.
4. Invokes `momentum:epic-grooming` on a minimal scenario covering both
   the absorbed legacy concerns (orphan resolution + value-analysis edit).

The single end-to-end trace collects every observation needed to discharge
all four Cascade-B stories' frozen contracts:

- **B1 contract** is exercised in step 1 (schema + migration + stories
  re-homing assertions) and is implicitly re-exercised by steps 2–4 (B2,
  B3, B4 all read `epics.json` as their input — any schema defect surfaces
  immediately as an error in those downstream skills).
- **B2 contract** is exercised in step 2 — both the happy-path
  (touches array populated from epic record) and the adversarial path
  (missing-epic error halts before index mutation) are observed in a single
  invocation pair.
- **B3 contract** is exercised in step 3 — the canvas surfaces the new
  routes, the new section id, lifecycle + audience in the L2 detail view,
  and the regression checks against the sprint and cycle lenses.
- **B4 contract** is exercised in step 4 — the unified epic-grooming
  skill is invoked, the legacy skill paths are confirmed absent, and the
  dispatch / architecture / command-file surfaces are inspected as part of
  the trace.

**Discharges:**
- b1-epic-schema-migration-define-epicsjson-migrate-features
- b2-create-story-input-routing-read-epic-context-instead-of
- b3-canvas-update-render-epics-instead-of-features
- b4-grooming-breakdown-skill-restructure

---

## Dedicated runs

### momentumintake-remove-worktree-isolation-story-add-is-safe — `dedicated-run`

**Rationale.** This story is standalone (no `depends_on`, no upstream from
Cascade A or B). Its observable behavior — intake stubs landing on main
without worktree isolation, even under concurrent fan-out — is unrelated
to any integration scenario in this sprint. The contract is exercised by
its own EDD eval scenarios, including the parallel-spawn safety scenario
that no Cascade-A or Cascade-B integration trace would naturally produce.

---

## Coverage roster (every story appears exactly once)

| Story | Disposition |
|---|---|
| a1-practice-ledger-schema-cli-redesign-true-append-only | covered-by-composition (Scenario 1) |
| a2-practice-ledger-hygiene-cleanup-close-12-stale-entries | covered-by-composition (Scenario 1) |
| a3-impetus-rule-update-honest-counts-new-ledger-retired | covered-by-composition (Scenario 1) |
| a4-skill-workflow-updates-point-retro-triage-sprint | covered-by-composition (Scenario 1) |
| b1-epic-schema-migration-define-epicsjson-migrate-features | covered-by-composition (Scenario 2) |
| b2-create-story-input-routing-read-epic-context-instead-of | covered-by-composition (Scenario 2) |
| b3-canvas-update-render-epics-instead-of-features | covered-by-composition (Scenario 2) |
| b4-grooming-breakdown-skill-restructure | covered-by-composition (Scenario 2) |
| momentumintake-remove-worktree-isolation-story-add-is-safe | dedicated-run |

Every approved story in the sprint appears exactly once. Every integration
scenario names at least one story it discharges. Dedicated runs are
reserved for stories whose contracts cannot be subsumed by an integration
trace.
