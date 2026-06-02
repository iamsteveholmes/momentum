---
title: "Code-review adapter: retire the in-house stub and repoint the command"
story_key: code-review-adapter-retire-stub
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - code-review-adapter-noninteractive-driver
  - code-review-adapter-normalize-triage
touches:
  - skills/momentum/skills/code-reviewer/SKILL.md
  - commands/code-reviewer.md
---

# Code-review adapter: retire the in-house stub and repoint the command

## Story

As the Conductor's build phase,
I want the in-house code-reviewer stub retired and the code-reviewer command repointed at the bmad-code-review adapter,
so that every code-review invocation in conduct produces real adapter-normalized findings instead of placeholder stub output, with a single reviewer of record.

## Description

The Conductor (the in-session, per-story, autonomous-build, single-end-gate rewrite of sprint-dev) drives code review through a code-reviewer command. Earlier in the conduct core-build sprint, two predecessor stories stood up the adapter that wraps `bmad-code-review`: one made it drive non-interactively, and the other normalized its triage output into the conduct finding shape (with dispositions and stakes classes). With those in place, the legacy in-house code-reviewer stub — which only ever emitted placeholder output, not genuine adversarial review findings — is now dead weight and a source of confusion: two things both claim to be "the reviewer."

This story removes that ambiguity. It deletes the in-house stub reviewer body (replacing the placeholder so it no longer behaves as a reviewer) and repoints the code-reviewer command shim so that invoking the command drives the `bmad-code-review` adapter end to end. After this change, there is exactly one reviewer of record, and its output is the adapter-normalized finding stream that the Conductor's auto-fix loop and end-gate already understand.

Pain context: while both the stub and the adapter coexist, any caller (and any reader of the practice) has to know which one is "real." The stub silently produces non-findings; if the command ever routed to it, the build phase would believe it had been reviewed when it had not. Retiring the stub closes that trap.

This is a pure plumbing change — deletion plus shim repoint. It does NOT introduce, alter, or interact with any of the DEC-036 escalation behavior: stakes classification, the mid-flight escalation tier, dismissal rationale rendering, and the anti-rubber-stamp end-gate are all owned by other conduct components and are unchanged by this story. What this story guarantees, in DEC-036 terms, is only that the findings flowing downstream to those components come from the adapter, not the stub.

Source decisions: DEC-035 (adopt conduct; single human end-gate; report organized by user-facing functionality; legible auto-fix loop) and DEC-036 (narrow stakes-gated mid-flight escalation tier; routine findings always auto-fixed; report renders dismissals; anti-rubber-stamp end-gate). Governing spec: section 4 ("Retire the stub") and section 12.

## Acceptance Criteria

1. The in-house code-reviewer stub no longer functions as a reviewer: its placeholder reviewer body has been removed or replaced, so invoking it directly does not produce review findings.
2. The code-reviewer command drives the `bmad-code-review` adapter when invoked — the command is repointed away from the in-house stub and onto the adapter.
3. Invoking the code-reviewer command produces adapter-normalized findings (findings carrying conduct's disposition and stakes-class shape), not the legacy placeholder stub output.
4. After this change there is exactly one reviewer of record reachable through the code-reviewer command: the adapter. No invocation path through the command reaches the retired stub body.
5. The findings produced through the repointed command are in the same normalized shape that downstream conduct components consume — each finding can carry a disposition (one of: fixed, dismissed, triaged-out, escalated) and a stakes class (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; or default routine). This story does not generate dispositions itself; it only ensures the command emits findings in that consumable shape.
6. This story does not add, remove, or alter any DEC-036 escalation behavior: it does not introduce stakes classification logic, does not introduce the mid-flight escalation tier, does not change dismissal-rationale rendering, and does not change the end-gate. Its only effect on DEC-036 behavior is that the finding stream now originates from the adapter rather than the stub. (UNCHANGED by DEC-036: this story is deletion + shim repoint only.)
7. Re-invoking the code-reviewer command on the same input is idempotent in behavior: it consistently routes to the adapter and never falls back to the retired stub.

## Tasks / Subtasks

- [ ] Remove the in-house stub reviewer body from `skills/momentum/skills/code-reviewer/SKILL.md` so it no longer behaves as a reviewer (replace the placeholder body; leave no live placeholder review path) (AC1, AC4)
- [ ] Repoint `commands/code-reviewer.md` so the command drives the `bmad-code-review` adapter rather than the in-house stub (AC2)
- [ ] Confirm the command's adapter routing depends on the two predecessor stories' work (non-interactive driver + normalized triage) and consumes their output shape (AC3, AC5)
- [ ] Verify that no invocation path through the command can reach the retired stub body (AC4, AC7)
- [ ] Verify the command, when invoked, returns adapter-normalized findings carrying the conduct disposition/stakes-class shape, not placeholder output (AC3, AC5)
- [ ] Confirm this change introduces no stakes-classification logic, no mid-flight tier, no dismissal-rendering change, and no end-gate change — it is plumbing only (AC6)
- [ ] Re-invoke the command on identical input and confirm it routes to the adapter both times with no stub fallback (AC7)

## Dev Notes

This is a skill-instruction change verified by skill-invoke. The two files touched are the in-house stub skill (`skills/momentum/skills/code-reviewer/SKILL.md`) and the command shim (`commands/code-reviewer.md`). The work is intentionally small: delete the stub's placeholder reviewer body and repoint the command at the adapter.

Dependency ordering matters. This story is `depends_on` two predecessors:
- `code-review-adapter-noninteractive-driver` — makes the `bmad-code-review` adapter run without interactive prompting, which is what lets the command drive it autonomously inside the Conductor's build phase.
- `code-review-adapter-normalize-triage` — normalizes the adapter's triage output into conduct's finding shape (dispositions: fixed | dismissed | triaged-out | escalated; stakes classes: security/auth-isolation, irreversible/destructive, high-blast-radius/architecture, default routine).

Because both are in place before this story runs, repointing the command yields findings that are already in the consumable normalized shape (AC3, AC5). This story adds no new normalization or classification of its own — it is purely deletion plus shim repoint.

DEC-036 scope guard: this story is explicitly UNCHANGED by DEC-036. DEC-036 amends DEC-035's single-gate model by permitting a narrow, high-bar, stakes-gated mid-flight escalation tier (irreversible-and-imminent OR build-invalidating ONLY), introduces the `escalated` disposition, requires the report to render dismissals (each with a non-empty rationale), and adds an anti-rubber-stamp end-gate. None of that machinery is created or modified here. The only DEC-036-relevant guarantee this story carries is provenance: downstream escalation/dismissal/end-gate components now receive their findings from the adapter rather than the retired stub (AC6). Do not add stakes-classification logic, the mid-flight tier, dismissal-rendering, or end-gate behavior in this story — those live in their own conduct components.

Governing spec sections (cited by number from the authoring brief; do not open the spec):
- Section 4 — "Retire the stub": the deletion of the in-house stub reviewer body and the rationale for a single reviewer of record.
- Section 12 — the command repoint onto the adapter.

Verification is black-box and behavioral: invoke the command, inspect that the findings returned are adapter-normalized (carry disposition/stakes-class shape) and not placeholder output; invoke the stub directly and confirm it no longer reviews; confirm no command path reaches the stub; confirm idempotent routing on repeated invocation.

### References

- Epic `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json`
- DEC-035 — adopt conduct; one human end-gate at the end; no story-count cap; report organized by user-facing functionality; legible auto-fix loop (`_bmad-output/planning-artifacts/decisions/`)
- DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 #1; routine findings always auto-fixed; report renders dismissals; anti-rubber-stamp end-gate (`_bmad-output/planning-artifacts/decisions/`)
- Governing spec sections 4 ("Retire the stub") and 12
