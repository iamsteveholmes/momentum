---
title: "Code-review adapter: normalize bmad triage into the canonical schema and populate stakes-class"
story_key: code-review-adapter-normalize-triage
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - code-review-adapter-noninteractive-driver
  - directed-fix-finding-schema
  - stakes-classification-rubric
touches:
  - skills/momentum/skills/code-reviewer/workflow.md
---

# Code-review adapter: normalize bmad triage into the canonical schema and populate stakes-class

## Story

As the Conductor's review leg,
I want the bmad-code-review triage output normalized into the single canonical finding schema with each finding tagged by stakes class,
so that the conduct fixer consumes a uniform stream of legitimate findings — each carrying the stakes signal that decides routine auto-fix vs. the narrow mid-flight escalation tier — instead of bmad's review-tool-specific buckets that carry no stakes signal at all.

## Description

conduct (the in-session, per-story, autonomous-build rewrite of sprint-dev) runs an adversarial code review as one input into its auto-fix loop. The underlying reviewer, bmad-code-review, emits its results as triage *buckets* (decision_needed / patch / defer / dismiss) that are specific to that tool. The conduct fixer downstream does not understand bmad buckets — it understands one canonical finding schema. This story is the **adapter**: it wires the bmad triage output into the canonical finding schema, stamping `source=bmad-code-review` on every finding it emits.

Two amendments from DEC-036 land in this adapter:

- **D2 — populate `stakes_class`.** The canonical schema now carries a `stakes_class` field, because stakes class is what routes a finding between the always-silent routine auto-fix path and the narrow mid-flight escalation tier. bmad-code-review emits **no** stakes or security signal — its triage only sorts findings into decision_needed / patch / defer / dismiss. So the adapter cannot read a stakes class off the bmad output; it must **consume the shared stakes-classification rubric** to assign one, and emit `routine` (or null) when the rubric finds no signal. This story owns only the *wiring* — calling the shared classifier and attaching its result. It does **not** re-own or re-define the rubric (that is the `stakes-classification-rubric` story).

- **D3 clarification — two different "dismiss" concepts.** bmad's own `dismiss` bucket (noise / false-positive / handled-elsewhere) is **correctly dropped at the bmad layer** and must NOT be carried forward into the canonical stream. This is a *distinct* concept from the DEC-036 fixer **dismissed disposition**, which lives downstream in the fixer leg and means "a legitimate-looking finding the fixer waved off, recorded with a required non-empty rationale, and rendered in the report." The adapter must drop only bmad-layer noise; it must NOT pre-empt findings the conduct fixer is supposed to see and dismiss-with-rationale itself. decision_needed / patch / defer are all legitimate findings and flow through to the fixer.

**Pain context.** Without this adapter, conduct would either have to teach the fixer bmad's tool-specific vocabulary (coupling the fixer to one reviewer) or would lose the stakes signal entirely (collapsing DEC-036's escalation tier back into the absolutist silent-auto-fix model DEC-035 originally specified). Either way the legibility and escalation guarantees DEC-036 added would not hold.

**Source decisions.** DEC-035 (adopt conduct; single end-gate; legible auto-fix loop) and DEC-036 (narrow stakes-gated mid-flight escalation; report renders dismissals; routine findings always auto-fixed), specifically amendments D2 and D3.

## Acceptance Criteria

1. Each bmad-code-review triage bucket that represents a real finding is emitted as a record in the single canonical finding schema shape — same field names and structure used by every other finding source consumed by the conduct fixer.
2. Every finding the adapter emits carries `source` set to `bmad-code-review`, identifying its origin.
3. The `decision_needed`, `patch`, and `defer` buckets each map to legitimate findings that the conduct fixer consumes; none of these three are dropped by the adapter.
4. The bmad `dismiss` bucket (noise / false-positive / handled-elsewhere) is dropped by the adapter and does not appear as a finding in the canonical stream.
5. Every finding the adapter emits carries a populated `stakes_class` field.
6. The `stakes_class` value is assigned by consulting the shared stakes-classification rubric — not invented or hard-coded inside this adapter — and the adapter does not redefine or duplicate the rubric's classification logic.
7. When bmad-code-review provides no stakes or security signal for a finding (its triage carries none), the adapter emits `stakes_class` as `routine` (or null where the schema permits absence of signal), never leaving the field unset.
8. The adapter assigns the recognized stakes classes — security/auth-isolation, irreversible/destructive, high-blast-radius/architecture, or default routine — strictly through the shared rubric's output, so a finding the rubric flags as a stakes class is tagged accordingly and a finding it does not flag defaults to routine.
9. The story documentation (this file and the skill instruction it produces) explicitly states that the dropped bmad `dismiss` bucket is a DISTINCT concept from the conduct fixer's `dismissed` disposition, so the adapter does not swallow findings the fixer is meant to see-and-dismiss-with-rationale.
10. The adapter does not pre-emptively dismiss, suppress, or filter any `decision_needed` / `patch` / `defer` finding on stakes or judgment grounds — only bmad-layer noise (the `dismiss` bucket) is removed; all stakes-class judgment beyond rubric tagging is deferred downstream to the fixer.

## Tasks / Subtasks

- [ ] Locate the code-reviewer skill instruction surface (`skills/momentum/skills/code-reviewer/workflow.md`) where bmad-code-review triage output is consumed, and confirm the non-interactive driver (dependency) hands triage results to this adapter step.
- [ ] Define the normalization mapping from each bmad triage bucket to the canonical finding schema:
  - [ ] `decision_needed` → canonical finding (legitimate; fixer-consumed)
  - [ ] `patch` → canonical finding (legitimate; fixer-consumed)
  - [ ] `defer` → canonical finding (legitimate; fixer-consumed)
  - [ ] `dismiss` → dropped at the adapter, not emitted
- [ ] Stamp `source=bmad-code-review` on every emitted finding.
- [ ] Wire the shared stakes-classification rubric into the adapter step: for each emitted finding, call the rubric and attach its returned `stakes_class`.
- [ ] Specify the no-signal default: when bmad gives no stakes/security signal, set `stakes_class` to `routine` (or null where the schema allows), never leaving it unset.
- [ ] Write the explicit instruction note distinguishing the dropped bmad `dismiss` bucket from the downstream fixer `dismissed` disposition, so the adapter is never tempted to filter legitimate findings the fixer must see-and-dismiss-with-rationale.
- [ ] Add a guard in the instruction: the adapter must not re-implement or branch the rubric's classification logic — it only consumes the rubric's output (keep ownership boundary clean).
- [ ] Confirm by black-box invocation that the four buckets behave as specified: three flow through with populated stakes_class; dismiss is dropped.

## Dev Notes

This is a **skill-instruction** change (`change_type: skill-instruction`, `verification_method: skill-invoke`). The deliverable is updated instruction text in the code-reviewer skill's `workflow.md`, not executable application code. There is no app/UI/backend lane in this repo — conduct is built entirely as skills, agent definitions, and spec docs.

**Ownership boundaries (keep tight):**

- This story owns the **wiring**: bucket → canonical schema mapping, `source` stamping, and *consuming* the shared classifier to populate `stakes_class`.
- It does **not** own the **rubric** — the `stakes-classification-rubric` dependency defines how a finding's stakes class is judged. This adapter only calls it and attaches the result. Re-implementing rubric logic here is an explicit anti-goal (AC 6, AC 8).
- The **canonical finding schema** shape — field names including `source`, `stakes_class`, and dispositions — is owned by the `directed-fix-finding-schema` dependency. This adapter conforms to that shape; it does not extend it.

**The two-"dismiss" trap (AC 9, the one most likely to be mis-built):**

- bmad's `dismiss` bucket = bmad's own noise filter (false-positive / handled-elsewhere). Dropping it at the adapter is correct and required (AC 4). It never becomes a canonical finding.
- conduct's `dismissed` **disposition** = a *fixer-leg* outcome: a legitimate-looking finding the fixer chose not to act on, recorded with a REQUIRED non-empty rationale and rendered in the end-gate report (per DEC-036). It lives downstream, not in this adapter.
- The danger: an over-eager adapter that "dismisses" decision_needed/patch/defer findings on its own judgment would rob the fixer of findings it is supposed to see and dismiss-with-rationale, and would silently shrink the report's dismissal ledger. AC 10 forbids this — the adapter drops *only* bmad-layer noise.

**Stakes vocabulary used here (for the rubric call and the no-signal default):** stakes classes are security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; and default routine. Dispositions in the canonical schema are fixed | dismissed (required non-empty rationale) | triaged-out | escalated. Timing tiers (consumed downstream, not decided here) are end-gate-expanded (default) and the narrow mid-flight tier. This adapter only tags `stakes_class`; it does not assign dispositions or timing tiers.

**Why the stakes_class field matters downstream (context, not this story's job):** stakes class is the routing key DEC-036 uses to decide whether a finding stays on the always-silent routine auto-fix path or qualifies for the narrow, high-bar mid-flight escalation tier (irreversible-and-imminent OR build-invalidating only). If this adapter emitted findings without a stakes_class, that routing could not run and DEC-036's escalation tier would collapse. The adapter's sole obligation is to ensure the field is always populated via the rubric (AC 5, AC 7).

**Governing spec sections (cited by number from the authoring brief):** DEC-036 amendment D2 (populate stakes_class via the shared rubric; emit routine/null on no signal) and DEC-036 amendment D3 / its clarification (bmad `dismiss` dropped at the bmad layer is distinct from the fixer `dismissed` disposition). DEC-035 establishes the legible auto-fix loop and single end-gate that this finding stream feeds.

### References

- Epic: `momentum-sprint-orchestration` — see `_bmad-output/planning-artifacts/epics.json`.
- Decision: DEC-035 (adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND dismissed).
- Decision: DEC-036 (narrow, stakes-gated mid-flight escalation tier; report renders dismissals; routine findings always auto-fixed; anti-rubber-stamp end-gate) — amendments **D2** and **D3** are the binding amendments for this story.
- Dependency stories: `code-review-adapter-noninteractive-driver` (supplies the bmad triage output non-interactively), `directed-fix-finding-schema` (owns the canonical finding schema shape this adapter targets), `stakes-classification-rubric` (owns the shared classifier this adapter consumes).
