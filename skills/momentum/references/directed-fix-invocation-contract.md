# Directed `momentum:dev` Fix-Mode Invocation Contract

**Version:** 1.0 — established with DEC-035 + DEC-036 (stakes-class escalation amendment)
**change_type:** specification
**Verification:** document-review

---

## Purpose

This document is the invocation contract for the directed `momentum:dev` fix-mode used by the Conductor during the conduct build phase of `momentum:sprint-dev`. The Conductor is the top-level session orchestrator that owns all git mutation, routing, and the single human end-gate. The directed fix-mode is a subagent invoked by the Conductor; it applies fixes and returns per-finding dispositions, but it never spawns additional humans-in-the-loop and never owns the pause/routing decision. This contract defines the seam between those two roles precisely enough that neither role bleeds into the other.

---

## Contract Shape

The contract is a single, narrow invocation shape:

> **Findings in → {applied fixes, per-finding dispositions} out.**

The fix-mode accepts a set of inbound findings — each conforming to the Canonical Normalized Finding Schema (see `finding-schema.md`) — and returns, for every finding, exactly one disposition plus, where applicable, the change it applied. No finding leaves the fix-mode without a disposition. There is no partial result, no deferred finding, and no silent drop.

---

## Disposition Vocabulary

Every finding processed by the fix-mode exits with exactly one of the following disposition values. These values are authoritative; no other value is valid.

| Disposition | Meaning |
|---|---|
| `fixed` | A fix was applied to the finding. The finding is resolved. |
| `dismissed` | The finding was judged not worth acting on. **Requires a non-empty rationale** — see Dismissed-Rationale Rule below. |
| `triaged-out` | The finding is legitimate but out of scope for this story; it is tracked separately and is not silently dropped. |
| `escalated` | The finding was raised for human attention rather than quietly resolved by the auto-fix path. This disposition is returned **instead of** applying a fix. |

### No Deferred Disposition

`deferred` is not a valid disposition value. Every inbound finding receives one of the four values above before the fix-mode exits. A finding that cannot be fixed, dismissed, or triaged-out must be escalated.

---

## Routine Path (Unchanged, Always-On Default)

When an inbound finding is `legitimate: true` and `stakes_class: routine`, the fix-mode applies a fix and returns `disposition: fixed` with the change committed. This path is **unchanged from prior behavior** and is the always-on default — the vast majority of findings follow this path autonomously without any interruption or escalation. This preserves the anti-firehose intent of DEC-035: routine findings never reach the human before the end-gate.

---

## Escalate-Do-Not-Fix Path (DEC-036 Amendment D2)

When an inbound finding is `legitimate: true` and `stakes_class` is one of the three stakes classes below, the fix-mode returns `disposition: escalated` together with an inline escalation payload. **No fix is applied. No fix commit is produced.** The finding travels to the Conductor as a decision card; only the Conductor decides whether and when to surface it to the human.

This path is the narrow relaxation of DEC-035's original absolutism. It applies only to stakes-class findings; routine findings remain always auto-fixed.

---

## Stakes Classes

The `stakes_class` field on an inbound finding (defined in `finding-schema.md`) determines which path is taken.

**Default class:** `routine` — any finding that does not meet the criteria of the three stakes classes below.

**`security-auth-isolation`**
Security, authentication, or isolation findings. Covers XSS, injection, privilege escalation, auth bypass, leaked credentials, inadequate sandboxing, and any finding where a mistake opens an exploit path or breaks a trust boundary. Triggers the escalate-do-not-fix path.

**`irreversible-destructive`**
Actions that cannot be undone or that destroy data/state with no safe rollback. Concrete examples: schema migrations, data deletes, force-pushes, production deploys, destructive file operations, and any change whose failure mode involves permanent loss. Triggers the escalate-do-not-fix path.

**`high-blast-radius-architecture`**
Changes with wide downstream effect — architectural decisions, cross-cutting concerns, shared interfaces, or design patterns that, if wrong, cascade across many consumers or require large-scale rework to correct. Triggers the escalate-do-not-fix path.

---

## Inline Escalation Payload (DEC-036 Amendment D5)

When a finding is escalated, the fix-mode's return MUST carry the escalation payload **inline** — embedded directly in the response, not as a pointer or external reference that the Conductor must fetch. The payload must contain, at minimum:

- **What** — a clear statement of the finding: what issue was detected and where.
- **Why** — the explanation of why this finding requires human attention rather than auto-fix: what stakes class applies and what the consequences of mis-handling are.
- **Evidence** — the concrete artifact excerpt (code snippet, spec quote, test output, or similar) that substantiates the finding and gives the human enough context to adjudicate without going back to the raw source.

The payload is a self-contained human decision card. It must be sufficient for a human to make an informed decision without additional retrieval.

---

## Timing Tier (DEC-036 Escalation Timing)

The escalation payload MUST also carry a `timing_tier` flag with one of exactly two values:

| Value | Meaning |
|---|---|
| `end-gate-expanded` | The escalation is held until the end-gate, where it appears as a decision card alongside the full conduct report. **This is the default.** |
| `mid-flight` | The escalation is flagged as requiring immediate attention before the fix loop continues. This is a narrow, high-bar exception. |

**Default:** `end-gate-expanded`. When in doubt, the finding belongs at the end-gate.

### The Narrow Mid-Flight Bar

`mid-flight` applies **only** to escalated findings that meet **at least one** of the following conditions:

1. **Irreversible-and-imminent** — the finding describes an action that is both irreversible (cannot be undone) and about to be executed as part of the current build step. Continuing would make recovery impossible.
2. **Build-invalidating** — the finding reveals that the build as currently structured cannot produce a valid artifact, and continuing would compound the invalid state (e.g., a foundational spec contradiction that makes all downstream stories invalid).

**This bar is intentionally narrow and must not be widened.** Urgency alone is not sufficient. Stakes class alone is not sufficient. Only the combination of irreversibility-or-build-invalidity with imminence triggers `mid-flight`. All other escalated findings — including all security, architecture, and destructive-action findings that do not meet this bar — belong to `end-gate-expanded`.

---

## Dismissed-Rationale Rule (DEC-036 Amendment D3)

When `disposition` is `dismissed`, the fix-mode's return MUST carry a non-empty `dismissal_rationale` string explaining why the finding was dismissed. A dismissal with a missing or empty rationale is invalid. Empty wave-offs defeat the legible auto-fix record required by DEC-035 D5 — dismissal explanations are not optional.

---

## Pause-Ownership Boundary

This contract defines what the fix-mode returns. It does **not** own or implement the mid-flight pause mechanism.

The fix-mode emits a `disposition` value and, for escalated findings, a `timing_tier` flag. That is the full extent of its routing output. The Conductor — which owns all git mutation, routing, and the single human end-gate — reads the disposition and timing-tier and decides whether and when to pause, prompt, or route the escalation. The fix-mode itself **never pauses, never blocks, and never prompts the human**. Consuming the timing-tier is the Conductor's responsibility, not the fix-mode's.

This boundary is stated explicitly to prevent the fix-mode from re-introducing a finding firehose or surprise pauses during the autonomous build phase.

---

## Disposition Rules Summary

These rules encode the DEC-036 amendment to DEC-035's binding decision #1.

| Condition | Disposition |
|---|---|
| `legitimate: true`, `stakes_class: routine` | `fixed` — auto-fixed and committed; no escalation |
| `legitimate: true`, `stakes_class` is `security-auth-isolation`, `irreversible-destructive`, or `high-blast-radius-architecture` | `escalated` — inline payload returned; no fix applied; no fix commit |
| `legitimate: false` | `dismissed` — non-empty rationale required; never fixed or escalated |
| `legitimate: true`, out of scope for this story | `triaged-out` — tracked separately; not silently dropped |

---

## Source Decisions

- **DEC-035** — Adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND what it dismissed.
- **DEC-036** — Amends DEC-035 binding decision #1 narrowly: stakes-class findings leave the silent auto-fix path and are escalated instead; dispositions extended to include `escalated` (D1); inline escalation payload required (D2, D5); non-empty rationale required on `dismissed` (D3); timing tier introduced (`end-gate-expanded` default; narrow `mid-flight` bar); anti-firehose intent and always-auto-fix for routine findings are preserved.

---

## Related References

- `skills/momentum/references/finding-schema.md` — Canonical Normalized Finding Schema; defines the inbound finding shape (including `stakes_class`, `legitimate`, `suggested_fix`) and the disposition and timing-tier fields this contract assigns.
