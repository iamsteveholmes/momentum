# Directed `momentum:dev` Fix-Mode Invocation Contract

**Version:** 1.2 — write-scope invariant added; cross-artifact triaged-out routing made explicit (2026-06-08)
**Previous:** 1.1 — seam contract declaration added; review scope explicit (2026-06-07)
**1.0:** established with DEC-035 + DEC-036 (stakes-class escalation amendment)
**change_type:** specification
**Verification:** document-review

---

## Purpose

This document is the invocation contract for the directed `momentum:dev` fix-mode used by the Conductor during the conduct build phase of `momentum:sprint-dev`. The Conductor is the top-level session orchestrator that owns all git mutation, routing, and the single human end-gate. The directed fix-mode is a subagent invoked by the Conductor; it applies fixes and returns per-finding dispositions, but it never spawns additional humans-in-the-loop and never owns the pause/routing decision. This contract defines the seam between those two roles precisely enough that neither role bleeds into the other.

---

## Seam Contract Declaration

This document is a **seam contract** — it defines a hand-off boundary between two distinct agents. When a story authors or modifies this contract, the per-story review scope MUST cover BOTH sides of the seam, not only the artifact the story most obviously produces.

| Role | Agent | What it owns |
|---|---|---|
| **Producer** | `momentum:dev` fix-mode (fixer subagent) | Emits per-finding disposition objects; echoes `finding_id` (Conductor-assigned); populates `disposition`, `files_changed`, `dismissal_rationale`, and the nested `escalation` object |
| **Consumer** | Conductor (`momentum:conductor`) | Reads disposition objects; joins on `finding_id` to recover inbound finding fields; routes on `F.escalation.timing_tier` |

**Field-shape compatibility requirement:** Any story that changes this contract — or either of the agents it binds — must verify that every field the producer emits is read at the correct path by the consumer. The canonical output shape in the [Canonical Fixer Output Shape](#canonical-fixer-output-shape) section below is the authoritative cross-side compatibility reference. A reviewer checking a seam story must confirm both sides agree on field names and nesting; a mismatch (e.g., producer nests a field at `escalation.timing_tier` but consumer reads it at `timing_tier`) is a cross-side field-shape incompatibility and must be reported as a `type: integration` finding.

---

## Contract Shape

The contract is a single, narrow invocation shape:

> **Findings in → {applied fixes, per-finding dispositions} out.**

The fix-mode accepts a set of inbound findings — each conforming to the Canonical Normalized Finding Schema (see `finding-schema.md`) — and returns, for every finding, exactly one disposition plus, where applicable, the change it applied. No finding leaves the fix-mode without a disposition. There is no partial result, no deferred finding, and no silent drop.

---

## Finding Identification

Each inbound finding carries a `finding_id` field assigned by the Conductor **before** the fix-mode is invoked. The `finding_id` is:

- **Assigned by:** the Conductor (not by any reviewer, not by the fix-mode itself)
- **Unique within:** the findings array of a single fix-mode invocation (one story's fix call)
- **Lifetime:** the Conductor uses it to correlate each returned disposition back to the inbound finding, and to key per-finding retry counts in `{{fix_attempts}}`

The fix-mode echoes `finding_id` in every returned disposition object so the Conductor can match dispositions to inbound findings without relying on positional ordering. The `finding_id` is a Conductor-internal correlation key; it is not part of the Canonical Normalized Finding Schema field set defined in `finding-schema.md`.

---

## Disposition Vocabulary

Every finding processed by the fix-mode exits with exactly one of the following disposition values. These values are authoritative; no other value is valid.

| Disposition | Meaning |
|---|---|
| `fixed` | A fix was applied to the finding. The finding is resolved. |
| `dismissed` | The finding was judged not a genuine issue (false positive). **Requires a non-empty rationale** — see Dismissed-Rationale Rule below. |
| `triaged-out` | The finding is legitimate but out of scope for this story; it is tracked separately via a `momentum:triage` backlog stub and rendered in the report's out-of-scope section (per `finding-schema.md` Rule 4) — it is not silently dropped. |
| `escalated` | The finding was raised for human attention rather than quietly resolved by the auto-fix path. This disposition is returned **instead of** applying a fix or producing a fix commit. |

### No Deferred Disposition

`deferred` is not a valid disposition value. Every inbound finding receives one of the four values above before the fix-mode exits. A finding that cannot be fixed, dismissed, or triaged-out must be escalated.

---

## Routine Path (Routing Unchanged, Always-On Default)

When an inbound finding is `legitimate: true` and `stakes_class: routine`, the fix-mode applies a fix to the working tree and returns `disposition: fixed` with `files_changed` populated. The Conductor then stages the fix (under the write-scope guard) and commits it. This path is the always-on default (unchanged in routing behavior — always auto-fixed, never escalated; the Conductor now produces the commit rather than the fixer). The vast majority of findings follow this path autonomously without any interruption or escalation. This preserves the anti-firehose intent of DEC-035: routine findings never reach the human before the end-gate.

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

## Dismissed-Rationale Rule (DEC-035 D5 / DEC-036 D3)

When `disposition` is `dismissed`, the fix-mode's return MUST carry a non-empty `dismissal_rationale` string explaining why the finding was dismissed. A dismissal with a missing or empty rationale is invalid. Empty wave-offs defeat the legible auto-fix record required by DEC-035 D5 — dismissal explanations are not optional. DEC-036 D3 extends this legibility requirement by mandating that dismissals be rendered in the conduct report (the "Dismissed / not-actioned" section), but the underlying non-empty-rationale requirement is grounded in DEC-035 D5.

---

## Pause-Ownership Boundary

This contract defines what the fix-mode returns. It does **not** own or implement the mid-flight pause mechanism.

The fix-mode emits a `disposition` value and, for escalated findings, a `timing_tier` flag. That is the full extent of its routing output. The Conductor — which owns all git mutation, routing, and the single human end-gate — reads the disposition and timing-tier and decides whether and when to pause, prompt, or route the escalation. The fix-mode itself **never pauses, never blocks, and never prompts the human**. Consuming the timing-tier is the Conductor's responsibility, not the fix-mode's.

This boundary is stated explicitly to prevent the fix-mode from re-introducing a finding firehose or surprise pauses during the autonomous build phase.

---

## Write-Scope Invariant

The fix-mode operates within a **declared writable file set** passed by the Conductor at invocation time. This set enumerates exactly which files the story is authorized to create or modify.

**Hard prohibitions — no exceptions:**

- **Never edit the story's own spec file** (`.momentum/stories/{story-slug}.md`). It is read-only input. Editing it constitutes scope leakage.
- **Never edit any other story's spec file** under `.momentum/stories/` or its verification contract under `.momentum/sprints/`. Those files belong to sibling stories and are outside this story's writable set.
- **Never write to any file outside the declared writable set.** If a finding points to a problem in a file not in the writable set, the correct disposition is `triaged-out`, not `fixed`.

**Cross-artifact findings — mandatory `triaged-out` routing:**

When a finding points to a problem that genuinely belongs to a different artifact (a file outside this story's writable set — including another story's spec, a shared reference document not in the writable set, or any file owned by a different story), the fix-mode MUST:

1. Return `disposition: triaged-out` for that finding.
2. Include in the triaged-out record enough context (location, summary, suggested_fix) for the Conductor to spin a reconciliation note against the owning story via `momentum:triage`.

**What this prevents:** The sprint-2026-06-02-conduct-core retro found 5 of 21 stories (24%) required a Conductor revert because the dev or fixer agent edited the story spec file or a sibling workflow file — files it was never authorized to touch. The write-scope constraint and the triaged-out cross-artifact routing eliminate the root cause of those reverts.

---

## Disposition Rules Summary

These rules encode the DEC-036 amendment to DEC-035's binding decision #1.

| Condition | Disposition |
|---|---|
| `legitimate: true`, `stakes_class: routine` | `fixed` — auto-fixed; committed by the Conductor; no escalation |
| `legitimate: true`, `stakes_class` is `security-auth-isolation`, `irreversible-destructive`, or `high-blast-radius-architecture` | `escalated` — inline payload returned; no fix applied; no fix commit |
| `legitimate: false` | `dismissed` — non-empty rationale required; never fixed or escalated |
| `legitimate: true`, out of scope for this story | `triaged-out` — tracked separately; not silently dropped |
| `legitimate: true`, finding targets a file outside this story's declared writable set | `triaged-out` — cross-artifact routing; DO NOT edit the out-of-scope file |

---

## Source Decisions

- **DEC-035** — Adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND what it dismissed.
- **DEC-036** — Amends DEC-035 binding decision #1 narrowly: D1 = stakes-and-timing escalation policy (the centerpiece — defines the three stakes classes, two timing tiers, and the narrow mid-flight bar); D2 = add a stakes finding-class to the fixer schema and hold stakes-class findings out of silent auto-fix; D3 = render the `dismissed` disposition in the conduct report (builds the unbuilt half of DEC-035 D5's legibility requirement); D5 = establish a decision-grade presentation standard with a self-sufficiency floor (the inline `what / why / evidence` payload requirement); anti-firehose intent and always-auto-fix for routine findings are preserved.

---

## Canonical Fixer Output Shape

This section codifies the authoritative per-finding output shape that the fix-mode fixer MUST produce and that the Conductor MUST consume. Both sides of the seam are bound to this shape.

### Per-finding disposition object

```json
{
  "finding_id": "<string — Conductor-assigned, echoed back>",
  "disposition": "fixed|dismissed|triaged-out|escalated",
  "files_changed": ["<file paths — populated for fixed; empty for all other dispositions>"],
  "dismissal_rationale": "<non-empty string if dismissed; null otherwise>",
  "escalation": {
    "what": "<description of the finding>",
    "why": "<rationale for escalation — stakes class and consequences>",
    "evidence": "<concrete artifact excerpt>",
    "timing_tier": "end-gate-expanded|mid-flight"
  }
}
```

**Key shape rules:**

- **`timing_tier` is INSIDE `escalation`** — it is a field of the `escalation` object, not a top-level field on the disposition object. A consumer reading `F.timing_tier` will find nothing; the correct path is `F.escalation.timing_tier`. Note: `finding-schema.md` lists `timing_tier` as a flat field on the *normalized-finding* object — that is a different object from this *disposition* object. The two schemas represent different stages of the pipeline (inbound finding vs. fixer return), not a contradiction; the nesting difference is intentional and correct.
- **`escalation` is present only when `disposition == "escalated"`** — for all other dispositions it is `null`.
- **The `escalation` object does NOT echo `stakes_class`, `summary`, or `location`** from the inbound finding — those fields live on the inbound finding only. The consumer (the Conductor) recovers them by **joining on `finding_id`** back to the stage-2 findings array it sent in.

### Conductor join pattern

When the Conductor routes an escalated finding, it MUST join by `finding_id` to recover the inbound finding's fields:

```
For disposition F where F.disposition == "escalated":
  I = stage2_findings.find(x => x.finding_id == F.finding_id)
  stakes_class   = I.stakes_class
  summary        = I.summary
  suggested_fix  = I.suggested_fix
  timing_tier    = F.escalation.timing_tier  ← nested inside escalation object
  evidence       = F.escalation.evidence     ← inline payload from fixer (preferred)
                   OR I.evidence             ← fallback if fixer evidence is absent
```

This join is the ONLY correct way to recover `stakes_class` and `summary` for an escalated finding. Reading those fields from the top-level disposition object will silently find `undefined`.

### Disposition-by-disposition shape reference

| Disposition | `files_changed` | `dismissal_rationale` | `escalation` |
|---|---|---|---|
| `fixed` | Populated | `null` | `null` |
| `dismissed` | Empty `[]` | Non-empty string | `null` |
| `triaged-out` | Empty `[]` | `null` | `null` |
| `escalated` | Empty `[]` | `null` | Fully populated object including `timing_tier` |

---

## Related References

- `skills/momentum/references/finding-schema.md` — Canonical Normalized Finding Schema; defines the inbound finding shape (including `stakes_class`, `legitimate`, `suggested_fix`) and the disposition and timing-tier fields this contract assigns.
