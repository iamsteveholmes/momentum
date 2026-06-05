# Eval: Synthesize-stage singleton makes duplicate documenters unreachable

## Scenario

The dynamic audit Workflow (`skills/momentum/skills/retro/audit-workflow.js`) is the Phase-4
mechanism. There is **no** `TeamCreate` and **no** `~/.claude/teams/{team}/config.json` — the old
"Shape A" team topology is gone, and with it the runtime member tally it required.

## Expected Behavior

A duplicate documenter cannot arise, because the `Synthesize` phase is a single `agent()` call by
construction. A reviewer inspecting `audit-workflow.js` confirms ALL of the following:

1. The `Synthesize` phase contains exactly one `agent(...)` call.
2. That call is **not** inside a loop, `parallel()`, or a multi-item `pipeline()` stage.
3. No `TeamCreate`, `SendMessage`, or `~/.claude/teams/.../config.json` machinery exists anywhere in
   Phase 4 or the audit Workflow.

There is no runtime "guard step" to halt on — the property is enforced structurally in the script,
which is strictly stronger than a post-hoc config tally. The old failure (5 documenters in a team
config) has no representation in this design.

## Pass Condition

Exactly one synthesize-stage `agent()` call; no `TeamCreate`/`SendMessage`/team-config machinery
present. A second documenter is unreachable by construction.

## Fail Condition

The `Synthesize` `agent()` call is wrapped in a loop / `parallel()` / multi-item `pipeline()` stage
(which could multiplex it), or any `TeamCreate`/config-tally machinery is re-introduced into Phase 4.

## What This Tests

- The duplicate-documenter defect is prevented structurally, not by a runtime guard.
- The TeamCreate/`config.json` topology has been fully removed.
- The single-writer property lives in the Workflow script and can be verified by reading it.

## Rationale

Migrated from the runtime team-cardinality guard (which tallied `config.json` members and halted on a
mismatch) to a structural invariant of the Workflow script: one `agent()` in `Synthesize`.
