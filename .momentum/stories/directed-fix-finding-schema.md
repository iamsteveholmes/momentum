---
title: Canonical normalized finding schema with stakes-class and escalated disposition
story_key: directed-fix-finding-schema
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - config-structure
verification_method: document-review
depends_on:
  - conduct-spec-revision-dec036
touches:
  - skills/momentum/references/finding-schema.md
---

# Canonical normalized finding schema with stakes-class and escalated disposition

## Story

As the Conductor orchestrating a conduct build phase,
I want a single canonical finding schema that code-review, AVFL, qa-reviewer, and the fixer all speak,
so that every reviewer emits findings in one shape, the fixer can route them deterministically by stakes, and the human end-gate can render exactly what was fixed, dismissed, triaged out, and escalated — with no finding silently lost.

## Description

This story produces the canonical normalized **finding schema** — the single referenceable schema document that every reviewer (code-review, AVFL, qa-reviewer) and the fixer speak. It is the hard root of the conduct directed-fix chain: it lands first after the spec revision, and every downstream leg of the escalation work blocks on it. The disposition-vocabulary change it carries is small in surface area but absolute in effect — it is the keystone the whole escalation chain stands on. If the disposition vocabulary and the stakes-class field are not nailed down here, no downstream leg (fixer routing, mid-flight escalation, report rendering, end-gate) can be built consistently.

**What it delivers.** A single schema document defining the normalized shape of a finding — the lingua franca of conduct's review-and-fix loop. Every reviewer normalizes its raw output into this shape before the fixer sees it; the fixer reads only this shape; the report and the end-gate render only this shape.

**The base fields** every finding carries: `story_slug`, `source`, `verdict`, `severity`, `type`, `location`, `summary`, `detail`, `evidence`, `ac_id`, `legitimate`, `suggested_fix`.

**Why now — the pain context.** The legacy sprint-dev (which conduct rewrites) had no single normalized finding shape; each reviewer emitted its own format and the loop's auto-fix behavior was an opaque firehose — findings were silently fixed or silently dropped, with no legible record of what changed and what was waved off. DEC-035 ruled that the auto-fix loop must be legible (it must show what it changed AND what it dismissed). DEC-036 then amended DEC-035 narrowly: not every legitimate finding can be silently auto-fixed. Stakes-class findings — the ones with real consequences — must leave the silent auto-fix path and be *raised*, not quietly resolved. That requires the schema to carry (a) a stakes classification orthogonal to severity, (b) a new disposition that means "raised, not silently fixed," (c) a timing marker that distinguishes the default end-gate-batched tier from the narrow mid-flight tier, and (d) a hard requirement that any dismissal carries a non-empty rationale so the legible record is never an empty wave-off.

**The invariant that changes.** Legacy intent was "a legitimate finding is ALWAYS auto-fixed." DEC-036 relaxes that single absolutism: a *routine* legitimate finding is still always auto-fixed, but a *stakes-class* legitimate finding is **escalated**, not auto-fixed. This story encodes that relaxed invariant directly in the schema's semantics so every downstream consumer inherits it.

**Source decisions.** DEC-035 (adopt conduct; one human gate at the end; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing changes and dismissals). DEC-036 (narrow, high-bar, stakes-gated mid-flight escalation tier; stakes-class findings leave the silent auto-fix path; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved). The mid-flight bar stays narrow by design — irreversible-and-imminent OR build-invalidating only — and the end-gate-expanded tier is the safety net; this schema models both tiers but never widens the narrow one.

## Acceptance Criteria

1. A single canonical finding-schema document exists at `skills/momentum/references/finding-schema.md`, and it is written to be referenced by code-review, AVFL, qa-reviewer, and the fixer as the one shared finding shape.

2. The schema defines every base field with a clear plain-English meaning: `story_slug`, `source`, `verdict`, `severity`, `type`, `location`, `summary`, `detail`, `evidence`, `ac_id`, `legitimate`, and `suggested_fix`.

3. The schema defines a `stakes_class` field that is explicitly **orthogonal to `severity`** (a finding has both independently), with exactly these allowed values: `security-auth-isolation`, `irreversible-destructive`, `high-blast-radius-architecture`, and `routine`.

4. The schema states that `stakes_class` defaults to `routine` when a finding is not classified into one of the three stakes classes.

5. The schema names the three non-routine values as the **stakes classes**: `security-auth-isolation` (security / auth-isolation), `irreversible-destructive` (irreversible or destructive actions — e.g. migration, delete, force-push, prod deploy), and `high-blast-radius-architecture` (high-blast-radius / architecture-level impact).

6. The schema defines a `disposition` field whose allowed values are exactly: `fixed`, `dismissed`, `triaged-out`, and `escalated`.

7. The schema documents `escalated` as a distinct disposition meaning **"raised, not silently fixed"** — the finding was surfaced for attention rather than quietly resolved by the auto-fix path.

8. The schema explicitly states there is **no deferred disposition** — `deferred` is not a valid disposition value, and findings are never parked in a deferred state.

9. The schema defines a `timing_tier` marker with exactly these allowed values: `end-gate-expanded` (the default) and `mid-flight`, and states that `end-gate-expanded` is the default tier.

10. The schema documents the narrow meaning of the `mid-flight` tier: it applies only to findings that meet the high bar of **irreversible-and-imminent OR build-invalidating**, and it states that this bar is intentionally narrow and must not be widened; all other escalations belong to the default `end-gate-expanded` tier (the safety net).

11. The schema requires that when `disposition` is `dismissed`, the finding carries a **non-empty rationale** — a dismissal with a missing or empty rationale is invalid by schema.

12. The schema encodes the relaxed auto-fix invariant: a **routine** legitimate finding is **always auto-fixed** (disposition `fixed`), while a **stakes-class** legitimate finding is **escalated** (disposition `escalated`), not silently auto-fixed.

13. The schema makes the routine fall-through explicit: any legitimate finding whose `stakes_class` is `routine` follows the always-auto-fixed path, preserving the anti-firehose intent for the common case.

14. The schema is internally consistent: `severity` and `stakes_class` are presented as independent axes (a finding may be low-severity yet stakes-class, or high-severity yet routine), and the disposition rules in AC 11–13 reference these fields by their defined names.

## Tasks / Subtasks

- [ ] Create `skills/momentum/references/finding-schema.md` as the single canonical finding-schema document, stating up front that code-review, AVFL, qa-reviewer, and the fixer all speak this schema.
- [ ] Document the base fields with plain-English meanings: `story_slug`, `source`, `verdict`, `severity`, `type`, `location`, `summary`, `detail`, `evidence`, `ac_id`, `legitimate`, `suggested_fix`.
- [ ] Add the `stakes_class` field section: enum values `security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine`, default `routine`, and an explicit note that it is orthogonal to `severity`.
- [ ] Describe each stakes class plainly, including the concrete examples for `irreversible-destructive` (migration, delete, force-push, prod deploy).
- [ ] Define the `disposition` enum: `fixed | dismissed | triaged-out | escalated`; document `escalated` as "raised, not silently fixed."
- [ ] Add the explicit "no deferred disposition" note — `deferred` is not valid and findings are never parked.
- [ ] Define the `timing_tier` marker: `end-gate-expanded` (default) | `mid-flight`, and document the narrow `mid-flight` bar (irreversible-and-imminent OR build-invalidating only; must not be widened; end-gate-expanded is the safety net).
- [ ] Add the required-rationale rule: `disposition: dismissed` requires a non-empty rationale; an empty/missing rationale is invalid.
- [ ] Encode the relaxed auto-fix invariant: routine legitimate → always `fixed`; stakes-class legitimate → `escalated`, not auto-fixed.
- [ ] State the routine fall-through explicitly (legitimate + `routine` stakes_class → always-auto-fixed path) to preserve anti-firehose intent for the common case.
- [ ] Cross-check internal consistency: severity and stakes_class presented as independent axes; disposition rules reference fields by their defined names.

## Dev Notes

This is a **config-structure** change: the deliverable is a schema/spec document, not executable logic. Verification is **document-review** — a reviewer confirms each required field, enum, disposition, and invariant by reading the produced `finding-schema.md`. No code runs.

**Governing spec sections (cite by number from the conduct spec brief):**
- **Spec section 4 — the canonical normalized finding schema.** This story IS the deliverable for section 4: the single referenceable schema that code-review, AVFL, qa-reviewer, and the fixer all speak. Base fields and the DEC-036 additions (stakes_class, escalated disposition, timing_tier, required dismissed-rationale, relaxed auto-fix invariant) are the section-4 contract.

**Why this is the hard root.** Every downstream conduct leg (fixer stakes-routing, mid-flight escalation, report rendering of dispositions, anti-rubber-stamp end-gate) consumes this schema. The disposition-vocabulary change (`escalated` added; `deferred` explicitly excluded) is small but absolute — it is the keystone the escalation chain stands on. Land this first; downstream stories block on it via `depends_on: conduct-spec-revision-dec036` and this story in turn.

**Vocabulary to use consistently in the document:**
- Stakes classes: `security-auth-isolation`, `irreversible-destructive`, `high-blast-radius-architecture`, default `routine`.
- Dispositions: `fixed`, `dismissed` (REQUIRED non-empty rationale), `triaged-out`, `escalated` (NEW — raised, not silently fixed). No `deferred`.
- Timing tiers: `end-gate-expanded` (default), `mid-flight` (narrow — irreversible-and-imminent OR build-invalidating only).

**The narrow-bar discipline.** The schema models the mid-flight tier but must encode it as deliberately narrow and non-widenable. The end-gate-expanded tier is the default and the safety net; biasing narrow on mid-flight is a hard requirement from DEC-036, not a preference.

**The relaxed invariant.** Legacy "legitimate → ALWAYS auto-fixed" is relaxed in exactly one place: stakes-class legitimate findings are escalated instead of auto-fixed. Routine legitimate findings remain always auto-fixed, preserving the anti-firehose intent. The schema's disposition semantics must make both halves of this rule explicit.

### References

- **Epic:** `momentum-sprint-orchestration` — see `_bmad-output/planning-artifacts/epics.json`. This story is the schema-foundation leg of the conduct (sprint-dev rewrite) build sprint.
- **DEC-035:** adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop (shows what it changed AND what it dismissed). See `_bmad-output/planning-artifacts/decisions/`.
- **DEC-036:** amends DEC-035 #1 narrowly — narrow, high-bar, stakes-gated mid-flight escalation tier; stakes-class findings leave the silent auto-fix path; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved. See `_bmad-output/planning-artifacts/decisions/`.
