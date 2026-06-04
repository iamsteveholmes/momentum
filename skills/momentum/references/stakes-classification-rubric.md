# Stakes-Classification Rubric

**Version:** 1.0 — established with DEC-035 + DEC-036 (stakes-class escalation amendment)

This document is the **single source of truth** for stakes classification logic. Every producer in the conduct pipeline — the code-review adapter, the qa-reviewer, and AVFL — references this rubric when assigning `stakes_class` and `timing_tier` to a finding. Producers carry only small emission-wiring that reads from this rubric; they do **not** define their own classification logic. Forking this logic into a producer is a violation of the single-source discipline that this document exists to enforce.

The output vocabulary defined here maps directly to the `stakes_class` and `timing_tier` fields in the canonical finding schema (`finding-schema.md`). A producer can copy the rubric's verdict straight into the schema fields without translation.

---

## Stakes Classes

Every finding lands in **exactly one** of the four classes below. The three non-routine classes are checked first; if none matches, the finding is `routine`. Together, the four classes are exhaustive and mutually exclusive.

### `security-auth-isolation`

Authentication, authorization, or isolation-boundary concerns — any finding where a mistake opens an exploit path or breaks a trust boundary.

**Match when the finding involves:**

- Authentication flows, session management, token handling, or credential verification
- Authorization checks, permission enforcement, role or scope validation, or access-control logic
- Secret or credential handling — storage, transmission, logging, or exposure of API keys, tokens, passwords, or private material
- Isolation- or tenancy-boundary enforcement — any mechanism that prevents one user, tenant, or process from accessing another's state or execution context
- Privilege escalation — any code path that grants elevated rights without proper gating
- Input validation at a security boundary (XSS, injection, SSRF, path traversal, and related classes)
- Inadequate sandboxing or capability restriction in a sensitive context

### `irreversible-destructive`

Actions that cannot be cheaply or safely undone, or that destroy data or state with no safe rollback path.

**Match when the finding involves:**

- Database schema migrations — any DDL change (ADD COLUMN, DROP TABLE, ALTER TYPE, etc.) that modifies live schema
- Data deletes — DELETE statements, bulk wipes, or any operation that permanently removes records
- Force-pushes to shared or protected branches — overwriting published Git history
- Production deploys — pushing a build to a live environment where rollback is costly or impossible
- Destructive file operations — irreversible overwrites, moves, or deletions of non-version-controlled state
- Any operation whose failure mode is **permanent data loss** or an unrecoverable production state

The defining test: *If this goes wrong, can we get back to a known-good state cheaply and safely?* If the answer is no, the finding is `irreversible-destructive`.

### `high-blast-radius-architecture`

Changes to architecture-level structure or shared contracts whose failure radiates widely across the system.

**Match when the finding involves:**

- Changes to shared or cross-cutting interfaces, contracts, or data schemas consumed by multiple components
- Architectural patterns or structural decisions (layering, dependency direction, module boundaries, event topology) whose effects cascade if wrong
- Surfaces or extension points that many other features or teams build on top of — a mistake here requires large-scale rework to correct
- Removal or incompatible modification of a public API, plugin interface, or shared configuration schema
- Design decisions that, if incorrect, invalidate a large downstream body of work rather than just one story

The defining test: *If this is wrong, how many things break or must change?* Wide blast radius — many consumers, many story-equivalents of rework — triggers this class.

### `routine` (fall-through)

Any finding that does not match any of the three stakes classes above is `routine`. This is the common case. Routine findings stay on the **always-on, silent auto-fix path**: they are never escalated, and they do not require human attention before the end-gate.

**The fall-through rule:** check the three non-routine classes in order. If none matches, assign `routine`. Do not assign routine affirmatively — it is the absence of a stakes-class match, not a positive characteristic of the finding itself.

---

## Timing-Tier Decision Rule

The timing tier applies only to **escalated** findings (`disposition: escalated`). It determines *when* the escalation reaches the human.

Two tiers exist:

| Tier | Description |
|---|---|
| `end-gate-expanded` | **Default.** The finding is held until the end-gate, where it appears as a decision card alongside the full conduct report. |
| `mid-flight` | The finding triggers an **immediate** escalation before the fix loop continues. Reserved for the narrow bar below. |

### The Narrow Mid-Flight Bar

A finding routes to `mid-flight` **only** when it meets **at least one** of the following conditions:

1. **Irreversible-and-imminent** — the finding describes an action that is both irreversible (cannot be undone) and about to execute as part of the current build step. Continuing would make recovery impossible.
2. **Build-invalidating** — the finding reveals that the build as currently structured cannot produce a valid artifact and that continuing would compound the invalid state (e.g., a foundational spec contradiction that makes all downstream stories invalid).

**Stakes class alone is not sufficient to trigger `mid-flight`.** Urgency alone is not sufficient. The combination of irreversibility-or-build-invalidity *with* imminence or build-invalidity is what crosses the bar. A security finding, an architecture finding, or a destructive-action finding that does not meet this test belongs to `end-gate-expanded`.

**Bias narrow. When in doubt, use `end-gate-expanded`.** The end-gate-expanded tier is the safety net — it catches everything the mid-flight tier deliberately excludes. A finding held to the end-gate is not lost; it is reviewed with full context. A mid-flight escalation that fires too early interrupts the human unnecessarily and undermines the anti-firehose intent of the whole conduct design.

### The Guardrail: This Bar Must Never Widen

The mid-flight bar is intentionally and permanently narrow. It must not be extended to cover:

- All stakes-class findings (only irreversible-and-imminent or build-invalidating ones)
- Urgency or business priority alone
- Reviewer judgment that "this one is really important"
- Any expansion decided unilaterally by a producer

Every proposed widening must be treated as a spec change, not a producer-level decision. The end-gate-expanded tier is the correct home for all findings that do not meet the narrow bar.

---

## Routine Findings — Always Auto-Fixed, Never Escalated

Routine findings (`stakes_class: routine`, `legitimate: true`) are always resolved autonomously by the fixer. They are never escalated, and they never appear in the mid-flight tier. This is the anti-firehose commitment: the vast majority of findings are handled without interrupting the human.

A routine finding can still be high-severity. Severity and stakes class are independent axes. A critical-severity logic bug in a UI component with no blast radius beyond that component is still `routine` and still auto-fixed. See `finding-schema.md` §Stakes Class for the severity-independence note.

---

## Consumption by Producers

The code-review adapter, qa-reviewer, and AVFL are the three conduct producers that assign `stakes_class`. Each producer applies **only emission-wiring** — logic that reads from this rubric and populates the schema field. They do not define their own classification heuristics.

**Code-review adapter** — reads the prose verdict from `bmad-code-review` and maps the described concern to a stakes class using this rubric's signal lists. When the finding prose matches a security, destructive, or architecture signal, the adapter assigns the corresponding class; otherwise `routine`.

**qa-reviewer** — classifies findings against this rubric using the acceptance-criterion diff signal: does the failing AC describe a security gate, an irreversible operation, or a shared contract? If yes, assign the class; otherwise `routine`.

**AVFL** — classifies integration-level findings against this rubric: does the finding reveal a cross-cutting failure that propagates across stories, or an integration seam whose failure is irreversible or architecturally wide? Assign accordingly; otherwise `routine`.

All three producers must be consistent with this rubric. If a producer's classification diverges from what this rubric prescribes, the rubric wins and the producer is corrected — not the rubric.

---

## Source Decisions

- **DEC-035** — Adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND what it dismissed.
- **DEC-036** — Amends DEC-035 binding decision #1 narrowly: stakes-and-timing escalation policy; stakes-class findings leave the silent auto-fix path; report renders dismissals with rationale; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved. The mid-flight bar stays narrow by design.
- **AES-004 Finding 2** — Stakes heuristic graded "missing/unwired — no heuristic flags high-risk." This rubric closes that gap: it is the heuristic, authored once, consumed by all producers.
