---
title: Directed momentum:dev fix-mode invocation contract with escalate-do-not-fix path
story_key: directed-fix-invocation-contract
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - specification
verification_method: document-review
depends_on:
  - directed-fix-finding-schema
touches:
  - skills/momentum/references/directed-fix-invocation-contract.md
---

# Directed momentum:dev fix-mode invocation contract with escalate-do-not-fix path

## Story

As the Conductor (the top-level session orchestrator that owns the conduct build phase),
I want a documented invocation contract for the directed `momentum:dev` fix-mode that takes
findings in and returns applied fixes plus a per-finding disposition for each one,
so that I can drive the auto-fix loop legibly — knowing exactly what was fixed, what was
dismissed and why, and which stakes-class findings were escalated rather than silently
fixed — without the contract reaching into my pause/routing responsibilities.

## Description

The conduct rewrite of `momentum:sprint-dev` runs an autonomous build phase with a single
human end-gate. During that phase, the Conductor repeatedly hands review findings to a
directed fix-mode of `momentum:dev` and expects a clean, machine-routable answer back for
every finding. Today no such contract exists: the legacy flow conflates "fix it" with "raise
it," provides no disposition vocabulary, and offers no path for a finding that must NOT be
silently fixed. This story specifies that contract as a reference document.

The contract defines a single, narrow shape: **findings in → {applied fixes, per-finding
dispositions} out.** Every inbound finding leaves with exactly one disposition. Routine,
legitimate findings are fixed and committed exactly as before — that path is unchanged and
remains the always-on default. The new behavior is an explicit **"escalate, do not fix"**
output path: when an inbound finding is stakes-class (security/auth-isolation;
irreversible/destructive such as a migration, delete, force-push, or prod deploy; or
high-blast-radius/architecture), the fix-mode does NOT apply a fix and does NOT produce a
fix commit. Instead it returns `disposition = escalated` together with an escalation payload
— the what/why/evidence a human decision card needs, carried inline, plus a timing-tier flag
(`mid-flight` or `end-gate-expanded`) so the Conductor can decide when to surface it.

This preserves the anti-firehose intent of DEC-035 (routine findings never interrupt the
human; one end-gate is the norm) while honoring the narrow relaxation in DEC-036: stakes-class
findings get to leave the silent auto-fix path and be raised rather than buried. The contract
also pins down two long-standing legibility requirements: a `dismissed` finding always carries
a non-empty rationale, and the produced report can render dismissals (not just fixes).

Critically, this contract owns disposition and timing **only**. It does NOT implement the
mid-flight pause. It emits a disposition plus a timing-tier flag and stops; the Conductor —
which owns all git mutation, routing, and the human gate — decides whether and when to pause.
This boundary is stated explicitly so the fix-mode never blocks, prompts, or pauses on its own.

Source decisions: DEC-035 (adopt conduct; one human end-gate; no story-count cap; legible
auto-fix loop reporting what it changed and what it dismissed); DEC-036, which amends DEC-035
binding decision #1 narrowly — permitting a high-bar, stakes-gated escalation tier
(amendments D1 disposition vocabulary including `escalated`, D2 the stakes-class escalate-do-not-fix
path with inline payload, D3 non-empty rationale on dismissals, D5 the inline-payload floor).

## Acceptance Criteria

1. The deliverable is a reference document at
   `skills/momentum/references/directed-fix-invocation-contract.md` that specifies the
   invocation contract for the directed `momentum:dev` fix-mode.
2. The document states the contract's overall shape in one place: **findings in →
   {applied fixes, per-finding dispositions} out** — the fix-mode accepts a set of findings
   and returns, for each one, a disposition (and, where applicable, the change it applied).
3. The document defines the disposition vocabulary as exactly these values: `fixed`,
   `dismissed`, `triaged-out`, and `escalated`. Each value has a written one-line meaning.
4. The document states that every inbound finding returns with exactly one disposition —
   no finding is left without a disposition.
5. **Routine path (unchanged):** the document states that a routine, legitimate finding
   (default stakes class) returns `disposition = fixed` with the fix applied and committed.
   This path is the always-on default and is described as unchanged from prior behavior.
6. **Escalate-do-not-fix path (DEC-036 D2):** the document states that a stakes-class inbound
   finding returns `disposition = escalated` and an escalation payload INSTEAD of applying a
   fix and INSTEAD of producing a fix commit. It explicitly states that no fix is applied and
   no fix commit is produced for an escalated finding.
7. The document enumerates the stakes classes that trigger the escalate-do-not-fix path:
   security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod
   deploy); and high-blast-radius/architecture. It states that the default class is `routine`.
8. **Inline payload floor (DEC-036 D5):** the document requires that the escalation payload
   be carried INLINE in the fix-mode's return and that it contain, at minimum, the what / why /
   evidence a human decision card needs to adjudicate the finding (not a pointer or external
   reference that must be fetched).
9. **Timing tier on escalation (DEC-036):** the document requires the escalation payload to
   carry a timing-tier flag whose only permitted values are `mid-flight` and
   `end-gate-expanded`, where `end-gate-expanded` is the default and `mid-flight` is the narrow,
   high-bar exception. It states the mid-flight bar is restricted to findings that are
   irreversible-and-imminent OR build-invalidating ONLY, and that the bar must stay narrow.
10. **Dismissed requires rationale (DEC-036 D3):** the document states that any finding
    returned with `disposition = dismissed` MUST carry a non-empty rationale explaining why it
    was dismissed, and that an empty or missing rationale is invalid.
11. **Pause-ownership boundary:** the document states explicitly that this contract does NOT
    own or implement the mid-flight pause mechanism. It emits a disposition plus a timing-tier
    flag only, so that the Conductor can route; the fix-mode itself never pauses, blocks, or
    prompts the human.
12. The document is written to verify by document review against the listed observable claims;
    its `change_type` is `specification` and it introduces no executable behavior of its own.

## Tasks / Subtasks

- [ ] Create `skills/momentum/references/directed-fix-invocation-contract.md` (new reference doc).
- [ ] Write a one-paragraph purpose statement: the directed `momentum:dev` fix-mode invocation
      contract used by the Conductor during the conduct build phase. (AC 1)
- [ ] Document the contract shape: findings in → {applied fixes, per-finding dispositions} out,
      with one disposition returned per inbound finding. (AC 2, AC 4)
- [ ] Define the disposition vocabulary `fixed | dismissed | triaged-out | escalated` with a
      one-line meaning for each. (AC 3)
- [ ] Document the routine path: routine/default-class legitimate finding → `fixed` + committed;
      mark it unchanged and always-on default. (AC 5)
- [ ] Document the escalate-do-not-fix path: stakes-class finding → `escalated` + escalation
      payload, with NO fix applied and NO fix commit produced; state this exclusion explicitly. (AC 6)
- [ ] Enumerate the stakes classes (security/auth-isolation; irreversible/destructive —
      migration, delete, force-push, prod deploy; high-blast-radius/architecture) and name
      `routine` as the default. (AC 7)
- [ ] Specify the inline escalation payload floor: what / why / evidence carried inline, sufficient
      for a human decision card, not a pointer. (AC 8)
- [ ] Specify the timing-tier flag on escalation: values `mid-flight | end-gate-expanded`,
      default `end-gate-expanded`; narrow mid-flight bar = irreversible-and-imminent OR
      build-invalidating ONLY; state the bar must stay narrow. (AC 9)
- [ ] Specify the dismissed-rationale rule: `dismissed` requires a non-empty rationale; empty/missing
      is invalid. (AC 10)
- [ ] Add the explicit pause-ownership boundary section: contract emits disposition + timing only;
      it does NOT implement the pause; the fix-mode never pauses/blocks/prompts. (AC 11)
- [ ] Confirm the doc declares no executable behavior and is a `specification`-type artifact. (AC 12)
- [ ] Self-check the document against every acceptance criterion above before signaling done.

## Dev Notes

This is a `specification` change in a markdown/bash repo: the deliverable is a reference
document under `skills/momentum/references/`, not executable code. It builds conduct as a
spec doc, not an app/UI/backend lane.

The contract is the seam between the Conductor (top-level orchestrator; owns all git mutation,
routing, and the single human end-gate) and the directed `momentum:dev` fix-mode (a subagent
that applies fixes but spawns no further humans-in-the-loop). The fix-mode's job is bounded:
take findings, return per-finding dispositions plus applied changes, and — for stakes-class
findings — return an inline escalation payload instead of a fix. The Conductor consumes
disposition + timing-tier and decides routing and pause behavior. Keeping that boundary crisp
is what prevents the fix-mode from re-introducing a finding firehose or surprise pauses.

Key vocabulary to use verbatim and consistently:
- **Stakes classes:** security/auth-isolation; irreversible/destructive (migration, delete,
  force-push, prod deploy); high-blast-radius/architecture; default `routine`.
- **Dispositions:** `fixed` | `dismissed` (REQUIRED non-empty rationale) | `triaged-out` |
  `escalated` (raised, not silently fixed — new).
- **Timing tiers:** `end-gate-expanded` (default) | `mid-flight` (narrow). The mid-flight bar
  is irreversible-and-imminent OR build-invalidating ONLY — bias narrow; the end-gate-expanded
  tier is the safety net. Never widen the mid-flight bar.

Dependency: this story depends on `directed-fix-finding-schema`, which defines the inbound
finding shape (including stakes class) that this contract consumes and the disposition fields
it emits. Author the contract to reference that schema's vocabulary rather than re-deriving it.

Governing spec sections (cited by number from the authoring brief, not opened):
- DEC-035: adopt conduct; ONE human gate at the end; no story-count cap; report organized by
  user-facing functionality; auto-fix loop must be legible (what it changed AND dismissed).
- DEC-036 amendments folded into this contract: D1 (disposition vocabulary including
  `escalated`), D2 (stakes-class escalate-do-not-fix path returning the escalation payload
  instead of a fix commit), D3 (non-empty rationale required on `dismissed`), D5 (inline-payload
  floor for the escalation). DEC-036 amends DEC-035 binding decision #1 narrowly; routine
  findings stay always auto-fixed and the anti-firehose intent is preserved.

Black-box note: this story's acceptance is judged purely by reading the produced reference
document for the observable claims above. The document must stand on its own as the contract
of record.

### References

- Epic: `momentum-sprint-orchestration` — from `_bmad-output/planning-artifacts/epics.json`.
- Decision: DEC-035 (adopt conduct; one human end-gate; no story-count cap; legible auto-fix
  loop) — `_bmad-output/planning-artifacts/decisions/`.
- Decision: DEC-036 (narrow, stakes-gated mid-flight escalation tier; amends DEC-035 binding
  decision #1; amendments D1/D2/D3/D5 folded into this contract) —
  `_bmad-output/planning-artifacts/decisions/`.
