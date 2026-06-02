---
title: Shared single-source stakes-classification rubric
story_key: stakes-classification-rubric
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
  - skills/momentum/references/stakes-classification-rubric.md
---

# Shared single-source stakes-classification rubric

## Story

As a developer building conduct,
I want one shared, referenceable rubric that classifies every finding into a stakes class and a timing tier from a single source of truth,
so that the code-review adapter, qa-reviewer, and AVFL all tag findings consistently — instead of three divergent classifiers — and the narrow mid-flight escalation path stays anchored to one explicit, auditable definition.

## Description

`directed-fix-finding-schema` adds the `stakes_class` FIELD to the finding schema. This story authors the LOGIC that POPULATES that field: a shared, human-readable rubric document defining what marks a finding as each stakes class, how the timing tier is decided, and how routine findings fall through.

The rubric defines three things:

1. **Stakes classes** — concrete, recognizable signals/patterns that mark a finding as each of the three classes:
   - **security/auth-isolation** — authentication, authorization, secret handling, isolation-boundary, privilege, or access-control concerns.
   - **irreversible/destructive** — migrations, deletes, force-pushes, production deploys, and other operations that cannot be cheaply undone.
   - **high-blast-radius/architecture** — changes touching architecture-level structure, shared contracts, or surfaces whose failure radiates widely.
2. **Timing-tier decision rule** — when a stakes-class finding routes to the NARROW `mid-flight` tier versus the default `end-gate-expanded` tier. Mid-flight is permitted ONLY for findings that are irreversible-and-imminent OR build-invalidating. Everything else (including most stakes-class findings) waits for the expanded end-gate. This bar is biased narrow on purpose: the end-gate-expanded tier is the safety net, and the mid-flight bar must never widen.
3. **Routine fall-through** — any finding that matches none of the three stakes-class signals is `routine` and stays on the always-on, silent auto-fix path.

**Why now / pain context.** Three legs of the build pipeline (the code-review adapter, the fixer, the qa-reviewer) each independently proposed a near-identical classifier. That is one shared rubric consumed by N producers, NOT three units of work. AES-004 Finding 2 grades the stakes heuristic itself as "missing/unwired — no heuristic flags high-risk." This story closes that gap by authoring the heuristic ONCE. Producers then receive only small emission-wiring touches in their own stories (the adapter sets the class from bmad-code-review prose; qa-reviewer from AC/diff signal; AVFL on integration findings) — they reference this rubric rather than re-deriving classification.

**Source decisions.** DEC-035 establishes the always-on silent auto-fix path with a single human end-gate and no story-count cap. DEC-036 narrowly amends DEC-035 binding decision #1 to permit a high-bar, stakes-gated mid-flight escalation tier: stakes-class findings leave the silent auto-fix path, the report renders dismissals with rationale, and the end-gate is anti-rubber-stamp. Routine findings stay ALWAYS auto-fixed. This rubric is the single definition those mechanisms depend on. (See also AES-004 Finding 2; impact brief `.momentum/handoffs/conduct-dec036-impact-brief-2026-06-01.md` §3 — the de-dup note that collapsed three proposed classifiers into one.)

## Acceptance Criteria

1. A single rubric artifact exists at `skills/momentum/references/stakes-classification-rubric.md`. It is the only place the stakes-classification logic is defined; it is written to be referenced by other producers rather than copied.

2. The rubric names exactly three stakes classes — security/auth-isolation, irreversible/destructive, and high-blast-radius/architecture — plus one routine fall-through, and states that these four together are exhaustive (every finding lands in exactly one).

3. For the **security/auth-isolation** class, the rubric lists concrete, recognizable signals a producer can match against — e.g., authentication, authorization, secret/credential handling, isolation- or tenancy-boundary, privilege escalation, and access-control concerns.

4. For the **irreversible/destructive** class, the rubric lists concrete signals — explicitly naming database migrations, deletes, force-pushes, and production deploys as exemplars — describing them as operations that cannot be cheaply or safely undone.

5. For the **high-blast-radius/architecture** class, the rubric lists concrete signals — e.g., changes to architecture-level structure, shared/cross-cutting contracts or interfaces, and surfaces whose failure radiates widely across the system.

6. The rubric states the **routine fall-through rule**: any finding that matches none of the three stakes-class signals is classified `routine`, and routine findings stay on the always-on, silent auto-fix path (never escalated).

7. The rubric states the **timing-tier decision rule** with two tiers: `end-gate-expanded` (the default) and `mid-flight` (narrow).

8. The rubric states that a finding routes to the **`mid-flight`** tier ONLY when it is irreversible-and-imminent OR build-invalidating, and that ALL other findings — including stakes-class findings that fail this test — default to `end-gate-expanded`. The rubric explicitly instructs the reader to bias narrow when in doubt.

9. The rubric explicitly states that the `mid-flight` bar must never be widened beyond irreversible-and-imminent / build-invalidating, and names the `end-gate-expanded` tier as the safety net that catches everything the mid-flight tier deliberately excludes.

10. The rubric states that it is the single source consumed by every producer (the code-review adapter, qa-reviewer, and AVFL), and that those producers carry only emission-wiring that references this rubric — they do not define their own classification logic.

11. The rubric's classification output is expressed in terms compatible with the finding schema's `stakes_class` field and the timing tiers (`end-gate-expanded`, `mid-flight`) so that a producer can populate the schema directly from the rubric without translation.

## Tasks / Subtasks

- [ ] Create the rubric artifact at `skills/momentum/references/stakes-classification-rubric.md` with a clear title and a one-paragraph statement of purpose (single source consumed by all producers).
- [ ] Author the **stakes-classes** section:
  - [ ] Define the security/auth-isolation class with its concrete signal list.
  - [ ] Define the irreversible/destructive class with its concrete signal list (naming migration, delete, force-push, prod deploy as exemplars).
  - [ ] Define the high-blast-radius/architecture class with its concrete signal list.
  - [ ] State that the three classes plus routine are exhaustive and mutually exclusive at the disposition level (every finding lands in exactly one class).
- [ ] Author the **routine fall-through** rule: no-match ⇒ `routine` ⇒ stays on the always-on silent auto-fix path.
- [ ] Author the **timing-tier decision rule**:
  - [ ] Name the two tiers: `end-gate-expanded` (default) and `mid-flight` (narrow).
  - [ ] State the narrow mid-flight test: irreversible-and-imminent OR build-invalidating ONLY.
  - [ ] State the default: everything else, including stakes-class findings that fail the mid-flight test, routes to `end-gate-expanded`.
  - [ ] Add the explicit "bias narrow / never widen" guardrail naming end-gate-expanded as the safety net.
- [ ] Add a **consumption** note: how each producer (code-review adapter, qa-reviewer, AVFL) references this rubric via small emission-wiring, and that they MUST NOT fork their own classifier.
- [ ] Align the rubric's output vocabulary with the `stakes_class` field and timing-tier values defined by `directed-fix-finding-schema` so producers can populate the schema directly.
- [ ] Self-check the rubric against every acceptance criterion before signaling done.

## Dev Notes

This is a `specification` change_type verified by `document-review` — the deliverable is the rubric document itself, evaluated by reading it. No executable behavior is added by this story; the populating producers are wired in their own stories.

**Relationship to the schema dependency.** `directed-fix-finding-schema` (this story's `depends_on`) is the structural half — it adds the `stakes_class` field and the disposition/timing-tier vocabulary to the finding schema. This story is the semantic half — it authors the logic that decides WHICH value goes in that field. Keep the rubric's output vocabulary identical to the schema's so a producer can copy the rubric's verdict straight into the field. The shared disposition vocabulary the rubric must stay compatible with is: `fixed | dismissed (required non-empty rationale) | triaged-out | escalated`; the timing tiers are `end-gate-expanded (default) | mid-flight (narrow)`.

**Governing spec sections (cited by number from the conduct brief; do not open the spec):**
- §1 (DEC-035) — always-on silent auto-fix path, single human end-gate, no story-count cap, report organized by user-facing functionality, legible auto-fix loop (what it changed AND dismissed).
- §2 (DEC-036) — narrow, high-bar, stakes-gated mid-flight escalation tier; stakes-class findings leave the silent path; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved (only the absolutism relaxed).
- The DEC-036 mid-flight bar definition: irreversible-and-imminent OR build-invalidating ONLY — bias narrow, never widen; end-gate-expanded is the safety net.

**Deep-review heuristic (not an AC in this story — forward note only).** DEC-036's stakes classes ARE the long-missing `review_depth: deep` heuristic referenced as the conduct spec's open question 5. The intent is that deep-review opt-in should LATER become an OUTPUT of this rubric (a finding's stakes class drives whether deep review is warranted), rather than a hand-set flag. This story does not implement that wiring; it only establishes the rubric the future heuristic will read from. Capturing it here so a downstream story can pick it up.

**Single-source discipline.** The whole point of this story is to prevent three divergent classifiers. The rubric must be written as a reference document, and the producer stories must wire emission to it — reviewers should be able to confirm by reading the rubric that it claims sole ownership of classification logic and that producers are expected to reference, not re-derive.

### References

- Epic `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json`.
- DEC-035 — adopt conduct; one human gate at the end; no story-count cap; report organized by user-facing functionality; legible auto-fix loop.
- DEC-036 — narrow, stakes-gated mid-flight escalation tier amending DEC-035 binding decision #1; dispositions include `escalated`; report renders dismissals; anti-rubber-stamp end-gate; routine stays always auto-fixed. `_bmad-output/planning-artifacts/decisions/`.
- AES-004 Finding 2 — stakes heuristic "missing/unwired — no heuristic flags high-risk." `_bmad-output/planning-artifacts/assessments/`.
- Impact brief — `.momentum/handoffs/conduct-dec036-impact-brief-2026-06-01.md` §3 (de-dup note: three proposed classifiers collapsed into one shared rubric).
