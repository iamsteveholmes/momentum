# Eval: A resume card surfaced repeatedly never leaves pending and never gains a failed/expired status

**Surface under test:** The resume-card contract's Anti-Expiry Invariant
(`references/resume-card.md`) and the shared-write fields (`resurface_count`, `waited_since`)
as exercised across repeated Impetus surfacings of the same Conductor-written card.

**Invariant guarded (AC 9, 10):** No elapsed time, resurface count, or session count ever changes
`status` away from `pending`. Prominence rises only through the waited-for line; the card's
rendered length otherwise does not grow.

## Scenario

**Given:** A resume card written by the Conductor with `status: "pending"`, `resurface_count: 0`,
and a `waited_since` timestamp several days in the past (simulated).

**When:** Three consecutive fresh sessions start, each one surfacing the still-pending card, with
no developer resolution in between.

**Then:**

1. After each session, `resurface_count` has increased by exactly 1 (0 → 1 → 2 → 3).
2. `waited_since` is byte-identical across all three sessions — it is never reset by a surfacing.
3. `status` reads `"pending"` after all three surfacings. No value other than `"pending"` or
   `"resolved"` ever appears in the `status` field at any point.
4. Each greeting's rendered pending-question surface adds exactly one waited-for line (elapsed time
   since `waited_since`, plus the current `resurface_count`) beyond what the first surfacing showed
   — the lead sentence, the question, and its options do not grow in length or detail across the
   three sessions.

## Pass Criteria

The counter strictly increases, `waited_since` never changes, `status` is `"pending"` throughout,
and the three rendered surfaces differ only by their waited-for line.

## Fail Criteria

Any surfacing or any card state shows `failed`, `expired`, `auto-resolved`, or any status value
outside `{pending, resolved}`; the counter fails to increase; `waited_since` is overwritten by a
surfacing; the rendered surface grows beyond the one permitted waited-for line.

## Verification Method

Inspection of `references/resume-card.md`'s Anti-Expiry Invariant and shared-write field
declarations, cross-checked against `.claude/rules/impetus.md`'s session-start read/write
instructions (confirm the increment touches only `resurface_count`, never `status`). Subagent
walkthrough: simulate three fresh-session reads/writes against a fixture card and diff the file
and the rendered greeting after each pass.
