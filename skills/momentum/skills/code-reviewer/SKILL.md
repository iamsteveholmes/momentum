---
name: code-reviewer
description: "Non-interactive bmad-code-review adapter for conduct. Accepts a single story diff, drives adversarial bug-hunt in report-only mode, normalizes surviving findings to the canonical schema with stakes_class populated, and returns the finding stream to the Conductor. Invoked by the Conductor — do not invoke directly."
model: claude-opus-4-6
context: fork
allowed-tools: Read Grep Bash
effort: high
user-invocable: false
---

# code-reviewer — Non-Interactive Normalizing Adapter

This skill is the **bmad-code-review adapter** for conduct's per-story review leg. It drives the
existing `bmad-code-review` adversarial bug-hunt engine in report-only, non-interactive mode
against a single story's diff, then normalizes the surviving findings into the **canonical finding
schema** (`finding-schema.md`) with `stakes_class` populated via the shared stakes-classification
rubric. The normalized finding stream is returned to the Conductor.

## What This Adapter Does

1. Drives the three adversarial review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor)
   non-interactively against the story's diff.
2. Triages findings into bmad buckets (patch / defer / dismiss / decision_needed).
3. **Drops** the bmad `dismiss` bucket (noise / false-positive / handled-elsewhere) — these are
   bmad-layer noise and do not become canonical findings.
4. Normalizes the surviving `decision_needed`, `patch`, and `defer` findings into the canonical
   finding schema, stamping `source=bmad-code-review` on every emitted record.
5. Populates `stakes_class` on every emitted finding by consulting
   `skills/momentum/references/stakes-classification-rubric.md`. Defaults to `routine` when the
   finding prose matches no stakes-class signal. Never leaves `stakes_class` unset.
6. Returns the canonical finding stream to the Conductor as text. Does not apply fixes, assign
   dispositions, or write any file.

## What This Adapter Is Not

**Not:** A DEC-036 fixer, escalator, or disposition assigner. The following are out of scope:
- Disposition assignment (fixed / dismissed / triaged-out / escalated) — fixer-assigned downstream
- Timing-tier selection (mid-flight vs. end-gate-expanded) — fixer-assigned downstream
- Fix application — the adapter is strictly read-only; it never mutates any tracked file

The adapter owns emission-wiring only: it consumes the shared rubric's signal list and attaches
the rubric's verdict to each finding. It does not re-implement or fork the rubric's logic.

## The Two "Dismiss" Concepts — Kept Distinct

The bmad `dismiss` bucket and the conduct fixer `dismissed` disposition are DISTINCT:
- **bmad `dismiss`** = bmad's own noise filter; dropped at the adapter layer (step 4). This is
  not a canonical finding. It never reaches the fixer.
- **conduct `dismissed` disposition** = a fixer-leg outcome; a legitimate-looking finding the
  fixer chose not to act on, recorded with a REQUIRED non-empty rationale and rendered in the
  end-gate report (DEC-036). This lives downstream — not in this adapter.

The adapter drops only bmad-layer noise. It does not pre-emptively suppress any `decision_needed`,
`patch`, or `defer` finding. Doing so would rob the fixer of findings it is supposed to see and
dismiss-with-rationale.

## Governing Decisions

- **DEC-035** — adopt conduct; one human end-gate; auto-fix loop must be legible
- **DEC-036** — narrow stakes-gated mid-flight escalation amending DEC-035; amendments D2
  (populate `stakes_class` via shared rubric; emit `routine` on no signal) and D3 (bmad `dismiss`
  dropped at the adapter layer is distinct from the fixer `dismissed` disposition) both land here
- **Spec section 4** — bmad-code-review is the chosen engine for the per-story review leg
- **Spec section 10** — config-scaffolding gap this adapter closes
- **Spec open question 3** — required config scaffolding and actionable error path

## Adapter Mode

The adapter is invoked with a single story's diff as its input context. It drives only the
adversarial review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor where spec is
available) and the triage step. It does **not** drive step-04-present from `bmad-code-review`
— that step owns file writes, HALTs, and fix-application logic that are incompatible with
autonomous execution.

Load and follow `./workflow.md` — it is the binding execution protocol for every adapter run.
