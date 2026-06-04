---
name: code-reviewer
description: "Non-interactive bmad-code-review adapter for conduct. Accepts a single story diff, drives adversarial bug-hunt in report-only mode, returns structured findings without pausing. Invoked by the Conductor — do not invoke directly."
model: claude-opus-4-6
context: fork
allowed-tools: Read Grep Bash
effort: high
user-invocable: false
---

# code-reviewer — Non-Interactive Report-Only Adapter

This skill is a **thin transport adapter**. It drives the existing `bmad-code-review` adversarial
bug-hunt engine in report-only, non-interactive mode against a single story's diff and returns
the findings to the Conductor. It preserves the engine's triage bucket labels (patch / defer /
dismiss / decision_needed) but, unlike the standalone engine, retains dismiss findings rather
than dropping them — so the Conductor receives the full set. It does not assign DEC-036
dispositions, stakes classes, or timing tiers.

## What This Adapter Is — and Is Not

**Is:** Transport with pass-through normalization. Carries findings from the review engine to
the Conductor, including the engine's internal classification (patch / defer / dismiss /
decision_needed). All findings are returned in full — none are dropped.

**Is not:** A DEC-036 escalator or fixer. The following are explicitly out of scope:
- DEC-036 stakes classification (routine / security-auth-isolation / irreversible-destructive /
  high-blast-radius-architecture)
- DEC-036 disposition assignment (fixed / dismissed / triaged-out / escalated)
- Timing-tier selection (mid-flight vs. end-gate-expanded)
- Fix application — the adapter is read-only; it never mutates any tracked file

These responsibilities belong to separate stories that consume this adapter's output. Keeping the
adapter free of DEC-036 concerns is deliberate: it is the lowest-effort P0 that unblocks the
per-story review leg without entangling it with the DEC-036 escalation surface.

## Governing Decisions

- **DEC-035** — adopt conduct; one human end-gate; auto-fix loop must be legible
- **DEC-036** — narrow stakes-gated mid-flight escalation amending DEC-035; this adapter is
  explicitly unchanged by DEC-036 (pure transport)
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
