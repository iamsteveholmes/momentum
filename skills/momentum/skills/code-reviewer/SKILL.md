---
name: code-reviewer
description: "Non-interactive bmad-code-review adapter for conduct. Accepts a single story diff, drives adversarial bug-hunt in report-only mode, normalizes surviving findings to the canonical schema with stakes_class populated, and returns the finding stream to the Conductor. Invoked by the Conductor — do not invoke directly."
model: claude-opus-4-6
context: fork
allowed-tools: Read Grep Bash
effort: high
user-invocable: false
---

# code-reviewer — bmad-code-review Adapter Shim

**The in-house stub reviewer has been retired.** This skill no longer contains an in-house
reviewer body. All review logic runs via the `bmad-code-review` adversarial engine, driven by
`./workflow.md`. Invoking this skill without following `workflow.md` produces no review findings.

## Role

This skill is the **single reviewer of record** for conduct's per-story review leg. It is a shim
that delegates all review execution to the `bmad-code-review` engine via `./workflow.md`. It does
not contain standalone reviewer logic.

## What the Adapter Produces

The adapter (via `workflow.md`) drives `bmad-code-review` non-interactively against a single
story's diff and returns a **canonical finding stream** — findings normalized to the schema in
`skills/momentum/references/finding-schema.md` with `stakes_class` populated from the shared
rubric in `skills/momentum/references/stakes-classification-rubric.md`.

Every emitted finding carries `source=bmad-code-review`. Disposition and timing-tier fields are
fixer-assigned downstream; this adapter leaves them absent.

## What This Adapter Is Not

This skill is not a fixer, escalator, or disposition assigner. It is read-only. It does not apply
patches, write files, or assign dispositions (fixed / dismissed / triaged-out / escalated). Those
responsibilities belong to downstream conduct components.

## Governing Decisions

- **DEC-035** — adopt conduct; one human end-gate; auto-fix loop must be legible
- **DEC-036** — narrow stakes-gated mid-flight escalation; this adapter is scoped to emission
  wiring only (populating `stakes_class` via the shared rubric; emitting `routine` on no signal)

## Execution Protocol

Load and follow `./workflow.md` — it is the binding execution protocol for every adapter run.
This skill body contains no review logic. `workflow.md` is the adapter.
